#!/usr/bin/env python3
"""
generate_content_index.py

Scans Jekyll Markdown posts in _posts/, extracts metadata, and writes
_data/content-index.yaml for use by AI agents, internal linking tools,
and sitemap checks.

This script never modifies Markdown posts.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)
FIELD_RE_TEMPLATE = r"^{field}[ \t]*:[ \t]*(.*)$"
VALID_PERMALINK_RE = re.compile(
    r"^/[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*/$"
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class PostEntry:
    """Successfully indexed post."""
    source: str
    title: str
    permalink: str
    cluster: str
    subcluster: Optional[str]


@dataclass
class SkippedPost:
    """Post excluded from the index, with reason."""
    source: str
    reasons: list[str] = field(default_factory=list)


@dataclass
class WarnPost:
    """Post included in the index but with non-blocking warnings."""
    source: str
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Front matter parsing  (intentionally self-contained — no shared import)
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[Optional[str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return match.group(1), text[match.end():]


def _parse_scalar(raw_yaml: str, field_name: str) -> Optional[str]:
    pattern = re.compile(
        FIELD_RE_TEMPLATE.format(field=re.escape(field_name)),
        re.MULTILINE,
    )
    match = pattern.search(raw_yaml)
    if not match:
        return None
    value = match.group(1).strip()
    if not value or value in {"null", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]
    return value.strip() or None


def _parse_categories(raw_yaml: str) -> list[str]:
    # Inline list: categories: ["foo", "bar"]
    inline = re.search(
        r"^categories[ \t]*:[ \t]*\[([^\]]*)\]", raw_yaml, re.MULTILINE
    )
    if inline:
        return [
            item.strip().strip('"').strip("'")
            for item in inline.group(1).split(",")
            if item.strip().strip('"').strip("'")
        ]

    lines = raw_yaml.splitlines()

    # Block list:
    # categories:
    #   - foo
    for i, line in enumerate(lines):
        if re.match(r"^categories[ \t]*:[ \t]*$", line):
            cats: list[str] = []
            for next_line in lines[i + 1:]:
                if not next_line.strip():
                    continue
                if re.match(r"^[ \t]*-[ \t]+", next_line):
                    item = re.sub(r"^[ \t]*-[ \t]+", "", next_line).strip()
                    item = item.strip('"').strip("'")
                    if item:
                        cats.append(item)
                    continue
                break
            return cats

    # Scalar: categories: foo
    scalar = _parse_scalar(raw_yaml, "categories")
    if scalar and scalar not in {"[]", "null", "~"}:
        return [scalar]

    return []


def _parse_subcluster(raw_yaml: str) -> Optional[str]:
    """Try 'subcluster' then 'subclusters' (first item if list)."""
    value = _parse_scalar(raw_yaml, "subcluster")
    if value:
        return value

    # Try plural form
    value = _parse_scalar(raw_yaml, "subclusters")
    if value:
        return value

    # Block list: subclusters: \n  - foo
    lines = raw_yaml.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^subclusters[ \t]*:[ \t]*$", line):
            for next_line in lines[i + 1:]:
                if not next_line.strip():
                    continue
                if re.match(r"^[ \t]*-[ \t]+", next_line):
                    item = re.sub(r"^[ \t]*-[ \t]+", "", next_line).strip()
                    return item.strip('"').strip("'") or None
                break

    return None


def _yaml_escape(value: str) -> str:
    """
    Return a YAML-safe scalar.
    Wraps in double quotes if the value contains special characters or
    starts/ends with whitespace.  Escapes embedded double-quotes and backslashes.
    """
    needs_quoting = (
        not value
        or value != value.strip()
        or any(ch in value for ch in ':#{}[]|>&*!,\'"\\')
        or value[0] in "-?@`"
    )
    if needs_quoting:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def _infer_subcluster_from_path(path: Path, posts_dir: Path) -> Optional[str]:
    """
    Fall back to folder-based subcluster inference.
    Looks at the path component immediately below the first-level cluster folder.
    e.g. _posts/burnout-e-lavoro/autenticita-in-ufficio/cornerstone/file.md
                                  ^--- this becomes the subcluster
    """
    try:
        rel = path.relative_to(posts_dir)
    except ValueError:
        return None
    parts = rel.parts
    # parts[0] = cluster folder, parts[1] = subcluster folder (if depth >= 3)
    if len(parts) >= 3:
        return parts[1]
    return None


def scan_post(path: Path, posts_dir: Path) -> tuple[
    Optional[PostEntry], Optional[SkippedPost], Optional[WarnPost]
]:
    """
    Returns (entry, skipped, warn). Exactly one of entry/skipped is non-None;
    warn may accompany a valid entry.
    """
    rel_source = str(path.relative_to(posts_dir.parent))
    reasons: list[str] = []
    warnings: list[str] = []

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return None, SkippedPost(source=rel_source, reasons=[f"Cannot read file: {exc}"]), None

    raw_yaml, _body = split_frontmatter(text)
    if raw_yaml is None:
        return None, SkippedPost(source=rel_source, reasons=["No valid YAML front matter"]), None

    title = _parse_scalar(raw_yaml, "title")
    if not title:
        reasons.append("title is missing")

    permalink = _parse_scalar(raw_yaml, "permalink")
    if not permalink:
        reasons.append("permalink is missing")
    elif not VALID_PERMALINK_RE.fullmatch(permalink):
        reasons.append(f"permalink '{permalink}' is invalid")
        permalink = None

    categories = _parse_categories(raw_yaml)
    if not categories:
        reasons.append("categories is missing")
        cluster = None
    else:
        cluster = categories[0].strip() or None
        if not cluster:
            reasons.append("first category is empty")

    if reasons:
        return None, SkippedPost(source=rel_source, reasons=reasons), None

    # title, permalink, cluster are all valid at this point
    subcluster = _parse_subcluster(raw_yaml)
    if not subcluster:
        subcluster = _infer_subcluster_from_path(path, posts_dir)
        if subcluster:
            warnings.append(f"subcluster inferred from folder path: '{subcluster}'")
        else:
            warnings.append("subcluster missing and could not be inferred")

    entry = PostEntry(
        source=rel_source,
        title=title,         # type: ignore[arg-type]  # checked above
        permalink=permalink,  # type: ignore[arg-type]
        cluster=cluster,      # type: ignore[arg-type]
        subcluster=subcluster,
    )
    warn = WarnPost(source=rel_source, warnings=warnings) if warnings else None
    return entry, None, warn


def scan_all(posts_dir: Path) -> tuple[
    list[PostEntry], list[SkippedPost], list[WarnPost]
]:
    entries: list[PostEntry] = []
    skipped: list[SkippedPost] = []
    warnings: list[WarnPost] = []

    for path in sorted(posts_dir.rglob("*.md")):
        entry, skip, warn = scan_post(path, posts_dir)
        if entry:
            entries.append(entry)
        if skip:
            skipped.append(skip)
        if warn:
            warnings.append(warn)

    return entries, skipped, warnings


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def find_duplicate_permalinks(entries: list[PostEntry]) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for e in entries:
        seen.setdefault(e.permalink, []).append(e.source)
    return {k: v for k, v in seen.items() if len(v) > 1}


# ---------------------------------------------------------------------------
# YAML output
# ---------------------------------------------------------------------------

def build_yaml(entries: list[PostEntry]) -> str:
    lines: list[str] = [
        "# MessyMind content index",
        "# Generated by scripts/generate_content_index.py",
        "# Do not edit manually.",
        "",
        "posts:",
        "",
    ]
    for e in entries:
        lines.append(f"  - title: {_yaml_escape(e.title)}")
        lines.append(f"    permalink: {_yaml_escape(e.permalink)}")
        lines.append(f"    cluster: {_yaml_escape(e.cluster)}")
        if e.subcluster:
            lines.append(f"    subcluster: {_yaml_escape(e.subcluster)}")
        else:
            lines.append(f"    subcluster: ~")
        lines.append(f"    source: {_yaml_escape(e.source)}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(
    entries: list[PostEntry],
    skipped: list[SkippedPost],
    warnings: list[WarnPost],
    duplicates: dict[str, list[str]],
    output_path: Path,
) -> str:
    n_total = len(entries) + len(skipped)
    missing_meta = [w for w in warnings if any("missing" in s for s in w.warnings)]

    lines: list[str] = [
        "# Content Index Report",
        "",
        f"- Post scansionati: **{n_total}**",
        f"- Post indicizzati: **{len(entries)}**",
        f"- Post saltati: **{len(skipped)}**",
        f"- Post con warning: **{len(warnings)}**",
        f"- Permalink duplicati: **{len(duplicates)}**",
        f"- File di output: `{output_path}`",
        "",
    ]

    # --- Indexed posts ---
    lines += ["## Post indicizzati", ""]
    if entries:
        for e in entries:
            lines.append(f"- `{e.source}` → `{e.permalink}`")
    else:
        lines.append("_Nessun post indicizzato._")
    lines.append("")

    # --- Skipped posts ---
    lines += ["## Post saltati", ""]
    if skipped:
        for s in skipped:
            reasons_str = "; ".join(s.reasons)
            lines.append(f"- `{s.source}`: {reasons_str}")
    else:
        lines.append("_Nessun post saltato._")
    lines.append("")

    # --- Warnings ---
    lines += ["## Warning", ""]
    if warnings:
        for w in warnings:
            for msg in w.warnings:
                lines.append(f"- `{w.source}`: {msg}")
    else:
        lines.append("_Nessun warning._")
    lines.append("")

    # --- Duplicate permalinks ---
    lines += ["## Permalink duplicati", ""]
    if duplicates:
        for permalink, sources in sorted(duplicates.items()):
            lines.append(f"### `{permalink}`")
            for src in sources:
                lines.append(f"- `{src}`")
            lines.append("")
    else:
        lines.append("_Nessun permalink duplicato._")
    lines.append("")

    # --- Missing metadata ---
    lines += ["## Metadata mancanti", ""]
    if missing_meta:
        for w in missing_meta:
            missing_fields = [msg for msg in w.warnings if "missing" in msg]
            for msg in missing_fields:
                lines.append(f"- `{w.source}`: {msg}")
    else:
        lines.append("_Nessun metadata mancante nei post indicizzati._")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate _data/content-index.yaml from Jekyll _posts/."
    )
    parser.add_argument("--posts-dir", default="_posts", help="Posts directory. Default: _posts")
    parser.add_argument(
        "--output", default="_data/content-index.yaml",
        help="Output YAML file. Default: _data/content-index.yaml"
    )
    parser.add_argument(
        "--report", default="content-index-report.md",
        help="Markdown report path. Default: content-index-report.md"
    )
    args = parser.parse_args()

    posts_dir = Path(args.posts_dir)
    output_path = Path(args.output)
    report_path = Path(args.report)

    if not posts_dir.is_dir():
        print(f"ERROR: posts directory not found: {posts_dir}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Scan ---
    print(f"Scanning {posts_dir} …")
    entries, skipped, warnings = scan_all(posts_dir)
    duplicates = find_duplicate_permalinks(entries)

    print(f"  Total posts scanned: {len(entries) + len(skipped)}")
    print(f"  Indexed:             {len(entries)}")
    print(f"  Skipped:             {len(skipped)}")
    print(f"  With warnings:       {len(warnings)}")
    print(f"  Duplicate permalinks:{len(duplicates)}")
    print()

    if skipped:
        print("Skipped posts:")
        for s in skipped:
            print(f"  [SKIP] {s.source}: {'; '.join(s.reasons)}")
        print()

    if duplicates:
        print("Duplicate permalink conflicts:")
        for permalink, sources in sorted(duplicates.items()):
            print(f"  {permalink}")
            for src in sources:
                print(f"    {src}")
        print()

    # --- Write YAML ---
    yaml_text = build_yaml(entries)
    output_path.write_text(yaml_text, encoding="utf-8")
    print(f"Index written to:  {output_path}")

    # --- Write report ---
    report_text = build_report(entries, skipped, warnings, duplicates, output_path)
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Report written to: {report_path}")

    return 1 if duplicates else 0


if __name__ == "__main__":
    sys.exit(main())
