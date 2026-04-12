# Phase 1b: Run Analytic Tools

After resolving the workspace in Phase 1, run the deterministic analysis tools before building the false-positive filter. These produce structured hints that sharpen your audit — they flag specific zones, metrics, and pattern counts that the guide sweeps should pay extra attention to.

## Run the tools

From the repository root, run both tools on the target prose file:

```
python3 tools/rhythm_scorer/score.py --json .afternoon/chapters/{chapterId}/{targetFile}
python3 tools/slop_checker/check.py --json .afternoon/chapters/{chapterId}/{targetFile}
```

Capture the JSON output from each.

## Parse the rhythm scorer output

The rhythm scorer reports two blocks: **rhythm** and **texture**.

### Rhythm metrics

- `comma_period_ratio` — syntactic complexity proxy. Compare against `rhythmMetrics.global.comma_period_ratio` in `.afternoon/style-guide.json`.
- `sentence.short_pct` — percentage of sentences <= 6 words
- `sentence.long_pct` — percentage of sentences >= 20 words
- `sentence.cv_length` — coefficient of variation (higher = more variety). Compare against `rhythmMetrics.global.sentence_length_cv`.
- `openers.entropy` — sentence opener variety (higher = more diverse)
- `paragraph.one_sentence_pct` — percentage of one-sentence paragraphs. Compare against `rhythmMetrics.global.one_sentence_paragraph_pct`.

### Texture metrics

The `texture` block measures structural sentence complexity — the joining constructions (participial phrases, compound clauses, em-dashes, semicolons) that create connective tissue in prose. Pipeline prose typically has a fraction of human texture density. The style guide's `textureMetrics` section specifies the human-measured values, targets, and acceptable ranges for each construction.

Parse these fields:

- `texture.participial_pct` — % of sentences with a participial phrase (`, Ving`). Compare against `textureMetrics.participial_pct` in `.afternoon/style-guide.json`. This is typically the single biggest gap.
- `texture.compound_pct` — % of sentences with compound clauses (`, and/but/or/yet/so`). Compare against `textureMetrics.compound_pct`.
- `texture.emdash_pct` — % of sentences with em-dashes. Compare against `textureMetrics.emdash_pct`.
- `texture.semicolon_pct` — % of sentences with semicolons. Compare against `textureMetrics.semicolon_pct`.
- `texture.short_pct` — % of sentences <= 8 words. Compare against `textureMetrics.short_pct`. High values = telegram prose.
- `texture.texture_score` — combined % of sentences with ANY joining construction. Compare against `textureMetrics.texture_score`.
- `texture.verdict` — "within_target", "borderline", or "below_target"
- `texture.verdict_reasons` — array of specific gaps with baselines
- `texture.interpretation` — **AGENT-ACTIONABLE**: specific instructions on what constructions to add and how. Read this field — it tells you exactly what the prose is missing and gives example fixes.
- `texture.flagged_passages` — array of problem zones:
  - `telegram_run` — 8+ consecutive short, textureless sentences (pure staccato)
  - `texture_desert` — 15+ consecutive sentences with zero joining constructions
  - Each has `start_sentence`, `end_sentence`, `sentence_count`, and `preview`

### How to interpret the texture verdict

- **within_target**: Texture metrics fall within calibrated human ranges. No structural concerns.
- **borderline**: 1-2 metrics outside range. Note in the summary but do not flag as a structural problem.
- **below_target**: 3+ metrics outside range. This is a structural problem. The prose is too flat/choppy. Note this prominently in the final verdict — downstream agents (slophunter, style-editor) need to know.

### Texture flagged passages

When a `telegram_run` or `texture_desert` overlaps with a passage you're auditing in Phase 3, this is corroborating evidence that the zone needs structural work — not just vocabulary or pattern fixes, but sentence-level joining. Mention these zones in the Phase 5 notes so downstream agents can target them for expansion.

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

## How hints feed into Phase 3

Tool signals are presumed-guilty evidence. They demand gate attention and carry a ~90% expected kill rate:

