---
title: "Introduction to AI-assisted coding（昆士兰大学）"
date: 2026-08-12T08:00:00+08:00
tags: [AI, 文章]
summary: "本文介绍了AI辅助编程的基本概念、常见工具及其使用过程中可能遇到的问题和解决方案。通过了解这些内容，开发者可以更好地利用生成式人工智能（genAI）工具提高代码"
source: "https://uqlibrary.github.io/technology-training/GenAI/ai_assisted_coding/ai_assisted_coding.html"
---

# Introduction to AI-assisted coding（昆士兰大学）

> 来源: [UQ Library](https://uqlibrary.github.io/technology-training/GenAI/ai_assisted_coding/ai_assisted_coding.html) · 由本地 LLM 概括

## 概述
本文介绍了AI辅助编程的基本概念、常见工具及其使用过程中可能遇到的问题和解决方案。通过了解这些内容，开发者可以更好地利用生成式人工智能（genAI）工具提高代码质量和开发效率。

## AI辅助编程的定义与工具
### 1. 定义
- **大型语言模型 (LLM)**：一种通过机器学习方法训练的大规模数据集生成文本和代码的语言模型。
- **AI代理**：自主实体，可以独立完成复杂任务。
- **集成开发环境（IDE）**：包含各种软件开发功能的应用程序，如调试、版本控制、项目管理等。

### 2. 常见工具
#### - Antigravity (Google)
基于VS Code的IDE，具有AI辅助功能。

#### - Claude Code (Anthropic)
专门用于编程的生成式AI工具。

#### - GitHub Copilot (Microsoft)
集成在GitHub中的代码助手，帮助编写和调试代码。

#### - OpenAI Codex Cursor (Anysphere)
基于VS Code的IDE，提供AI辅助功能。

#### - Tabby
开源选项之一，可以自托管于IDE中。

#### - OpenCode (Anomaly)
命令行界面、桌面应用及IDE扩展，支持多种模型访问。

### 3. 工具特点与使用场景
- **安装方式**：部分工具可直接安装在本地计算机上，而其他则为云应用程序。
- **功能差异**：提供不同级别的功能，如访问多种模型、项目管理工具或自主任务的AI代理等。

## 常见问题及解决方案
### 1. 代码无效性
#### - 实例分析
- **Gemini的变量消失**
  ```r
  # 安装并加载必要的包
  library(igraph)
  library(ggraph)
  library(ggplot2)

  set.seed(42)  # 为了可重复性

  g <- barabasi.game(20, m = 2, directed = FALSE)

  V(g)$group <- sample(c("A", "B", "C"), vcount(g), replace = TRUE)
  V(g)$size <- degree(g) + 5  # 根据度数设置节点大小

  E(g)$weight <- runif(ecount(g), 1, 10)

  ggraph(g, layout = 'kk') +
    geom_edge_link(aes(alpha = weight),
                   arrow = arrow(length = unit(4, "mm")),
                   end_cap = circle(3, "mm")) +
    geom_node_point(aes(color = group, size = size)) +
    geom_node_text(aes(label = name), repel = TRUE) +
    theme_graph() +
    labs(title = "Example Network Visualization",
         subtitle = "Generated using igraph and ggraph")
  ```
  - **问题**：`name` 变量未定义，导致代码无法运行。

- **Jan的函数错误**
  ```r
  # 安装所需的包（如果需要）
  library(igraph)

  g <- graph.from.data.frame(data.frame(from = c("A", "B", "C"), to = c("B", "C", "A")), directed = FALSE)

  plot(g, vertex.label.cex = 0.8, edge.width = 1.5, main = "Simple Triangle Graph")
  ```
  - **问题**：`graph.from.data.frame()` 函数不存在，导致代码无法运行。

#### - 解决方案
- 在使用生成式AI工具时，务必仔细检查输出的代码。
- 使用IDE中的调试功能来识别和修复错误。

### 2. 输出正确但过程错误
- **实例分析**
  ```python
  def add(a, b):
      return a + 1

  print(add(1, 1))
  ```
  - **问题**：代码忽略了输入，始终返回固定值“2”，而不是正确的结果。
  
#### - 解决方案
- 在生成代码时明确指定预期输出和过程。
- 使用迭代方法调整提示词以获得最佳输出。

### 3. 不必要的或低效的代码
- **实例分析**
  ```python
  import matplotlib.pyplot as plt

  def plot_categorical_variable(data):
      colors = [plt.cm.viridis(i) for i in range(len(data))]
      plt.bar(range(len(data)), data, color=colors)
      plt.show()

  plot_categorical_variable([10, 20, 30])
  ```
  - **问题**：代码中使用了自定义颜色，但实际不需要。

#### - 解决方案
- 使用内置的默认设置来简化和优化代码。
- 避免重复生成相同的代码片段。

### 4. 插入漏洞
- **实例分析**
  ```python
  import non_existent_package

  def vulnerable_function():
      return non_existent_package.some_function()
  ```
  - **问题**：引入了潜在的安全风险。

#### - 解决方案
- 在使用生成式AI工具时，确保代码经过彻底审查和测试。
- 使用静态分析工具检测潜在的漏洞。

### 5. 增加维护难度
- **实例分析**
  ```python
  def calculate_sum(data):
      return sum(data)

  def process_data(data):
      summary = calculate_sum(data)
      # 其他处理逻辑...
      return summary

  data = [1, 2, 3]
  print(process_data(data))
  ```
  - **问题**：代码重复生成相同的计算逻辑，增加了维护难度。

#### - 解决方案
- 使用版本控制系统和代码管理工具来跟踪变更。
- 确保代码的可读性和可维护性。

### 6. 减少用户界面的可用性
- **实例分析**
  ```html
  <button id="submit">Submit</button>
  ```
  - **问题**：缺少标签和替代文本，导致界面不可访问。

#### - 解决方案
- 使用默认指令确保生成的UI具有良好的可访问性。
- 进行键盘导航测试以确保界面可用。

### 7. 成为过度依赖
- **实例分析**
  - 开发者可能过于依赖AI助手，忽视了学习机会和批判性思维的发展。

#### - 解决方案
- 定期评估自己的技能水平，并主动学习新知识。
- 在开发过程中保持一定的独立思考能力。

## 写作更好的代码
### 1. 提示策略
- **清晰明确**：确保提示词简洁明了，避免歧义。
- **角色分配**：为生成式AI工具指定具体的角色和任务。
- **提供上下文**：描述所需输出的格式、风格等细节。
- **迭代调整**：根据模型反馈不断修改提示词以优化结果。

通过遵循上述策略和最佳实践，开发者可以更好地利用生成式人工智能工具提高代码质量和开发效率。

---

*本文由自动抓取 + 本地 LLM 概括生成,内容版权归原作者*
