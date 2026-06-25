---
title: 规划 LLM 训练项目
aliases: [LLM Training Plan, 大模型训练流程]
type: how-to
domain: llm
status: canonical
sources:
  - juliet-llm#7.2
  - juliet-llm#7.3
  - juliet-llm#7.4
  - juliet-llm#2.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [pretraining]
related: [supervised-fine-tuning, distributed-training]
---

# 规划 LLM 训练项目

## 1. 先选择最低成本的干预

依次判断提示、RAG、SFT、继续预训练或从头预训练是否足够。不要把模型训练当作所有知识问题的默认
答案。

## 2. 定义能力与回归边界

列出目标任务、不可退化的通用能力、安全要求、延迟和部署预算，并在训练前冻结评估集。

## 3. 建立数据治理

记录来源、许可、版本、去重、质量分、类别、语言和使用次数。训练、验证和测试集要防止语义污染。

## 4. 做小规模实验

用小模型或短训练验证 tokenizer、数据配比、学习率、loss 曲线和评估流程，再决定扩展预算。

## 5. 设计可恢复训练

包括 checkpoint、随机种子、数据游标、优化器状态、故障恢复和异常数据回退。

## 6. 分层监控

同时观察总 loss、各数据 channel loss、梯度、吞吐、显存、硬件错误和固定能力探针。

## 7. 发布前独立评估

比较基础模型与训练后模型的收益和回归，并在真实推理模板、量化方案和部署硬件上重新评估。

