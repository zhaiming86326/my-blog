---
title: "用 Chains 从零搭建 RAG 管道"
date: 2026-08-12T08:00:00+08:00
tags: [AI, 文章]
summary: "本文将指导读者从零开始使用Chains库构建一个检索增强生成（RAG）管道。我们将详细介绍如何设置环境、创建必要的组件以及测试和部署该系统。"
source: "https://docs.baseten.co/examples/chains-build-rag"
---

# 用 Chains 从零搭建 RAG 管道

> 来源: [Baseten](https://docs.baseten.co/examples/chains-build-rag) · 由本地 LLM 概括

## 概述

本文将指导读者从零开始使用Chains库构建一个检索增强生成（RAG）管道。我们将详细介绍如何设置环境、创建必要的组件以及测试和部署该系统。

## 前提条件

在开始之前，你需要安装uv并拥有Baseten账户及其API密钥。如果你打算在本地调试模式下运行此示例，还需要安装`chromadb`：

```bash
pip install chromadb
```

完整的代码可以在Chains的示例仓库中找到。

## 项目结构与初始化

1. 创建一个新的目录，并在其中创建一个名为`rag.py`的文件：
    ```bash
    mkdir rag
    touch rag/rag.py
    cd rag
    ```

2. 在`rag.py`文件中定义三个主要组件：`VectorStore`、`LLMClient`和`RAG`。

## Vector store Chainlet

1. 定义一个名为`VectorStore`的类，继承自Chains的`ChainletBase`：
    ```python
    import truss_chains as chains
    
    class VectorStore(chains.ChainletBase):
        remote_config = chains.RemoteConfig(
            docker_image=chains.DockerImage(pip_requirements=["chromadb"])
        )
        
        def __init__(self):
            import chromadb
            self._chroma_client = chromadb.EphemeralClient()
            self._collection = self._chroma_client.create_collection(name="bios")
            
            documents = [
                # 示例文档...
            ]
            self._collection.add(documents=documents, ids=[f"id{n}" for n in range(len(documents))])
        
        async def run_remote(self, query: str) -> list[str]:
            results = self._collection.query(query_texts=[query], n_results=2)
            if not results or not results["documents"] or not results["documents"][0]:
                raise ValueError("No bios returned from the query")
            return results["documents"][0]
    ```

## LLM inference stub

1. 定义一个名为`LLMClient`的类，继承自Chains的`StubBase`：
    ```python
    class LLMClient(chains.StubBase):
        async def run_remote(self, new_bio: str, bios: list[str]) -> str:
            prompt = f"""You are matching alumni of a college to help them make connections. Explain why the person described first would want to meet the people selected from the matching database.
            Person you're matching:
            {new_bio}
            People from database:
            {' '.join(bios)}
            """
            resp = await self._remote.predict_async(json_payload={"messages": [{"role": "user", "content": prompt}], "stream": False})
            return resp["output"][len(prompt):].strip()
    ```

## RAG entrypoint Chainlet

1. 定义一个名为`RAG`的类，继承自Chains的`ChainletBase`：
    ```python
    @chains.mark_entrypoint
    class RAG(chains.ChainletBase):
        def __init__(self, vector_store: VectorStore = chains.depends(VectorStore),
                     context: chains.DeploymentContext = chains.depends_context()):
            self._vector_store = vector_store
            self._llm = LLMClient.from_url(LLM_URL, context)
        
        async def run_remote(self, new_bio: str) -> str:
            bios = await self._vector_store.run_remote(new_bio)
            contacts = await self._llm.run_remote(new_bio, bios)
            return contacts
    ```

## 测试本地运行

1. 设置Baseten API密钥作为环境变量：
    ```bash
    export BASETEN_API_KEY=your_api_key_here
    ```

2. 运行`rag.py`文件以测试本地行为：
    ```python
    if __name__ == "__main__":
        import os
        import asyncio
        
        with chains.run_local(secrets={"baseten_chain_api_key": os.environ["BASETEN_API_KEY"]}):
            rag_client = RAG()
            result = asyncio.run(rag_client.run_remote("""
                Sam just moved to Manhattan for his new job at a large bank.
                In college, he enjoyed building sets for student plays.
                """))
            print(result)
    ```

3. 运行脚本：
    ```bash
    python rag.py
    ```

## 部署到生产环境

1. 使用`truss chains push`命令部署Chain：
    ```bash
    truss chains push rag.py
    ```

2. 通过API端点调用部署的Chain。可以通过cURL或Python脚本实现：

### cURL示例
```bash
curl -X POST 'https://chain-abc123.api.baseten.co/production/run_remote' \
-H "Authorization: Bearer $BASETEN_API_KEY" \
-d '{"new_bio": "Sam just moved to Manhattan for his new job at a large bank. In college, he enjoyed building sets for student plays."}'
```

### Python脚本示例
```python
import requests
import os

RAG_CHAIN_URL = ""
baseten_api_key = os.environ["BASETEN_API_KEY"]

if not RAG_CHAIN_URL:
    raise ValueError("Please insert the URL for the RAG chain.")

new_bio = (
    "Sam just moved to Manhattan for his new job at a large bank. "
    "In college, he enjoyed building sets for student plays."
)
resp = requests.post(RAG_CHAIN_URL,
                     headers={"Authorization": f"Bearer {baseten_api_key}"},
                     json={"new_bio": new_bio})
print(resp.json())
```

3. 使用`truss chains push --watch rag.py`命令在开发过程中进行迭代。

通过以上步骤，你可以成功地从零开始构建并部署一个RAG管道。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
