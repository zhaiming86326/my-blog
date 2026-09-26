---
title: "2026-09-05 AI 知识库日报"
date: 2026-09-05T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 8 条对话,提炼 8 条,含代码片段"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(8/8 条有效)。
> 信息来源分布:Codex VSCode 扩展 (本地)(3条)、Codex 桌面版 (本地)(3条)、Roo Code (本地)(2条)

## 今日知识要点

### 数据库操作与安装
- **核心结论**: 安装 `ete3` 包并构建 NCBI taxonomy 本地数据库。
- **关键要点**:
  - 在当前目录创建虚拟环境并安装 `ete3`、`six` 和 `numpy`。
  - 使用 `NCBITaxa` 模块从 NCBI 下载 taxonomy 数据并构建本地数据库。
  - 生成的 `ncbi_taxa.sqlite` 文件可用于物种名称到 TaxID 的匹配。
- **信息来源**: Codex VSCode 扩展 (本地) [来源: Codex VSCode 扩展 (本地)]

### 插件管理
- **核心结论**: 安装 `ponytail` 插件。
- **关键要点**:
  - 检查本地插件目录和配置文件，确认 `ponytail` 插件已配置。
  - 使用 `codex plugin add ponytail` 命令安装插件。
  - 重启 Codex 客户端以加载新插件。
- **信息来源**: Codex 桌面版 (本地) [来源: Codex 桌面版 (本地)]

### 数据库表结构设计
- **核心结论**: 在 `taxa` 表中添加新字段，并创建新表用于存放形态、生活型和用途枚举。
- **关键要点**:
  - 在 `taxa` 表中添加 `wikidata_id`、`taxid`、`tagline`、`description`、`identification_features` 和 `image_url` 字段。
  - 创建 `morphology_enums`、`life_form_enums` 和 `use_enums` 表，用于存放形态、生活型和用途枚举。
  - 适配 Cloudflare D1 数据库方言，确保 SQL 语句符合 D1 要求。
- **信息来源**: Codex VSCode 扩展 (本地) [来源: Codex VSCode 扩展 (本地)]

### 文件操作与数据库迁移
- **核心结论**: 将 CSV 文件转换为 SQL 文件，并导入到 Cloudflare D1 数据库。
- **关键要点**:
  - 将 `植物界-2026-48356.csv` 转换为 SQL 文件 `schema.d1.taxa.sql`。
  - 使用 `wrangler d1 execute` 命令将 SQL 文件执行到远端 D1 数据库。
- **信息来源**: Codex VSCode 扩展 (本地) [来源: Codex VSCode 扩展 (本地)]

### 文件路径与数据库查询
- **核心结论**: 确认 `new_taxdump` 目录下的文件包含物种 TaxID。
- **关键要点**:
  - `new_taxdump` 目录下的 `nodes.dmp` 和 `names.dmp` 文件包含物种 TaxID。
- **信息来源**: Roo Code (本地) [来源: Roo Code (本地)]

### 数据处理与脚本编写
- **核心结论**: 根据 NCBI 数据库处理 CSV 文件中的 Taxonomy ID 缺失问题，可以分为几种情况分别处理。
- **关键要点**:
  - 缺失 Taxonomy ID 的物种分为三类:
    - **原变种/原亚种**: 可以继承正种的 Taxonomy ID。
    - **种下等级但种级在 NCBI 收录**: 可以继承种级的 Taxonomy ID，但需标记为父级锚点。
    - **NCBI 中完全不存在**: 无法直接获取 Taxonomy ID，需通过其他数据库补充。
- **信息来源**: Roo Code (本地)

### Python 脚本示例
- **脚本**: `extract_nodes_first3.py`
  ```python
  # 读取 nodes.dmp 文件，提取前三列数据
  with open('H:/vs-workspace/ncbi-data/new_taxdump/nodes.dmp', 'r') as nodes_file, open('H:/vs-workspace/ncbi-data/new_taxdump/nodes_first3cols.dmp', 'w') as output_file:
      for line in nodes_file:
          cols = line.strip().split('\t')
          output_file.write('\t'.join(cols[:3]) + '\n')
  ```
- **脚本**: `extract_names_scientific_first2.py`
  ```python
  # 读取 names.dmp 文件，提取第四列为 scientific name 的行，输出前两列
  with open('H:/vs-workspace/ncbi-data/new_taxdump/names.dmp', 'r') as names_file, open('H:/vs-workspace/ncbi-data/new_taxdump/names_scientific_first2cols.dmp', 'w') as output_file:
      for line in names_file:
          cols = line.strip().split('\t')
          if cols[3] == 'scientific name':
              output_file.write('\t'.join(cols[:2]) + '\n')
  ```
