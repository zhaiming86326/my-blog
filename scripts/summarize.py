"""每日 AI 对话总结脚本:提炼知识库并发布到博客。

流程:
1. 从 .capture/capture.db 读取指定日期(默认昨天)的对话记录
2. 过滤噪音(空响应 / 错误响应 / 无实质内容的调用)
3. 调用本机 Ollama(qwen2.5:7b-instruct)逐条提炼知识卡片
4. 生成 Hugo 博文 content/posts/YYYY-MM-DD-ai-knowledge.md
5. git add/commit/push → 触发 GitHub Actions 自动部署到 Cloudflare

用法:
    python scripts/summarize.py [YYYY-MM-DD] [--dry-run]
示例:
    python scripts/summarize.py             # 总结昨天
    python scripts/summarize.py 2026-08-09
    python scripts/summarize.py --dry-run   # 只生成 md,不 git push
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from capture.db import DATA_DIR, query_by_day  # noqa: E402

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
# 默认 7b(速度/质量平衡, 几分钟/次); 想用 14b 提质: 设环境变量 OLLAMA_MODEL=qwen2.5:14b-instruct
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b-instruct")
# stream=False 时 Ollama 生成完毕才返回数据, 期间 socket 无数据可读,
# 超时按"生成总时长"计算; 7b 一般 10-20 token/s, 单批最多几分钟, 留足余量
TIME_OUT = 1800  # 秒

# 单次送模型的输入字符上限: 一天可能数百条对话, 全部塞进一次调用会超过
# qwen2.5 默认 num_ctx=32768(约 2 字符/token), 模型只会看到输入尾部 -> 总结失真。
# 超过则自动分批总结再合并。
CHUNK_CHARS = 40_000

# 明显是噪音/错误的响应特征(截断匹配)
NOISE_RESPONSE_MARKERS = (
    "WWW-Authenticate header missing",
    "Connection error",
    "client does not trust",
    '"error"',
    "Authentication Fails",
)


def _detect_source(row: dict) -> str:
    """根据请求内容特征推断来源应用(IDE/插件)。"""
    if row.get("provider") == "deepseek-harness":
        return "DeepSeek Harness"
    if row.get("provider") in ("local-continue", "local-roo", "local-reasonix"):
        return {
            "local-continue": "Continue (本地)",
            "local-roo": "Roo Code (本地)",
            "local-reasonix": "Reasonix (本地)",
        }[row["provider"]]
    prompt = row.get("prompt") or ""
    path = row.get("path") or ""
    markers = [
        ("Reasonix", "You are Reasonix"),
        ("VSCode Roo", "You are Roo"),
        ("IDEA ProxyAI", "ProxyAI Agent"),
    ]
    for name, marker in markers:
        if marker in prompt:
            return name
    if path and "/api/v0/chat/completion" in path:
        return "DeepSeek 网页"
    if path and "chat/completions" in path:
        return "DeepSeek API"
    return "DeepSeek API"


# Markdown 围栏代码块: ```lang\n...```
CODE_FENCE_RE = re.compile(r"```([\w+#-]*)\n(.*?)```", re.DOTALL)
MAX_CODE_BLOCKS = 10     # 日报最多展示的代码片段数
MAX_CODE_LINES = 200     # 每个片段最多行数

# 敏感信息脱敏(发布前强制兜底, 不依赖总结模型)
SENSITIVE_PATTERNS = [
    # API 密钥: sk-xxxx / AKIA... / ghp_... (github) 等
    (re.compile(r"\b(sk-[A-Za-z0-9_-]{12,})\b"), "sk-[已脱敏]"),
    (re.compile(r"\b(AKIA[0-9A-Z]{16})\b"), "AKIA[已脱敏]"),
    (re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,})\b"), "gh[已脱敏]"),
    (re.compile(r"\b(xox[baprs]-[A-Za-z0-9-]{10,})\b"), "xox[已脱敏]"),
    # 私有密钥块
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
     "-----BEGIN PRIVATE KEY-----[已脱敏]-----END PRIVATE KEY-----"),
    # 赋值形式的凭据: password= / api_key: / token = 等
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|client[_-]?secret|token|bearer)\b\s*[=:]\s*['\"]?[^\s'\"&;]{6,}"),
     lambda m: m.group(1) + "=[已脱敏]"),
    # 数据库/服务连接串 user:pass@
    (re.compile(r"([a-z][a-z0-9+.-]*://[^/\s:@]+):([^@/\s]+)@"), r"\1:[已脱敏]@"),
    # 邮箱
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]{2,}\b"), "[邮箱已脱敏]"),
    # 中国大陆手机号
    (re.compile(r"\b1[3-9]\d{9}\b"), "[手机号已脱敏]"),
    # 身份证
    (re.compile(r"\b\d{17}[\dXx]\b"), "[身份证已脱敏]"),
]


def _redact_sensitive(text: str) -> str:
    """对文本做敏感信息强制脱敏(正则兜底)。"""
    for pat, repl in SENSITIVE_PATTERNS:
        text = pat.sub(repl, text)
    return text


def _extract_code_blocks(text: str) -> list[tuple[str, str]]:
    """从文本中提取围栏代码块,返回 [(lang, code)]。"""
    out = []
    for m in CODE_FENCE_RE.finditer(text):
        lang = (m.group(1) or "").strip()
        code = m.group(2).rstrip()
        if not code.strip():
            continue
        lines = code.splitlines()
        if len(lines) > MAX_CODE_LINES:
            code = "\n".join(lines[:MAX_CODE_LINES]) + "\n…(截断)"
        out.append((lang, code))
    return out


def _dedup_blocks(blocks: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen = set()
    out = []
    for lang, code in blocks:
        code = _redact_sensitive(code)  # 代码块强制脱敏
        key = code[:200]
        if key in seen:
            continue
        seen.add(key)
        out.append((lang, code))
        if len(out) >= MAX_CODE_BLOCKS:
            break
    return out


def _is_worth_keeping(row: dict) -> bool:
    """过滤噪音:空响应、错误响应、无实质用户消息的调用。"""
    prompt = (row.get("prompt") or "").strip()
    resp = (row.get("response") or "").strip()
    if not resp:
        return False
    if len(resp) < 3:
        return False
    if any(m in resp for m in NOISE_RESPONSE_MARKERS):
        return False
    # 新格式(addon 改造后): prompt 本身就是用户本轮输入, 无 role 前缀;
    # 旧数据: 可能带 system:/user: 前缀。只过滤纯 system 提示词调用(无任何用户侧内容)
    p = prompt[:4000]
    if "system: You are" in p and not re.search(r"user:|prompt:|输入:|用户", p):
        return False
    return True


def _truncate(text: str, limit: int = 1500) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n…(截断)"


# ---------------------------------------------------------------- DeepSeek Harness 会话日志源
# harness(Node) 不走系统代理, mitmproxy 抓不到, 日报需直接解析其会话日志。
# 日志位置: <DSH_HOME>/sessions/<workspace>/<session-id>/session.jsonl[.zstd]
HARNESS_SESSIONS_ROOT = Path(os.environ.get("DSH_HOME", str(Path.home() / ".dsh"))) / "sessions"

# 日志里非用户真实输入的消息块(截断匹配), 提取 prompt 时剔除
HARNESS_INJECT_MARKERS = (
    "<system-reminder>",
    "<interrupted-turn-recovery>",
    "<background-jobs>",
    "Current runtime context",
    "<reasoning-language>",
    "<execution-policy>",
)

HARNESS_MAX_RESPONSE_CHARS = 400_000


def _harness_log_paths() -> list[Path]:
    """枚举 <DSH_HOME>/sessions 下的会话日志(压缩/未压缩)。"""
    if not HARNESS_SESSIONS_ROOT.is_dir():
        return []
    return sorted(HARNESS_SESSIONS_ROOT.glob("*/*/session.jsonl*"))


def _parse_harness_log(path: Path, day: str) -> list[dict]:
    """把一个 harness 会话日志按 turn 整理成与 capture 同结构的记录。

    只收根会话(delegationDepth=0)、以 completed 结束的 turn; 每轮取第一条
    真实用户消息为 prompt, 拼接该 turn 全部 assistant text 为 response,
    丢弃 reasoning/tool-call 等非正文内容。
    """
    raw = path.read_bytes()
    if path.suffix == ".zstd":
        import io
        import zstandard
        raw = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(raw)).read()
    lines = raw.decode("utf-8", errors="replace").splitlines()

    header = None
    events = []
    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "session":
            header = obj
        else:
            events.append(obj)

    # 只收根会话: 子代理(delegationDepth>0)会重复父会话内容
    if header is None or (header.get("delegationDepth") or 0) > 0:
        return []

    turns: dict[int, dict] = {}
    order: list[int] = []
    cur_turn: int | None = None
    for ev in events:
        t = ev.get("type")
        data = ev.get("data") or {}
        # user/message 等事件自身不带 turn 字段, 用当前 turn 推断
        turn = data.get("turn") if data.get("turn") is not None else cur_turn
        if t == "turn/start":
            cur_turn = turn
            if turn is not None and turn not in turns:
                turns[turn] = {"prompt": None, "texts": [], "ok": False, "time": ev.get("time")}
                order.append(turn)
        elif t == "user/message":
            if turn is None or turn not in turns:
                continue
            if (data.get("source") or {}).get("kind") != "user":
                continue
            texts = [c.get("text", "") for c in data.get("content") or []
                     if isinstance(c, dict) and c.get("type") == "text"]
            prompt = "\n".join(texts).strip()
            if not prompt or any(m in prompt for m in HARNESS_INJECT_MARKERS):
                continue
            if turns[turn]["prompt"] is None:
                turns[turn]["prompt"] = prompt
                if turns[turn]["time"] is None:
                    turns[turn]["time"] = ev.get("time")
        elif t == "assistant/message":
            if turn is None or turn not in turns:
                continue
            for c in (data.get("message") or {}).get("content") or []:
                if (isinstance(c, dict) and c.get("type") == "text"
                        and isinstance(c.get("text"), str) and c["text"].strip()):
                    turns[turn]["texts"].append(c["text"])
        elif t == "turn/end":
            if turn is None or turn not in turns:
                continue
            if (data.get("reason") or {}).get("kind") == "completed":
                turns[turn]["ok"] = True

    out = []
    for turn in order:
        it = turns[turn]
        if not it["ok"] or not it["prompt"] or not it["texts"]:
            continue
        ts = it["time"]
        if not ts:
            continue
        dt = datetime.fromtimestamp(ts / 1000)
        if dt.strftime("%Y-%m-%d") != day:
            continue
        response = "\n\n".join(it["texts"])[:HARNESS_MAX_RESPONSE_CHARS]
        out.append({
            "ts": dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "provider": "deepseek-harness",
            "model": None,
            "path": "harness-log",
            "session_id": path.parent.name,
            "prompt": it["prompt"][:40_000],
            "response": response,
            "truncated": False,
        })
    return out


def query_harness_by_day(day: str) -> list[dict]:
    """读取指定本地日期的 DeepSeek Harness 会话日志, 返回与 capture 同结构的记录。"""
    rows = []
    for path in _harness_log_paths():
        try:
            rows += _parse_harness_log(path, day)
        except Exception as e:
            print(f"[!] 解析 harness 会话日志失败 {path}: {e}")
    return rows


def _build_input(rows: list[dict]) -> str:
    """把一天的对话整理成给模型的输入文本,标注每条来源。"""
    parts = []
    for i, r in enumerate(rows, 1):
        provider = r["provider"] or "?"
        source = _detect_source(r)
        prompt = _truncate(r["prompt"] or "", 1200)
        resp = _truncate(r["response"] or "", 2000)
        parts.append(
            f"### 对话 {i} [{provider}] [来源: {source}]\n"
            f"【用户/输入】\n{prompt}\n\n"
            f"【AI 输出】\n{resp}"
        )
    return "\n\n".join(parts)


def _chunk_rows(rows: list[dict]) -> list[list[dict]]:
    """把一天的有效对话按估算长度分批, 每批单独送模型, 避免上下文溢出。"""
    chunks: list[list[dict]] = []
    cur: list[dict] = []
    size = 0
    for r in rows:
        est = len(r.get("prompt") or "") + len(r.get("response") or "") + 200
        if cur and size + est > CHUNK_CHARS:
            chunks.append(cur)
            cur, size = [], 0
        cur.append(r)
        size += est
    if cur:
        chunks.append(cur)
    return chunks


def _merge_chunks(parts: list[str]) -> str:
    """合并多批总结: 只保留第一个 "## 今日知识要点" 标题, 后续批次的标题去掉、内容拼接。"""
    merged = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if p.startswith("## 今日知识要点"):
            p = p[len("## 今日知识要点"):].strip()
        if p and p != "(无实质内容)":
            merged.append(p)
    if not merged:
        return "## 今日知识要点\n(无实质内容)"
    return "## 今日知识要点\n\n" + "\n\n".join(merged)


SUMMARIZE_PROMPT = """你是一个知识库整理助手。下面是一天内用户与 AI 助手(DeepSeek/ChatGPT/Grok 等)的对话记录(可能有工具调用、思考过程、系统提示词等噪音)。

