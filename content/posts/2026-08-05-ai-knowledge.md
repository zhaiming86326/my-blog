---
title: "2026-08-05 AI 知识库日报"
date: 2026-08-05T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 4 条对话,提炼 4 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(4/4 条有效)。
> 信息来源分布:Codex VSCode 扩展 (本地)(2条)、Continue (本地)(1条)、Roo Code (本地)(1条)

## 今日知识要点

### 如何屏蔽 Markdown 文件中的 TypeScript 代码警告
- **核心结论**: 在 Markdown 文件中写 TypeScript 代码块时，可以通过添加 `// @ts-nocheck` 来屏蔽编辑器的警告。
- **关键要点**:
  - 在每个 `ts` 代码块第一行添加 `// @ts-nocheck`。
  - 这种方法保留了 TypeScript 语法高亮，但让编辑器不要检查这些 Markdown 示例代码。
  - 如果警告来自 VS Code 插件，可以按来源关闭相关插件。
- **信息来源**: Codex VSCode 扩展 (本地)

### 从零开始学习 Agent 开发的要点
- **核心结论**: 从零开始学习 Agent 开发需要记录基础组成、工程结构、常见坑、测试评估和下一步计划。
- **关键要点**:
  - 记录常用语言和框架信息，如 JavaScript/TypeScript、Python、Java 等。
  - 记录每种语言的核心开发信息，如项目结构、包管理方式、构建方式、测试方式等。
  - 记录常用的开发框架版本及其优缺点。
- **信息来源**: Codex VSCode 扩展 (本地)

### 如何避免 AI 提供的代码过时
- **核心结论**: 建立一套可持续更新、可检索、可约束 AI 行为的工程知识系统。
- **关键要点**:
  - 不要试图一次性穷举所有语言和框架。
  - 建立分层知识库，记录常用语言的核心开发信息。
  - 定期更新知识库，确保信息准确。
- **信息来源**: Codex VSCode 扩展 (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(text)
```text
TypeScript
- 包管理：npm / pnpm / yarn
- 构建：tsc / vite / next / tsup
- 测试：vitest / jest / playwright
- 格式化：prettier / eslint
- 常见框架：React / Next.js / NestJS / Express
```
### 片段 2(text)
```text
frontend/
  React
  Vue
  Svelte
  Next.js
  Nuxt
  Vite

backend/
  Express
  NestJS
  Fastify
  Django
  FastAPI
  Flask
  Spring Boot
  Gin
  Fiber

database/
  Prisma
  Drizzle
  SQLAlchemy
  TypeORM
  Hibernate

mobile/
  React Native
  Flutter
  SwiftUI
  Android Compose

ai-agent/
  LangChain
  LlamaIndex
  OpenAI Agents SDK
  Vercel AI SDK
  AutoGen
  CrewAI
  MCP
```
### 片段 3(text)
```text
我要实现什么功能？
用户怎么使用？
输入是什么？
输出是什么？
边界情况是什么？
哪些文件可以改？
哪些文件不能改？
是否需要测试？
是否需要兼容旧逻辑？
```
### 片段 4(text)
```text
帮我加一个登录功能
```
### 片段 5(text)
```text
在现有 Next.js 项目中添加邮箱密码登录。
只修改 app/login 和 lib/auth 相关文件。
使用现有 UI 组件。
登录成功后跳转 /dashboard。
失败时显示错误信息。
不要引入新的状态管理库。
需要增加基础测试。
```
### 片段 6(text)
```text
先阅读项目结构、依赖、已有代码风格，再决定实现方案。
优先复用现有工具函数、组件、类型和测试方式。
不要引入新框架，除非明确说明原因。
```
### 片段 7(text)
```text
完成后运行：
- 类型检查
- 单元测试
- 构建
- lint
```
### 片段 8(text)
```text
实现后请运行 npm test 和 npm run build。
如果失败，继续修复直到通过。
```
### 片段 9(text)
```text
language-framework-knowledge.md
coding-agent-guidelines.md
project-context-rules.md
```
### 片段 10(text)
```text
- 先读代码，再改代码。
- 优先复用现有模式。
- 不随意引入依赖。
- 不修改无关文件。
- 不删除用户已有代码。
- 修改后必须说明改了什么。
- 能跑测试就跑测试。
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
