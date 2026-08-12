---
title: "用 Vercel AI SDK 构建 AI Agent"
date: 2025-11-03T08:00:00+08:00
tags: [AI, 文章]
summary: "本文将指导你如何使用Vercel和AISDK构建一个简单的AI代理。我们将从调用大型语言模型（LLM）、定义工具到创建能够根据用户输入执行任务的代理进行详细介绍"
source: "https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk"
---

# 用 Vercel AI SDK 构建 AI Agent

> 来源: [Vercel](https://vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk) · 由本地 LLM 概括

## 概述
本文将指导你如何使用 Vercel 和 AI SDK 构建一个简单的 AI 代理。我们将从调用大型语言模型（LLM）、定义工具到创建能够根据用户输入执行任务的代理进行详细介绍。

## 前提条件
在开始之前，请确保你已经：
- 拥有一个 Vercel 账户。
- 熟悉 TypeScript 和 Next.js。
- 从你的仪表板中创建了一个 AI Gateway 密钥。具体步骤请参阅 AI Gateway 开始指南中的第三步。
- 在项目中安装了 `ai` 和 `zod` 包。
- 安装了 Vercel CLI（可选，用于命令行部署）。

## 调用 LLM
构建代理的第一步是调用大型语言模型。AI SDK 提供了一个 API 可以使用各种模型生成文本。以下示例使用 OpenAI，但你也可以使用 Anthropic、Google、Mistral 等其他提供商。
```typescript
import { generateText } from 'ai';

export async function getWeather({ location }: string) {
  const { text } = await generateText({
    model: 'openai/gpt-5',
    prompt: `What is the weather like today in ${location}?`
  });
  console.log(text);
}
```
因为你在使用 AI Gateway 和 AI SDK，所以不需要安装和导入 openai 包；你可以仅通过字符串定义模型。更多详情请参阅 AI Gateway 文档。

## 使用工具
工具是模型可以调用的函数，用于执行特定任务。代理可以根据对话上下文使用这些工具来扩展其功能并执行操作。
### 工具的工作原理
当你向模型提供工具时，它可以根据用户的输入决定是否和如何使用它们。如果模型选择使用某个工具，则会返回一个结构化的响应，指示要调用的工具及其必要的参数：
```json
{
  "tool": "weather",
  "arguments": {
    "location": "San Francisco"
  }
}
```
AI SDK 自动处理以下内容：
- 从模型输出中提取工具调用。
- 根据 `inputSchema` 验证参数。
- 执行函数，并将调用及其结果存储在对话历史记录中。

### 定义工具
AI SDK 提供了一种使用 `tool` 函数定义工具的方法。该函数接受描述、输入模式（由 zod 定义）和执行函数作为参数。
```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';

export async function getWeather({ location }: string) {
  const { text } = await generateText({
    model: 'openai/gpt-5',
    prompt: `What is the weather in ${location}?`,
    tools: {
      weather: tool({
        description: 'Get the weather in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
        execute: async ({ location }) => ({
          location,
          temperature: 72 + Math.floor(Math.random() * 21) - 10
        })
      }),
      activities: tool({
        description: 'Get the activities in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the activities for') }),
        execute: async ({ location }) => ({
          location,
          activities: ['hiking', 'swimming', 'sightseeing']
        })
      })
    }
  });
  console.log(text);
}
```

## 创建代理
创建一个能够根据用户输入执行任务的代理。
```typescript
import { generateText, tool, stepCountIs } from 'ai';
import { z } from 'zod';

export const maxDuration = 60;

export async function POST(request: Request) {
  const { prompt }: { prompt?: string } = await request.json();
  if (!prompt) {
    return new Response('Prompt is required', { status: 400 });
  }
  const result = await generateText({
    model: 'openai/gpt-5',
    prompt,
    stopWhen: stepCountIs(5),
    tools: {
      weather: tool({
        description: 'Get the weather in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
        execute: async ({ location }) => ({
          location,
          temperature: 72 + Math.floor(Math.random() * 21) - 10
        })
      }),
      activities: tool({
        description: 'Get the activities in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the activities for') }),
        execute: async ({ location }) => ({
          location,
          activities: ['hiking', 'swimming', 'sightseeing']
        })
      })
    }
  });
  return Response.json({
    steps: result.steps,
    finalAnswer: result.text
  });
}
```

## 部署 AI 代理到 Vercel
要部署你的代理，请创建一个 API 路由并使用以下代码。代理将循环执行步骤，直到达到停止条件（即收到文本响应）。
```typescript
import { generateText, tool, stepCountIs } from 'ai';
import { z } from 'zod';

export const maxDuration = 60;

export async function POST(request: Request) {
  const { prompt }: { prompt?: string } = await request.json();
  if (!prompt) {
    return new Response('Prompt is required', { status: 400 });
  }
  const result = await generateText({
    model: 'openai/gpt-5',
    prompt,
    stopWhen: stepCountIs(5),
    tools: {
      weather: tool({
        description: 'Get the weather in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the weather for') }),
        execute: async ({ location }) => ({
          location,
          temperature: 72 + Math.floor(Math.random() * 21) - 10
        })
      }),
      activities: tool({
        description: 'Get the activities in a location',
        inputSchema: z.object({ location: z.string().describe('The location to get the activities for') }),
        execute: async ({ location }) => ({
          location,
          activities: ['hiking', 'swimming', 'sightseeing']
        })
      })
    }
  });
  return Response.json({
    steps: result.steps,
    finalAnswer: result.text
  });
}
```

## 部署到 Vercel
使用以下命令部署你的代理：
```bash
vercel deploy
```

## 测试代理
部署后，你可以使用 `curl` 测试你的代理。
```bash
curl -X POST https://your-project.vercel.app/api/agent \
-H "Content-Type: application/json" \
-d '{"prompt":"What is the weather in Tokyo?"}'
```
响应将包括代理的步骤和最终答案。

## 观察代理行为
部署后，你可以在 Vercel 仪表板中的“Observability”和“Logs”标签页中观察代理的行为。
### Observability 标签页
Observability 标签页提供了以下洞察：
- 每小时请求数量。
- 响应时间和延迟指标。
- 错误率和模式。
- 性能趋势。

### Logs 标签页
如果你在代理中添加了日志记录（使用 `console.log`、`console.error` 等），你可以在 Logs 标签页中查看这些日志。这对于调试工具执行和理解代理决策过程非常有帮助。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
