"""Shared constants for rhythm and texture analysis."""

import re

# ---------------------------------------------------------------------------
# Texture detection regexes (validated against 384K words human prose)
# ---------------------------------------------------------------------------

# Participial: comma followed by word ending in -ing
#   ", turning back", ", gripping the rail", ", watching him go"
PARTICIPIAL_RE = re.compile(r',\s+\w+ing\b')

# Compound: comma followed by coordinating conjunction
#   ", and she", ", but the", ", or they", ", yet he", ", so we"
COMPOUND_RE = re.compile(r',\s+(?:and|but|or|yet|so)\s+')

# Em-dash (unicode or double-hyphen)
EMDASH_RE = re.compile(r'\u2014|--')

# Semicolon
SEMICOLON_RE = re.compile(r';')

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

SHORT_THRESHOLD = 8       # texture short-sentence threshold (words)
TELEGRAM_WINDOW = 8       # sliding window for telegram-run detection
TELEGRAM_SHORT_PCT = 0.75 # short-sentence ratio to flag window
DESERT_MIN_SENTENCES = 15 # min zero-texture consecutive sentences to flag

# ---------------------------------------------------------------------------
# Calibrated texture baselines -- Sanderson Way of Kings (384K words)
# vs 24 pipeline v4b chapters.
#
# Measured with prose-aware sentence splitter (handles hard-wrapped text).
# Ranges: editorial judgment of acceptable variance.
# Override via --baselines flag or style-guide.json textureMetrics.
# ---------------------------------------------------------------------------

DEFAULT_TEXTURE_BASELINES = {
    "participial_pct": {"human": 11.0, "target": 8.0, "range": [5.0, 15.0]},
    "compound_pct": {"human": 8.5, "target": 6.0, "range": [4.0, 12.0]},
    "emdash_pct": {"human": 3.5, "target": 2.5, "range": [1.0, 5.0]},
    "semicolon_pct": {"human": 1.4, "target": 0.8, "range": [0.3, 2.5]},
    "short_pct": {"human": 52.2, "target": 52.0, "range": [38.0, 62.0]},
    "texture_score": {"human": 24.4, "target": 17.0, "range": [10.0, 30.0]},
}
