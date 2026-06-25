---
title: 混合检索
aliases: [Hybrid Retrieval, 稀疏与密集检索]
type: concept
domain: rag
status: canonical
sources:
  - juliet-llm#3.1.6
  - juliet-llm#3.4.4
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [rag, text-embeddings]
related: [reranking, vector-index]
---

# 混合检索

混合检索组合词法检索与语义检索，以覆盖不同类型的相关性。

## 两类召回互补

- **稀疏/词法检索**擅长精确词项、编号、人名、产品名和罕见术语；
- **密集/向量检索**擅长同义表达、自然语言改写和语义相近内容。

只使用其中一种，会分别面临“词不匹配”或“精确细节被语义平均化”的问题。

## 典型流程

1. 用同一查询分别执行词法与向量检索。
2. 规范化不同检索器的分数，或只使用各自排名。
3. 用加权融合或 Reciprocal Rank Fusion 合并候选。
4. 去重后交给 [重排](reranking.md) 模型精排。

## 应优先优化什么

召回阶段的目标是让正确证据进入候选集，不必过早追求完美排序。候选集太小会漏掉证据；太大会增加
重排成本和噪声。应通过查询集测量 Recall@K、命中率和延迟，而不是凭直觉设置 K。

