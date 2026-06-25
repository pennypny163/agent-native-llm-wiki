---
title: AI Agent
aliases: [智能体, LLM Agent, 基于大模型的智能体]
type: concept
domain: agent
status: canonical
sources:
  - agent-from-zero#1.2
  - agent-from-zero#2.2
  - juliet-llm#4.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: []
related: [agent-planning, agent-memory, tool-use, react-loop]
---

# AI Agent

AI Agent 是一个围绕目标持续获取状态、决定下一步行动、调用外部能力并根据结果调整行为的系统。
在本知识库中，“Agent”默认指以大语言模型作为核心决策组件的 Agent。

## 最小闭环

1. 接收目标和当前环境信息。
2. 判断任务是否已经完成。
3. 选择下一步行动，必要时调用工具。
4. 读取行动结果。
5. 更新工作状态并继续，直到完成、失败或触发人工接管。

因此，“使用了 LLM”不等于“是 Agent”。如果系统只根据一次输入生成一次文本，没有行动、反馈和
状态更新，它更接近普通的模型调用或工作流节点。

## 常见组成

- **模型**：理解任务、生成候选行动和综合结果。
- **规划**：分解目标、维护步骤并根据观察调整计划。
- **工具**：搜索、代码执行、数据库、API 或物理执行器。
- **记忆/状态**：保存当前任务状态，以及可供未来任务使用的信息。
- **控制层**：限制循环、处理异常、记录轨迹并实施权限策略。

“LLM + 规划 + 记忆 + 工具”是有用的教学概括，但工程系统不一定把它们实现为四个独立模块。

## 能力边界

Agent 的优势来自闭环执行，不来自“自主”这个标签本身。系统最终能力仍受以下因素限制：

- 模型能否正确理解任务和工具返回；
- 工具是否提供充分、可靠且权限合适的能力；
- 环境能否给出可观察的反馈；
- 是否存在明确的完成条件和失败恢复路径；
- 关键结果是否能被验证。

## 相关页面

- [规划](agent-planning.md)
- [记忆](agent-memory.md)
- [工具使用](tool-use.md)
- [ReAct 循环](../explanations/react-loop.md)

