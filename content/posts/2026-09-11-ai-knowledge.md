---
title: "2026-09-11 AI 知识库日报"
date: 2026-09-11T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 2 条对话,提炼 2 条"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(2/2 条有效)。
> 信息来源分布:Codex 桌面版 (本地)(2条)

## 今日知识要点

### 数据库重构建议
- **核心结论**: 可以按照建议重新整理数据，将“分类主干”和“生态/性状数据”分开，但需调整现有 schema。
- **关键要点**:
  - WFO/WCVP 应作为主分类骨架，NCBI 适合作为外部 ID 映射。
  - 保留现有 schema 中的 `source_records`、`dataset_releases`、`taxa`、`taxon_source_mappings`。
  - `trait` 表建议命名为 `trait_assertions` 或 `taxon_traits`，保留 `trait_name`、`trait_value`、`raw_value`、`source_id`、`reference_url`、`license_id`、`confidence_score`、`retrieved_at` 等字段。
  - 主表只保留内部 `taxon_id` 和接受名关系，避免重复和不一致。
  - 异名处理思路正确，保留 `taxonomic_status + accepted_taxon_id`。
- **信息来源**: Codex 桌面版 (本地)

### WCVP 介绍
- **核心结论**: WCVP 是 World Checklist of Vascular Plants，主要提供维管植物的学名、分类等级、accepted name / synonym 关系等信息。
- **关键要点**:
  - WCVP 由 Kew 英国皇家植物园整理，重点覆盖蕨类、裸子植物、被子植物等维管植物。
  - 提供学名、作者信息、分类等级、accepted name / synonym 关系、科属种关系、分布区域等信息。
- **信息来源**: Codex 桌面版 (本地)


---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
