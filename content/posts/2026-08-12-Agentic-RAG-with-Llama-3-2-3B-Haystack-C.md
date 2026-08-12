---
title: "Agentic RAG with Llama 3.2 3B（Haystack Cookbook）"
date: 2026-08-12T08:00:00+08:00
tags: [AI, 文章]
summary: "本文介绍了如何使用Llama 3.2 3B模型构建一个基于知识库的Agentic Retrieval Augmented Generation (RAG)应用，该应用能在知识库中找不到答案时通过网络搜索获取更多信息。"
source: "https://haystack.deepset.ai/cookbook/llama32_agentic_rag"
---

# Agentic RAG with Llama 3.2 3B（Haystack Cookbook）

> 来源: [Haystack](https://haystack.deepset.ai/cookbook/llama32_agentic_rag) · 由本地 LLM 概括（原文经 Wayback Machine 快照抓取）

**摘要**: 本文介绍了如何使用Llama 3.2 3B模型构建一个基于知识库的Agentic Retrieval Augmented Generation (RAG)应用，该应用能在知识库中找不到答案时通过网络搜索获取更多信息。

## 要点

- 使用DuckDuckGo API进行网络搜索以补充知识库中的信息
- 利用SentenceTransformers生成文档向量并存储在内存数据库中
- 定义包含条件路由的提示模板来指导模型回答问题或返回“no_answer”
- 通过HyDE (Hypothetical Document Embeddings)改进检索效果

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
