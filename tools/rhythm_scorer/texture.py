"""Texture analysis helper functions."""

import math

from .constants import (
    COMPOUND_RE,
    DESERT_MIN_SENTENCES,
    EMDASH_RE,
    PARTICIPIAL_RE,
    SEMICOLON_RE,
    SHORT_THRESHOLD,
    TELEGRAM_SHORT_PCT,
    TELEGRAM_WINDOW,
)


def classify_sentence_texture(text: str) -> dict:
    """Classify a single sentence for structural texture features."""
    wc = len(text.split())
    return {
        "participial": bool(PARTICIPIAL_RE.search(text)),
        "compound": bool(COMPOUND_RE.search(text)),
        "emdash": bool(EMDASH_RE.search(text)),
        "semicolon": bool(SEMICOLON_RE.search(text)),
        "short": wc <= SHORT_THRESHOLD,
        "word_count": wc,
    }


def find_telegram_runs(
    classifications: list[dict], sent_texts: list[str],
) -> list[dict]:
    """Find runs of choppy, textureless prose via sliding window.

    A telegram run = TELEGRAM_WINDOW+ consecutive sentences where >=75%
    are short (<=8 words) AND zero have any texture construction.
    """
    n = len(classifications)
    if n < TELEGRAM_WINDOW:
        return []

    flagged = []
    i = 0
    while i <= n - TELEGRAM_WINDOW:
        window = classifications[i:i + TELEGRAM_WINDOW]
        short_count = sum(1 for c in window if c["short"])
        texture_count = sum(
            1 for c in window
            if c["participial"] or c["compound"] or c["emdash"] or c["semicolon"]
        )

        if short_count / TELEGRAM_WINDOW >= TELEGRAM_SHORT_PCT and texture_count == 0:
            # Extend the run
            end = i + TELEGRAM_WINDOW
            while end < n:
                c = classifications[end]
                has_tex = c["participial"] or c["compound"] or c["emdash"] or c["semicolon"]
                if c["short"] and not has_tex:
                    end += 1
                else:
                    break

            run_cls = classifications[i:end]
            run_short = sum(1 for c in run_cls if c["short"]) / len(run_cls) * 100

            preview_sents = sent_texts[i:min(i + 3, end)]
            preview = " ".join(s[:60] for s in preview_sents)
            if len(preview) > 200:
                preview = preview[:197] + "..."

            flagged.append({
                "type": "telegram_run",
                "start_sentence": i,
                "end_sentence": end - 1,
                "sentence_count": end - i,
                "short_pct_in_run": round(run_short, 1),
                "preview": preview,
            })
            i = end
        else:
            i += 1

    return flagged


def find_texture_deserts(
    classifications: list[dict], sent_texts: list[str],
) -> list[dict]:
    """Find long stretches with zero texture constructions.

    A texture desert = DESERT_MIN_SENTENCES+ consecutive sentences
    with no participial, compound, em-dash, or semicolon.
    """
    n = len(classifications)
    flagged = []
    run_start = None

    for i, c in enumerate(classifications):
        has_texture = c["participial"] or c["compound"] or c["emdash"] or c["semicolon"]
        if not has_texture:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None and (i - run_start) >= DESERT_MIN_SENTENCES:
                length = i - run_start
                preview_sents = sent_texts[run_start:min(run_start + 3, i)]
                preview = " ".join(s[:60] for s in preview_sents)
                if len(preview) > 200:
                    preview = preview[:197] + "..."
                flagged.append({
                    "type": "texture_desert",
                    "start_sentence": run_start,
                    "end_sentence": i - 1,
                    "sentence_count": length,
                    "preview": preview,
                })
            run_start = None

    # Trailing desert
    if run_start is not None and (n - run_start) >= DESERT_MIN_SENTENCES:
        length = n - run_start
        preview_sents = sent_texts[run_start:min(run_start + 3, n)]
        preview = " ".join(s[:60] for s in preview_sents)
        if len(preview) > 200:
            preview = preview[:197] + "..."
        flagged.append({
            "type": "texture_desert",
            "start_sentence": run_start,
            "end_sentence": n - 1,
            "sentence_count": length,
            "preview": preview,
        })

    return flagged


# ---------------------------------------------------------------------------
# Balanced texture scoring (0–100 normalized scale)
# ---------------------------------------------------------------------------

DECAY_K = 25    # log-decay steepness: 10pp off target → dimension score ~42
TOLERANCE = 1.0  # ±1 percentage-point dead zone around each target


def dimension_score(actual: float, target: float) -> float:
    """Score how close a single metric is to its target (0–100).

    Returns 100 when within ±TOLERANCE of target.
    Symmetric log-decay penalty for both undershoot and overshoot:
        penalty = DECAY_K × ln(1 + excess_beyond_tolerance)
    """
    delta = abs(actual - target)
    if delta <= TOLERANCE:
        return 100.0
    excess = delta - TOLERANCE
    penalty = DECAY_K * math.log1p(excess)
    return max(0.0, 100.0 - penalty)


