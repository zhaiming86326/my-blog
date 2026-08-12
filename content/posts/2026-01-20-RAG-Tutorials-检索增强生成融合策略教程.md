---
title: "RAG-Tutorials：检索增强生成融合策略教程"
date: 2026-01-20T08:00:00+08:00
tags: [AI, 文章]
summary: "本教程介绍了RAG（Retrieval-AugmentedGeneration）融合策略的实现，包括几种不同的方法：`none`、`query`、`logits"
source: "https://github.com/luffy06/RAG-Tutorials"
---

# RAG-Tutorials：检索增强生成融合策略教程

> 来源: [GitHub](https://github.com/luffy06/RAG-Tutorials) · 由本地 LLM 概括

## 概述

本教程介绍了RAG（Retrieval-Augmented Generation）融合策略的实现，包括几种不同的方法：`none`、`query`、`logits`、`latent` 和 `parametric`。这些方法旨在通过检索增强生成来改进自然语言处理任务的表现。

## 代码结构

### 源码目录
- **src/main.py**: 统一的推理入口，支持多种融合策略。
- **src/train_latent.py**: 训练 latent 融合适配器的脚本。
- **src/train_parametric.py**: 训练文档级参数化 LoRA 适配器的脚本。
- **src/fusion/**: 各种融合实现。
- **src/retriever/**: BM25 和 FAISS 检索器实现。
- **scripts/**: 准备好的 shell 脚本，用于训练和推理。

### 环境配置
```bash
conda activate ragdemo
```

## 推理脚本

### 基线模型推理
```bash
bash scripts/run.sh
```

### 查询融合推理
```bash
bash scripts/run_query.sh
```

### 对数融合推理
```bash
bash scripts/run_logits.sh
```

### 潜在融合推理
```bash
bash scripts/run_latent.sh
```

### 参数化融合推理
```bash
bash scripts/run_parametric.sh
```

## 训练脚本

### 训练潜在融合适配器
```bash
bash scripts/train_latent.sh
```

### 训练文档级参数化 LoRA 适配器
```bash
bash scripts/train_parametric.sh
```

## 主命令行接口 (CLI)

统一入口：
```bash
python -m src.main \
  --dataset hotpotqa/hotpot_qa \
  --config distractor \
  --split validation \
  --model-name Qwen/Qwen2.5-1.5B \
  --fusion none
```

重要参数说明：
- `--fusion`: 可选值为 `none`、`query`、`logits`、`latent` 和 `parametric`
- `--retriever`: 可选值为 `bm25` 或 `faiss`
- `--encoder-model-name`: 仅在使用 FAISS 时需要
- `--user-prompt`: 提示模板；对于查询风格的文本插入，使用 `{context}`
- `--top-k`: 检索到的邻居数量
- `--max-samples`: 仅评估一小部分样本用于快速测试
- `--logits-lambda`: 对于对数融合使用的混合权重
- `--latent-checkpoint`: 训练好的潜在适配器检查点路径
- `--parametric-checkpoint`: 训练好的参数化适配器银行路径
- `--lora-rank`、`--lora-alpha`: LoRA 配置

## 方法说明

### 查询融合 (Query Fusion)
当前实现是最简单的形式：使用 BM25 检索，将检索到的内容插入用户提示中的 `{context}` 位置，然后进行生成。

示例提示模板：
```plaintext
Use the retrieved context to answer the question.

Question: {question}

{context}

Answer:
```

### 对数融合 (Logits Fusion)
这是一个最小版本。对于每个查询，模型会执行以下步骤：
1. 使用 BM25 检索邻居。
2. 为每个邻居构建一个增强的提示。
3. 从每个邻居提示中读取下一个标记分布。
4. 根据检索得分加权邻居目标。
5. 将邻居分布与基础模型分布混合。

### 潜在融合 (Latent Fusion)
当前实现假设：
- 检索使用 FAISS 和 sentence-transformer 向量。
- 基础模型冻结。
- 仅训练潜在投影层。
- 加权检索嵌入注入到 QKV 投影输出中。

### 参数化融合 (Parametric Fusion)
当前实现假设：
- 每个文档拥有一个 LoRA 适配器。
- 训练使用检索到的邻居文档来帮助重构目标文档。
- 推理时检索相关文档，加载其适配器，并在生成前计算加权平均适配器。

## 状态

该仓库目前仍处于教程代码阶段。实现有意保持简单，旨在逐个方法迭代改进。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
