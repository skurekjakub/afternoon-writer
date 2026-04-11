#!/usr/bin/env python3
"""Rhythm & texture scorer — prose rhythm and structural complexity analysis.

RHYTHM METRICS:
  - Comma:period ratio (syntactic complexity proxy)
  - Sentence length distribution (mean, stdev, CV, short/long %)
  - Sentence opener variety (first-word entropy)
  - Paragraph length uniformity
  - Vocabulary richness (MATTR)

TEXTURE METRICS (structural sentence complexity):
  - Participial phrases: ', Ving' constructions (human ~14%, pipeline ~2%)
  - Compound sentences: ', and/but/or/yet/so' clauses (human ~10%, pipeline ~6%)
  - Em-dashes: mid-sentence pivots and asides (human ~5%, pipeline ~1%)
  - Semicolons: clause-joining (human ~2%, pipeline ~0.3%)
  - Short sentences: <=8 words (human ~36%, pipeline ~47%)
  - Texture score: combined % of sentences with any joining construction

Usage:
    python3 tools/rhythm_scorer/score.py --json path/to/draft.md
    python3 tools/rhythm_scorer/score.py --summary path/to/draft.md
    python3 tools/rhythm_scorer/score.py --compare path/to/draft.md --target path/to/source.md
"""

import argparse
import json
import os
import sys

# Ensure parent package is importable when run as script
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from tools.rhythm_scorer.analyze import analyze_rhythm, report_from_json_targets
from tools.rhythm_scorer.constants import DEFAULT_TEXTURE_BASELINES
from tools.rhythm_scorer.formatters import format_comparison, format_json, format_summary


def main():
    parser = argparse.ArgumentParser(
        description="Rhythm & texture scorer: prose rhythm and structural complexity analysis"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", action="store_true", help="Output JSON report")
    group.add_argument("--summary", action="store_true", help="Output human-readable summary")
    group.add_argument("--compare", action="store_true", help="Compare draft vs target")
    parser.add_argument("file", help="Path to prose file")
    parser.add_argument("--target", help="Target file for comparison mode")
    parser.add_argument("--target-json", help="JSON file with rhythm targets (e.g. style-guide.json)")
    parser.add_argument("--baselines", help="JSON file with texture baselines (overrides defaults)")

    args = parser.parse_args()

    if args.compare and not args.target and not args.target_json:
        print("--compare requires --target or --target-json", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Load texture baselines
    texture_bl = DEFAULT_TEXTURE_BASELINES
    if args.baselines:
        with open(args.baselines, encoding="utf-8") as f:
            loaded = json.load(f)
            texture_bl = loaded.get("textureMetrics", loaded)

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    # Strip markdown headers from analysis
    text_lines = [ln for ln in text.split('\n') if not ln.startswith('#')]
    text = '\n'.join(text_lines)

    report = analyze_rhythm(text, texture_baselines=texture_bl)

    if args.json:
        print(format_json(report, args.file))
    elif args.summary:
        print(format_summary(report, args.file))
    elif args.compare:
        if args.target_json:
            target_report = report_from_json_targets(args.target_json)
            target_label = f"{args.target_json} (stored targets)"
        else:
            with open(args.target, encoding="utf-8") as f:
                target_text = f.read()
            target_text_lines = [ln for ln in target_text.split('\n') if not ln.startswith('#')]
            target_text = '\n'.join(target_text_lines)
            target_report = analyze_rhythm(target_text, texture_baselines=texture_bl)
            target_label = args.target
        print(format_comparison(report, target_report, args.file, target_label))


if __name__ == "__main__":
    main()
