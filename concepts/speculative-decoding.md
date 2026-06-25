---
title: Speculative Decoding
aliases: [投机解码, 推测解码, Draft-and-Verify]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#6.6
  - juliet-llm#6.6.1
  - juliet-llm#6.6.2
  - juliet-llm#6.6.3
  - juliet-llm#6.6.4
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [llm-inference, decoding-strategies]
related: [inference-metrics]
---

# Speculative Decoding

投机解码先用更便宜的机制生成多个候选 token，再由目标模型并行验证，希望一次接受多个 token，减少
昂贵的串行解码轮数。

## 两个组件

- **Drafter**：小模型、目标模型的浅层/额外头、n-gram 或其他快速预测器；
- **Verifier**：目标模型对候选进行并行评分并接受、修正或拒绝。

某些验证算法可以保持与目标模型原始采样分布一致；近似接受方法可能用质量和分布变化换取更高速度。

## 加速由什么决定

- 每轮候选数量；
- 候选 token 接受率；
- drafter 自身延迟；
- 验证 batch 的计算效率；
- 目标模型、硬件和当前服务 batch。

候选越多不一定越快。额外计算超过内存带宽瓶颈后，收益会下降。应同时测量有效接受长度、端到端
延迟和输出一致性。

