# Skeleton Strip Expansion Research

> Synthesized from 9 web searches across 3 rounds, plus direct inspection of
> the SlopSquid/Antislop open-source data. June 2025.

## Problem Statement

The original skeleton strip catches **what the prose says** — abstract vs
concrete vocabulary and interpretive filter patterns. But LLM prose has
additional failure modes that are invisible to the model's self-review because
they're statistical, not semantic. The model literally cannot count how many
times it started a sentence with "She looked" or measure whether its sentence
lengths cluster in a suspiciously narrow band.

This document catalogs every additional measurable pattern discovered through
research, evaluates each for implementation cost and signal quality, and
recommends which to build as skeleton strip analysis modules.

---

## Discovered Patterns

### 1. Sentence-Length Uniformity

**What it catches:** AI prose defaults to a narrow sentence-length range
(typically 12-18 words per sentence) with low variance. Human fiction swings
wildly — 2-word punches, 50-word run-ons, deliberate rhythm. The variance
itself is the signal.

**Evidence:**
- Physica A paper (Robustness of sentence length measures): sentence-length
  distribution in human prose follows right-skewed (negative binomial) shapes
  with high variance. AI text tends toward flatter, more Gaussian distributions.
- Springer (On sentence length distribution as an authorship attribute):
  mean, variance, kurtosis, and skewness of sentence length are statistically
  significant discriminators between authors — and between human/AI text.
- Writers' CLC Sentence Variety Analyzer: visualizes sentence-length rhythm,
  quantifies variety via standard deviation. Passages with uniform length
  "feel monotonous to readers."
- ProWritingAid research: popular fiction averages 12-16 words/sentence but
  with notable variability. "Good human prose rarely settles into monotony."

**Measurable stats (all stdlib Python):**
- Mean sentence length (words)
- Standard deviation
- Min / Max
- Coefficient of variation (CV = stdev/mean)
- Skewness (right-skewed is human-like; symmetric is AI-like)

**Implementation cost:** ~15 lines. Sentence split on `.!?`, count words per
sentence, compute stats.

**Signal quality:** HIGH. This is one of the most reliable mechanical
discriminators. Combined with comma density (below), it catches "telegram
prose" — our #1 AI writing complaint.

---

### 2. Comma Density (Telegram Prose Detector)

**What it catches:** AI fiction defaults to short, choppy sentences with
minimal internal punctuation. Our system prompt already specifies "aim for
1.5-2.5 commas per period." Comma density mechanically enforces this.

**Evidence:**
- Dev.to (AI detection via perplexity and burstiness): punctuation entropy
  (including comma placement regularity) is "a strong signal" — AI distributes
  punctuation at more regular intervals than humans, resulting in lower entropy.
- Fiction writing guidance (King, Leonard, our own system prompt): good prose
  has subordinate clauses, appositives, participial phrases — all requiring
  commas. Telegram prose skips all of these.

**Measurable stats:**
- Commas per period (our target: 1.5-2.5)
- Comma density per 100 words
- Variance of commas-per-sentence across the text

**Implementation cost:** ~10 lines. Count commas, count periods, divide.

**Signal quality:** HIGH for our specific use case. Directly maps to a rule
we already enforce in prose. Below 1.0 = telegram prose. Above 3.5 = run-on
territory.

---

### 3. Paragraph-Length Uniformity

**What it catches:** AI produces paragraphs of suspiciously similar length
(often 3-4 sentences, 40-60 words each). Human writers vary paragraph length
deliberately for pacing — one-sentence punches, long atmospheric builds.

**Evidence:**
- HumanizeThisAI Analyzer: specifically measures paragraph uniformity as
  an AI detection signal.
- SearchAtlas AI Pattern Detector: uses stylometric and statistical signals
  including paragraph-level uniformity.
- SlopSquid leaderboard: reports average paragraph length as a scored metric.

**Measurable stats:**
- Mean paragraph length (words and sentences)
- Standard deviation of paragraph lengths
- CV of paragraph lengths
- Presence of one-sentence paragraphs (healthy prose has some; AI avoids them)

**Implementation cost:** ~15 lines. Split on double newlines, measure each.

