---
title: RAG 的根本失败通常发生在生成之前
aliases: [RAG 根本失败模式]
type: evergreen
domain: rag
status: canonical
sources:
  - juliet-llm#3.1.8
  - juliet-llm#3.1.9
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [rag]
related: [rag-failure-modes, evaluate-rag]
maturity: growing
claim: 如果来源、解析或召回没有提供正确证据，更强的生成模型通常只能更流畅地掩盖失败。
review_triggers:
  - 新的端到端检索生成架构改变阶段边界
  - 评估数据表明主要错误来源发生转移
---

# RAG 的根本失败通常发生在生成之前

RAG 常被当成“给模型接一个向量数据库”，于是答案错误时首先调整提示或更换生成模型。但回答能够成立
的前提是：

1. 来源中存在正确内容；
2. 解析没有破坏表格、标题或关键关系；
3. 检索单元保留了需要的上下文；
4. 查询把正确证据召回并排到足够靠前；
5. 上下文没有被重复、冲突和无关内容淹没。

只要这些前提失败，生成阶段就没有可靠材料。更强的模型有时能凭参数知识猜对，却会破坏 RAG 的
可追溯性，也让系统难以知道答案究竟来自哪里。

因此排障应按“来源 → 解析 → 召回 → 排序 → 上下文 → 生成”的顺序进行。

