---
title: Agent Tool Use
aliases: [工具使用, Tool Calling, Function Calling]
type: concept
domain: agent
status: canonical
sources:
  - agent-from-zero#3.5
  - juliet-llm#4.5
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [ai-agent]
related: [agent-planning, react-loop]
---

# Agent Tool Use

工具使用把模型生成的意图连接到外部读取或写入操作。工具可以是函数、API、搜索系统、数据库、
代码执行环境或其他 Agent。

## 好工具的接口特征

- 名称和描述能清楚区分使用场景；
- 输入结构明确，字段含义和约束具体；
- 返回值稳定、结构化并带错误信息；
- 读操作和写操作可以区分；
- 高风险写操作支持预览、确认、幂等或回滚；
- 结果包含验证所需的信息，而不只返回“成功”。

## 工具选择不是越多越好

工具过多或描述重叠会增加误选概率。优先给 Agent 当前任务真正需要的最小工具集，并把复杂工具拆成
可理解但不过度琐碎的操作。

## 可靠调用流程

1. 根据目标选择工具。
2. 检查参数和权限。
3. 执行并读取结构化结果。
4. 验证结果是否满足当前步骤。
5. 更新任务状态，决定继续、重试或终止。

具体 SDK 和框架接口变化快，来源文档中的代码示例应视为教学材料，使用前需重新核对官方文档。

