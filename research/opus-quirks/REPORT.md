# Claude Opus 5.5 prose tells: audit of ten blind samples

Saved from the auditor agent's final report. The harness blocked the agent from writing this file itself.

**Corpus:** `research/opus-quirks/samples/01-*.md` to `10-*.md`, 11,783 words. Opus 5.5 wrote them from short briefs without seeing any guide. The samples were not edited.

**Method:**

1. Ran `tools/slop_checker/check.py --json` and `tools/rhythm_scorer/score.py --json --baselines .afternoon/style-guide.json` on each sample.
2. Read every sample against the Pass A guides (negation addiction, intent smear, recurring prose tics), the Pass B guides (`gpt-5-prose-issues.md` F1–F7, narrator seep, phantom concreteness, fake simplification), `references/slop-hitlist.md`, and `references/ai-quirks/` (the README, sentence-level 01–09, and 10-counting-devices).
3. Recorded each instance with the catalogue entry it breaks. A pattern with no catalogue entry was recorded as NEW only if it turned up in at least three of the ten samples.

**Counting:** "Instances" means occurrences of the pattern's shape. A guide's verdict logic may still keep some of them; where it does, the ledger marks them KEEP. Raw filter-verb counts include literal perception and are marked as raw.

Per-sample tool outputs (JSON): `/tmp/claude-1000/-home-jakubs-repositories-tuesdays-universe/a12a7cb7-0c3c-4f5a-ae88-c224785a8bd7/scratchpad/tools/`. That folder is temporary.

## 1. Per-sample tool results

### Slop checker

