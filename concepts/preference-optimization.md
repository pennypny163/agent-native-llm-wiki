---
title: Preference Optimization
aliases: [偏好优化, RLHF, PPO, DPO, GRPO]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.2
  - juliet-llm#2.2.9
  - juliet-llm#2.2.10
  - juliet-llm#2.2.11
last_verified: 2026-06-25
freshness: high
confidence: medium
prerequisites: [supervised-fine-tuning]
related: [evaluate-llm]
---

# Preference Optimization

偏好优化使用人类反馈、规则奖励或比较数据，让模型输出更符合目标行为。它通常发生在预训练和 SFT
之后。

## 两类常见路线

- **基于强化学习**：训练或定义奖励，对策略模型进行更新，并限制新策略偏离参考模型；
- **直接偏好优化**：从“哪个回答更好”的成对数据直接优化策略，避免显式在线强化学习循环。

PPO、DPO、GRPO 等方法的具体目标不同，但都需要面对奖励定义、策略漂移、训练稳定性和数据偏差。

## 关键风险

- 奖励黑客：模型优化了指标而非真实意图；
- 偏好数据覆盖不足；
- 对齐税：目标行为提升但其他能力下降；
- 输出多样性和探索能力崩塌；
- 评估模型与训练目标形成自我强化偏差。

“奖励上升”不能单独证明模型变好。应同时测试真实任务正确性、通用能力、安全、风格和分布外行为。
