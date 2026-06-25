---
title: Positional Encoding
aliases: [位置编码, Position Embedding, RoPE]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.4
  - juliet-llm#1.4.1
  - juliet-llm#1.4.2
  - juliet-llm#1.4.3
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [self-attention]
related: [transformer, long-context]
---

# Positional Encoding

Self-Attention 对输入排列本身不敏感，位置编码把顺序或相对距离引入表示或注意力计算。

## 主要思路

- **绝对位置表示**：为每个位置提供固定或可学习向量；
- **相对位置偏置**：根据两个 token 的距离调整注意力分数；
- **RoPE**：对 Query 和 Key 施加与位置相关的旋转，使内积自然包含相对位置信息；
- **ALiBi 等偏置方法**：直接对不同距离的注意力分数加入规则化偏置。

## 与长上下文的关系

模型能接收更长位置编号，不代表能可靠使用长上下文。扩展方法需要同时考虑：

- 训练时见过的长度分布；
- 位置表示在新长度上的外推或插值；
- 注意力和 KV Cache 成本；
- 信息在长上下文中的可检索性；
- 短上下文能力是否退化。

因此上下文窗口大小应通过实际任务和位置分布评估，而不能只看配置中的最大 token 数。

