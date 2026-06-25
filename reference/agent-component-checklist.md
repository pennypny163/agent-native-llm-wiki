---
title: Agent 组件检查表
aliases: [Agent Checklist]
type: reference
domain: agent
status: canonical
sources:
  - agent-from-zero#3
  - agent-from-zero#5
  - juliet-llm#4.1
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [ai-agent]
related: [design-reliable-agent]
---

# Agent 组件检查表

## 目标

- [ ] 目标可以被系统明确表示
- [ ] 存在可执行的完成条件
- [ ] 明确失败、取消和人工接管条件

## 状态与规划

- [ ] 当前任务状态可持久化和恢复
- [ ] 步骤包含预期产物与验证方式
- [ ] 有循环次数、时间和成本预算

## 工具

- [ ] 工具名称和描述可区分
- [ ] 参数具有结构和约束
- [ ] 返回值包含结果与错误细节
- [ ] 写操作具备确认、幂等或回滚策略
- [ ] 权限遵循最小授权

## 记忆

- [ ] 区分工作状态、历史事件和语义知识
- [ ] 写入前有筛选规则
- [ ] 检索结果包含来源与时间
- [ ] 支持更正、删除和隐私控制

## 观测与评估

- [ ] 保存关键工具调用和状态变化
- [ ] 能重放或解释失败路径
- [ ] 有代表性的任务评估集
- [ ] 同时测量正确性、风险、延迟与成本

