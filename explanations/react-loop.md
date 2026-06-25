---
title: ReAct 循环
aliases: [Reasoning and Acting, 思考-行动-观察]
type: explanation
domain: agent
status: canonical
sources:
  - agent-from-zero#4.1
  - juliet-llm#4.3.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [ai-agent, tool-use]
related: [agent-planning]
---

# ReAct 循环

ReAct 把推理和行动交错进行：系统根据当前状态选择行动，读取环境反馈，再决定下一步。

```text
目标 → 选择行动 → 调用工具 → 观察结果
 ↑                         ↓
 └──── 更新状态并判断是否完成 ────┘
```

它适合初始信息不足、工具结果会改变计划的任务。与一次性生成完整计划相比，它可以利用真实反馈；
代价是循环次数、模型调用成本和错误传播都可能增加。

## 工程实现不必暴露完整思维过程

可靠系统需要保存的是可审计的决策信息：

- 当前目标；
- 选择了什么工具及参数；
- 工具返回了什么；
- 如何判断步骤成功；
- 为什么继续、重试或停止。

这些结构化轨迹足以支持调试。没有必要依赖或向用户展示模型内部的长篇自由文本推理。

## 必要护栏

- 最大步骤数和总成本；
- 每轮完成条件；
- 工具参数验证；
- 重复行动检测；
- 高风险动作确认；
- 超出能力时的人工接管。

