# Troubleshooting

Common failures, how to diagnose them, and how to fix them.

## Reading Status Files

Every agent writes `.afternoon/agents/{name}/status.json` on completion or failure:

```json
// Success
{
  "agent": "writer",
  "chapterId": "chapter-1",
  "status": "completed",
  "artifacts": [".afternoon/chapters/chapter-1/v1.md"],
  "summary": "Chapter written from 33 beats across 5 scenes."
}

// Failure
{
  "agent": "writer",
  "chapterId": "chapter-1",
  "status": "failed",
  "error": "Missing plan file: .afternoon/plans/chapter-1.json not found"
}
```

To check pipeline state, read status files:
```bash
for f in .afternoon/agents/*/status.json; do echo "=== $f ==="; cat "$f"; echo; done
```

## Reading the Manifest

`.afternoon/manifest.json` tracks overall progress:

```json
{
  "status": "in-progress",
  "currentChapter": "chapter-2",
  "currentAgent": "writer",
  "progress": {
    "chaptersCompleted": 1,
    "chaptersTotal": 3
  },
  "log": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "chapter": "chapter-1",
      "agent": "planner",
      "status": "completed",
      "artifacts": [".afternoon/plans/chapter-1-initial.json"]
    }
  ]
}
```

Key fields:
- `currentChapter` + `currentAgent`: where the pipeline stopped
- `blocked`: chapters that failed twice and were skipped
- `chaptersCompleted`: how many chapters finished successfully

## Common Failures

### "Missing plan file" / "Missing config"

**Symptom:** Agent status shows `"failed"` with "not found" error
**Cause:** Previous agent didn't produce its output, or file path is wrong
**Fix:**
1. Check if the previous agent's status shows "completed"
2. Check if the expected file actually exists at the path
3. If previous agent completed but file is missing → the agent wrote to the wrong path. Check the agent file for path mismatches.
4. If previous agent didn't complete → the orchestrator skipped it incorrectly. Check crash recovery logic.

### Agent produces output but orchestrator doesn't see it

**Symptom:** Orchestrator re-dispatches an agent that already succeeded
**Cause:** The orchestrator checks `status.json`, not output files. The agent may have written v1.md but failed to write status.json (crash mid-write).
**Fix:** Manually write the status.json file for the agent, then restart the pipeline.

### Chapter marked "blocked"

**Symptom:** Manifest shows a chapter in the `blocked` array
**Cause:** An agent failed twice for that chapter
**Fix:**
1. Read the failed agent's status.json to find the error
2. Fix the underlying issue (missing input, config error, etc.)
3. Remove the chapter from the `blocked` array in manifest.json
4. Set `currentChapter` to that chapter and `currentAgent` to the failed agent
5. Restart the pipeline — crash recovery will pick up from there

### Crash recovery loops

**Symptom:** Pipeline keeps restarting and re-dispatching the same agent
**Cause:** Agent fails consistently (same error each time)
**Fix:**
1. Read the start script logs in `logs/afternoon/`
2. Find the agent's error in status.json
3. Fix the root cause before restarting

### Memory files are stale or corrupted

**Symptom:** Writer or style-editor references incorrect facts
**Cause:** Memory-keeper failed or was skipped, so memory files are from an older chapter
**Fix:**
1. Check memory-keeper's status.json — did it complete for the expected chapter?
2. If it failed, fix the issue and re-run it manually (dispatch as `afternoon-memory-keeper` with the correct chapterId)
3. If memory files exist but are wrong, delete them and re-run the memory-keeper

### ContinuityStatus annotations are wrong

**Symptom:** Writer treats established info as new, or callbacks reference nothing
**Cause:** Planner or plan-verifier didn't catch the mismatch
**Fix:**
1. Check plans/{chapterId}.json — are the continuityStatus values correct?
2. Check if memory files exist and contain the expected information
3. If memory files are missing → memory-keeper didn't run for the prior chapter
4. If memory files exist but plan-verifier missed them → check plan-verifier's continuity annotation instructions

### Slop-gate fails after max iterations

**Symptom:** Manifest contains `"slopGateExhausted"` field for a chapter. The pipeline continued with best-effort prose.
**Cause:** The slop-gate found violations that the slophunter's revision mode couldn't fix within the max iteration limit. The orchestrator promoted the latest revision and continued rather than halting.
**Post-run action:**
1. Read the last `slop-gate-notes-r{N}.json` to see what the gate still flagged
2. Read the corresponding `v2.md` (promoted from the last revision) to see the current state
3. Either: manually fix the remaining patterns in the final chapter output
4. Or: increase `agents.slopGate.maxIterations` in config.json for future runs

