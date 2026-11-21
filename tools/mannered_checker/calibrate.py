"""Calibrate the mannered checker and the rhythm/texture baselines from human reference prose.

Reference corpora come from `.afternoon/config.json -> priming.humanCorpora`, a list of files
or directories (every .md/.txt inside a directory is read), each with an optional weight. Each
corpus is measured on its own and the blend is the weighted mean across corpora, so corpus size
doesn't decide the blend: a 50K-word sample at weight 2 counts twice as much as a 380K-word novel
at weight 1. LitRPG furniture ([Skill] brackets, level-up lines) is stripped before measuring.

Writes:
  - tools/mannered_checker/calibration.json — per-corpus and blended rates for every mannered
    pattern, polysyndeton density and the rhythm/texture metrics, plus a fingerprint of the
    corpora. check.py reads it to set caps, and recalibrates on its own when the fingerprint no
    longer matches (a sample added, removed or edited).
  - .afternoon/style-guide.json — rhythmMetrics.global and textureMetrics are re-anchored on the
    blend. Each metric keeps its hand-set offset: new target = blend + (old target - old human),
    and the range moves the same way. Re-running with unchanged corpora changes nothing.

Usage:
    python3 tools/mannered_checker/calibrate.py
    python3 tools/mannered_checker/calibrate.py --no-style-guide
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.mannered_checker import check as mc  # noqa: E402
from tools.rhythm_scorer.analyze import analyze_rhythm  # noqa: E402
from tools.rhythm_scorer.formatters import format_json  # noqa: E402

CALIBRATION_PATH = os.path.join(os.path.dirname(__file__), "calibration.json")
CONFIG_PATH = os.path.join(REPO_ROOT, ".afternoon", "config.json")
STYLE_GUIDE_PATH = os.path.join(REPO_ROOT, ".afternoon", "style-guide.json")
DEFAULT_CORPORA = ["style-samples/travel.md"]

# style-guide.json rhythmMetrics.global key -> rhythm_scorer JSON path
RHYTHM_KEYS = {
    "comma_period_ratio": ("comma_period_ratio",),
    "sentence_length_mean": ("sentence", "mean_length"),
    "sentence_length_cv": ("sentence", "cv_length"),
    "short_sentence_pct": ("sentence", "short_pct"),
    "long_sentence_pct": ("sentence", "long_pct"),
    "opener_entropy": ("openers", "entropy"),
    "one_sentence_paragraph_pct": ("paragraph", "one_sentence_pct"),
    "mattr": ("vocabulary", "mattr"),
}
TEXTURE_KEYS = ["participial_pct", "compound_pct", "emdash_pct", "semicolon_pct", "short_pct"]


# ---------------------------------------------------------------------------
# Corpora
# ---------------------------------------------------------------------------

def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write_json_atomic(path, data):
    """Write to a temp file and rename it over the target, so a pipeline agent reading the
    file at the same moment sees the old version or the new one, never half of one."""
    tmp = f"{path}.{os.getpid()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def corpus_specs():
    """[(path, weight)] from priming.humanCorpora. Entries are a path or {"path": ..., "weight": ...}."""
    try:
        cfg = _load_json(CONFIG_PATH)
        entries = cfg.get("priming", {}).get("humanCorpora") or DEFAULT_CORPORA
    except (OSError, ValueError):
        entries = DEFAULT_CORPORA
    specs = []
    for e in entries:
        path, weight = (e, 1.0) if isinstance(e, str) else (e.get("path"), float(e.get("weight", 1.0)))
        if path and weight > 0 and os.path.exists(os.path.join(REPO_ROOT, path)):
            specs.append((path, weight))
    return specs


def corpus_paths():
    return [p for p, _ in corpus_specs()]


def corpus_files(path):
    full = os.path.join(REPO_ROOT, path)
    if os.path.isdir(full):
        return sorted(os.path.join(full, f) for f in os.listdir(full) if f.endswith((".md", ".txt")))
    return [full]


# Genre furniture that should never be measured as prose rhythm: LitRPG skill calls,
# system screens and level-ups. A paragraph that is only skill calls is dropped, and
# inline [Skill Name] brackets keep the name and lose the brackets.
SKILL_ONLY_PARA = re.compile(r'^\s*["“]?(?:\[[^\]\n]+\]\.?\s*)+["”]?\s*$')
SYSTEM_LINE = re.compile(r"^\s*(?:\*{3}|Level Up!|You are now (?:a )?level\b.*|\[[^\]\n]+\])\s*$", re.IGNORECASE)
INLINE_SKILL = re.compile(r"\[([^\]\n]{1,40})\]")


def strip_genre_furniture(text):
    paras = re.split(r"\n\s*\n", text)
    kept = []
    for para in paras:
        if SKILL_ONLY_PARA.match(para):
            continue
        lines = [ln for ln in para.split("\n") if not SYSTEM_LINE.match(ln)]
        if any(ln.strip() for ln in lines):
            kept.append(INLINE_SKILL.sub(r"\1", "\n".join(lines)))
    return "\n\n".join(kept)


def read_corpus(path):
    parts = [mc.read_text(f) for f in corpus_files(path)]
    return strip_genre_furniture(mc.normalise_quotes(mc.strip_headers("\n\n".join(parts))))


def fingerprint(specs=None):
    """Identity of the corpora as configured: paths, weights, and each file's size and mtime."""
    specs = corpus_specs() if specs is None else specs
    out = []
    for p, w in specs:
        out.append([p, w])
        for f in corpus_files(p):
            st = os.stat(f)
            out.append([os.path.relpath(f, REPO_ROOT), st.st_size, int(st.st_mtime)])
    return out


