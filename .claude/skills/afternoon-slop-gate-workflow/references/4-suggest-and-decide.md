# Phase 4: Suggest and Decide

After all guide audits are complete, turn every KILL into an actionable revision target and compute the pass verdict.

## Cross-validated suggestions

For each KILL finding across all guides:

1. Write a concrete replacement for the flagged text. Do not describe the fix - write the replacement.
2. Re-read every guide in the current pass guide pack, not just the guide that flagged the line.
3. Verify that the replacement does not introduce a new violation under any guide in that same pass pack.
4. If the replacement fails a guide, revise it and cross-check again.
5. If you cannot produce a clean fix after the allowed attempts, set:
   - `suggestedFix: null`
   - `fixDifficulty: "high"`

Every KILL must end with:

- `suggestedFix` - concrete replacement text or `null`
- `fixDifficulty` - `"low"` when `suggestedFix` is non-null, `"high"` when it is null
- `crossChecked` - array of every guide filename in the current pass pack that you validated the fix against

## Suggestion quality rules

- Preserve the scene's meaning and the POV character's voice.
- Do not add exposition, new observations, or extra content.
- Make the fix drop-in replaceable at the same approximate position in the paragraph.
- Prefer deletion when the flagged text is decorative scaffolding.
- When one sentence attracts kills from three or more guides, consider deletion before attempting a creative rewrite.

## Iteration-aware fix conservatism

Before finalizing suggestions, read `.afternoon/manifest.json` and inspect the pass-specific trajectory:

- pass `a` reads `slopGateLoop.iterationKillsA`
- pass `b` reads `slopGateLoop.iterationKillsB`

Use the trajectory after detection, not during detection.

- **Default strategy**: no prior history, or counts strictly decreasing. Full rewrites are allowed. Use up to three attempts before marking the fix unfixable.
- **Conservative strategy**: the latest count is greater than or equal to the minimum prior count. The loop is oscillating. Switch to:
  - prefer deletion over rewrite
  - prefer minimal word substitution over sentence restructuring
  - prefer shorter fixes
  - lower the unfixable threshold to two attempts

This strategy shift never changes what you flag. Every audit is still a fresh sweep.

## Final verdict

1. Compile per-guide summaries from the accumulated findings.
2. Count MODERATE and SEVERE kills separately from MILD kills.
3. Decide the verdict:
   - any MODERATE or SEVERE kill -> `verdict: "fail"`
   - more than 3 MILD-only kills -> `verdict: "fail"`
   - 3 or fewer MILD-only kills and zero MODERATE/SEVERE kills -> `verdict: "pass"`
   - there is no FLAG category; all guides resolve to KILL or KEEP
4. Finalize the notes JSON summary with:
   - `totalKills`
   - `totalKeeps`
   - `mildKills`
   - `moderateOrSevereKills`
   - `guidesRun`
   - `guidesWithKills`
   - `killsWithFix`
   - `killsUnfixable`
   - `verdict`
   - `verdictReason`
5. Finalize the scratchpad content with all KEEP decisions grouped by guide.

## Before moving to Phase 5

You should have:
- a `suggestedFix`, `fixDifficulty`, and `crossChecked` value for every KILL
- the verdict computed for the current pass
- finalized notes JSON content in memory
- finalized scratchpad content in memory
