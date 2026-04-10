# Chapter 12 Benchmark Comparison - final.md vs grounded-v2 vs grounded-v3

## Scope

Compared:

- `.afternoon/chapters/chapter12/final.md`
- `.afternoon/chapters/chapter12/final-grounded-gpt-negative-v2.md`
- `.afternoon/chapters/chapter12/final-grounded-gpt-negative-v3.md`
- `.afternoon/chapters/chapter12/grounder-notes-gpt-negative-v2.json`
- `.afternoon/chapters/chapter12/grounding-map.json`
- `.afternoon/chapters/chapter12/grounder-notes.json`

The goal here is not just "which prose sounds better." The real question is whether the new map-driven grounder design produces a materially better grounding pass than:

1. the ungrounded baseline (`final.md`)
2. the prior grounded benchmark (`final-grounded-gpt-negative-v2.md`)

---

## File stats

| File | Lines | Words | Notes claim |
|---|---:|---:|---|
| `final.md` | 547 | 3972 | baseline |
| `final-grounded-gpt-negative-v2.md` | 529 | 4019 | notes file reports `4044` / `1.8%` growth |
| `final-grounded-gpt-negative-v3.md` | 551 | 4258 | notes file reports `4258` / `7.2%` growth |

Important note: the v2 notes file's wordcount metadata does **not** match the actual file on disk. The v3 notes file does.

---

## Executive verdict

`final-grounded-gpt-negative-v3.md` is still the strongest **process benchmark**, but the prose result is a closer call than the first pass suggested.

Why:

1. It makes the sanctum feel most like a real working room instead of a generic debate chamber.
2. It improves the chapter's room logic and scene infrastructure more intelligently than v2.
3. It feels less like noun substitution than v2. The detail is more often routed through infrastructure, contact, and pressure.
4. The new `grounding-map.json` looks like a real execution scaffold, and the prose quality tracks that improvement.

The main remaining weakness is still the same one the map predicted:

- the long ethics/ban/mirror argument in the middle remains partially abstract
- dialogue embodiment is improved, but not fully solved
- the **very end** of the Sylvanas-approach sequence is lighter than v2 and in places much closer to the source than the notes imply

So the verdict is not "v3 solved everything." It is:

**v3 is the best foundation to tune the prompt against, but v2 still outperforms it in late-scene enrichment density at the tail.**

---

## Zone-by-zone comparison

## 1. Opening / sanctum establishment

### Baseline (`final.md`)

The baseline is already competent, but still partly portable:

- `final.md:3` - "an office at the bottom of a grave"
- `final.md:5-9` - good shelves/folios/jars/chalk texture, but the room still reads as a generalized necromancer workspace

### Prior grounded benchmark (`v2`)

v2 pushes named/world-bound specificity hard and immediately:

- `v2:3-6` - "Caer Darrow's old crypt spine," "grave-fungi," "brass retorts," "preserving salts"
- `v2:9` - "Violet Citadel"
- `v2:13` - "vellum page," "river-stone paperweight"

This is clearly stronger than the baseline, but it sometimes reads like a better noun pack dropped onto the same scene skeleton.

### Current benchmark (`v3`)

v3 is the best-integrated version of the opening:

- `v3:3-6` - "Scholomance's old crypt spine," "Darrowmere's cold came up through the flagstone," "air itself had been dried and salted against rot," "hidden stair below Caer Darrow"
- `v3:9` - Antonidas's marks now extend to jar labels, not just abstract "every surface"
- `v3:25` - ward lines are felt through the table before they are heard

This is the key improvement over v2: the room is not just better named. It is more physically inhabited.

**Verdict:** `v3 > v2 > final`

---

## 2. Mechanism lesson + ethics duel

This is the hardest section in all versions because the chapter is fundamentally a scholar-duel in one room.

### Baseline (`final.md`)

The baseline is clean and readable, but it relies heavily on conceptual clarity:

- `final:141-179`
- `final:181-223`

There are anchors, but the scene still risks becoming argument in empty air.

### Prior grounded benchmark (`v2`)

v2 adds real value here:

