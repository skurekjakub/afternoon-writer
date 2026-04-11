"""Rhythm analysis helper functions."""

import math
import re
from collections import Counter


def count_punctuation(text: str) -> tuple[int, int]:
    """Count commas and sentence-ending punctuation."""
    commas = text.count(',')
    periods = len(re.findall(r'[.!?]+', text))
    return commas, max(periods, 1)


def word_count(sentence_text: str) -> int:
    """Count words in a sentence."""
    return len(re.findall(r'\S+', sentence_text))


def compute_mattr(words: list[str], window: int = 50) -> float:
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


def opener_stats(
    sentences: list[str],
) -> tuple[int, float, list[tuple[str, int]]]:
    """Analyze sentence opener (first word) distribution."""
    openers: list[str] = []
    for s in sentences:
        words = s.split()
        if words:
            w = words[0].strip('"\u201c\u201d\u2018\u2019').lower()
            if w:
                openers.append(w)

    if not openers:
        return 0, 0.0, []

    counts = Counter(openers)
    n = len(openers)
    distinct = len(counts)

    entropy = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            entropy -= p * math.log2(p)

    top = counts.most_common(5)
    return distinct, entropy, top
