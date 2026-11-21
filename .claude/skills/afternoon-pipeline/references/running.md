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
- `AFTERNOON_MODE`: execution mode (`auto`, `accept-edits`, `plan`; default `auto`)
- `AFTERNOON_MODEL`: optional model slug override (run `agy models` to list available Gemini slugs; leave unset to use `agy` defaults and per-agent tiers)

Run logs are written to `logs/afternoon/agy_gemini_<timestamp>.log`.

### Interactive Usage

```bash
agy --agent afternoon-orchestrator
agy --agent afternoon-outline-builder
agy --agent afternoon-style-extractor
```

### Gemini Model Tier Mapping

Each `.agents/agents/afternoon-*.md` agent is assigned a Gemini tier (`pro` or `flash`), enforced both in frontmatter and in `invoke_subagent` calls:

- **`pro`** (creative prose, prose revision, structural verification, and adversarial gates): `afternoon-plan-verifier`, `afternoon-writer`, `afternoon-writer-craft-auditor`, `afternoon-writer-craft-reviser`, `afternoon-writer-continuity-gate`, `afternoon-slophunter`, `afternoon-slop-gate`, `afternoon-grounder`, `afternoon-grounding-gate`, `afternoon-style-extractor`
- **`flash`** (routers, structured JSON builders, targeted patchers, continuity librarian): `afternoon-orchestrator`, `afternoon-writer-coordinator`, `afternoon-planner`, `afternoon-writer-continuity-writer`, `afternoon-memory-keeper`, `afternoon-outline-builder`, `afternoon-writer-expander`

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