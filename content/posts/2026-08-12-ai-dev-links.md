---
title: "AI 开发教程与实践精选（2026-08-12）"
date: 2026-08-12T09:00:00+08:00
tags: [AI, 教程, 精选, 实践]
summary: "从网络搜集的 AI 开发教程与实践资源精选，共 15 条，附来源链接。"
---

> 由网络搜索自动搜集整理的 AI 开发教程与实践资源，按主题分组，标注来源与链接。内容为条目摘要，版权归原作者。

## LLM工程

- **AI 工程常见错误：企业采用 AI 时的十个坑**（tech.yahoo.com）：资深 AI 工程师总结企业落地 AI 的常见错误：混淆幻觉与 RAG、prompt 无人做版本管理、缺乏可观测性、忽视安全与合规等。 [链接](https://tech.yahoo.com/ai/chatgpt/articles/m-ai-engineer-mistakes-see-140000013.html)

## RAG

- **RAG-Tutorials：检索增强生成融合策略教程**（GitHub）：AI Review 2026 综述配套教程，用 Notebook 实现 BM25、FAISS、logits、latent 与参数化记忆等多样化的检索融合策略。 [链接](https://github.com/luffy06/RAG-Tutorials)
- **Advance-RAG：混合检索、重排与融合实现**（GitHub）：高级 RAG 进阶 Notebook：混合检索、RRF 融合、交叉编码器重排、查询改写与自适应检索的完整代码。 [链接](https://github.com/MudassarHakim/Advance-RAG-ReRanking-FusionRetreival-RRF-HyDe)
- **用 Chains 从零搭建 RAG 管道**（Baseten）：Baseten 官方示例：用 Chains 组件化地搭出最小可运行的 RAG 管道，含分步说明与代码。 [链接](https://docs.baseten.co/examples/chains-build-rag)

## Agent

- **Agentic RAG with Llama 3.2 3B（Haystack Cookbook）**（Haystack）：用 Llama 3.2 3B 与 Haystack 实现 agentic RAG：让模型自主决定走检索还是直接回答，附可运行 cookbook。 [链接](https://haystack.deepset.ai/cookbook/llama32_agentic_rag)
- **Agentic Loop 提示指南：如何驱动 AI 编码代理**（GitHub）：agentic 编码环境下的提示指南：用声明式、可验证的 prompt 让 AI 编码代理可靠地完成复杂任务。 [链接](https://github.com/allierays/agentic-loop/blob/HEAD/docs/PROMPTING-GUIDE.md)
- **用 Vercel AI SDK 构建 AI Agent**（Vercel）：Vercel 官方指南：用 AI SDK 实现工具调用、流式响应与多步骤 agent 循环，从零构建可部署的 agent。 [链接](https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk)
- **How to Build AI Agents: A Developer's Guide in 2026**（Scrimba）：面向开发者的 agent 构建指南：agent 循环五阶段（感知/推理/行动/观察/迭代）与主流工具链选型对比。 [链接](https://scrimba.com/articles/how-to-build-ai-agents/)
- **agentic-ai-engineering：从零构建 AI Agent 教程**（GitHub）：动手教程：从 LLM API 调用、提示工程、工具调用到完整 agent loop，配套可运行示例逐步构建 agent。 [链接](https://github.com/agenticloops-ai/agentic-ai-engineering)
- **agentic-ai-from-scratch：纯 Python 构建 Agent**（GitHub/Udacity）：Udacity 直播配套代码：不用任何框架，从单次 LLM 调用一步步演进到多 agent 工作流。 [链接](https://github.com/udacity/agentic-ai-from-scratch-webinar)

## 提示工程

- **开发者提示工程指南（中文）**（GitHub）：面向开发者的中文提示工程指南，覆盖代码审查、重构、单测生成、架构设计等场景的实战 prompt 写法。 [链接](https://github.com/microwind/ai-prompt/blob/main/docs/articles/developer_prompt_engineering_guide.md)
- **AI Prompting Guide：提示工程与情境工程双语手册**（GitHub）：开源中英双语手册：提示工程、情境工程，以及 2026 年 Claude Code / OpenAI Codex 等 agentic vibe coding 实践。 [链接](https://github.com/thc1006/ai-prompting-guide)

## AI编程

- **coding-with-ai：AI 编码助手工作流指南**（UDEL）：特拉华大学整理的 AI 编码助手实践指南：选择工具、组织任务、拆分变更与审查 AI 生成代码的工作流。 [链接](https://lem.che.udel.edu/git/furst/coding-with-ai)
- **Introduction to AI-assisted coding（昆士兰大学）**（UQ Library）：昆士兰大学图书馆培训课程：AI 辅助编程基础，含负责任使用、提示策略、输出质量评估与伦理要点。 [链接](https://uqlibrary.github.io/technology-training/GenAI/ai_assisted_coding/ai_assisted_coding.html)

## Copilot

- **GitHub Copilot Bootcamp：提示工程与定制**（GitHub）：Copilot 深度定制训练营：instructions、自定义 prompts 与 agents 三层配置，Week2 专讲提示工程与个性化。 [链接](https://github.com/Pwd9000-ML/GitHub-Copilot-Bootcamp/blob/master/Workshops/Week2/1-Prompt-Engineering-and-Customisation.md)

---

*本页由搜索整理脚本自动生成*