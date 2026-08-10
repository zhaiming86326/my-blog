---
title: "2026-08-10 AI 知识库日报"
date: 2026-08-10T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 390 条对话,提炼 13 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(13/390 条有效)。
> 信息来源分布:VSCode Roo(1条)、DeepSeek 网页(4条)、DeepSeek API(8条)

## 今日知识要点

### 检查 DeepSeek 连接问题的步骤

核心结论: 当连接 DeepSeek API 出现错误时，可以通过检查账户余额、模型名称配置和网络设置来排查问题。

关键要点:
- **检查账户余额**: 登录DeepSeek开发者后台确认账户状态。
- **核对模型ID**: 确保使用正确的模型ID（如 `deepseek-chat` 或 `deepseek-reasoner`）。
- **禁用IDE代理**: 在IDE设置中找到代理配置并暂时禁用，然后重启IDE试试。
- **检查系统网络权限**: macOS用户前往 `系统设置 -> 隐私与安全性 -> 本地网络` 确保应用有访问本地网络的权限。
- **直接测试API**: 使用命令行工具直接测试API连接：
    ```bash
    curl -v "https://api.deepseek.com/v1/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -d '{
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}]
      }'
    ```
- **检查请求参数**: 确保请求中显式设置 `stream=False`。
- **工具调用功能配置**: 如果启用了“工具调用”功能，尝试关闭或调整相关设置。

信息来源: VSCode Roo / DeepSeek 网页

### ProxyAI 配置 DeepSeek 的方法

核心结论: 在ProxyAI中通过"Custom OpenAI"手动填写DeepSeek支持的模型名称来配置连接。

关键要点:
- **确认配置位置**: 进入 `Settings` -> `Tools` -> `ProxyAI` -> `Providers` -> `Custom OpenAI`。
- **正确填写信息**：
    - URL: `https://api.deepseek.com/v1/chat/completions`
    - API Key: 您的DeepSeek API密钥
    - Model (在Body中): 手动输入 `deepseek-chat` 或 `deepseek-reasoner`

信息来源: DeepSeek 网页

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
