---
title: "2026-08-10 AI 知识库日报"
date: 2026-08-10T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 300 条对话,提炼 13 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(13/300 条有效)。
> 信息来源分布:VSCode Roo(1条)、DeepSeek 网页(4条)、DeepSeek API(8条)

## 今日知识要点

### API模型名称配置错误排查与解决

#### 核心结论
确保使用DeepSeek API时，正确设置模型名称。常见错误包括使用不支持的模型名或下拉菜单中未列出的标准模型。

#### 关键要点
- **检查模型名称**：确认使用的模型名称是 `deepseek-chat` 或 `deepseek-reasoner`。
- **手动配置**：在ProxyAI等工具中，通过“Custom OpenAI”方式手动输入正确的模型名称。
- **常见错误示例**
  ```json
  {"error":{"message":"The supported API model names are deepseek-v4-pro or deepseek-v4-flash, but you passed gpt-4.1.","type":"invalid_request_error","param":null,"code":"invalid_request_error"}}
  ```
- **正确配置步骤**：
  1. 进入 `Settings` -> `Tools` -> `ProxyAI` -> `Providers` -> `Custom OpenAI`。
  2. 填写以下信息：
     - **URL**: `https://api.deepseek.com/v1/chat/completions`
     - **API Key**: 您的DeepSeek API密钥
     - **Model (在Body中)**: 手动输入 `deepseek-chat` 或 `deepseek-reasoner`
  3. 保存设置并重试连接。

#### 来源:
- ProxyAI / IDEA ProxyAI [来源: DeepSeek 网页]

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
