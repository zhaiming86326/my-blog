"""从本地 IDE/agent 的历史文件导入对话到 SQLite,替代抓包采集。

覆盖三个来源:
  - Continue     : ~/.continue/sessions/*.json
                   每条 {message:{role, content:[{type,text}] }};无时间戳,用文件 mtime 归日
  - Roo Code     : %APPDATA%/Code/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<id>/api_conversation_history.json
                   {role, content:[{type,text/tool_use/tool_result}]};全局 _index.json 提供 ts/title
  - Reasonix     : %APPDATA%/reasonix/archive/context-*.jsonl
                   {role, content, reasoning_content}

去重策略(增量导入):
  每 writer 记录一条 UNIQUE(provider, session_id);重复会话跳过。
  同会话文件后续新增的轮次不会重复导入(会话级去重)。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 使 capture.db 可导入
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from capture import db  # noqa: E402

# 每个会话最多读入的轮次(防止超大会话拖慢总结)
MAX_TURNS = 60


# ---------- 工具函数 ----------

def _norm_role(role: str) -> str:
    role = (role or "").strip().lower()
    if role in ("user", "human", "you"):
        return "user"
    if role in ("assistant", "ai", "model"):
        return "assistant"
    if role in ("tool", "function", "system"):
        return role
    return "other"


def _extract_text_from_content(content) -> str:
    """从 content(可能 str / list[{type,text}] )提取纯用户文本,跳过 tool 噪音。"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    out = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                t = item.get("type", "")
                if t == "toolUse" or t == "tool_result":
                    continue
                if t in ("text", "input_text", "thinking_text", "image_url"):
                    txt = item.get("text") or item.get("input") or ""
                    if isinstance(txt, str):
                        out.append(txt)
    elif isinstance(content, dict):
        out.append(str(content.get("text") or content.get("content") or ""))
    return "\n".join(p for p in out if p and p.strip())


def _parse_ts_local(s) -> datetime | None:
    """把各种时间戳(ms epoch / ISO)转成本地 datetime,解析失败返回 None。"""
    if not s:
        return None
    if isinstance(s, (int, float)):
        s = s / 1000 if s > 1e12 else s  # 毫秒 -> 秒
        return datetime.fromtimestamp(s)
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone()
    except Exception:
        return None


def _preferred_localday(dt: datetime) -> str:
    """归日:落在 06:00 后算当天, 06:00 前归前一天(与每日 06:00 定时对齐)。"""
    d = dt.date()
    if dt.hour < 6:
        d -= timedelta(days=1)
    return d.isoformat()


# ---------- 各来源解析器 ----------

def _iter_continue(sessions_dir: Path):
    for f in sorted(sessions_dir.glob("*.json")):
        if f.name == "sessions.json":
            continue
        try:
            s = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        history = s.get("history") or []
        if not history:
            continue
        fstat = f.stat().st_mtime
        day = _preferred_localday(datetime.fromtimestamp(fstat))
        title = str(s.get("title") or f.stem)[:120]
        prompt_parts, resp_parts = [], []
        for m in history:
            msg = m.get("message", {}) if isinstance(m, dict) else {}
            role = _norm_role(msg.get("role"))
            text = _extract_text_from_content(msg.get("content"))
            if not text.strip():
                continue
            if role == "user":
                prompt_parts.append(text)
            elif role == "assistant":
                resp_parts.append(text)
        if not prompt_parts:
            continue
        yield {
            "source": "continue",
            "day": day,
            "ts": datetime.fromtimestamp(fstat),
            "title": title,
            "prompt": "\n\n".join(prompt_parts)[:8000],
            "response": "\n\n".join(resp_parts)[:16000],
            "session": f"continue-{f.stem}",
        }


def _iter_roo(tasks_dir: Path):
    idx = tasks_dir / "_index.json"
    meta = {}
    if idx.exists():
        try:
            for e in (json.load(open(idx, encoding="utf-8")).get("entries") or []):
                ts = _parse_ts_local(e.get("ts"))
                if ts:
                    meta[e.get("id")] = {
                        "day": _preferred_localday(ts),
                        "ts": ts,
                        "title": str(e.get("task") or "")[:120],
                    }
        except Exception:
            pass
    for sub in sorted(tasks_dir.iterdir()):
        if not sub.is_dir():
            continue
        fp = sub / "api_conversation_history.json"
        if not fp.exists():
            continue
        try:
            rows = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        if not rows:
            continue
        m = meta.get(sub.name, {})
        prompt_parts, resp_parts = [], []
        for r in rows:
            if not isinstance(r, dict):
                continue
            role = _norm_role(r.get("role"))
            c = r.get("content")
            texts = _extract_text_from_content(c) if isinstance(c, str) else ""
            texts = texts or ""
            if isinstance(c, list):
                for item in c:
                    if isinstance(item, str):
                        texts += item + "\n"
                    elif isinstance(item, dict):
                        t = item.get("type")
                        if t in ("text", "input_text"):
                            texts += str(item.get("text") or item.get("content") or "") + "\n"
            texts = texts.strip()
            if not texts:
                continue
            if role == "user":
                prompt_parts.append(texts)
            elif role == "assistant":
                resp_parts.append(texts)
        if not prompt_parts:
            continue
        ts = m.get("ts") or datetime.fromtimestamp(fp.stat().st_mtime)
        day = m.get("day") or _preferred_localday(ts)
        yield {
            "source": "roo",
            "day": day,
            "ts": ts,
            "title": m.get("title") or sub.name[:30],
            "prompt": "\n\n".join(prompt_parts)[:8000],
            "response": "\n\n".join(resp_parts)[:16000],
            "session": f"roo-{sub.name}",
        }


