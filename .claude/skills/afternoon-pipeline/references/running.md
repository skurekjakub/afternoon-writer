# Running The Pipeline

## Before You Start

Make sure these exist:

- `.afternoon/config.json`
- the file named by `storyOverview`
- at least one `chapter-*.md` in `.afternoon/outlines/`
- the style target and priming paths from config
- the voice-sheet directory
- any configured `materials`

## Start

```bash
./afternoon-start.sh
```

The start script checks basic inputs, dispatches the orchestrator, and waits for the completion marker.

## Running on Gemini (Antigravity CLI)

The pipeline also runs natively on Google Antigravity CLI (`agy`) using custom agents in `.agents/agents/afternoon-*.md` and shared skills registered in `.agents/skills.json`.

Prerequisite: install `agy` and authenticate interactively once by running `agy`.

### Autonomous Run (with crash-recovery restart loop)

```bash
./afternoon-start-gemini.sh
```

Optional environment variables:

- `AFTERNOON_EFFORT`: reasoning effort (`low`, `medium`, `high`, `xhigh`, `max`; default `high`)
- `AFTERNOON_SKIP_PERMISSIONS`: passes `--dangerously-skip-permissions` for headless autonomous runs (default `true`; avoids `--mode auto` account-tier blocks)
- `AFTERNOON_MODE`: optional `--mode` override (unset by default; e.g., `accept-edits`)
- `AFTERNOON_MODEL`: optional model slug override (run `agy models` to list available Gemini slugs; leave unset to use `agy` defaults and per-agent tiers)

Output is enforced and validated against `.agents/schemas/orchestrator-result.schema.json` using `--output-format json --json-schema`. Structured stdout and stderr logs are written to `logs/afternoon/agy_gemini_<timestamp>.json` and `.stderr.log`. A fatal `"status": "error"` exits non-zero cleanly instead of reporting false completion.

### Interactive Usage

```bash
agy --agent afternoon-orchestrator
agy --agent afternoon-outline-builder
agy --agent afternoon-style-extractor
```

### Lean Gemini Pipeline Flow & Model Tier Mapping

The Gemini pipeline in `.agents/agents/` uses a lean 6-step chain per chapter (`v0.md -> v1.md -> v2.md -> final.md`):

1. `afternoon-planner` (`flash`) → `.afternoon/plans/{chapterId}-initial.json`
2. `afternoon-plan-verifier` (`pro`) → `.afternoon/plans/{chapterId}.json`
3. `afternoon-writer-coordinator` (`flash`) → dispatches `afternoon-writer` (`pro`) per scene (`v0.md`), then `afternoon-writer-continuity-gate` (`pro`) ↔ `afternoon-writer-continuity-writer` (`flash`) (max 3 iterations → `v1.md`)
4. `afternoon-slophunter` (`pro`) → primary cleanup (`v1.md -> v2.md`) backed by `python3 tools/prose_check.py --json`
5. `afternoon-slop-gate` (`pro`) ↔ `afternoon-slophunter` (`pro`, revision mode) → single combined pass (max 3 iterations; covers Gemini prose tics, over-textured runs, mannered prose/refrains, POV/agency/negation)
6. Promote `v2.md -> final.md` → `afternoon-memory-keeper` (`flash`) updates `.afternoon/plans/memory/`

Craft-audit, grounder/grounding-gate, expander, and final-slophunter are omitted from `.agents/agents/` (they remain intact in `.claude/agents/`).

Per-agent Gemini tier (`pro` or `flash`), enforced both in frontmatter and in `invoke_subagent` calls:

- **`pro`** (creative prose, prose cleanup, structural verification, and adversarial gates): `afternoon-plan-verifier`, `afternoon-writer`, `afternoon-writer-continuity-gate`, `afternoon-slophunter`, `afternoon-slop-gate`, `afternoon-style-extractor`
- **`flash`** (routers, structured JSON builders, targeted continuity patcher, continuity librarian, outline builder): `afternoon-orchestrator`, `afternoon-writer-coordinator`, `afternoon-planner`, `afternoon-writer-continuity-writer`, `afternoon-memory-keeper`, `afternoon-outline-builder`

## What To Watch

- `.afternoon/manifest.json`: current chapter, current agent, overall status
- `.afternoon/agents/*/status.json`: per-agent success or failure
- `.afternoon/chapters/{chapterId}/`: draft and audit artifacts
- `logs/afternoon/`: run logs

Useful checks:

```bash
cat .afternoon/manifest.json
ls .afternoon/agents/*/status.json
ls .afternoon/chapters/*
```

## Done Means

- the completion marker was printed
- `manifest.json` says the run is completed
- each finished chapter has `.afternoon/chapters/{chapterId}/final.md`

## Practical Notes

- To run only some chapters, keep only those outline files in `.afternoon/outlines/`.
- To add chapters later, add the outlines and restart the run with the manifest back in progress.
- The full pipeline is slow and expensive; grounding and gate loops are the biggest multipliers.