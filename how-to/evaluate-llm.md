---
title: 评估 LLM
aliases: [LLM Evaluation, 大模型评估]
type: how-to
domain: llm
status: canonical
sources:
  - juliet-llm#7.4
  - juliet-llm#6.4
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [pretraining]
related: [inference-metrics, preference-optimization]
---

# 评估 LLM

模型评估需要同时回答“学会了什么、退化了什么、上线后是否可用”，不能只依赖单一 benchmark。

## 训练层

- 总 loss 和按语言、领域、代码等划分的 channel loss；
- 梯度、学习率和数值稳定性；
- 独立验证集上的 perplexity；
- 固定概率探针和数据污染检查。

Perplexity 适合比较同一 tokenizer 和相近设置下的训练进展，不适合直接横跨不同 tokenizer 排名。

## 能力层

根据目标任务建立可复现评估集，覆盖知识、推理、代码、工具调用、长上下文、格式遵循和多语言。
公开 benchmark 可作为参照，但必须补充真实业务任务。

## 行为与风险层

- 幻觉和证据支持；
- 拒答、澄清和边界情况；
- 偏见、毒性和敏感信息；
- 对抗提示与越权工具调用；
- SFT 或偏好优化后的通用能力回归。

## 部署层

在最终聊天模板、解码参数、量化模型和实际硬件上重新评估：

- 正确性和格式；
- TTFT、TPOT、尾延迟和吞吐；
- 成本与显存；
- 并发下的错误和稳定性。

模型评审可以帮助扩展测试规模，但其偏差必须用人工抽检和确定性验证器校准。

