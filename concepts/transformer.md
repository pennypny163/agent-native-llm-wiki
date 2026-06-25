---
title: Transformer
aliases: [Transformer 架构]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.2
  - juliet-llm#1.2.2
  - juliet-llm#1.2.3
  - juliet-llm#1.2.4
last_verified: 2026-06-25
freshness: low
confidence: high
prerequisites: [self-attention, positional-encoding]
related: [normalization, pretraining, llm-inference]
---

# Transformer

Transformer 是以注意力和前馈网络为主要计算单元的序列模型架构。

## 基本块

一个典型块包含：

- 多头注意力；
- 逐位置前馈网络；
- 残差连接；
- LayerNorm 或 RMSNorm 等归一化。

## 三种常见结构

- **Encoder-only**：双向读取上下文，常用于理解、分类和表示学习。
- **Decoder-only**：使用因果掩码预测下一个 token，是生成式 LLM 的常见结构。
- **Encoder–Decoder**：Encoder 编码输入，Decoder 通过 Cross-Attention 读取编码结果，适合条件生成。

## Pre-Norm 与 Post-Norm

差别在归一化相对残差分支的位置。Pre-Norm 通常更容易训练很深的网络；Post-Norm 的优化行为不同，
往往需要更谨慎的初始化、学习率和 warmup。选择应视具体架构和训练配方，而不是把二者简单排序。

## 核心限制

标准全注意力对长序列成本高；自回归解码又具有逐 token 串行性。因此训练和推理系统发展出了
FlashAttention、稀疏注意力、KV Cache、PagedAttention 和投机解码等优化。

