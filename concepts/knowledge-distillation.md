---
title: Knowledge Distillation
aliases: [知识蒸馏, Teacher-Student Training]
type: concept
domain: llm
status: canonical
sources:
  - juliet-llm#2.3.3
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [supervised-fine-tuning]
related: [model-compression]
---

# Knowledge Distillation

知识蒸馏训练较小的学生模型模仿教师模型，以转移特定能力并降低部署成本。

## 黑盒蒸馏

只使用教师生成的答案、标签或偏好数据。它适用于无法访问教师权重的情况，实施简单，但可能复制教师
错误，且需要仔细控制生成数据的覆盖和质量。

## 白盒蒸馏

利用教师的 logits、特征、中间层或样本关系作为训练信号。信息更丰富，但需要访问内部状态，并解决
教师与学生架构和层级对齐问题。

## 设计要点

- 明确要蒸馏的是知识、格式、推理行为还是任务能力；
- 保留真实数据，避免训练集完全由教师自举；
- 对教师错误和不确定性进行过滤；
- 使用学生模型独立评估集；
- 检查能力压缩后的边界，而不只看平均分。

