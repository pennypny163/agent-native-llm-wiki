---
title: Agent Memory 不等于上下文窗口
aliases: [Memory 与 Context 的边界]
type: evergreen
domain: agent
status: canonical
sources:
  - agent-from-zero#3.4
  - juliet-llm#4.4
last_verified: 2026-06-25
freshness: medium
confidence: high
prerequisites: [agent-memory]
related: [rag, long-context]
maturity: growing
claim: 上下文是本次模型调用可见的信息；记忆是跨步骤或跨任务保存、筛选和重新引入信息的制度。
review_triggers:
  - 模型持久状态机制改变上下文与记忆的边界
  - 隐私或数据治理要求发生变化
---

# Agent Memory 不等于上下文窗口

上下文窗口描述一次调用能直接读取多少 token。扩大窗口可以减少摘要和检索，但不会自动解决：

- 哪些信息值得长期保存；
- 谁可以写入和修改；
- 何时应该取回；
- 如何区分事实、推测和过期状态；
- 如何删除错误或敏感信息。

记忆是一套生命周期机制：写入、组织、检索、验证、更新和遗忘。上下文只是记忆被重新提供给模型时的
一个载体。

把全部历史塞进上下文，会提高成本并放大噪声；把全部历史写进向量库，则会永久积累未经筛选的信息。
好的记忆系统追求的不是容量最大，而是正确的信息在正确时刻被可靠取回。

