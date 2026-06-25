---
title: 向量索引
aliases: [Vector Index, ANN, ANNS, 向量检索索引]
type: concept
domain: rag
status: canonical
sources:
  - juliet-llm#3.3
  - juliet-llm#3.3.1
  - juliet-llm#3.3.8
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [text-embeddings]
related: [hybrid-retrieval, reranking]
---

# 向量索引

向量索引用于在大量高维表示中找到与查询最接近的候选。索引选择是在召回率、延迟、内存、构建成本
和更新能力之间取舍。

## 主要类别

- **Flat**：扫描全部向量，结果精确，规模增大后成本高。
- **IVF**：先把向量空间聚类，查询时只搜索部分簇；探测更多簇通常提高召回并增加延迟。
- **PQ/SQ 等量化索引**：压缩向量以降低存储和距离计算成本，可能损失召回。
- **HNSW**：在分层近邻图上导航，常提供较好的低延迟与召回平衡，但索引内存和构建成本较高。
- **磁盘型 ANN**：把大部分数据放在磁盘，以更低内存支持更大规模。

## 选择时先回答

- 数据量和增长速度多大；
- 更新是批量还是实时；
- 可接受的 Recall@K 与尾延迟；
- 是否需要元数据过滤、混合检索和多租户隔离；
- 内存、磁盘与运营预算；
- 是否需要备份、复制和高可用。

向量数据库不是 RAG 质量的替代品。错误的文档解析、表示或查询策略，无法靠更复杂的索引补救。

