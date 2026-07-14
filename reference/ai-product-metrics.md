---
title: AI 产品指标体系
aliases: [AI Product Metrics, AI 产品评估指标]
type: reference
domain: ai-pm
status: canonical
sources:
  - ai-pm-guide#模型测评思路
  - ai-pm-guide#▶️ 步骤7：构建AI产品经理的决策模型
  - interview-playbook-27#Part 8 ：数据分析
  - rag-deep-dive#3. 评估RAG：如何知道你的系统靠不靠谱？
last_verified: 2026-07-15
freshness: medium
confidence: high
prerequisites: [ai-product-manager]
related: [evaluate-ai-feature, evaluate-rag, ai-product-patterns]
---

# AI 产品指标体系

AI 产品评估不能只看“准确率”。准确率只能说明模型输出和标准答案的匹配程度，不能证明用户任务完成、产品体验变好或商业结果成立。

## 指标分层

| 层级 | 典型指标 | 回答的问题 |
|---|---|---|
| 模型质量 | 准确率、召回率、忠实度、拒答正确率、安全违规率 | 模型本身是否可靠 |
| 检索与上下文 | Recall@K、MRR、NDCG、引用准确率、上下文相关性 | 正确信息是否进入上下文 |
| 任务完成 | 任务完成率、一次解决率、人工接管率、编辑率、采纳率 | 用户是否真的完成任务 |
| 体验 | 首 token 延迟、总延迟、失败恢复率、满意度 | 使用过程是否可接受 |
| 商业 | 转化率、留存、ARPU、单次任务成本、ROI | 是否创造可持续价值 |
| 风险治理 | 幻觉率、敏感内容率、投诉率、误操作率、审计通过率 | 错误是否被控制在可接受范围 |

## AI PM 常用指标组合

### AI Search / RAG

- 检索召回：Recall@K、MRR、NDCG；
- 答案质量：faithfulness、answer relevancy、context relevancy；
- 引用质量：声明级引用准确率；
- 用户结果：问题解决率、追问率、人工转接率。

### Copilot

- 建议采纳率；
- 采纳后编辑率；
- 任务节省时间；
- 用户撤销率；
- 专家复核通过率。

### Agent

- 任务完成率；
- 计划成功率；
- 工具调用成功率；
- 人工确认次数；
- 越权或错误动作率；
- 单任务成本和耗时。

### AIGC 内容工具

- 首版可用率；
- 编辑轮次；
- 生成内容发布率；
- 风格一致性；
- 审核拦截率；
- 内容带来的转化或互动。

## 反模式

- 只报模型 benchmark，不报用户任务指标；
- 只看平均分，不拆查询类型、用户分层和失败类别；
- 只看满意度，不看真实采纳和复访；
- 只看单次调用效果，不看成本、延迟和规模化稳定性；
- 把“用户没有投诉”误判为“AI 功能可用”。

## 指标选择原则

每个 AI 功能至少要有四类指标：

1. 一个质量指标，证明输出可用；
2. 一个任务指标，证明用户获得结果；
3. 一个体验指标，证明流程可接受；
4. 一个约束指标，证明成本和风险可控。
