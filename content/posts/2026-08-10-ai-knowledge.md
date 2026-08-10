---
title: "2026-08-10 AI 知识库日报"
date: 2026-08-10T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 360 条对话,提炼 13 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(13/360 条有效)。
> 信息来源分布:VSCode Roo(1条)、DeepSeek 网页(4条)、DeepSeek API(8条)

## 今日知识要点

### 连接 DeepSeek API 错误排查

核心结论: 当连接DeepSeek API时遇到问题，可以按步骤检查账户余额、模型ID和API信息等基础项，并进一步排查网络环境或插件设置。

关键要点:
- 检查账户余额是否充足。
- 确认使用正确的模型ID（如`deepseek-chat`）。
- 核实API密钥与DeepSeek官方API Key一致。
- 排查本地网络和代理设置，确保IDE应用有访问本地网络的权限。
- 使用命令行工具直接测试API连接：
  ```bash
  curl -v "https://api.deepseek.com/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -d '{
      "model": "deepseek-chat",
      "messages": [{"role": "user", "content": "Hello"}]
    }'
  ```
- 检查插件功能配置，如工具调用（Tools）和请求参数设置。
- 注意模型名称的准确性，避免使用非官方或过时的模型名。

信息来源: VSCode Roo / DeepSeek 网页

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(bash)
```bash
    # 把 YOUR_API_KEY 换成你自己的
    curl -v "https://api.deepseek.com/v1/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -d '{
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}]
      }'
```
### 片段 2
```
https://api.deepseek.com/v1/chat/completions
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
