---
title: 单 Agent 与多 Agent
aliases: [Single-agent vs Multi-agent, 多智能体]
type: explanation
domain: agent
status: canonical
sources:
  - agent-from-zero#6
  - juliet-llm#4.2
  - juliet-llm#4.6
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [ai-agent]
related: [agent-planning]
---

# 单 Agent 与多 Agent

多 Agent 的价值不在于“模拟一个团队”，而在于任务是否真的需要独立上下文、并行执行、权限隔离或
不同的优化目标。

## 优先选择单 Agent

当一个 Agent 可以在同一状态空间中可靠完成任务时，单 Agent 通常更容易调试、评估和控制成本。
角色提示不同并不足以证明需要多个 Agent。

## 多 Agent 可能合理的情况

- 子任务可以真正并行；
- 不同角色需要隔离的工具权限或数据；
- 独立验证者能使用不同证据检查产物；
- 上下文过大，需要按领域拆分；
- 工作天然跨越多个长期运行的责任边界。

## 新增的系统成本

- 通信和状态同步；
- 任务重复、遗漏或互相覆盖；
- 错误在 Agent 之间传播；
- 难以确定最终责任和完成条件；
- Token、延迟和观测成本增加。

设计多 Agent 前，应先证明“拆分带来的收益大于协调成本”，并为每个 Agent 定义输入、输出、
权限和验收条件。

