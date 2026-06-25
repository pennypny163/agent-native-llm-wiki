---
title: Transformer Normalization
aliases: [归一化, LayerNorm, RMSNorm]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#1.6
  - juliet-llm#1.6.2
  - juliet-llm#1.6.5
last_verified: 2026-06-25
freshness: low
confidence: high
prerequisites: [transformer]
related: [pretraining]
---

# Transformer Normalization

归一化控制隐藏表示的尺度，改善深层网络的优化稳定性。Transformer 中常见的是 LayerNorm 和
RMSNorm，而不是依赖批次统计的 BatchNorm。

## LayerNorm

对单个 token 表示的特征维度计算均值和方差，再应用可学习缩放与偏置。它不依赖其他样本，适合变长
序列和小批次训练。

## RMSNorm

只根据均方根缩放，不执行均值中心化，计算更简单。它保留可学习缩放，并常用于现代 Decoder-only
模型。

## 放置位置

Pre-Norm 和 Post-Norm 描述归一化相对残差分支的位置。它会影响梯度传播和训练配方，不能只把
Normalization 当作可随意替换的局部组件。

