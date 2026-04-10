# Phase 2: Interpretive Pattern Detector

**Version**: v1
**Goal**: Build a regex-based pattern matcher that catches the 7 known interpretive filter structures regardless of vocabulary.
**Dependencies**: None (independent of Phase 1 — vocabulary scoring and pattern matching are complementary layers)
**Outputs consumed by**: Phase 3 (CLI combines both layers)

---

## Context

The concreteness scorer (Phase 1) catches abstract VOCABULARY — words like "deliberation", "familiarity", "expression" that score low on the Brysbaert scale. But interpretive prose also uses recognizable STRUCTURES that abstract vocabulary doesn't fully capture:

- "the kind of X that Y" — typological sorting
- "something about the way she Z" — vague pointing
- "as if she had decided to W" — narrator interpretation after action

These structures can use relatively concrete words ("the kind of *walk* that suggested...") and still fail the Artist Test. The structural pattern is the violation, not the individual words.

This is Layer 2 of the hybrid: regex-based structure detection. Combined with Layer 1 (word-level concreteness), the two layers cover both vocabulary drift and structural drift.

---

## Tasks

### 2.1 — Build the pattern matching module

**New file**: `tools/skeleton-strip/patterns.py`

A collection of regex patterns targeting the 7 flag patterns from `references/ai-quirks/sentence-level/18-interpretive-filter.md`, plus additional structural patterns discovered during research.

**Changes**:

1. **Pattern definitions**: Each pattern is a named regex with a human-readable description and category.

```python
@dataclass
class PatternMatch:
    pattern_name: str          # e.g. "kind_of_noun_that"
    category: str              # e.g. "typological_sorting"
    matched_text: str          # the actual matched substring
    start: int                 # character offset in source
    end: int                   # character offset in source
    description: str           # why this is a problem

PATTERNS = [
    # 1. "the expression of someone who..." — categorical face description
    {
        "name": "expression_of_someone",
        "category": "categorical_face",
        "regex": r"the\s+(expression|look|face|eyes|gaze|air|manner)\s+of\s+(someone|a\s+\w+)\s+who",
        "description": "Categorizes a face/expression by TYPE instead of describing physical detail"
    },
    # 2. "the kind of [noun] that..." — typological sorting
    {
        "name": "kind_of_noun_that",
        "category": "typological_sorting",
        "regex": r"the\s+kind\s+of\s+\w+\s+that",
        "description": "Sorts into categories instead of describing the specific instance"
    },
    # 3. "something about [noun]" — vague pointing
    {
        "name": "something_about",
        "category": "vague_pointer",
        "regex": r"something\s+(about|in|behind)\s+(the\s+way|her|his|their|\w+['']?s?)\b",
        "description": "Points vaguely instead of naming the specific detail"
    },
    # 4. "the way [pronoun] [verb]ed suggested/implied/betrayed..." — action + interpretation
    {
        "name": "way_suggested",
        "category": "narrator_interpretation",
        "regex": r"the\s+way\s+(she|he|they|it|\w+)\s+\w+(?:ed|ing|s)?\s+(suggested|implied|betrayed|revealed|spoke\s+of|hinted|indicated|conveyed)",
        "description": "Narrates an action then interprets it instead of letting the action speak"
    },
    # 5. "[noun] spoke of / suggested / betrayed / revealed" — inanimate interpretation
    {
        "name": "inanimate_interpretation",
        "category": "personification",
        "regex": r"(?:the\s+)?\w+\s+(spoke\s+of|suggested|betrayed|revealed|announced|proclaimed|whispered\s+of|hinted\s+at)",
        "description": "Inanimate objects performing interpretation — describe what it looks like instead"
    },
    # 6. "as if [abstract clause]" after physical description
    {
        "name": "as_if_interpretation",
        "category": "appended_interpretation",
        "regex": r"as\s+if\s+(she|he|they|it|the\s+\w+)\s+(had\s+)?(decided|chosen|made|determined|resolved|accepted|understood|realized|known|sensed|felt)",
        "description": "Appends narrator interpretation to a physical image — the image was enough"
    },
    # 7. Forced noun-metaphors (X was a/an Y, X had become Y)
    {
        "name": "forced_noun_metaphor",
        "category": "metaphor_label",
        "regex": r"(she|he|they|it|I)\s+(was|had\s+become|became|felt\s+like)\s+(a|an|the)\s+(wall|mask|ghost|shadow|statue|stone|island|fortress|armor|furniture|weapon|tool|machine|mirror|anchor|beacon)\b",
        "description": "Labels a person/thing as a metaphor-noun instead of describing their physical state"
    },
    # 8. "with the [exact/precise/careful] [noun] of" — mechanical process framing
    {
        "name": "mechanical_precision",
        "category": "process_framing",
        "regex": r"with\s+the\s+(exact|precise|careful|practiced|deliberate|studied|measured)\s+\w+\s+of",
        "description": "Frames a human action as a mechanical process instead of showing the action"
    },
    # 9. Emotional state labels: "felt a surge/wave/rush of [emotion]"
    {
        "name": "emotion_surge",
        "category": "emotional_label",
        "regex": r"felt\s+a\s+(surge|wave|rush|flicker|pang|stab|jolt|flash|bloom|twist|knot)\s+of\s+(anger|fear|sadness|joy|grief|shame|guilt|pride|love|longing|dread|panic|relief|hope|despair|anxiety|rage|jealousy|envy|tenderness|warmth|cold|heat)",
        "description": "Labels an emotional state with a canned metaphor instead of showing through action"
    },
    # 10. "the [noun] was [adjective] in a way that [interpretation]"
    {
        "name": "adjective_way_that",
        "category": "appended_interpretation",
        "regex": r"in\s+a\s+way\s+that\s+(suggested|implied|made\s+\w+|felt|seemed|reminded|spoke|hinted)",
        "description": "Appends interpretation to a description via 'in a way that' — cut the interpretation"
    },
]
```

2. **`find_patterns(text)` → list[PatternMatch]**: Run all patterns against text. Return matches with positions. Case-insensitive matching. Dedup overlapping matches (keep longest).

3. **`find_patterns_in_sentences(sentences)` → dict[int, list[PatternMatch]]**: Takes a list of sentence strings (indexed), returns a map of sentence_index → matches. This is the per-sentence view the CLI will use.

**Design decisions**:
- Regex over spacy/dependency parsing. The interpretive filter patterns have distinctive surface forms that regex catches reliably. We don't need syntactic analysis to find "the kind of X that" — it's a string pattern.
- Case-insensitive. "The kind of" at sentence start capitalizes "The" — the pattern should still match.
- Pattern list is extensible. New patterns can be added to the `PATTERNS` list without changing the matching logic. This is important — we'll discover new patterns during calibration.
- False positive tolerance: some of these patterns have legitimate uses ("the kind of coffee that dissolves paint" in dialogue is fine). The CLI will flag them; the LLM gate decides if the defense applies. The pattern detector is a high-recall, moderate-precision tool. The LLM provides the precision layer.

**Acceptance Criteria**:
- [ ] `patterns.py` defines ≥10 regex patterns covering the 7 core flags plus extensions
- [ ] `find_patterns("She moved with the kind of deliberation that suggested awareness")` returns ≥1 match (kind_of_noun_that)
- [ ] `find_patterns("She picked up her coffee")` returns 0 matches
- [ ] `find_patterns("Something about the way she walked betrayed familiarity")` returns ≥2 matches (something_about + way_suggested or inanimate_interpretation)
- [ ] Matches include character offsets for locating in source text
- [ ] Case-insensitive: "The Kind of" at sentence start matches
