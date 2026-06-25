#!/usr/bin/env python3
"""完整构建：来源导入 → 本地索引 → 验证。"""

from __future__ import annotations

import subprocess
import sys

from kb_common import ROOT


def run(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / script)], check=True)


def main() -> None:
    run("import_docx.py")
    run("build_indexes.py")
    run("verify_wiki.py")
    print("BUILD COMPLETE")


if __name__ == "__main__":
    main()

