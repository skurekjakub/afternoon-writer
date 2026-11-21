# Phase 1b: Run Analytic Tools

After resolving the workspace in Phase 1, run the deterministic analysis tools before building the false-positive filter. These produce structured hints that sharpen your audit — they flag specific zones, metrics, and pattern counts that the guide sweeps should pay extra attention to.

## Run the tools

From the repository root, run the tools on the target prose file with one command.

Passes `a` and `b`:

```
python3 tools/prose_check.py --json --tools rhythm,slop .afternoon/chapters/{chapterId}/{targetFile}
```

Pass `c` also needs the mannered-prose and refrain checker, so run all three:

```
python3 tools/prose_check.py --json .afternoon/chapters/{chapterId}/{targetFile}
```

The report has one block per tool: `rhythm`, `slop` and, for pass C, `mannered`. Each block is exactly that tool's own `--json` output, described below. The rhythm block is scored against `.afternoon/style-guide.json`.

If `failed` names a tool, its block holds only `error` and `traceback`. Run that tool on its own once:

```
python3 tools/rhythm_scorer/score.py --json --baselines .afternoon/style-guide.json .afternoon/chapters/{chapterId}/{targetFile}
python3 tools/slop_checker/check.py --json .afternoon/chapters/{chapterId}/{targetFile}
python3 tools/mannered_checker/check.py --json .afternoon/chapters/{chapterId}/{targetFile}
```

If it fails again, note it in the scratchpad and audit without that tool's hints.

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
- `texture.texture_score` — balanced 0–100 score (100 = all dimensions on target). ≥90 passes. Compare against `textureMetrics.texture_score`.
- `texture.verdict` — "within_target" or "below_target"
- `texture.verdict_reasons` — array of specific gaps with baselines
- `texture.interpretation` — **AGENT-ACTIONABLE**: specific directional instructions (`OVER-TEXTURED`, `UNDER-TEXTURED`, or `MIXED TEXTURE IMBALANCE`) telling you whether to cut excess ornament (Gemini failure mode) or add connective tissue (GPT-5/Opus failure mode), with concrete fixes. Always follow the direction reported here — do NOT assume `below_target` means "add more constructions."
- `texture.flagged_passages` — array of problem zones:
  - `telegram_run` — 8+ consecutive short, textureless sentences (pure staccato)
  - `texture_desert` — 10+ consecutive sentences with zero joining constructions
  - `over_textured_run` — 6+ consecutive sentences with excess em-dashes (>=4/6), chained participials (>=5/6), or stacked markers (>=10 in 6 sentences) — Gemini over-ornate prose signal
  - Each has `start_sentence`, `end_sentence`, `sentence_count`, and `preview`

### How to interpret the texture verdict

- **within_target**: Texture metrics fall within calibrated human ranges. No structural concerns.
- **below_target** (`UNDER-TEXTURED`): 1+ metrics below range (or `short_pct` above ceiling). Flag as a structural texture deficit — downstream agents should add joining constructions.
- **below_target** (`OVER-TEXTURED`): 1+ metrics above range (e.g. excess em-dashes or participials, or `short_pct` below floor). Flag as **over-ornate / over-textured prose** (classic Gemini failure mode) — downstream agents must **cut** excess em-dashes/participials and break bloated sentences rather than adding more ornament.
- **below_target** (`MIXED TEXTURE IMBALANCE`): Some dimensions overshoot while others undershoot (e.g. em-dash spam paired with low compound clauses). Pass the exact `texture.interpretation` downstream so revisers cut what is above target and add only what is below target.

### Texture flagged passages

When a `telegram_run`, `texture_desert`, or `over_textured_run` overlaps with a passage you're auditing in Phase 3, this is corroborating evidence that the zone needs structural work — either sentence-level joining (`telegram_run` / `texture_desert`) or de-ornamenting / cutting stacked clauses (`over_textured_run`). Mention these zones in the Phase 5 notes so downstream agents can target them.

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

## Parse the mannered checker output (pass `c` only)

The mannered checker reports four blocks:

