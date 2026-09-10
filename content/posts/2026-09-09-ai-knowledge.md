---
title: "2026-09-09 AI 知识库日报"
date: 2026-09-09T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 2 条对话,提炼 2 条"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(2/2 条有效)。
> 信息来源分布:Roo Code (本地)(2条)

## 今日知识要点

### 数据库字段重命名与查询
- **核心结论**: 在D1数据库中，将`taxa`表中的`parent_taxon_id`重命名为`phylum_taxon_id`，并根据`family_taxon_id`查询`phylum_taxon_id`。
- **关键要点**:
  - `taxa`表中的`parent_taxon_id`需要重命名为`phylum_taxon_id`。
  - 通过`higher_taxa`表查询`phylum_taxon_id`，其中`higher_taxa`表的实际字段为`taxid`和`parent_taxid`。
  - 使用Cloudflare D1数据库进行查询，实际字段为`taxid`和`parent_taxid`。
  - 重命名SQL脚本示例:
    ```sql
    ALTER TABLE taxa RENAME COLUMN parent_taxon_id TO phylum_taxon_id;
    ```
- **信息来源**: Roo Code (本地)

### SQL查询示例
- **查询示例**:
  ```sql
  -- 重命名字段
  ALTER TABLE taxa RENAME COLUMN parent_taxon_id TO phylum_taxon_id;

  -- 查询phylum_taxon_id
  SELECT t1.phylum_taxon_id
  FROM taxa t1
  JOIN higher_taxa t2 ON t1.taxon_id = t2.taxon_id
  WHERE t1.family_taxon_id = [具体科id];
  ```
- **信息来源**: Roo Code (本地)

### 数据补全与匹配
- **核心结论**: 需要根据 `wcvp_backbone.sqlite` 和 `hasname.xlsx` 补全中文名。
- **关键要点**:
  - 检查 SQLite 数据库和 Excel 文件的结构。
  - 分析数据库和现有 CSV 文件之间的关系，确定哪些条目需要补全中文名。
  - 量化需要补全中文名的范围，包括同义匹配。
  - 确认 `hasname.xlsx` 是否为最新或独立的数据源。
- **信息来源**: Roo Code (本地)

### 代码示例
```python
import pandas as pd
import sqlite3

# 连接 SQLite 数据库
conn = sqlite3.connect('H:/vs-workspace/plants-data/clean/wcvp_backbone.sqlite')

# 读取 Excel 文件
hasname_df = pd.read_excel('H:/vs-workspace/plants-data/china/hasname.xlsx')

# 查询数据库中缺少中文名的记录
query = "SELECT * FROM your_table_name WHERE chinese_name IS NULL"
missing_names_df = pd.read_sql_query(query, conn)

# 合并数据并补全中文名
merged_df = pd.merge(missing_names_df, hasname_df, on='common_name', how='left')

# 更新数据库
for index, row in merged_df.iterrows():
    conn.execute("UPDATE your_table_name SET chinese_name = ? WHERE id = ?", (row['chinese_name'], row['id']))
    conn.commit()

# 关闭数据库连接
conn.close()
```

- **信息来源**: Roo Code (本地)


---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
