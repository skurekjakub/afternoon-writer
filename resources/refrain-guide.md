# Refrain Hunt Guide — LLM Adversarial Edition

## Your role and stance

Every other guide audits one chapter in isolation. This one audits the chapter **against the book**. A model writing chapter 6 has read chapter 5 (the writer reads the prior chapter's `final.md` for continuity) and the voice sheets, and it reaches for what worked there. The result is a book that keeps saying the same clever thing.

Real cases from chapters 1-5:

- **The yardstick.** "She'd have flayed a ranger for that excuse" (Ch 1). Then "She'd have had the hide off any ranger who sent a warning on that" (Ch 3), "She would have flayed a ranger for that" (Ch 3, again), and "She had taken the skin off him for it in front of his post" (Ch 5). About eleven uses in five chapters. Jaina got her own copy: "She'd have sent a first-year back to his bench for it."
- **Voice-sheet lifts.** The sheet's shape example "*Brilliant, Jaina. Antonidas's prize student, and a ranger read the boot prints before she did.*" became "Brilliant, Jaina. Antonidas's prize student, talking down to a woman a mile ahead of her" (Ch 2), and then "Brilliant, Jaina. Antonidas's prize student, sure as stone with nothing in her hands to prove it" (Ch 4).
- **Recycled micro-scene.** Lyriel jokes, Jaina laughs "short and surprised", Lyriel glances at Cyndia, and Cyndia is watching the hedge. This happens in Ch 2, and again in Ch 5 with the trees.
- **Recycled openings.** "She had not slept since the night before the troll hollow. Her eyes were full of sand" (Ch 3) became "Her eyes felt rubbed with sand. She had not slept since the night before the village" (Ch 5).
- **Tag phrases.** Cyndia stands or reports "with her weight even" at almost every appearance. Humans look at the elves' ears five times in Ch 5. Jaina gets on and off a horse "badly, as always."
- **Recycled similes.** "It was like biting a boot" (Ch 2), then "It's like standing in a boot" (Ch 5). "Soft as an overripe plum" (Ch 2), then "an overripe plum" (Ch 4). "a bird's foot" (Ch 3 and Ch 5).

Each instance is fine on its own page. Together they turn the book into a set of tics. **Default stance: the second use of a signature move is guilty.**

---

## Core definition

**Refrain:** wording, an image, a joke, or a beat sequence that the book has already used, appearing again without the text treating it as a deliberate callback.

**Signature move:** something a reader would notice and remember, such as a figurative phrase, a joke, a simile, a self-judgment, a reaction beat or a character tag. Plain physical vocabulary for recurring objects is not a signature move. "The heel of the staff", "the crook of her dead arm" and "the crown of the road" are continuity, not refrains.

---

## Inputs

1. The `refrains` block from `tools/mannered_checker/check.py --json` (Phase 1b):
   - `crossChapter`: word runs shared with earlier chapters' `final.md`
   - `voiceSheet`: word runs lifted from voice sheets
   - `withinChapter`: word runs repeated inside this chapter
   - `families`: known signature beats with their budgets (`overBudget`, `countHere`, `windowTotal`, `bookCounts`)
2. The **previous chapter's** `final.md`, read in full, for the R5 sweep. It is the writer's direct source.
3. The voice sheets for the POV characters, including their "Shape examples" sections.

---

## Decision procedure

### Step 1 — Is it a signature move?

For each tool candidate, and for each move you notice in your own read:

- A figurative phrase, joke, simile, self-judgment, reaction beat or character tag counts. Go to Step 2.
- Plain description of a recurring object, place or formation counts once per chapter ("Sylvanas in front, Cyndia on the left, Lyriel on the right"). It is continuity. KEEP, and note it in the scratchpad.

### Step 2 — Is the repeat deliberate?

KEEP only when **the text marks the callback**:

- a character quotes or remembers an earlier line, usually in italics ("*Empty going up, full coming down.* She'd thought that on the Millhaven bridge");
- the chapter plan or outline requires the motif (check `continuityStatus`, `memoryRef` and the beat's motif notes);
- the repeat is the point of the scene, for example a ritual phrase, a formal address, or a spelled name.

A callback the reader would not notice as a callback is not deliberate. It is a refrain.

**Plan-named beat over budget.** When the chapter plan names a signature beat (for example "she measures this against what she'd do to a ranger"), KEEP exactly one instance, the one that does the plan's job, even if the family is over budget. KILL every other instance in the chapter. Mention the plan's beat in the finding's `reason` so a human can see that the plan keeps reseeding it. The plan licenses one beat. It does not license its wording: if the kept instance reuses an earlier chapter's phrasing, still fix the phrasing (R1).

### Step 3 — Budget

For refrain families in the tool output, `overBudget: true` means the chapter's use is over the family's per-chapter or rolling budget. KILL the weakest instance in this chapter. **Never kill an earlier chapter's instance; those are published.**

For signature moves without a family, use these defaults:

- **Cross-chapter verbatim run** (R1): KILL in this chapter unless Step 2 clears it.
- **Voice-sheet lift** (R2): KILL. Shape examples show the shape of a thought, not its words. Even a near-verbatim paraphrase of a shape example is a lift.
- **Within-chapter repeat** (R3): KILL the second occurrence of a figurative phrase, simile or reaction beat. Repeated plain description is fine.
- **Recycled beat** (R4/R5): KILL when the same beat sequence (setup, reaction, reaction to the reaction) appeared in the previous chapter or within the last three chapters per `bookCounts`.

---

## Pattern catalog

### R1 — Cross-chapter verbatim reuse — MODERATE

A run of five or more words (excluding names) shared with an earlier chapter, that is not ordinary English (the tool drops runs that occur in the human corpus).

> She had not slept since the night before the village... *(Ch 5; Ch 3 has "She had not slept since the night before the troll hollow.")*

**Fix:** write this chapter's version from this chapter's facts. Here, the bitten fingers and the flour in her glove seams are new. Do not paraphrase the old line; a paraphrase keeps the refrain.

### R2 — Voice-sheet lift — MODERATE

Wording or a distinctive image lifted from a voice sheet's shape examples, quoted lines or trait descriptions.

> Brilliant, Jaina. Antonidas's prize student, sure as stone with nothing in her hands to prove it.

**Fix:** usually deletion. In Ch 4 the line before it already does the work: "What would she show anyone, if anyone asked? A taste, a crystal that clicked, and her own face going green." If the trait has to show, give it a form tied to this scene's evidence. Do not swap in a fresh quip, which is M9 in the mannered-prose guide.

### R3 — Within-chapter repeat — MILD (MODERATE if 3+ uses)

The same figurative phrase, simile, reaction or tag twice in one chapter.

> "Garran's breath caught at the top, and caught, and caught." *(twice in Ch 4)*
> "the sun... lying across the floor in a long bright slab" *(twice in Ch 5)*

**Fix:** keep the first or the stronger one. Replace the other with a different particular, or cut it.

### R4 — Family over budget — MILD per instance (MODERATE if `windowTotal` ≥ 3× `perWindow`)

A known signature beat past its budget (`families[].overBudget`). The yardstick, the blush, the ears stare, the weight-even tag, the empty places at the back, the no-sleep opener, the short surprised laugh.

**Fix:** cut the beat, or replace it with something this scene's evidence supports. When Sylvanas judges herself, use the actual cost in front of her ("A day north and a day back"), not the imagined ranger she would punish.

### R5 — Recycled micro-scene — MODERATE

A beat *sequence* reused from the previous chapter, even in fresh words. Read the previous chapter's `final.md` and list its five most distinctive beats: jokes and their reactions, arrivals, self-judgments, chapter-opening moves, chapter-closing images. Then check this chapter for each one.

> Ch 2: Lyriel's joke → Jaina "laughed before she could help it, a short surprised sound" → "Lyriel glanced at Cyndia. Cyndia was watching the hedge and gave no sign of having heard a word."
> Ch 5: Lyriel's joke → "The mage laughed. It came out short and surprised" → "Lyriel turned to Cyndia. Cyndia was watching the trees..."

**Fix:** keep the joke and change what happens next, using a reaction only this scene could produce. If the voice sheet requires the beat (Lyriel checks whether a joke landed), cap it at one per three chapters and vary the response.

---

## Severity and verdict input

| Code | Pattern | Severity |
|---|---|---|
| R1 | Cross-chapter verbatim reuse | MODERATE |
| R2 | Voice-sheet lift | MODERATE |
| R3 | Within-chapter repeat | MILD (MODERATE at 3+) |
| R4 | Family over budget | MILD (MODERATE at 3× window budget) |
| R5 | Recycled micro-scene | MODERATE |

---

## Output format

Each KILL finding in the notes JSON:

```json
{
  "id": "C-R4-1",
  "line": 417,
  "text": "She had taken the skin off him for it in front of his post.",
  "pattern": "R4 - family over budget (subordinate_yardstick)",
  "source": "chapter3/final.md lines 576, 792; chapter1/final.md line 67",
  "verdict": "KILL",
  "severity": "MILD",
  "reason": "Seventh yardstick beat in five chapters; windowTotal 7 against a budget of 1 per 3 chapters.",
  "suggestedFix": "",
  "fixNote": "Delete the sentence. The sentence before it ('She had heard that excuse from a ranger once, at the Pass...') already carries the memory.",
  "fixDifficulty": "low",
  "crossChecked": ["mannered-prose-guide.md", "refrain-guide.md"],
  "toolSignal": "family:subordinate_yardstick"
}
```

---

## Adversarial self-check

1. Did you read the previous chapter's `final.md` for R5, or only the tool output?
2. Did you KEEP a repeat as "a callback" when the text gives the reader no sign that it is one?
3. Did you replace a refrain with a paraphrase of the same beat? A paraphrase is still the refrain.
4. Did you kill plain continuity vocabulary as a refrain? Don't.
5. Did you check the chapter's opening and closing paragraphs against the previous chapter's? Openings and closings are where the writer copies most.
