---
title: "Advance-RAG：混合检索、重排与融合实现"
date: 2026-01-11T08:00:00+08:00
tags: [AI, 文章]
summary: "Advance-RAG是一个专注于Retrieval-AugmentedGeneration(RAG)技术的综合教程集合，涵盖了查询扩展、混合搜索和智能重排序等"
source: "https://github.com/MudassarHakim/Advance-RAG-ReRanking-FusionRetreival-RRF-HyDe"
---

# Advance-RAG：混合检索、重排与融合实现

> 来源: [GitHub](https://github.com/MudassarHakim/Advance-RAG-ReRanking-FusionRetreival-RRF-HyDe) · 由本地 LLM 概括

## 概述
Advance-RAG 是一个专注于 Retrieval-Augmented Generation (RAG) 技术的综合教程集合，涵盖了查询扩展、混合搜索和智能重排序等先进主题。该仓库提供了生产级别的代码实现，并通过多个框架（LangChain 和 LlamaIndex）展示了实际应用案例。

## 项目结构
- **utils**: 包含辅助函数。
- **01_HyDe.ipynb**: 虚构文档嵌入 (HyDe) 实现。
- **02_fusion_retrieval.ipynb**: 混合检索实现。
- **03_reranking.ipynb**: 重排序策略实现。
- **04_query_transformations.ipynb**: 查询转换实现。
- **05_adaptive_retrieval.ipynb**: 自适应检索实现。
- **06_context_enrichment_window.ipynb**: 上下文增强窗口实现。
- **adv_sparse_embeddings.ipynb**: 先进稀疏嵌入实现。

## 技术栈
- **LLM Frameworks**: LangChain (LCEL, chains, retrievers), LlamaIndex (query engines, postprocessors)
- **Vector Databases**: FAISS (in-memory), ChromaDB (embedded), Milvus (production-scale)
- **Sparse Retrieval**: BM25 (statistical), SPLADE (neural sparse vectors), RRF (rank fusion)
- **Reranking**: Cross-Encoders, Cohere Rerank API
- **LLM Providers**: OpenAI (GPT-4o, GPT-4o-mini), Ollama (local), Cohere
- **Embeddings**: OpenAI embeddings, sentence-transformers, SPLADE
- **Tools**: Pydantic (structured outputs), pymupdf (PDF processing), deepeval (evaluation)

## 安装与配置

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   cd advanced-rag-tutorials
   ```

2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   - 复制示例 `.env` 文件：
     ```bash
     cp .env.example .env
     ```
   - 编辑 `.env` 并添加 API 密钥：
     ```ini
     OPENAI_API_KEY=your_openai_api_key_here
     COHERE_API_KEY=your_cohere_api_key_here (optional)
     ```

4. 启动 Jupyter Notebook 或 JupyterLab：
   - 打开任意一个笔记本文件：
     ```bash
     jupyter notebook 01_HyDe.ipynb
     ```
   - 使用 JupyterLab：
     ```bash
     jupyter lab
     ```

5. 如果使用 Milvus（稀疏嵌入笔记本）：
   - 启动 Docker 容器：
     ```bash
     bash standalone_embed.sh start
     ```

## 常见问题与解决方法

- **连接错误**：确保 Docker 正在运行。如果在笔记本中遇到 `ConnectionNotExistException`，请检查 `MilvusClient` 和 `connections.connect` 设置是否匹配你的 Docker 端口（默认为 19530）。
- **索引错误**：稀疏向量需要在加载前创建索引。现在每个笔记本都包含自动处理此问题的逻辑（`ensure_milvus_ready`）。
- **磁盘空间不足**：Milvus 在 `volumes/` 目录中存储数据。如果搜索失败，请确保有足够的磁盘空间。

## 详细教程

### Hypothetical Document Embeddings (HyDe)
1. 打开 HyDe 笔记本：
   ```bash
   jupyter notebook 01_HyDe.ipynb
   ```
2. 理解关键概念：
   - 使用 LLM 生成的假设文档进行查询扩展。
   - 基于假设答案和原始查询的检索。
3. 实现细节：
   - 自定义 `HyDERetriever` 类。
   - LangChain 的 `HypotheticalDocumentEmbedder`。
   - LlamaIndex 的 `HyDEQueryTransform`。

### Fusion Retrieval
1. 打开 Fusion Retrieval 笔记本：
   ```bash
   jupyter notebook 02_fusion_retrieval.ipynb
   ```
2. 理解关键概念：
   - 混合检索：稠密（BM25）和稀疏（SPLADE）嵌入的结合。
3. 实现细节：
   - 自定义 `Milvus` 集成。
   - 使用 RRF 进行排名。

### 重排序策略
1. 打开重排序策略笔记本：
   ```bash
   jupyter notebook 03_reranking.ipynb
   ```
2. 理解关键概念：
   - 使用交叉编码器进行重排序。
3. 实现细节：
   - 自定义 `Cross-Encoders` 和 Cohere Rerank API。

### 查询转换
1. 打开查询转换笔记本：
   ```bash
   jupyter notebook 04_query_transformations.ipynb
   ```
2. 理解关键概念：
   - 调整参数以优化检索结果。
3. 实现细节：
   - 使用不同的 alpha 值、重排序阈值和上下文窗口大小。

### 自适应检索
1. 打开自适应检索笔记本：
   ```bash
   jupyter notebook 05_adaptive_retrieval.ipynb
   ```
2. 理解关键概念：
   - 根据用户查询动态调整检索策略。
3. 实现细节：
   - 使用 LLM 提供商和嵌入工具。

### 上下文增强窗口
1. 打开上下文增强笔记本：
   ```bash
   jupyter notebook 06_context_enrichment_window.ipynb
   ```
2. 理解关键概念：
   - 增强检索结果的上下文信息。
3. 实现细节：
   - 使用 FAISS 和 OpenAI 嵌入。

### 先进稀疏嵌入
1. 打开先进稀疏嵌入笔记本：
   ```bash
   jupyter notebook adv_sparse_embeddings.ipynb
   ```
2. 理解关键概念：
   - BM25 和 SPLADE 的混合检索。
3. 实现细节：
   - 使用 Milvus 进行大规模稀疏向量存储和索引。

## 评估框架

- **evaluation_deep_eval.ipynb**: 深度评估框架集成。
- **evaluation_grouse.ipynb**: GROUSE 评估指标。
- **define_evaluation_metrics.ipynb**: 自定义评估指标定义。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
