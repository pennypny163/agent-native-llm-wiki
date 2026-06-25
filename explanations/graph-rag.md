---
title: GraphRAG
aliases: [Graph RAG, 图检索增强生成]
type: explanation
domain: rag
status: canonical
sources:
  - juliet-llm#3.6
  - juliet-llm#3.6.1
  - juliet-llm#3.6.2
last_verified: 2026-06-25
freshness: high
confidence: medium
prerequisites: [rag]
related: [agentic-rag]
---

# GraphRAG

GraphRAG 把实体、关系、事件或主题组织成图，并利用图的连接结构辅助检索与综合。它适合回答需要跨
文档关系、多跳路径或全局主题的问题。

## 典型构建过程

1. 从来源中抽取实体、关系和声明。
2. 进行实体消歧、合并和来源绑定。
3. 构建图结构，并可进一步发现社区或主题层级。
4. 为节点、边、社区摘要和原文片段建立检索入口。

## 查询方式

- **局部查询**：从具体实体出发，扩展其邻居、关系和支持文本；
- **全局查询**：利用社区或主题摘要综合整个语料中的模式；
- **混合查询**：图检索定位关系，原文检索提供精确证据。

## 何时值得使用

当问题经常涉及“谁与谁有什么关系”“一个变化影响哪些对象”“跨多份文档形成什么主题”时，图结构
可能比孤立 chunk 更有效。

如果实体抽取、消歧和来源质量不足，GraphRAG 会把噪声固化成看似权威的关系。对普通事实问答，
高质量混合检索与重排通常更简单。

