# Phase 1b: Run Analytic Tools

After resolving the workspace in Phase 1, run the deterministic analysis tools before building the false-positive filter. These produce structured hints that sharpen your audit — they flag specific zones, metrics, and pattern counts that the guide sweeps should pay extra attention to.

## Run the tools

From the repository root, run all three tools on the target prose file:

```
python3 tools/skeleton_strip/strip.py --json .afternoon/chapters/{chapterId}/{targetFile}
python3 tools/rhythm_scorer/score.py --json .afternoon/chapters/{chapterId}/{targetFile}
python3 tools/slop_checker/check.py --json .afternoon/chapters/{chapterId}/{targetFile}
```

Capture the JSON output from each.

## Parse the skeleton strip output

The skeleton strip reports:
- `overall.verdict` — "grounded", "mixed", or "abstract"
- `overall.abstract_percentage` — percentage of sentences classified abstract
- `overall.total_pattern_matches` — count of interpretive filter patterns detected
- `flagged_zones[]` — clusters of abstract paragraphs with specific sentences

For each flagged zone, note:
- Which paragraph indices are in the `paragraphs` array
- The specific `sentences` within those zones (each has `paragraph`, `index`, `text`, `density`, `patterns`, `verdict`)
- Which patterns were detected (these map to guide categories: `narrator_interpretation` → narrator-seep, `emotional_label` → phantom-concreteness, `dramatic_negation` → negation-addiction, etc.)

## Parse the rhythm scorer output

The rhythm scorer reports:
- `comma_period_ratio` — syntactic complexity proxy (published fiction baseline: 0.6–1.6)
- `sentence.short_pct` — percentage of sentences ≤ 6 words
- `sentence.long_pct` — percentage of sentences ≥ 20 words
- `sentence.cv_length` — coefficient of variation (higher = more variety; target ≥ 0.6)
- `openers.entropy` — sentence opener variety (higher = more diverse)
- `paragraph.one_sentence_pct` — percentage of one-sentence paragraphs (target: ≤ 45%)

## Parse the slop checker output

The slop checker reports:
- `total_matches` — total pattern matches across all categories
- `total_violations` — count of patterns exceeding their per-chapter hard cap
- `categories[]` — each with `category`, `combined_count`, optional `combined_cap`, and `patterns[]`

Each pattern has:
- `name` — pattern identifier (e.g., `filler_nodded`, `abstract_locomotion`, `adverb_on_tag`)
- `count` — number of matches in the chapter
- `cap` — maximum allowed per chapter (0 = zero tolerance)
- `over_cap` — boolean, true if count > cap
- `matches[]` — each with `text`, `line`, and `context` snippet

Key categories to watch:
- **Zero-tolerance** (`cap: 0`): `abstract_locomotion`, `verbose_phrases`, `expression_decomposition`, `academic_register`, `clinical_anatomy`, `dialogue_register`, `negation_addiction`, `melodramatic` — any match is a violation
- **Zero-tolerance AI vocabulary**: `delved`, `tapestry`, `testament`, `palpable`, `ethereal`, `juxtaposition`, `ministrations`, `countenance`, `elicited`, `cascading`, `emboldened`, `mosaic`, `ephemeral`, `sublime`, `liminal`, `ineffable`, `resonated`, `hauntingly` — any match is a violation
- **Zero-tolerance slopsquid**: AI-only bigrams (122 phrases: "voice low", "eyes widened", "mind racing", etc.) and trigrams (416 phrases: "voice barely whisper", "took deep breath", etc.) — statistically derived from 67-LLM comparison, zero occurrences in 384K words of human prose. Any match is a strong AI signal.
- **AI vocabulary cap-1**: `wistful`, `visceral`, `poignant`, `nuanced` — legitimate in small doses, flag at 2+
- **Hard-capped per-chapter**: `filler_actions` (4/verb, 15 combined), `filter_words` (3/verb, 7 combined), `said_bookisms` (2/bookism + 3 adverb_on_tag, 5 combined), `breath_tells` (3 combined), `vague_pointers` (3 combined)
- **Per-word-proportional**: `participial_trailing` (1/250w), `simile_like` (1/500w), `punct_semicolon` (1/500w), `punct_ellipsis` (1/600w), `punct_colon_narration` (1/1000w)
- **Hedging individual**: `seemed`/`perhaps` (6 each), `almost` (6), `seemed_to` (3), `appeared_to` (1), `might_have_been` (1), `somehow`/`simply`/`slightly` (2 each)
- **Soft-capped** (density matters): `body_cliches` (1 each), `contact_verbs` (6 each), `simile_as_if` (5)
- **Paragraph structure**: opener repetition (3+ consecutive same-word openers, or >3 She-openers in 6-paragraph window) — `paragraph_structure` category

