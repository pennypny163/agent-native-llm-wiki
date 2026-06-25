---
title: 设计可靠的 Agent
aliases: [Agent 可靠性指南]
type: how-to
domain: agent
status: canonical
sources:
  - agent-from-zero#5
  - agent-from-zero#9
  - juliet-llm#4.3
  - juliet-llm#4.6
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [ai-agent, agent-planning, tool-use]
related: [agent-component-checklist]
---

# 设计可靠的 Agent

## 1. 先定义完成条件

把“做好调研”改为可验证产物，例如：覆盖哪些问题、使用多少独立来源、必须包含哪些字段，以及什么
情况算失败。

## 2. 从最小闭环开始

先实现一个模型、少量工具和明确状态机。只有发现真实瓶颈后，再增加长期记忆、多 Agent 或复杂规划。

## 3. 限制行动空间

- 只提供当前任务需要的工具；
- 使用结构化输入输出；
- 区分读取和写入；
- 对不可逆或高影响操作增加确认。

## 4. 每一步都验证

不要把“工具调用没有报错”当成任务成功。检查返回内容、目标对象、数量、状态变化和必要的外部证据。

## 5. 设计失败路径

设置最大循环数、超时、成本预算、重试策略、重复动作检测，以及无法继续时需要返回给人的上下文。

## 6. 保存可审计轨迹

记录目标、工具调用、关键观察、状态变化和最终验证结果。避免只保存最终自然语言答案。

## 7. 用任务集评估

评估至少覆盖：

- 任务完成率；
- 工具选择和参数正确率；
- 最终结果正确性；
- 高风险错误率；
- 延迟和成本；
- 失败后能否安全停止或恢复。

