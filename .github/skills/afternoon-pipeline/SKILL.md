---
name: afternoon-pipeline
description: "Domain knowledge for the afternoon fiction-writing pipeline. Use this skill when editing afternoon agents, orchestrator flow, config.json, memory/continuity behavior, crash recovery, or any file under .afternoon/ or .github/agents/afternoon-*.agent.md."
---

# Afternoon Pipeline

Use this skill for pipeline work: agent prompts, orchestrator routing, config, memory flow, or recovery behavior.

## Quick Flow

```text
style-extractor -> style-guide.json
outline-builder -> outlines/{chapterId}.md

planner -> plan-verifier -> writer-coordinator
writer-coordinator -> writer per scene -> craft loop -> continuity loop -> v1.md
v1.md -> slophunter -> slop-gate loop -> grounder -> grounding-gate loop -> cp v2g.md v3.md -> final-slophunter -> memory-keeper -> cp v5.md final.md
```

## Read The Right File

| Task | File |
|---|---|
| Overall flow | `references/architecture.md` |
| Agent I/O and ownership | `references/agents.md` |
| Config fields | `references/config.md` |
| Memory and continuity | `references/memory-system.md` |
| Adding an agent | `references/adding-agents.md` |
| Running the pipeline | `references/running.md` |
| Debugging a run | `references/troubleshooting.md` |

## Rules That Matter

- The orchestrator is prose-blind. It reads `config.json`, `manifest.json`, and agent `status.json` files only.
- Routing and crash recovery use `status.json`, not output-file existence.
- Canonical draft chain: `v0.md -> v0c.md -> v1.md -> v2.md -> v2g.md -> v3.md -> v5.md -> final.md`.
- Slop-gate and grounding-gate audit failures are not operational failures; they return completed status with a fail verdict and trigger revision loops.
- The grounder can be disabled or can degrade to `cp v2.md v2g.md` without blocking the chapter.
- If you change what an agent reads or writes, update every downstream reader in the same session.