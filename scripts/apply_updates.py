#!/usr/bin/env python3
"""增量导入来源，并报告受影响的 canonical / evergreen 页面。"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date

from kb_common import ROOT, knowledge_files, parse_frontmatter, write_json


STATE_PATH = ROOT / ".cache" / "source-state.json"
REPORT_PATH = ROOT / "meta" / "update-report.md"


def read_manifests() -> dict:
    manifests = {}
    for path in sorted((ROOT / "sources" / "imported").glob("*/manifest.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        manifests[data["source_id"]] = data
    return manifests


def section_map(manifest: dict) -> dict[str, dict]:
    return {section["title"]: section for section in manifest.get("sections", [])}


def compare(before: dict, after: dict) -> list[dict]:
    changes = []
    for source_id in sorted(set(before) | set(after)):
        old_sections = section_map(before.get(source_id, {}))
        new_sections = section_map(after.get(source_id, {}))
        for title in sorted(set(old_sections) | set(new_sections)):
            if title not in old_sections:
                kind = "added"
            elif title not in new_sections:
                kind = "removed"
            elif old_sections[title].get("sha256") != new_sections[title].get("sha256"):
                kind = "changed"
            else:
                continue
            changes.append({"source_id": source_id, "section": title, "kind": kind})
    return changes


def impacted_pages(changes: list[dict]) -> list[dict]:
    impacted = []
    for path in knowledge_files():
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        refs = meta.get("sources", [])
        if isinstance(refs, str):
            refs = [refs]
        matches = []
        for change in changes:
            prefix = f"{change['source_id']}#"
            for ref in refs:
                if not ref.startswith(prefix):
                    continue
                section = ref.split("#", 1)[1]
                changed_section = change["section"]
                if changed_section.startswith(section) or section.startswith(changed_section):
                    matches.append(f"{change['source_id']}#{changed_section}")
        if matches:
            impacted.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "title": meta.get("title", path.stem),
                    "matches": sorted(set(matches)),
                }
            )
    return impacted


def main() -> None:
    before = (
        json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if STATE_PATH.exists()
        else read_manifests()
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "import_docx.py")], check=True
    )
    after = read_manifests()
    changes = compare(before, after)
    impacted = impacted_pages(changes)

    lines = [
        "# 来源增量影响报告",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
    ]
    if not changes:
        lines.append("没有检测到来源章节变化。")
    else:
        lines.extend(["## 来源变化", ""])
        for change in changes:
            lines.append(
                f"- `{change['kind']}` `{change['source_id']}#{change['section']}`"
            )
        lines.extend(["", "## 需要复核的知识页", ""])
        if impacted:
            for page in impacted:
                refs = "、".join(f"`{ref}`" for ref in page["matches"])
                lines.append(f"- [{page['title']}](../{page['path']})：{refs}")
        else:
            lines.append("- 没有现有页面引用这些变化；需要判断是否创建新页面。")
    lines.extend(
        [
            "",
            "> 本命令不会自动改写 canonical 页面。Agent 应阅读变化、更新受影响页面、",
            "> 修改 `last_verified`，再执行 `make verify_wiki`。",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    write_json(STATE_PATH, after)
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_indexes.py")], check=True
    )
    print(
        f"OK: {len(changes)} source change(s), {len(impacted)} impacted page(s)"
    )
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

