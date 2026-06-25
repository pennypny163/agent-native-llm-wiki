---
title: Supervised Fine-Tuning
aliases: [SFT, 有监督微调, 指令微调]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [pretraining]
related: [parameter-efficient-finetuning, preference-optimization]
---

# Supervised Fine-Tuning

SFT 使用输入—目标输出样本继续训练预训练模型，使模型学会任务格式、交互风格、工具调用模式或领域
行为。

## SFT 擅长

- 输出格式和风格；
- 指令遵循；
- 特定任务流程；
- 工具调用示例；
- 把已有能力稳定地映射到业务场景。

## SFT 不等同于知识库

用 SFT 注入大量易变事实，更新和追溯成本高，也可能造成灾难性遗忘或行为退化。动态知识通常更适合
RAG；数据分布差距很大时可考虑继续预训练。

## 数据质量

高质量、覆盖边界情况且相互一致的数据通常比机械扩充数量更重要。训练前应检查：

- 指令和答案是否真实可执行；
- 格式与线上推理模板是否一致；
- 是否包含拒答、澄清和失败样本；
- 合成数据是否带来单一模型的偏差；
- 训练集与评估集是否污染。

全量微调还是 PEFT，应根据资源、任务差异、数据量和部署方式实验决定。

