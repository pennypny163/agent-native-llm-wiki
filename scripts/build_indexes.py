#!/usr/bin/env python3
"""为纯 Markdown 知识库构建本地检索索引和链接图。"""

from __future__ import annotations

import re

from kb_common import (
    ROOT,
    body_without_frontmatter,
    internal_links,
    knowledge_files,
    parse_frontmatter,
    write_json,
)


def normalize_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"[#>*_`|[\]()]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def index_files():
    files = list(knowledge_files())
    files.extend(sorted((ROOT / "sources" / "imported").glob("*/*.md")))
    return sorted(set(files))


def main() -> None:
    records = []
    graph: dict[str, list[str]] = {}
    backlinks: dict[str, list[str]] = {}

    knowledge_set = set(knowledge_files())
    for path in index_files():
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        relative = path.relative_to(ROOT).as_posix()
        first_heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        layer = "knowledge" if path in knowledge_set else "source"
        links = []
        for resolved in internal_links(path, text):
            try:
                target = resolved.relative_to(ROOT).as_posix()
            except ValueError:
                continue
            if resolved.exists() and resolved.suffix == ".md":
                links.append(target)
                backlinks.setdefault(target, []).append(relative)
        graph[relative] = sorted(set(links))
        records.append(
            {
                "path": relative,
                "slug": path.stem,
                "title": meta.get(
                    "title", first_heading.group(1) if first_heading else path.stem
                ),
                "aliases": meta.get("aliases", []),
                "type": meta.get("type", "source"),
                "domain": meta.get("domain", "source"),
                "status": meta.get("status", "generated"),
                "freshness": meta.get("freshness", ""),
                "layer": layer,
                "body": normalize_text(body_without_frontmatter(text)),
            }
        )

    write_json(ROOT / ".cache" / "search-index.json", records)
    write_json(
        ROOT / ".cache" / "link-graph.json",
        {"outgoing": graph, "backlinks": backlinks},
    )
    print(f"OK: indexed {len(records)} Markdown pages")


if __name__ == "__main__":
    main()
