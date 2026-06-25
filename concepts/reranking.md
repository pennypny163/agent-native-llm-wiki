---
title: 检索重排
aliases: [Reranking, ReRank, 精排]
type: concept
domain: rag
status: canonical
sources:
  - juliet-llm#3.4
  - juliet-llm#3.4.2
  - juliet-llm#3.4.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [rag, hybrid-retrieval]
related: [vector-index]
---

# 检索重排

重排对第一阶段召回的候选重新计算查询—文档相关性，以提高最相关证据进入上下文的概率。

## 为什么比向量相似度更精细

双编码器分别压缩查询和文档，文档表示可以预计算，因此召回很快，但查询和文档之间没有充分的
Token 级交互。Cross-Encoder 类重排器把查询与候选文档共同输入模型，可以针对当前查询建模细粒度
关系，代价是每个候选都需要额外推理。

## 两阶段检索

```text
快速召回较大候选集 → 重排模型精排 → 选择少量高质量上下文
```

第一阶段优化召回率，第二阶段优化前排精度。这通常比直接对整个文档库运行高成本模型更可行。

## 工程参数

- 初始候选数量；
- 重排模型的最大输入长度；
- 最终保留数量；
- 是否按文档去重或限制同一来源占比；
- 相关性阈值；
- 重排延迟和批处理策略。

具体模型排名和接口变化较快，应通过本领域验证集选择，而不是照搬通用榜单。

