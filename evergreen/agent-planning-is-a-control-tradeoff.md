---
title: Agent Planning 是控制与适应性的权衡
aliases: [Agent Planning 权衡]
type: evergreen
domain: agent
status: canonical
sources:
  - agent-from-zero#3.3
  - agent-from-zero#4.2
  - juliet-llm#4.3
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [agent-planning]
related: [react-loop, design-reliable-agent]
maturity: growing
claim: 计划越固定越容易审计，越动态越能适应环境；可靠 Agent 需要在两者之间设计反馈边界。
review_triggers:
  - 新规划方法显著改变成本或可靠性曲线
  - 真实任务评估显示当前权衡不成立
---

# Agent Planning 是控制与适应性的权衡

一次性计划便于估算成本、并行执行和人工审查，但它假设任务信息在开始时已经足够完整。逐步规划能够
利用工具反馈，却增加模型调用、循环和偏航风险。

可靠系统通常不是二选一，而是分层：

- 上层维护相对稳定的目标、里程碑和完成条件；
- 下层根据当前观察选择下一步行动；
- 每个阶段设置预算、验证和重新规划条件。

计划的价值不在于提前写出很多步骤，而在于让执行可约束、可观测、可停止。