def checker_hash():
    """Changes whenever a detector or the shared text helpers change, so edits trigger recalibration."""
    from tools.prose_core import text as core_text

    h = hashlib.sha1()
    for path in (mc.__file__, core_text.__file__):
        with open(path, "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:12]


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def _dig(d, keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


CHUNK_WORDS = 12000  # about one chapter; rhythm metrics like opener entropy grow with text length


def chapter_chunks(text):
    """Split a large corpus into chapter-sized chunks on paragraph boundaries."""
    chunks, current, count = [], [], 0
    for para in re.split(r"\n\s*\n", text):
        current.append(para)
        count += len(para.split())
        if count >= CHUNK_WORDS:
            chunks.append("\n\n".join(current))
            current, count = [], 0
    if current and (count >= CHUNK_WORDS / 2 or not chunks):
        chunks.append("\n\n".join(current))
    return chunks


def rhythm_of(text):
    rhythm_json = json.loads(format_json(analyze_rhythm(text), "corpus"))
    rhythm = {k: _dig(rhythm_json, path) for k, path in RHYTHM_KEYS.items()}
    texture = {k: _dig(rhythm_json, ("texture", k)) for k in TEXTURE_KEYS}
    return rhythm, texture


def measure(text):
    """Pattern rates over the whole corpus; rhythm and texture as the mean over chapter-sized chunks,
    so a 380K-word novel and a 10K-word sample are measured at the scale a chapter is scored at."""
    words = len(text.split())
    per = 10000 / words if words else 0
    patterns, poly, _ = mc.run_patterns(text, None)
    rates = {p["name"]: round(p["count"] * per, 3) for p in patterns}
    parts = [rhythm_of(c) for c in chapter_chunks(text)]
    rhythm = {k: _mean((r.get(k), 1.0) for r, _ in parts) for k in RHYTHM_KEYS}
    texture = {k: _mean((t.get(k), 1.0) for _, t in parts) for k in TEXTURE_KEYS}
    return {"words": words, "chunks": len(parts), "patternsPer10k": rates, "polysyndetonPer10k": poly["per10k"],
            "rhythm": rhythm, "texture": texture}


def _mean(pairs):
    """Weighted mean of (value, weight) pairs, skipping missing values."""
    pairs = [(v, w) for v, w in pairs if isinstance(v, (int, float))]
    total = sum(w for _, w in pairs)
    return round(sum(v * w for v, w in pairs) / total, 3) if total else None


def blend(measured, weights):
    names = sorted({n for m in measured for n in m["patternsPer10k"]})
    mw = list(zip(measured, weights))
    return {
        "patternsPer10k": {n: _mean((m["patternsPer10k"].get(n, 0.0), w) for m, w in mw) for n in names},
        "polysyndetonPer10k": _mean((m["polysyndetonPer10k"], w) for m, w in mw),
        "rhythm": {k: _mean((m["rhythm"].get(k), w) for m, w in mw) for k in RHYTHM_KEYS},
        "texture": {k: _mean((m["texture"].get(k), w) for m, w in mw) for k in TEXTURE_KEYS},
    }


# ---------------------------------------------------------------------------
# style-guide.json
# ---------------------------------------------------------------------------

def _reanchor(entry, anchor_key, new_anchor):
    """Move an entry's anchor to new_anchor, keeping its target and range offsets."""
    old = entry.get(anchor_key)
    if not isinstance(old, (int, float)) or new_anchor is None:
        return False
    shift = new_anchor - old
    if abs(shift) < 1e-9:
        return False
    entry[anchor_key] = round(new_anchor, 3)
    if isinstance(entry.get("target"), (int, float)):
        entry["target"] = round(entry["target"] + shift, 3)
    if isinstance(entry.get("range"), list) and len(entry["range"]) == 2:
        entry["range"] = [round(entry["range"][0] + shift, 3), round(entry["range"][1] + shift, 3)]
    return True


def style_guide_drifted(blended) -> bool:
    """True when style-guide.json's anchors no longer match the calibration blend."""
    if not os.path.exists(STYLE_GUIDE_PATH):
        return False
    try:
        guide = _load_json(STYLE_GUIDE_PATH)
    except ValueError:
        return False
    rg = guide.get("rhythmMetrics", {}).get("global", {})
    tm = guide.get("textureMetrics", {})
    pairs = [(rg.get(k, {}).get("measured"), blended["rhythm"].get(k)) for k in RHYTHM_KEYS if k in rg]
    pairs += [(tm.get(k, {}).get("human"), blended["texture"].get(k)) for k in TEXTURE_KEYS if k in tm]
    return any(isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) > 1e-6 for a, b in pairs)


def sync_style_guide(blended, paths, per_corpus, weights=None):
    if not os.path.exists(STYLE_GUIDE_PATH):
        return []
    guide = _load_json(STYLE_GUIDE_PATH)
    changed = []
    weights = weights or [1.0] * len(paths)
    sources = " + ".join(f"{p} (weight {w:g})" for p, w in zip(paths, weights))
    rg = guide.get("rhythmMetrics", {}).get("global", {})
    for key in RHYTHM_KEYS:
        if key in rg and _reanchor(rg[key], "measured", blended["rhythm"].get(key)):
            changed.append(f"rhythmMetrics.global.{key}")
    tm = guide.get("textureMetrics", {})
    for key in TEXTURE_KEYS:
        if key in tm and _reanchor(tm[key], "human", blended["texture"].get(key)):
            changed.append(f"textureMetrics.{key}")
    if "rhythmMetrics" in guide:
        guide["rhythmMetrics"]["source"] = f"weighted blend of {sources}, via tools/mannered_checker/calibrate.py"
    if "textureMetrics" in guide:
        guide["textureMetrics"]["source"] = f"weighted blend of {sources}, via tools/mannered_checker/calibrate.py"
        guide["textureMetrics"]["perCorpus"] = {p: m["texture"] for p, m in zip(paths, per_corpus)}
    if "rhythmMetrics" in guide:
        guide["rhythmMetrics"]["perCorpus"] = {p: m["rhythm"] for p, m in zip(paths, per_corpus)}
    _write_json_atomic(STYLE_GUIDE_PATH, guide)
    return changed


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

def calibrate(update_style_guide=True, quiet=False):
    specs = corpus_specs()
    if not specs:
        raise SystemExit("no reference corpora found; set priming.humanCorpora in .afternoon/config.json")
    paths = [p for p, _ in specs]
    weights = [w for _, w in specs]
    per_corpus = [measure(read_corpus(p)) for p in paths]
    blended = blend(per_corpus, weights)
    data = {
        "_doc": "Generated by tools/mannered_checker/calibrate.py. Do not hand-edit; add samples to priming.humanCorpora and re-run.",
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "headroom": mc.HEADROOM,
        "zeroRelease": mc.ZERO_RELEASE,
        "fingerprint": fingerprint(specs),
        "checkerHash": checker_hash(),
        "corpora": [{"path": p, "weight": w, **m} for (p, w), m in zip(specs, per_corpus)],
        "blend": blended,
    }
    _write_json_atomic(CALIBRATION_PATH, data)
    changed = sync_style_guide(blended, paths, per_corpus, weights) if update_style_guide else []
    if not quiet:
        print(f"calibrated from {len(paths)} corpora: " + ", ".join(f"{p} ({m['words']} words, weight {w:g})" for p, w, m in zip(paths, weights, per_corpus)))
        print(f"  wrote {os.path.relpath(CALIBRATION_PATH, REPO_ROOT)}")
        if update_style_guide:
            print(f"  style-guide.json: {len(changed)} metrics re-anchored" + (f" ({', '.join(changed)})" if changed else ""))
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-style-guide", action="store_true", help="only write calibration.json")
    args = ap.parse_args()
    data = calibrate(update_style_guide=not args.no_style_guide)
    b = data["blend"]
    rows = [("polysyndeton/10k", [c["polysyndetonPer10k"] for c in data["corpora"]], b["polysyndetonPer10k"])]
    rows += [(f"texture.{k}", [c["texture"][k] for c in data["corpora"]], b["texture"][k]) for k in TEXTURE_KEYS]
    rows += [(f"rhythm.{k}", [c["rhythm"][k] for c in data["corpora"]], b["rhythm"][k]) for k in RHYTHM_KEYS]
    names = sorted(b["patternsPer10k"])
    rows += [(f"{n}/10k", [c["patternsPer10k"].get(n, 0) for c in data["corpora"]], b["patternsPer10k"][n]) for n in names]
    header = " | ".join(os.path.basename(c["path"].rstrip("/")) for c in data["corpora"])
    print(f"\n{'metric':34s} {header} | blend")
    for name, vals, bl in rows:
        print(f"{name:34s} " + " | ".join(f"{v if v is not None else '-':>8}" for v in vals) + f" | {bl}")


if __name__ == "__main__":
    main()
