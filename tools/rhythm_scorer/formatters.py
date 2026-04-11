"""Output formatting for rhythm and texture reports."""

import json

from .models import RhythmReport
from .texture import texture_interpretation


def format_json(report: RhythmReport, filepath: str) -> str:
    """Format report as JSON with rhythm + texture blocks.

    The texture block includes an 'interpretation' field with specific,
    actionable instructions for agents on what to fix and how.
    """
    tex_metrics = {
        "participial_pct": report.participial_pct,
        "compound_pct": report.compound_pct,
        "emdash_pct": report.emdash_pct,
        "semicolon_pct": report.semicolon_pct,
        "short_pct": report.texture_short_pct,
        "texture_score": report.texture_score,
    }

    interpretation = texture_interpretation(
        tex_metrics, report.texture_baselines,
        report.texture_verdict, report.texture_verdict_reasons,
    )

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
        "texture": {
            "participial_pct": report.participial_pct,
            "compound_pct": report.compound_pct,
            "emdash_pct": report.emdash_pct,
            "semicolon_pct": report.semicolon_pct,
            "short_pct": report.texture_short_pct,
            "texture_score": report.texture_score,
            "verdict": report.texture_verdict,
            "verdict_reasons": report.texture_verdict_reasons,
            "interpretation": interpretation,
            "baselines": report.texture_baselines,
            "flagged_passages": report.texture_flagged,
        },
    }, indent=2)


def format_summary(report: RhythmReport, filepath: str) -> str:
    """Format report as human-readable summary with rhythm + texture."""
    lines = [
        f"RHYTHM & TEXTURE: {filepath}",
        f"",
        f"--- RHYTHM ---",
        f"COMMA:PERIOD RATIO: {report.cp_ratio:.2f}",
        f"  (commas={report.commas}, periods={report.periods})",
        f"",
        f"SENTENCE LENGTH:",
        f"  count={report.sentence_count}  mean={report.mean_sentence_length:.1f}"
        f"  stdev={report.stdev_sentence_length:.1f}  CV={report.cv_sentence_length:.2f}",
        f"  short(<=6w)={report.short_sentence_pct*100:.1f}%"
        f"  long(>=20w)={report.long_sentence_pct*100:.1f}%",
        f"",
        f"OPENERS:",
        f"  distinct={report.opener_count}  entropy={report.opener_entropy:.2f}",
        f"  top 5: {', '.join(f'{w}({c})' for w, c in report.top_openers)}",
        f"",
        f"PARAGRAPHS:",
        f"  count={report.paragraph_count}"
        f"  mean_sents={report.mean_paragraph_sentences:.1f}"
        f"  stdev={report.stdev_paragraph_sentences:.1f}",
        f"  one-sentence paragraphs: {report.one_sentence_paragraph_pct*100:.1f}%",
        f"",
        f"VOCABULARY:",
        f"  MATTR={report.mattr:.3f}  unique={report.unique_words}/{report.total_words}",
        f"",
        f"--- TEXTURE ---",
        f"  participial: {report.participial_pct:.1f}%"
        f"  compound: {report.compound_pct:.1f}%"
        f"  emdash: {report.emdash_pct:.1f}%"
        f"  semicolon: {report.semicolon_pct:.1f}%",
        f"  short(<=8w): {report.texture_short_pct:.1f}%"
        f"  texture_score: {report.texture_score:.1f}",
        f"  verdict: {report.texture_verdict}",
    ]

    if report.texture_verdict_reasons:
        lines.append("  GAPS: " + "; ".join(report.texture_verdict_reasons))

    if report.texture_flagged:
        lines.append(f"  FLAGGED PASSAGES: {len(report.texture_flagged)}")
        for fp in report.texture_flagged[:5]:
            lines.append(
                f"    {fp['type']} sents {fp['start_sentence']}-{fp['end_sentence']}"
                f" ({fp['sentence_count']} sents): {fp.get('preview', '')[:80]}"
            )
        if len(report.texture_flagged) > 5:
            lines.append(f"    ... and {len(report.texture_flagged) - 5} more")

    return "\n".join(lines)