请提炼出**值得沉淀的知识**,输出 Markdown 格式的知识卡片:

## 输出格式要求
- 以 "## 今日知识要点" 开头,按主题分组,每个主题一个小节(### 主题名)
- 每个小节包含:核心结论(1-2 句)、关键要点(条目列表)、**信息来源**(这条知识来自哪个 IDE/插件:Reasonix / VSCode Roo / IDEA ProxyAI / DeepSeek 网页 / DeepSeek API,在"来源:"后列出)
- **如果排查问题涉及代码**:在要点中保留关键代码片段(用 ```语言 换行 代码 换行 ``` 的 Markdown 代码块格式),尽量给出修复前/修复后的对比
- **只输出提炼后的知识**,不要复述对话原文
- 忽略:寒暄、废话、系统提示词、工具调用细节、思考过程
- 如果当天没有实质知识,输出 "## 今日知识要点\n(无实质内容)"
- 涉及邮箱/手机号/密钥/隐私信息时用 [已脱敏] 替代

## 细节保留铁律(非常重要)
- **具体的操作步骤、菜单路径(如 设置 → 代理 →)、配置项名称、选项位置、按钮名称必须原文保留**,不得替换为"检查相关设置""进行相应配置"之类的模糊表述
- **具体的 URL、API 端点、HTTP 方法、请求参数、字段名(如请求 body 里的 model 字段)、命令行参数必须原文保留**
- **具体的错误信息、报错文本、版本号、端口号、文件路径必须原文保留**
- **宁多勿漏**:拿不准是否值得保留的操作细节,一律保留;只有在确认是寒暄/噪音时才省略
- 允许并鼓励使用列表形式逐条列出操作步骤,而不是把它们合并成一句话

## 对话记录
{input}
"""


def call_ollama(input_text: str) -> str:
    """调用本地 Ollama 生成总结。"""
    body = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": SUMMARIZE_PROMPT.format(input=input_text),
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 32768},
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIME_OUT) as r:
        data = json.loads(r.read().decode("utf-8"))
    return (data.get("response") or "").strip()


def _make_markdown(day: str, stats: dict, knowledge: str, code_blocks: list | None = None) -> str:
    tags = "AI知识库, daily"
    sources = stats.get("sources", {})
    src_line = "、".join(f"{k}({v}条)" for k, v in sources.items()) or "无"

    code_section = ""
    if code_blocks:
        parts = ["", "## 排查涉及的代码片段", "> 从当日对话中提取,供快速参考。"]
        for i, (lang, code) in enumerate(code_blocks, 1):
            parts.append(f"### 片段 {i}" + (f"({lang})" if lang else ""))
            parts.append(f"```{lang}\n{code}\n```")
        code_section = "\n".join(parts)

    return f"""---
title: "{day} AI 知识库日报"
date: {day}T06:00:00+08:00
tags: [{tags}]
summary: "AI 对话知识提炼:共 {stats['total']} 条对话,提炼 {stats['kept']} 条{',含代码片段' if code_blocks else ''}"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录({stats['kept']}/{stats['total']} 条有效)。
> 信息来源分布:{src_line}

{knowledge}
{code_section}

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
"""


def _git_push(repo: Path, files: list[Path], dry_run: bool) -> None:
    if not files:
        return
    if dry_run:
        print(f"[dry-run] 跳过 git push({len(files)} 个文件)")
        return
    try:
        subprocess.run(["git", "add", *[str(f) for f in files]], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"docs: add AI knowledge daily summary ({date.today().isoformat()})"],
            cwd=repo, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "master"], cwd=repo, check=True, capture_output=True)
        print(f"[*] 已提交并推送 GitHub({len(files)} 篇日报)")
    except subprocess.CalledProcessError as e:
        print(f"[!] git 操作失败: {e.stderr.decode()[:300] if e.stderr else e}")


def ensure_ollama() -> bool:
    """确保 Ollama 服务在运行,否则尝试启动。"""
    import socket
    try:
        with socket.create_connection(("127.0.0.1", 11434), timeout=2):
            return True
    except OSError:
        pass
    # 尝试启动 ollama serve
    candidates = [
        Path.home() / "AppData" / "Local" / "Programs" / "Ollama" / "ollama.exe",
        Path("C:/Program Files/Ollama/ollama.exe"),
    ]
    for exe in candidates:
        if exe.exists():
            subprocess.Popen([str(exe), "serve"], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            for _ in range(10):
                time.sleep(1)
                try:
                    with socket.create_connection(("127.0.0.1", 11434), timeout=1):
                        return True
                except OSError:
                    continue
            break
    return False


def _last_summarized_day() -> date | None:
    """扫描已发布的日报, 返回已总结的最大日期(文件名=数据日期)。"""
    posts_dir = REPO_ROOT / "content" / "posts"
    if not posts_dir.exists():
        return None
    dates = []
    for f in posts_dir.glob("*-ai-knowledge.md"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-ai-knowledge\.md$", f.name)
        if m:
            dates.append(date.fromisoformat(m.group(1)))
    return max(dates) if dates else None


def summarize_day(day: str, dry_run: bool = False) -> Path | None:
    """总结某一天, 返回生成的 md 文件路径; 无数据返回 None。"""
    rows = query_by_day(day)
    harness_rows = query_harness_by_day(day)
    rows = rows + harness_rows
    if not rows:
        print(f"[!] {day} 没有对话记录,跳过")
        return None
    kept = [r for r in rows if _is_worth_keeping(r)]
    print(f"[*] {day} 共 {len(rows)} 条记录(capture {len(rows) - len(harness_rows)} + harness {len(harness_rows)}),有效 {len(kept)} 条")

    from collections import Counter
    src_counter = Counter(_detect_source(r) for r in kept)
    print(f"[*] 来源分布: {dict(src_counter)}")

    if not kept:
        knowledge = "## 今日知识要点\n(无实质内容)"
    else:
        chunks = _chunk_rows(kept)
        parts = []
        for i, chunk in enumerate(chunks, 1):
            input_text = _build_input(chunk)
            print(f"[*] 第 {i}/{len(chunks)} 批({len(chunk)} 条) 送 Ollama ...")
            out = call_ollama(input_text)
            if out:
                parts.append(out)
        knowledge = _merge_chunks(parts)
        print(f"[*] Ollama 总结完成({len(knowledge)} 字符, {len(chunks)} 批)")

    # 从原始对话中提取代码片段(独立于总结, 避免代码丢失)
    raw_blocks = []
    for r in kept:
        raw_blocks += _extract_code_blocks((r.get("prompt") or "") + "\n" + (r.get("response") or ""))
    code_blocks = _dedup_blocks(raw_blocks)
    if code_blocks:
        print(f"[*] 提取到 {len(code_blocks)} 个代码片段(已脱敏)")

    # 知识总结也做强制脱敏兜底
    knowledge = _redact_sensitive(knowledge)

    md = _make_markdown(day, {
        "total": len(rows),
        "kept": len(kept),
        "sources": dict(src_counter),
    }, knowledge, code_blocks)

    out_dir = REPO_ROOT / "content" / "posts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{day}-ai-knowledge.md"
    out_file.write_text(md, encoding="utf-8")
    print(f"[*] 已生成: {out_file}")
    return out_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?", default=None, help="要总结的日期 YYYY-MM-DD; 不填则自动补漏上次日报之后的所有日期")
    parser.add_argument("--dry-run", action="store_true", help="只生成 md,不 git push")
    parser.add_argument("--no-import", action="store_true", help="跳过本地会话导入(纯抓包数据)")
    args = parser.parse_args()

    # 每次总结前先同步本地 IDE/agent 会话(Continue/Roo/Reasonix)新记录到库
    if not args.no_import:
        try:
            from import_local import import_all
            import_all(dry_run=args.dry_run, days_back=90)
        except Exception as e:
            print(f"[!] 本地会话导入失败(继续): {e}")

    if not ensure_ollama():
        print("[!] Ollama 服务不可用,无法总结")
        sys.exit(1)

    if args.day:
        days = [args.day]
    else:
        # 自动补漏: 上次日报之后(含) 到 昨天, 逐天总结
        today = date.today()
        last = _last_summarized_day()
        if last is None:
            start = today - timedelta(days=1)
            print("[*] 无历史日报,从昨天开始")
        else:
            start = last + timedelta(days=1)
        end = today - timedelta(days=1)
        if start > end:
            print("[*] 没有需要补总结的日期")
            return
        days = [(start + timedelta(days=i)).isoformat() for i in range((end - start).days + 1)]
        print(f"[*] 补漏 {len(days)} 天: {days[0]} ~ {days[-1]}")

    files = []
    for d in days:
        f = summarize_day(d, args.dry_run)
        if f:
            files.append(f)

    _git_push(REPO_ROOT, files, args.dry_run)


if __name__ == "__main__":
    main()
