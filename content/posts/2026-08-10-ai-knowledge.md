---
title: "2026-08-10 AI 知识库日报"
date: 2026-08-10T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 291 条对话,提炼 13 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(13/291 条有效)。
> 信息来源分布:VSCode Roo(1条)、DeepSeek 网页(4条)、DeepSeek API(8条)

## 今日知识要点

### API模型名称配置错误排查与解决方法
- **核心结论**：确保使用正确的DeepSeek模型名称，避免因误用导致的API调用失败。
- **关键要点**
  - 检查并确认使用的模型名称是否为`deepseek-chat`或`deepseek-reasoner`等官方支持的名称。
  - 在配置中手动填写模型名称，而非依赖下拉菜单选择。
  - 使用正确的URL：`https://api.deepseek.com/v1/chat/completions`。
- **信息来源:** DeepSeek 网页

### 解决网络与代理设置问题
- **核心结论**：确保本地网络配置正确，并检查插件或IDE的代理设置是否影响API调用。
- **关键要点**
  - 检查并临时禁用IDE中的代理设置，重启IDE后重新测试连接。
  - 确认系统网络权限设置，特别是macOS上的隐私与安全性设置。
  - 使用命令行工具直接测试API连通性。
- **信息来源:** DeepSeek 网页

### 处理400错误
- **核心结论**：当遇到400错误时，可能是模型名称或请求参数不正确导致的。
- **关键要点**
  - 核实使用的模型名称是否为DeepSeek支持的版本（如`deepseek-chat`、`deepseek-reasoner`）。
  - 检查API请求参数是否符合标准格式。
- **信息来源:** DeepSeek 网页

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(bash)
```bash
    # 把 YOUR_API_KEY 换成你自己的
    curl -v "https://api.deepseek.com/v1/chat/completions" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -d '{
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}]
      }'
```
### 片段 2
```
https://api.deepseek.com/v1/chat/completions
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
