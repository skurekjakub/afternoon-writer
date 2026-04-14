# Architecture

## Flow

The pipeline runs chapters in order. Chapter `N+1` does not start until chapter `N` reaches memory-keeper.

```text
planner -> plan-verifier -> writer-coordinator
writer-coordinator -> writer per scene -> craft-auditor/craft-reviser loop -> continuity-gate/continuity-writer loop -> v1.md
v1.md -> slophunter -> slop-gate loop -> grounder -> grounding-gate loop -> cp v2g.md v3.md -> final-slophunter -> memory-keeper -> cp v5.md final.md
```

Separate user tools:

- `outline-builder` creates `outlines/{chapterId}.md`
- `style-extractor` creates `.afternoon/style-guide.json`

Removed from the live chain:

- `expander`
- `style-editor`
- `style-auditor`
- post-texture slop-gate

## Draft Stages

| File | Owner | Meaning |
|---|---|---|
| `v0.md` | writer | raw scene draft |
| `v0c.md` | craft loop | craft-clean draft |
| `v1.md` | continuity loop | coordinator final draft |
| `v2.md` | slophunter | slop-reduced draft |
| `v2g.md` | grounder | grounded draft, or copy of `v2.md` |
| `v3.md` | orchestrator | copy of `v2g.md` |
| `v5.md` | final-slophunter | final polish |
| `final.md` | orchestrator | copy of `v5.md` |

Revision files stay versioned (`v2-rN.md`, `v2g-rN.md`) until promoted back to the canonical path.

## Main Folders

- `.afternoon/config.json`: project settings
- `.afternoon/overview.md`: story overview
- `.afternoon/manifest.json`: run state and recovery
- `.afternoon/outlines/`: outline inputs
- `.afternoon/plans/`: verified plans plus memory
- `.afternoon/chapters/{chapterId}/`: prose drafts, notes, gate artifacts
- `.afternoon/agents/{agent}/status.json`: completion signals

## Router Rules

- Dispatches are synchronous.
- Skip logic and recovery depend on `status.json` only.
- Slop-gate and grounding-gate loop until pass or iteration limit.
- Grounder failure degrades gracefully: `cp v2.md v2g.md`, skip grounding-gate, continue.
- Final assembly is `cp v5.md final.md`.

## Recovery

`manifest.json` holds `currentChapter`, `currentAgent`, and loop state such as `slopGateLoop` or `groundingGateLoop`.

- If an agent already wrote `status: completed` for the active chapter, the orchestrator advances.
- If not, it re-dispatches from that point.
- Never infer state from prose files alone.