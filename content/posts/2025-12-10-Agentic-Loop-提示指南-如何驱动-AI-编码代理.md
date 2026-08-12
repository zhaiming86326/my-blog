---
title: "Agentic Loop 提示指南：如何驱动 AI 编码代理"
date: 2025-12-10T08:00:00+08:00
tags: [AI, 文章]
summary: "AgenticLoop提供了一套详细的提示指南，帮助开发者更有效地与AI编码助手进行交互。本文将详细介绍如何使用这些技巧来提高生成代码的质量，并提供具体的实践步"
source: "https://github.com/allierays/agentic-loop/blob/HEAD/docs/PROMPTING-GUIDE.md"
---

# Agentic Loop 提示指南：如何驱动 AI 编码代理

> 来源: [GitHub](https://github.com/allierays/agentic-loop/blob/HEAD/docs/PROMPTING-GUIDE.md) · 由本地 LLM 概括

## 概述
Agentic Loop 提供了一套详细的提示指南，帮助开发者更有效地与AI编码助手进行交互。本文将详细介绍如何使用这些技巧来提高生成代码的质量，并提供具体的实践步骤。

## 基础知识
### 1. 具体化需求
- **示例**：明确描述功能细节。
    - 不佳示例：
        ```plaintext
        "Build a login form"
        ```
    - 改进示例：
        ```plaintext
        "Build a login form with email and password fields. Include:
        Client-side validation (email format, password min 8 chars)
        Error messages shown below each field
        Loading state on submit button
        Redirect to /dashboard on success
        Use our existing Button and Input components from @/components/ui"
        ```
- **要点**：
    - 明确列出所有需求。
    - 包含具体的技术细节，如组件、库等。

### 2. 指定技术栈
- **示例**：明确指定使用的库和框架。
    - 不佳示例：
        ```plaintext
        "Add form validation"
        ```
    - 改进示例：
        ```plaintext
        "Add form validation using react-hook-form and zod. Follow the patterns in our existing UserForm component."
        ```
- **要点**：
    - 指定使用的库和框架。
    - 引用现有代码中的模式。

### 3. 参考现有模式
- **示例**：参考现有的API端点结构。
    ```plaintext
    "Create a POST /api/users endpoint following the same pattern as our existing /api/products endpoint. Use the same error handling and response format."
    ```
- **要点**：
    - 引用现有代码中的模式和结构。
    - 确保一致性。

## 高级提示技巧
### 1. 先写测试（TDD）
- **示例**：先编写测试用例，再实现功能。
    ```plaintext
    "Before implementing this feature, write the tests first. I want to see the failing tests, then we'll implement the code to make them pass."
    ```
- **要点**：
    - 强制AI考虑代码逻辑和边界条件。
    - 有助于发现潜在问题。

### 2. 考虑可能出错的地方
- **示例**：预测代码中的潜在错误点。
    ```plaintext
    "What could go wrong with this code? What errors should we handle?"
    ```
- **要点**：
    - 引导AI考虑网络故障、无效输入等常见问题。
    - 有助于提高代码健壮性。

### 3. 请求解释
- **示例**：要求详细解释每个决策的理由。
    ```plaintext
    "Implement this, and explain why you made each decision."
    ```
- **要点**：
    - 帮助开发者学习和理解代码逻辑。
    - 检查潜在的不合理决策。

### 4. 请求替代方案
- **示例**：请求展示两种不同的实现方式及其优缺点。
    ```plaintext
    "Show me two different ways to implement this, with pros and cons of each."
    ```
- **要点**：
    - 当不确定最佳方法时使用。
    - 学习新模式或进行架构决策。

## 常见场景提示技巧
### 1. 避免使用 `any` 类型
- **示例**：明确指定类型接口。
    ```plaintext
    "Don't use any. Create proper TypeScript interfaces for this data structure based on the API response."
    ```
- **要点**：
    - 使用具体的数据结构定义，避免模糊性。

### 2. 避免过长的函数
- **示例**：将大函数拆分为小函数。
    ```plaintext
    "This function is doing too many things. Break it into smaller functions, each with a single responsibility."
    ```
- **要点**：
    - 提高代码可读性和维护性。

### 3. 避免空的 `catch` 块
- **示例**：正确处理错误。
    ```plaintext
    "Handle this error properly. Log it, show user feedback, or re-throw. Don't silently swallow errors."
    ```
- **要点**：
    - 确保错误得到妥善处理，避免隐藏错误。

### 4. 避免硬编码值
- **示例**：使用环境变量配置。
    ```plaintext
    "Use environment variables for configuration. This needs to work in dev, staging, and production."
    ```
- **要点**：
    - 提高代码的灵活性和可维护性。

### 5. 避免忽略边缘情况
- **示例**：处理各种状态。
    ```plaintext
    "Add handling for: loading state, error state, empty state, and unauthorized state."
    ```
- **要点**：
    - 确保代码能够处理所有可能的情况。

## 审查清单
### 1. 检查类型定义
- **示例**：确保没有使用 `any` 类型。
    ```plaintext
    "Are there any any types that should be specific?"
    ```

### 2. 函数长度检查
- **示例**：限制函数行数。
    ```plaintext
    "Is any function longer than 50 lines?"
    ```

### 3. 错误处理检查
- **示例**：确保所有错误都被妥善处理。
    ```plaintext
    "Is every error handled appropriately?"
    ```

### 4. 配置检查
- **示例**：使用环境变量配置URL和密钥。
    ```plaintext
    "Are URLs and secrets in environment variables?"
    ```

### 5. 测试覆盖率检查
- **示例**：确保代码经过充分测试。
    ```plaintext
    "Is this code tested? Should it be?"
    ```

### 6. 安全性检查
- **示例**：检查是否存在安全漏洞。
    ```plaintext
    "Could this be exploited (XSS, SQL injection, etc.)?"
    ```

### 7. 边缘情况处理
- **示例**：确保代码能够处理各种异常情况。
    ```plaintext
    "What happens when things go wrong?"
    ```

## 迭代模式
### 1. 改进循环（Refinement Loop）
- **步骤**：
    1. 获取初始实现。
        - 提示：`"What could be improved?"`
    2. 应用改进。
    3. 重复直到满意。

### 2. 挑战模式
- **示例**：针对不确定的部分提出问题。
    ```plaintext
    "I'm not sure about [specific part]. What are the downsides of this approach? Is there a better way?"
    ```

### 3. 上下文添加
- **示例**：提醒AI考虑现有系统和约束条件。
    ```plaintext
    "This needs to work with our existing auth system that uses JWT tokens stored in httpOnly cookies. Update the implementation."
    ```

### 4. 约束添加
- **示例**：简化或增强代码实现。
    - 简化：
        ```plaintext
        "This is simpler than I need. Give me the minimal implementation that just does X."
        ```
    - 增强：
        ```plaintext
        "This needs to be production-ready. Add proper error handling, logging, and type safety."
        ```

## 反模式避免
### 1. 不要直接接受第一输出
- **示例**：迭代优化。
    ```plaintext
    "AI's first response is rarely its best. Iterate."
    ```

### 2. 不要忽略理解
- **示例**：请求解释代码逻辑。
    ```plaintext
    "If you don't understand the code, ask AI to explain it. Don't ship code you can't maintain."
    ```

### 3. 不要忽视警告
- **示例**：修复代码问题。
    ```plaintext
    "If your linter, type checker, or tests complain, fix the issues. Don't tell AI to 'make the errors go away' (it will use hacks like any or // @ts-ignore)."
    ```

### 4. 不要忘记上下文
- **示例**：提醒AI注意现有代码库。
    ```plaintext
    "AI doesn't remember your whole codebase. Remind it of: Existing patterns to follow, Libraries you're using, Constraints and requirements."
    ```

## 提示模板
### 1. 新功能实现
- **示例**：
    ```plaintext
    Implement [feature] that:
    - [Requirement 1]
    - [Requirement 2]
    - [Requirement 3]

    Follow the patterns in [existing file]. Use [specific libraries].

    Handle these edge cases:
    - [Edge case 1]
    - [Edge case 2]

    Write tests first.
    ```

### 2. 错误修复
- **示例**：
    ```plaintext
    There's a bug where [describe the bug].

    Expected behavior: [what should happen]
    Actual behavior: [what happens instead]

    Here's the relevant code: [paste code]

    Find the root cause and fix it. Explain why this bug occurred.
    ```

### 3. 重构
- **示例**：
    ```plaintext
    Refactor this code to:
    - [Goal 1, e.g., "be more testable"]
    - [Goal 2, e.g., "follow single responsibility principle"]
    - [Goal 3, e.g., "use proper TypeScript types"]

    Keep the same functionality. Show me the before/after.
    ```

### 4. 代码审查
- **示例**：
    ```plaintext
    Review this code for:
    - Security vulnerabilities
    - Performance issues
    - Error handling gaps
    - Code quality issues
    - Missing edge cases

    Be critical. I want to ship production-quality code.
    ```

### 5. 元提示（Meta-Prompt）
- **示例**：当不确定如何提问时。
    ```plaintext
    "I want to [goal]. I'm not sure the best way to approach this. What are the downsides of this approach? Is there a better way?"
    ```

## 总结
通过遵循这些提示技巧和模板，可以显著提高代码质量和开发效率。确保每次迭代都进行充分的审查，并不断优化实现细节。利用AI助手的同时，保持对代码逻辑和业务需求的理解至关重要。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
