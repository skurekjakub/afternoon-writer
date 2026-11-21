# Phase 3 Route: Pass C Guides

Pass C owns the reader-editor guides. These patterns survive passes A and B because they contain no banned word, no laundered agent and no narrator verdict. They are still sentences a sharp human editor would mark.

- `mannered-prose-guide.md` — bent idioms, literal-sense failures, equative montage, cadence lists with a turn, maxims, comic self-consciousness, self-monitoring beats, interpreter glosses, house wit, planted echo inserts, stylised figures, argument templates, "the way" similes (M1-M13)
- `refrain-guide.md` — cross-chapter reuse, voice-sheet lifts, within-chapter repeats, signature-beat budgets, recycled micro-scenes (R1-R5)

Audit only these two guides in this run.

## Extra inputs for pass C

- The `tools/mannered_checker/check.py --json` report from Phase 1b. Its `patterns` feed the mannered guide, and its `refrains` block feeds the refrain guide.
- The previous chapter's `final.md` (the highest-numbered chapter below this one that has a `final.md`). Read it in full before the refrain audit; R5 depends on it. If no earlier chapter exists, record `"R5": "no previous chapter"` in `cleanReason`.
- The voice sheets for the POV character(s) in this chapter, including their "Shape examples". Phase 2 already loads voice context; for R2, re-read the shape examples verbatim.

## Pass-specific emphasis

- **Read every sentence with the plain-paraphrase test** (mannered guide, Test 1). M2 literal-sense failures have no tool coverage and are the most damaging pattern. Do not sample.
- **The character-voice defense from Phase 2 does not lift a cap.** Voice decides *which* instances of a capped pattern survive. It never decides *how many*.
- **Dialogue is in scope.** Audit spoken lines for answer + reason + maxim stacks (M5) and for joke counts per speaker (M9).
- **Do not double-report pass A/B patterns.** If a sentence's only problem is a pass A or B pattern (a negation pivot, a permission tag, body-part agency, a narrator verdict tag), leave it; those passes own it. Report it here only if it also fails a pass C pattern.
- **Never kill text in earlier chapters.** Refrain findings always target the current chapter's instance.
- **Record cap decisions.** In each guide's audit summary, add `capCounts`. For every capped pattern, give the count, the cap and the line numbers you kept, so the next iteration's fresh sweep can see the survivors were chosen on purpose.

## Before moving to Phase 4

You should have:
- audited both pass C guides
- run Test 1 (plain paraphrase) on every sentence
- read the previous chapter's `final.md` for R5
- applied caps with explicit survivor choices
- kept the run scoped to the pass C guide pack
