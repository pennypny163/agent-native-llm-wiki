---
title: LLM Pretraining
aliases: [预训练, Language Model Pretraining]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#7.1
  - juliet-llm#7.2
  - juliet-llm#7.3
  - juliet-llm#7.4
  - juliet-llm#7.5
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [transformer, tokenization]
related: [supervised-fine-tuning, distributed-training]
---

# LLM Pretraining

预训练通过大规模语料上的语言建模目标，让模型学习语言规律、世界知识和可迁移表示。对于
Decoder-only 模型，常见目标是根据已有 token 预测下一个 token。

## 主要系统

- 数据收集、许可与去重；
- 质量、安全和语言过滤；
- 数据分类、配比和采样顺序；
- tokenizer 与模型架构；
- 优化器、学习率、批次和训练并行；
- checkpoint、监控和恢复；
- 独立验证集和能力评估。

## 数据决定能力边界

数据规模并不是唯一目标。重复、污染、低质量合成内容和不当配比都会影响模型。应按语言、代码、
数学、领域等 channel 分别监控 loss，而不是只看一个总 loss。

## Scaling Law 的作用

小规模实验可以帮助估计模型参数、数据 token 和计算预算的配比，但经验规律依赖架构、数据和训练
方法。它适合规划实验，不应替代实际验证。

## 继续预训练

当基础模型与目标领域的数据分布差距大时，可在领域无标注文本上继续语言建模。领域数据比例过高可能
损害通用能力，因此应同时监控领域和通用验证集，并与 RAG、SFT 等更低成本方案比较。

