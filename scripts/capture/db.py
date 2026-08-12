"""SQLite 存储层:只存脱敏后的对话文本,绝不存 headers / cookies / API keys。

数据文件位于 <repo>/.capture/capture.db,已加入 .gitignore,永远不进 git。
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# <repo>/scripts/capture/db.py -> <repo>/scripts/capture -> <repo>/scripts -> <repo>
REPO_ROOT = Path(__file__).resolve().parents[2]
# 可用 CAPTURE_DB_DIR 环境变量覆盖数据目录(测试时指向临时目录)
DATA_DIR = Path(os.environ["CAPTURE_DB_DIR"]) if os.environ.get("CAPTURE_DB_DIR") else REPO_ROOT / ".capture"
DB_PATH = DATA_DIR / "capture.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT    NOT NULL,                -- ISO8601 UTC, e.g. 2026-04-22T06:00:00Z
    provider   TEXT    NOT NULL,                -- deepseek-api / chatgpt / gemini / grok ...
    model      TEXT,
    path       TEXT,                            -- 请求路径(便于过滤与追踪)
    session_id TEXT,                            -- 会话标识(无状态API无现成id,取首条用户消息哈希)
    prompt     TEXT,                            -- 用户侧输入(纯文本,已脱敏)
    response   TEXT,                            -- AI 侧输出(纯文本,已脱敏)
    truncated  INTEGER NOT NULL DEFAULT 0       -- 1 = 原始内容过长被截断
);
CREATE INDEX IF NOT EXISTS idx_conversations_ts ON conversations (ts);
CREATE INDEX IF NOT EXISTS idx_conversations_provider ON conversations (provider);
"""


def _connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """建表(幂等),并迁移旧库补 path 列。"""
    with _connect() as conn:
        conn.executescript(SCHEMA)
        cols = [r[1] for r in conn.execute("PRAGMA table_info(conversations)")]
        if "path" not in cols:
            conn.execute("ALTER TABLE conversations ADD COLUMN path TEXT")
        if "session_id" not in cols:
            conn.execute("ALTER TABLE conversations ADD COLUMN session_id TEXT")


def insert_conversation(
    *,
    ts: datetime,
    provider: str,
    model: str | None,
    path: str | None = None,
    session_id: str | None = None,
    prompt: str,
    response: str,
    truncated: bool = False,
) -> int:
    """写入一条对话记录,返回自增 id。所有字段在调用前已完成脱敏。"""
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO conversations (ts, provider, model, path, session_id, prompt, response, truncated)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                provider,
                model,
                path,
                session_id,
                prompt,
                response,
                1 if truncated else 0,
            ),
        )
        return int(cur.lastrowid)


def query_by_day(day: str) -> list[dict]:
    """取某一天(本地时区 YYYY-MM-DD)的全部记录,供每日总结使用。

    day 按本机本地时区解释:当天 00:00:00 至 23:59:59.999。
    注意 ts 以 UTC 存储,这里用 SQLite 的 localtime 修正回本地时区比较。
    """
    start, end = day + " 00:00:00", day + " 23:59:59.999"
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM conversations"
            " WHERE datetime(ts, 'localtime') BETWEEN datetime(?, 'localtime') AND datetime(?, 'localtime')"
            " ORDER BY ts",
            (start, end),
        ).fetchall()
    return [dict(r) for r in rows]


def count_all() -> int:
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) AS n FROM conversations").fetchone()["n"]


def prune_before(days: int = 90) -> int:
    """清理 days 天前的原始记录(总结已入博客,原文可弃),返回删除条数。"""
    cutoff = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        cur = conn.execute(
            "DELETE FROM conversations WHERE ts < datetime(?, '-%d days')" % days,
            (cutoff,),
        )
        return cur.rowcount


if __name__ == "__main__":
    init_db()
    print(f"DB ready: {DB_PATH} (total rows: {count_all()})")
