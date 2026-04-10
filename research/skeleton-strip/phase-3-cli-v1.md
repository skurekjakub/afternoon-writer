# Phase 3: The Skeleton Strip CLI

**Version**: v1
**Goal**: Build the main CLI tool that takes a prose file, runs both scoring and pattern layers, and outputs a structured report the gate agent can consume.
**Dependencies**: Phase 1 (scorer), Phase 2 (patterns)
**Outputs consumed by**: Phase 4 (gate integration), Phase 5 (writer integration)

---

## Context

The skeleton strip CLI is the "Fourier transform" — it takes prose (spatial domain) and produces a structured decomposition (frequency domain) that makes invisible concreteness patterns visible. The output must be consumable by an LLM agent via bash tool output.

Two output modes:
1. **Skeleton view** (human-readable) — the original text with abstract content struck through, showing only what survives the filter. This is the "X-ray" view.
2. **Density report** (JSON) — per-sentence and per-paragraph concreteness metrics, pattern matches, and flagged zones. This is what the gate agent consumes programmatically.

---

## Tasks

### 3.1 — Build the sentence splitter

**New file**: `tools/skeleton-strip/splitter.py`

Prose-aware sentence splitting. Standard regex sentence splitting breaks on abbreviations ("Dr. Mars"), dialogue mid-sentence, and ellipses. We need something that handles fiction prose.

**Changes**:

1. **`split_sentences(text)` → list[Sentence]`**: Split on period/question mark/exclamation mark followed by whitespace and capital letter, BUT preserve:
   - Abbreviations: "Dr.", "Mrs.", "Mr.", "Ms.", "Jr.", "Sr.", "St.", "Ave.", "Blvd."
   - Dialogue mid-sentence: don't split on punctuation inside quotation marks
   - Ellipses: "..." is not a sentence boundary when followed by lowercase
   - Em-dashes: "—" is not a sentence boundary

```python
@dataclass
class Sentence:
    text: str                  # the raw sentence text
    index: int                 # position in the document (0-based)
    paragraph_index: int       # which paragraph it belongs to
    start_char: int            # character offset in source
    end_char: int              # character offset in source
    is_dialogue: bool          # contains quotation marks
```

2. **`split_paragraphs(text)` → list[Paragraph]`**: Split on double newlines. Track paragraph boundaries.

```python
@dataclass
class Paragraph:
    text: str
    index: int
    sentences: list[Sentence]
    start_char: int
    end_char: int
```

**Acceptance Criteria**:
- [ ] Handles abbreviations: `"Dr. Mars walked in."` is one sentence, not two
- [ ] Handles dialogue: `"She said, 'I know. I've always known.' Then she left."` is one sentence
- [ ] Handles ellipses: `"She waited... and then moved."` is one sentence
- [ ] Paragraph detection works on standard markdown prose (double newline separation)

### 3.2 — Build the strip engine

**New file**: `tools/skeleton-strip/engine.py`

Combines the scorer (Phase 1) and patterns (Phase 2) into the complete analysis pipeline.

**Changes**:

1. **`analyze_sentence(sentence, norms)` → SentenceAnalysis`**:
```python
@dataclass
class SentenceAnalysis:
    sentence: Sentence
    word_score: SentenceScore          # from scorer.py
    pattern_matches: list[PatternMatch] # from patterns.py
    skeleton: str                       # text with abstract words removed
    density: float                      # concrete_ratio from word_score
    flags: list[str]                    # human-readable flag summaries
    verdict: str                        # "concrete", "mixed", "abstract"
```

The verdict thresholds:
- `concrete_ratio >= 0.5` AND 0 pattern matches → "concrete"
- `concrete_ratio >= 0.3` AND ≤1 pattern match → "mixed"
- `concrete_ratio < 0.3` OR ≥2 pattern matches → "abstract"

2. **`analyze_paragraph(paragraph, norms)` → ParagraphAnalysis`**:
```python
@dataclass
class ParagraphAnalysis:
    paragraph: Paragraph
    sentences: list[SentenceAnalysis]
    mean_density: float                 # average density across sentences
    abstract_sentence_count: int        # sentences with verdict "abstract"
    total_pattern_matches: int
    verdict: str                        # "grounded", "drifting", "abstract"
```

Paragraph verdicts:
- ≥70% of sentences are "concrete" → "grounded"
- 40-70% "concrete" → "drifting"
- <40% "concrete" → "abstract"

