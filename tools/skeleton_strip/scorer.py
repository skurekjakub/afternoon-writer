"""Concreteness scoring engine using Brysbaert psycholinguistic norms.

Loads ~40K word→concreteness mappings (1.0=abstract, 5.0=concrete) and
provides word-level and sentence-level scoring. No external deps — stdlib only.

Function words (articles, prepositions, pronouns, auxiliaries, conjunctions)
are excluded from scoring because they dominate every sentence at ~1.0 concreteness
and drown out the content-word signal. The ratio measures content words only.
"""

import csv
import os
import re
from dataclasses import dataclass, field

# --- Thresholds (calibratable) ---
CONCRETE_THRESHOLD = 4.0   # words scoring >= this are "concrete"
ABSTRACT_THRESHOLD = 2.5   # words scoring <= this are "abstract"

# Default path to norms CSV
_DEFAULT_NORMS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "concreteness_norms.csv"
)

# Simple tokenizer regex: word characters, contractions, possessives
_TOKEN_RE = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)?")

# Function words excluded from concreteness scoring.
# These have Brysbaert scores (~1.0-1.5) but carry no imageable content.
_FUNCTION_WORDS = frozenset({
    # articles / determiners
    "a", "an", "the", "this", "that", "these", "those", "some", "any",
    "each", "every", "no", "all", "both", "few", "many", "much", "most",
    "other", "another", "such",
    # pronouns
    "i", "me", "my", "mine", "myself",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves",
    "who", "whom", "whose", "which", "what", "that",
    "one", "ones",
    # prepositions
    "in", "on", "at", "to", "for", "of", "with", "by", "from",
    "into", "onto", "upon", "about", "above", "across", "after",
    "against", "along", "among", "around", "before", "behind",
    "below", "beneath", "beside", "between", "beyond", "down",
    "during", "except", "inside", "near", "off", "out",
    "outside", "over", "past", "since", "through", "throughout",
    "toward", "towards", "under", "underneath", "until", "up",
    "within", "without",
    # conjunctions
    "and", "but", "or", "nor", "so", "yet", "for", "because",
    "although", "though", "while", "whereas", "whether", "if",
    "unless", "than", "as",
    # auxiliaries / modals
    "be", "am", "is", "are", "was", "were", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did",
    "will", "would", "shall", "should",
    "can", "could", "may", "might", "must",
    # common adverbs / particles that are functional
    "not", "just", "also", "too", "very", "quite", "rather",
    "then", "now", "here", "there", "when", "where", "how", "why",
    "still", "already", "even", "only", "ever",
    # misc functional
    "like", "well", "way",
})


@dataclass
class SentenceScore:
    text: str
    tokens: list[str]
    content_tokens: list[tuple[str, float]]  # content words with scores
    function_tokens: list[str]               # excluded function words
    unscored_tokens: list[str]               # not in norms at all
    concrete_words: list[str]
    abstract_words: list[str]
    mean_concreteness: float | None          # mean over content words only
    concrete_ratio: float                    # concrete / content words
    abstract_ratio: float                    # abstract / content words


def load_norms(path: str | None = None) -> dict[str, float]:
    """Load Brysbaert norms CSV into {word_lower: concreteness_mean} dict."""
    path = path or _DEFAULT_NORMS_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Norms not found at {path}. Run download_norms.py first."
        )

    norms: dict[str, float] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            word = row["Word"].strip().lower()
            try:
                score = float(row["Conc.M"])
            except (ValueError, KeyError):
                continue
            norms[word] = score
    return norms


def tokenize(text: str) -> list[str]:
    """Extract word tokens from text. Lowercase, no punctuation."""
    return [m.group().lower() for m in _TOKEN_RE.finditer(text)]


def is_function_word(word: str) -> bool:
    """Check if a word is a function word (excluded from scoring)."""
    return word.lower() in _FUNCTION_WORDS


def score_word(word: str, norms: dict[str, float]) -> float | None:
    """Look up a word's concreteness score. Returns None if not in norms."""
    return norms.get(word.lower())


def score_sentence(text: str, norms: dict[str, float]) -> SentenceScore:
    """Score a sentence for concreteness.

    Function words are excluded from scoring. The concrete_ratio measures
    the proportion of content words (nouns, verbs, adjectives, abstract nouns)
    that are concrete vs. total content words scored.
    """
    tokens = tokenize(text)
    content: list[tuple[str, float]] = []
    function: list[str] = []
    unscored: list[str] = []
    concrete: list[str] = []
    abstract: list[str] = []

    for tok in tokens:
        if is_function_word(tok):
            function.append(tok)
            continue
        s = norms.get(tok)
        if s is not None:
            content.append((tok, s))
            if s >= CONCRETE_THRESHOLD:
                concrete.append(tok)
            elif s <= ABSTRACT_THRESHOLD:
                abstract.append(tok)
        else:
            unscored.append(tok)

    n_content = len(content)
    mean = (sum(s for _, s in content) / n_content) if n_content > 0 else None
    c_ratio = len(concrete) / n_content if n_content > 0 else 0.0
    a_ratio = len(abstract) / n_content if n_content > 0 else 0.0

    return SentenceScore(
        text=text,
        tokens=tokens,
        content_tokens=content,
        function_tokens=function,
        unscored_tokens=unscored,
        concrete_words=concrete,
        abstract_words=abstract,
        mean_concreteness=mean,
        concrete_ratio=c_ratio,
        abstract_ratio=a_ratio,
    )
