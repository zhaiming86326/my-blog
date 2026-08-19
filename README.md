# AI 知识库博客

自动把每天的 AI 对话记录提炼成知识卡片,发布到 Hugo 博客(Cloudflare Workers 托管)。

## 数据流

```
本地来源(每天自动/手动导入)
├─ Continue     ~/.continue/sessions/*.json
├─ Roo Code     %APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\tasks\<id>\api_conversation_history.json
├─ Reasonix     %APPDATA%\reasonix\archive\context-*.jsonl
├─ DeepSeek Harness  <DSH_HOME>/sessions/<ws>/<session>/session.jsonl[.zstd]
└─ 抓包(可选)   mitmproxy 8080 -> .capture/capture.db(DeepSeek API 等)

        ↓  scripts/import_local.py(会话级增量去重)
   SQLite  .capture/capture.db  (已 gitignore, 永不入库)

        ↓  scripts/summarize.py
   本机 Ollama(qwen2.5:7b-instruct) 分批提炼知识卡片 + 正则强制脱敏

        ↓
   content/posts/YYYY-MM-DD-ai-knowledge.md
        ↓  git push
   GitHub Actions(.github/workflows/deploy.yml) -> hugo -> Cloudflare Workers
```

## 常用命令

```powershell
# 生成并发布日报(默认补漏上次日报之后到昨天的所有日期)
python scripts\summarize.py

# 只生成 md, 不推送
python scripts\summarize.py 2026-08-19 --dry-run

# 指定某一天
python scripts\summarize.py 2026-08-19

# 只重新导入本地会话(不总结)
python scripts\import_local.py --dry-run   # 先预览, 去掉 --dry-run 真正导入

# 本地预览博客
hugo server
```

## 配置

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `OLLAMA_MODEL` | `qwen2.5:7b-instruct` | 总结用模型;提质可设 `qwen2.5:14b-instruct` |
| `DSH_HOME` | `~/.dsh` | DeepSeek Harness 会话日志根目录 |
| `CAPTURE_DB_DIR` | `<repo>/.capture` | 数据库目录(测试时可指向临时目录) |

总结前需保证 Ollama 已运行(`ollama serve` / 桌面应用),脚本会自动尝试拉起。
超过一天上下文容量的输入会自动分批总结后合并(`CHUNK_CHARS` 可调)。

## 抓包(可选, 已基本被本地导入取代)

- 启动: `scripts\run-capture.ps1`(需 v2rayN 10809 端口)或 `scripts\run-deepseek.ps1`(仅 DeepSeek)
- 停止: `scripts\stop-capture.ps1`(恢复系统代理, 重要!)
- 首次使用需管理员运行 `scripts\install-cert.ps1` 安装 mitmproxy 证书

> 注意: 抓包会通过 PAC 设置系统代理并写入 HTTP_PROXY/HTTPS_PROXY 用户环境变量。
> 不抓包时请运行 `stop-capture.ps1` 还原, 否则 Android 模拟器等共享主机网络的应用可能无法联网。

## 安全

- 原始对话只进 `.capture/capture.db`(已 gitignore), 绝不入库 git
- 发布前 `summarize.py` 做两层脱敏: 提示词约束 + 正则兜底(密钥/邮箱/手机号/身份证/连接串)
- GitHub 部署只读仓库内容, 需要 `CLOUDFLARE_API_TOKEN` secret