3. **`analyze_document(text, norms)` → DocumentAnalysis`**:
```python
@dataclass
class DocumentAnalysis:
    paragraphs: list[ParagraphAnalysis]
    total_sentences: int
    abstract_sentences: int
    total_pattern_matches: int
    mean_density: float
    flagged_zones: list[tuple[int, int]]  # paragraph ranges that are "abstract" or "drifting"
    overall_verdict: str
```

4. **The skeleton itself**: For each sentence, build a "skeleton" string that keeps ONLY:
   - Words with concreteness score ≥ CONCRETE_THRESHOLD (4.0)
   - Words with no score (function words, names — they're structural)
   - Remove words with score < ABSTRACT_THRESHOLD (2.5)
   - Words between 2.5-4.0 stay (they're neutral — not actively abstract)

   The skeleton of "She moved with the kind of deliberation that suggested she was very aware of being watched" becomes: "She moved with the ___ of ___ that ___ she was very ___ of being ___" — the gaps are visible.

   Better: just show the concrete words that survived: `[moved]` — one word from a 17-word sentence. That ratio (1/17 = 0.06) is the density.

**Acceptance Criteria**:
- [ ] `analyze_sentence` produces correct verdicts for known good/bad examples
- [ ] Skeleton of "Chin up. Steps even. Not looking at anyone." retains most content
- [ ] Skeleton of "She moved with the kind of deliberation that suggested awareness" is nearly empty
- [ ] Paragraph analysis correctly identifies "drifting" zones
- [ ] Document analysis aggregates paragraph analyses

### 3.3 — Build the CLI entry point

**New file**: `tools/skeleton-strip/strip.py`

The CLI tool that orchestrates the full pipeline. Invocable by the gate agent via bash.

**Changes**:

1. **CLI interface**:
```bash
# Full JSON report (for gate agent consumption)
python3 tools/skeleton-strip/strip.py --json path/to/draft.md

# Human-readable skeleton view (for debugging/development)
python3 tools/skeleton-strip/strip.py --skeleton path/to/draft.md

# Summary only (for writer self-check — just the flagged zones)
python3 tools/skeleton-strip/strip.py --summary path/to/draft.md
```

2. **JSON output** (for `--json`):
```json
{
    "file": "path/to/draft.md",
    "overall": {
        "total_sentences": 142,
        "abstract_sentences": 23,
        "abstract_percentage": 16.2,
        "total_pattern_matches": 7,
        "mean_density": 0.41,
        "verdict": "mixed"
    },
    "flagged_zones": [
        {
            "paragraphs": [3, 4],
            "reason": "2 consecutive abstract paragraphs",
            "sentences": [
                {
                    "index": 12,
                    "text": "She moved with the kind of deliberation...",
                    "density": 0.06,
                    "patterns": ["kind_of_noun_that"],
                    "verdict": "abstract"
                }
            ]
        }
    ],
    "by_paragraph": [...]
}
```

3. **Skeleton output** (for `--skeleton`):
```
PARAGRAPH 1 [grounded, density=0.62]
  "She picked up her coffee, two sugars, black."
   SKELETON: [picked, coffee, sugars, black] density=0.67 ✅

  "The mug was chipped on the rim."
   SKELETON: [mug, chipped, rim] density=0.60 ✅

PARAGRAPH 2 [abstract, density=0.12]
  "She moved with the kind of deliberation that suggested she was very aware of being watched."
   SKELETON: [moved] density=0.06 ❌
   PATTERNS: kind_of_noun_that

  "Something about the way she carried herself spoke of a familiarity with being observed."
   SKELETON: [carried] density=0.07 ❌
   PATTERNS: something_about, inanimate_interpretation
```

4. **Summary output** (for `--summary`):
```
DRAFT: path/to/draft.md
OVERALL: 142 sentences, 16.2% abstract, mean density 0.41
FLAGGED ZONES: 3
  ¶3-4: 2 abstract paragraphs (density 0.12, 0.15)
  ¶11: 1 abstract paragraph (density 0.18), 2 pattern matches
  ¶22-23: 2 drifting paragraphs (density 0.28, 0.31)
```

**Acceptance Criteria**:
- [ ] `python3 tools/skeleton-strip/strip.py --json draft.md` produces valid JSON to stdout
- [ ] `python3 tools/skeleton-strip/strip.py --skeleton draft.md` produces readable skeleton view
- [ ] `python3 tools/skeleton-strip/strip.py --summary draft.md` produces concise flagged-zone summary
- [ ] Exit code 0 on success, 1 on file not found, 2 on missing norms data
- [ ] Handles markdown files with YAML frontmatter (skips it)