- `v2:137-170` - Council of Six, stronger institutional frame
- `v2:197-223` - ridge blood memory, Violet Citadel reference, labeled boxes, Antonidas notation

But the pass still feels mostly substitutional. It adds named context and material cues, yet the underlying conversational float remains only partly interrupted.

### Current benchmark (`v3`)

v3 is better again, but this is also where its limit shows most clearly:

- `v3:163-175` - "smooth from years of sleeves, wrists, and spread pages," plus palm-up folio/table handling
- `v3:203-205` - ridge blood memory carried into Jaina's body
- `v3:227-230` - shelf contact, dry wood, cool, solid

These are good corrections. But the middle duel still has long stretches where the force comes mainly from clean argument rather than load-bearing physical beats:

- `v3:141-176`
- `v3:181-225`
- `v3:261-279`

So v3 improves the zone, but does **not** fully cure it.

**Verdict:** `v3 > v2 > final`, but only narrowly. This remains the benchmark's unresolved weakness.

---

## 3. Mirror / Antonidas wound

This is where the structural difference between v2 and v3 becomes obvious.

### v2

The v2 notes collapse the chapter into three big zones:

1. sanctum/threshold
2. mechanism/ethics/scale
3. Sylvanas's approach

The mirror material is inside the large mid-chapter block. The prose improves, but the pass does not appear to treat the Antonidas wound as its own grounding problem.

### v3

The v3 map isolates this as **Scene 3: The Mirror** and identifies the exact risk:

- mentor wound
- mirror-scene
- contactless dialogue risk

That shows up in the prose:

- `v3:281-294` - chair scrape, return to the table, page exposure

This is not a huge visible rewrite, but it is a better diagnosis and a cleaner execution model.

**Verdict:** v3 is structurally smarter here even where the prose delta is subtle.

---

## 4. Lich King / Burning Legion reveal

### Baseline (`final.md`)

The baseline reveal is already strong, but it skews toward briefing clarity:

- `final:303-353`

The scene works because the chapter itself is strong, not because the room is doing much extra work.

### Prior grounded benchmark (`v2`)

v2 increases named/world-binding aggressively:

- `v2:287-345` - stronger Lordaeron/Northrend/Council framing, more cosmological naming, more material nouns around folios and fungi

Useful, but occasionally close to "better lore nouns" rather than deeper scene embodiment.

### Current benchmark (`v3`)

v3 keeps the reveal personal and room-bound more consistently:

- `v3:295-307` - new diagram framing remains desk-bound
- `v3:315-355` - table-edge pressure, named scale, treated grain under tarpaulin, institutions slowing to classification
- `v3:373-387` - Darrowmere beyond the wall, final folio tightening the room again

This is the better balance:

- still legible
- still named
- less list-like than v2
- more physically staged than baseline

**Verdict:** `v3` is slightly ahead of `v2`, and clearly ahead of `final`.

---

## 5. Final third / Sylvanas approach

This is the most important comparison zone, because the redesign specifically targeted tail attenuation.

### Baseline (`final.md`)

The baseline ending is already one of the chapter's strongest passages:

- `final:499-547`

It has pulse, ward response, stair/landing progression, and a clean Sylvanas recognition.

### Prior grounded benchmark (`v2`)

v2 sharpens route geometry and material identity aggressively:

- `v2:497-529` - Caer Darrow flagstone, crypt spine, Scholomance protections, ward-stones, leather boots, Barov stone

This is not just "more nouns." The route, surface, and mover identity all become clearer.

### Current benchmark (`v3`)

v3 still does good work in the **recurrence** subsection just before the approach:

- `v3:431-447` - chair blow, breath, wound held physically

But once the actual approach sequence starts, v3 becomes much lighter and in places reverts close to the source:

- `final:509-547` and `v3:513-552` are very close at the sentence-structure level
- where v2 says `Caer Darrow flagstone`, `Scholomance's old protections`, `leather boots`, and `Barov stone`, v3 often falls back to `floor`, `sanctum's old protections`, `a body`, and `stone`

So the important correction is:

- v3 does **not** win the tail on local enrichment density
- v2 is the stronger final-approach benchmark
- v3's tail strength is mostly rhythm protection plus a few structural clarifications, not sustained enrichment

