"""Core analysis functions."""

import math
import re

from tools.skeleton_strip.splitter import split_paragraphs

from .constants import DEFAULT_TEXTURE_BASELINES
from .models import RhythmReport
from .rhythm import compute_mattr, count_punctuation, opener_stats, word_count
from .texture import (
    balanced_texture_score,
    classify_sentence_texture,
    find_telegram_runs,
    find_texture_deserts,
    texture_verdict,
)


def analyze_rhythm(text: str, texture_baselines: dict = None) -> RhythmReport:
    """Compute all rhythm and texture metrics for a text."""
    if texture_baselines is None:
        texture_baselines = DEFAULT_TEXTURE_BASELINES

    paragraphs = split_paragraphs(text)

    # Flatten sentences
    all_sentences: list[str] = []
    para_sent_counts: list[int] = []
    for p in paragraphs:
        sents = [s.text for s in p.sentences]
        all_sentences.extend(sents)
        para_sent_counts.append(len(sents))

    # Comma:period ratio
    commas, periods = count_punctuation(text)
    cp_ratio = commas / periods

    # Sentence lengths (rhythm thresholds: <=6, >=20)
    lengths = [word_count(s) for s in all_sentences]
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
            texture_baselines=texture_baselines,
        )

    mean_len = sum(lengths) / n_sent
    variance = sum((ln - mean_len) ** 2 for ln in lengths) / n_sent
    stdev_len = math.sqrt(variance)
    cv_len = stdev_len / mean_len if mean_len > 0 else 0.0
    short_pct = sum(1 for ln in lengths if ln <= 6) / n_sent
    long_pct = sum(1 for ln in lengths if ln >= 20) / n_sent

    # Openers
    opener_count_val, opener_entropy_val, top_openers_val = opener_stats(all_sentences)

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
    mattr = compute_mattr(all_words)

    # --- Texture analysis ---
    classifications = [classify_sentence_texture(s) for s in all_sentences]

    participial_count = sum(1 for c in classifications if c["participial"])
    compound_count = sum(1 for c in classifications if c["compound"])
    emdash_count = sum(1 for c in classifications if c["emdash"])
    semicolon_count = sum(1 for c in classifications if c["semicolon"])
    texture_short_count = sum(1 for c in classifications if c["short"])

    tex_metrics = {
        "participial_pct": round(participial_count / n_sent * 100, 1),
        "compound_pct": round(compound_count / n_sent * 100, 1),
        "emdash_pct": round(emdash_count / n_sent * 100, 1),
        "semicolon_pct": round(semicolon_count / n_sent * 100, 1),
        "short_pct": round(texture_short_count / n_sent * 100, 1),
    }

    # Balanced 0–100 score: 100 = all dimensions on target
    tex_score, tex_dim_scores = balanced_texture_score(tex_metrics, texture_baselines)
    tex_metrics["texture_score"] = tex_score

    # Flagged passages
    telegram_runs = find_telegram_runs(classifications, all_sentences)
    texture_deserts = find_texture_deserts(classifications, all_sentences)
    flagged = telegram_runs + texture_deserts
    flagged.sort(key=lambda f: f["start_sentence"])

    # Verdict
    verdict, verdict_reasons = texture_verdict(
        tex_metrics, texture_baselines, tex_dim_scores,
    )

    return RhythmReport(
        commas=commas, periods=periods, cp_ratio=cp_ratio,
        sentence_count=n_sent, mean_sentence_length=mean_len,
        stdev_sentence_length=stdev_len, cv_sentence_length=cv_len,
        short_sentence_pct=short_pct, long_sentence_pct=long_pct,
        opener_count=opener_count_val, opener_entropy=opener_entropy_val,
        top_openers=top_openers_val,
        paragraph_count=n_para,
        mean_paragraph_sentences=mean_para,
        stdev_paragraph_sentences=stdev_para,
        one_sentence_paragraph_pct=one_sent_pct,
        mattr=mattr, unique_words=len(set(all_words)), total_words=len(all_words),
        # Texture
        participial_pct=tex_metrics["participial_pct"],
        compound_pct=tex_metrics["compound_pct"],
        emdash_pct=tex_metrics["emdash_pct"],
        semicolon_pct=tex_metrics["semicolon_pct"],
        texture_short_pct=tex_metrics["short_pct"],
        texture_score=tex_score,
        texture_verdict=verdict,
        texture_verdict_reasons=verdict_reasons,
        texture_flagged=flagged,
        texture_baselines=texture_baselines,
        texture_dimension_scores=tex_dim_scores,
    )


def report_from_json_targets(json_path: str) -> RhythmReport:
    """Build a RhythmReport from stored rhythm targets in a JSON file.

    Reads rhythmMetrics.global and textureMetrics from style-guide.json.
    """
    import json

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    metrics = data.get("rhythmMetrics", {}).get("global", data)
    tex = data.get("textureMetrics", {})

    def _val(d, key, fallback=0):
        entry = d.get(key, {})
        if isinstance(entry, dict):
            return float(entry.get("target", entry.get("measured", entry.get("human", fallback))))
        return float(entry) if entry else fallback

    return RhythmReport(
        commas=0,
        periods=0,
        cp_ratio=_val(metrics, "comma_period_ratio"),
        sentence_count=0,
        mean_sentence_length=_val(metrics, "sentence_length_mean"),
        stdev_sentence_length=0.0,
        cv_sentence_length=_val(metrics, "sentence_length_cv"),
        short_sentence_pct=_val(metrics, "short_sentence_pct") / 100,
        long_sentence_pct=_val(metrics, "long_sentence_pct") / 100,
        opener_count=0,
        opener_entropy=_val(metrics, "opener_entropy"),
        top_openers=[],
        paragraph_count=0,
        mean_paragraph_sentences=0.0,
        stdev_paragraph_sentences=0.0,
        one_sentence_paragraph_pct=_val(metrics, "one_sentence_paragraph_pct") / 100,
        mattr=_val(metrics, "mattr"),
        unique_words=0,
        total_words=0,
        # Texture
        participial_pct=_val(tex, "participial_pct"),
        compound_pct=_val(tex, "compound_pct"),
        emdash_pct=_val(tex, "emdash_pct"),
        semicolon_pct=_val(tex, "semicolon_pct"),
        texture_short_pct=_val(tex, "short_pct"),
        texture_score=100.0,  # target is 100 by definition on balanced scale
        texture_verdict="stored_target",
        texture_verdict_reasons=[],
        texture_flagged=[],
        texture_baselines=tex if tex else DEFAULT_TEXTURE_BASELINES,
    )
