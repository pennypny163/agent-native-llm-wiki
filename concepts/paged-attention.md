---
title: PagedAttention
aliases: [Paged Attention, 分页注意力]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6.3.1
  - juliet-llm#6.3.3
  - juliet-llm#6.3.4
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [kv-cache]
related: [continuous-batching]
---

# PagedAttention

PagedAttention 借鉴虚拟内存分页，把每条序列逻辑连续的 KV Cache 映射到非连续的固定大小物理块。

## 解决的问题

如果按最大输出长度为每个请求预留连续显存，会产生内部浪费；不同长度请求的分配和释放又会形成外部
碎片。分页让系统按需增加 block，并通过映射表找到实际存储位置。

## 带来的能力

- 更高的 KV Cache 显存利用率；
- 支持更多并发序列；
- 更容易实现 Copy-on-Write 和共享前缀 block；
- 与 Continuous Batching 配合动态加入和移除请求。

## 代价

系统需要维护 block 表、分配器和专用注意力 kernel。block 大小影响元数据开销、碎片和访问效率，
应通过负载测试选择。

