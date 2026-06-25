#!/usr/bin/env python3
"""生成公开 Wiki 的发布视图，不修改事实源 Markdown。"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from kb_common import ROOT


OUT = ROOT / ".cache" / "public-docs"
CONTENT_DIRS = (
    "concepts",
    "evergreen",
    "explanations",
    "how-to",
    "reference",
    "maps",
    "learning-paths",
)
SOURCE_LINK = re.compile(
    r"\[([^\]]+)\]\((?:\.\./)*sources/imported/[^)]+\)"
)


def public_text(text: str) -> str:
    return SOURCE_LINK.sub(r"\1（来源档案保留在本地知识库）", text)


def copy_markdown(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        public_text(source.read_text(encoding="utf-8")), encoding="utf-8"
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    copy_markdown(ROOT / "public" / "index.md", OUT / "index.md")
    copy_markdown(ROOT / "public" / "about.md", OUT / "about.md")

    for directory in CONTENT_DIRS:
        for source in sorted((ROOT / directory).glob("*.md")):
            copy_markdown(source, OUT / directory / source.name)

    # 使用专门的公开 Evergreen 索引覆盖目录中不存在的 index。
    copy_markdown(
        ROOT / "public" / "evergreen-index.md", OUT / "evergreen" / "index.md"
    )
    shutil.copytree(
        ROOT / "public" / "stylesheets",
        OUT / "stylesheets",
        dirs_exist_ok=True,
    )
    print(f"OK: prepared public docs at {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

