# MCP 知识服务

本项目提供只读 stdio MCP Server，让 Codex、Claude Desktop 等客户端调用 canonical 知识库。

## 工具

| 工具 | 用途 |
|---|---|
| `search_knowledge(query)` | 按标题、别名和正文检索 canonical 页面 |
| `read_canonical_page(slug)` | 读取页面元数据与 Markdown 正文 |
| `trace_sources(slug)` | 回溯到导入来源章节并返回摘录 |
| `find_related_topics(slug)` | 返回前置知识、相关页面、出链和反向链接 |
| `list_stale_pages()` | 根据 freshness 与 last_verified 查找待复核页面 |

MCP Server 不修改事实源。知识更新仍通过 Markdown、Git 和 `make verify_wiki` 完成。

## 安装

```bash
python3 -m venv .venv-mcp
source .venv-mcp/bin/activate
pip install -r requirements-mcp.txt
make mcp-test
```

## 接入 Codex

```bash
codex mcp add agent-native-llm-wiki -- \
  /absolute/path/to/wiki/.venv-mcp/bin/python \
  /absolute/path/to/wiki/mcp_server/server.py
```

检查：

```bash
codex mcp list
```

## 接入 Claude Desktop

在 Claude Desktop MCP 配置中加入：

```json
{
  "mcpServers": {
    "agent-native-llm-wiki": {
      "command": "/absolute/path/to/wiki/.venv-mcp/bin/python",
      "args": ["/absolute/path/to/wiki/mcp_server/server.py"]
    }
  }
}
```

## Demo

```bash
make mcp-demo
```

演示链路：

```text
用户询问 RAG 为什么失败
→ 搜索 canonical 页面
→ 回溯来源章节
→ 基于证据回答
→ 检查页面时效
→ 给出更新建议
```

