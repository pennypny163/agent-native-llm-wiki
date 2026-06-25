---
title: LLM 工程师学习路径
aliases: [大模型学习路径]
type: learning-path
domain: llm
status: canonical
sources:
  - juliet-llm#1
  - juliet-llm#2
  - juliet-llm#6
  - juliet-llm#7
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: []
related: [llm-foundations, llm-training, llm-inference]
---

# LLM 工程师学习路径

## 第一阶段：理解模型

1. [Tokenization](../concepts/tokenization.md)
2. [Text Embeddings](../concepts/text-embeddings.md)
3. [Self-Attention](../concepts/self-attention.md)
4. [Transformer](../concepts/transformer.md)
5. [位置编码](../concepts/positional-encoding.md)
6. [解码策略](../concepts/decoding-strategies.md)

## 第二阶段：理解模型如何获得能力

1. [预训练](../concepts/pretraining.md)
2. [SFT](../concepts/supervised-fine-tuning.md)
3. [PEFT](../concepts/parameter-efficient-finetuning.md)
4. [偏好优化](../concepts/preference-optimization.md)
5. [规划训练项目](../how-to/plan-llm-training.md)
6. [评估 LLM](../how-to/evaluate-llm.md)

## 第三阶段：理解模型如何上线

1. [Prefill 与 Decode](../concepts/prefill-decode.md)
2. [KV Cache](../concepts/kv-cache.md)
3. [Continuous Batching](../concepts/continuous-batching.md)
4. [PagedAttention](../concepts/paged-attention.md)
5. [推理指标](../reference/inference-metrics.md)
6. [优化推理服务](../how-to/optimize-llm-serving.md)

## 第四阶段：进入应用系统

- [RAG 主题地图](../maps/rag.md)
- [Agent 主题地图](../maps/agent.md)
