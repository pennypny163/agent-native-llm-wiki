---
title: Text Embeddings
aliases: [文本嵌入, 语义向量, Embedding]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.7
  - juliet-llm#1.7.1
  - juliet-llm#1.7.2
  - juliet-llm#1.7.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [tokenization]
related: [rag, hybrid-retrieval, reranking]
---

# Text Embeddings

文本嵌入把文本映射为可比较的数值表示。需要区分模型内部的 token embedding 与面向检索、聚类等
任务的句子或文档 embedding。

## 静态与上下文化表示

早期静态表示为每个词提供固定向量，无法根据上下文区分多义词。上下文化模型则让同一 token 的表示
随句子变化。

## 检索中的双编码器

双编码器分别编码查询和文档，再用点积或余弦相似度比较。文档向量可离线计算，因此适合大规模召回；
缺点是查询和文档在编码阶段缺少细粒度交互。

## 训练信号

检索 embedding 常通过对比学习训练：提高查询与正样本的相似度，降低与负样本的相似度。批次大小、
困难负样本、领域数据和查询—文档不对称性会显著影响效果。

## 使用注意

- 统一模型不一定适合所有语言和领域；
- 长文本压缩成单个向量可能丢失局部信息；
- 相似度高不等于事实支持；
- 更换模型后通常需要重新生成文档向量；
- 应在自己的查询—证据评估集上选择模型。

