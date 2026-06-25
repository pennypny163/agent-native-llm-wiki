"""Read-only knowledge operations shared by the MCP tools and tests."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
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
FRESHNESS_DAYS = {"high": 30, "medium": 120, "low": 365}
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")


def _frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    return "" if end < 0 else text[4:end]


def _parse_scalar(value: str):
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return (
            []
            if not inner
            else [part.strip().strip("'\"") for part in inner.split(",")]
        )
    return value.strip("'\"")


def parse_frontmatter(text: str) -> dict:
    result: dict = {}
    current: str | None = None
    for line in _frontmatter_block(text).splitlines():
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match:
            current = match.group(1)
            result[current] = _parse_scalar(match.group(2))
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
    return sorted(
        path
        for directory in KNOWLEDGE_DIRS
        for path in (ROOT / directory).glob("*.md")
    )


def page_records() -> list[dict]:
    records = []
    for path in knowledge_files():
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "slug": path.stem,
                "title": metadata.get("title", path.stem),
                "aliases": metadata.get("aliases", []),
                "type": metadata.get("type", ""),
                "domain": metadata.get("domain", ""),
                "status": metadata.get("status", ""),
                "freshness": metadata.get("freshness", ""),
                "last_verified": metadata.get("last_verified", ""),
                "metadata": metadata,
                "body": body_without_frontmatter(text).strip(),
            }
        )
    return records


def _query_terms(query: str) -> list[str]:
    latin = re.findall(r"[a-zA-Z0-9_.+-]+", query.lower())
    chinese = re.findall(r"[\u4e00-\u9fff]+", query)
    chinese_terms = []
    for group in chinese:
        chinese_terms.append(group)
        if len(group) > 2:
            chinese_terms.extend(group[index : index + 2] for index in range(len(group) - 1))
    return list(dict.fromkeys(latin + chinese_terms))


def _count(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term.lower()) for term in terms)


def search_knowledge(query: str, limit: int = 8, domain: str | None = None) -> dict:
    """Search canonical knowledge, prioritizing titles/aliases over full text."""
    terms = _query_terms(query)
    results = []
    for record in page_records():
        if domain and record["domain"] != domain:
            continue
        name_text = " ".join(
            [record["slug"], record["title"], *record.get("aliases", [])]
        )
        lowered_name = name_text.lower()
        name_score = sum(1 for term in terms if term.lower() in lowered_name)
        text_score = _count(record["body"], terms)
        if not name_score and not text_score:
            continue
        score = name_score * 100 + min(text_score, 30)
        snippet = re.sub(r"\s+", " ", record["body"])[:320]
        results.append(
            {
                "score": score,
                "slug": record["slug"],
                "title": record["title"],
                "path": record["path"],
                "type": record["type"],
                "domain": record["domain"],
                "freshness": record["freshness"],
                "last_verified": record["last_verified"],
                "snippet": snippet,
            }
        )
    results.sort(key=lambda item: (-item["score"], item["path"]))
    return {"query": query, "count": min(len(results), limit), "results": results[:limit]}


def _resolve_page(slug: str) -> dict:
    normalized = slug.removesuffix(".md").strip("/")
    for record in page_records():
        if normalized in {record["slug"], record["path"], record["title"]}:
            return record
    matches = search_knowledge(slug, limit=3)["results"]
    raise ValueError(
        f"Page not found: {slug}. Closest: "
        + ", ".join(item["slug"] for item in matches)
    )


def read_canonical_page(slug: str) -> dict:
    """Read one canonical page with metadata and Markdown body."""
    record = _resolve_page(slug)
    return {
        "slug": record["slug"],
        "title": record["title"],
        "path": record["path"],
        "metadata": record["metadata"],
        "content": record["body"],
    }


def _source_file(source_id: str) -> Path:
    path = ROOT / "sources" / "imported" / source_id
    if not path.is_dir():
        raise ValueError(f"Unknown source: {source_id}")
    return path


def _source_excerpt(source_id: str, section: str, max_chars: int) -> dict:
    candidates = sorted(_source_file(source_id).glob("*.md"))
    heading = re.compile(
        rf"^#+\s+{re.escape(section)}(?:[\s.、]|$).*?$", re.MULTILINE
    )
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        match = heading.search(text)
        if not match:
            continue
        start = match.start()
        next_heading = re.search(r"^#{1,3}\s+", text[match.end() :], re.MULTILINE)
        end = (
            match.end() + next_heading.start()
            if next_heading
            else min(len(text), start + max_chars)
        )
        excerpt = re.sub(r"\n{3,}", "\n\n", text[start:end]).strip()
        return {
            "reference": f"{source_id}#{section}",
            "path": path.relative_to(ROOT).as_posix(),
            "excerpt": excerpt[:max_chars],
        }
    return {
        "reference": f"{source_id}#{section}",
        "path": None,
        "excerpt": "Referenced section was not found in the imported source.",
    }


def trace_sources(slug: str, max_chars: int = 1800) -> dict:
    """Trace a canonical page to imported source sections with excerpts."""
    record = _resolve_page(slug)
    refs = record["metadata"].get("sources", [])
    refs = [refs] if isinstance(refs, str) else refs
    sources = []
    for ref in refs:
        source_id, separator, section = ref.partition("#")
        if not separator:
            continue
        sources.append(_source_excerpt(source_id, section, max_chars))
    return {
        "slug": record["slug"],
        "title": record["title"],
        "source_count": len(sources),
        "sources": sources,
    }


def _link_targets(record: dict) -> list[str]:
    path = ROOT / record["path"]
    targets = []
    for _, target in LINK_RE.findall(record["body"]):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        try:
            targets.append(resolved.relative_to(ROOT).as_posix())
        except ValueError:
            continue
    return targets


def find_related_topics(slug: str, limit: int = 12) -> dict:
    """Return metadata relations, outgoing links, and backlinks."""
    record = _resolve_page(slug)
    records = page_records()
    by_path = {item["path"]: item for item in records}
    outgoing = _link_targets(record)
    backlinks = [
        item["path"] for item in records if record["path"] in _link_targets(item)
    ]
    metadata_slugs = []
    for field in ("prerequisites", "related"):
        value = record["metadata"].get(field, [])
        metadata_slugs.extend([value] if isinstance(value, str) else value)

    seen: set[str] = set()
    related = []
    for candidate in metadata_slugs + outgoing + backlinks:
        matched = None
        for item in records:
            if candidate in {item["slug"], item["path"]}:
                matched = item
                break
        if not matched or matched["slug"] in seen or matched["slug"] == record["slug"]:
            continue
        seen.add(matched["slug"])
        related.append(
            {
                "slug": matched["slug"],
                "title": matched["title"],
                "path": matched["path"],
                "type": matched["type"],
                "domain": matched["domain"],
            }
        )
    return {
        "slug": record["slug"],
        "title": record["title"],
        "count": min(len(related), limit),
        "related": related[:limit],
    }


def list_stale_pages(
    as_of: str | None = None, domain: str | None = None, limit: int = 50
) -> dict:
    """List pages beyond their freshness review interval."""
    today = (
        datetime.strptime(as_of, "%Y-%m-%d").date() if as_of else date.today()
    )
    stale = []
    for record in page_records():
        if domain and record["domain"] != domain:
            continue
        freshness = record["freshness"]
        if freshness not in FRESHNESS_DAYS or not record["last_verified"]:
            continue
        verified = datetime.strptime(record["last_verified"], "%Y-%m-%d").date()
        age = (today - verified).days
        overdue = age - FRESHNESS_DAYS[freshness]
        if overdue <= 0:
            continue
        stale.append(
            {
                "slug": record["slug"],
                "title": record["title"],
                "path": record["path"],
                "domain": record["domain"],
                "freshness": freshness,
                "last_verified": record["last_verified"],
                "age_days": age,
                "overdue_days": overdue,
                "suggestion": "Re-check primary sources, update the page and last_verified, then run make verify_wiki.",
            }
        )
    stale.sort(key=lambda item: (-item["overdue_days"], item["path"]))
    return {"as_of": today.isoformat(), "count": min(len(stale), limit), "pages": stale[:limit]}
