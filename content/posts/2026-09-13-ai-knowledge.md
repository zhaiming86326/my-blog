---
title: "2026-09-13 AI 知识库日报"
date: 2026-09-13T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 6 条对话,提炼 5 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(5/6 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(5条)

## 今日知识要点

### 代码部署与 GitHub 整理
- **核心结论**: 将网页相关代码和 SQL 分离并部署到 GitHub，每次更新 GitHub 将自动推送至 Cloudflare。
- **关键要点**:
  - 将明确相关的代码、SQL、前端和工作流文件加入 Git 暂存区。
  - 提交已核对的文件到本地 Git 历史，并推送到 GitHub origin/main 分支。
  - 使用短期凭证克隆现有 Sites 项目到临时目录，为重新发布前端做准备。
  - 在临时 Sites 源仓库创建已暂存内容的本地提交，并推送到 main 分支以触发重新部署。
- **信息来源**: Codex 桌面版 (本地)

### 爬取与数据处理
- **核心结论**: 从 Wikimedia 爬取植物详情并存入新库，考虑使用 CSV 文件存储数据以避免查询限制。
- **关键要点**:
  - 爬取任务启动后，数据写入新库不受额度限制。
  - 可以将需要爬取的数据写入 CSV 文件，减少网络请求次数。
  - Wikipedia 和 Wikimedia 之间的区别在于数据来源和限制，Wikipedia 限制每 6 小时 1 条数据。
- **信息来源**: Codex 桌面版 (本地)

### API 使用与调试
- **核心结论**: API 调用和部署过程中遇到的错误可以通过重新部署和调试解决。
- **关键要点**:
  - 使用 GitHub 仓库 Secrets 配置好后，重新部署前端并验证 API 调用。
  - 通过 GitHub Actions 监控部署状态，确保数据正确写入目标库。
- **信息来源**: Codex 桌面版 (本地)

### 脚本编写与数据提取
- **核心结论**: 编写了一个脚本用于从维基百科提取植物数据，并输出到CSV文件。
- **关键要点**:
  - 脚本文件名: `extract_zhwiki_plant_data.py`
  - 脚本功能: 从 `zhwiki-latest-pages-articles-multistream.xml` 文件中提取植物数据，包括名称、简介、形态、用途、栽培、繁殖、变种、每100 g 食物营养值、保护状况。
  - 输出文件: `zhwiki-plant-data.csv`
  - 校验机制: 匹配维基页面中的学名、属、科与CSV中的信息，确保数据一致性。
  - 运行命令:
    ```powershell
    python scripts\extract_zhwiki_plant_data.py
    ```
- **信息来源**: Codex 桌面版 (本地)

### 数据源测试与样例生成
- **核心结论**: 测试了多个植物数据源，并生成了样例文件。
- **关键要点**:
  - 测试数据源: Wikipedia、PFAF、theferns
  - 样例文件命名: `zhwiki-plant-data.sample.csv`、`zhwiki-plant-data-review.sample.csv`
  - 样例生成命令:
    ```powershell
    python scripts\extract_zhwiki_plant_data.py --limit 1 --progress-every 1000 --output zhwiki-plant-data.sample.csv --review-output zhwiki-plant-data-review.sample.csv
    ```
- **信息来源**: Codex 桌面版 (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(powershell)
```powershell
+npx wrangler d1 execute flora-atlas --remote --file ".\db\import\refresh-summary-cache.sql"
+
```
### 片段 2(kotlin)
```kotlin
zhwiki-plant-data.csv和zhwiki-plant-data.sample.csv有什么不同
```
### 片段 3(powershell)
```powershell
python scripts\extract_zhwiki_plant_data.py
```
### 片段 4(text)
```text
wiki-enrichment-targets.csv
zhwiki-latest-pages-articles-multistream.xml
```
### 片段 5(text)
```text
zhwiki-plant-data.csv
```
### 片段 6(powershell)
```powershell
python scripts\extract_zhwiki_plant_data.py --self-test
python scripts\extract_zhwiki_plant_data.py --limit 1 --output zhwiki-plant-data.sample.csv
```
### 片段 7(text)
```text
Malus domestica / Malus / taxonomy_match=scientific_name,genus
```
### 片段 8(text)
```text
zhwiki-plant-data-review.csv
```
### 片段 9(powershell)
```powershell
python scripts\extract_zhwiki_plant_data.py --output zhwiki-plant-data.csv --review-output zhwiki-plant-data-review.csv
```
### 片段 10(text)
```text
zhwiki-plant-data.csv
zhwiki-plant-data-review.csv
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
