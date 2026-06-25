---
title: 优化 LLM 推理服务
aliases: [LLM Serving Optimization]
type: how-to
domain: llm
status: canonical
sources:
  - juliet-llm#6.1
  - juliet-llm#6.2
  - juliet-llm#6.3
  - juliet-llm#6.4
  - juliet-llm#6.6
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [llm-inference]
related: [inference-metrics]
---

# 优化 LLM 推理服务

## 1. 明确负载和 SLA

记录输入长度、输出长度、到达率、并发、流式需求、TTFT/TPOT 目标和成本上限。没有负载模型就没有
可解释的优化。

## 2. 建立分阶段基线

分别测量排队、tokenization、Prefill、Decode 和网络时间，并记录 KV Cache 峰值。

## 3. 优先解决主要瓶颈

- 显存不足：量化、GQA/MQA、KV Cache 低精度、分页或 offload；
- 吞吐不足：Continuous Batching、合理 batch、更多副本；
- TTFT 高：Prefill 优化、Chunked Prefill、前缀缓存；
- TPOT 高：更高效 kernel、量化、张量并行或投机解码；
- 长尾严重：优先级、长度限制、隔离长请求和 admission control。

## 4. 再考虑复杂架构

Prefill/Decode 分离、多级 KV 存储和多节点并行会增加网络、路由和故障复杂性。只有单机或简单副本
无法满足目标时再引入。

## 5. 验证质量没有退化

量化、上下文截断、近似接受和推理链压缩都可能改变输出。性能测试必须与任务质量、格式正确率和安全
评估一起运行。

