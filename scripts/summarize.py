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
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from capture.db import DATA_DIR, query_by_day  # noqa: E402

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b-instruct"
TIME_OUT = 900  # 秒,模型总结可能较慢

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
    # 需要包含用户侧输入(user: 或 prompt: 或 messages 形式)
    if not re.search(r"user:|prompt:|输入:|用户", prompt[:4000]):
        return False
    # 过滤明显是"我"的纯系统提示词调用(没有用户消息)
    if "system: You are" in prompt and "user:" not in prompt:
        return False
    return True


def _truncate(text: str, limit: int = 1500) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n…(截断)"


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


SUMMARIZE_PROMPT = """你是一个知识库整理助手。下面是一天内用户与 AI 助手(DeepSeek/ChatGPT/Grok 等)的对话记录(可能有工具调用、思考过程、系统提示词等噪音)。

请提炼出**值得沉淀的知识**,输出 Markdown 格式的知识卡片:

## 输出格式要求
- 以 "## 今日知识要点" 开头,按主题分组,每个主题一个小节(### 主题名)
- 每个小节包含:核心结论(1-2 句)、关键要点(条目列表)、**信息来源**(这条知识来自哪个 IDE/插件:Reasonix / VSCode Roo / IDEA ProxyAI / DeepSeek 网页 / DeepSeek API,在"来源:"后列出)
- **只输出提炼后的知识**,不要复述对话原文
- 忽略:寒暄、废话、系统提示词、工具调用细节、思考过程
- 如果当天没有实质知识,输出 "## 今日知识要点\n(无实质内容)"
- 涉及邮箱/手机号/密钥/隐私信息时用 [已脱敏] 替代

## 对话记录
{input}
"""


def call_ollama(input_text: str) -> str:
    """调用本地 Ollama 生成总结。"""
    body = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": SUMMARIZE_PROMPT.format(input=input_text),
        "stream": False,
        "options": {"temperature": 0.3, "num_ctx": 32768},
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIME_OUT) as r:
        data = json.loads(r.read().decode("utf-8"))
    return (data.get("response") or "").strip()


def _make_markdown(day: str, stats: dict, knowledge: str) -> str:
    tags = "AI知识库, daily"
    sources = stats.get("sources", {})
    src_line = "、".join(f"{k}({v}条)" for k, v in sources.items()) or "无"
    return f"""---
title: "{day} AI 知识库日报"
date: {date.today().isoformat()}T06:00:00+08:00
tags: [{tags}]
summary: "AI 对话知识提炼:共 {stats['total']} 条对话,提炼 {stats['kept']} 条"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录({stats['kept']}/{stats['total']} 条有效)。
> 信息来源分布:{src_line}

{knowledge}

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
"""


def _git_push(repo: Path, dry_run: bool) -> None:
    file = f"content/posts/{date.today().isoformat()}-ai-knowledge.md"
    if dry_run:
        print(f"[dry-run] 跳过 git push({file})")
        return
    try:
        subprocess.run(["git", "add", file], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"docs: add AI knowledge daily summary ({date.today().isoformat()})"],
            cwd=repo, check=True, capture_output=True,
        )
        subprocess.run(["git", "push", "origin", "master"], cwd=repo, check=True, capture_output=True)
        print("[*] 已提交并推送 GitHub")
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?", default=None, help="要总结的日期 YYYY-MM-DD,默认昨天")
    parser.add_argument("--dry-run", action="store_true", help="只生成 md,不 git push")
    args = parser.parse_args()

    day = args.day or (date.today() - timedelta(days=1)).isoformat()

    if not ensure_ollama():
        print("[!] Ollama 服务不可用,无法总结")
        sys.exit(1)

    rows = query_by_day(day)
    if not rows:
        print(f"[!] {day} 没有对话记录,退出")
        return
    kept = [r for r in rows if _is_worth_keeping(r)]
    print(f"[*] {day} 共 {len(rows)} 条记录,有效 {len(kept)} 条")

    from collections import Counter
    src_counter = Counter(_detect_source(r) for r in kept)
    print(f"[*] 来源分布: {dict(src_counter)}")

    if not kept:
        knowledge = "## 今日知识要点\n(无实质内容)"
    else:
        input_text = _build_input(kept)
        knowledge = call_ollama(input_text)
        print(f"[*] Ollama 总结完成({len(knowledge)} 字符)")

    md = _make_markdown(day, {
        "total": len(rows),
        "kept": len(kept),
        "sources": dict(src_counter),
    }, knowledge)

    out_dir = REPO_ROOT / "content" / "posts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{date.today().isoformat()}-ai-knowledge.md"
    out_file.write_text(md, encoding="utf-8")
    print(f"[*] 已生成: {out_file}")

    _git_push(REPO_ROOT, args.dry_run)


if __name__ == "__main__":
    main()
