#!/usr/bin/env python3
"""Deterministic smoke tests for the MCP knowledge functions."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp_server"))

from knowledge import (  # noqa: E402
    find_related_topics,
    list_stale_pages,
    read_canonical_page,
    search_knowledge,
    trace_sources,
)


def main() -> None:
    search = search_knowledge("RAG 为什么失败", limit=5)
    assert search["results"], search
    assert search["results"][0]["slug"] in {
        "rag-fails-before-generation",
        "rag-failure-modes",
    }

    page = read_canonical_page("rag-fails-before-generation")
    assert "生成之前" in page["title"]

    sources = trace_sources("rag-fails-before-generation", max_chars=600)
    assert sources["source_count"] >= 1
    assert sources["sources"][0]["path"]

    related = find_related_topics("rag-fails-before-generation")
    assert related["related"]

    stale = list_stale_pages(as_of="2026-08-01", domain="rag")
    assert stale["pages"], stale

    print(
        json.dumps(
            {
                "search_top": search["results"][0]["slug"],
                "source_count": sources["source_count"],
                "related_count": related["count"],
                "stale_count_on_2026-08-01": stale["count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

