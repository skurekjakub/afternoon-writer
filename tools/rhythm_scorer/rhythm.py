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
    """Moving Average Type-Token Ratio. Window size 50 is standard.

    Slides one window across the text with running counts, so it is O(n)
    rather than O(n * window). Each window's ratio is the same as the direct
    definition and they are summed the same way (sum() over the list, which
    is compensated since Python 3.12), so the result is bit-for-bit the same.
    """
    if len(words) < window:
        if not words:
            return 0.0
        return len(set(words)) / len(words)

    counts = Counter(words[:window])
    distinct = len(counts)
    ttrs = [distinct / window]
    for i in range(1, len(words) - window + 1):
        out_word = words[i - 1]
        counts[out_word] -= 1
        if counts[out_word] == 0:
            del counts[out_word]
            distinct -= 1
        in_word = words[i + window - 1]
        if in_word not in counts:
            distinct += 1
        counts[in_word] += 1
        ttrs.append(distinct / window)
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
