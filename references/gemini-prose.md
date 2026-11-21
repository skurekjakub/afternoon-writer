# Gemini 2.5 / 3 Pro Prose Calibration Notes

Empirical calibration notes for running the Afternoon Writer fiction pipeline on Gemini models (via Antigravity CLI) alongside Claude and GPT-5.

## The Structural Asymmetry: Gemini vs. GPT-5 / Claude Opus

The original linter and rhythm scorer were tuned primarily against GPT-5 and Claude Opus failure modes. Gemini 2.5 / 3 Pro fails in the **opposite structural direction**:

| Axis | GPT-5 / Claude Opus failure mode | Gemini 2.5 / 3 Pro failure mode |
|---|---|---|
| **Texture direction** | `UNDER-TEXTURED` — staccato telegram runs, texture deserts, short-sentence spam | `OVER-TEXTURED` — em-dash clusters, chained participial tails, bloated 25–40w sentences |
| **Pacing trick** | Mechanically even medium sentences (`F1`) | Whiplash between lush multi-clause sentences and 1-word stinger paragraphs (`Silence.`, `Too late.`) |
| **Modifiers** | Hedge drag (`almost`, `seemed`, `slightly`) | Double-barrel adjective pairs (`a slow, measured breath`, `a sharp, clinical click`) |
| **Sensory register** | Generic / abstract placeholders (`something in her voice`) | Recycled cinematic wallpaper (`ozone`, `copper and rot`, `bathed in moonlight`, `shattered the silence`) |
| **Interiority** | Filter verbs (`she noticed`, `she realized`) | Somatic `something` (`something in her chest tightened`) and `X of Y` nominalizations (`a flicker of doubt`, `a ghost of a smile`) |
| **Register bleed** | Essay brain / corporate pleasantness | Clinical / technical bleed (`architect of`, `calibrated`, `surgical precision`, `kinetic`) |
| **Negation** | Parallel `Not X, but Y. Not A, but B.` and `Not X; Y` | Period/em-dash pivots (`It wasn't X. It was Y.`, `It wasn't X—it was Y.`, `Not X—Y.`, `not merely/out of X, but`) |
| **Slow-burn romance** | Polite emotional over-explanation / therapy-speak | Romance stock choreography (`breath hitched`, `heat pooled`, `gaze dropped to her lips`, `magnetic pull`) |

## Human-Corpus Empirical Calibration

All 35 patterns in `tools/slop_checker/patterns/gemini_prose_tics.py` and the over-ornate detector in `tools/rhythm_scorer/texture.py` were benchmarked against the repo's gold-standard human fantasy corpora (with genre furniture and headers stripped identically to `tools/mannered_checker/calibrate.py`):

- **`style-samples/travel.md`** (Brandon Sanderson, *The Way of Kings*): **380,906 words** (39,749 sentences; 76 × ~5K-word slices)
- **`style-samples/archmage/`** (23 chapters): **56,529 words** (4,867 sentences; 23 chapters)
- **Total human benchmark corpus**: **437,435 words** (44,616 sentences; 99 chapter-sized slices)
- **Blend weighting**: 1:2 (`travel.md` weight 1, `archmage/` weight 2), matching `.afternoon/config.json`

### Pattern Benchmarks (`tools/slop_checker/patterns/gemini_prose_tics.py`)

