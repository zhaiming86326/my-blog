---
title: "2026-08-16 AI 知识库日报"
date: 2026-08-16T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 162 条对话,提炼 129 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(129/162 条有效)。
> 信息来源分布:DeepSeek API(126条)、VSCode Roo(2条)、DeepSeek Harness(1条)

从你的需求来看，你可能更倾向于第二种方案，即使用支持皮肤的第三方输入法。下面我将详细介绍如何安装和使用搜狗输入法和百度输入法，因为它们提供了丰富的皮肤选择。

### 搜狗输入法

1. **下载安装**：
   - 访问[搜狗输入法官网](https://pinyin.sogou.com/)，下载最新版本的搜狗输入法安装包。
   - 运行安装包，按照提示完成安装。

2. **更换皮肤**：
   - 安装完成后，右键点击输入法图标，选择“皮肤”选项。
   - 在皮肤界面中，你可以选择不同的皮肤风格，包括经典、可爱、清新等多种风格。
   - 选择你喜欢的皮肤，点击“应用”即可更换。

### 百度输入法

1. **下载安装**：
   - 访问[百度输入法官网](https://shurufa.baidu.com/)，下载最新版本的百度输入法安装包。
   - 运行安装包，按照提示完成安装。

2. **更换皮肤**：
   - 安装完成后，右键点击输入法图标，选择“皮肤”选项。
   - 在皮肤界面中，你可以选择不同的皮肤风格，包括简约、清新、可爱等多种风格。
   - 选择你喜欢的皮肤，点击“应用”即可更换。

### 其他输入法

- **讯飞输入法**：如果你更注重语音输入功能，可以考虑讯飞输入法。它同样支持更换皮肤，但皮肤选择可能不如搜狗和百度丰富。
- **QQ输入法**：如果你喜欢简洁的界面，可以考虑QQ输入法。它也支持更换皮肤，但皮肤选择相对较少。
- **手心输入法**：手心输入法同样支持更换皮肤，但皮肤选择可能不如搜狗和百度丰富。

### 开源输入法（Rime）

如果你更注重隐私和安全性，可以考虑使用开源输入法Rime（小狼毫/Weasel）。虽然它没有内置的皮肤系统，但你可以通过配置文件自定义输入法的外观。

1. **下载安装**：
   - 访问[Rime官网](https://rime.im/)，下载最新版本的Rime输入法。
   - 安装完成后，按照官方文档进行配置。

2. **自定义皮肤**：
   - 通过修改配置文件（如`schema.yaml`）来自定义输入法的外观。
   - 你可以参考[Rime官方文档](https://rime.im/docs/)中的配置指南，进行详细的自定义设置。

### 总结

- **搜狗输入法**：皮肤选择最多，适合追求个性化外观的用户。
- **百度输入法**：皮肤选择丰富，AI功能强大，适合追求智能化输入体验的用户。
- **Rime**：开源输入法，高度可定制，适合注重隐私和安全性的用户。

希望这些信息对你有所帮助！如果你有其他具体需求或问题，欢迎继续提问。

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(yaml)
```yaml
- id: session-query-sqlite
  config:
    path: ':memory:'
    openAt: never
```
### 片段 2
```
mitmproxy(8080) 抓到 AI 请求 → .capture/capture.db → summarize.py 提炼 → 日报
```
### 片段 3
```
   21:52:21 user/message 这个项目有上下文的使用长度记录等dashboard功能么
   21:52:21 user/message <system-reminder>...
   21:52:21 user/message Current runtime context...
   21:52:21 user/message <system-reminder>...
```
### 片段 4
```
def _detect_source(row: dict) -> str:
    """根据请求内容特征推断来源应用(IDE/插件)。"""
    prompt = row.get("prompt") or ""
    path = row.get("path") or ""
```
### 片段 5
```
def _detect_source(row: dict) -> str:
    """根据请求内容特征推断来源应用(IDE/插件)。"""
    if row.get("provider") == "deepseek-harness":
        return "DeepSeek Harness"
    prompt = row.get("prompt") or ""
    path = row.get("path") or ""
```
### 片段 6
```
def _build_input(rows: list[dict]) -> str:
```
### 片段 7
```
    rows = query_by_day(day)
    if not rows:
        print(f"[!] {day} 没有对话记录,跳过")
        return None
    kept = [r for r in rows if _is_worth_keeping(r)]
    print(f"[*] {day} 共 {len(rows)} 条记录,有效 {len(kept)} 条")
```
### 片段 8
```
    rows = query_by_day(day)
    harness_rows = query_harness_by_day(day)
    rows = rows + harness_rows
    if not rows:
        print(f"[!] {day} 没有对话记录,跳过")
        return None
    kept = [r for r in rows if _is_worth_keeping(r)]
    print(f"[*] {day} 共 {len(rows)} 条记录(capture {len(rows) - len(harness_rows)} + harness {len(harness_rows)}),有效 {len(kept)} 条")
```
### 片段 9(python)
```python
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
    for ev in events:
        t = ev.get("type")
        data = ev.get("data") or {}
        turn = data.get("turn")
        if t == "turn/start":
            if turn not in turns:
                turns[turn] = {"prompt": None, "texts": [], "ok": False, "time": ev.get("time")}
                order.append(turn)
        elif t == "user/message":
            if turn not in turns:
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
            if turn not in turns:
                continue
            for c in (data.get("message") or {}).get("content") or []:
                if (isinstance(c, dict) and c.get("type") == "text"
                        and isinstance(c.get("text"), str) and c["text"].strip()):
                    turns[turn]["texts"].append(c["text"])
        elif t == "turn/end":
            if turn not in turns:
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
```
### 片段 10(python)
```python
# -*- coding: utf-8 -*-
"""给 D:\\workspace\\my-blog\\scripts\\summarize.py 打补丁:
新增 DeepSeek Harness 会话日志数据源(直接解析 $DSH_HOME/sessions 下的 JSONL/zstd),
并合并进每日总结。
用法: python patch-summarize-harness.py [--apply] [--verify]
  --apply   应用补丁(默认只检查能否应用, 不改文件)
  --verify  应用后加载模块, 验证 2026-08-15 能读到 harness 记录
"""
import argparse, importlib.util, sys
from pathlib import Path

TARGET = Path(r"D:\workspace\my-blog\scripts\summarize.py")

PATCHES = [ (old, new), ... ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    src = TARGET.read_text(encoding="utf-8")
    for i, (old, new) in enumerate(PATCHES, 1):
        n = src.count(old)
        if n == 0:
            print(f"[!] 补丁 {i} 未找到原文(可能已应用或文件已变), 中止")
            sys.exit(1)
        if n > 1:
            print(f"[!] 补丁 {i} 原文出现 {n} 次, 无法精确定位, 中止")
            sys.exit(1)
        src = src.replace(old, new)

    if not args.apply:
        print("[*] 检查通过: 4 处补丁均可精确应用。加 --apply 实际修改。")
        return

    TARGET.write_text(src, encoding="utf-8")
    print(f"[*] 已应用补丁: {TARGET}")

    if args.verify:
        spec = importlib.util.spec_from_file_location("summarize_patched", TARGET)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rows = mod.query_harness_by_day("2026-08-15")
        print(f"[*] query_harness_by_day(2026-08-15): {len(rows)} 条")
        for r in rows:
            print(f"  - {r['prompt'][:40]!r} | resp {len(r['response'])} 字符")

if __name__ == "__main__":
    main()
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
