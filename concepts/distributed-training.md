---
title: Distributed LLM Training
aliases: [分布式训练, 数据并行, 张量并行, 流水线并行]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.4
  - juliet-llm#2.4.1
  - juliet-llm#2.4.2
  - juliet-llm#2.4.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [pretraining]
related: [llm-inference]
---

# Distributed LLM Training

分布式训练把模型、数据和优化器状态分布到多个设备，以突破单卡容量或缩短训练时间。

## 主要并行维度

- **数据并行**：每个副本处理不同样本，再同步梯度；
- **张量并行**：把单个算子或权重矩阵切到多个设备；
- **流水线并行**：把不同层分配到不同阶段，以 micro-batch 形成流水；
- **序列并行**：沿序列维度切分部分激活计算；
- **状态分片**：分散参数、梯度和优化器状态。

## 主要成本

并行不是免费加速。通信、负载不均、流水线气泡、重计算、offload 和容错都会降低有效利用率。

## 选择原则

1. 先估算参数、梯度、优化器状态和激活显存。
2. 优先使用通信最少且能容纳模型的组合。
3. 让拓扑与服务器内高速互连、跨机网络相匹配。
4. 用模型 FLOPs 利用率、吞吐和稳定性衡量，而不只看 GPU 数量。

