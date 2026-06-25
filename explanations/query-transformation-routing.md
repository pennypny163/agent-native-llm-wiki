---
title: RAG 查询转换与路由
aliases: [Query Translation, Query Routing, 查询重写]
type: explanation
domain: rag
status: canonical
sources:
  - juliet-llm#3.1.2
  - juliet-llm#3.1.3
  - juliet-llm#3.1.4
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [rag]
related: [hybrid-retrieval, agentic-rag]
---

# RAG 查询转换与路由

用户问题不一定是最适合检索的表达。查询处理层负责把对话语言转换为检索器和数据源能有效执行的
请求。

## 查询转换

- **独立问题重写**：把依赖对话上下文的“这个怎么办”改写成完整问题。
- **Multi-query**：从多个角度生成查询，合并结果以提高召回。
- **分解**：把需要多步证据的问题拆成子问题。
- **Step-back**：生成更抽象的问题，用于召回背景知识。
- **HyDE**：先生成假设性答案或文档表示，再用它进行语义检索。

转换会增加召回范围，也可能引入模型臆测。原始问题应始终保留，转换结果应可观测，并通过评估确定
是否真正改善证据召回。

## 路由

路由选择知识库、搜索引擎、数据库、API 或特定检索策略。实现方式包括规则、分类模型、语义相似度
和 LLM 分类。

路由器应允许：

- 多源并行，而不是强制只选一个来源；
- 低置信度时回退到更广搜索；
- 记录为何选择某数据源；
- 对敏感数据源执行权限检查。

## 查询构造

面对结构化数据，系统还需要把自然语言转换为字段搜索、过滤条件、时间范围或 SQL 等可执行查询。
生成后的查询必须经过语法、字段、权限和成本验证。

