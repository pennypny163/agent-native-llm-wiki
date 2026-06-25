---
title: KV Cache
aliases: [Key-Value Cache, 键值缓存]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6.2
  - juliet-llm#6.2.1
  - juliet-llm#6.2.2
  - juliet-llm#6.2.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [self-attention, prefill-decode]
related: [paged-attention, continuous-batching]
---

# KV Cache

KV Cache 保存每层历史 token 的 Key 和 Value。生成新 token 时，只计算当前位置的 Q/K/V，并让 Query
与缓存交互，避免反复重算整个前缀。

## 空间成本

KV Cache 大小大致随以下因素线性增长：

- 并发序列数；
- 上下文和输出总长度；
- 层数；
- KV head 数与 head dimension；
- 存储精度。

因此它常成为长上下文和高并发服务的主要显存约束。

## 常见优化

- MQA/GQA 减少 KV head 数；
- 低精度存储；
- 滑动窗口或稀疏保留；
- GPU、CPU 甚至磁盘之间的分层调度；
- [PagedAttention](paged-attention.md) 减少分配碎片；
- 对共享系统提示或文档前缀进行跨请求复用。

缓存复用必须绑定模型版本、tokenizer、精确 token 前缀和推理配置，否则可能复用错误状态。

