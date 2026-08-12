---
title: "agentic-ai-from-scratch：纯 Python 构建 Agent"
date: 2026-06-25T08:00:00+08:00
tags: [AI, 文章]
summary: "本文介绍了如何使用纯Python构建一个简单的AI代理，该过程基于Udacity的一小时网络研讨会。整个教程通过一系列脚本逐步展示了从基本的LLM调用到多代理协"
source: "https://github.com/udacity/agentic-ai-from-scratch-webinar"
---

# agentic-ai-from-scratch：纯 Python 构建 Agent

> 来源: [GitHub/Udacity](https://github.com/udacity/agentic-ai-from-scratch-webinar) · 由本地 LLM 概括

## 概述

本文介绍了如何使用纯Python构建一个简单的AI代理，该过程基于Udacity的一小时网络研讨会。整个教程通过一系列脚本逐步展示了从基本的LLM调用到多代理协作的工作流构建。每个步骤都详细记录了所需的命令和代码片段。

## 先决条件与环境设置

### 1. 安装依赖项
首先，确保安装了Python 3.11+版本，并准备好Azure CLI。接下来，创建必要的资源组、Azure OpenAI资源以及RBAC启用的Key Vault。

```bash
az login
az group create --name agents-webinar-rg --location eastus

az cognitiveservices account create \
  --name <unique-openai-resource-name> \
  --resource-group agents-webinar-rg \
  --location eastus \
  --kind OpenAI \
  --sku S0 \
  --custom-domain <unique-openai-resource-name>

az keyvault create \
  --name <unique-vault-name> \
  --resource-group agents-webinar-rg \
  --location eastus \
  --enable-rbac-authorization true
```

### 2. 配置Key Vault
在Microsoft Foundry门户中，部署`gpt-4.1-mini`模型，并给它一个有意义的名字。然后，在Key Vault中创建必要的秘密。

```bash
az role assignment create \
  --role "Key Vault Secrets Officer" \
  --assignee <your-sign-in-email> \
  --scope /subscriptions/<subscription-id>/resourceGroups/agents-webinar-rg/providers/Microsoft.KeyVault/vaults/<unique-vault-name>
```

在Key Vault中创建以下秘密：

| Secret name | Value |
|-------------|-------|
| aoai-endpoint | https://<resource-name>.openai.azure.com |
| aoai-key | Azure OpenAI key 1 or key 2 |
| aoai-deployment | Your deployment name, for example webinar-gpt-41-mini |

### 3. 配置环境变量
在本地创建一个`.env`文件，并添加以下内容：

```plaintext
WEBINAR_KEY_VAULT_URL=https://<unique-vault-name>.vault.azure.net/
```

## 构建基础LLM调用

### 1. 运行基本的LLM调用
运行脚本以进行一次简单的LLM调用。

```bash
python 01_model_call.py
```

该脚本会提出一个关于搬迁的问题，但不会提供角色或个人背景信息。输出将显示模型的回答。

### 2. 分析问题与回答
暂停并询问参与者：
- 模型应该扮演什么角色？
- 它对即将搬家的人了解多少？
- 应该用什么样的约束来指导它的答案？
- 它应该产生哪种类型的答案？

## 添加上下文和个人背景

### 1. 运行带有个人背景的LLM调用
运行脚本以添加个人背景信息。

```bash
python 02_persona_call.py
```

该脚本提供了一个角色和一个特定区域的知识。通过对比回答，可以识别出以下三个概念：
- 角色：Riley的身份及其沟通方式；
- 知识：Riley可能使用的奥斯汀地区的事实；
- 范围：Riley只回答与其角色相关的提问。

### 2. 分析输出
观察输出并讨论这些概念如何影响模型的回答。强调这是LLM调用，尚未包含持久记忆、工具或行动循环。

## 构建代理类

### 1. 运行单个代理脚本
运行脚本来构建一个简单的代理类。

```bash
python 03_single_agent.py
```

该脚本定义了一个`HousingAgent`类，并展示了其四个组成部分：角色、知识、工具和记忆。通过对比两个实例的回答，强调了持久记忆的重要性。

### 2. 分析输出
观察每次调用的详细过程，包括内存读写和历史记录。讨论温度设置为零以减少无关变异性。

## 让代理选择工具

### 1. 运行代理循环脚本
运行脚本来让代理根据需要选择工具。

```bash
python 04_agent_loop.py
```

该脚本创建了一个`AgentLoop`实例，并展示了决策、行动、观察和循环的概念。强调代理决定，而确定性运行时控制执行。

### 2. 分析输出
观察打印的跟踪信息，理解每个步骤的具体含义。

## 改进答案通过代理反馈

### 1. 运行协作脚本
运行脚本来展示评估者-优化者的模式。

```bash
python 05_agent_collaboration.py
```

该脚本展示了两个代理如何合作以改进最终答案。强调不同责任的代理可以提高质量，而不仅仅是将工作分解为顺序步骤。

### 2. 分析输出
观察打印的消息，理解反馈循环的具体含义。

## 构建路由代理工作流

### 1. 运行路由代理脚本
运行脚本来构建一个路由代理工作流。

```bash
python 06_routed_workflow.py
```

该脚本定义了两个类：`RouterAgent`和`HomeFindingWorkflow`。通过终端跟踪，展示了每个阶段的详细信息，并强调代理之间消息传递的具体方式。

### 2. 分析输出
观察终端中的每一步骤，理解路由验证和工作流控制的概念。尝试通过更改`main()`函数中的字符串来测试不同的提示。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
