---
title: "GitHub Copilot Bootcamp：提示工程与定制"
date: 2026-01-22T08:00:00+08:00
tags: [AI, 文章]
summary: "本文档详细介绍了GitHubCopilot的提示工程与定制，包括如何通过有效的提示引导Copilot生成高质量代码、设置组织标准以及创建可重用的提示模板。内容涵"
source: "https://github.com/Pwd9000-ML/GitHub-Copilot-Bootcamp/blob/master/Workshops/Week2/1-Prompt-Engineering-and-Customisation.md"
---

# GitHub Copilot Bootcamp：提示工程与定制

> 来源: [GitHub](https://github.com/Pwd9000-ML/GitHub-Copilot-Bootcamp/blob/master/Workshops/Week2/1-Prompt-Engineering-and-Customisation.md) · 由本地 LLM 概括

## 概述
本文档详细介绍了 GitHub Copilot 的提示工程与定制，包括如何通过有效的提示引导 Copilot 生成高质量代码、设置组织标准以及创建可重用的提示模板。内容涵盖了从基本概念到具体操作的各个方面。

## 概述
GitHub Copilot 提供了一种强大的工具来辅助软件开发过程中的代码生成和优化。本文档旨在帮助开发者掌握如何通过有效的提示工程（Prompt Engineering）来引导 Copilot 生成高质量代码，并介绍 Copilot 的定制方法，包括设置组织标准、创建可重用的提示模板等。

## Prompt 工程与定制
### Duration 和格式
- **Duration**: 45-60 分钟
- **Format**: 演示文稿结合互动实例

### 目标
- 掌握如何通过有效的提示工程引导 Copilot 生成高质量代码。
- 学习 Copilot 的三种定制方法：指令文件、提示文件和自定义代理。

## Prompt 工程介绍
### 什么是提示工程？
- 提示工程是编写清晰具体指令的过程，以指导像 GitHub Copilot 这样的 AI 工具生成所需的输出。这类似于学习如何与 AI 合作伙伴有效沟通。
- **重要性**：更好的提示 = 更好的代码建议；减少迭代时间和返工；确保团队标准的一致性；提高复杂任务的准确性。

### CRAFT 框架
- 使用 CRAFT 提示框架来结构化你的提示，以获得最佳结果：
  - **C (Context)**: 项目或任务背景信息。
    ```markdown
    "In a Node.js Express application..."
    ```
  - **R (Role)**: Copilot 应该采取的视角。
    ```markdown
    "As a senior developer..."
    ```
  - **A (Action)**: 需要执行的具体任务。
    ```markdown
    "...create a function that..."
    ```
  - **F (Format)**: 输出应如何结构化。
    ```markdown
    "...with JSDoc comments and error handling"
    ```
  - **T (Tone)**: 遵循的任何风格或标准。
    ```markdown
    "...following our team's naming conventions"
    ```

### 强大的代理提示（Agentic Prompting）
- 现代提示工程还包括选择正确的 Copilot 表面，而不仅仅是编写更好的注释。强大的代理提示描述了目标、背景信息、约束条件、批准边界、预期验证以及助手在编辑文件之前应执行的操作。
  - **示例**：
    ```markdown
    "Add CSV export for the orders table."
    ```
    ```markdown
    "Use #codebase and the selected API route."
    ```

## Prompt 类型与使用场景
### Comment-Driven Prompts（注释驱动的提示）
1. 基本示例：
   ```markdown
   // Function to validate email addresses
   function validateEmail(email) {
     // Copilot generates the implementation
   }
   ```
2. 增强示例（使用 CRAFT）：
   ```markdown
   /**
    * Performs basic validation of an email address format using common rules,
    * without claiming full RFC 5322 or RFC 5321 compliance.
    * Returns true if valid, false otherwise.
    * Should handle edge cases like empty strings and null values.
    *
    * @param {string} email - The email address to validate
    *
    * @returns {boolean} - Whether the email is valid
    */
   function validateEmail(email) {
     // Copilot generates a more robust implementation
   }
   ```

### Chat-Based Prompts（聊天驱动的提示）
1. 弱示例：
   ```markdown
   "Write a function"
   ```
2. 强示例：
   ```markdown
   "Write a JavaScript function to add a new book to an inventory array. The book should have properties for title, author, genre, and publication year. Prevent duplicate entries based on the title. Include input validation and return appropriate error messages."
   ```

### 模板生成提示（Template Generation Prompts）
1. 基本功能：
   ```markdown
   "Generate a JavaScript function template to add a new book with fields like title, author, and genre."
   ```
2. 升级功能：
   ```markdown
   "Can you create a reusable function to add books with properties such as title, author, genre, and publication year? Include validation to prevent duplicates."
   ```
3. 搜索功能：
   ```markdown
   "Write a function template to search for books in an inventory by title or genre. Make it case-insensitive and support partial matches."

## 写作有效提示的最佳实践
1. 具体和详细：
   - 弱示例：创建一个搜索函数。
     ```markdown
     "Create a function to search for books by title or genre, returning all matches as an array"
     ```
   - 强示例：处理错误。
     ```markdown
     "Add try-catch blocks with specific error messages for network failures and validation errors"
     ```

2. 提供背景信息：
   - 无背景信息的提示：写一个登录函数。
     ```markdown
     "Write a function to log in users."
     ```
   - 带有背景信息的提示：写一个登录函数。
     ```markdown
     "Write a function to log in users. Use JWT for authentication and store tokens securely."
     ```

3. 使用模板生成提示：
   - 创建可重用的提示模板，例如在 `.github/prompts/` 目录下创建 `code-review.prompt.md` 文件。

## 设置组织标准
### 指令文件（Copilot Instructions）
1. 在仓库根目录下创建 `.github/copilot-instructions.md` 文件：
   ```markdown
   #
   Copilot Instructions for This Repository
   ##
   Code Style
   -
   Use TypeScript for all new files
   -
   Follow ESLint rules defined in .eslintrc
   -
   Use functional components for React
   -
   Prefer async/await over .then() chains
   ##
   Naming Conventions
   -
   Use camelCase for variables and functions
   -
   Use PascalCase for classes and React components
   -
   Use SCREAMING_SNAKE_CASE for constants
   -
   Prefix private methods with underscore
   ##
   Documentation
   -
   All public functions must have JSDoc comments
   -
   Include @param, @returns, and @throws tags
   -
   Add usage examples for complex functions
   ##
   Error Handling
   -
   Always use try-catch for async operations
   -
   Log errors with context using our logger utility
   -
   Return standardised error objects: { success: false, error: string, code: number }
   ##
   Security
   -
   Never hardcode credentials or API keys
   -
   Sanitise all user inputs
   -
   Use parameterised queries for database operations
   ```

### 文件特定指令（File-Specific Instructions）
1. 为特定文件类型或目录创建指令：
   - 在 `.github/instructions/` 目录下创建 `tests.instructions.md` 文件。
     ```markdown
     ---
     applyTo: "**/*.test.js,**/*.spec.ts"
     description: "Guidelines for writing unit tests"
     ---
     #
     Test File Instructions
     -
     Use Jest as the testing framework
     -
     Follow AAA pattern: Arrange, Act, Assert
     -
     Use descriptive test names: "should [expected behavior] when [condition]"
     -
     Mock external dependencies
     -
     Aim for 80% code coverage minimum
     ```

## Prompt 文件（可重用提示）
1. 在 `.github/prompts/` 目录下创建可重用的提示模板，例如 `code-review.prompt.md`：
   ```markdown
   ---
   agent:
     'agent'
   name: 'code-review'
   description: 'Language-agnostic code review with repository analysis and fix-oriented feedback'
   argument-hint: 'focus=<security|performance|readability>'
   model: '<model-id>'
   tools: ['codebase', 'githubRepo', 'search', 'usages', 'myMcpServer/*']
   ---
   #
   Code Review
   Perform a comprehensive code review of the selected code:
   ##
   Review Checklist
   -
   [ ] Logic correctness and edge case handling
   -
   [ ] Error handling and defensive programming
   -
   [ ] Code readability and naming conventions
   -
   [ ] Performance considerations
   -
   [ ] Adherence to SOLID principles
   ##
   Output Format
   Provide feedback as:
   1. **Critical issues**
      - Must fix before merge
   2. **Suggestions**
      - Recommended improvements
   ```

通过以上步骤，开发者可以有效地利用 GitHub Copilot 提供的强大功能来提高代码质量和开发效率。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
