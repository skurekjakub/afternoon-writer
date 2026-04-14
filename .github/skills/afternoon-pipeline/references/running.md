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