| Sample | Words | Matches | Over cap | Simile | Filter | Hedging | Contact | Participial | Punctuation | Temporal | Permission | Other | Over-cap pattern(s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 ambush | 1280 | 9 | 1 | 4 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 1 verdict | verdict_enough_for |
| 02 interrogation | 1132 | 9 | 1 | 2 | 1 | 4 | 0 | 0 | 0 | 1 | 0 | 1 vague | hedge_something_like |
| 03 grief | 1178 | 12 | 1 | 1 | 0 | 3 | 3 | 0 | 4 | 1 | 0 | 0 | punct_colon_narration |
| 04 journey | 1211 | 3 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | none |
| 05 banter | 1109 | 7 | 1 | 0 | 1 | 2 | 2 | 1 | 0 | 0 | 1 | 0 | permission_tag_she_let_it |
| 06 council | 1259 | 9 | 1 | 1 | 1 | 0 | 2 | 0 | 2 | 1 | 1 | 1 filler | permission_tag_let_feeling_work |
| 07 first kiss | 1069 | 5 | 0 | 3 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | none |
| 08 dread | 1088 | 16 | 3 | 5 | 4 | 3 | 1 | 0 | 2 | 0 | 0 | 1 opener | simile_like, punct_colon_narration, opener_consecutive_repeat |
| 09 first person | 1140 | 5 | 1 | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | permission_tag_she_let_it |
| 10 reunion | 1283 | 10 | 0 | 1 | 2 | 1 | 0 | 1 | 1 | 0 | 0 | 2 filler, 1 breath, 1 vague | none |
| **Total** | 11,749 | 85 | 9 | 19 | 13 | 14 | 9 | 5 | 11 | 3 | 3 | 8 | |

Notes on the checker hits:

- **Colons.** None of the colon hits is on a markdown title line. Four introduce written words in the scene (03 L17, 03 L19, 03 L39, 08 L5); those are legitimate. The explanatory colons that remain are 03 L27, 06 L71, 07 L19, 08 L53, 09 L31 and 10 L27.
- **01 `verdict_enough_for`** (`close enough for Dace to smell him, woodsmoke and sour wine`) is a concrete distance. KEEP.
- **05 `permission_tag_she_let_it`** (`I've let it go, out of affection, for eleven years`) is a dialogue idiom. Borderline.
- **02 hedging (4)** counts `seemed` and `seemed to` in one phrase. `something like a smile` is also counted under vague pointers.
- **08 `opener_consecutive_repeat`** (`He` ×3 at L9) is not sustained, so not F1. KEEP.

### Rhythm scorer

| Sample | Sent. | Mean len | SD | CV | Short % | Long % | Comma/period | Top opener (share) | Paras | 1-sent para % | MATTR | Particip. % | Compound % | Em dash % | Semicolon % | Texture | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 103 | 12.4 | 10.4 | 0.84 | 40.8 | 21.4 | 0.70 | he 21 (20%) | 37 | 24.3 | 0.780 | 3.9 | 18.4 | 0.0 | 0.0 | 61.3 | below |
| 02 | 148 | 7.6 | 6.8 | 0.89 | 57.4 | 6.8 | 0.43 | i 14 (9%) | 72 | 50.0 | 0.781 | 0.0 | 8.8 | 0.0 | 0.0 | 71.0 | below |
| 03 | 79 | 14.9 | 11.5 | 0.77 | 26.6 | 32.9 | 0.85 | she 27 (34%) | 20 | 15.0 | 0.738 | 0.0 | 15.2 | 0.0 | 0.0 | 61.8 | below |
| 04 | 107 | 11.3 | 10.0 | 0.88 | 43.0 | 20.6 | 0.51 | he 16 (15%) | 38 | 31.6 | 0.805 | 2.8 | 14.0 | 0.0 | 0.0 | 65.1 | below |
| 05 | 143 | 7.8 | 6.9 | 0.89 | 58.7 | 8.4 | 0.53 | i 11 (8%) | 73 | 53.4 | 0.753 | 1.4 | 5.6 | 2.8 | 0.0 | 71.2 | below |
| 06 | 110 | 11.4 | 9.1 | 0.79 | 36.4 | 12.7 | 0.60 | i 10 (9%) | 36 | 30.6 | 0.786 | 0.9 | 10.9 | 0.0 | 0.9 | 76.3 | below |
| 07 | 99 | 10.8 | 12.7 | 1.17 | 58.6 | 14.1 | 0.76 | he 11 (11%) | 50 | 50.0 | 0.790 | 0.0 | 13.1 | 2.0 | 0.0 | 69.4 | below |
| 08 | 101 | 10.8 | 10.9 | 1.02 | 48.5 | 16.8 | 0.60 | he 22 (22%) | 37 | 40.5 | 0.749 | 3.0 | 13.9 | 0.0 | 0.0 | 65.4 | below |
| 09 | 106 | 10.8 | 9.2 | 0.86 | 43.4 | 14.2 | 0.65 | i 23 (22%) | 24 | 16.7 | 0.781 | 1.9 | 17.0 | 0.0 | 0.0 | 61.0 | below |
| 10 | 150 | 8.6 | 9.5 | 1.11 | 63.3 | 8.7 | 0.45 | she 20 (13%) | 59 | 30.5 | 0.779 | 2.0 | 11.3 | 0.7 | 0.0 | 72.8 | below |

What the rhythm numbers show:

- Sentence length varies a lot (CV 0.77–1.17), so F1 length sameness is not the problem.
- All ten samples score below target. Participial phrases run 0–3.9% against a 12% target. Em dashes run 0–2.8%, all of them cut-off speech. Compound `, and` joins run high in 01, 03, 04 and 09 (14–18%). Opus 5.5 joins clauses with `and` where the style guide expects participles and dashes.
- Only 03 crosses the F1 opener threshold (`she` 34%).

## 2. Prevalence

### (a) Patterns the catalogues already cover

| Pattern | Catalogue entry | Samples /10 | Instances |
|---|---|---|---|
| Filter verbs (raw, includes literal perception) | gpt-5 F3; ai-quirks 04 | 10 | 75 |
| Lists of three (narration 20, dialogue 10) | hitlist "triple and chaining" | 10 | 30 |
| Temporal padding (`for a while`, `for a long time`, `at last`) | gpt-5 F3 | 10 | 24 |
| No contractions in narration | ai-quirks 07 | 9 | 64 (against 5 contracted) |
| `and`-chained sentences (3+ `and`) | hitlist "triple and chaining" | 9 | 33 |
| Hedges (`perhaps`, `a little`, `as if/as though`, `something like`, `almost`, `rather`, `seemed`) | gpt-5 F3; ai-quirks 03 | 9 | 27 |
| Negation pivots (P1, P2, P4, P5, P7) | negation guide; hitlist | 9 | 22 KILL (+6 KEEP) |
| Essay-brain paragraphs | gpt-5 F6 | 8 | 16 |
| Closure addiction, incl. false ambiguity | gpt-5 F7 | 8 | 13 |
| Over-translation | gpt-5 F4 | 8 | 11 |
| Eye/gaze reaction beats | RPT Tic 5 | 9 (over cap of 4 in 05, 06, 10) | 31 |
| `like`/`as if`/`as though` similes (checker) | hitlist simile overload | 7 (over cap in 08) | 18 |
| `as if`/`as though` plus an imagined motive | gpt-5 F3; hitlist simile | 6 | 10 |
| Generalizing narration, incl. generic `you` | narrator seep A7 | 6 | 11 |
| Verdict tails (`, which was not allowed`, `Not quickly.`) | narrator seep A1 | 6 | 8 |
| Explanatory colons | ai-quirks 07 | 6 (over cap in 03, 08) | 8 |
| Generic dialogue beats, plus same-mouth speech | gpt-5 F2 | 5 | 9 |
| Counting devices | ai-quirks 10 | 4 | 7 |
| Abstract-noun locomotion | hitlist | 4 | 4 |
| `Something` as vague pointer | hitlist | 4 | 4 |
| Adverb on a speech tag | ai-quirks 06 | 4 | 5 |
| Permission tags | hitlist; intent smear P11; ai-quirks 08 | 3 (2 clear) | 3 |
| Contact verb with agency | hitlist; ai-quirks 09 | 3 | 3 |
| Pleasantness bias | gpt-5 F5 | 3 | 3 |
| Time-skip awareness | narrator seep B3 | 3 | 3 |
| Intent smear | intent smear P4, P8, P10 | 3 | 3 |
| Said-avoidance tags (`agreed`, `added`, `told it`) | RPT Tic 7 | 2 (over cap in 05) | 5 |
| Weight as emotion | RPT Tic 6 | 2 | 2 |
| Slogan or note-speak dialogue | phantom concreteness P1, P5 | 2 | 2 |
| Filler `nodded` | ai-quirks 01 | 2 | 2 |
| Opener monotony over 30% | gpt-5 F1 | 1 | 1 |
| Body-language cliché and breath tell | ai-quirks 02; hitlist breath | 1 | 2 |
| Fake simplification, dialogue register contamination, em dash, corner-of-mouth, tightened/eased, `shifted` | various | 0 | 0 |

### (b) NEW recurring patterns (now F8–F15 in `resources/gpt-5-prose-issues.md`)

| Code | Pattern | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | Samples | Instances |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F12 | Non-action beats | 4 | 2 | 2 | 4 | 1 | 5 | 3 | 4 | 1 | 6 | 10 | 32 |
| F11 | Anaphoric runs | 1 | 4 | 3 | 0 | 3 | 2 | 1 | 3 | 4 | 3 | 9 | 24 |
| F10 | Briefing-stack dialogue | 0 | 3 | 0 | 4 | 3 | 4 | 2 | 0 | 0 | 3 | 6 | 19 |
| F8 | Echo exchange | 1 | 2 | 0 | 0 | 5 | 4 | 5 | 0 | 0 | 1 | 6 | 18 |
| F9 | Name-only lines and vocative tagging | 3 | 5 | 0 | 1 | 0 | 4 | 2 | 0 | 1 | 0 | 6 | 16 |
| F13 | Demonstrative caption | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 2 | 3 | 3 | 6 | 12 |
| F14 | Fenced manner adverb | 0 | 2 | 1 | 1 | 1 | 0 | 2 | 2 | 0 | 0 | 6 | 9 |
| F15 | Dying-fall coda | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 5 | 5 |

Why each of these is NEW rather than covered:

- **F12.** Negation pattern 5 needs a positive pivot after the negation. A standalone `He did not answer.` has none, so no guide catches it.
- **F11.** F1 measures opener sameness over a whole stretch. The hitlist's "triple and chaining" covers `and`-chains inside one sentence, and paragraph-level/09 covers paragraph openers. None covers consecutive sentences opening with the same words for weight.
- **F10.** The hitlist's Document Voice section polices vocabulary. Here the words are plain and the syntax is the report. F2's same-mouth test is the nearest check, and F10 cites it.
- **F8, F9.** No catalogue mentions echoed replies or vocative names.
- **F13.** Narrator seep A1 covers verdict fragments and `, which…` tails, not the complete `That was…` sentence. F6 and F7 catch it only when it closes a paragraph.
- **F14.** Adverb-on-tag covers speech tags only.
- **F15.** F7 explicitly allows a scene to end on image or action, so this cadence passes F7.

## 3. Verdicts on the previously seen tells

| Tell | Verdict | Evidence |
|---|---|---|
| `had the air of someone who…` | Rejected as written (0/10) | The same job is done by `as if`/`as though` plus an imagined motive: 6/10, 10 instances. Covered by F3, simile overload and F4. |
| `, and she let it` | Rejected as written (0/10); the family is present (3/10) | 06 `The Provost let the silence sit.` · 09 `I'd learned to let it go past me like wind.` · 05 `I've let it go, out of affection` (borderline idiom) |
| Negation staccato `She did not look at them. She…` | Confirmed, in two forms | Pivot form: 3/10, 3 instances (`She did not cry. She looked down at the table`). The standalone non-action beat is 10/10, 32 instances, and is now F12. |
| Long chains with `and`, `which` and dashes | Confirmed for `and`; partly for `which`; rejected for dashes | `and`: 33 sentences in 9/10, and 24 sentences of 40+ words. `which`: 26 tails in 9/10, about 8 of them verdict tails (A1). No em dashes in narration in any sample. |
| Report-shaped briefing speech | Confirmed, now F10 | 6/10, 19 |
| Name or rank as a tag on many lines | Confirmed, now F9 | 6/10, 16 |
| Echo exchanges | Confirmed, now F8 | 6/10, 18 |
| Tautology quips | Rejected (2/10) | 03 `A hacksaw was a hacksaw.` · 05 `That was the job. Guarding the cellar was the job.` |
| Triplets | Confirmed, already covered | Dialogue 5/10 (10), narration 9/10 (20). |

## 4. Patterns considered and not added

- **Tautology quips:** 2/10. Below the bar.
- **Generic `you` in third-person narration:** 4/10, 7. Filed under narrator seep A7. A7 now lists it (added after this audit).
- **Disclaimed knowledge** (`could not entirely account for`, `did not know what she was apologising for. All of it, perhaps.`): 5/10. Filed under F7 step 4.
- **`the way…` gloss clauses:** 15 in 9/10. The generic versions are filed under A7, and the ones stacked on a fenced adverb are folded into F14.
- **`than it should have`:** 3/10, but only one is emotional. Not added.

## 5. Files changed

- `resources/gpt-5-prose-issues.md`: "seven" became "fifteen"; table rows, sections, output-format blocks and SUMMARY lines added for F8–F15; a one-line Opus 5.5 marker above F8; self-check updated. F1–F7 are unchanged against `HEAD`.
- `resources/narrator-seep-guide.md`: A7 now lists generic `you` (applied after the audit).
- Checked, no change needed: `.claude/agents/afternoon-slop-gate.md`, `.claude/agents/afternoon-slophunter.md`, `.claude/skills/afternoon-slop-gate-workflow/references/*.md`. `.github/` was not touched.

## Appendix: instance ledger

The full per-sample instance ledger (exact quotes for every finding in all ten samples) is in the auditor agent's hand-back in the session that produced this report. The prevalence tables above summarise it. Re-run the audit on `research/opus-quirks/samples/` to regenerate it.
