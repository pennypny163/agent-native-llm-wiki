---
title: Agent 工程师学习路径
aliases: [Agent 学习路径]
type: learning-path
domain: agent
status: canonical
sources:
  - agent-from-zero#1
  - agent-from-zero#3
  - juliet-llm#4
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: []
related: [agent]
---

# Agent 工程师学习路径

## 第一阶段：建立正确心智模型

1. [AI Agent](../concepts/ai-agent.md)
2. [工具使用](../concepts/tool-use.md)
3. [ReAct 循环](../explanations/react-loop.md)

目标：能区分普通 LLM 调用、固定工作流和闭环 Agent。

## 第二阶段：理解长任务

1. [规划](../concepts/agent-planning.md)
2. [记忆](../concepts/agent-memory.md)
3. [RAG](../concepts/rag.md)

目标：能设计任务状态、完成条件、检索和失败恢复。

## 第三阶段：构建可靠系统

1. [可靠 Agent 设计指南](../how-to/design-reliable-agent.md)
2. [Agent 组件检查表](../reference/agent-component-checklist.md)
3. [单 Agent 与多 Agent](../explanations/single-vs-multi-agent.md)

目标：先构建可评估的单 Agent，再根据真实瓶颈决定是否增加多 Agent。

## 第四阶段：回到完整来源

- 阅读 [Agent 入门资料](../sources/imported/agent-from-zero/index.md) 获取教程、案例和代码。
- 阅读 [居丽叶 LLM 体系：Agent 篇](../sources/imported/juliet-llm/4-4-agent篇.md)
  补充 Planning、Memory、Tool、MCP 与多 Agent 失败模式。

来源中的框架代码具有时效性。实际运行前应重新核对对应项目的官方文档。

