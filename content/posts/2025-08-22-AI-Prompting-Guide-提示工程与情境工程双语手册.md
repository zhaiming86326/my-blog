---
title: "AI Prompting Guide：提示工程与情境工程双语手册"
date: 2025-08-22T08:00:00+08:00
tags: [AI, 文章]
summary: "AI提示词宝典（AIPromptingGuide）是一本免费的双语手册，涵盖了提示工程、情境工程以及2026年的代理式编程（agentic vibe coding）与Claude Code/OpenAI Codex 等AI编码代理的实践方法。"
source: "https://github.com/thc1006/ai-prompting-guide"
---

# AI Prompting Guide：提示工程与情境工程双语手册

> 来源: [GitHub](https://github.com/thc1006/ai-prompting-guide) · 由本地 LLM 概括

## 概述

AI 提示词宝典（AI Prompting Guide）是一本免费的双语手册，涵盖了提示工程、情境工程以及2026年的代理式编程（agentic "vibe" coding）。本书由蔡秀吉撰写，并使用Docusaurus 3构建。本文档将详细介绍如何安装和运行此项目，以及其内容结构。

## 安装与运行

要本地开发AI提示词宝典，请按照以下步骤操作：

1. **安装依赖项**
   ```bash
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm start
   ```
   这将在`http://localhost:3000`上启动开发服务器。

3. **构建生产版本**
   ```bash
   npm run build
   ```
   此命令将生成双语版本的文档，输出路径为`./build`。

4. **本地运行生产版本**
   ```bash
   npm run serve
   ```

## 项目结构

AI提示词宝典项目的文件结构如下：

- `docs/`: 包含英文源文档。
- `i18n/zh-TW/`: 包含繁体中文翻译和主题字符串。
- `blog/`: 包含博客文章。
- `src/`: 包含主页、React组件和自定义CSS。
- `static/`: 包含图片和其他静态资源。
- `docusaurus.config.js`: 网站配置文件。
- `sidebars.js`: 文档侧边栏结构。

## 内容概览

### 基础知识

- **提示工程简介**: 介绍什么是提示、提示结构和常见模式，以及快速入门指南。
- **提示与情境工程**: 描述从2025年至2026年的过渡期，重点介绍Claude Code和OpenAI Codex的领域指南、项目上下文文件（CLAUDE.md / AGENTS.md）、代理式工作流程、规格驱动开发、套件工程以及验证/安全/工程纪律（TDD、小CLs、少年童子军规则）。
- **实用教程**: 包括内容创作、代码生成和数据分析等内容。

### 高级技术

- **链式思考与提示链**: 介绍链式思考方法和多模态提示。
- **最佳实践**: 包含测试与优化、生产部署、安全与伦理以及团队协作的最佳实践。

### 应用案例研究

- **商业智能**: 提供企业部署案例研究。
- **博客**: 记录关于提示工程教育及相关主题的笔记。

## 贡献指南

- **问题和拉取请求**：欢迎在`github.com/thc1006/ai-prompting-guide`上提交问题和拉取请求。
- **文档同步**：请确保英文源文档与繁体中文翻译保持一致，位于`docs/`和`i18n/zh-TW/`目录下。

## 许可证

AI提示词宝典遵循Apache License 2.0许可协议。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
