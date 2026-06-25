---
title: Long Context
aliases: [长上下文, 上下文窗口扩展]
type: explanation
domain: llm
status: canonical
sources:
  - juliet-llm#3.5
  - juliet-llm#3.5.1
  - juliet-llm#3.5.2
  - juliet-llm#3.5.3
  - juliet-llm#3.5.4
last_verified: 2026-06-25
freshness: high
confidence: medium
prerequisites: [transformer, positional-encoding]
related: [rag, kv-cache]
---

# Long Context

长上下文技术扩大模型一次可接收或有效利用的信息范围，但“窗口更大”“成本可接受”和“能准确使用
远处信息”是三个不同目标。

## 主要路径

- 调整位置编码的外推或插值；
- 稀疏、滑动窗口或近似注意力；
- 分段处理、层级摘要和提示压缩；
- 改善注意力内核、并行和内存管理；
- 训练时加入更长序列并专门评估。

## 与 RAG 的关系

长上下文减少了必须精确切分和召回的压力，RAG 则减少了每次输入无关资料的成本。实际系统常将二者
组合：检索定位候选文档，较长窗口保留更完整的局部上下文。

## 评估陷阱

单个“needle in a haystack”命中率不足以代表真实长文档能力。还需要测试多证据整合、位置变化、
干扰信息、顺序关系、延迟和 KV Cache 占用。

