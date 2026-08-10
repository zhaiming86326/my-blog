"""mitmproxy 抓包插件:记录 AI 服务的对话请求/响应到 SQLite。

原则:
- 只记录 POST 请求的对话文本(prompt)与响应文本(response)
- 绝不落库 headers / cookies / API keys —— 脱敏发生在提取阶段
- 不修改任何流量,插件只读,代理照常转发
- 任何异常都不允许影响代理本身

启动: mitmdump -s addon.py -p 8080
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from mitmproxy import http

# addon.py 会被 mitmdump -s 作为顶层脚本加载,相对导入会失败;
# 把 scripts/ 注入 sys.path 后用绝对导入。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture.db import DATA_DIR, insert_conversation, init_db  # noqa: E402

# 设 CAPTURE_DEBUG_SSE=1 时把 SSE 载荷结构写入 .capture/sse_debug.log,用于排查格式
DEBUG_SSE = os.environ.get("CAPTURE_DEBUG_SSE") == "1"
DEBUG_SSE_LOG = DATA_DIR / "sse_debug.log"
# 设 CAPTURE_DEBUG_FILTER=1 时记录被过滤的请求与 WebSocket 活动,用于诊断漏抓
DEBUG_FILTER = os.environ.get("CAPTURE_DEBUG_FILTER") == "1"
DEBUG_FILTER_LOG = DATA_DIR / "filter_debug.log"

log = logging.getLogger("ai-capture")

# 域名 -> provider 名(支持子域名匹配,如 ai.chatgpt.com)
HOST_PROVIDERS = {
    "api.deepseek.com": "deepseek-api",   # DeepSeek API
    "chat.deepseek.com": "deepseek",      # DeepSeek 网页
    "chatgpt.com": "chatgpt",
    "chat.openai.com": "chatgpt",
    "grok.com": "grok",
    "api.x.ai": "grok-api",               # xAI API
}

# 提取时视为敏感的字段名(递归脱敏,防止 API key 混入 body 落库)
SENSITIVE_KEYS = {
    "api_key", "apikey", "x-api-key", "x-api-key",
    "authorization", "access_token", "token", "secret",
    "client_secret", "password", "cookie", "session_id",
    "sessionid", "key",
}

MAX_PROMPT_CHARS = 40_000        # prompt 过长截断
MAX_RESPONSE_CHARS = 400_000     # response 过长截断
MAX_BODY_BYTES = 2 * 1024 * 1024 # 超过 2MB 的请求体(如图片上传)跳过

# AI 回复里的引用标注,如 [citation:2],对知识库无意义,统一剥掉
CITATION_RE = re.compile(r"\[citation:\d+\]")


def _strip_citations(text: str) -> str:
    return CITATION_RE.sub("", text).strip()


def provider_for(host: str) -> str | None:
    host = (host or "").lower()
    for domain, provider in HOST_PROVIDERS.items():
        if host == domain or host.endswith("." + domain):
            return provider
    return None


# ---------------------------------------------------------------- 脱敏

def _is_sensitive_key(key: str) -> bool:
    k = str(key).lower().replace(" ", "_")
    return any(s in k for s in SENSITIVE_KEYS)


def redact(obj):
    """递归把敏感字段的值替换为 [REDACTED],返回新对象,不修改原对象。"""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k] = "[REDACTED]" if _is_sensitive_key(k) else redact(v)
        return out
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


# ---------------------------------------------------------------- 文本提取

def _iter_texts(obj):
    """递归产出对话正文文本(只认 text / content / parts 键,过滤 id/metadata 噪音)。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "parts" and isinstance(v, list):
                for item in v:
                    if isinstance(item, str):
                        if item.strip():
                            yield item
                    else:
                        yield from _iter_texts(item)
            elif k in ("text", "content") and isinstance(v, str):
                if v.strip():
                    yield v
            else:
                yield from _iter_texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _iter_texts(v)


def _find_messages(obj):
    """递归找第一个 messages 数组(网页版与 API 版通用的对话载体)。"""
    if isinstance(obj, dict):
        if isinstance(obj.get("messages"), list):
            return obj["messages"]
        for v in obj.values():
            r = _find_messages(v)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_messages(v)
            if r is not None:
                return r
    return None


