# Phase 1: Foundation — Concreteness Dataset & Scoring Engine

**Version**: v1
**Goal**: Download the Brysbaert concreteness norms and build a Python module that scores individual words on a 1-5 abstract→concrete scale.
**Dependencies**: None (entry phase)
**Outputs consumed by**: Phase 2 (strip algorithm), Phase 3 (CLI tool)

---

## Context

The Brysbaert et al. (2014) concreteness norms rate ~40,000 English words on a 1-5 scale where 1 = maximally abstract ("justice", "theory") and 5 = maximally concrete ("jaw", "coffee", "floor"). This is the empirical backbone of the skeleton strip — it lets us mechanically classify words as concrete or abstract without relying on an LLM's judgment (which shares the same bias we're trying to detect).

The dataset lives on HuggingFace as a CSV: `StephanAkkerman/concreteness-ratings`. Columns: `Word`, `Conc.M` (mean rating), `Conc.SD`, `Unknown`, `Total`, `Percent_known`, `SUBTLEX`, `Dom_Pos`.

We only need `Word` and `Conc.M`. The rest is metadata for psycholinguistic research.

---

## Tasks

### 1.1 — Install Python dependencies

**New files**: `tools/skeleton-strip/requirements.txt`

We need minimal dependencies — no heavy NLP frameworks. The scoring engine is a dictionary lookup, not a model.

**Dependencies**:
- `pandas` — for loading and querying the CSV efficiently
- No spacy, no nltk, no transformers. Simple tokenization via regex is sufficient for word-level lookup.

```
pandas>=2.0
```

**Acceptance Criteria**:
- [ ] `requirements.txt` exists at `tools/skeleton-strip/requirements.txt`
- [ ] `pip install -r tools/skeleton-strip/requirements.txt` succeeds
- [ ] `python3 -c "import pandas"` succeeds after install

### 1.2 — Download and cache the Brysbaert norms

**New file**: `tools/skeleton-strip/download_norms.py`
**New artifact**: `tools/skeleton-strip/data/concreteness_norms.csv`

A one-time download script that fetches the CSV from HuggingFace and caches it locally. Subsequent runs skip the download if the file exists.

**Changes**:

1. **Download script**: Fetch the raw CSV from HuggingFace:
   ```
   https://huggingface.co/datasets/StephanAkkerman/concreteness-ratings/resolve/main/concreteness_ratings.csv
   ```
   Save to `tools/skeleton-strip/data/concreteness_norms.csv`.

2. **Verification**: After download, load with pandas and verify:
   - Column `Word` exists
   - Column `Conc.M` exists
   - At least 39,000 rows (original dataset has ~40K)
   - Print summary: row count, mean concreteness, a few sample entries

3. **Idempotency**: If `data/concreteness_norms.csv` already exists and has >39K rows, print "Already downloaded" and exit.

**Edge cases**:
- Network failure → print clear error, exit 1
- Corrupt/partial download → delete partial file, exit 1
- HuggingFace URL changes → easy to update one string

**Acceptance Criteria**:
- [ ] Running `python3 tools/skeleton-strip/download_norms.py` produces `tools/skeleton-strip/data/concreteness_norms.csv`
- [ ] CSV has columns `Word` and `Conc.M`
- [ ] CSV has ≥39,000 rows
- [ ] Running the script again prints "Already downloaded" and exits cleanly

### 1.3 — Build the word-level scoring module

**New file**: `tools/skeleton-strip/scorer.py`

The core scoring engine. Loads the Brysbaert norms into a dictionary and provides functions to score words and tokenize text.

**Changes**:

1. **`load_norms(path)` → dict[str, float]**: Load CSV, build `{word_lower: conc_m}` dict. Normalize all keys to lowercase. ~40K entries fits easily in memory.

2. **`tokenize(text)` → list[str]**: Simple regex tokenizer. Split on whitespace and punctuation, lowercase, strip possessives ('s), strip leading/trailing punctuation. No lemmatization needed — the Brysbaert norms already contain common inflected forms. Return list of tokens.

3. **`score_word(word, norms)` → float | None**: Look up a single word in the norms dict. Return the concreteness score (1.0-5.0) or `None` if not found. Function words (the, a, is, was, etc.) won't be in the norms — that's fine, they're neither concrete nor abstract, they're structural.

4. **`score_sentence(text, norms)` → SentenceScore`**: Tokenize the sentence. Look up each token. Return a dataclass/namedtuple:
   ```python
   @dataclass
   class SentenceScore:
       text: str                          # original sentence
       tokens: list[str]                  # all tokens
       scored_tokens: list[tuple[str, float]]  # (word, score) for found words
       unscored_tokens: list[str]         # words not in norms
       concrete_words: list[str]          # score >= 4.0
       abstract_words: list[str]          # score <= 2.5
       mean_concreteness: float | None    # mean of scored tokens, or None if no tokens scored
       concrete_ratio: float              # len(concrete) / len(scored) or 0.0
   ```

5. **Thresholds** (constants at module top):
   ```python
   CONCRETE_THRESHOLD = 4.0   # words scoring >= this are "concrete"
   ABSTRACT_THRESHOLD = 2.5   # words scoring <= this are "abstract"
   ```
   These are calibratable. 4.0 is conservative — "hand" (4.7), "coffee" (4.9), "floor" (4.8) all clear it. "Feeling" (2.2), "deliberation" (1.8), "expression" (2.6) all fall below.

**Design decisions**:
- No lemmatization. The Brysbaert norms contain many inflected forms ("hands", "walked", "running"). Missing forms get `None` — we don't interpolate. This is intentional: we want high-precision concrete identification, not exhaustive coverage. A missed concrete word is a false negative (safe); a misclassified abstract word is a false positive (dangerous).
- Simple regex tokenization over spacy/nltk. We're doing dictionary lookup, not parsing. The simplicity is a feature — fewer dependencies, fewer failure modes, faster execution.

**Acceptance Criteria**:
- [ ] `scorer.py` loads norms CSV and builds lookup dict
- [ ] `tokenize("She picked up her coffee.")` returns `['she', 'picked', 'up', 'her', 'coffee']`
- [ ] `score_word("coffee", norms)` returns ~4.9
- [ ] `score_word("deliberation", norms)` returns ~1.8
- [ ] `score_word("the", norms)` returns `None` (function word)
- [ ] `score_sentence(...)` returns correct concrete/abstract classification for known test cases
