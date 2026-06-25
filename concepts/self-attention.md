---
title: Self-Attention
aliases: [自注意力, Scaled Dot-Product Attention]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.1
  - juliet-llm#1.1.2
  - juliet-llm#1.1.3
last_verified: 2026-06-25
freshness: low
confidence: high
prerequisites: [tokenization]
related: [transformer, positional-encoding, kv-cache]
---

# Self-Attention

Self-Attention 让序列中每个位置根据同一序列的其他位置构造上下文化表示。

## 核心计算

输入表示经过线性投影得到 Query、Key 和 Value：

```text
Attention(Q, K, V) = softmax(QKᵀ / √dₖ) V
```

Query 表示当前位置要寻找什么，Key 表示各位置可被匹配的特征，Value 是匹配后汇总的信息。
缩放因子避免维度增大时点积过大，使 softmax 进入饱和区域。

## 多头注意力

多头注意力使用多组投影并行计算，再拼接输出。不同头可以学习不同的关系模式，但“每个头必然具有
可解释语义”并不是架构保证。

## 优势与成本

- 序列位置之间的路径短，便于建模远距离依赖；
- 训练时可并行处理整段序列；
- 标准注意力的时间和注意力矩阵空间通常随序列长度平方增长；
- 注意力本身不包含顺序，需要结合 [位置编码](positional-encoding.md)。

自回归生成时，因果掩码阻止当前位置读取未来 token；[KV Cache](kv-cache.md) 则避免重复计算历史
位置的 Key 和 Value。

