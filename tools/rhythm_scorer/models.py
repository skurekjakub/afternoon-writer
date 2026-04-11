"""Data models for rhythm and texture analysis."""

from dataclasses import dataclass, field


@dataclass
class RhythmReport:
    """Combined rhythm + texture analysis report."""

    # --- Rhythm ---
    commas: int
    periods: int
    cp_ratio: float

    sentence_count: int
    mean_sentence_length: float
    stdev_sentence_length: float
    cv_sentence_length: float       # coefficient of variation
    short_sentence_pct: float       # sentences <=6 words (rhythm threshold)
    long_sentence_pct: float        # sentences >=20 words

    opener_count: int               # distinct first words
    opener_entropy: float           # Shannon entropy of first-word distribution
    top_openers: list[tuple[str, int]]

    paragraph_count: int
    mean_paragraph_sentences: float
    stdev_paragraph_sentences: float
    one_sentence_paragraph_pct: float

    mattr: float
    unique_words: int
    total_words: int

    # --- Texture ---
    participial_pct: float = 0.0    # % sentences with ', Ving' phrase
    compound_pct: float = 0.0       # % sentences with ', and/but/or/yet/so'
    emdash_pct: float = 0.0         # % sentences with em-dash
    semicolon_pct: float = 0.0      # % sentences with semicolon
    texture_short_pct: float = 0.0  # % sentences <=8 words (texture threshold)
    texture_score: float = 0.0      # combined joining-construction %
    texture_verdict: str = ""       # within_target / borderline / below_target
    texture_verdict_reasons: list[str] = field(default_factory=list)
    texture_flagged: list[dict] = field(default_factory=list)
    texture_baselines: dict = field(default_factory=dict)
