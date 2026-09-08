---
title: "2026-09-07 AI 知识库日报"
date: 2026-09-07T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 2 条对话,提炼 2 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(2/2 条有效)。
> 信息来源分布:Roo Code (本地)(2条)

## 今日知识要点

### 忽略目录设置
- **核心结论**: 设置 SQL 和 data 文件夹为提交代码的忽视目录。
- **关键要点**:
  - 在 `.gitignore` 文件中添加 `sql/` 和 `.openai/sql/` 目录。
  - 确认 `data/` 目录已被 git 忽略。
- **信息来源**: Roo Code (本地) [来源: VSCode Roo]

### 文件移动与引用更新
- **核心结论**: 成功将 `public/assets/` 下的四个文件移动到 `public/fonts/` 并更新引用路径。
- **关键要点**:
  - 移动文件: `FloraSans.otf`, `FloraSerif.otf`, `favicon.svg`, `OFL.txt`。
  - 更新引用路径:
    ```html
    public/index.html:8: href="assets/favicon.svg" → href="fonts/favicon.svg"
    public/style.css:1-2: url('assets/FloraSans.otf') → url('fonts/...')
    README.md:23: public/assets/OFL.txt → public/fonts/OFL.txt
    ```
- **信息来源**: Roo Code (本地) [来源: VSCode Roo]

### SQL 外键约束问题排查
- **核心结论**: 外键约束失败是因为 SQL 文件中的 `family_taxon_id` 和 `genus_taxon_id` 使用了 NCBI TaxID 和 WFO ID，而不是 `taxa` 表中的 UUID。
- **关键要点**:
  - SQL 文件中的 `family_taxon_id` 和 `genus_taxon_id` 实际上是 NCBI TaxID 和 WFO ID，而不是 `taxa` 表中的 UUID。
  - `taxa` 表的 `family_taxon_id` 和 `genus_taxon_id` 外键引用 `taxa` 表的 `taxon_id`。
  - 外键约束在 D1 中已启用，且 `taxa` 表中所有 `family_taxon_id` 和 `genus_taxon_id` 为 NULL。
  - 临时关闭外键约束在 D1 上被忽略。
- **信息来源**: Roo Code (本地)

### 修复方案
- **步骤**:
  1. 确认 `taxa` 表的结构和外键定义。
  2. 检查 SQL 文件中的 `family_taxon_id` 和 `genus_taxon_id` 是否正确引用 `taxa` 表中的 `taxon_id`。
  3. 如果需要移除外键约束，需在 D1 中创建任务清单并评估重建影响。
  4. 临时关闭外键约束在 D1 上不可行，需整表重建。
- **代码片段**:
  ```sql
  -- 临时关闭外键约束
  PRAGMA foreign_keys = OFF;

  -- 重新启用外键约束
  PRAGMA foreign_keys = ON;
  ```

- **信息来源**: Roo Code (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1
```
SELECT name, sql FROM sqlite_master WHERE type='table' AND sql LIKE '%REFERENCES%' ...
```
### 片段 2(sql)
```sql
CREATE TABLE taxa (
  taxon_id TEXT PRIMARY KEY,
  ...
  parent_taxon_id TEXT,       -- 原 REFERENCES taxa 已去掉
  accepted_taxon_id TEXT,     -- 原 REFERENCES taxa 已去掉
  family_taxon_id TEXT,       -- 原 REFERENCES taxa 已去掉
  genus_taxon_id TEXT,        -- 原 REFERENCES taxa 已去掉
  ...
  CHECK (parent_taxon_id IS NULL OR parent_taxon_id <> taxon_id)
)
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
