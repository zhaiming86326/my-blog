---
title: "Agentic RAG with Llama 3.2 3B（Haystack Cookbook）"
date: 2026-08-12T08:00:00+08:00
tags: [AI, 文章]
summary: "本文档将详细介绍如何使用Llama3.23B构建一个AgenticRetrievalAugmentedGeneration(RAG)应用程序。我们将通过具体的步"
source: "https://haystack.deepset.ai/cookbook/llama32_agentic_rag"
---

# Agentic RAG with Llama 3.2 3B（Haystack Cookbook）

> 来源: [Haystack](https://haystack.deepset.ai/cookbook/llama32_agentic_rag) · 由本地 LLM 概括

## 概述
本文档将详细介绍如何使用 Llama 3.2 3B 构建一个 Agentic Retrieval Augmented Generation (RAG) 应用程序。我们将通过具体的步骤和代码示例，展示如何从数据准备、模型加载到构建 RAG 管道的整个过程。

## 前言
在 Meta 的 Llama 3.2 收集中，Meta 发布了两个小型但强大的语言模型。本文档将使用其中的 3B 模型来构建一个 Agentic RAG 应用程序，该应用程序能够从知识库中回答问题，并在无法找到答案时通过网络搜索获取额外上下文。

## 环境准备
### 安装依赖包

首先确保安装了所有必要的 Python 包。可以通过以下命令进行安装：

```bash
pip install haystack-ai duckduckgo-api-haystack transformers sentence-transformers datasets
```

## 数据集加载与预处理
### 下载数据集

我们将使用 Hugging Face 的 `datasets` 库下载有关古代世界七大奇迹的数据集。

```python
from datasets import load_dataset

dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
```

### 创建文档对象并添加元数据

将每个文档的内容和元数据封装到 `Document` 对象中，并存储在内存数据库中：

```python
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Document

document_store = InMemoryDocumentStore()
docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]
doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
doc_embedder.warm_up()
docs_with_embeddings = doc_embedder.run(docs)
document_store.write_documents(docs_with_embeddings["documents"])
```

## 模型加载
### 授权与模型加载

需要一个 Hugging Face 账户并接受 Meta 的条件。然后使用以下代码加载 Llama 3.2-3B 模型：

```python
import getpass, os

os.environ["HF_TOKEN"] = getpass.getpass("Your Hugging Face token")
```

### 加载模型

使用 Hugging Face Transformers 库加载模型，并进行预热以准备推理。

```python
from haystack.components.generators import HuggingFaceLocalGenerator
import torch

generator = HuggingFaceLocalGenerator(
    model="meta-llama/Llama-3.2-3B-Instruct",
    huggingface_pipeline_kwargs={"device_map": "auto", "torch_dtype": torch.bfloat16},
    generation_kwargs={"max_new_tokens": 256}
)
generator.warm_up()
```

## 构建 Agentic RAG 管道
### 初始化检索组件

初始化用于初始检索阶段的嵌入和检索器：

```python
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
retriever = InMemoryEmbeddingRetriever(document_store, top_k=5)
```

### 定义提示模板

定义用于生成提示的模板，该模板指示模型根据检索到的文档回答查询：

```python
from haystack.components.builders import PromptBuilder

prompt_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Answer the following query given the documents.
If the answer is not contained within the documents reply with 'no_answer'.
If the answer is contained within the documents, start the answer with "FROM THE KNOWLEDGE BASE: ".
Documents:
{
% for document in documents %}
{{document.content}}
{
% endfor %}
Query: {{query}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

prompt_builder = PromptBuilder(template=prompt_template)
```

### 定义条件路由器

定义一个条件路由器组件，根据模型的回复进行数据路由：

```python
from haystack.components.routers import ConditionalRouter

routes = [
    {
        "condition": "{{'no_answer' in replies[0]}}",
        "output": "{{query}}",
        "output_name": "go_to_websearch",
        "output_type": str,
    },
    {
        "condition": "{{'no_answer' not in replies[0]}}",
        "output": "{{replies[0]}}",
        "output_name": "answer",
        "output_type": str,
    }
]
```

## 运行 Agentic RAG 管道
### 构建并运行管道

构建完整的 Agentic RAG 管道，并通过一个示例查询进行测试：

```python
from haystack.components import Pipeline

pipeline = Pipeline()
pipeline.add_component(generator, name="generator")
pipeline.add_component(prompt_builder, name="prompt_builder")
pipeline.add_component(retriever, name="retriever")
pipeline.add_component(ConditionalRouter(routes), name="router")

# 示例查询
query = "What is the capital of France?"
response = pipeline.run(prompt=query)
print(response["answer"])
```

通过以上步骤，你可以成功构建并运行一个 Agentic RAG 管道。这将帮助你在知识库中找到答案，并在必要时进行网络搜索以获取更多信息。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
