#!/usr/bin/env python3
"""Rhythm scorer — measures prose rhythm metrics against a style target.

Metrics:
  - Comma:period ratio (syntactic complexity proxy)
  - Sentence length distribution (mean, stdev, CV, short%)
  - Sentence opener variety (first-word repetition rate)
  - Paragraph length uniformity
  - Vocabulary richness (MATTR — Moving Average Type-Token Ratio)

Usage:
    python3 tools/rhythm_scorer/score.py --json path/to/draft.md
    python3 tools/rhythm_scorer/score.py --summary path/to/draft.md
    python3 tools/rhythm_scorer/score.py --compare path/to/draft.md --target path/to/source.md
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from tools.skeleton_strip.splitter import split_paragraphs, split_sentences


@dataclass
class RhythmReport:
    # Comma:period ratio
    commas: int
    periods: int
    cp_ratio: float

    # Sentence length
    sentence_count: int
    mean_sentence_length: float
    stdev_sentence_length: float
    cv_sentence_length: float       # coefficient of variation
    short_sentence_pct: float       # sentences <= 6 words
    long_sentence_pct: float        # sentences >= 20 words

    # Opener variety
    opener_count: int               # distinct first words
    opener_entropy: float           # Shannon entropy of first-word dist
    top_openers: list[tuple[str, int]]  # top 5 most common openers

    # Paragraph rhythm
    paragraph_count: int
    mean_paragraph_sentences: float
    stdev_paragraph_sentences: float
    one_sentence_paragraph_pct: float

    # Vocabulary richness (MATTR with window=50)
    mattr: float
    unique_words: int
    total_words: int


def _count_punctuation(text: str) -> tuple[int, int]:
    """Count commas and sentence-ending punctuation."""
    commas = text.count(',')
    # Periods, question marks, exclamation marks as sentence-enders
    periods = len(re.findall(r'[.!?]+', text))
    return commas, max(periods, 1)  # avoid div by zero


def _word_count(sentence_text: str) -> int:
    """Count words in a sentence."""
    return len(re.findall(r'\S+', sentence_text))


def _compute_mattr(words: list[str], window: int = 50) -> float:
    """Moving Average Type-Token Ratio. Window size 50 is standard."""
    if len(words) < window:
        if not words:
            return 0.0
        return len(set(words)) / len(words)

    ttrs: list[float] = []
    for i in range(len(words) - window + 1):
        chunk = words[i:i + window]
        ttrs.append(len(set(chunk)) / window)
    return sum(ttrs) / len(ttrs)


def _opener_stats(
    sentences: list[str],
) -> tuple[int, float, list[tuple[str, int]]]:
    """Analyze sentence opener (first word) distribution."""
    openers: list[str] = []
    for s in sentences:
        words = s.split()
        if words:
            # Normalize: strip quotes, lowercase
            w = words[0].strip('""\u201C\u201D\u2018\u2019').lower()
            if w:
                openers.append(w)

    if not openers:
        return 0, 0.0, []

    counts = Counter(openers)
    n = len(openers)
    distinct = len(counts)

    # Shannon entropy
    entropy = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            entropy -= p * math.log2(p)

    top = counts.most_common(5)
    return distinct, entropy, top


def analyze_rhythm(text: str) -> RhythmReport:
    """Compute all rhythm metrics for a text."""
    paragraphs = split_paragraphs(text)

    # Flatten sentences
    all_sentences: list[str] = []
    para_sent_counts: list[int] = []
    for p in paragraphs:
        sents = [s.text for s in p.sentences]
        all_sentences.extend(sents)
        para_sent_counts.append(len(sents))

    # Comma:period ratio
    commas, periods = _count_punctuation(text)
    cp_ratio = commas / periods

    # Sentence lengths
    lengths = [_word_count(s) for s in all_sentences]
    n_sent = len(lengths)
    if n_sent == 0:
        return RhythmReport(
            commas=commas, periods=periods, cp_ratio=cp_ratio,
            sentence_count=0, mean_sentence_length=0.0,
            stdev_sentence_length=0.0, cv_sentence_length=0.0,
            short_sentence_pct=0.0, long_sentence_pct=0.0,
            opener_count=0, opener_entropy=0.0, top_openers=[],
            paragraph_count=len(paragraphs),
            mean_paragraph_sentences=0.0, stdev_paragraph_sentences=0.0,
            one_sentence_paragraph_pct=0.0,
            mattr=0.0, unique_words=0, total_words=0,
        )

    mean_len = sum(lengths) / n_sent
    variance = sum((l - mean_len) ** 2 for l in lengths) / n_sent
    stdev_len = math.sqrt(variance)
    cv_len = stdev_len / mean_len if mean_len > 0 else 0.0
    short_pct = sum(1 for l in lengths if l <= 6) / n_sent
    long_pct = sum(1 for l in lengths if l >= 20) / n_sent

    # Openers
    opener_count, opener_entropy, top_openers = _opener_stats(all_sentences)

    # Paragraph rhythm
    n_para = len(para_sent_counts)
    mean_para = sum(para_sent_counts) / n_para if n_para > 0 else 0.0
    para_var = (
        sum((c - mean_para) ** 2 for c in para_sent_counts) / n_para
        if n_para > 0 else 0.0
    )
    stdev_para = math.sqrt(para_var)
    one_sent_pct = (
        sum(1 for c in para_sent_counts if c == 1) / n_para if n_para > 0 else 0.0
    )

    # MATTR
    all_words = [
        w.lower() for s in all_sentences
        for w in re.findall(r'[a-zA-Z]+', s)
    ]
    mattr = _compute_mattr(all_words)

    return RhythmReport(
        commas=commas, periods=periods, cp_ratio=cp_ratio,
        sentence_count=n_sent, mean_sentence_length=mean_len,
        stdev_sentence_length=stdev_len, cv_sentence_length=cv_len,
        short_sentence_pct=short_pct, long_sentence_pct=long_pct,
        opener_count=opener_count, opener_entropy=opener_entropy,
        top_openers=top_openers,
        paragraph_count=n_para,
        mean_paragraph_sentences=mean_para,
        stdev_paragraph_sentences=stdev_para,
        one_sentence_paragraph_pct=one_sent_pct,
        mattr=mattr, unique_words=len(set(all_words)), total_words=len(all_words),
    )


def report_from_json_targets(json_path: str) -> RhythmReport:
    """Build a RhythmReport from stored rhythm targets in a JSON file.

    Supports two formats:
    1. Style-guide format: top-level 'rhythmMetrics' key
    2. Direct format: top-level keys matching rhythm metric names
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    metrics = data.get("rhythmMetrics", data)

    return RhythmReport(
        commas=0,
        periods=0,
        cp_ratio=float(metrics.get("commaPeriodRatio", 0)),
        sentence_count=0,
        mean_sentence_length=float(metrics.get("sentenceLengthMean", 0)),
        stdev_sentence_length=0.0,
        cv_sentence_length=float(metrics.get("sentenceLengthCV", 0)),
        short_sentence_pct=float(metrics.get("shortSentencePct", 0)) / 100,
        long_sentence_pct=float(metrics.get("longSentencePct", 0)) / 100,
        opener_count=0,
        opener_entropy=float(metrics.get("openerEntropy", 0)),
        top_openers=[],
        paragraph_count=0,
        mean_paragraph_sentences=0.0,
        stdev_paragraph_sentences=0.0,
        one_sentence_paragraph_pct=float(metrics.get("oneSentenceParagraphPct", 0)) / 100,
        mattr=float(metrics.get("mattr", 0)),
        unique_words=0,
        total_words=0,
    )


