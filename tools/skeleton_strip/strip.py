#!/usr/bin/env python3
"""Skeleton strip CLI — analyze prose concreteness and interpretive patterns.

Usage:
    python3 -m tools.skeleton-strip.strip --json   path/to/draft.md
    python3 -m tools.skeleton-strip.strip --skeleton path/to/draft.md
    python3 -m tools.skeleton-strip.strip --summary  path/to/draft.md

Or directly:
    python3 tools/skeleton-strip/strip.py --json path/to/draft.md
"""

import argparse
import json
import sys
import os

# Allow running as script or module
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from tools.skeleton_strip.scorer import load_norms
from tools.skeleton_strip.engine import analyze_document, DocumentAnalysis


def format_json(analysis: DocumentAnalysis, filepath: str) -> str:
    """Format analysis as JSON for gate agent consumption."""
    result = {
        "file": filepath,
        "overall": {
            "total_sentences": analysis.total_sentences,
            "abstract_sentences": analysis.abstract_sentences,
            "concrete_sentences": analysis.concrete_sentences,
            "abstract_percentage": round(
                analysis.abstract_sentences / analysis.total_sentences * 100, 1
            ) if analysis.total_sentences > 0 else 0,
            "total_pattern_matches": analysis.total_pattern_matches,
            "mean_density": round(analysis.mean_density, 3),
            "verdict": analysis.overall_verdict,
        },
        "flagged_zones": [
            {
                "paragraphs": fz.paragraph_indices,
                "reason": fz.reason,
                "mean_density": round(fz.mean_density, 3),
                "pattern_count": fz.pattern_count,
                "sentences": [
                    {
                        "paragraph": sa.sentence.paragraph_index,
                        "index": sa.sentence.index,
                        "text": sa.sentence.text[:200],
                        "density": round(sa.density, 3),
                        "abstract_words": sa.stripped_words[:10],
                        "patterns": [pm.pattern_name for pm in sa.pattern_matches],
                        "verdict": sa.verdict,
                    }
                    for pa in analysis.paragraphs
                    if pa.paragraph.index in fz.paragraph_indices
                    for sa in pa.sentences
                    if sa.verdict in ("abstract", "mixed")
                ],
            }
            for fz in analysis.flagged_zones
        ],
        "by_paragraph": [
            {
                "index": pa.paragraph.index,
                "sentence_count": len(pa.sentences),
                "mean_density": round(pa.mean_density, 3),
                "abstract_sentences": pa.abstract_sentence_count,
                "pattern_matches": pa.total_pattern_matches,
                "verdict": pa.verdict,
            }
            for pa in analysis.paragraphs
        ],
    }
    return json.dumps(result, indent=2)


def format_skeleton(analysis: DocumentAnalysis) -> str:
    """Format analysis as human-readable skeleton view."""
    lines: list[str] = []

    for pa in analysis.paragraphs:
        verdict_icon = {"grounded": "\u2705", "drifting": "\u26A0\uFE0F", "abstract": "\u274C"}.get(pa.verdict, "?")
        lines.append(
            f"\nPARAGRAPH {pa.paragraph.index + 1} [{pa.verdict}, density={pa.mean_density:.2f}] {verdict_icon}"
        )

        for sa in pa.sentences:
            s_icon = {"concrete": "\u2705", "mixed": "\u26A0\uFE0F", "abstract": "\u274C"}.get(sa.verdict, "?")
            # Truncate long sentences
            display_text = sa.sentence.text
            if len(display_text) > 120:
                display_text = display_text[:117] + "..."
            lines.append(f'  "{display_text}"')

            concrete_display = ", ".join(sa.word_score.concrete_words[:8])
            abstract_display = ", ".join(sa.stripped_words[:8])
            lines.append(
                f"   SKELETON: [{concrete_display}] density={sa.density:.2f} {s_icon}"
            )
            if abstract_display:
                lines.append(f"   STRIPPED: [{abstract_display}]")
            if sa.pattern_matches:
                pnames = ", ".join(pm.pattern_name for pm in sa.pattern_matches)
                lines.append(f"   PATTERNS: {pnames}")

    return "\n".join(lines)


def format_summary(analysis: DocumentAnalysis, filepath: str) -> str:
    """Format analysis as concise flagged-zone summary."""
    lines = [
        f"DRAFT: {filepath}",
        f"OVERALL: {analysis.total_sentences} sentences, "
        f"{analysis.abstract_sentences / analysis.total_sentences * 100:.1f}% abstract, "
        f"mean density {analysis.mean_density:.2f}, "
        f"verdict: {analysis.overall_verdict}"
        if analysis.total_sentences > 0 else "OVERALL: empty document",
    ]

    if analysis.flagged_zones:
        lines.append(f"FLAGGED ZONES: {len(analysis.flagged_zones)}")
        for fz in analysis.flagged_zones:
            para_str = (
                f"\u00B6{fz.paragraph_indices[0] + 1}"
                if len(fz.paragraph_indices) == 1
                else f"\u00B6{fz.paragraph_indices[0] + 1}-{fz.paragraph_indices[-1] + 1}"
            )
            extra = f", {fz.pattern_count} pattern matches" if fz.pattern_count > 0 else ""
            lines.append(f"  {para_str}: {fz.reason} (density {fz.mean_density:.2f}{extra})")
    else:
        lines.append("FLAGGED ZONES: 0")

    # Paragraph breakdown (compact)
    lines.append("")
    lines.append("PARAGRAPH VERDICTS:")
    for pa in analysis.paragraphs:
        icon = {"grounded": "\u2705", "drifting": "\u26A0\uFE0F", "abstract": "\u274C"}.get(pa.verdict, "?")
        lines.append(
            f"  \u00B6{pa.paragraph.index + 1}: {pa.verdict} "
            f"(density={pa.mean_density:.2f}, sents={len(pa.sentences)}, "
            f"patterns={pa.total_pattern_matches}) {icon}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Skeleton strip: prose concreteness analyzer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", action="store_true", help="Output JSON report")
    group.add_argument("--skeleton", action="store_true", help="Output skeleton view")
    group.add_argument("--summary", action="store_true", help="Output flagged-zone summary")
    parser.add_argument("file", help="Path to prose file (markdown)")
    parser.add_argument("--norms", help="Path to concreteness norms CSV", default=None)

    args = parser.parse_args()

    # Load prose
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    # Load norms
    try:
        norms = load_norms(args.norms)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)

    # Analyze
    analysis = analyze_document(text, norms)

    # Output
    if args.json:
        print(format_json(analysis, args.file))
    elif args.skeleton:
        print(format_skeleton(analysis))
    elif args.summary:
        print(format_summary(analysis, args.file))


if __name__ == "__main__":
    main()
