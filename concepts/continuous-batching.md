---
title: Continuous Batching
aliases: [持续批处理, Iteration Batching]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6.3.2
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [prefill-decode, kv-cache]
related: [paged-attention, inference-metrics]
---

# Continuous Batching

Continuous Batching 在每个解码迭代边界重新组成 batch：完成的请求立即释放位置，新请求可以加入，
从而减少静态批处理中等待最长序列造成的空闲。

## 为什么有效

自回归生成每轮只前进一步，不同请求的输出长度差异很大。静态 batch 必须等待最慢请求，持续批处理
则让调度器不断填补空位，提高设备利用率和吞吐。

## 调度器要处理

- Prefill 与 Decode 的资源冲突；
- 不同长度 KV Cache 的内存分配；
- 请求优先级、取消和超时；
- 长 prompt 是否分块；
- 为吞吐合批与满足延迟 SLA 的平衡。

持续批处理主要提升系统利用率，不会改变单个 token 的模型数学计算。批越大也不一定越好：排队、
尾延迟和显存压力可能随之增加。

