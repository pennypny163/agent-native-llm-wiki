---
title: Parameter-Efficient Fine-Tuning
aliases: [PEFT, 参数高效微调, LoRA, QLoRA]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.1.1
  - juliet-llm#2.1.2
  - juliet-llm#2.1.3
  - juliet-llm#2.1.5
  - juliet-llm#2.1.6
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [supervised-fine-tuning]
related: [model-quantization]
---

# Parameter-Efficient Fine-Tuning

PEFT 冻结大部分基础模型参数，只训练少量新增或选定参数，以降低显存、存储和多任务适配成本。

## LoRA

LoRA 为权重更新增加低秩分解矩阵，只训练这些矩阵。适配器可以按任务单独保存，并在部署前合并到
基础权重或运行时加载。

关键选择包括：

- 应用到哪些层和投影矩阵；
- rank、缩放和 dropout；
- 学习率与目标模块覆盖范围；
- 是否合并权重；
- 多适配器如何组合。

## QLoRA

QLoRA 以低比特形式存储冻结的基础模型权重，计算时反量化到较高精度，同时训练 LoRA 参数。它主要
降低基础权重和优化过程的显存压力，不代表所有计算都在 4-bit 中完成。

## 其他方法

Adapter 在网络中插入小型模块；Prefix/Prompt Tuning 学习连续提示表示。它们在延迟、上下文占用、
表达能力和部署复杂度上有不同取舍。

PEFT 降低训练成本，但不自动保证质量。仍需与全量微调基线比较，并在目标任务、通用能力和安全集上
评估。

