PYTHON := /Users/panningyi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3

.PHONY: import check build_wiki apply_updates verify_wiki index search docs-prepare docs-serve docs-build

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

docs-serve: docs-prepare
	mkdocs serve

docs-build: docs-prepare
	mkdocs build --strict