def format_json(report: RhythmReport, filepath: str) -> str:
    """Format report as JSON."""
    return json.dumps({
        "file": filepath,
        "comma_period_ratio": round(report.cp_ratio, 3),
        "sentence": {
            "count": report.sentence_count,
            "mean_length": round(report.mean_sentence_length, 1),
            "stdev_length": round(report.stdev_sentence_length, 1),
            "cv_length": round(report.cv_sentence_length, 3),
            "short_pct": round(report.short_sentence_pct * 100, 1),
            "long_pct": round(report.long_sentence_pct * 100, 1),
        },
        "openers": {
            "distinct_count": report.opener_count,
            "entropy": round(report.opener_entropy, 2),
            "top_5": [{"word": w, "count": c} for w, c in report.top_openers],
        },
        "paragraph": {
            "count": report.paragraph_count,
            "mean_sentences": round(report.mean_paragraph_sentences, 1),
            "stdev_sentences": round(report.stdev_paragraph_sentences, 1),
            "one_sentence_pct": round(report.one_sentence_paragraph_pct * 100, 1),
        },
        "vocabulary": {
            "mattr": round(report.mattr, 3),
            "unique_words": report.unique_words,
            "total_words": report.total_words,
        },
    }, indent=2)


def format_summary(report: RhythmReport, filepath: str) -> str:
    """Format report as human-readable summary."""
    lines = [
        f"RHYTHM: {filepath}",
        f"",
        f"COMMA:PERIOD RATIO: {report.cp_ratio:.2f}",
        f"  (commas={report.commas}, periods={report.periods})",
        f"",
        f"SENTENCE LENGTH:",
        f"  count={report.sentence_count}  mean={report.mean_sentence_length:.1f}  stdev={report.stdev_sentence_length:.1f}  CV={report.cv_sentence_length:.2f}",
        f"  short(≤6w)={report.short_sentence_pct*100:.1f}%  long(≥20w)={report.long_sentence_pct*100:.1f}%",
        f"",
        f"OPENERS:",
        f"  distinct={report.opener_count}  entropy={report.opener_entropy:.2f}",
        f"  top 5: {', '.join(f'{w}({c})' for w, c in report.top_openers)}",
        f"",
        f"PARAGRAPHS:",
        f"  count={report.paragraph_count}  mean_sents={report.mean_paragraph_sentences:.1f}  stdev={report.stdev_paragraph_sentences:.1f}",
        f"  one-sentence paragraphs: {report.one_sentence_paragraph_pct*100:.1f}%",
        f"",
        f"VOCABULARY:",
        f"  MATTR={report.mattr:.3f}  unique={report.unique_words}/{report.total_words}",
    ]
    return "\n".join(lines)


