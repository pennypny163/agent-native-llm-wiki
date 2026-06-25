---
title: Model Quantization
aliases: [模型量化, PTQ, QAT]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.3.1
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [transformer]
related: [model-compression, parameter-efficient-finetuning, llm-inference]
---

# Model Quantization

模型量化用更低精度表示权重、激活或 KV Cache，以减少存储和数据搬运，并在硬件支持时提高推理效率。

## 两种训练时机

- **PTQ**：训练完成后量化，实施成本低，通常需要校准数据；
- **QAT**：训练中模拟量化误差，使模型适应低精度，成本更高。

## 关键设计维度

- 量化对象：权重、激活、KV Cache；
- 位宽与数据类型；
- 对称或非对称量化；
- per-tensor、per-channel、per-group 等粒度；
- 是否保留离群值或关键权重的高精度；
- 目标硬件是否有对应高效 kernel。

参数文件变小不等于端到端一定更快。反量化、混合精度、批大小、内存带宽和 kernel 支持都会影响
真实延迟。

