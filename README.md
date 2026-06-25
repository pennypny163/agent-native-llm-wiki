# LLM / Agent 知识库

这是一个面向人和 Agent 的知识管理系统。两份 Word 文档是上游资料，`sources/imported/`
保存可重建的来源层，其他目录保存经过整理、验证和链接的知识。

## 从这里开始

- [LLM 主题地图](maps/llm.md)
- [LLM 工程师学习路径](learning-paths/llm-engineer.md)
- [RAG 主题地图](maps/rag.md)
- [Agent 主题地图](maps/agent.md)
- [Agent 工程师学习路径](learning-paths/agent-engineer.md)
- [知识库维护方法](meta/maintenance.md)
- [内容模型：Diátaxis + Evergreen](meta/content-model.md)
- [Evergreen 核心判断](evergreen/)

## 内容层级

| 层级 | 目录 | 用途 | 是否允许人工修改 |
|---|---|---|---|
| 原始资料 | 根目录下的 `.docx` | 原始事实与上下文 | 否 |
| 来源层 | `sources/imported/` | DOCX 的结构化、可检索副本 | 否，可重新生成 |
| 证据层 | `evidence/` | 来源清单、验证记录、冲突记录 | 是 |
| 规范知识层 | `concepts/`、`explanations/`、`reference/` | 去重后的当前最佳表述 | 是 |
| 行动层 | `how-to/`、`learning-paths/` | 完成任务和学习的路径 | 是 |
| 导航层 | `maps/` | 主题关系与入口 | 是 |

## 常用命令

```bash
# 完整重建来源层、索引并验证
make build_wiki

# 增量导入并列出受影响的知识页
make apply_updates

# 完整验证
make verify_wiki

# 分层搜索
make search Q="KV Cache"
```

## 核心原则

1. 原始资料不直接改写。
2. 一个主题只保留一篇 `canonical` 页面，其他页面链接到它。
3. 结论必须能回到来源文档及其章节。
4. 教程、操作指南、解释和参考资料分开组织。
5. 模型、框架、价格、API 等易变信息必须标注验证日期。

Git 跟踪 Markdown、脚本和规则；原始 Word、来源图片和本地索引属于可重建二进制，不进入普通 Git
历史。
