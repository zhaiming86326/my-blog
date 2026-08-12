---
title: "Advance-RAG：混合检索、重排与融合实现"
date: 2026-01-11T08:00:00+08:00
tags: [AI, 文章]
summary: "Advance-RAG 是一个全面的生产级笔记本集合，专注于 Retrieval-Augmented Generation (RAG) 技术，包括 Query Expansion、Hybrid Search 和 Intelligent ReRanking 等关键模块。"
source: "https://github.com/MudassarHakim/Advance-RAG-ReRanking-FusionRetreival-RRF-HyDe"
---

# Advance-RAG：混合检索、重排与融合实现

> 来源: [GitHub](https://github.com/MudassarHakim/Advance-RAG-ReRanking-FusionRetreival-RRF-HyDe) · 由本地 LLM 概括

**摘要**: Advance-RAG 是一个全面的生产级笔记本集合，专注于 Retrieval-Augmented Generation (RAG) 技术，包括 Query Expansion、Hybrid Search 和 Intelligent ReRanking 等关键模块。

## 要点

- Hypothetical Document Embeddings (HyDe): 使用 LLM 生成假设文档进行查询扩展和检索。
- Fusion Retrieval: 结合向量（语义）和 BM25（关键词）检索，使用 RRF 进行多排名融合。
- Reranking Strategies: 采用两阶段检索策略，先快速获取再智能重排以提高相关性。
- Adaptive Retrieval: 根据查询类型动态选择最优检索策略的智能系统。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
