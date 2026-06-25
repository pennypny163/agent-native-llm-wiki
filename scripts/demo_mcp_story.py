#!/usr/bin/env python3
"""Render the portfolio demo story with real knowledge operations."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp_server"))

from knowledge import list_stale_pages, search_knowledge, trace_sources  # noqa: E402


def main() -> None:
    query = "RAG 为什么失败？"
    search = search_knowledge(query, limit=3)
    top = search["results"][0]
    sources = trace_sources(top["slug"], max_chars=500)
    stale = list_stale_pages(as_of="2026-08-01", domain="rag", limit=3)

    print(f"用户问题：{query}")
    print(f"1. 搜索 canonical：{top['title']} ({top['path']})")
    print(f"2. 回溯来源：{', '.join(item['reference'] for item in sources['sources'])}")
    print("3. 综合回答：RAG 的错误常在来源、解析、召回和排序阶段已经形成；")
    print("   更强的生成模型往往只能把缺失证据包装得更流畅。")
    if stale["pages"]:
        page = stale["pages"][0]
        print(
            f"4. 时效检查：截至 {stale['as_of']}，{page['title']} "
            f"已超复核周期 {page['overdue_days']} 天。"
        )
        print(f"5. 更新建议：{page['suggestion']}")


if __name__ == "__main__":
    main()

