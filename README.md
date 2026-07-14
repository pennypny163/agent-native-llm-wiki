# Agent-Native AI Wiki

[公开 Wiki](https://pennypny163.github.io/agent-native-llm-wiki/) ·
[MCP 使用说明](meta/mcp.md)

这是一个面向人和 Agent 的 AI 知识管理系统。Word 文档是上游资料，`sources/imported/`
保存本地可重建的来源层，其他目录保存经过整理、验证和链接的知识。

## 从这里开始

- [LLM 主题地图](maps/llm.md)
- [LLM 工程师学习路径](learning-paths/llm-engineer.md)
- [RAG 主题地图](maps/rag.md)
- [Agent 主题地图](maps/agent.md)
- [Agent 工程师学习路径](learning-paths/agent-engineer.md)
- [AI 产品管理主题地图](maps/ai-product-management.md)
- [AI PM 秋招面试准备路线](learning-paths/ai-pm-interview-prep.md)
- [知识库维护方法](meta/maintenance.md)
- [内容模型：Diátaxis + Evergreen](meta/content-model.md)
- [Evergreen 核心判断](evergreen/)
- [发布 MkDocs Wiki](meta/publishing.md)
- [MCP 知识服务](meta/mcp.md)

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

# 生成公开 Wiki 发布视图
make docs-prepare

# 安装 requirements-docs.txt 后本地预览
make docs-serve

# 测试和演示 MCP 知识服务
make mcp-test
make mcp-demo
```

## 核心原则

1. 原始资料不直接改写。
2. 一个主题只保留一篇 `canonical` 页面，其他页面链接到它。
3. 结论必须能回到来源文档及其章节。
4. 教程、操作指南、解释和参考资料分开组织。
5. 模型、框架、价格、API 等易变信息必须标注验证日期。

Git 跟踪公开 Markdown、脚本和规则；原始 Word、私有来源全文、来源图片和本地索引属于可重建材料，不进入普通 Git 历史。

代码、自动化和 MCP 实现使用 [MIT License](LICENSE-CODE)；知识内容与上游材料的权利边界见
[CONTENT-NOTICE](CONTENT-NOTICE.md)。
