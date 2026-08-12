---
title: "agentic-ai-engineering：从零构建 AI Agent 教程"
date: 2026-01-25T08:00:00+08:00
tags: [AI, 文章]
summary: "`agentic-ai-engineering`是一个旨在帮助工程师从零开始构建AI代理的GitHub仓库。它提供了详细的教程，涵盖了从LLMAPI调用到生产评"
source: "https://github.com/agenticloops-ai/agentic-ai-engineering"
---

# agentic-ai-engineering：从零构建 AI Agent 教程

> 来源: [GitHub](https://github.com/agenticloops-ai/agentic-ai-engineering) · 由本地 LLM 概括

## 概述

`agentic-ai-engineering` 是一个旨在帮助工程师从零开始构建 AI 代理的 GitHub 仓库。它提供了详细的教程，涵盖了从 LLM API 调用到生产评估框架的整个过程。本文将详细介绍如何使用该仓库来构建自己的 AI 代理，并提供具体的操作步骤和代码示例。

## 快速入门

1. 安装 `uv` 工具：
   ```bash
   brew install uv
   ```
2. 或者通过 pipx 安装：
   ```bash
   pipx install uv
   ```
3. 克隆仓库：
   ```bash
   git clone https://github.com/agenticloops-ai/agentic-ai-engineering.git
   cd agentic-ai-engineering
   ```
4. 复制 `.env.example` 文件并添加 Anthropic 和/或 OpenAI 的 API 密钥：
   ```bash
   cp .env.example .env
   # 添加你的 Anthropic 和/或 OpenAI API 密钥
   ```
5. 运行第一个教程中的简单 LLM 调用示例：
   ```bash
   uv run --directory 01-foundations/01-simple-llm-call python 01_llm_call_anthropic.py
   ```

## 基础模块

### 简单的 LLM 调用

1. 在 `01-foundations` 目录中，找到并运行 `01_simple_llm_call.py` 文件：
   ```bash
   cd 01-foundations/01-simple-llm-call
   python 01_simple_llm_call.py
   ```
2. 查看输出结果，确保 LLM 调用成功。
3. 检查 `.env` 文件中的 API 密钥是否正确配置。

### 提示工程

1. 在 `01-foundations` 目录中，找到并运行 `02_prompt_engineering.py` 文件：
   ```bash
   cd 01-foundations/02-prompt-engineering
   python 02_prompt_engineering.py
   ```
2. 根据提示调整模型行为。
3. 观察输出结果，并记录下任何需要改进的地方。

### 工具使用

1. 在 `01-foundations` 目录中，找到并运行 `03_tool_use.py` 文件：
   ```bash
   cd 01-foundations/03-tool-use
   python 03_tool_use.py
   ```
2. 启用函数调用。
3. 观察工具使用的效果，并记录下任何需要改进的地方。

### 自主代理循环

1. 在 `01-foundations` 目录中，找到并运行 `04_agent_loop.py` 文件：
   ```bash
   cd 01-foundations/04-agent-loop
   python 04_agent_loop.py
   ```
2. 观察自主工具使用代理的行为。
3. 记录下任何需要改进的地方。

## 高级模块

### 结构化输出

1. 在 `03-advanced-techniques` 目录中，找到并运行 `01_structured_output.py` 文件：
   ```bash
   cd 03-advanced-techniques/01-structured-output
   python 01_structured_output.py
   ```
2. 使用 JSON 模式、模式和约束生成。
3. 观察输出结果，并记录下任何需要改进的地方。

### 流式处理

1. 在 `03-advanced-techniques` 目录中，找到并运行 `02_streaming.py` 文件：
   ```bash
   cd 03-advanced-techniques/02-streaming
   python 02_streaming.py
   ```
2. 使用 SSE、逐个 token 输出和流式工具调用。
3. 观察输出结果，并记录下任何需要改进的地方。

### 上下文工程

1. 在 `03-advanced-techniques` 目录中，找到并运行 `03_context_engineering.py` 文件：
   ```bash
   cd 03-advanced-techniques/03-context-engineering
   python 03_context_engineering.py
   ```
2. 使用窗口策略、总结和工具上下文。
3. 观察输出结果，并记录下任何需要改进的地方。

### 成本优化

1. 在 `04-testing-evaluation` 目录中，找到并运行 `01_prompt_caching.py` 文件：
   ```bash
   cd 04-testing-evaluation/01-prompt-caching
   python 01_prompt_caching.py
   ```
2. 使用提示缓存、模型路由。
3. 观察输出结果，并记录下任何需要改进的地方。

## 测试与评估

### 单元测试代理

1. 在 `04-testing-evaluation` 目录中，找到并运行 `02_unit_testing_agents.py` 文件：
   ```bash
   cd 04-testing-evaluation/02-unit-testing-agents
   python 02_unit_testing_agents.py
   ```
2. 模拟 LLM、确定性测试。
3. 观察输出结果，并记录下任何需要改进的地方。

### 评估框架

1. 在 `04-testing-evaluation` 目录中，找到并运行 `03_eval_frameworks.py` 文件：
   ```bash
   cd 04-testing-evaluation/03-eval-frameworks
   python 03_eval_frameworks.py
   ```
2. 使用 Promptfoo、Braintrust 和 Langfuse 整合。
3. 观察输出结果，并记录下任何需要改进的地方。

## 循环工程

### 技能

1. 在 `05-loop-engineering` 目录中，找到并运行 `01_skills.py` 文件：
   ```bash
   cd 05-loop-engineering/01-skills
   python 01_skills.py
   ```
2. 使用技能扩展代理。
3. 观察输出结果，并记录下任何需要改进的地方。

### 构建框架

1. 在 `06-frameworks` 目录中，找到并运行 `01_no_framework.py` 文件：
   ```bash
   cd 06-frameworks/01-no-framework
   python 01_no_framework.py
   ```
2. 使用原始 SDK 基线。
3. 观察输出结果，并记录下任何需要改进的地方。

## 生产模块

### 12 因素代理

1. 在 `07-production` 目录中，找到并运行 `01_12_factor_agents.py` 文件：
   ```bash
   cd 07-production/01-12-factor-agents
   python 01_12_factor_agents.py
   ```
2. 遵循生产级代理的原则。
3. 观察输出结果，并记录下任何需要改进的地方。

### 成本优化

1. 在 `07-production` 目录中，找到并运行 `02_cost_optimization.py` 文件：
   ```bash
   cd 07-production/02-cost-optimization
   python 02_cost_optimization.py
   ```
2. 使用令牌预算、缓存和模型路由。
3. 观察输出结果，并记录下任何需要改进的地方。

### 安全与护栏

1. 在 `07-production` 目录中，找到并运行 `03_security_guardrails.py` 文件：
   ```bash
   cd 07-production/03-security-guardrails
   python 03_security_guardrails.py
   ```
2. 使用认证、沙箱和注入防御。
3. 观察输出结果，并记录下任何需要改进的地方。

## 结论

通过以上步骤，你可以逐步构建自己的 AI 代理。每个模块都提供了详细的代码示例和学习目标，帮助你深入理解每一步的操作。希望这些操作指南能帮助你在构建 AI 代理的过程中取得成功！

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
