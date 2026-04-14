# Phase 5: Write Artifacts

Before writing, read `.github/skills/large-file-handling/SKILL.md`.

Use `create` for the initial file structure, then sequential `edit` calls if the notes or scratchpad grow large. Append guide sections sequentially rather than attempting one giant write. Do not return file contents in your response. Write them to disk.

## Notes JSON

Write the notes JSON to the output path resolved in Phase 1.

This is the pipeline artifact consumed by slophunter revision mode. It contains KILL findings only.

Required top-level fields:

- `chapterId`
- `stage`
- `pass`
- `iteration`
- `targetFile`
- `verdict`
- `audits`
- `summary`

Rules:

- every KILL finding includes `suggestedFix`, `fixDifficulty`, and `crossChecked` covering the current pass guide pack
- every KILL finding that was detected or corroborated by the slop checker includes `"toolSignal": "<pattern_name>"` citing the slop_checker pattern that flagged it. This lets the slophunter and human reviewers see which kills had deterministic tool backing
- guides with zero KILLs include `cleanReason`
- guide findings keep the guide-specific fields required by that guide
- the summary block includes `killsWithFix`, `killsUnfixable`, and these analytic sub-blocks from Phase 1b:
  - `rhythmMetrics` — key rhythm metrics + deltas from style-guide targets (comma_period_ratio, sentence_length_cv, one_sentence_paragraph_pct). Note any metrics outside their `range` as "structural rhythm concerns"
  - `textureMetrics` — the full texture verdict, verdict_reasons, interpretation, and flagged passage counts (telegram_run count, texture_desert count). If verdict is "below_target", note "structural texture deficit"
  - `analyticHints.slopChecker` — violation summary (total_violations, over-cap categories)
- pass-with-warnings still includes the remaining MILD findings in the notes JSON for downstream editors

## Scratchpad markdown

Write the scratchpad markdown to the output path resolved in Phase 1.

This is a human-audit artifact only. It contains KEEP findings only, grouped by guide, with the full keep rationale or defense.

Format:

```markdown
# Slop-Gate Scratchpad - chapter1 / pass a (iteration 0)

Target: v2.md

## intent-smear-agency-laundering-guide.md (2 keeps)

**KEEP** | P5 | character-voice
> The camp moved on without her.
Collective actor - camp is people, established in scene. They moved. She didn't.
```

## Status JSON

Write `.afternoon/agents/slop-gate/status.json`.

Use these contracts:

- **Pass / pass-with-warnings**
  - `"status": "completed"`
  - `"verdict": "pass"`
  - `totalFindings` = `0` for a clean pass, or the MILD count for pass-with-warnings
  - `mildFindings` = MILD count
  - `artifacts` lists the notes JSON and scratchpad paths
- **Fail**
  - `"status": "completed"`
  - `"verdict": "fail"`
  - `totalFindings` = total KILL count
  - `mildFindings` = MILD count
  - `artifacts` lists the notes JSON and scratchpad paths
- **Operational failure**
  - `"status": "failed"`
  - `"verdict": null`
  - `artifacts: []`
  - summary explains the operational error

The orchestrator routes on `verdict` when `status` is `"completed"`:

- `verdict: "pass"` -> continue the pipeline
- `verdict: "fail"` -> re-dispatch slophunter revision
- `status: "failed"` -> standard retry-once logic

## Before finishing the run

You should have:
- written the notes JSON to disk
- written the scratchpad markdown to disk
- written `.afternoon/agents/slop-gate/status.json` to disk