**Verdict:** `v2 > v3 > final` for the actual Sylvanas-approach subsection of the final third.

---

## Scaffolding comparison: v2 notes vs v3 map + notes

## v2 scaffold quality

`grounder-notes-gpt-negative-v2.json` is useful but retrospective and broad:

- 3 large scene buckets
- mostly lists added anchors
- less explicit risk modeling
- no scene contract fields
- inaccurate wordcount metadata

This is enough for a post-hoc summary, but not enough to prove the pass was guided scene-by-scene.

## v3 scaffold quality

`grounding-map.json` is materially better:

- explicit chunking reason (`3972` words / `5` scenes over thresholds)
- global risks (`dialogue-heavy`, `static-room`, `tail-risk`, etc.)
- per-scene `biggestGap`
- per-scene source banks
- five-part scene contract:
  - place anchor
  - material anchor
  - POV anchor
  - dialogue anchor
  - exit anchor
- explicit dialogue runs and risk levels

`grounder-notes.json` then reports against that same structure:

- 5 scenes, not 3
- per-scene touch counts
- per-scene summaries aligned with the map
- accurate wordcount metadata

This is the strongest evidence that the new design is not just theoretically cleaner. It produced a cleaner benchmark artifact and a more trustworthy audit trail.

---

## Failure-surface assessment

Using the grounding evaluation surface:

### Baseline (`final.md`)

Residual risk:

- mild G2 / G6 in the opening because the room is not fully world-bound yet
- mild G3 / G5 through the middle because the duel is intellectually clean
- no major G7 tail attenuation problem; the source ending was already structurally strong

### v2

v2 reduces G2/G6 well, especially through immediate naming and room dressing.

But it sometimes feels like it solves grounding by upgrading nouns rather than re-binding the whole beat. That keeps some G3/G4/G5 pressure alive in the middle.

### v3

v3 mostly clears the chapter on:

- G1 white-room paragraphs
- G2 generic noun fallback
- G6 institutional/geographic underbinding
- G7 tail attenuation relative to the baseline source
- G9 over-grounding/noun spam

The main residual weaknesses are:

- mild G3 contactless dialogue runs
- mild G4 positionless conflict
- mild G5 abstract operational language
- a lighter-than-promised final approach sequence when compared against v2 and against the v3 notes/map ambitions

So the middle remains the primary problem, but the tail now needs a more precise note: **v3 preserves the ending better than it enriches it.**

---

## Comparative ranking

## Best opening
1. `v3`
2. `v2`
3. `final`

## Best middle
1. `v3`
2. `v2`
3. `final`

Gap between 1 and 2 is real but not huge. This is still the chapter's hardest zone.

## Best final third
1. `v2`
2. `v3`
3. `final`

## Best scaffold / explainability
1. `v3`
2. `v2`
3. `final` (no grounder scaffold)

## Best overall benchmark

Split verdict:

- **Best prompt/process benchmark:** `v3`
- **Best tail-enrichment exemplar:** `v2`
- **Best raw source chapter:** `final`

---

## Prompt implications

The main takeaway is **not** "add even more specificity."

The main takeaway is:

1. **Map-before-modify works.** Keep it.
2. **Chunked mode + final-third audit are not sufficient by themselves.** v3 proves the map can diagnose the tail, but the actual late-pass execution can still collapse back toward source language.
3. **Scene-contract grounding beats noun substitution.** v3 wins because it grounds through room systems, pressure objects, and contact, not because it simply adds more proper nouns.
4. **Next gains are in dialogue embodiment and tail-delta enforcement.** The remaining work is mostly in the long ethics/ban argument runs plus the very late Sylvanas-approach subsection where v3 under-enriches relative to v2.

If iterating again, target:

- 2-4 more load-bearing physical/relation beats in Scene 2 and early Scene 4
- an explicit "late-section delta check" against source so the final approach cannot silently revert to near-baseline phrasing
- object pressure and hierarchy, not extra lore nouns
- preservation of clipped syntax **without** defaulting back to source-generic nouns like `floor`, `body`, and `stone`

Do **not** respond to the remaining weakness by widening the pass everywhere. The opening and ending are already where they should be.
