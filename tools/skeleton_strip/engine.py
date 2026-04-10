"""Skeleton strip analysis engine.

Combines concreteness scoring (scorer.py) and pattern matching (patterns.py)
into document-level analysis with per-sentence and per-paragraph verdicts.
"""

from dataclasses import dataclass, field

from .scorer import (
    SentenceScore, score_sentence, CONCRETE_THRESHOLD, ABSTRACT_THRESHOLD,
)
from .patterns import PatternMatch, find_patterns
from .splitter import Sentence, Paragraph, split_paragraphs


@dataclass
class SentenceAnalysis:
    sentence: Sentence
    word_score: SentenceScore
    pattern_matches: list[PatternMatch]
    skeleton_words: list[str]       # concrete + neutral words that survived
    stripped_words: list[str]       # abstract words removed
    density: float                  # concrete_ratio from word_score
    verdict: str                    # "concrete", "mixed", "abstract"


@dataclass
class ParagraphAnalysis:
    paragraph: Paragraph
    sentences: list[SentenceAnalysis]
    mean_density: float
    abstract_sentence_count: int
    concrete_sentence_count: int
    total_pattern_matches: int
    verdict: str                    # "grounded", "drifting", "abstract"


@dataclass
class FlaggedZone:
    paragraph_indices: list[int]
    reason: str
    mean_density: float
    pattern_count: int


@dataclass
class DocumentAnalysis:
    paragraphs: list[ParagraphAnalysis]
    total_sentences: int
    abstract_sentences: int
    concrete_sentences: int
    total_pattern_matches: int
    mean_density: float
    flagged_zones: list[FlaggedZone]
    overall_verdict: str


def _sentence_verdict(
    density: float, pattern_count: int, content_word_count: int,
) -> str:
    """Classify a sentence as concrete, mixed, abstract, or short.

    Calibrated against Sanderson (Way of Kings) distribution:
      p25=0.00, p50=0.27, p75=0.50
    Sentences with fewer than 3 content words can't be meaningfully classified.
    """
    # Too few content words to classify
    if content_word_count < 3:
        if pattern_count >= 1:
            return "abstract"
        return "short"
    if pattern_count >= 2:
        return "abstract"
    if density >= 0.35 and pattern_count == 0:
        return "concrete"
    if density >= 0.10:
        return "mixed"
    # Below 0.10 with enough content words — genuinely abstract
    return "abstract"


def _paragraph_verdict(
    mean_density: float, abstract_pct: float, pattern_density: float,
) -> str:
    """Classify a paragraph as grounded, drifting, or abstract.

    Calibrated: Sanderson paragraphs average ~0.30 mean density.
    """
    if mean_density >= 0.25 and abstract_pct <= 0.5 and pattern_density < 1.0:
        return "grounded"
    if mean_density >= 0.15 or abstract_pct <= 0.6:
        return "drifting"
    return "abstract"


def analyze_sentence(
    sentence: Sentence, norms: dict[str, float]
) -> SentenceAnalysis:
    """Analyze a single sentence for concreteness and patterns."""
    ws = score_sentence(sentence.text, norms)
    pms = find_patterns(sentence.text)

    # Build skeleton: keep concrete + neutral words, strip abstract
    skeleton: list[str] = []
    stripped: list[str] = []
    for tok, score in ws.content_tokens:
        if score >= ABSTRACT_THRESHOLD:
            skeleton.append(tok)
        else:
            stripped.append(tok)
    # Unscored words (names, domain-specific) are structural — keep them
    skeleton.extend(ws.unscored_tokens)

    verdict = _sentence_verdict(ws.concrete_ratio, len(pms), len(ws.content_tokens))

    return SentenceAnalysis(
        sentence=sentence,
        word_score=ws,
        pattern_matches=pms,
        skeleton_words=skeleton,
        stripped_words=stripped,
        density=ws.concrete_ratio,
        verdict=verdict,
    )


def analyze_paragraph(
    paragraph: Paragraph, norms: dict[str, float]
) -> ParagraphAnalysis:
    """Analyze a paragraph: score all sentences, aggregate."""
    analyses = [analyze_sentence(s, norms) for s in paragraph.sentences]

    if not analyses:
        return ParagraphAnalysis(
            paragraph=paragraph,
            sentences=[],
            mean_density=0.0,
            abstract_sentence_count=0,
            concrete_sentence_count=0,
            total_pattern_matches=0,
            verdict="abstract",
        )

    n = len(analyses)
    concrete_count = sum(1 for a in analyses if a.verdict == "concrete")
    abstract_count = sum(1 for a in analyses if a.verdict == "abstract")
    pattern_total = sum(len(a.pattern_matches) for a in analyses)
    densities = [a.density for a in analyses]
    mean_d = sum(densities) / n if n > 0 else 0.0

    concrete_pct = concrete_count / n if n > 0 else 0.0
    abstract_pct = abstract_count / n if n > 0 else 0.0
    pattern_density = pattern_total / n if n > 0 else 0.0
    verdict = _paragraph_verdict(mean_d, abstract_pct, pattern_density)

    return ParagraphAnalysis(
        paragraph=paragraph,
        sentences=analyses,
        mean_density=mean_d,
        abstract_sentence_count=abstract_count,
        concrete_sentence_count=concrete_count,
        total_pattern_matches=pattern_total,
        verdict=verdict,
    )


