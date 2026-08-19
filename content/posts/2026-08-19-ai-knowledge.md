---
title: "2026-08-19 AI 知识库日报"
date: 2026-08-19T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 68 条对话,提炼 61 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(61/68 条有效)。
> 信息来源分布:DeepSeek API(60条)、DeepSeek Harness(1条)

## 今日知识要点

### 如何将 IDE 插件对话记录本地化并统一管理

#### 核心结论
- 通过直接读取插件本地历史文件，可以实现将 Continue、Roo Code 和 Reasonix 的对话记录本地化并统一管理。
- 无需依赖抓包系统，直接读取本地文件即可覆盖所有插件的对话记录。

#### 关键要点
- **Continue 插件**:
  - 存储位置: `~/.continue/sessions/*.json`
  - 格式: 每个会话一个 JSON,包含 `history[]` 数组，每个消息有 `role` 和 `content`。
  - 解析: 从 `history` 数组中提取 `role` 和 `content`，时间戳用文件的 `mtime`。

- **Roo Code 插件**:
  - 存储位置: `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\tasks\`
  - 格式: 每个任务一个 JSON 文件，包含 `role` 和 `content`，全局 `_index.json` 有精确时间戳。
  - 解析: 从 `_index.json` 中提取任务信息，从每个任务文件中提取 `role` 和 `content`。

- **Reasonix 插件**:
  - 存储位置: `%APPDATA%\reasonix\archive\context-*.jsonl`
  - 格式: 每条记录包含 `role` (user/assistant/tool)、`content` 和 `reasoning_content`。
  - 解析: 从 `context-*.jsonl` 文件中提取 `role` 和 `content`，时间戳用文件的 `mtime`。

- **导入脚本**:
  - `scripts/import_local.py`:
    - 读取 Continue、Roo Code 和 Reasonix 的本地历史文件。
    - 解析消息并提取 `role` 和 `content`。
    - 时间戳用文件的 `mtime`。
    - 去重: 使用会话内容哈希识别重复对话。
    - 写入 SQLite 数据库，标记来源为 `local-continue`、`local-roo` 或 `local-reasonix`。

- **总结与入库**:
  - 在 `summarize.py` 中调用 `import_local.import_all()`，确保每次总结前自动同步最新的本地对话。
  - 更新 `_detect_source` 和 `_make_markdown`，确保本地来源被正确识别和显示。

#### 信息来源
- 来源: DeepSeek API

### 本地导入与抓包采集的切换

- **本地导入**:
  - 通过读取插件本地历史文件，可以覆盖所有插件的对话记录，无需依赖抓包系统。
  - 优点: 100% 覆盖所有插件，不依赖代理/v2rayN/CA 证书。

- **抓包采集**:
  - 保留抓包采集，用于覆盖网页/API 流量。
  - 优点: 能捕获网页/API 流量，但 Continue 和 Reasonix 的 Node 流量需要通过代理。

- **切换方案**:
  - 完全切换到本地导入，保留抓包采集用于特定流量。
  - 优点: 简化系统，提高数据完整性。

#### 信息来源
- 来源: DeepSeek API

### 优化翻译速度
- **核心结论**: 通过更换模型和优化生成参数，显著提升了翻译速度。
- **关键要点**:
  - **硬件限制**: RTX 2060 显存为 6GB，无法容纳 `qwen2.5:14b-instruct` 模型，导致大部分计算在 CPU 上进行。
  - **优化方案**:
    - **更换模型**: 使用 `qwen2.5:7b-instruct` 模型，GPU 占比提升至 82%，速度提升约 6 倍。
    - **优化参数**:
      - `num_ctx=4096`: 缩小上下文窗口，节省显存空间，提升 GPU 占比。
      - `num_predict=300`: 控制输出长度，避免冗长输出拖慢速度。
      - `temperature=0`: 降低温度值，使生成结果更简洁确定。
- **信息来源**: DeepSeek API

### 代码示例
```kotlin
// 修改后的 Translator.kt
MODEL = "qwen2.5:7b-instruct"
num_ctx = 4096
num_predict = 300
temperature = 0
```

### 优化后的翻译速度对比
| 配置 | GPU 占比 | 速度 | 一段话（约 30 token）耗时 |
|---|---|---|---|
| 14B（原插件配置，32K 上下文） | 27% | 5.6 tok/s | 约 9 秒，长文本 20~40 秒 |
| 14B + `num_ctx=4096` | 43% | 7.1 tok/s | 快约 27%（需一次重载） |
| **7B + `num_ctx=4096`（新配置）** | **82%** | **33.5 tok/s** | **约 2 秒** |

### 优化后的插件更新
- **构建产物**: `build\distributions\idea-trans-1.0.0.zip`
- **安装步骤**: `Settings → Plugins → ⚙ → Install Plugin from Disk...` → 重启 IDE

### 如果你想用回 14B
- **修改配置**: 将 `Translator.kt` 中的 `MODEL` 改回 `qwen2.5:14b-instruct`，`num_ctx=4096` 参数同样有效，但 GPU 占比仍为 43%。

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(python)
```python
last = _last_summarized_day()
days = 从 last+1 到 昨天
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