| Pattern | Cap | `travel.md` (381K) | `/10K` | `archmage/` (57K) | `/10K` | Blend `/5K` |
|---|---:|---:|---:|---:|---:|---:|
| `gemini_neg_wasnt_period` | 1 | 19 | 0.50 | 0 | 0.00 | 0.08 |
| `gemini_neg_wasnt_emdash` | 0 | 1 | 0.03 | 0 | 0.00 | 0.00 |
| `gemini_neg_not_emdash` | 0 | 2 | 0.05 | 0 | 0.00 | 0.01 |
| `gemini_neg_not_merely_out_of` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_scent_ozone` | 1* | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_copper_pair` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_metallic_tang` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_thick_with_scent` | 0 | 1 | 0.03 | 0 | 0.00 | 0.00 |
| `gemini_bathed_in_light` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_pools_of_shadow` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_cast_long_shadows` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_broken_only_by` | 0 | 1 | 0.03 | 0 | 0.00 | 0.00 |
| `gemini_shattered_silence` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_deafening_silence` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_ghost_of_smile` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_flicker_of_emotion` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_veneer_facade` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_symphony_labyrinth` | 0 | 3 | 0.08 | 0 | 0.00 | 0.01 |
| `gemini_sheer_weight_of` | 0 | 1 | 0.03 | 0 | 0.00 | 0.00 |
| `gemini_sliver_of_abstract` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_echo_of_abstract` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_something_body_shifted` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_the_kind_of_that` | 1 | 3 | 0.08 | 0 | 0.00 | 0.01 |
| `gemini_micro_time` | 1 | 1 | 0.03 | 2 | 0.35 | 0.12 |
| `gemini_one_thing_certain` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_razor_precision` | 0 | 1 | 0.03 | 0 | 0.00 | 0.00 |
| `gemini_clinical_bleed` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_un_adjectives` | 1 | 4 | 0.11 | 1 | 0.18 | 0.08 |
| `gemini_double_barrel_adj` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_stinger_paragraph` | 1 | 4 | 0.11 | 0 | 0.00 | 0.02 |
| `gemini_romance_breath_hitched` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_romance_pulse_spiked` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_romance_heat_pooled` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_romance_gaze_lips` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |
| `gemini_romance_magnetic_pull` | 0 | 0 | 0.00 | 0 | 0.00 | 0.00 |

\* `gemini_scent_ozone` is capped at `1` (rather than `0`) because `.afternoon/style-guide.json` permits `"the taste of ozone"` as a physical arcane-casting sensation for Jaina POV. One earned use per chapter passes; Gemini ozone spam violates.

### Combined-Cap Validation (`COMBINED_CAP = 6`)

- **All 35 patterns combined on `travel.md`**: 41 hits total (`0.54 / 5K`), max **4** in any 5K-word slice, **0 of 76 slices** exceed `COMBINED_CAP = 6`.
- **All 35 patterns combined on `archmage/`**: 3 hits total (`0.27 / 5K`), max **1** in any chapter, **0 of 23 chapters** exceed `COMBINED_CAP = 6`.
- **24 of 35 patterns** occur literally **0 times** across all 437,435 human words.

### Over-Ornate Texture Benchmarks (`tools/rhythm_scorer/texture.py`)

Measured across all 44,616 sentences of the human corpora using a 6-sentence sliding window (`ORNATE_WINDOW = 6`):

| Trigger (`over_textured_run`) | `travel.md` (39,749 sents) | `archmage/` (4,867 sents) | Notes |
|---|---:|---:|---|
| `>= 4/6` em-dash sentences | **0** (0.00/10K) | **0** (0.00/10K) | Clean Gemini em-dash spam detector |
| `>= 10` total texture markers in 6 sentences | **0** (0.00/10K) | **0** (0.00/10K) | Catches stacked em-dash + participial + compound ornament |
| `>= 5/6` participial sentences | 13 (0.34/10K) | **0** (0.00/10K) | Sanderson runs high participial (11.1%); catches runaway `, Ving` chains |

### Directional Texture Guidance

`tools/rhythm_scorer/texture.py` keeps the JSON `verdict` contract (`"within_target"` / `"below_target"`, meaning overall `texture_score < 90` or `short_pct` out of range) while making `interpretation` explicitly directional:
- **`OVER-TEXTURED (cut excess ornament; do NOT add more constructions):`** when every failing dimension is above target (and/or `short_pct` is below floor).
- **`UNDER-TEXTURED (add connective tissue):`** when every failing dimension is below target (and/or `short_pct` is above ceiling).
- **`MIXED TEXTURE IMBALANCE (cut over-represented constructions, add under-represented ones):`** when the draft overshoots on one construction (e.g. em-dashes) while undershooting on another.
