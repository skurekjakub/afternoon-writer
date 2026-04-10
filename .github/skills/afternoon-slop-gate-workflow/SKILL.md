---
name: afternoon-slop-gate-workflow
description: "Sequential workflow for the afternoon-slop-gate agent. Covers: read workspace and dispatch state -> build the false-positive filter -> audit the assigned pass -> cross-check fixes and decide verdict -> write notes, scratchpad, and status. Read this skill at the start of every invocation and follow phases in order."
---

# Afternoon Slop Gate Workflow

This skill routes you through the slop-gate audit phase by phase. Read the reference file for your current phase only.

| Phase | Reference file | Summary |
|---|---|---|
| 1. Read Workspace | `references/1-read-workspace.md` | Parse the dispatch, choose the pass, resolve the target prose and output paths |
| 2. Build False-Positive Filter | `references/2-build-false-positive-filter.md` | Prime POV, subject-matter, dialogue, and intent defenses from the chapter plan |
| 3. Audit Assigned Pass | `references/3-audit-assigned-pass.md` | Run the guide loop for the current pass, then load the matching pass route |
| 4. Suggest and Decide | `references/4-suggest-and-decide.md` | Cross-check fixes against the current pass guide pack and compute the pass verdict |
| 5. Write Artifacts | `references/5-write-artifacts.md` | Write the notes JSON, scratchpad markdown, and status.json |

## How to use

1. Start at Phase 1.
2. Complete Phase 2 after Phase 1.
3. In Phase 3, read only the pass route that matches `pass`:
   - `references/3a-pass-a-guides.md`
   - `references/3b-pass-b-guides.md`
4. Then continue to Phases 4 and 5 in order.
