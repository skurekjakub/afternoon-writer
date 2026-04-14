# Slop Gate Scratchpad — Chapter 1, Pass A, Iteration 2

**Target:** `v2-r2.md` (416 lines, ~2889 words)
**Verdict:** FAIL (1 MODERATE kill)
**Strategy:** Conservative (iterationKillsA trajectory [8] → 9, non-decreasing)

---

## KEEP Register

### Negation Addiction KEEPs

**KEEP neg-K1 | Lines 125/129**
> "wasn't breaching so much as…" / "Measuring, ma'am."

Binary diagnostic in dialogue. Breaching vs. measuring are mutually exclusive
operational categories that change Sylvanas's military response. Keep condition 1
(binary diagnostic with scene consequence). Deletion test: removing "wasn't breaching
so much as" destroys Cyndia's tactical distinction; the question IS this distinction.

**KEEP neg-K2 | Line 277**
> "she had done it with the ward rather than against it"

Binary diagnostic. Cooperative vs. hostile magic is the core assessment driving
Sylvanas's entire response to the prisoner. Keep condition 1 (binary diagnostic
with scene consequence). Deletion test: "she had done it with the ward" loses the
contrast that makes Sylvanas's military evaluation function.

### Intent Smear KEEPs

**KEEP is-K1 | Line 169**
> "old satisfaction moved through her"

POV emotional metaphor (keep condition 2). No command, judgment, memory, or deception
verb. "Moved through" describes how satisfaction feels physically to a character who
has been alive long enough for emotions to have familiar textures.

**KEEP is-K2 | Line 239**
> "anger had worn down into hard focus"

POV emotional metaphor (keep condition 2). Emotion transforming, not commanding.
"Worn down" is a physical metaphor for emotional attrition — no agency laundering.

**KEEP is-K3 | Line 397**
> "magic had bitten back"

Subject-matter defense + keep condition 3 (literal non-human force). Magic IS an
active force in this setting. "Bitten back" describes literal magical backlash
causing frostbite — the ward-stone system has documented resistance behaviors.

**KEEP is-K4 | Line 413**
> "She let the silence pull tight"

Real agent explicit. Sylvanas is named as the one permitting the silence. Matches
calibration example: "The silence held because she let it" → KEEP.

### Recurring Prose Tics KEEPs

**KEEP tic-K1 | Line 389**
> "Inside:"

Strongest colon use — spatial-perceptual shift. Sylvanas is looking into a holding
cell; the colon enacts a threshold crossing. Retained at cap (2/2).

**KEEP tic-K2 | Line 327**
> "A line in the margin:"

Second-strongest — introduces quoted text from a physical document. The colon is
grammatically correct and serves a different function than catalog-introducing.
Retained at cap (2/2).

**Other tic keeps:** Tic 1 (mouth twitch, line 242) at cap 1/1 — physical,
character-specific gesture. Tic 2 (marked, line 219) at 1/2 — literal physical
description of ink-stained hands. Tic 5 (eye/gaze, 3 instances) at 3/4. All
under cap; all physical and grounded. participial_trailing (3/11), punct_semicolon
(2/5), punct_ellipsis (2/4), simile_as_if (1/5) — all well under cap.

---

## Structural Concerns (informational, not findings)

### Rhythm Profile
The prose has 7 of 8 global rhythm metrics outside style-guide range. Only vocabulary
diversity (MATTR 0.858) is in range.

Critical gaps:
- **comma_period_ratio** 0.304 vs target 0.72 (range 0.6–0.85) — extremely low
  syntactic complexity
- **one_sentence_paragraph_pct** 58.9% vs target 19.0% (range 15–24%) — massive
  single-sentence paragraph overuse (3× ceiling)
- **short_sentence_pct** 60.1% vs target 35.0% (range 28–42%) — telegram prose
- **sentence_length_mean** 7.1 vs target 11.0 (range 9.0–13.0)

### Texture Profile
All 6 texture metrics outside style-guide range. Texture score 6.4% vs floor 22.0%.
- participial_pct 1.5% (floor 9.0%) — nearly absent
- compound_pct 3.9% (floor 7.0%)
- emdash_pct 0.5% (floor 2.5%)
- short_pct 69.9% (ceiling 55.0%)

The prose has a severe structural texture deficit. The slophunter edits may have been
too aggressive — stripping connective tissue along with the slop. Downstream agents
(expander, style-editor) will need to rebuild sentence complexity.

### Slop Checker Signals
- `narrator_verdict` (3 uses, cap 1): Maps to Pass B narrator-seep guide. Not audited
  this pass. The over-cap instances are at lines 9 ("late enough to be decoration")
  and 393 ("too fast for indifference, too controlled for panic" — also killed here
  under negation addiction).
- `punct_colon_narration` (6 uses, cap 2): Handled — 4 killed, 2 retained at cap.

---

## Cross-Check Summary

All 9 KILL fixes were cross-checked against all three Pass A guides:
- No suggested fix introduces a new negation pattern
- No suggested fix introduces intent smear
- No suggested fix introduces a new recurring tic
- 2 fixes replace colons with em-dashes (lines 5, 15), which helps the emdash_pct
  texture deficit (0.5% → closer to 2.5% floor)
- 1 fix replaces colon with period (line 31), 1 with comma (line 65) — varied to
  avoid creating a new repetition pattern

## Duplicate-Line Alert

Line 65 has TWO independent kills:
- neg-1 (negation: "neither setting it, both keeping it")
- tic-1 (colon: "Around them:")

The slophunter should apply both fixes to this line. Combined result:
"Around them, gold leaves that never quite turned, dark water somewhere off the road,
the ward-stones' low note under everything. They rode on at the pace they had fallen
into years ago, both keeping it."
