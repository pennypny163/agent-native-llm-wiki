---
title: Agent Planning
aliases: [Agent 规划, 任务规划, Planning]
type: concept
domain: agent
status: canonical
sources:
  - agent-from-zero#3.3
  - agent-from-zero#4.2
  - juliet-llm#4.3
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [ai-agent]
related: [react-loop, tool-use]
---

# Agent Planning

Agent Planning 是把目标转换为可执行行动，并在获得新信息后调整行动顺序的过程。

## 规划解决什么问题

- 复杂目标无法通过一次工具调用完成；
- 不同步骤存在依赖关系；
- 中间结果会改变后续决策；
- 系统需要知道何时完成、何时重试或何时请求人工帮助。

## 三种常见粒度

### 即时选择

每轮只决定下一个行动。适合环境不确定、反馈丰富的探索型任务，典型表现是
[ReAct 循环](../explanations/react-loop.md)。

### 先计划后执行

先生成一组步骤，再依次或并行执行。优点是可观察、易估算成本；缺点是初始计划可能很快过时。

### 分层规划

上层维护里程碑，下层为当前里程碑选择行动。它在长任务中通常比“一次规划到底”更稳健。

## 一个可执行计划应包含

- 目标和明确的完成条件；
- 步骤、依赖关系和预期产物；
- 每一步可调用的工具和权限；
- 验证方法；
- 失败、重试、回滚和升级路径；
- 时间、成本和循环次数预算。

计划不是为了产生好看的步骤列表，而是为了约束执行和支持验证。

