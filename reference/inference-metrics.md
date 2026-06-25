---
title: LLM 推理指标
aliases: [Inference Metrics, TTFT, TPOT, ITL, Throughput]
type: reference
domain: llm
status: canonical
sources:
  - juliet-llm#6.4
  - juliet-llm#6.4.2
  - juliet-llm#6.4.3
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [llm-inference]
related: [prefill-decode, continuous-batching]
---

# LLM 推理指标

| 指标 | 含义 | 主要受什么影响 |
|---|---|---|
| TTFT | 请求到首 token 的时间 | 排队、Prefill、输入长度 |
| TPOT / ITL | 输出 token 之间的平均延迟 | Decode、batch、KV Cache、带宽 |
| E2E Latency | 请求到完整回答的总时间 | TTFT、输出长度、TPOT |
| Tokens/s | 单请求或系统每秒生成 token 数 | 模型、硬件、batch、量化 |
| Throughput | 单位时间完成的请求或 token | 调度、并发、请求长度分布 |
| P95/P99 | 尾部延迟 | 排队、长请求、资源争用 |
| Goodput | 满足 SLA 的有效吞吐 | 延迟约束和调度策略 |
| GPU 利用率 | 设备计算忙碌程度 | batch 和 kernel；不能单独代表效率 |

## 压测必须记录

- 模型、精度和并行方式；
- GPU 型号、数量和互连；
- 输入与输出长度分布；
- 并发、到达模式和 warmup；
- 是否启用流式输出、缓存和投机解码；
- 统计窗口及错误率。

只报告“tokens/s 提升若干倍”而缺少这些条件，通常无法复现或比较。