def _find_model(obj) -> str | None:
    if isinstance(obj, dict):
        m = obj.get("model")
        if isinstance(m, str) and m:
            return m
        for v in obj.values():
            r = _find_model(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_model(v)
            if r:
                return r
    return None


def _message_text(m: dict) -> str:
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        parts = c.get("parts")
        if isinstance(parts, list):
            return "\n".join(p for p in parts if isinstance(p, str))
        return ""
    if isinstance(c, list):
        return "\n".join(str(x) for x in c if isinstance(x, str))
    return ""


def extract_request(body: bytes) -> tuple[str, str | None, bool]:
    """从请求体提取 (prompt, model, truncated)。fallback:脱敏后的原文截断。"""
    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:
        return "", None, False

    obj = None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        pass

    if isinstance(obj, dict):
        msgs = _find_messages(obj)
        if msgs:
            lines = []
            for m in msgs:
                if not isinstance(m, dict):
                    continue
                role = m.get("role")
                author = m.get("author")
                if not role and isinstance(author, dict):
                    role = author.get("role")
                txt = _message_text(m).strip()
                if txt:
                    lines.append(f"{role or '?'}: {txt}")
            if lines:
                prompt = "\n\n".join(lines)
                if len(prompt) > MAX_PROMPT_CHARS:
                    return prompt[:MAX_PROMPT_CHARS], _find_model(obj), True
                return prompt, _find_model(obj), False
        # ChatGPT 新版用单数 "message" 字段(如 {"action":"next", "message": {...}})
        if isinstance(obj.get("message"), dict):
            m = obj["message"]
            txt = _message_text(m)
            if txt.strip():
                role = m.get("role")
                author = m.get("author")
                if not role and isinstance(author, dict):
                    role = author.get("role")
                return f"{role or 'user'}: {txt.strip()}", _find_model(obj), False
        # 无 messages 数组:合并 system + 单轮对话字段(DeepSeek 网页版 prompt / Responses API input)
        parts: list[str] = []
        sys_prompt = obj.get("system")
        if isinstance(sys_prompt, list) and sys_prompt:
            sys_texts = list(_iter_texts(sys_prompt))
            if sys_texts:
                parts.append("system: " + "\n".join(sys_texts))
        for key in ("prompt", "input", "query"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                parts.append(f"{key}: {v.strip()}")
                break
            if isinstance(v, (dict, list)):
                texts = list(_iter_texts(v))
                if texts:
                    parts.append(f"{key}: " + "\n".join(texts))
                    break
        if parts:
            joined = "\n\n".join(parts)
            return joined[:MAX_PROMPT_CHARS], _find_model(obj), len(joined) > MAX_PROMPT_CHARS
        # 兜底:落库脱敏后的完整 JSON
        safe = json.dumps(redact(obj), ensure_ascii=False)
        truncated = len(safe) > MAX_PROMPT_CHARS
        return safe[:MAX_PROMPT_CHARS], _find_model(obj), truncated

    truncated = len(text) > MAX_PROMPT_CHARS
    return text[:MAX_PROMPT_CHARS], None, truncated


def extract_response(content: bytes) -> tuple[str, bool]:
    """从响应体提取 response 文本。兼容 JSON、SSE(data: 行)、纯文本。"""
    try:
        text = content.decode("utf-8", errors="replace")
    except Exception:
        return "", False

    if "data:" in text:  # SSE 流式
        objs: list = []
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            payload = line[len("data:"):].strip()
            if not payload or payload == "[DONE]":
                continue
            try:
                objs.append(json.loads(payload))
            except json.JSONDecodeError:
                continue

        # 协议识别:
        #  - Anthropic 风格(DeepSeek API): type=content_block_delta,
        #    delta.text(正文)/delta.thinking(思考),增量 token,需无缝拼接
        #  - OpenAI 风格: choices[].delta.content,增量 token,无缝拼接
        #  - DeepSeek 网页版 JSON-Patch: {"o":"APPEND","v":"..."} 或 {"v":"..."},
        #    文本增量在 v 字段,需无缝拼接(状态字段如 BATCH/FINISHED 需忽略)
        #  - 块状(其他网页版完整消息):载荷间用空行分隔
        anthropic = any(
            isinstance(o, dict) and o.get("type") in (
                "content_block_delta", "content_block_start", "message_start", "message_stop",
            )
            for o in objs
        )
        openai = any(
            isinstance(o, dict)
            and isinstance(o.get("choices"), list)
            and any(isinstance(c, dict) and "delta" in c for c in o["choices"])
            for o in objs
        )
        patch_style = any(
            isinstance(o, dict)
            and (
                o.get("o") == "APPEND"
                or (isinstance(o.get("v"), str) and "p" not in o and "o" not in o)
            )
            for o in objs
        )

        if anthropic:
            text_parts: list[str] = []
            thinking_parts: list[str] = []
            for o in objs:
                d = o.get("delta") if isinstance(o, dict) else None
                if not isinstance(d, dict):
                    continue
                if d.get("type") == "text_delta" and isinstance(d.get("text"), str):
                    text_parts.append(d["text"])
                elif d.get("type") == "thinking_delta" and isinstance(d.get("thinking"), str):
                    thinking_parts.append(d["thinking"])
            joined = "".join(text_parts)
            if thinking_parts:
                thinking = "".join(thinking_parts)
                head = f"【思考】\n{thinking}"
                joined = f"{head}\n\n【回答】\n{joined}" if joined else head
        elif patch_style:
            # 只拼 APPEND 操作或纯增量载荷(仅含 v)的文本;
            # SET/BATCH 状态载荷(p 或 o 存在且非 APPEND)不提取,避免 FINISHED 等拼入
            joined = "".join(
                o["v"] for o in objs
                if isinstance(o.get("v"), str)
                and (o.get("o") == "APPEND" or ("p" not in o and "o" not in o))
            )
        elif openai:
            joined = "".join("".join(_iter_texts(o)) for o in objs)
        else:
            joined = "\n\n".join("\n".join(_iter_texts(o)) for o in objs)

        if DEBUG_SSE:
            with open(DEBUG_SSE_LOG, "a", encoding="utf-8") as f:
                f.write(f"\n=== SSE @ {datetime.now(timezone.utc).isoformat()} ===\n")
                for i, o in enumerate(objs):
                    texts = list(_iter_texts(o))
                    f.write(f"payload#{i}: {json.dumps(o, ensure_ascii=False)[:400]}\n")
                    f.write(f"  -> texts: {texts[:5]!r}\n")
                f.write(f"  => joined({len(objs)} payloads): {joined[:300]!r}\n")
        return joined[:MAX_RESPONSE_CHARS], len(joined) > MAX_RESPONSE_CHARS

    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return text, len(text) > MAX_RESPONSE_CHARS  # 纯文本原样

    out = list(_iter_texts(obj))
    if not out:
        return text[:MAX_RESPONSE_CHARS], len(text) > MAX_RESPONSE_CHARS

    joined = "\n".join(out)
    return joined[:MAX_RESPONSE_CHARS], len(joined) > MAX_RESPONSE_CHARS


# ---------------------------------------------------------------- 插件主体

def _is_conversation_request(provider: str, path: str, body: bytes) -> bool:
    """过滤掉非对话请求(页面初始化 / 遥测埋点 / 反爬探测 / 二进制等噪音)。

    provider 特化:只保留真正发送对话消息的接口。
    """
    path = path.rstrip("/")
    text = ""
    if body:
        try:
            text = body.decode("utf-8", errors="ignore")
        except Exception:
            pass

    # ---- 通用规则 ----
    # 二进制 body(protobuf 等)跳过
    if body and any(b in body for b in (b"\x00", b"\x01", b"\x08", b"\x0b")):
        return False
    # urlencoded 埋点(data=...)跳过
    if body and body.startswith(b"data="):
        return False

    if provider == "deepseek":
        # 网页版只有 /api/v0/chat/completion 是真正的对话接口
        return path.endswith("/api/v0/chat/completion")

    if provider == "chatgpt":
        # 只记录对话接口 /backend-api/conversation,且必须包含用户消息
        if not path.endswith("/backend-api/conversation"):
            return False
        if '"prepare_token"' in text or '"proofofwork"' in text or '"obi"' in text:
            return False
        # 预检请求(action=next 不带 message)跳过,真正对话必含 message/messages
        if '"message"' not in text and '"messages"' not in text:
            return False
        return True

    if provider == "grok":
        # 跳过页面初始化 / 遥测 / 限额查询 / 历史对话拉取
        if not text.strip() or text.strip() in ("{}", "[]"):
            return False
        if "load-responses" in path or "loadResponses" in path:
            return False
        for noise in (
            '"locale"', '"modelName"', '"pageSize"', '"refreshToken"',
            "botox", "pressure_observer", "bing_worker", "citation_view",
            "client_fetch_success", "send_query", "auth_session_refetch",
            '"event"',
        ):
            if noise in text:
                return False
        # 只保留对话/聊天相关路径
        return any(k in path for k in ("app-chat", "conversation", "completion", "/chat"))

    return True


class AICapture:
    def __init__(self):
        self._ws: dict = {}  # flow.id -> {"provider","prompt","response","ts"}

    def request(self, flow: http.HTTPFlow) -> None:
        try:
            if flow.request.method != "POST":
                return
            provider = provider_for(flow.request.host)
            if provider is None:
                # 兼容 reverse 代理等场景:URL host 是 IP,但 Host 头带着目标域名
                provider = provider_for(flow.request.headers.get("Host", "").split(":")[0])
            if provider is None:
                return
            if not _is_conversation_request(provider, flow.request.path, flow.request.content or b""):
                if DEBUG_FILTER:
                    with open(DEBUG_FILTER_LOG, "a", encoding="utf-8") as f:
                        body = (flow.request.content or b"")[:400]
                        f.write(f"[{datetime.now(timezone.utc).isoformat()}] REJECT {provider} "
                                f"{flow.request.method} {flow.request.path} body={body!r}\n")
                return
            flow.metadata["ai_provider"] = provider
            flow.metadata["ai_path"] = flow.request.path
        except Exception:
            log.exception("request hook failed")

    def websocket_message(self, flow: http.HTTPFlow) -> None:
        """提取 WebSocket 对话(ChatGPT/Grok 新版都用 ws 传输对话内容)。"""
        try:
            provider = provider_for(flow.request.host)
            if provider is None:
                return
            msg = flow.websocket.messages[-1]
            content = msg.content or b""

            if DEBUG_FILTER:
                with open(DEBUG_FILTER_LOG, "a", encoding="utf-8") as f:
                    snippet = content[:300]
                    if b"response.chunk" in content[:150]:
                        snippet = content  # chunk 消息完整记录, 便于分析 step_id
                    f.write(f"[{datetime.now(timezone.utc).isoformat()}] WS {provider} "
                            f"{flow.request.path} {'C->S' if msg.from_client else 'S->C'} "
                            f"len={len(content)} content={snippet!r}\n")

            try:
                obj = json.loads(content.decode("utf-8"))
            except Exception:
                return
            ev = obj.get("event") if isinstance(obj, dict) else None
            etype = (ev or {}).get("type") if isinstance(ev, dict) else None

            buf = self._ws.setdefault(flow.id, {
                "provider": provider,
                "prompt": [],
                "response": [],  # [(step_id, text), ...]
                "ts": datetime.now(timezone.utc),
            })

            if provider == "grok":
                if msg.from_client:
                    if etype == "conversation.item.create":
                        text = self._grok_input_text(ev)
                        if text:
                            buf["prompt"].append("user: " + text)
                else:
                    if etype == "response.chunk":
                        chunk = ev.get("chunk") or {}
                        t = (chunk.get("text") or {}).get("text")
                        if isinstance(t, str) and t:
                            step = (chunk.get("metadata") or {}).get("step_id", 0)
                            buf["response"].append((step, t))
                    elif etype == "response.done":
                        self._flush_ws(flow.id, buf)
        except Exception:
            log.exception("websocket_message failed")

    def websocket_end(self, flow: http.HTTPFlow) -> None:
        """连接关闭时兜底落库(防止 response.done 未触发)。"""
        buf = self._ws.pop(flow.id, None)
        if buf:
            self._flush_ws(flow.id, buf)

    @staticmethod
    def _grok_input_text(ev) -> str:
        item = ev.get("item") or {}
        for c in (item.get("x_grok") or {}).get("input_chunks") or []:
            t = ((c.get("text") or {}).get("text"))
            if isinstance(t, str) and t:
                return t
        for c in item.get("content") or []:
            if isinstance(c, dict) and isinstance(c.get("text"), str) and c["text"]:
                return c["text"]
        return ""

    def _flush_ws(self, flow_id, buf: dict) -> None:
        try:
            prompt = "\n\n".join(p for p in buf["prompt"] if p)
            # 按 step_id 分组拼接(诊断阶段:保留 step 标记, 用于确认 thinking/回答语义)
            groups: dict = {}
            for step, text in buf["response"]:
                groups.setdefault(step, []).append(text)
            if groups:
                parts = [f"[step{step}]\n" + "".join(texts) for step, texts in sorted(groups.items())]
                response = "\n\n".join(parts)
            else:
                response = ""
            prompt = _strip_citations(prompt)
            response = _strip_citations(response)
            if prompt.strip() or response.strip():
                insert_conversation(
                    ts=buf["ts"],
                    provider=buf["provider"],
                    model=None,
                    path="/ws",
                    prompt=prompt.strip(),
                    response=response.strip(),
                    truncated=len(response) > MAX_RESPONSE_CHARS,
                )
        except Exception:
            log.exception("ws flush failed")
        finally:
            self._ws.pop(flow_id, None)

    def response(self, flow: http.HTTPFlow) -> None:
        provider = flow.metadata.get("ai_provider")
        if provider is None:
            return
        try:
            if not flow.response or not flow.response.content:
                return
            if len(flow.request.content or b"") > MAX_BODY_BYTES:
                return  # 大概率是图片/文件上传,跳过

            prompt, model, p_trunc = extract_request(flow.request.content or b"")
            resp_text, r_trunc = extract_response(flow.response.content)
            prompt = _strip_citations(prompt)
            resp_text = _strip_citations(resp_text)
            if not prompt.strip() and not resp_text.strip():
                return

            insert_conversation(
                ts=datetime.now(timezone.utc),
                provider=provider,
                model=model,
                path=flow.metadata.get("ai_path"),
                prompt=prompt.strip(),
                response=resp_text.strip(),
                truncated=p_trunc or r_trunc,
            )
        except Exception:
            log.exception("response hook failed")


addons = [AICapture()]


def load(l):
    init_db()