- **脚本**: `split_nodes_by_species.py`
  ```python
  # 读取 nodes_first3cols.dmp 文件，按第三列是否为 species 分流
  with open('H:/vs-workspace/ncbi-data/new_taxdump/nodes_first3cols.dmp', 'r') as nodes_file, open('H:/vs-workspace/ncbi-data/new_taxdump/nodes_species.dmp', 'w') as species_file, open('H:/vs-workspace/ncbi-data/new_taxdump/nodes_not_species.dmp', 'w') as not_species_file:
      for line in nodes_file:
          cols = line.strip().split('\t')
          if cols[2] == 'species':
              species_file.write(line)
          else:
              not_species_file.write(line)
  ```

### 处理缺失 Taxonomy ID 的建议
- **核心结论**: 缺失 Taxonomy ID 的物种需根据具体情况分别处理。
- **关键要点**:
  - **原变种/原亚种**: 可以继承正种的 Taxonomy ID。
  - **种下等级但种级在 NCBI 收录**: 可以继承种级的 Taxonomy ID，但需标记为父级锚点。
  - **NCBI 中完全不存在**: 无法直接获取 Taxonomy ID，需通过其他数据库补充。
- **信息来源**: Roo Code (本地)

## 排查涉及的代码片段
> 从当日对话中提取,供快速参考。
### 片段 1(python)
```python
{2: 'Bacteria', 3702: 'Arabidopsis thaliana', 9606: 'Homo sapiens'}
{2: 'domain', 3702: 'species', 9606: 'species'}
```
### 片段 2(powershell)
```powershell
.\.venv\Scripts\python.exe
```
### 片段 3(python)
```python
from ete3 import NCBITaxa

ncbi = NCBITaxa(dbfile="ncbi_taxa.sqlite")
```
### 片段 4(text)
```text
总行数: 48356
匹配到 TaxID: 36933
未匹配到: 11423
当前列数: 16
新增列名: TaxID
```
### 片段 5(text)
```text
× Agropogon lutosus => 416053
× Bolboschoenoplectus mariqueter => 3122982
Abelia chinensis => 180068
Abelia forrestii => 1630336
```
### 片段 6(sql)
```sql
(
  'metasequoia-glyptostroboides',  -- slug/前端ID，schema.sql 里没有直接字段
  '水杉',                          -- 中文名 -> vernacular_names.name
  'Metasequoia glyptostroboides',  -- 学名 -> taxa.scientific_name / source_records.scientific_name / search_names
  'Hu & W.C.Cheng',                -- 命名作者 -> taxa.authorship / source_records.authorship
  'Q156800',                       -- Wikidata ID，schema.sql 里没有直接字段
  'gymnosperms',                   -- 分组 -> taxa.group_code
  'Cupressaceae',                  -- 科学科名 -> 可作为 family_taxon_id 指向的 taxa 记录，或 source_records.family_name
  '柏科',                          -- 中文科名 -> vernacular_names，归属到“柏科”这个 taxon
  'Metasequoia',                   -- 属名 -> 可作为 genus_taxon_id 指向的 taxa 记录，或 source_records.genus_name
  '水杉属',                        -- 中文属名 -> vernacular_names，归属到“水杉属”这个 taxon
  '乔木',                          -- 形态/生活型，当前 schema 没有专门字段
  ['绿化','观赏'],                 -- 用途类别 -> use_assertions.category
  ['Dawn redwood'],                -- 英文俗名 -> vernacular_names.name
  '一棵树，留住远古的回响。',       -- 展示文案/短标语，当前 schema 没有专门字段
  '落叶针叶乔木...',               -- 描述文本，当前 schema 没有专门字段
  '中国',                          -- 原产地/分布，当前 schema 没有专门字段
  '线形叶对生...',                 -- 识别特征，当前 schema 没有专门字段
  '用于公园...',                   -- 用途摘要 -> use_assertions.summary
  '',                              -- 可能是图片/来源/备注，需看代码定义
  []                               -- 可能是媒体、标签或扩展数据，需看代码定义
)
```
### 片段 7(js)
```js
group_code: 'gymnosperms'
group_label_zh: '裸子植物'
group_label_en: 'Gymnosperms'
external_ids: {
  wikidata: 'Q133712',
  ncbi_taxonomy: '1437180',
  gbif: '...',
  col: '...'
}
```
### 片段 8(sql)
```sql
growth_form
```
### 片段 9(sql)
```sql
life_form
```
### 片段 10(sql)
```sql
taxon_traits
```

---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
