---
title: Decoding Strategies
aliases: [解码策略, Sampling, 采样策略]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.5
  - juliet-llm#1.5.1
  - juliet-llm#1.5.2
  - juliet-llm#1.5.3
  - juliet-llm#1.5.4
  - juliet-llm#1.5.5
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [tokenization]
related: [llm-inference, speculative-decoding]
---

# Decoding Strategies

解码策略从模型对下一 token 的概率分布中选择输出，决定生成的稳定性、多样性和搜索成本。

## 常见方法

- **Greedy**：每步选择最高概率 token，确定且快，但容易陷入局部最优和重复。
- **Beam Search**：保留若干高分序列，适合某些约束生成任务，但成本更高，开放式对话中未必更自然。
- **Temperature**：缩放 logits；较低时分布更尖锐，较高时更多低概率 token 获得机会。
- **Top-k**：只在概率最高的 k 个 token 中采样。
- **Top-p**：在累计概率达到阈值的最小候选集中采样。

## 选择原则

- 结构化提取、工具参数和可复现评测偏向确定性；
- 创作和多候选探索可以增加随机性；
- 采样参数必须与模型、提示和任务共同评估；
- 低 temperature 不能保证事实正确，高 temperature 也不等于更有创造力。

生成停止条件、重复惩罚、最大长度和输出约束同样属于解码系统的一部分。

