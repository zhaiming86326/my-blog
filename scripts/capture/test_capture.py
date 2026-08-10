"""抓包插件纯函数测试(无需真实网络)。

运行: python scripts/capture/test_capture.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture.addon import (  # noqa: E402
    _is_conversation_request,
    extract_request,
    extract_response,
    provider_for,
    redact,
)

PASS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS
    if cond:
        PASS += 1
        print(f"  ok  {name}")
    else:
        print(f"FAIL  {name}  {detail}")
        raise SystemExit(1)


def test_provider_for():
    print("[provider_for]")
    check("api.deepseek.com -> deepseek-api", provider_for("api.deepseek.com") == "deepseek-api")
    check("chatgpt.com -> chatgpt", provider_for("chatgpt.com") == "chatgpt")
    check("子域名 ai.chatgpt.com -> chatgpt", provider_for("ai.chatgpt.com") == "chatgpt")
    check("grok.com -> grok", provider_for("grok.com") == "grok")
    check("gemini 已停用 -> None", provider_for("gemini.google.com") is None)
    check("aistudio.google.com -> None", provider_for("aistudio.google.com") is None)
    check("无关域名 -> None", provider_for("example.com") is None)
    check("大小写不敏感", provider_for("API.DEEPSEEK.COM") == "deepseek-api")


def test_redact():
    print("[redact]")
    obj = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "hi"}],
        "api_key": "sk-123456",
        "meta": {"token": "abc", "ok": True},
    }
    out = redact(obj)
    assert out["api_key"] == "[REDACTED]"
    assert out["meta"]["token"] == "[REDACTED]"
    assert out["model"] == "deepseek-chat" and out["messages"] == obj["messages"]
    assert obj["api_key"] == "sk-123456"  # 原对象未被修改
    check("敏感字段被替换且原对象不变", True)


def test_extract_request_deepseek_api():
    print("[extract_request: DeepSeek/OpenAI 风格 API]")
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是助手"},
            {"role": "user", "content": "什么是量子纠缠?"},
        ],
        "stream": True,
    }).encode()
    prompt, model, truncated = extract_request(body)
    check("提取到 user 消息", "什么是量子纠缠?" in prompt, prompt)
    check("提取到 system 消息", "你是助手" in prompt, prompt)
    check("model 正确", model == "deepseek-chat", str(model))
    check("未截断", truncated is False)


def test_extract_request_chatgpt_web():
    print("[extract_request: ChatGPT 网页版]")
    body = json.dumps({
        "action": "next",
        "messages": [{
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": ["帮我写个冒泡排序"]},
        }],
        "model": "gpt-4o",
    }).encode()
    prompt, model, _ = extract_request(body)
    check("提取到网页版 user 消息", "帮我写个冒泡排序" in prompt, prompt)
    check("model 正确", model == "gpt-4o", str(model))


def test_extract_request_fallback_redact():
    print("[extract_request: 无对话字段时落脱敏 JSON]")
    body = json.dumps({
        "session": "s-001",
        "credential": {"api_key": "sk-999"},
        "note": "metadata only",
    }).encode()
    prompt, _, _ = extract_request(body)
    check("正文保留", "metadata only" in prompt, prompt)
    check("api_key 被脱敏", "sk-999" not in prompt, prompt)
    check("落库文本含 [REDACTED]", "[REDACTED]" in prompt, prompt)


def test_extract_request_deepseek_web():
    print("[extract_request: DeepSeek 网页版单轮 prompt 字段]")
    body = json.dumps({
        "chat_session_id": "abc123",
        "parent_message_id": 4,
        "prompt": "你的价格是从哪里获得的?",
        "thinking_enabled": False,
    }).encode()
    prompt, model, _ = extract_request(body)
    check("提取到 prompt 字段", prompt == "prompt: 你的价格是从哪里获得的?", repr(prompt))
    check("不落库整个 JSON", "chat_session_id" not in prompt, prompt)


def test_extract_request_responses_api():
    print("[extract_request: Responses 风格 system 字段]")
    body = json.dumps({
        "model": "deepseek-v4",
        "system": [{"type": "text", "text": "You are an assistant."}],
        "input": [{"role": "user", "content": "hello"}],
    }).encode()
    prompt, model, _ = extract_request(body)
    check("提取到 system 文本", "system: You are an assistant." in prompt, prompt)
    check("提取到 input 文本", "input: hello" in prompt, prompt)
    check("model 正确", model == "deepseek-v4", str(model))


def test_extract_response_api_sse():
    print("[extract_response: API 流式 SSE]")
    sse = (
        'data: {"id":"1","choices":[{"delta":{"role":"assistant","content":"量子纠缠是"}}]}\n\n'
        'data: {"id":"1","choices":[{"delta":{"content":"一种量子现象。"}}]}\n\n'
        'data: [DONE]\n\n'
    ).encode()
    resp, truncated = extract_response(sse)
    check("SSE 拼接完整", resp == "量子纠缠是一种量子现象。", repr(resp))
    check("未截断", truncated is False)


def test_extract_response_web_sse():
    print("[extract_response: 网页版 SSE (parts 结构)]")
    sse = (
        'data: {"message":{"author":{"role":"assistant"},'
        '"content":{"content_type":"text","parts":["你好呀!","有什么可以帮你?"]}}}\n\n'
        'data: [DONE]\n\n'
    ).encode()
    resp, _ = extract_response(sse)
    check("parts 数组拼接", "你好呀!" in resp and "有什么可以帮你?" in resp, repr(resp))


def test_extract_response_gemini_web():
    print("[extract_response: Gemini 网页版嵌套结构]")
    payload = {
        "result": [{
            "content": [{"parts": [{"text": "量子纠缠是量子力学中的一种现象。"}]}],
        }],
    }
    resp, _ = extract_response(json.dumps(payload).encode())
    check("嵌套 text 提取", "量子纠缠是量子力学中的一种现象。" in resp, repr(resp))


def test_is_conversation_request():
    print("[is_conversation_request: 非对话请求过滤]")
    check("deepseek 对话接口保留",
          _is_conversation_request("deepseek", "/api/v0/chat/completion", b"{}") is True)
    check("challenge 探测跳过",
          _is_conversation_request("deepseek", "/api/v0/chat/completion/challenge", b"{}") is False)
    check("文件上传跳过",
          _is_conversation_request("deepseek", "/api/v0/file/upload_file", b"{}") is False)
    check("设置同步跳过",
          _is_conversation_request("deepseek", "/api/v0/chat/settings", b"{}") is False)
    check("建会话跳过",
          _is_conversation_request("deepseek", "/api/v0/chat_session", b"{}") is False)
    check("二进制 body 跳过",
          _is_conversation_request("chatgpt", "/backend-api/conversation", b"\x00\x01\x08abc") is False)
    check("urlencoded 埋点跳过",
          _is_conversation_request("grok", "/rest/app-chat/conversations", b"data=W3siZXZlbnQiOiJ4In1d") is False)
    check("chatgpt 对话请求(含 message)保留",
          _is_conversation_request("chatgpt", "/backend-api/conversation",
                                   b'{"action":"next","message":{"content":{"parts":["hi"]}}}') is True)
    check("chatgpt 预检(无 message)跳过",
          _is_conversation_request("chatgpt", "/backend-api/conversation",
                                   b'{"action":"next","parent_message_id":"x"}') is False)
    check("chatgpt prepare_token 跳过",
          _is_conversation_request("chatgpt", "/backend-api/conversation",
                                   b'{"prepare_token":"abc"}') is False)
    check("chatgpt 非对话路径跳过",
          _is_conversation_request("chatgpt", "/backend-api/me", b"{}") is False)
    check("grok 遥测 locale 跳过",
          _is_conversation_request("grok", "/rest/app-chat/modes", b'{"locale":"zh"}') is False)
    check("grok 对话路径保留",
          _is_conversation_request("grok", "/rest/app-chat/conversations/new",
                                   b'{"message":"hello"}') is True)


def test_extract_response_anthropic_sse():
    print("[extract_response: Anthropic 风格 SSE (DeepSeek 网页/API)]")
    sse = (
        'data: {"type":"message_start","message":{"role":"assistant","model":"deepseek-v4-flash","content":[]}}\n\n'
        'data: {"type":"content_block_start","index":0,"content_block":{"type":"thinking","thinking":""}}\n\n'
        'data: {"type":"ping"}\n\n'
        'data: {"type":"content_block_delta","index":0,"delta":{"type":"thinking_delta","thinking":"让我"}}\n\n'
        'data: {"type":"content_block_delta","index":0,"delta":{"type":"thinking_delta","thinking":"想想。"}}\n\n'
        'data: {"type":"content_block_delta","index":1,"delta":{"type":"text_delta","text":"量子纠缠是"}}\n\n'
        'data: {"type":"content_block_delta","index":1,"delta":{"type":"text_delta","text":"一种量子现象。"}}\n\n'
        'data: {"type":"message_stop"}\n\n'
    ).encode()
    resp, _ = extract_response(sse)
    check("思考无缝拼接", "让我想想。" in resp, repr(resp))
    check("正文无缝拼接(无换行分隔)", "量子纠缠是一种量子现象。" in resp, repr(resp))
    check("思考与正文分区", "【思考】" in resp and "【回答】" in resp, repr(resp))
    check("非增量 token 不被空行分隔", "量子纠缠是\n\n一种" not in resp, repr(resp))


def test_extract_response_deepseek_web_patch():
    print("[extract_response: DeepSeek 网页版 JSON-Patch 流式]")
    sse = (
        'data: {"request_message_id":1,"response_message_id":2,"model_type":"default"}\n\n'
        'data: {"updated_at":1786348648.638227}\n\n'
        'data: {"p":"response/fragments/-1/content","o":"APPEND","v":"快速"}\n\n'
        'data: {"v":"下载"}\n\n'
        'data: {"v":"对话记录"}\n\n'
        'data: {"p":"response/status","o":"SET","v":"FINISHED"}\n\n'
        'data: {"p":"response","o":"BATCH","v":[{"p":"accumulated_token_usage","v":283},{"p":"quasi_status","v":"FINISHED"}]}\n\n'
        'data: [DONE]\n\n'
    ).encode()
    resp, _ = extract_response(sse)
    check("v 字段无缝拼接", resp == "快速下载对话记录", repr(resp))
    check("状态字段不拼入", "FINISHED" not in resp, repr(resp))
    check("元信息载荷被忽略", "request_message_id" not in resp, repr(resp))


def test_extract_request_chatgpt_message_singular():
    print("[extract_request: ChatGPT 新版单数 message 字段]")
    body = json.dumps({
        "action": "next",
        "conversation_id": "abc",
        "message": {
            "author": {"role": "user"},
            "content": {"content_type": "text", "parts": ["帮我写首诗"]},
        },
    }).encode()
    prompt, model, _ = extract_request(body)
    check("提取到 message 文本", prompt == "user: 帮我写首诗", repr(prompt))
    check("不落库整个 JSON", "conversation_id" not in prompt, prompt)


def test_extract_response_plain_text():
    print("[extract_response: 纯文本响应]")
    resp, truncated = extract_response("普通文本返回".encode())
    check("原样返回", resp == "普通文本返回", repr(resp))
    check("未截断", truncated is False)


if __name__ == "__main__":
    test_provider_for()
    test_redact()
    test_extract_request_deepseek_api()
    test_extract_request_chatgpt_web()
    test_extract_request_fallback_redact()
    test_extract_request_deepseek_web()
    test_extract_request_responses_api()
    test_extract_request_chatgpt_message_singular()
    test_is_conversation_request()
    test_extract_response_api_sse()
    test_extract_response_web_sse()
    test_extract_response_gemini_web()
    test_extract_response_anthropic_sse()
    test_extract_response_deepseek_web_patch()
    test_extract_response_plain_text()
    print(f"\n全部通过: {PASS} 项检查")
