#!/usr/bin/env python3
"""Karpathy-style Wiki 验证：结构、来源、重复、代码、时效和孤页。"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime

from kb_common import (
    ROOT,
    body_without_frontmatter,
    internal_links,
    knowledge_files,
    parse_frontmatter,
)


FRESHNESS_DAYS = {"high": 30, "medium": 120, "low": 365}
DIR_TYPES = {
    "concepts": {"concept"},
    "evergreen": {"evergreen"},
    "explanations": {"explanation"},
    "how-to": {"how-to"},
    "reference": {"reference"},
    "learning-paths": {"learning-path", "tutorial"},
    "maps": {"map"},
}


def main() -> None:
    base = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_kb.py")],
        text=True,
        capture_output=True,
    )
    if base.returncode:
        print(base.stdout + base.stderr)
        raise SystemExit(base.returncode)

    warnings: list[str] = []
    errors: list[str] = []
    titles: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, int] = defaultdict(int)
    blocks: dict[str, list[str]] = defaultdict(list)
    files = knowledge_files()

    for path in files:
        text = path.read_text(encoding="utf-8")
        body = body_without_frontmatter(text)
        meta = parse_frontmatter(text)
        relative = path.relative_to(ROOT).as_posix()
        title = str(meta.get("title", path.stem))
        titles[title.lower()].append(relative)

        if meta.get("type") not in DIR_TYPES.get(path.parent.name, set()):
            errors.append(
                f"{relative}: type={meta.get('type')} 与目录 {path.parent.name} 不匹配"
            )

        if path.parent.name == "evergreen":
            for field in ("maturity", "claim", "review_triggers"):
                if field not in meta:
                    errors.append(f"{relative}: Evergreen 缺少 {field}")

        last_verified = meta.get("last_verified")
        freshness = meta.get("freshness")
        if last_verified and freshness in FRESHNESS_DAYS:
            try:
                age = (date.today() - datetime.strptime(
                    str(last_verified), "%Y-%m-%d"
                ).date()).days
                if age > FRESHNESS_DAYS[freshness]:
                    warnings.append(
                        f"{relative}: 已超过 {freshness} 复核周期（{age} 天）"
                    )
            except ValueError:
                errors.append(f"{relative}: last_verified 日期格式错误")

        if body.count("```") % 2:
            errors.append(f"{relative}: 代码围栏未闭合")

        for resolved in internal_links(path, text):
            try:
                target = resolved.relative_to(ROOT).as_posix()
            except ValueError:
                continue
            incoming[target] += 1

        for paragraph in re.split(r"\n\s*\n", body):
            normalized = re.sub(r"\s+", " ", paragraph).strip().lower()
            if len(normalized) >= 180 and not normalized.startswith(
                ("```", "|", "#")
            ):
                blocks[normalized].append(relative)

    for title, paths in titles.items():
        if len(paths) > 1:
            errors.append(f"重复标题 {title}: {', '.join(paths)}")
    for _, paths in blocks.items():
        unique = sorted(set(paths))
        if len(unique) > 1:
            warnings.append(f"疑似重复长段落: {', '.join(unique)}")
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if (
            meta.get("status") == "canonical"
            and path.parent.name not in {"maps"}
            and incoming[relative] == 0
        ):
            warnings.append(f"{relative}: canonical 页面没有内部入链")

    if errors:
        print("\n".join(f"ERROR {item}" for item in errors))
    if warnings:
        print("\n".join(f"WARN  {item}" for item in warnings))
    print(
        f"VERIFY: {len(files)} knowledge pages, "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