def format_comparison(draft: RhythmReport, target: RhythmReport, draft_path: str, target_path: str) -> str:
    """Compare draft rhythm against target, highlighting deviations."""
    def delta(d: float, t: float) -> str:
        if t == 0:
            return "n/a"
        pct = ((d - t) / t) * 100
        arrow = "↑" if pct > 0 else "↓"
        return f"{arrow}{abs(pct):.0f}%"

    lines = [
        f"RHYTHM COMPARISON",
        f"  Draft:  {draft_path}",
        f"  Target: {target_path}",
        f"",
        f"{'Metric':<30} {'Draft':>8} {'Target':>8} {'Delta':>8}",
        f"{'-'*56}",
        f"{'Comma:period ratio':<30} {draft.cp_ratio:>8.2f} {target.cp_ratio:>8.2f} {delta(draft.cp_ratio, target.cp_ratio):>8}",
        f"{'Mean sentence length':<30} {draft.mean_sentence_length:>8.1f} {target.mean_sentence_length:>8.1f} {delta(draft.mean_sentence_length, target.mean_sentence_length):>8}",
        f"{'Sentence CV':<30} {draft.cv_sentence_length:>8.2f} {target.cv_sentence_length:>8.2f} {delta(draft.cv_sentence_length, target.cv_sentence_length):>8}",
        f"{'Short sentences (≤6w)':<30} {draft.short_sentence_pct*100:>7.1f}% {target.short_sentence_pct*100:>7.1f}% {delta(draft.short_sentence_pct, target.short_sentence_pct):>8}",
        f"{'Long sentences (≥20w)':<30} {draft.long_sentence_pct*100:>7.1f}% {target.long_sentence_pct*100:>7.1f}% {delta(draft.long_sentence_pct, target.long_sentence_pct):>8}",
        f"{'Opener entropy':<30} {draft.opener_entropy:>8.2f} {target.opener_entropy:>8.2f} {delta(draft.opener_entropy, target.opener_entropy):>8}",
        f"{'1-sentence paragraphs':<30} {draft.one_sentence_paragraph_pct*100:>7.1f}% {target.one_sentence_paragraph_pct*100:>7.1f}% {delta(draft.one_sentence_paragraph_pct, target.one_sentence_paragraph_pct):>8}",
        f"{'MATTR':<30} {draft.mattr:>8.3f} {target.mattr:>8.3f} {delta(draft.mattr, target.mattr):>8}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rhythm scorer: prose rhythm analysis")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", action="store_true", help="Output JSON report")
    group.add_argument("--summary", action="store_true", help="Output human-readable summary")
    group.add_argument("--compare", action="store_true", help="Compare draft vs target")
    parser.add_argument("file", help="Path to prose file")
    parser.add_argument("--target", help="Target file for comparison mode")
    parser.add_argument("--target-json", help="JSON file with rhythm targets (e.g. style-guide.json)")

    args = parser.parse_args()

    if args.compare and not args.target and not args.target_json:
        print("--compare requires --target or --target-json", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    report = analyze_rhythm(text)

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
            target_report = analyze_rhythm(target_text)
            target_label = args.target
        print(format_comparison(report, target_report, args.file, target_label))


if __name__ == "__main__":
    main()
