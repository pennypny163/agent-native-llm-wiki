---
title: 为什么 Self-Attention 能建模长距离依赖
aliases: [Self-Attention 长距离依赖]
type: evergreen
domain: llm
status: canonical
sources:
  - juliet-llm#1.1.2
last_verified: 2026-06-25
freshness: low
confidence: high
prerequisites: [self-attention]
related: [transformer, long-context]
maturity: growing
claim: Self-Attention 缩短了任意位置之间的信息路径，但可达不等于模型一定能可靠利用远距离信息。
review_triggers:
  - 长上下文架构或注意力机制发生根本变化
  - 新证据改变对远距离信息利用能力的理解
---

# 为什么 Self-Attention 能建模长距离依赖

在循环网络中，位置相距越远，信息通常需要经过越多次状态传递。Self-Attention 允许一个位置直接读取
另一个位置的 Value，因此任意两个位置之间的计算路径更短，训练时也能并行处理整个序列。

但这里有一个重要边界：

> “可以直接建立联系”不等于“模型一定知道应该关注哪里”。

模型能否真正使用长距离信息，还受训练数据、位置编码、注意力分布、上下文噪声和优化目标影响。
序列变长后，标准注意力的计算和显存成本也快速增加。

因此，Self-Attention 解决的是远距离交互的结构性障碍，不是长上下文可靠性的全部问题。

