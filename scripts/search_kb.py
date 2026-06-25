#!/usr/bin/env python3
"""按标题/别名、全文、链接图顺序搜索知识库。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

from kb_common import ROOT


def tokens(query: str) -> list[str]:
    latin = re.findall(r"[a-zA-Z0-9_.+-]+", query.lower())
    chinese = re.findall(r"[\u4e00-\u9fff]+", query)
    units = latin + chinese
    units.extend(char for group in chinese for char in group if len(group) > 1)
    return list(dict.fromkeys(units))


def occurrences(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term.lower()) for term in terms)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    query = " ".join(args.query)

    index_path = ROOT / ".cache" / "search-index.json"
    graph_path = ROOT / ".cache" / "link-graph.json"
    if not index_path.exists() or not graph_path.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_indexes.py")], check=True
        )
    records = json.loads(index_path.read_text(encoding="utf-8"))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    terms = tokens(query)

    scored = []
    for record in records:
        name_text = " ".join(
            [record["path"], record["title"], *record.get("aliases", [])]
        )
        name_score = occurrences(name_text, terms)
        body_score = occurrences(record["body"], terms)
        if not name_score and not body_score:
            continue
        layer_boost = 20 if record.get("layer") == "knowledge" else 0
        score = name_score * 100 + min(body_score, 30) + layer_boost
        scored.append([score, name_score, body_score, record])

    scored.sort(key=lambda item: (-item[0], item[3]["path"]))
    top_paths = {item[3]["path"] for item in scored[: args.limit]}
    for item in scored:
        path = item[3]["path"]
        neighbors = graph["outgoing"].get(path, [])
        backlinks = graph["backlinks"].get(path, [])
        link_score = sum(1 for neighbor in neighbors + backlinks if neighbor in top_paths)
        item[0] += link_score * 5
    scored.sort(key=lambda item: (-item[0], item[3]["path"]))

    print(f'Query: "{query}"')
    print("Order: title/alias → full text → link graph")
    for rank, (_, name_score, body_score, record) in enumerate(
        scored[: args.limit], start=1
    ):
        links = len(graph["outgoing"].get(record["path"], []))
        backs = len(graph["backlinks"].get(record["path"], []))
        print(
            f"{rank:>2}. {record['title']} "
            f"[{record.get('layer', 'knowledge')}:{record['type']}/{record['status']}]\n"
            f"    {record['path']} | name={name_score} text={body_score} "
            f"links={links} backlinks={backs}"
        )
    if not scored:
        print("No results.")


if __name__ == "__main__":
    main()