### Slop-gate crash during revision loop

**Symptom:** Pipeline restarts and re-enters the revision loop from the wrong point.
**Cause:** Crash during the slop-gate revision loop. The manifest's `slopGateLoop` object tracks loop state for recovery.
**Fix:**
1. Check `manifest.json` for the `slopGateLoop` object — it shows the current `iteration` and `phase`
2. The orchestrator should auto-recover from the correct phase. If it doesn't, manually set the phase and iteration.
3. If recovery is stuck, delete the `slopGateLoop` object from manifest and set `currentAgent` to "slophunter" to restart from the slophunter dispatch.

### Slop-gate revision file promotion

When the gate passes after a revision, the orchestrator promotes exactly two files to canonical paths:
- `v2-r{N}.md` → `v2.md` (so downstream agents always read `v2.md`)
- `slophunter-revision-r{N}-notes.json` → `slophunter-notes.json`

The versioned files (`v2-r*.md`, `slophunter-revision-r*-notes.json`, `slop-gate-notes-r*.json`) are NOT deleted — they remain as audit history. Only `slop-gate-notes.json` (or the latest `slop-gate-notes-r{N}.json`) reflects the final passing audit.

### Grounder failure / degradation

**Symptom:** Grounder status shows `"failed"`. Pipeline continues normally.
**Cause:** Grounder could not complete (missing memory files, grounding framework error, etc.).
**What happens:** The orchestrator copies `v2.md → v2g.md` and proceeds to the expander. Downstream agents read `v2g.md` (which is identical to `v2.md` in this case). No chapter blocking occurs.
**Post-run action:**
1. Check `agents/grounder/status.json` for the error message
2. Fix the underlying issue (missing materials, config error, etc.)
3. To re-run with grounding: delete `v2g.md`, `grounder-notes.json`, and downstream files, reset status files, restart

### Grounder producing excessive wordcount growth

**Symptom:** `v2g.md` is significantly larger than `v2.md` (>80% growth).
**Cause:** The grounder may have added lore dumps or narrator exposition instead of weaving detail into existing flow. Expected growth is 40-70%.
**Action:** Check `grounder-notes.json` for the per-scene enrichment log. If growth comes from lore-dump paragraphs rather than woven specificity, the style-editor and final-slophunter will trim excess downstream.

## Diagnostic Commands

```bash
# Check all agent statuses
for f in .afternoon/agents/*/status.json; do echo "=== $f ==="; cat "$f" 2>/dev/null || echo "(missing)"; echo; done

# Check manifest state
cat .afternoon/manifest.json 2>/dev/null || echo "No manifest (fresh start)"

# Check what outlines exist
ls -la .afternoon/outlines/

# Check what chapters have been started
ls -la .afternoon/chapters/*/

# Check memory files
ls -la .afternoon/plans/memory/*/

# Check plan files
ls -la .afternoon/plans/*.json

# Word counts of draft versions
wc -w .afternoon/chapters/*/v*.md 2>/dev/null

# Check start script logs
ls -lt logs/afternoon/ | head -5
```

## Resetting the Pipeline

### Fresh start (keep outlines, discard everything else):
```bash
rm -rf .afternoon/manifest.json .afternoon/agents/ .afternoon/chapters/ .afternoon/plans/*.json .afternoon/plans/memory/
mkdir -p .afternoon/agents/{planner,plan-verifier,writer,slophunter,slop-gate,grounder,expander,style-editor,style-auditor,final-slophunter,memory-keeper}
```

### Re-run a single chapter:
1. Delete that chapter's artifacts: `rm -rf .afternoon/chapters/{chapterId}/ .afternoon/plans/{chapterId}.json .afternoon/plans/{chapterId}-initial.json`
2. Delete all agent status files: `rm .afternoon/agents/*/status.json`
3. Update manifest: set `currentChapter` to the target, `currentAgent` to "planner"
4. Restart the pipeline

### Re-run from a specific agent:
1. Delete that agent's status.json and all downstream agent status files
2. Delete downstream output files (e.g., if re-running from slophunter, delete v2.md, v3.md, v4.md, style-notes.json, expander-notes.json)
3. Update manifest: set `currentAgent` to the target agent
4. Restart the pipeline
