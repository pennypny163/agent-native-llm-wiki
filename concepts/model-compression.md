---
title: Model Compression
aliases: [模型压缩, 剪枝, 蒸馏]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.3
  - juliet-llm#2.3.2
  - juliet-llm#2.3.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [transformer]
related: [model-quantization, knowledge-distillation]
---

# Model Compression

模型压缩降低部署所需的存储、显存、计算或延迟。主要路线包括量化、剪枝和知识蒸馏。

## 剪枝

剪枝删除权重、通道、注意力头或整层。非结构化稀疏如果缺乏硬件和 kernel 支持，参数变少也可能没有
实际加速；结构化剪枝更容易转化为密集矩阵上的收益，但对能力影响可能更大。

## 量化

参见 [模型量化](model-quantization.md)。它通常是部署中最先尝试的压缩方式，因为不必改变模型拓扑。

## 蒸馏

参见 [知识蒸馏](knowledge-distillation.md)。它通过训练较小学生模型学习教师模型的输出或内部表示，
可以获得真正更小的网络。

压缩方案应以目标硬件上的质量—延迟—吞吐—成本曲线评估，而不是只比较参数量或文件大小。

