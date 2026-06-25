---
title: LLM Inference
aliases: [大模型推理, LLM Serving]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6
  - juliet-llm#6.1
  - juliet-llm#6.4
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [transformer, decoding-strategies]
related: [prefill-decode, kv-cache, inference-metrics]
---

# LLM Inference

LLM 推理把输入 token 转换为输出 token。服务系统需要同时管理模型计算、显存、请求调度、并发、
流式输出和故障处理。

## 两个阶段

- [Prefill 与 Decode](prefill-decode.md)：前者并行处理输入，后者逐 token 生成；
- [KV Cache](kv-cache.md)：保存历史 Key/Value，避免重复计算。

## 三类优化

- **模型级**：量化、蒸馏、稀疏化、注意力结构和投机解码；
- **内核与内存级**：FlashAttention、PagedAttention、KV Cache 量化与复用；
- **调度级**：Continuous Batching、Chunked Prefill、请求优先级和阶段分离。

## 优化目标并不唯一

交互式聊天重视 TTFT 和 TPOT；批处理重视吞吐与成本；长上下文任务受 KV Cache 容量约束；严格
SLA 还需要关注尾延迟与 goodput。任何“更快”结论都必须说明负载、硬件、批大小和输出长度。

