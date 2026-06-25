#!/usr/bin/env python3
"""stdio MCP server for the Agent-Native LLM Wiki."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from knowledge import (
    find_related_topics,
    list_stale_pages,
    read_canonical_page,
    search_knowledge,
    trace_sources,
)


mcp = FastMCP(
    "agent-native-llm-wiki",
    instructions=(
        "Read-only access to a traceable LLM, RAG and Agent knowledge base. "
        "Prefer canonical pages, trace claims to imported sources, and flag stale pages."
    ),
)

mcp.tool()(search_knowledge)
mcp.tool()(read_canonical_page)
mcp.tool()(trace_sources)
mcp.tool()(find_related_topics)
mcp.tool()(list_stale_pages)


if __name__ == "__main__":
    mcp.run(transport="stdio")

