#!/usr/bin/env python3
"""
add_missing_permalinks.py

Scans Jekyll Markdown posts for missing `permalink` fields and can add them
safely.

Rules:
- Existing permalinks are never changed.
- Missing permalinks are generated as /{first-category}/{filename-slug}/.
- --dry-run never writes posts.
- --apply is blocked if there are invalid files, invalid generated permalinks,
  or duplicate permalinks.
- The report is generated from the current run, not from stale data.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)
FIELD_RE_TEMPLATE = r"^{field}[ \t]*:[ \t]*(.*)$"
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}-")
VALID_PERMALINK_RE = re.compile(r"^/[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*/$")


@dataclass
class PostResult:
    path: Path
    has_frontmatter: bool = False
    had_permalink: bool = False
    existing_permalink: Optional[str] = None
    generated_permalink: Optional[str] = None
    categories: list[str] | None = None
    slug: str = ""
    error: Optional[str] = None
    applied: bool = False
    apply_error: Optional[str] = None

    @property
    def effective_permalink(self) -> Optional[str]:
        return self.existing_permalink or self.generated_permalink


def split_frontmatter(text: str) -> tuple[Optional[str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return match.group(1), text[match.end():]


def parse_yaml_field(raw_yaml: str, field: str) -> Optional[str]:
    pattern = re.compile(
        FIELD_RE_TEMPLATE.format(field=re.escape(field)),
        re.MULTILINE,
    )
    match = pattern.search(raw_yaml)
    if not match:
        return None

    value = match.group(1).strip()
    if not value or value in {"null", "~"}:
        return None

    # Ignore block-style values here. They are handled separately for categories.
    if value == "":
        return None

    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]

    return value.strip()


def parse_categories(raw_yaml: str) -> list[str]:
    # Inline list:
    # categories: ["foo", "bar"]
    inline = re.search(r"^categories[ \t]*:[ \t]*\[([^\]]*)\]", raw_yaml, re.MULTILINE)
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
            categories: list[str] = []
            for next_line in lines[i + 1:]:
                stripped = next_line.strip()

                if not stripped:
                    continue

                if re.match(r"^[ \t]*-[ \t]+", next_line):
                    item = re.sub(r"^[ \t]*-[ \t]+", "", next_line).strip()
                    item = item.strip('"').strip("'")
                    if item:
                        categories.append(item)
                    continue

                break

            return categories

    # Scalar:
    # categories: foo
    scalar = parse_yaml_field(raw_yaml, "categories")
    if scalar and scalar not in {"[]", "null", "~"}:
        return [scalar]

    return []


def normalize_url_segment(value: str) -> str:
    """
    Convert text to a conservative URL segment:
    - lowercase
    - accents removed
    - non-alphanumeric groups converted to hyphens
    - no leading/trailing hyphens
    """
    value = value.strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def filename_slug(filename: str) -> str:
    name = filename

    # Handle accidental double extension such as .md.md
    while name.lower().endswith(".md"):
        name = name[:-3]

    name = DATE_PREFIX_RE.sub("", name)
    return normalize_url_segment(name)


def generate_permalink(cluster: str, slug: str) -> str:
    cluster_segment = normalize_url_segment(cluster)
    slug_segment = normalize_url_segment(slug)
    return f"/{cluster_segment}/{slug_segment}/"


def validate_permalink(permalink: str) -> bool:
    return bool(VALID_PERMALINK_RE.fullmatch(permalink))


def insert_permalink_into_frontmatter(raw_yaml: str, permalink: str) -> str:
    lines = raw_yaml.splitlines(keepends=True)
    insert_at = len(lines)

    for i, line in enumerate(lines):
        if re.match(r"^date[ \t]*:", line):
            insert_at = i + 1
            break

    # Ensure the line before the insertion point ends with a newline so the
    # permalink is not concatenated onto the previous content.
    if insert_at > 0 and lines and not lines[insert_at - 1].endswith("\n"):
        lines[insert_at - 1] += "\n"

    lines.insert(insert_at, f"permalink: {permalink}\n")
    return "".join(lines)


def rebuild_file(raw_yaml: str, body: str) -> str:
    if raw_yaml and not raw_yaml.endswith("\n"):
        raw_yaml += "\n"
    return f"---\n{raw_yaml}---\n{body}"


def scan_post(path: Path) -> PostResult:
    result = PostResult(path=path, categories=[])

    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        result.error = f"Cannot read file: {exc}"
        return result

    raw_yaml, _body = split_frontmatter(text)
    if raw_yaml is None:
        result.error = "No valid YAML front matter found"
        return result

    result.has_frontmatter = True

    existing_permalink = parse_yaml_field(raw_yaml, "permalink")
    if existing_permalink:
        result.had_permalink = True
        result.existing_permalink = existing_permalink
        if not validate_permalink(existing_permalink):
            result.error = f"Existing permalink '{existing_permalink}' is invalid"
        return result

    categories = parse_categories(raw_yaml)
    result.categories = categories

    if not categories:
        result.error = "No categories defined; cannot generate permalink"
        return result

    cluster = categories[0]
    if not cluster or not cluster.strip():
        result.error = "First category is empty; cannot generate permalink"
        return result

    slug = filename_slug(path.name)
    result.slug = slug
    if not slug:
        result.error = "Could not extract slug from filename"
        return result

    permalink = generate_permalink(cluster, slug)
    if not validate_permalink(permalink):
        result.error = f"Generated permalink '{permalink}' is invalid"
        return result

    result.generated_permalink = permalink
    return result


def scan_all(posts_dir: Path) -> list[PostResult]:
    return [scan_post(path) for path in sorted(posts_dir.rglob("*.md"))]


def find_duplicates(results: list[PostResult]) -> dict[str, list[Path]]:
    seen: dict[str, list[Path]] = {}

    for result in results:
        permalink = result.effective_permalink
        if permalink:
            seen.setdefault(permalink, []).append(result.path)

    return {permalink: paths for permalink, paths in seen.items() if len(paths) > 1}


def apply_permalink(result: PostResult) -> Optional[str]:
    if not result.generated_permalink:
        return "No generated permalink available"

    try:
        text = result.path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"Cannot read file during apply: {exc}"

    raw_yaml, body = split_frontmatter(text)
    if raw_yaml is None:
        return "No valid YAML front matter found during apply"

    # Safety: do not add a second permalink if the file changed after scan.
    if parse_yaml_field(raw_yaml, "permalink"):
        return "File already has permalink during apply; skipped to avoid duplicate field"

    new_yaml = insert_permalink_into_frontmatter(raw_yaml, result.generated_permalink)
    new_text = rebuild_file(new_yaml, body)

    try:
        result.path.write_text(new_text, encoding="utf-8")
    except Exception as exc:
        return f"Cannot write file: {exc}"

    return None


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def build_report(
    *,
    pre_results: list[PostResult],
    post_results: list[PostResult],
    dry_run: bool,
    posts_root: Path,
    duplicate_groups: dict[str, list[Path]],
    blocked: bool,
) -> str:
    """
    Build report from:
    - pre_results: scan before any writes (used for planned/error classification)
    - post_results: scan after writes (reflects real file state).
      In dry-run mode, post_results == pre_results.
    """
    mode_label = "DRY RUN" if dry_run else "APPLY"

    pre_needs = [r for r in pre_results if r.generated_permalink and not r.error]
    pre_already = [r for r in pre_results if r.had_permalink]
    pre_blocked_files = [r for r in pre_results if r.error]

    pre_needs_paths = {r.path for r in pre_needs}
    post_by_path = {r.path: r for r in post_results}

    if not dry_run:
        applied = [
            post_by_path[p] for p in pre_needs_paths
            if p in post_by_path and post_by_path[p].had_permalink
        ]
        write_errors = [
            pre for pre in pre_needs
            if pre.path not in post_by_path
            or not post_by_path[pre.path].had_permalink
        ]
    else:
        applied = []
        write_errors = []

    title = f"# Permalink Report ({mode_label})"

    def r_rel(path: Path) -> str:
        return rel(path, posts_root.parent)

    lines: list[str] = [
        title,
        "",
        f"- Post scansionati: **{len(post_results)}**",
        f"- Già con permalink: **{len(pre_already)}**",
        f"- Permalink pianificati: **{len(pre_needs)}**",
        f"- Permalink applicati: **{len(applied)}**",
        f"- File bloccati (errori individuali): **{len(pre_blocked_files)}**",
        f"- Errori di scrittura: **{len(write_errors)}**",
        f"- Apply bloccato (duplicati): **{'sì' if blocked else 'no'}**",
        f"- Gruppi di permalink duplicati: **{len(duplicate_groups)}**",
        "",
    ]

    # --- Permalink applicati ---
    lines += ["## Permalink applicati", ""]
    if applied:
        for r in applied:
            pre = next((p for p in pre_needs if p.path == r.path), None)
            permalink = pre.generated_permalink if pre else r.existing_permalink
            lines.append(f"- `{r_rel(r.path)}` → `{permalink}`")
    elif dry_run:
        lines.append("_Dry-run: nessun file modificato._")
    else:
        lines.append("_Nessun permalink applicato in questa esecuzione._")
    lines.append("")

    # --- Permalink pianificati ---
    lines += ["## Permalink pianificati", ""]
    if dry_run and pre_needs:
        for r in pre_needs:
            lines.append(f"- `{r_rel(r.path)}` → `{r.generated_permalink}`")
    elif not dry_run and pre_needs:
        lines.append("_Tutti i permalink pianificati sono stati tentati._")
        lines.append("_Vedi «Permalink applicati» e «Errori di scrittura» per il risultato._")
    else:
        lines.append("_Nessuna modifica pianificata._")
    lines.append("")

    # --- Articoli già con permalink ---
    lines += ["## Articoli già con permalink", ""]
    if pre_already:
        for r in pre_already:
            lines.append(f"- `{r_rel(r.path)}` → `{r.existing_permalink}`")
    else:
        lines.append("_Nessuno._")
    lines.append("")

    # --- File bloccati ---
    lines += ["## File bloccati", ""]
    if pre_blocked_files:
        for r in pre_blocked_files:
            lines.append(f"- `{r_rel(r.path)}`: {r.error}")
    else:
        lines.append("_Nessun file bloccato._")
    lines.append("")

    # --- Errori di scrittura ---
    lines += ["## Errori di scrittura", ""]
    if write_errors:
        for r in write_errors:
            lines.append(f"- `{r_rel(r.path)}` (permalink atteso: `{r.generated_permalink}`)")
    else:
        lines.append("_Nessun errore di scrittura._")
    lines.append("")

    # --- Permalink duplicati ---
    lines += ["## Permalink duplicati", ""]
    if duplicate_groups:
        for permalink, paths in sorted(duplicate_groups.items()):
            lines.append(f"### `{permalink}`")
            for path in paths:
                lines.append(f"- `{r_rel(path)}`")
            lines.append("")
    else:
        lines.append("_Nessun permalink duplicato._")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add missing explicit permalinks to Jekyll Markdown posts."
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Show changes without editing files.")
    mode.add_argument("--apply", action="store_true", help="Apply changes if validation passes.")

    parser.add_argument("--posts-dir", default="_posts", help="Posts directory. Default: _posts")
    parser.add_argument("--report", default="permalink-report.md", help="Markdown report path.")

    args = parser.parse_args()

    posts_dir = Path(args.posts_dir)
    report_path = Path(args.report)

    if not posts_dir.is_dir():
        print(f"ERROR: posts directory not found: {posts_dir}", file=sys.stderr)
        return 1

    # --- Initial scan ---
    print(f"Scanning {posts_dir} …")
    pre_results = scan_all(posts_dir)

    needs_permalink = [r for r in pre_results if r.generated_permalink and not r.error]
    already_done = [r for r in pre_results if r.had_permalink]
    file_errors = [r for r in pre_results if r.error]
    duplicate_groups = find_duplicates(pre_results)

    # Only duplicate generated permalinks block apply.
    # Individual file errors (no categories, no front matter) skip that file only.
    blocked = bool(duplicate_groups)

    print(f"  Total posts:                  {len(pre_results)}")
    print(f"  Already have permalink:       {len(already_done)}")
    print(f"  Missing permalink (candidates):{len(needs_permalink)}")
    print(f"  Files with errors (skipped):  {len(file_errors)}")
    print(f"  Duplicate permalink groups:   {len(duplicate_groups)}")
    print()

    if needs_permalink:
        print("Planned changes:")
        for r in needs_permalink:
            print(f"  {r.path}  →  {r.generated_permalink}")
        print()

    if file_errors:
        print("Files skipped (individual errors — apply not blocked by these):")
        for r in file_errors:
            print(f"  [SKIP] {r.path}: {r.error}")
        print()

    if duplicate_groups:
        print("Duplicate permalink conflicts (BLOCKING apply):")
        for permalink, paths in sorted(duplicate_groups.items()):
            print(f"  {permalink}")
            for p in paths:
                print(f"    {p}")
        print()

    # --- Apply ---
    post_results = pre_results  # dry-run: report from pre-scan

    if args.apply:
        if blocked:
            print(
                "BLOCKED: --apply is disabled because duplicate generated permalinks were found.\n"
                "Resolve the conflicts listed above, then re-run.",
                file=sys.stderr,
            )
        else:
            print("Applying changes …")
            for r in needs_permalink:
                err = apply_permalink(r)
                if err:
                    r.apply_error = err
                    print(f"  [FAILED] {r.path}: {err}")
                else:
                    r.applied = True
                    print(f"  [OK]     {r.path}  →  {r.generated_permalink}")
            print()

            n_ok = sum(1 for r in needs_permalink if r.applied)
            n_fail = sum(1 for r in needs_permalink if r.apply_error)
            print(f"Done. {n_ok} written, {n_fail} failed.")
            print()

            # Re-scan to build the report from real file state
            print(f"Re-scanning {posts_dir} to verify …")
            post_results = scan_all(posts_dir)
            n_post_permalink = sum(1 for r in post_results if r.had_permalink)
            print(f"  Posts with permalink after apply: {n_post_permalink}")
            print()

    report_text = build_report(
        pre_results=pre_results,
        post_results=post_results,
        dry_run=args.dry_run,
        posts_root=posts_dir,
        duplicate_groups=duplicate_groups,
        blocked=blocked,
    )
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Report written to: {report_path}")

    if args.apply and blocked:
        return 2

    if any(r.apply_error for r in pre_results):
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())