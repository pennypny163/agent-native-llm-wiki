---
title: RAG 优化模式
aliases: [RAG Optimization Patterns, RAG 查询优化, RAG 索引优化]
type: reference
domain: rag
status: canonical
sources:
  - rag-deep-dive#二、RAG查询优化策略
  - rag-deep-dive#三、路由优化和问题构建策略
  - rag-deep-dive#二、Multi-representation Indexing（多表示索引）
  - rag-deep-dive#三、RAPTOR（递归抽象处理树状检索）
  - rag-deep-dive#四、ColBERT（Token级别上下文检索）
  - rag-deep-dive#4. 多向量检索（Multi-Vector Retrieval）
last_verified: 2026-07-15
freshness: medium
confidence: medium
prerequisites: [rag]
related: [build-rag-system, evaluate-rag, rag-failure-modes, hybrid-retrieval, reranking]
---

# RAG 优化模式

RAG 优化不要从“换模型”开始。先判断失败发生在查询、路由、索引、检索、重排、上下文组织还是生成阶段。

## 查询优化

| 模式 | 解决问题 | 代价 |
|---|---|---|
| Multi Query | 用户表达单一导致召回不足 | 多次检索，延迟上升 |
| RAG-Fusion | 多个查询结果需要融合排序 | 需要稳定融合策略 |
| Decomposition | 复杂问题包含多个子问题 | 需要合并子答案和覆盖检查 |
| Step Back | 具体问题缺少上位背景 | 可能引入泛化噪声 |
| HyDE | 查询与文档表达不对称 | 依赖生成的假设文档质量 |

## 路由与查询构建

| 模式 | 适用场景 | 注意点 |
|---|---|---|
| Routing | 多知识库、多工具、多模型 | 路由错误会直接错过正确来源 |
| Text-to-SQL | 结构化数据库查询 | 必须做权限、语法和安全校验 |
| Text-to-Cypher | 图数据库问答 | 需要稳定 schema 和关系建模 |
| 混合查询 | 同时需要语义召回和字段过滤 | 过滤条件过强会损伤召回 |

## 索引优化

| 模式 | 核心思想 | 适用问题 |
|---|---|---|
| Multi-representation | 用摘要、标题或问题等表示检索，返回原文 | 原文长且噪声大 |
| RAPTOR | 构建层级摘要树，支持不同抽象层级检索 | 既有细节问题又有综合问题 |
| ColBERT | token 级 late interaction，保留细粒度匹配 | 关键词和细节匹配要求高 |
| Multi-Vector | 一个文档保留多种向量表示 | 单一 embedding 难覆盖多意图 |

## 检索与重排优化

| 模式 | 作用 | 风险 |
|---|---|---|
| Parent Document Retrieval | 小块检索，大块返回 | 返回上下文可能过长 |
| Hybrid Retrieval | 结合稀疏和密集检索 | 融合权重需要调参 |
| Re-ranking | 用更强模型重新排序候选 | 增加延迟和成本 |
| CRAG | 评估检索质量，必要时纠错或外部搜索 | 系统复杂度上升 |

## 选择顺序

1. 先看知识源是否覆盖问题；
2. 再看切分和索引是否保留语义；
3. 再看查询是否需要改写、分解或路由；
4. 再看召回和重排；
5. 最后才优化生成 prompt 或更换生成模型。

优化前后都要用同一批评估样本验证，否则很容易只是在个别 demo 上变好。
