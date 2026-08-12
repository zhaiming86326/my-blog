---
title: "用 Vercel AI SDK 构建 AI Agent"
date: 2025-11-03T08:00:00+08:00
tags: [AI, 文章]
summary: "本文介绍了如何使用 Vercel AI SDK 构建 AI Agent，包括调用大语言模型、定义工具以及创建多步骤的代理循环。"
source: "https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk"
---

# 用 Vercel AI SDK 构建 AI Agent

> 来源: [Vercel](https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk) · 由本地 LLM 概括

**摘要**: 本文介绍了如何使用 Vercel AI SDK 构建 AI Agent，包括调用大语言模型、定义工具以及创建多步骤的代理循环。

## 要点

- 使用 `generateText` 函数调用大语言模型生成文本。
- 定义工具并将其与模型集成以执行特定任务。
- 通过配置 `stopWhen` 和 `stepCountIs` 参数实现多步推理。
- 在 Vercel 上部署 AI 代理，利用 Fluid 计算提供更长的函数运行时间和并发工作负载支持。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
