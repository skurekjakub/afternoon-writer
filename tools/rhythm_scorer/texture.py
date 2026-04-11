"""Texture analysis helper functions."""

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


def texture_verdict(
    metrics: dict, baselines: dict,
) -> tuple[str, list[str]]:
    """Determine texture verdict and list specific gaps."""
    reasons = []

    for key in ("participial_pct", "compound_pct", "emdash_pct", "semicolon_pct", "texture_score"):
        if key in baselines:
            val = metrics[key]
            lo, hi = baselines[key]["range"]
            human = baselines[key]["human"]
            if val < lo:
                reasons.append(
                    f"{key} {val:.1f}% below floor {lo}% (human: {human}%)"
                )
            elif val > hi:
                reasons.append(
                    f"{key} {val:.1f}% above ceiling {hi}% (human: {human}%)"
                )

    if "short_pct" in baselines:
        val = metrics["short_pct"]
        lo, hi = baselines["short_pct"]["range"]
        human = baselines["short_pct"]["human"]
        if val > hi:
            reasons.append(
                f"short_pct {val:.1f}% above ceiling {hi}% -- telegram prose (human: {human}%)"
            )
        elif val < lo:
            reasons.append(
                f"short_pct {val:.1f}% below floor {lo}% -- over-connected (human: {human}%)"
            )

    if not reasons:
        return "within_target", reasons
    elif len(reasons) >= 3:
        return "below_target", reasons
    else:
        return "borderline", reasons


def texture_interpretation(
    metrics: dict, baselines: dict, verdict: str, reasons: list[str],
) -> str:
    """Build agent-readable interpretation with concrete fix instructions.

    This tells the consuming agent WHAT is wrong and HOW to fix it,
    with example constructions for each gap.
    """
    if verdict == "within_target":
        return "Texture within target range. No structural changes needed."

    parts = []

    bl = baselines.get("participial_pct", {})
    if bl and metrics["participial_pct"] < bl.get("range", [0])[0]:
        parts.append(
            f"PARTICIPIAL PHRASES: {metrics['participial_pct']:.1f}% "
            f"(floor: {bl['range'][0]}%, human: {bl['human']}%). "
            f"Add ', Ving' phrases to connect actions: "
            f"', turning back to the fire' / ', gripping the railing with both hands'. "
            f"These create connective tissue between actions."
        )

    bl = baselines.get("compound_pct", {})
    if bl and metrics["compound_pct"] < bl.get("range", [0])[0]:
        parts.append(
            f"COMPOUND CLAUSES: {metrics['compound_pct']:.1f}% "
            f"(floor: {bl['range'][0]}%, human: {bl['human']}%). "
            f"Join related ideas: ', and' / ', but' / ', yet'. "
            f"Adjacent short sentences often want combining."
        )

    bl = baselines.get("emdash_pct", {})
    if bl and metrics["emdash_pct"] < bl.get("range", [0])[0]:
        parts.append(
            f"EM-DASHES: {metrics['emdash_pct']:.1f}% "
            f"(floor: {bl['range'][0]}%, human: {bl['human']}%). "
            f"Use for mid-sentence pivots and asides: "
            f"'The door\u2014the same one she'd slammed that morning\u2014stood open.'"
        )

    bl = baselines.get("semicolon_pct", {})
    if bl and metrics["semicolon_pct"] < bl.get("range", [0])[0]:
        parts.append(
            f"SEMICOLONS: {metrics['semicolon_pct']:.1f}% "
            f"(floor: {bl['range'][0]}%, human: {bl['human']}%). "
            f"Join related clauses: "
            f"'She didn't answer; the question wasn't meant for her.'"
        )

    bl = baselines.get("short_pct", {})
    if bl and metrics["short_pct"] > bl.get("range", [0, 100])[1]:
        parts.append(
            f"SHORT SENTENCES: {metrics['short_pct']:.1f}% "
            f"(ceiling: {bl['range'][1]}%, human: {bl['human']}%). "
            f"Too choppy. Combine adjacent short sentences using the constructions above."
        )

    if not parts:
        return f"Borderline texture. Minor gaps: {'; '.join(reasons)}"

    return " | ".join(parts)