## How hints feed into Phase 3

These hints do **not** create automatic KILLs. They sharpen your attention:

1. **Flagged abstract zones** — when a guide sweep reaches a paragraph inside a flagged zone, inspect the detected patterns. If the pattern aligns with the guide's detection criteria (e.g., `emotional_label` pattern + phantom-concreteness guide), that's corroborating evidence for a KILL. If the guide sweep would KEEP the line, the deterministic flag alone is not sufficient to override.

2. **Pattern-to-guide mapping (skeleton strip):**
   - `dramatic_negation` → negation-addiction guide (pass A)
   - `narrator_interpretation`, `appended_interpretation` → narrator-seep guide (pass B)
   - `emotional_label`, `evidence_of` → phantom-concreteness guide (pass B)
   - `personification`, `metaphor_label` → gpt-5 prose issues guide (pass B)
   - `categorical_face`, `typological_sorting`, `process_framing` → intent-smear guide (pass A)
   - `vague_pointer` → phantom-concreteness guide (pass B)

3. **Pattern-to-guide mapping (slop checker):**
   - `filter_words`, `filler_actions` → recurring-tics guide (pass A)
   - `said_bookisms`, `adverb_on_tag` → recurring-tics guide (pass A)
   - `abstract_locomotion`, `inanimate_agency` → phantom-concreteness guide (pass B)
   - `verbose_phrases`, `expression_decomposition` → narrator-seep guide (pass B)
   - `academic_register`, `dialogue_register` → narrator-seep guide (pass B)
   - `ai_vocabulary`, `clinical_anatomy` → gpt-5 prose issues guide (pass B)
   - `negation_addiction` → negation-addiction guide (pass A)
   - `breath_tells`, `body_cliches` → recurring-tics guide (pass A)
   - `hedging`, `vague_pointers` → phantom-concreteness guide (pass B)
   - `simile_overload` → recurring-tics guide (pass A)
   - `participial_attachment` → recurring-tics guide (pass A)
   - `temporal_padding` → recurring-tics guide (pass A)
   - `punctuation_tics` → recurring-tics guide (pass A)
   - `paragraph_structure` → recurring-tics guide (pass A)
   - `slopsquid` → gpt-5 prose issues guide (pass B) — statistical AI-overuse collocations

4. **Slop checker violations** — when the checker reports `over_cap: true` or `over_combined_cap: true`, that category has concrete evidence of pattern overuse. During Phase 3, treat each violation as strong corroborating evidence for the mapped guide. Zero-tolerance matches (`cap: 0`) are especially strong signals — these should almost always corroborate a KILL unless the context is genuinely exceptional.

5. **Rhythm metrics** — include in the final notes JSON `summary.rhythmMetrics` block. Compare against `.afternoon/style-guide.json` → `rhythmMetrics` targets when available — report the delta for each metric. If `comma_period_ratio` < 0.5 or `one_sentence_pct` > 50%, note these as "structural rhythm concerns" in the verdict reason. These don't affect the pass/fail verdict directly — they inform the style-editor downstream.

## Store the results

Hold all three JSON objects in working memory. You will:
- Reference them during Phase 3 guide audits
- Include rhythm metrics in the Phase 5 notes JSON summary
- Include slop checker violation summary in the Phase 5 notes JSON `analyticHints.slopChecker` block
- Note the skeleton strip verdict in the status.json summary

## Before moving to Phase 2

You should have:
- skeleton strip JSON parsed with flagged zones and pattern-to-guide mappings noted
- rhythm scorer JSON parsed with key metric values noted
- slop checker JSON parsed with violation counts, over-cap categories, and pattern-to-guide mappings noted
- all three results held in working memory for Phase 3 and Phase 5
