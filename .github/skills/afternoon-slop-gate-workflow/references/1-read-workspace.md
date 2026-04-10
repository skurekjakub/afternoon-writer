# Phase 1: Read Workspace

Resolve the dispatch before you make any guide judgments. This phase sets the audit boundaries, the file targets, and the output paths.

1. Read `.afternoon/config.json`.
2. Parse the dispatch prompt parameters:
   - `chapterId` (required)
   - `pass` (required) - must be `a` or `b`
   - `iteration` (optional, default `0`)
   - `targetFile` (optional, default `v2.md`)
3. If `pass` is missing or not `a` / `b`, write `.afternoon/agents/slop-gate/status.json` with:
   - `"status": "failed"`
   - `"verdict": null`
   - `"artifacts": []`
   - a summary explaining the dispatch error
   Then stop.
4. Lock the current guide pack:
   - Pass `a` audits `negation-addiction-hunting-guide.md`, `intent-smear-agency-laundering-guide.md`, and `recurring-prose-tics.md`
   - Pass `b` audits `gpt-5-prose-issues.md`, `narrator-seep-guide.md`, `phantom-concreteness-guide.md`, and `fake-simplification-guide.md`
   Audit only the selected guide pack in this run.
5. Fresh-sweep prohibition: do not read prior gate artifacts or revision artifacts. On iteration 1+, do not open:
   - `slop-gate-notes-*.json`
   - `slop-gate-notes-r*?.json`
   - `slop-gate-scratchpad-*.md`
   - `slop-gate-scratchpad-r*?.md`
   - `slophunter-revision-r*-notes.json`
6. Determine output paths:
   - Notes JSON:
     - iteration `0`, pass `a`: `.afternoon/chapters/{chapterId}/slop-gate-notes-a.json`
     - iteration `0`, pass `b`: `.afternoon/chapters/{chapterId}/slop-gate-notes-b.json`
     - iteration `N>0`, pass `a`: `.afternoon/chapters/{chapterId}/slop-gate-notes-r{N}a.json`
     - iteration `N>0`, pass `b`: `.afternoon/chapters/{chapterId}/slop-gate-notes-r{N}b.json`
   - same for scratchpad naming
7. Read `.afternoon/chapters/{chapterId}/{targetFile}` into context. This is the only prose input for the run.
8. Track the work as ordered phases with dependencies:
   - read workspace
   - build false-positive filter
   - audit each guide in the assigned pass
   - suggest and decide
   - write artifacts

## Before moving to Phase 2

You should have:
- `chapterId`, `pass`, `iteration`, and `targetFile` resolved
- the current pass locked
- output paths resolved
- the target prose loaded
- the fresh-sweep prohibition fixed in mind
