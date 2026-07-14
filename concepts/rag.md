---
title: Retrieval-Augmented Generation
aliases: [RAG, 检索增强生成]
type: concept
domain: rag
status: canonical
sources:
  - juliet-llm#3.1
  - rag-deep-dive#一、概览
  - ai-pm-guide#▍ RAG的工作原理与产品决策
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [llm]
related: [agent-memory, agent]
---

# Retrieval-Augmented Generation

RAG 在生成回答前，从外部知识源检索与问题相关的内容，并把检索结果作为生成上下文。

从产品视角看，RAG 不是“接一个向量数据库”，而是一套让模型回答可以回到外部事实源的系统机制。

## 基本链路

1. 接收并分析查询。
2. 在索引或知识源中召回候选内容。
3. 必要时过滤、融合或重排。
4. 将相关内容和来源标识交给模型。
5. 生成回答并附上可核查引用。

这条链路可以进一步拆成离线的知识构建和在线的查询处理：

- **离线**：解析资料、切分或建立其他检索单元、生成表示、写入索引；
- **在线**：理解查询、选择数据源、召回候选、重排、构建上下文、生成与引用。

## RAG 与 Agent 的关系

RAG 主要解决“从哪里取得相关知识”。Agent 则还需要决定是否检索、选择何种工具、如何使用结果，
以及下一步采取什么行动。RAG 可以是 Agent 的一个工具或记忆检索组件，但两者不能互相替代。

## 质量取决于整条链路

向量数据库不是 RAG 的全部。内容结构、查询转换、召回、重排、上下文组织、引用和评估中的任一环节
都可能成为瓶颈。

因此 RAG 的优化也应按链路定位：先查知识源和解析，再查查询、路由、索引、召回、重排和生成。

## 体系入口

- [文档切分](chunking.md)
- [混合检索](hybrid-retrieval.md)
- [重排](reranking.md)
- [向量索引](vector-index.md)
- [查询转换与路由](../explanations/query-transformation-routing.md)
- [RAG 评估](../how-to/evaluate-rag.md)
- [RAG 失败模式](../reference/rag-failure-modes.md)
- [RAG 优化模式](../reference/rag-optimization-patterns.md)
