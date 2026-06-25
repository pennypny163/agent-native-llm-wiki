# 内容模型：Diátaxis + Evergreen

知识库使用两套互补模型。

## Diátaxis：面向阅读任务

| 用户需求 | 目录 | 页面类型 |
|---|---|---|
| 从零学习并获得成功体验 | `learning-paths/` | `learning-path` / `tutorial` |
| 完成一个具体任务 | `how-to/` | `how-to` |
| 理解为什么和如何运作 | `explanations/` | `explanation` |
| 快速查询事实、参数和检查表 | `reference/` | `reference` |

`concepts/` 保存稳定定义和边界，作为多个 Diátaxis 页面共享的语义节点；`maps/` 负责导航。

## Evergreen：面向长期演化

`evergreen/` 只保存值得持续修订的核心判断。每篇必须：

- 围绕一个明确、可争论的 `claim`；
- 标记成熟度 `maturity`；
- 写明什么新证据会触发复核 `review_triggers`；
- 链接稳定概念页和支持来源；
- 随理解变化重写，而不是按时间追加流水账。

Evergreen 不是所有笔记的默认类型。术语定义放在 `concepts/`，步骤放在 `how-to/`，参数表放在
`reference/`。