**Signal quality:** MEDIUM. Less discriminating than sentence-level metrics
because paragraph boundaries in fiction depend on dialogue formatting. Still
useful as a secondary signal.

---

### 4. Vocabulary Richness (Lexical Diversity)

**What it catches:** AI overuses common words and hedge words ("seemed,"
"felt," "something," "almost," "slightly"). Low vocabulary diversity means
the prose draws from a shallow pool even when the model "knows" richer words.

**Evidence:**
- LexicalRichness package docs: MATTR (Moving Average Type-Token Ratio,
  Covington & McFall 2010) is "more reliable than raw TTR for comparing texts
  of different lengths" — ideal for chapters of varying size.
- SlopSquid leaderboard: uses MATTR-500 as a primary metric.
- Swizec Teller blog + Magnus Nissel gist: Yule's K implementation in pure
  Python, no deps. Higher K = more repetitive vocabulary.

**Recommended metrics:**

| Metric | What it measures | Formula |
|---|---|---|
| MATTR-100 | Vocabulary diversity (windowed) | Average TTR across sliding 100-word windows |
| Yule's K | Vocabulary repetitiveness | 10000 × (M2 - N) / N² where M2 = Σ(f² × V(f)) |
| Hapax ratio | % of words used only once | hapax_count / total_types |

**Implementation cost:** ~40 lines total. Regex tokenizer + Counter + sliding
window. All stdlib Python — no NLTK, no spacy, no lexicalrichness package.

**Signal quality:** MEDIUM-HIGH. MATTR is the strongest of the three — it's
the one SlopSquid uses on their leaderboard. Yule's K and hapax ratio are
secondary confirmation. Together they catch "this chapter uses 400 unique
words when it should use 800+."

---

### 5. Sentence Opener Monotony

**What it catches:** AI starts too many sentences with the same 2-word
pattern. "She looked," "He turned," "The room" — when 20% of your sentences
start the same way, the prose feels robotic even if each sentence is
individually fine.

**Evidence:**
- Reliable AI Check: flags repeated transition phrases and sentence starters
  as "common AI tells."
- Sentence Variety Analyzer (justbuildthings.com): examines opening variety,
  highlights monotonous openers.
- Writey AI Detector: uses sentence-start variation as a detection signal.

**Measurable stats:**
- Frequency table of first-2-word openers
- Max frequency (any opener appearing >3× per 1000 words = flag)
- Unique opener ratio (unique openers / total sentences)
- Paragraph-opener version (first 2 words of each paragraph)

**Implementation cost:** ~20 lines. Split sentences, extract first 2 words,
Counter, report any above threshold.

**Signal quality:** HIGH for fiction. This catches one of the most common
complaints in our voice sheets: "don't start every sentence with the
character's name + verb."

---

### 6. Slop Word/Phrase Frequency

**What it catches:** Known AI-overused words and phrases by raw count — not
semantic detection (the LLM gate does that) but mechanical frequency. "You
used 'flickered' 4 times and 'gleaming' 3 times in 3000 words" is something
the LLM literally cannot count.

**Evidence:**
- Antislop paper (Paech et al., 2025, arxiv 2510.15061): identifies patterns
  via frequency ratio ρ = f_LLM / f_human. Words appearing 1000× more often
  in LLM output than human text.
- SlopSquid: open-source MIT-licensed JSON data files. Three tiers:
  - `slop_list.json`: 1648 flagged words
  - `slop_list_bigrams.json`: 200 bigram patterns
  - `slop_list_trigrams.json`: 430 trigram patterns
- Slop Score composite: 60% word hits + 25% not-x-but-y + 15% trigram hits,
  all per 1000 words.

**Downloaded artifacts** (saved to `research/slopsquid-data/`):
- `slop_list.json` — 1648 words. Many are fantasy-specific names (aelara,
  eldric, grimoire) that won't trigger in our prose. The useful subset is
  smaller: words like "flickered," "gleaming," "crimson," "etched,"
  "billowing," "cacophony," "enigmatic," "ethereal."
- `slop_list_bigrams.json` — 200 bigrams. Top hits: "said voice," "deep
  breath," "voice barely," "heart pounding," "mind racing."
