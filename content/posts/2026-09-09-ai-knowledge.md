---
title: "2026-09-09 AI 知识库日报"
date: 2026-09-09T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 5 条对话,提炼 5 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(5/5 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(3条)、Roo Code (本地)(2条)

## 今日知识要点

### 植物大全网站开发建议
- **核心结论**: 项目初期应先构建一个小型 MVP，确保数据模型和数据库设计正确后再逐步扩展。
- **关键要点**:
  - 使用 `Astro + React + TypeScript` 作为前端框架。
  - 采用 `Cloudflare Pages` 部署前端。
  - 利用 `Cloudflare Worker` 和 `Cloudflare D1` 提供 API 服务。
  - 数据库设计初期只建立基础表结构。
  - 用 20 种植物的假数据进行初步测试。
  - 先构建首页、植物列表、植物详情页面。
  - 写 D1 schema 并导入 mock 数据。
  - 最终部署到 Cloudflare。
- **信息来源:** Codex 桌面版 (本地)

### 代码示例
```javascript
// worker/index.js
export async function GET(request) {
  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const limit = parseInt(url.searchParams.get('limit'), 10) || 10;

  try {
    const db = D1Client.connect();
    const results = await db.query(
      `SELECT * FROM plants WHERE name ILIKE $1 LIMIT $2`,
      [query, limit]
    );
    return new Response(JSON.stringify(results.rows), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { 'Content-Type': 'application/json' },
      status: 500,
    });
  }
}
```

```javascript
// tests/worker.test.js
import { fetch } from 'node-fetch';

test('GET request with query and limit', async () => {
  const response = await fetch('https://example.com/worker', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    searchParams: { q: 'rose', limit: '5' },
  });

  expect(response.status).toBe(200);
  const data = await response.json();
  expect(data.length).toBe(5);
});

test('GET request with invalid limit', async () => {
  const response = await fetch('https://example.com/worker', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    searchParams: { q: 'rose', limit: 'invalid' },
  });

  expect(response.status).toBe(500);
  const data = await response.json();
  expect(data.error).toBe('Invalid limit');
});
```

- **信息来源:** Codex 桌面版 (本地)

### 数据库字段重命名与查询
- **核心结论**: 在D1数据库中，`taxa`表的`parent_taxon_id`字段需要重命名为`phylum_taxon_id`，并通过`higher_taxa`表根据`family_taxon_id`查询`phylum_taxon_id`。
- **关键要点**:
  - `taxa`表中的`parent_taxon_id`字段需要重命名为`phylum_taxon_id`。
  - `higher_taxa`表用于查询`phylum_taxon_id`，其中包含`taxid`和`parent_taxid`字段。
  - `higher_taxa`表的实际字段为`taxid`, `parent_taxid`, `rank`, `scientific_name`, `chinese_name`。
  - 通过`worker/index.js`中的代码片段可以连接到D1数据库。
  - 使用Cloudflare D1数据库的远程读取权限进行查询。
- **信息来源**: Roo Code (本地)

### SQL脚本示例
```sql
-- 重命名字段
ALTER TABLE taxa RENAME COLUMN parent_taxon_id TO phylum_taxon_id;

-- 查询phylum_taxon_id
SELECT t1.phylum_taxon_id
FROM taxa t1
JOIN higher_taxa t2 ON t1.taxon_id = t2.taxid
WHERE t1.family_taxon_id = [具体科id];
```

- **信息来源**: Roo Code (本地)

### 数据清洗与入库流程
- **核心结论**: 数据清洗和入库流程需按用户要求进行，确保数据准确性和完整性。
- **关键要点**:
  - 使用开源库 `wcvpy` 下载 WCVP 数据。
  - 数据清洗和入库工作在本地 SQLite 数据库中进行。
  - 优先清洗和入库维管植物数据，删除非植物、真菌或藻类的数据。
  - 验证物种对应的 NCBI TaxID、WCVP ID、WFO ID 和 GBIF ID 的准确性。
- **信息来源**: Codex 桌面版 (本地)

### 本地文件操作
- **核心结论**: 本地文件操作需谨慎，确保操作范围明确且无网络或凭据影响。
- **关键要点**:
  - 删除单个已盘点的工程根目录草稿文件。
  - 删除旧 SQL 数据镜像文件。
  - 删除旧枚举 SQL 文件。
  - 删除已明确标记为旧文件的单个 SQL 文件。
  - 删除空目录。
  - 读取并显示已迁移的 XLSX 文件元数据。
  - 删除已确认不再被构建使用的旧 schema.sql 文件。
- **信息来源**: Codex 桌面版 (本地)

### 数据补全流程
- 核心结论: 需要根据 SQLite 数据库和 Excel 文件补全中文名。
- 关键要点:
  - 检查 SQLite 数据库 `wcvp_backbone.sqlite` 和 Excel 文件 `hasname.xlsx` 的结构。
  - 分析数据库和 Excel 文件之间的关系，确定哪些条目需要补全中文名。
  - 量化需要补全中文名的范围，包括同义词匹配。
  - 检查数据库中的中文名与主 CSV 文件之间的差异。
- **信息来源:** Roo Code (本地)

### 代码片段
```python
# 检查 SQLite 数据库结构
import sqlite3
conn = sqlite3.connect('H:/vs-workspace/plants-data/clean/wcvp_backbone.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
tables
```

```python
# 检查 Excel 文件结构
import pandas as pd
excel_file = pd.read_excel('H:/vs-workspace/plants-data/china/hasname.xlsx')
excel_file.head()
```

## 今日知识要点
(无实质内容)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(text)
```text
Astro + React + TypeScript
Cloudflare Pages
Cloudflare Worker
Cloudflare D1
Cloudflare R2
```
### 片段 2(text)
```text
首页
/plants 植物列表
/plants/rosa-chinensis 植物详情
/family/rosaceae 科页面
/genus/rosa 属页面
/search 搜索
/explore 条件筛选
```
### 片段 3(text)
```text
taxon
taxon_identifier
taxon_name
plant_profile
plant_trait
plant_image
plant_distribution
source
```
### 片段 4(text)
```text
plant-atlas/
├─ apps/
│  ├─ web/        # Astro 前端
│  └─ api/        # Cloudflare Worker API
├─ packages/
│  ├─ db/         # D1 schema / queries
│  ├─ types/      # 共享类型
│  └─ ui/         # UI 组件
├─ data/
│  ├─ seed/       # 20 条模拟植物
│  └─ importers/  # 以后接 WFO / GBIF
└─ migrations/
```
### 片段 5(text)
```text
npm test
python tests/importer_test.py
npm run build
```
### 片段 6(text)
```text
SELECT * FROM taxa
```
### 片段 7(text)
```text
GET /api/plants?limit=24&cursor=xxx
```
### 片段 8(json)
```json
{
  "items": [],
  "nextCursor": "xxx",
  "hasMore": true
}
```
### 片段 9(text)
```text
offset=100000
```
### 片段 10(sql)
```sql
WHERE scientific_name > ?
ORDER BY scientific_name
LIMIT 24
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
