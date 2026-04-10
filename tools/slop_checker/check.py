"""Slop pattern checker — deterministic detection of AI prose tics.

Detects specific word-level and phrase-level patterns that indicate AI-generated
prose, with hard caps per chapter. Each pattern has a name, category, compiled
regex, and a per-chapter cap. The tool counts occurrences and reports violations.

Separate from skeleton_strip (which does psycholinguistic concreteness scoring).
This tool catches surface-level AI fingerprint patterns: filler actions, said
bookisms, filter words, hedging, breath tells, abstract-noun locomotion, etc.

Usage:
    python3 tools/slop_checker/check.py --json path/to/chapter.md
    python3 tools/slop_checker/check.py --summary path/to/chapter.md
    python3 tools/slop_checker/check.py --violations path/to/chapter.md
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Match:
    """A single pattern match in the text."""
    pattern_name: str
    category: str
    matched_text: str
    line_number: int
    context: str  # surrounding text snippet
    cap: int  # the effective per-chapter cap (after per-word scaling)


@dataclass
class PatternResult:
    """Aggregate result for one pattern."""
    name: str
    category: str
    cap: int
    count: int
    over_cap: bool
    matches: list[Match]


@dataclass
class CategoryResult:
    """Aggregate result for one category (may have combined caps)."""
    category: str
    combined_cap: int | None  # None if no combined cap
    combined_count: int
    over_combined_cap: bool
    patterns: list[PatternResult]


@dataclass
class CheckReport:
    """Full chapter check report."""
    total_words: int
    total_violations: int  # patterns over their cap
    total_matches: int
    categories: list[CategoryResult]


# ---------------------------------------------------------------------------
# Pattern definitions — loaded from per-category modules in patterns/
# ---------------------------------------------------------------------------

from tools.slop_checker.patterns import ALL_PATTERNS as _PATTERNS
from tools.slop_checker.patterns import COMBINED_CAPS as _COMBINED_CAPS


# ---------------------------------------------------------------------------
# Compile
# ---------------------------------------------------------------------------

_COMPILED = [
    {**p, "compiled": re.compile(p["regex"], re.IGNORECASE)}
    for p in _PATTERNS
]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _line_number(text: str, pos: int) -> int:
    """Return 1-based line number for a character position."""
    return text[:pos].count("\n") + 1


def _context_snippet(text: str, start: int, end: int, window: int = 40) -> str:
    """Extract a context snippet around a match."""
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    prefix = "..." if ctx_start > 0 else ""
    suffix = "..." if ctx_end < len(text) else ""
    snippet = text[ctx_start:ctx_end].replace("\n", " ")
    return f"{prefix}{snippet}{suffix}"


def check_prose(text: str) -> CheckReport:
    """Run all slop patterns against the text and return a structured report."""
    # Strip markdown header lines — they're metadata, not prose
    lines = text.split('\n')
    prose_lines = [l if not l.startswith('#') else '' for l in lines]
    prose_text = '\n'.join(prose_lines)

    total_words = len(prose_text.split())

    # Collect matches per pattern
    pattern_matches: dict[str, list[Match]] = defaultdict(list)

    for p in _COMPILED:
        # Compute effective cap: scale by word count if cap_per_words is set
        cap = p["cap"]
        cap_per_words = p.get("cap_per_words")
        if cap_per_words is not None and total_words > 0:
            cap = max(1, total_words // cap_per_words)

        for m in p["compiled"].finditer(prose_text):
            match = Match(
                pattern_name=p["name"],
                category=p["category"],
                matched_text=m.group(),
                line_number=_line_number(prose_text, m.start()),
                context=_context_snippet(prose_text, m.start(), m.end()),
                cap=cap,
            )
            pattern_matches[p["name"]].append(match)

    # Build per-pattern results
    pattern_results: dict[str, PatternResult] = {}
    for p in _COMPILED:
        matches = pattern_matches.get(p["name"], [])
        count = len(matches)
        # Recompute effective cap consistently
        cap = p["cap"]
        cap_per_words = p.get("cap_per_words")
        if cap_per_words is not None and total_words > 0:
            cap = max(1, total_words // cap_per_words)
        over = count > cap
        pattern_results[p["name"]] = PatternResult(
            name=p["name"],
            category=p["category"],
            cap=cap,
            count=count,
            over_cap=over,
            matches=matches,
        )

    # Group into categories
    cat_patterns: dict[str, list[PatternResult]] = defaultdict(list)
    for pr in pattern_results.values():
        cat_patterns[pr.category].append(pr)

    categories: list[CategoryResult] = []
    total_violations = 0

    for cat_name, prs in sorted(cat_patterns.items()):
        combined_cap = _COMBINED_CAPS.get(cat_name)
        combined_count = sum(pr.count for pr in prs)
        over_combined = combined_cap is not None and combined_count > combined_cap

        # Count violations: patterns over individual cap OR category over combined cap
        for pr in prs:
            if pr.over_cap:
                total_violations += 1
        if over_combined:
            total_violations += 1

        categories.append(CategoryResult(
            category=cat_name,
            combined_cap=combined_cap,
            combined_count=combined_count,
            over_combined_cap=over_combined,
            patterns=sorted(prs, key=lambda x: -x.count),
        ))

    categories.sort(key=lambda c: (-int(c.over_combined_cap), -c.combined_count))
    total_matches = sum(pr.count for pr in pattern_results.values())

    # --- Paragraph-level checks ---
    para_violations = _check_paragraph_openers(prose_text)
    if para_violations:
        para_patterns = []
        for pv in para_violations:
            pr = PatternResult(
                name=pv["name"],
                category="paragraph_structure",
                cap=pv["cap"],
                count=pv["count"],
                over_cap=pv["count"] > pv["cap"],
                matches=pv["matches"],
            )
            para_patterns.append(pr)
            if pr.over_cap:
                total_violations += 1
            total_matches += pr.count

        categories.append(CategoryResult(
            category="paragraph_structure",
            combined_cap=None,
            combined_count=sum(p.count for p in para_patterns),
            over_combined_cap=False,
            patterns=sorted(para_patterns, key=lambda x: -x.count),
        ))

    categories.sort(key=lambda c: (-int(c.over_combined_cap), -c.combined_count))

    return CheckReport(
        total_words=total_words,
        total_violations=total_violations,
        total_matches=total_matches,
        categories=categories,
    )


def _check_paragraph_openers(text: str) -> list[dict]:
    """Detect paragraph opener repetition patterns.

    Rules from 09-opener-repetition.md:
    - No more than 2 consecutive paragraphs starting with the same word
    - No more than 3 'She' openers in any 6-paragraph stretch
    """
    # Split into paragraphs (non-empty, non-header lines after a blank line)
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        # Skip pure dialogue paragraphs (start with quote mark)
        first_char = block[0] if block else ""
        if first_char in '"\u201c':
            # Still track the opener for repetition purposes
            first_word = block.lstrip('"\u201c\u201d ').split()[0] if block.lstrip('"\u201c\u201d ') else ""
            paragraphs.append({"text": block, "opener": first_word, "is_dialogue": True,
                               "line": text[:text.find(block)].count("\n") + 1})
        else:
            first_word = block.split()[0] if block.split() else ""
            paragraphs.append({"text": block, "opener": first_word, "is_dialogue": False,
                               "line": text[:text.find(block)].count("\n") + 1})

    violations = []

    # Check consecutive same-word openers (3+ in a row = violation)
    consecutive_runs = []
    i = 0
    while i < len(paragraphs):
        word = paragraphs[i]["opener"].lower().rstrip(".,;:!?")
        run_start = i
        while i < len(paragraphs) and paragraphs[i]["opener"].lower().rstrip(".,;:!?") == word:
            i += 1
        run_len = i - run_start
        if run_len >= 3:
            consecutive_runs.append((word, run_start, run_len))

    if consecutive_runs:
        matches = []
        for word, start_idx, run_len in consecutive_runs:
            p = paragraphs[start_idx]
            snippet = p["text"][:80].replace("\n", " ")
            matches.append(Match(
                pattern_name="opener_consecutive_repeat",
                category="paragraph_structure",
                matched_text=f"{run_len}x '{word}'",
                line_number=p["line"],
                context=f"{run_len} consecutive paragraphs starting with '{word}': {snippet}...",
                cap=0,
            ))
        violations.append({
            "name": "opener_consecutive_repeat",
            "cap": 0,
            "count": len(matches),
            "matches": matches,
        })

    # Check 'She' density: >3 'She' openers in any 6-paragraph window
    she_heavy_windows = []
    for window_start in range(len(paragraphs) - 5):
        window = paragraphs[window_start:window_start + 6]
        she_count = sum(1 for p in window if p["opener"].lower().rstrip(".,;:!?") == "she")
        if she_count > 3:
            she_heavy_windows.append((window_start, she_count))

    if she_heavy_windows:
        # Deduplicate overlapping windows — report the worst one
        worst = max(she_heavy_windows, key=lambda x: x[1])
        start_idx, count = worst
        p = paragraphs[start_idx]
        matches = [Match(
            pattern_name="opener_she_density",
            category="paragraph_structure",
            matched_text=f"{count}/6 'She' openers",
            line_number=p["line"],
            context=f"{count} of 6 consecutive paragraphs start with 'She' (max 3)",
            cap=0,
        )]
        violations.append({
            "name": "opener_she_density",
            "cap": 0,
            "count": 1,
            "matches": matches,
        })

    return violations


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_json(report: CheckReport, filepath: str) -> str:
    """Format as JSON for gate consumption."""
    cats = []
    for cr in report.categories:
        pats = []
        for pr in cr.patterns:
            if pr.count == 0:
                continue
            pats.append({
                "name": pr.name,
                "count": pr.count,
                "cap": pr.cap,
                "over_cap": pr.over_cap,
                "matches": [
                    {
                        "text": m.matched_text,
                        "line": m.line_number,
                        "context": m.context,
                    }
                    for m in pr.matches
                ],
            })
        if not pats and not cr.over_combined_cap:
            continue
        cat_obj = {
            "category": cr.category,
            "combined_count": cr.combined_count,
            "patterns": pats,
        }
        if cr.combined_cap is not None:
            cat_obj["combined_cap"] = cr.combined_cap
            cat_obj["over_combined_cap"] = cr.over_combined_cap
        cats.append(cat_obj)

    return json.dumps({
        "file": filepath,
        "total_words": report.total_words,
        "total_matches": report.total_matches,
        "total_violations": report.total_violations,
        "categories": cats,
    }, indent=2)


def format_summary(report: CheckReport, filepath: str) -> str:
    """Human-readable summary."""
    lines = [
        f"SLOP CHECK: {filepath}",
        f"Words: {report.total_words}  Matches: {report.total_matches}  Violations: {report.total_violations}",
        "",
    ]

    for cr in report.categories:
        if cr.combined_count == 0:
            continue

        cap_str = ""
        if cr.combined_cap is not None:
            marker = " !!!" if cr.over_combined_cap else ""
            cap_str = f"  [combined: {cr.combined_count}/{cr.combined_cap}{marker}]"

        lines.append(f"  {cr.category}: {cr.combined_count} total{cap_str}")

        for pr in cr.patterns:
            if pr.count == 0:
                continue
            marker = " !!!" if pr.over_cap else ""
            lines.append(f"    {pr.name}: {pr.count}/{pr.cap}{marker}")

    return "\n".join(lines)


def format_violations(report: CheckReport, filepath: str) -> str:
    """Show only violations — patterns over their cap, with match locations."""
    lines = [
        f"SLOP VIOLATIONS: {filepath}",
        f"Total violations: {report.total_violations}",
        "",
    ]

    any_found = False
    for cr in report.categories:
        cat_violations = []

        if cr.over_combined_cap:
            cat_violations.append(
                f"  COMBINED CAP EXCEEDED: {cr.combined_count}/{cr.combined_cap}"
            )
            # Show all matches in category when combined cap is violated
            for pr in cr.patterns:
                if pr.count == 0:
                    continue
                cat_violations.append(f"    {pr.name}: {pr.count}")
                for m in pr.matches:
                    cat_violations.append(f"      L{m.line_number}: {m.context.strip()}")

        for pr in cr.patterns:
            if not pr.over_cap:
                continue
            cat_violations.append(f"  {pr.name}: {pr.count}/{pr.cap}")
            for m in pr.matches:
                cat_violations.append(f"    L{m.line_number}: {m.context.strip()}")

        if cat_violations:
            any_found = True
            lines.append(f"[{cr.category}]")
            lines.extend(cat_violations)
            lines.append("")

    if not any_found:
        lines.append("  No violations found.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Slop pattern checker: AI prose tic detection with hard caps"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", action="store_true", help="Output JSON report")
    group.add_argument("--summary", action="store_true", help="Output human-readable summary")
    group.add_argument("--violations", action="store_true", help="Show only violations with context")
    parser.add_argument("file", help="Path to prose file")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    report = check_prose(text)

    if args.json:
        print(format_json(report, args.file))
    elif args.summary:
        print(format_summary(report, args.file))
    elif args.violations:
        print(format_violations(report, args.file))


if __name__ == "__main__":
    main()
