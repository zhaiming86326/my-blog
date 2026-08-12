---
title: "2026-08-11 AI 知识库日报"
date: 2026-08-12T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 21 条对话,提炼 21 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(21/21 条有效)。
> 信息来源分布:DeepSeek API(20条)、DeepSeek 网页(1条)

## 今日知识要点

### 如何理解一个陌生工程的代码
核心结论:可以通过符号检索、文件结构分析和上下文引用关系来逐步理解陌生工程的代码。
关键要点:
- 使用 `find_symbol` 工具按名称查找函数或类的位置。
- 利用 `include_body=True` 参数获取函数体内容,以便进一步了解其逻辑。
- 通过 `find_referencing_symbols` 查找哪些其他符号引用了目标符号,以理解上下文关系。

### Serena 的入口结构与调用链
核心结论:Serena 的启动和工具注册过程涉及多个文件和模块的协作。
关键要点:
- 启动入口在 `pyproject.toml` 中定义。
- 通过 `cli.py` 调用 `mcp.py` 和 `agent.py` 来初始化 MCP 服务器。

### Serena 工具层详解
核心结论:Serena 提供了多种工具来支持代码检索和编辑操作,这些工具基于语言服务器的符号树进行高效查询。
关键要点:
- 每个工具继承自 `Tool` 基类并实现特定逻辑。
- 编辑类工具使用 `EditingToolWithDiagnostics` 以自动诊断文件更改。

### 语言服务器如何快速定位代码
核心结论:Serena 使用缓存机制和符号树匹配来加速代码位置的查找过程。
关键要点:
- 符号检索通过 LSP 请求获取文件内的符号树,并利用双层磁盘缓存减少重复请求。
- 名称路径模式匹配在内存中进行以提高效率。

### 工具只检索、LLM 才理解语义
核心结论:Serena 的工具负责提供代码的结构化信息,而 LLM 则基于这些信息推断出完整的语义和意图。
关键要点:
- `find_symbol` 和 `include_body=True` 用于获取函数体内容以供 LLM 分析。
- `find_referencing_symbols` 提供上下文引用关系作为额外证据。

### Serena 是否会收集代码注释
核心结论:Serena 不主动采集注释,但通过工具调用可以间接读取文档注释和行内注释。
关键要点:
- 通过 `include_info=True` 和 `include_body=True` 参数获取符号的 docstring 和源码内容。

### LLM 为什么优先使用 Serena 的工具
核心结论:Serena 使用多层提示词引导和工具描述来确保 LLM 优先选择其提供的工具进行操作。
关键要点:
- 系统提示词明确禁止使用内置工具处理代码文件。
- 工具描述中嵌入了何时优先使用的说明。

### 元数据的定义
核心结论:元数据是指关于工具自身的静态信息,而不是工具执行后产生的内容。
关键要点:
- 工具的名称、描述和参数格式属于元数据。
- 与之相对的是工具执行后的返回结果,即数据部分。

### Serena 插件报错诊断及修复方案
核心结论:版本不匹配导致 `project.yml` 文件中的字段名无法被识别。
关键要点:
- 报错原因是安装的 serena-agent 版本为 v1.6.1，而项目配置文件使用了新版格式。
- 解决方法包括升级到最新版或手动修改 `.serena/project.yml` 中的字段。

### V2rayN 上不了 Grok 和 ChatGPT 的排查步骤
核心结论:代理软件的分流规则可能出错,导致特定网站流量未被正确转发。
关键要点:
1. 切换路由模式至全局模式以快速判断问题所在。
2. 检查并自定义路由规则，为 Grok 和 ChatGPT 添加单独代理规则。
3. 尝试开启 TUN 模式解决复杂连接问题。

**信息来源:** DeepSeek API

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1
```
浏览器 → PAC(18081)
   ├─ 谷歌/github/youtube → 10809 (v2rayN)  → ✅ 正常
   └─ AI域名(chatgpt/openai/deepseek/grok/x.ai) → 8080 (mitmproxy抓包)
                                                 → ❌ 全挂
```
### 片段 2
```
浏览器 → 8080 mitmproxy ──直连──→ chatgpt.com
                   ↑
             mitmproxy 自己直接连目标
                   ↓
              被墙拦截, 失败 ❌
```
### 片段 3
```
浏览器 → 8080 mitmproxy → 10809 v2rayN → chatgpt.com
              ↑                    ↑
         在这里抓包          在这里翻墙/分流
```
### 片段 4(yaml)
```yaml
   - name: Serena
     command: serena
     args:
       - start-mcp-server
       - --context
       - ide
       - --project
       - H:/idea-workspace/embabel-agent
       - --open-web-dashboard
       - "False"
```
### 片段 5(json)
```json
{
  "mcpServers": {
    "serena": {
      "command": "serena",
      "args": [
        "start-mcp-server",
        "--context", "ide",
        "--project", "H:/idea-workspace/embabel-agent",
        "--open-web-dashboard", "False"
      ]
    }
  }
}
```
### 片段 6(toml)
```toml
[[plugins]]
name    = "serena"
command = "serena"
args    = ["start-mcp-server", "--context", "ide", "--project", "H:/idea-workspace/embabel-agent", "--open-web-dashboard", "False"]
```
### 片段 7
```
LLM 调用工具
  → FastMCP 收到请求 (mcp.py: SerenaFastMCPTool.execute_fn)
  → Tool.apply_ex() (tools_base.py:330)  ← 统一入口:校验、日志、异常兜底
  → 具体 Tool.apply()  ← 业务逻辑
  → 若是编辑类:EditingToolWithDiagnostics 自动跑 LSP 诊断
  → 结果返回给 LLM
```
### 片段 8(python)
```python
symbol_retriever = self.create_language_server_symbol_retriever()
symbols = symbol_retriever.find(name_path_pattern, ...)   # 在符号树里做模式匹配
```
### 片段 9(python)
```python
for lang_server in self._ls_manager.iter_language_servers():      # 遍历所有语言服务器
    symbol_roots = lang_server.request_full_symbol_tree(...)      # 拿整棵符号树
    for root in symbol_roots:
        symbols.extend(LanguageServerSymbol(root).find(name_path_pattern, ...))
```
### 片段 10(python)
```python
file_hash_and_result = self._document_symbols_cache.get(cache_key)   # key = 相对文件路径
if file_hash == file_data.content_hash:                              # 文件内容没变?
    return document_symbols                                          # 直接返回,不发 LSP 请求
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
