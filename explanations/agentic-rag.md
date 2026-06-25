---
title: Agentic RAG
aliases: [代理式 RAG, Agent RAG]
type: explanation
domain: rag
status: canonical
sources:
  - juliet-llm#3.7
  - juliet-llm#3.7.1
  - juliet-llm#3.7.2
  - juliet-llm#3.7.3
last_verified: 2026-06-25
freshness: high
confidence: high
prerequisites: [rag, ai-agent]
related: [query-transformation-routing, graph-rag]
---

# Agentic RAG

Agentic RAG 让系统根据任务和中间结果动态决定是否检索、检索什么、使用哪个来源、是否需要再次检索
或验证，而不是固定执行一次“召回后生成”。

## 与普通 RAG 的差别

普通 RAG 的流程通常预先确定；Agentic RAG 引入规划、工具选择、反馈和状态，使检索策略可以随查询
变化。

适合的场景包括：

- 问题必须分解为多个子问题；
- 数据分散在文档、数据库和实时 API；
- 中间证据决定下一步检索；
- 需要验证、纠错或补充证据。

## 最小可用设计

单 Agent 通常已经足够：

1. 对问题分类并制定检索计划；
2. 调用一个或多个检索工具；
3. 判断证据是否充分和一致；
4. 必要时改写查询或换数据源；
5. 基于证据生成带引用回答。

只有在并行、权限隔离或独立验证确有收益时，才应增加多个 Agent。

## 主要风险

- 检索循环和成本失控；
- 模型根据错误中间结论继续搜索；
- 多 Agent 状态不同步；
- 重复查询和来源污染；
- 将“反思文本”误当成真实验证。

因此需要步骤预算、明确完成条件、外部验证器、来源追踪和可重放轨迹。

