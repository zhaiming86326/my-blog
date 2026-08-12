---
title: "Agentic Loop 提示指南：如何驱动 AI 编码代理"
date: 2025-12-10T08:00:00+08:00
tags: [AI, 文章]
summary: "本文提供了如何更有效地与AI编码助手交流的指导，包括具体要求、技术栈指定、参考现有模式等技巧。"
source: "https://github.com/allierays/agentic-loop/blob/HEAD/docs/PROMPTING-GUIDE.md"
---

# Agentic Loop 提示指南：如何驱动 AI 编码代理

> 来源: [GitHub](https://github.com/allierays/agentic-loop/blob/HEAD/docs/PROMPTING-GUIDE.md) · 由本地 LLM 概括

**摘要**: 本文提供了如何更有效地与AI编码助手交流的指导，包括具体要求、技术栈指定、参考现有模式等技巧。

## 要点

- 具体说明需求：例如，“构建一个带有邮箱和密码字段的登录表单。包含客户端验证（邮箱格式校验，密码至少8位）、每个字段下方显示错误信息、提交按钮加载状态，在成功时重定向到 /dashboard。”
- 指定技术栈：明确指出使用的库，如“使用react-hook-form和zod进行表单验证，遵循现有UserForm组件的模式。”
- 引用现有模式：例如，“创建一个POST /api/users端点，遵循现有/api/products端点的相同模式。使用相同的错误处理和响应格式。”

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
