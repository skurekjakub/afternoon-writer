# AI Quirks Reference Library

A categorized library of ~850 bad/good prose example pairs, organized by anti-pattern type. Editor agents read relevant files before editing to cross-check their work against concrete examples.

## How Agents Should Use This

### Slop Editor (v1 → v2)
Read ALL sentence-level files (01-13) before editing. These are your primary hunting targets. Skim paragraph-level (08-11) for context.

### Expander (v2 → v3)
Read paragraph-level files (08-11) before expanding. When expanding near transitions, also read scene-level (12-16). Expansion must not introduce quirks — check 01-07 after expanding.

### Style Editor (v3 → v4)
Read ALL files. You're the full-spectrum quality check. Sentence-level for word choices, paragraph-level for structure, scene-level for emotional architecture.

### Final Editor (v4 → v5)
Read scene-level files (12-17) as primary. Skim sentence-level (01-07) for any survivors. Your job is the macro patterns that earlier editors might have introduced while fixing micro patterns.

### Writer (raw draft)
Read sentence-level (01-07) and paragraph-level (08-11) before writing. Prevention is cheaper than cure. These are the patterns your model will default to — knowing them helps you avoid them.

## Structure

### sentence-level/ (files 01-07)
Word and phrase-level patterns. Most granular, most enforceable.

- **01-filler-actions.md** — nodded/sighed/smiled/shrugged/glanced/frowned + stacking
- **02-body-language-cliches.md** — raised eyebrow, crossed arms, clenched jaw, etc.
- **03-hedging-tentative.md** — seemed to, appeared to, almost, might have been, something like
- **04-filter-words.md** — she noticed/realized/saw/heard/knew/decided/wondered/remembered
- **05-ai-vocabulary.md** — delve, tapestry, ethereal, palpable, cascaded, emboldened
- **06-said-bookisms.md** — dialogue attribution: bookisms, adverb-on-tag, beat overload
- **07-punctuation-tics.md** — em dash clusters, semicolons, no contractions, length uniformity
- **08-permission-tags.md** — `she let it`, `let it settle`, `let the fear do its work`
- **09-contact-verb-agency.md** — body parts that `found`, discovery-wrapper `found`, sensations that `settled`
- **10-counting-devices.md** — counted strides, heartbeats and arrows, clock minutes, distances by number
- **11-unplaceable-then-placed.md** — `a smell she couldn't place, [identifies it]`; disclaimed then answered
- **12-claim-then-gloss.md** — statement then a sentence that explains, caps or puns on it; `Which left X.`; `Close enough to reach. Close enough to be reached.`
- **13-no-look-handoff.md** — `Without looking, she held X out. Y took it.`

### paragraph-level/ (files 08-11)
Paragraph rhythm, structure, and grounding. Requires reading 3-5 paragraphs in context.

- **08-density-modulation.md** — every sentence beautiful, no breathing room, poetic overload
- **09-opener-repetition.md** — "She" / "The" starting every paragraph, gerund/clause repetition
- **10-essay-structure.md** — topic-sentence → support → conclusion in fiction paragraphs
- **11-white-room-syndrome.md** — setting vanishes, dialogue floats in void, no re-grounding

### scene-level/ (files 12-17)
Emotional architecture across a scene. Requires reading the full scene to diagnose.

- **12-emotional-throughline.md** — emotion resets between paragraphs, no accumulation
- **13-emotional-register.md** — all-earnest/all-poetic/all-intense with no tonal counterpoint
- **14-monologue-overload.md** — 5+ sentences of thinking, self-therapy, summary-not-drama
- **15-resolution-too-fast.md** — apology → forgiveness same scene, anger-but-understood
- **16-emotional-whiplash.md** — sad → happy with no bridge, mood switches with no residue
- **17-mixed-metaphors.md** — domain collision, extended metaphor switches, metaphor overload

## File Format

Each file contains ~50 bad/good example pairs grouped by sub-variant. Every pair has:
- **Bad** — the AI-pattern example
- **Good** — a rewrite that fixes it
- **Why** — 1-2 sentence explanation of what changed and why