- `calibration` — which human reference corpora the caps were calibrated against (`priming.humanCorpora` in config, currently Way of Kings plus the Archmage sample). The checker recalibrates on its own when a sample is added or changed.
- `patterns[]` — one entry per detector, with `name`, `code` (M1-M13, matching `mannered-prose-guide.md`), `count`, `cap` (calibrated), `guideCap`, `overCap`, `per10k`, `humanPer10k`, `ratioToHuman` and `matches[]` (`line`, `text`, `context`). A chapter-sized slice of the reference prose trips 0-3 hits in total; pipeline chapters trip 30-50.
- `codeCaps` — combined caps for M4, M5, M7, M11 and M13 (`count`, `cap`, `overCap`). **Use the checker's `cap` and `codeCaps` as the caps for this chapter.** They come from the human reference prose: twice the human rate at this chapter's length, and 0 for any pattern the reference prose uses under 0.5 times per 10K words. Nearly every cap is 0; the maxim is the exception. `guideCap` is the fallback used only when the checker has no calibration.
- `polysyndeton` — narration sentences with 3+ "and"s per 10K words (`per10k`, the calibrated `humanPer10k` and `softCapPer10k`) and `densestParagraphs[]`. Over the soft cap, audit the densest paragraphs first for M4 lists with a turn.
- `refrains` — `crossChapter[]` (runs shared with earlier chapters' `final.md`, with `source` and `sourceLine`), `voiceSheet[]` (runs lifted from voice sheets), `withinChapter[]` (runs repeated in the target, with all `lines`) and `families[]` (signature beats with `countHere`, `windowTotal`, `bookCounts` and `overBudget`). Runs that also appear in the human corpus are already dropped.
- `summary` — headline counts for the notes JSON.

Map these hints into pass C the same way as slop checker hints: every hit is an audit candidate, and every KILL backed by a hit carries `"toolSignal": "<pattern name>"`, or `"toolSignal": "family:<family name>"` for refrain families. Include `summary` in the notes JSON as `analyticHints.manneredChecker`.

## How hints feed into Phase 3

Tool signals are presumed-guilty evidence. They demand gate attention and carry a ~90% expected kill rate:

1. **Pattern-to-guide mapping (slop checker):**
   - `filter_words`, `filler_actions` -> recurring-tics guide (pass A)
   - `said_bookisms`, `adverb_on_tag` -> recurring-tics guide (pass A)
  - `abstract_locomotion`, `inanimate_agency` -> intent-smear guide (pass A)
   - `verbose_phrases`, `expression_decomposition` -> narrator-seep guide (pass B)
   - `academic_register`, `dialogue_register` -> narrator-seep guide (pass B)
   - `ai_vocabulary`, `clinical_anatomy` -> gpt-5 prose issues guide (pass B)
   - `negation_addiction` -> negation-addiction guide (pass A)
   - `breath_tells`, `body_cliches` -> recurring-tics guide (pass A)
   - `hedging`, `vague_pointers` -> phantom-concreteness guide (pass B)
  - `ambient_inversion` -> narrator-seep guide (pass B)
   - `simile_overload` -> recurring-tics guide (pass A)
   - `participial_attachment` -> recurring-tics guide (pass A)
   - `temporal_padding` -> recurring-tics guide (pass A)
   - `punctuation_tics` -> recurring-tics guide (pass A)
   - `paragraph_structure` -> recurring-tics guide (pass A)
   - `slopsquid` -> gpt-5 prose issues guide (pass B) — statistical AI-overuse collocations
   - `gemini_prose_tics` -> gemini prose issues guide (pass B) — Gemini negation pivots, stock sensory/atmospheric pairs, `X of Y` nominalizations, somatic `something`, double-barrel adjectives, clinical bleed, stingers, and slow-burn romance clichés
   - `narrator_verdict` -> narrator-seep guide (pass B) — verdict-tag fragments ("X enough to be Y", "too X for Y")

2. **Tool-flagged lines are audit candidates.** When the slop checker reports a match, the gate must evaluate it against the mapped guide. The tool is deterministic — it catches syntactic shapes, not semantic intent, so some matches are legitimate prose. The gate LLM reads context and decides KILL or KEEP. Zero-tolerance matches (`cap: 0`) and `over_cap` violations deserve close scrutiny — KEEP requires an articulable defense grounded in character voice, scene function, or concrete (not abstract) content. Expected kill rate for tool-flagged lines in AI-generated prose: ~90% (human prose triggers the same patterns at ~1/18K words, so occasional KEEPs are normal). Tool-flagged findings must cite the source: include `"toolSignal": "<pattern_name>"` in the finding JSON.

3. **Rhythm metrics** — include in the final notes JSON `summary.rhythmMetrics` block. Compare against `.afternoon/style-guide.json` → `rhythmMetrics` targets when available — report the delta for each metric. If any metric falls outside its `range`, note these as "structural rhythm concerns" in the verdict reason. These don't affect the pass/fail verdict directly — they inform the style-editor downstream.

4. **Texture metrics** — include in the final notes JSON `summary.textureMetrics` block. Report the full `texture.verdict`, `texture.verdict_reasons`, and `texture.interpretation`. If `texture.verdict` is "below_target", check `texture.interpretation` for direction and add `"structural texture deficit"` (`UNDER-TEXTURED`), `"over-ornate texture excess"` (`OVER-TEXTURED`), or `"mixed texture imbalance"` (`MIXED TEXTURE IMBALANCE`) to the verdict reason for the overall notes so downstream agents (slophunter in revision mode, style-editor) know whether to add connective tissue or cut excess ornament. Include counts of `telegram_run`, `texture_desert`, and `over_textured_run` flagged passages.

5. **Texture-flagged zones in Phase 3** — when a guide sweep reaches a paragraph that falls inside a `telegram_run`, `texture_desert`, or `over_textured_run`, note this in the finding. The slophunter revision fix should address both the guide-level issue AND the structural direction (joining choppy sentences for `telegram_run`/`texture_desert`, or stripping excess em-dashes and participial chains for `over_textured_run`).

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
- for pass `c`: mannered checker JSON parsed, with over-cap patterns, refrain runs and over-budget families noted
- both results held in working memory for Phase 3 and Phase 5