def format_comparison(
    draft: RhythmReport, target: RhythmReport,
    draft_path: str, target_path: str,
) -> str:
    """Compare draft against target, highlighting deviations."""
    def delta(d: float, t: float) -> str:
        if t == 0:
            return "n/a"
        pct = ((d - t) / t) * 100
        arrow = "\u2191" if pct > 0 else "\u2193"
        return f"{arrow}{abs(pct):.0f}%"

    lines = [
        f"RHYTHM & TEXTURE COMPARISON",
        f"  Draft:  {draft_path}",
        f"  Target: {target_path}",
        f"",
        f"{'Metric':<30} {'Draft':>8} {'Target':>8} {'Delta':>8}",
        f"{'-'*56}",
        f"{'Comma:period ratio':<30} {draft.cp_ratio:>8.2f}"
        f" {target.cp_ratio:>8.2f}"
        f" {delta(draft.cp_ratio, target.cp_ratio):>8}",
        f"{'Mean sentence length':<30} {draft.mean_sentence_length:>8.1f}"
        f" {target.mean_sentence_length:>8.1f}"
        f" {delta(draft.mean_sentence_length, target.mean_sentence_length):>8}",
        f"{'Sentence CV':<30} {draft.cv_sentence_length:>8.2f}"
        f" {target.cv_sentence_length:>8.2f}"
        f" {delta(draft.cv_sentence_length, target.cv_sentence_length):>8}",
        f"{'Short sentences (<=6w)':<30} {draft.short_sentence_pct*100:>7.1f}%"
        f" {target.short_sentence_pct*100:>7.1f}%"
        f" {delta(draft.short_sentence_pct, target.short_sentence_pct):>8}",
        f"{'Long sentences (>=20w)':<30} {draft.long_sentence_pct*100:>7.1f}%"
        f" {target.long_sentence_pct*100:>7.1f}%"
        f" {delta(draft.long_sentence_pct, target.long_sentence_pct):>8}",
        f"{'Opener entropy':<30} {draft.opener_entropy:>8.2f}"
        f" {target.opener_entropy:>8.2f}"
        f" {delta(draft.opener_entropy, target.opener_entropy):>8}",
        f"{'1-sentence paragraphs':<30} {draft.one_sentence_paragraph_pct*100:>7.1f}%"
        f" {target.one_sentence_paragraph_pct*100:>7.1f}%"
        f" {delta(draft.one_sentence_paragraph_pct, target.one_sentence_paragraph_pct):>8}",
        f"{'MATTR':<30} {draft.mattr:>8.3f}"
        f" {target.mattr:>8.3f}"
        f" {delta(draft.mattr, target.mattr):>8}",
        f"",
        f"{'--- Texture ---':<30}",
        f"{'Participial phrases':<30} {draft.participial_pct:>7.1f}%"
        f" {target.participial_pct:>7.1f}%"
        f" {delta(draft.participial_pct, target.participial_pct):>8}",
        f"{'Compound sentences':<30} {draft.compound_pct:>7.1f}%"
        f" {target.compound_pct:>7.1f}%"
        f" {delta(draft.compound_pct, target.compound_pct):>8}",
        f"{'Em-dashes':<30} {draft.emdash_pct:>7.1f}%"
        f" {target.emdash_pct:>7.1f}%"
        f" {delta(draft.emdash_pct, target.emdash_pct):>8}",
        f"{'Semicolons':<30} {draft.semicolon_pct:>7.1f}%"
        f" {target.semicolon_pct:>7.1f}%"
        f" {delta(draft.semicolon_pct, target.semicolon_pct):>8}",
        f"{'Short (<=8w)':<30} {draft.texture_short_pct:>7.1f}%"
        f" {target.texture_short_pct:>7.1f}%"
        f" {delta(draft.texture_short_pct, target.texture_short_pct):>8}",
        f"{'Texture score':<30} {draft.texture_score:>7.1f}%"
        f" {target.texture_score:>7.1f}%"
        f" {delta(draft.texture_score, target.texture_score):>8}",
    ]
    return "\n".join(lines)
