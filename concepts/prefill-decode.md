---
title: Prefill and Decode
aliases: [预填充与解码, Prefill, Decode]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6.1
  - juliet-llm#6.1.1
  - juliet-llm#6.1.2
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [llm-inference]
related: [kv-cache, continuous-batching, inference-metrics]
---

# Prefill and Decode

自回归 LLM 生成分为资源特征不同的两个阶段。

## Prefill

Prefill 一次并行处理完整输入，计算隐藏状态并为各层建立 KV Cache。长 prompt 会带来大规模矩阵
计算，通常更偏计算密集，并直接影响首 token 延迟。

## Decode

Decode 每轮处理一个新 token，读取历史 KV Cache，追加当前 Key/Value 并产生下一 token。它并行度
较低、重复次数多，通常更受显存带宽和 KV Cache 访问影响。

## 为什么要区分

同一硬件和调度策略很难同时适合两个阶段。常见优化包括：

- Chunked Prefill，避免长输入长期占用调度；
- Prefill/Decode 分离部署；
- Decode 请求持续合批；
- 共享前缀复用 Prefill 产生的 KV Cache。

阶段分离增加了 KV 传输、路由和容量规划复杂度，应在真实请求分布下验证收益。

