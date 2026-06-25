#!/usr/bin/env python3
"""检查 Markdown 内部链接、元数据和来源引用。"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_META = {
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "meta" / "schema.md",
    ROOT / "meta" / "changelog.md",
    ROOT / "evidence" / "conflicts.md",
}
CONTENT_DIRS = {
    "maps",
    "learning-paths",
    "concepts",
    "evergreen",
    "explanations",
    "how-to",
    "reference",
}
REQUIRED = {
    "title",
    "aliases",
    "type",
    "domain",
    "status",
    "sources",
    "last_verified",
    "freshness",
    "confidence",
    "prerequisites",
    "related",
}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    return text[4:end]


def frontmatter(text: str) -> set[str]:
    block = frontmatter_block(text)
    keys = set()
    for line in block.splitlines():
        match = re.match(r"^([a-z_]+):", line)
        if match:
            keys.add(match.group(1))
    return keys


def source_refs(text: str) -> list[str]:
    block = frontmatter_block(text)
    lines = block.splitlines()
    refs: list[str] = []
    in_sources = False
    for line in lines:
        if line.startswith("sources:"):
            in_sources = True
            inline = line.split(":", 1)[1].strip()
            if inline not in {"", "[]"}:
                refs.append(inline.strip("'\""))
            continue
        if in_sources and re.match(r"^[a-z_]+:", line):
            break
        if in_sources:
            match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if match:
                refs.append(match.group(1).strip("'\""))
    return refs


def main() -> None:
    errors: list[str] = []
    files = []
    for filename in ("README.md", "AGENTS.md", "CONTRIBUTING.md", "CONTENT-NOTICE.md"):
        path = ROOT / filename
        if path.exists():
            files.append(path)
    for directory in (
        "concepts",
        "evergreen",
        "explanations",
        "how-to",
        "reference",
        "maps",
        "learning-paths",
        "meta",
        "evidence",
    ):
        files.extend((ROOT / directory).rglob("*.md"))
    files.extend((ROOT / "sources" / "imported").glob("*/index.md"))
    files = sorted(set(files))
    source_dirs = {
        path.name: path
        for path in (ROOT / "sources" / "imported").iterdir()
        if path.is_dir()
    }
    source_headings = {
        source_id: [
            heading
            for path in sorted(directory.glob("*.md"))
            for heading in re.findall(
                r"^#+\s+(.+?)\s*$",
                path.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        ]
        for source_id, directory in source_dirs.items()
    }
    for path in files:
        text = path.read_text(encoding="utf-8")
        if path.parent.name in CONTENT_DIRS and path not in SKIP_META:
            missing = REQUIRED - frontmatter(text)
            if missing:
                errors.append(f"{path.relative_to(ROOT)}: 缺少元数据 {sorted(missing)}")
            for ref in source_refs(text):
                source_id, separator, section = ref.partition("#")
                if source_id not in source_dirs:
                    errors.append(
                        f"{path.relative_to(ROOT)}: 未知来源 {source_id}"
                    )
                    continue
                if separator and section:
                    if not any(
                        heading == section
                        or heading.startswith((section + " ", section + ".", section + "、"))
                        for heading in source_headings[source_id]
                    ):
                        errors.append(
                            f"{path.relative_to(ROOT)}: 来源章节不存在 {ref}"
                        )

        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            if (
                "sources/imported" in path.as_posix()
                and target.startswith("assets/")
            ):
                # 来源图片是可由 DOCX 重建的本地二进制，不进入普通 Git 历史。
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: 无效链接 {target}"
                )

    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        print(f"\n{len(errors)} error(s)")
        sys.exit(1)
    print(f"OK: checked {len(files)} Markdown files")


if __name__ == "__main__":
    main()