1. **Pattern-to-guide mapping (slop checker):**
   - `filter_words`, `filler_actions` -> recurring-tics guide (pass A)
   - `said_bookisms`, `adverb_on_tag` -> recurring-tics guide (pass A)
   - `abstract_locomotion`, `inanimate_agency` -> phantom-concreteness guide (pass B)
   - `verbose_phrases`, `expression_decomposition` -> narrator-seep guide (pass B)
   - `academic_register`, `dialogue_register` -> narrator-seep guide (pass B)
   - `ai_vocabulary`, `clinical_anatomy` -> gpt-5 prose issues guide (pass B)
   - `negation_addiction` -> negation-addiction guide (pass A)
   - `breath_tells`, `body_cliches` -> recurring-tics guide (pass A)
   - `hedging`, `vague_pointers` -> phantom-concreteness guide (pass B)
   - `simile_overload` -> recurring-tics guide (pass A)
   - `participial_attachment` -> recurring-tics guide (pass A)
   - `temporal_padding` -> recurring-tics guide (pass A)
   - `punctuation_tics` -> recurring-tics guide (pass A)
   - `paragraph_structure` -> recurring-tics guide (pass A)
   - `slopsquid` -> gpt-5 prose issues guide (pass B) — statistical AI-overuse collocations
   - `narrator_verdict` -> narrator-seep guide (pass B) — verdict-tag fragments ("X enough to be Y", "too X for Y")

2. **Tool-flagged lines are audit candidates.** When the slop checker reports a match, the gate must evaluate it against the mapped guide. The tool is deterministic — it catches syntactic shapes, not semantic intent, so some matches are legitimate prose. The gate LLM reads context and decides KILL or KEEP. Zero-tolerance matches (`cap: 0`) and `over_cap` violations deserve close scrutiny — KEEP requires an articulable defense grounded in character voice, scene function, or concrete (not abstract) content. Expected kill rate for tool-flagged lines in AI-generated prose: ~90% (human prose triggers the same patterns at ~1/18K words, so occasional KEEPs are normal). Tool-flagged findings must cite the source: include `"toolSignal": "<pattern_name>"` in the finding JSON.

3. **Rhythm metrics** — include in the final notes JSON `summary.rhythmMetrics` block. Compare against `.afternoon/style-guide.json` → `rhythmMetrics` targets when available — report the delta for each metric. If any metric falls outside its `range`, note these as "structural rhythm concerns" in the verdict reason. These don't affect the pass/fail verdict directly — they inform the style-editor downstream.

4. **Texture metrics** — include in the final notes JSON `summary.textureMetrics` block. Report the full `texture.verdict`, `texture.verdict_reasons`, and `texture.interpretation`. If `texture.verdict` is "below_target", add "structural texture deficit" to the verdict reason for the overall notes — downstream agents (slophunter in revision mode, style-editor) need this signal to add joining constructions. Include the count of `telegram_run` and `texture_desert` flagged passages.

5. **Texture-flagged zones in Phase 3** — when a guide sweep reaches a paragraph that falls inside a `telegram_run` or `texture_desert`, note this in the finding. The zone has both a guide-level issue AND a structural texture deficit. The slophunter revision fix should address both: fix the slop pattern AND add structural complexity to the surrounding sentences.

## Store the results

Hold both JSON objects in working memory. You will:
- Reference them during Phase 3 guide audits
- Include rhythm metrics in the Phase 5 notes JSON `summary.rhythmMetrics` block
- Include texture metrics in the Phase 5 notes JSON `summary.textureMetrics` block (verdict, reasons, interpretation, flagged passage count)
- Include slop checker violation summary in the Phase 5 notes JSON `analyticHints.slopChecker` block

## Before moving to Phase 2

You should have:
- rhythm scorer JSON parsed with key rhythm metric values noted
- rhythm scorer texture block parsed with verdict, reasons, interpretation, and flagged passages noted
- slop checker JSON parsed with violation counts, over-cap categories, and pattern-to-guide mappings noted
- both results held in working memory for Phase 3 and Phase 5