def balanced_texture_score(
    metrics: dict, baselines: dict,
) -> tuple[float, dict]:
    """Compute normalized 0–100 texture score from four dimensions.

    Each dimension (participial, compound, emdash, semicolon) is scored
    independently via dimension_score() and weighted equally (25% each).
    100 = all dimensions exactly on target. Both over and under penalized.

    Returns:
        (overall_score, dimension_details)
        dimension_details maps name → {actual, target, score}
    """
    dimensions = {
        "participial": "participial_pct",
        "compound": "compound_pct",
        "emdash": "emdash_pct",
        "semicolon": "semicolon_pct",
    }

    details = {}
    total = 0.0
    for name, key in dimensions.items():
        actual = metrics.get(key, 0.0)
        bl = baselines.get(key, {})
        target = float(bl.get("target", bl.get("human", 0.0)))
        score = dimension_score(actual, target)
        details[name] = {
            "actual": round(actual, 1),
            "target": target,
            "score": round(score, 1),
        }
        total += score

    overall = round(total / len(dimensions), 1)
    return overall, details


# ---------------------------------------------------------------------------
# Verdict and interpretation
# ---------------------------------------------------------------------------

def texture_verdict(
    metrics: dict, baselines: dict,
    dimension_scores: dict | None = None,
) -> tuple[str, list[str]]:
    """Determine texture verdict from balanced 0–100 score.

    Passes when overall texture_score >= 90 and short_pct is in range.
    Per-dimension reasons are always included for the reviser's benefit.
    """
    reasons = []

    if dimension_scores:
        for name, detail in dimension_scores.items():
            if detail["score"] < 90:
                direction = "below" if detail["actual"] < detail["target"] else "above"
                reasons.append(
                    f"{name}: {detail['actual']:.1f}% {direction} target "
                    f"{detail['target']}% (score {detail['score']:.0f}/100)"
                )

    short_violation = False
    if "short_pct" in baselines:
        val = metrics.get("short_pct", 0.0)
        bl = baselines["short_pct"]
        lo, hi = bl["range"]
        human = bl["human"]
        if val > hi:
            reasons.append(
                f"short_pct {val:.1f}% above ceiling {hi}% (human: {human}%)"
            )
            short_violation = True
        elif val < lo:
            reasons.append(
                f"short_pct {val:.1f}% below floor {lo}% (human: {human}%)"
            )
            short_violation = True

    score = metrics.get("texture_score", 0.0)
    if score >= 90.0 and not short_violation:
        return "within_target", reasons
    return "below_target", reasons


def texture_interpretation(
    metrics: dict, baselines: dict, verdict: str, reasons: list[str],
    dimension_scores: dict | None = None,
) -> str:
    """Build agent-readable fix instructions with per-dimension guidance.

    Handles both UNDER-target (add constructions) and OVER-target
    (reduce/replace constructions) for each dimension.
    """
    if verdict == "within_target" and not reasons:
        return "Texture within target range. No structural changes needed."

    parts = []

    if dimension_scores:
        for name, detail in dimension_scores.items():
            if detail["score"] >= 90:
                continue
            actual, target = detail["actual"], detail["target"]
            score_str = f"(score {detail['score']:.0f}/100)"

            if actual < target:
                instructions = {
                    "participial": (
                        "Add ', Ving' phrases: ', turning back to the fire' / "
                        "', gripping the railing'. Connective tissue between actions."
                    ),
                    "compound": (
                        "Join related clauses: ', and' / ', but' / ', yet'. "
                        "Adjacent short sentences often want combining."
                    ),
                    "emdash": (
                        "Use for mid-sentence pivots: "
                        "'The door\u2014the same one she'd slammed\u2014stood open.'"
                    ),
                    "semicolon": (
                        "Join related clauses: "
                        "'She didn't answer; the question wasn't for her.'"
                    ),
                }
            else:
                instructions = {
                    "participial": (
                        "Too many ', Ving' phrases. Convert some to independent "
                        "clauses or action beats."
                    ),
                    "compound": (
                        "Too many ', and/but/yet' joins. Break some into "
                        "separate sentences for punch."
                    ),
                    "emdash": (
                        "Too many em-dashes. Replace some with commas, "
                        "parenthetical clauses, or sentence breaks."
                    ),
                    "semicolon": (
                        "Too many semicolons. Convert some to periods "
                        "or coordinating conjunctions."
                    ),
                }

            parts.append(
                f"{name.upper()}: {actual:.1f}% \u2192 target {target}% {score_str}. "
                f"{instructions.get(name, '')}"
            )

    # Short-sentence guidance (range-based, not dimension-scored)
    bl = baselines.get("short_pct", {})
    if bl:
        val = metrics.get("short_pct", 0.0)
        lo, hi = bl.get("range", [0, 100])
        if val > hi:
            parts.append(
                f"SHORT SENTENCES: {val:.1f}% (ceiling: {hi}%). "
                f"Too choppy. Combine adjacent shorts using constructions above."
            )
        elif val < lo:
            parts.append(
                f"SHORT SENTENCES: {val:.1f}% (floor: {lo}%). "
                f"Too dense. Break some long sentences for rhythm variety."
            )

    if not parts:
        return f"Borderline texture. Minor gaps: {'; '.join(reasons)}"

    return " | ".join(parts)
