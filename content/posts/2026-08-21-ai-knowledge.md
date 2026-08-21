---
title: "2026-08-21 AI 知识库日报"
date: 2026-08-21T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 5 条对话,提炼 4 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(4/5 条有效)。
> 信息来源分布:Roo Code (本地)(1条)、DeepSeek Harness(3条)

## 今日知识要点

### 8080 代理开机启动原因
- **核心结论**: 开机启动 8080 代理是因为 `capture-service.ps1` 脚本被注册为 Windows 登录计划任务 "AI抓包服务"，每次开机都会自动运行，启动 mitmdump(8080) 代理。
- **关键要点**:
  - `mitmdump` 命令行工具在监听 8080 端口，代理数据到 2rayN(10809)。
  - `capture-service.ps1` 脚本被注册为 Windows 登录计划任务 "AI抓包服务"，每次开机自动运行。
  - 项目已改为本地抓取数据，但计划任务依然存在，导致 8080 代理开机启动。
- **信息来源**: DeepSeek Harness

### 误发内容处理
- **核心结论**: 误发的内容不会影响后续会话，但可以采取措施使其在后续轮次中消失。
- **关键要点**:
  - **开新会话**: 完全清零上下文，旧会话留在磁盘上不再参与。
  - **输入 `/compact`**: 历史被折叠成摘要，后续只看到摘要，不再看到原文。
  - **手动改 session 文件**: 不建议，会话正被运行中的 harness 持有，手改 JSONL 有损坏风险。
- **信息来源**: DeepSeek Harness

### 8080 代理启动排查
- **核心结论**: 8080 代理启动原因在于 `capture-service.ps1` 脚本被注册为 Windows 登录计划任务 "AI抓包服务"。
- **关键要点**:
  - 使用 PowerShell 和 COM 接口查找计划任务。
  - `capture-service.ps1` 脚本被注册为 "AI抓包服务"，每次开机自动运行。
  - 项目已改为本地抓取数据，但计划任务依然存在，导致 8080 代理开机启动。
- **信息来源**: DeepSeek Harness

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1
```
mitmdump --mode upstream:http://127.0.0.1:10809 -s "D:\workspace\my-blog\scripts\capture\addon.py" -p 8080
```
### 片段 2
```
powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "D:\workspace\my-blog\scripts\capture-service.ps1"
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
