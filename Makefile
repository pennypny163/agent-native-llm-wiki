PYTHON := /Users/panningyi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
MKDOCS := $(shell if [ -x .venv-docs/bin/mkdocs ]; then echo .venv-docs/bin/mkdocs; else echo mkdocs; fi)

.PHONY: import check build_wiki apply_updates verify_wiki index search docs-install docs-prepare docs-serve docs-build mcp-install mcp-test mcp-demo

import:
	$(PYTHON) scripts/import_docx.py

check:
	$(PYTHON) scripts/check_kb.py

build_wiki:
	$(PYTHON) scripts/build_wiki.py

apply_updates:
	$(PYTHON) scripts/apply_updates.py

verify_wiki:
	$(PYTHON) scripts/verify_wiki.py

index:
	$(PYTHON) scripts/build_indexes.py

search:
	$(PYTHON) scripts/search_kb.py "$(Q)"

docs-prepare:
	$(PYTHON) scripts/prepare_mkdocs.py

docs-install:
	$(PYTHON) -m venv .venv-docs
	.venv-docs/bin/pip install -r requirements-docs.txt

docs-serve: docs-prepare
	$(MKDOCS) serve

docs-build: docs-prepare
	$(MKDOCS) build --strict

mcp-install:
	$(PYTHON) -m venv .venv-mcp
	.venv-mcp/bin/pip install -r requirements-mcp.txt

mcp-test:
	$(PYTHON) scripts/test_mcp_tools.py

mcp-demo:
	$(PYTHON) scripts/demo_mcp_story.py