- `slop_list_trigrams.json` — 430 trigrams. Top hits: "voice barely whisper,"
  "took deep breath," "could help feel," "heart pounding chest."

**Implementation options:**
1. Use SlopSquid lists raw (fast, proven) — but many entries are
   fantasy-name noise irrelevant to our stories
2. Curate a fiction-specific subset (~100-200 words, ~50-100 trigrams)
3. Parse our own `slop-hitlist.md` into countable patterns
4. Merge approach: SlopSquid data filtered for fiction relevance + our hitlist

**Implementation cost:** ~25 lines + JSON loading. No deps beyond stdlib.

**Signal quality:** MEDIUM. Overlaps with what the LLM gate already does
by reading slop-hitlist.md — but the mechanical count adds a dimension the
LLM can't replicate. Most useful as a frequency cap enforcer: "no slop word
should appear more than 2× per 5000 words."

---

### 7. Patterns Evaluated and Rejected

**Perplexity-based burstiness (via local Ollama):**
Measures per-sentence perplexity variance using a language model. Human text
is "bursty" (high variance), AI is smooth. Rejected because: (a) sentence-
length variance + comma density catch most of the same signal without model
inference, (b) adds Ollama dependency and ~10s per chapter of inference time,
(c) perplexity is model-dependent — which model's perplexity? Future
consideration if simpler metrics prove insufficient.

**Full n-gram overuse analysis:**
Compute frequency of all bigrams/trigrams, compare to human baseline (need
large reference corpus). Rejected because: overkill for our pipeline. The
slop frequency module (curated lists) catches the worst offenders without
needing a reference corpus.

**Structural symmetry / wrap-up detection:**
Detecting formulaic paragraph-ending sentences ("Thus, it is clear that...").
Rejected because: more relevant for essays than fiction. Our gate already
checks for this class of pattern semantically.

**Punctuation entropy:**
Full Shannon entropy over punctuation distribution. Rejected because: comma
density captures 80% of the signal much more simply. Could be added later
as a refinement.

---

## Recommended Module Priority

| Priority | Module | Signal | Cost | Deps |
|---|---|---|---|---|
| 1 | Rhythm (sentence length + comma density) | HIGH | ~25 lines | stdlib |
| 2 | Openers (sentence-start monotony) | HIGH | ~20 lines | stdlib |
| 3 | Vocabulary (MATTR + Yule's K + hapax) | MEDIUM-HIGH | ~40 lines | stdlib |
| 4 | Paragraph rhythm | MEDIUM | ~15 lines | stdlib |
| 5 | Slop frequency | MEDIUM | ~25 lines | stdlib + JSON |

Modules 1-3 are the highest-leverage additions. Module 4 is trivial to add
alongside Module 1 (same math, different unit). Module 5 has the most overlap
with existing LLM-based detection but adds mechanical counting the LLM can't
do.

---

## Key Sources

1. Paech et al. (2025). "Antislop: A Comprehensive Framework for Identifying
   and Eliminating Repetitive Patterns in LLMs." arxiv 2510.15061.
2. SlopSquid / slop-score (MIT). github.com/sam-paech/slop-score
3. Covington & McFall (2010). "Cutting the Gordian Knot: The Moving-Average
   Type-Token Ratio (MATTR)." J. Quantitative Linguistics.
4. Physica A (2018). "Robustness of sentence length measures in written texts."
   sciencedirect.com/science/article/pii/S0378437118305326
5. On sentence length distribution as an authorship attribute (Springer).
6. IBM Analytic Hints approach (cited in abstract-voice-research.md).
7. Writers' CLC Sentence Variety Analyzer. writersclc.com
8. Dev.to — "How to Detect AI-Generated Content Using Perplexity and
   Burstiness."

## Downloaded Artifacts

Saved to `research/slopsquid-data/`:
- `slop_list.json` — 1648 words (MIT licensed)
- `slop_list_bigrams.json` — 200 bigrams (MIT licensed)
- `slop_list_trigrams.json` — 430 trigrams (MIT licensed)

Source: github.com/sam-paech/slop-score @ commit 289264ab
License: MIT (see slop-score repo LICENSE file)
