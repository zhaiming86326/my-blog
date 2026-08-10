---
title: "2026-08-10 AI 知识库日报"
date: 2026-08-10T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 233 条对话,提炼 13 条"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(13/233 条有效)。
> 信息来源分布:VSCode Roo(1条)、DeepSeek 网页(4条)、DeepSeek API(8条)

## 今日知识要点

### API 配置与模型选择
- **核心结论**：在使用 DeepSeek API 时，确保正确配置模型名称和 URL。
- **关键要点**
  - 模型名称应为 `deepseek-chat` 或 `deepseek-reasoner` 而不是 `gpt-4.1` 等其他值。
  - 配置界面中可能没有下拉菜单选项，需要手动填写模型名称。
  - URL 应设置为 `https://api.deepseek.com/v1/chat/completions`。
  - 如果使用的是 ProxyAI（原名CodeGPT），需通过“Custom OpenAI”方式进行配置。
- **信息来源:** DeepSeek 网页

### 网络与代理设置排查
- **核心结论**：网络和代理设置可能影响插件与 API 的通信。
- **关键要点**
  - 检查并临时禁用 IDE 代理设置。
  - 确认系统网络权限配置正确。
  - 使用命令行工具直接测试 API 连接。
- **信息来源:** DeepSeek 网页

### 插件功能与兼容性问题
- **核心结论**：插件的某些高级功能可能与 API 不兼容，导致请求失败。
- **关键要点**
  - 检查并关闭工具调用（Tools）功能。
  - 在模型配置文件中设置 `"capabilities": { "tools": true }` 或禁用此功能。
  - 显式设置 `stream=False` 关闭流式传输。
- **信息来源:** DeepSeek 网页

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