def analyze_document(text: str, norms: dict[str, float]) -> DocumentAnalysis:
    """Full document analysis: paragraphs, flagged zones, overall verdict."""
    paragraphs = split_paragraphs(text)
    para_analyses = [analyze_paragraph(p, norms) for p in paragraphs]

    total_sent = sum(len(pa.sentences) for pa in para_analyses)
    abstract_sent = sum(pa.abstract_sentence_count for pa in para_analyses)
    concrete_sent = sum(pa.concrete_sentence_count for pa in para_analyses)
    total_patterns = sum(pa.total_pattern_matches for pa in para_analyses)
    densities = [pa.mean_density for pa in para_analyses if pa.sentences]
    mean_d = sum(densities) / len(densities) if densities else 0.0

    # Find flagged zones: consecutive abstract paragraphs OR low-density clusters.
    # Drifting paragraphs are normal in fiction (dialogue, transitions).
    # Only "abstract" paragraphs form zones. A single drifting paragraph adjacent
    # to abstract ones is absorbed into the zone, but drifting-only runs don't flag.
    flagged: list[FlaggedZone] = []
    zone_indices: list[int] = []
    has_abstract_in_zone = False

    for pa in para_analyses:
        if pa.verdict == "abstract":
            zone_indices.append(pa.paragraph.index)
            has_abstract_in_zone = True
        elif pa.verdict == "drifting" and has_abstract_in_zone:
            # Absorb drifting into an active abstract zone
            zone_indices.append(pa.paragraph.index)
        else:
            if zone_indices and has_abstract_in_zone:
                zone_pas = [pa2 for pa2 in para_analyses if pa2.paragraph.index in zone_indices]
                abstract_in_zone = sum(1 for z in zone_pas if z.verdict == "abstract")
                flagged.append(FlaggedZone(
                    paragraph_indices=list(zone_indices),
                    reason=f"{abstract_in_zone} abstract + {len(zone_indices) - abstract_in_zone} drifting paragraph(s)",
                    mean_density=sum(z.mean_density for z in zone_pas) / len(zone_pas),
                    pattern_count=sum(z.total_pattern_matches for z in zone_pas),
                ))
            zone_indices = []
            has_abstract_in_zone = False

    # Close final zone
    if zone_indices and has_abstract_in_zone:
        zone_pas = [pa2 for pa2 in para_analyses if pa2.paragraph.index in zone_indices]
        abstract_in_zone = sum(1 for z in zone_pas if z.verdict == "abstract")
        flagged.append(FlaggedZone(
            paragraph_indices=list(zone_indices),
            reason=f"{abstract_in_zone} abstract + {len(zone_indices) - abstract_in_zone} drifting paragraph(s)",
            mean_density=sum(z.mean_density for z in zone_pas) / len(zone_pas),
            pattern_count=sum(z.total_pattern_matches for z in zone_pas),
        ))

    # Also flag pattern-heavy paragraphs (regardless of density)
    flagged_set = {idx for fz in flagged for idx in fz.paragraph_indices}
    for pa in para_analyses:
        if pa.total_pattern_matches >= 2 and pa.paragraph.index not in flagged_set:
            flagged.append(FlaggedZone(
                paragraph_indices=[pa.paragraph.index],
                reason=f"pattern-heavy ({pa.total_pattern_matches} matches)",
                mean_density=pa.mean_density,
                pattern_count=pa.total_pattern_matches,
            ))

    flagged.sort(key=lambda fz: fz.paragraph_indices[0])

    # Overall verdict — zone-based, not percentage-based.
    # Published fiction (Sanderson) has ~30% abstract sentences by count,
    # but those are spread evenly (short dialogue, transitions). What matters
    # is whether abstract sentences cluster into long ungrounded zones.
    n_para = len(para_analyses)
    if total_sent == 0:
        overall = "empty"
    else:
        # Count paragraphs in long flagged zones (3+ consecutive paragraphs)
        long_zone_paras = sum(
            len(fz.paragraph_indices) for fz in flagged
            if len(fz.paragraph_indices) >= 3
        )
        long_zone_pct = long_zone_paras / n_para if n_para > 0 else 0.0
        if long_zone_pct <= 0.05 and total_patterns <= 3:
            overall = "grounded"
        elif long_zone_pct <= 0.15:
            overall = "mixed"
        else:
            overall = "abstract"

    return DocumentAnalysis(
        paragraphs=para_analyses,
        total_sentences=total_sent,
        abstract_sentences=abstract_sent,
        concrete_sentences=concrete_sent,
        total_pattern_matches=total_patterns,
        mean_density=mean_d,
        flagged_zones=flagged,
        overall_verdict=overall,
    )
