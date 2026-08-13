---
title: "2026-08-12 AI 知识库日报"
date: 2026-08-13T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 184 条对话,提炼 153 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(153/184 条有效)。
> 信息来源分布:DeepSeek API(153条)

### 修复总结与后续步骤

**问题描述：**
用户发现文章中的相对链接（如 "详见第5节"）点击后指向不存在的博客链接。这些链接是原文中包含的相对路径，在生成 Markdown 文章时被保留下来，导致 Hugo 渲染时解析成站内死链。

**修复措施：**

1. **清理已有文章：**
   - 扫描所有已发布的 19 篇文章。
   - 发现 `coding-with-ai` 这篇文章中有 4 处相对链接（第3/4/5/7节）。
   - 删除这些链接的语法，保留文字部分。

2. **防止复发：**
   - 在 `publish_articles.py` 中添加 `_clean_relative_links` 函数，在生成 Markdown 文件之前自动清理所有非 `http(s)` 开头的链接（包括相对路径和空链接）。
   - 确保以后生成的文章不会包含类似的站内死链。

3. **验证与部署：**
   - 通过 Hugo 构建验证，确认已修复的问题不再存在。
   - 提交并推送更改到 GitHub，触发自动部署流程。

### 验证结果

- 扫描和清理所有文章中的相对链接后，确保没有遗留任何站内死链。
- `publish_articles.py` 已更新，包含 `_clean_relative_links` 函数以防止未来生成的文章中出现类似问题。
- 构建验证通过，并已推送至 GitHub（提交哈希：a4255d4）。

### 后续建议

1. **刷新页面确认修复：**
   - 用户可以刷新博客页面，再次点击 "详见第5节" 等链接，确保它们现在只是普通文本而不再跳转到死链。
   
2. **检查所有文章：**
   - 建议用户浏览一遍全部文章，确认没有其他类似问题。

3. **定期扫描与清理：**
   - 定期运行脚本扫描和清理相对链接，以确保未来生成的文章不会出现此类问题。

### 结论

通过上述修复措施，已成功解决了站内死链的问题，并防止了未来再次发生。用户可以放心浏览博客内容，不会再遇到类似问题。

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(python)
```python
import os, tempfile
os.environ["CAPTURE_DB_DIR"] = temp_dir
from capture import db
db.init_db()
db.insert_conversation(ts=..., provider="test", model=None, path="/t", session_id="abc", prompt="p", response="r")
# 查回验证
```
### 片段 2(python)
```python
# 客户端注入到用户消息里的策略/指令块, 不属于用户输入
INJECTED_BLOCK_RES = [
    re.compile(r"<reasoning-language>.*?</reasoning-language>", re.DOTALL),
    re.compile(r"<execution-policy[^>]*>.*?</execution-policy>", re.DOTALL),
]

def _strip_injected(text: str) -> str:
    for r in INJECTED_BLOCK_RES:
        text = r.sub("", text)
    return text.strip()
```
### 片段 3
```
#1248  session_id: a48d2e5e31f2b5d1
prompt: 现在我发消息了. 你看下 <execution-policy...>...</execution-policy>
```
### 片段 4
```
#1256  session=a48d2e5e31f2b5d1
prompt: '验证 execution-policy 剥除的最终效果'   （27 字符，无任何注入块）
#1255  session=a48d2e5e31f2b5d1
prompt: '现在我发消息了. 你看下'                （重启后连上一条的块也剥干净了）
```
### 片段 5(python)
```python
HOST_PROVIDERS = {
    "api.deepseek.com": "deepseek-api",   # Reasonix/Roo/IDEA/Zed 等工具走 DeepSeek Anthropic/OpenAI 兼容 API
    "api.x.ai": "grok-api",               # xAI API(工具类)
}
```
### 片段 6(python)
```python
HOST_PROVIDERS = {
    "api.deepseek.com": "deepseek-api",
    "api.x.ai": "grok-api",
}
```
### 片段 7(sql)
```sql
   DELETE FROM conversations WHERE session_id IS NULL AND (
       prompt IS NULL OR prompt = '' OR prompt LIKE 'system: You are%'
       OR prompt LIKE 'user: You are Roo%' OR prompt LIKE '{%'
   )
```
### 片段 8(sql)
```sql
   UPDATE conversations SET prompt = substr(prompt, 6) WHERE session_id IS NULL AND prompt LIKE 'user:%' AND prompt NOT LIKE 'user: You are Roo%';
   UPDATE conversations SET prompt = substr(prompt, 8) WHERE session_id IS NULL AND prompt LIKE 'prompt:%';
```
### 片段 9(sql)
```sql
   UPDATE conversations SET prompt = trim(substr(prompt, 6)) WHERE ... LIKE 'user:%' AND ...;
   UPDATE conversations SET prompt = trim(substr(prompt, 8)) WHERE ... LIKE 'prompt:%';
```
### 片段 10(python)
```python
import sqlite3, hashlib, shutil, os
from datetime import datetime

db = r"D:\workspace\my-blog\.capture\capture.db"
bak = db + ".bak-" + datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(db, bak)
print("备份:", bak)

c = sqlite3.connect(db)
cur = c.cursor()

# 1. 确认待删数量
n_del = cur.execute("""SELECT count(*) FROM conversations WHERE session_id IS NULL AND (
    prompt IS NULL OR prompt = '' OR prompt LIKE 'system: You are%'
    OR prompt LIKE 'user: You are Roo%' OR prompt LIKE '{%')""").fetchone()[0]
print("待删除:", n_del)

# 2. 确认待清洗数量
n_clean = cur.execute("""SELECT count(*) FROM conversations WHERE session_id IS NULL AND prompt IS NOT NULL AND prompt != '' AND (
    (prompt LIKE 'user:%' AND prompt NOT LIKE 'user: You are Roo%') OR prompt LIKE 'prompt:%')""").fetchone()[0]
print("待清洗:", n_clean)

# 执行
cur.execute("""DELETE FROM conversations WHERE session_id IS NULL AND (
    prompt IS NULL OR prompt = '' OR prompt LIKE 'system: You are%'
    OR prompt LIKE 'user: You are Roo%' OR prompt LIKE '{%')""")

rows = cur.execute("""SELECT id, prompt FROM conversations WHERE session_id IS NULL AND prompt IS NOT NULL AND prompt != '' AND (
    (prompt LIKE 'user:%' AND prompt NOT LIKE 'user: You are Roo%') OR prompt LIKE 'prompt:%')""").fetchall()
for rid, p in rows:
    if p.startswith("user:"):
        newp = p[5:].strip()
    else:  # prompt:
        newp = p[7:].strip()
    sid = hashlib.sha256(newp.encode("utf-8", errors="ignore")).hexdigest()[:16]
    cur.execute("UPDATE conversations SET prompt=?, session_id=? WHERE id=?", (newp, sid, rid))

c.commit()
# 验证
print("清洗后总数:", cur.execute("SELECT count(*) FROM conversations").fetchone()[0])
print("session_id 非空:", cur.execute("SELECT count(*) FROM conversations WHERE session_id IS NOT NULL").fetchone()[0])
print("残留拼接检查:", cur.execute("""SELECT count(*) FROM conversations WHERE prompt LIKE 'system: You are%' OR prompt LIKE 'user: You are Roo%' OR prompt LIKE '{%'""").fetchone()[0])
c.close()
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