def _iter_reasonix(archive_dir: Path):
    for f in sorted(archive_dir.glob("context-*.jsonl")):
        try:
            lines = [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
        except Exception:
            continue
        if not lines:
            continue
        prompt_parts, resp_parts = [], []
        ts = None
        for ln in lines:
            try:
                o = json.loads(ln)
            except Exception:
                continue
            role = _norm_role(o.get("role"))
            content = o.get("content")
            if role == "user" and isinstance(content, str) and content.strip():
                prompt_parts.append(content)
            elif role == "assistant" and isinstance(content, str) and content.strip():
                text = content
                rc = o.get("reasoning_content")
                if rc:
                    text = f"【思考】\n{rc}\n\n【回答】\n{text}"
                resp_parts.append(text)
            if ts is None and o.get("ts"):
                ts = _parse_ts_local(o.get("ts"))
        if not prompt_parts:
            continue
        if ts is None:
            ts = datetime.fromtimestamp(f.stat().st_mtime)
        day = _preferred_localday(ts)
        yield {
            "source": "reasonix",
            "day": day,
            "ts": ts,
            "title": f.stem[:30],
            "prompt": "\n\n".join(prompt_parts)[:8000],
            "response": "\n\n".join(resp_parts)[:16000],
            "session": f"reasonix-{f.stem}",
        }


SOURCES = {
    "continue": (os.environ["USERPROFILE"], ".continue", "sessions", _iter_continue),
    "roo": (os.environ.get("APPDATA"), "Code", "User", "globalStorage",
            "rooveterinaryinc.roo-cline", "tasks", _iter_roo),
    "reasonix": (os.environ.get("APPDATA"), "reasonix", "archive", _iter_reasonix),
}


def import_all(dry_run: bool = False, days_back: int = 90, min_day: str | None = None) -> dict:
    db.init_db()
    conn = db._connect()
    conn.execute("PRAGMA foreign_keys=OFF")
    seen_prov_sess = set(
        row[0] for row in conn.execute(
            "SELECT DISTINCT provider || ':' || COALESCE(session_id,'') FROM conversations"
        ).fetchall()
    )

    stats = {"imported": 0, "skipped_dup": 0, "sources": {}}
    cutoff = datetime.now() - timedelta(days=days_back)
    for src, spec in SOURCES.items():
        base = Path(os.path.join(*spec[:-1]))
        iterfn = spec[-1]
        if not base.exists():
            stats["sources"].setdefault(src, "no_dir")
            continue
        n = 0
        for rec in iterfn(base):
            if rec["ts"] < cutoff:
                continue
            if min_day and rec["day"] < min_day:
                continue
            # 跳过无内容的
            if not rec["prompt"].strip():
                continue
            key = f"local-{src}:{rec['session']}"
            if key in seen_prov_sess:
                stats["skipped_dup"] += 1
                continue
            seen_prov_sess.add(key)
            provider = f"local-{src}"
            session_id = rec["session"]
            if dry_run:
                n += 1
                continue
            db.insert_conversation(
                ts=rec["ts"].astimezone(),
                provider=provider,
                model=None,
                path=f"local:{src}",
                session_id=session_id,
                prompt=rec["prompt"],
                response=rec["response"],
                truncated=len(rec["prompt"]) + len(rec["response"]) > 24000,
            )
            n += 1
        if n:
            stats["sources"][src] = n
    conn.close()
    return stats


def main():
    ap = argparse.ArgumentParser(description="从本地 IDE/agent 历史文件导入对话到 SQLite")
    ap.add_argument("--dry-run", action="store_true", help="只统计,不写库")
    ap.add_argument("--days", type=int, default=90, help="只导入最近 N 天(默认90)")
    ap.add_argument("--since", help="只导入 >= 该日期 YYYY-MM-DD 的会话")
    args = ap.parse_args()

    stats = import_all(dry_run=args.dry_run, days_back=args.days, min_day=args.since)
    total = sum(v for k, v in stats["sources"].items() if isinstance(v, int))
    print(f"[*] {'[dry-run] ' if args.dry_run else ''}导入结果: 新增 {total} 条, "
          f"去重跳过 {stats['skipped_dup']} 条")
    for k, v in stats["sources"].items():
        print(f"    {k}: {v}")
    print(f"    数据库总记录: {db.count_all()}")


if __name__ == "__main__":
    main()
