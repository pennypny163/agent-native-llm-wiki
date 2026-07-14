#!/usr/bin/env python3
"""知识库脚本共享函数。只依赖 Python 标准库。"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIRS = (
    "concepts",
    "evergreen",
    "explanations",
    "how-to",
    "reference",
    "learning-paths",
    "maps",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return "" if end < 0 else text[4:end]


def parse_scalar(value: str):
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("'\"") for part in inner.split(",")]
    return value.strip("'\"")


def parse_frontmatter(text: str) -> dict:
    block = frontmatter_block(text)
    result: dict = {}
    current: str | None = None
    for line in block.splitlines():
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match:
            current = match.group(1)
            result[current] = parse_scalar(match.group(2))
            continue
        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item and current:
            if not isinstance(result.get(current), list):
                result[current] = []
            result[current].append(item.group(1).strip("'\""))
    return result


def body_without_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    return text if end < 0 else text[end + 5 :]


def knowledge_files() -> list[Path]:
    files: list[Path] = []
    for directory in KNOWLEDGE_DIRS:
        root = ROOT / directory
        if root.exists():
            files.extend(root.glob("*.md"))
    return sorted(files)


def internal_links(path: Path, text: str) -> list[Path]:
    links: list[Path] = []
    for target in LINK_RE.findall(text):
        target = target.strip()
        if "\n" in target or "\r" in target or len(target) > 240:
            continue
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if target:
            links.append((path.parent / target).resolve())
    return links


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
