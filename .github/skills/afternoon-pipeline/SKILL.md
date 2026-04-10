---
name: afternoon-pipeline
description: "Domain knowledge for the afternoon fiction-writing pipeline — a 12-agent sequential system that transforms beat plans into polished prose. Use this skill whenever editing afternoon agent files, modifying pipeline behavior, adding new agents, changing config.json, troubleshooting pipeline runs, understanding how the memory/continuity system works, or asking any question about how the afternoon agents interact. Also triggers on: 'afternoon pipeline', 'afternoon agents', 'edit the writer agent', 'add an agent to afternoon', 'fix the pipeline', 'config.json fields', 'continuityStatus', 'requiredMemory', 'memory-keeper passes', 'why did the pipeline fail', 'crash recovery', 'how does the orchestrator work', 'status.json', 'manifest.json', or any request involving the .afternoon/ directory or .github/agents/afternoon-*.agent.md files."
---

# Afternoon Pipeline

The afternoon pipeline is a 12-agent sequential system that transforms user-authored beat plans into polished fiction. This skill gives you the domain knowledge to work on any part of it.

## Pipeline at a Glance

```
style-extractor (user-invocable, run once per story) → style-guide.json
outline-builder (interactive, user-facing) → outlines/{chapterId}.md

Orchestrator (pure router) — per chapter, sequentially:
    1. Planner         → validates beats, enriches with research → plans/{chapterId}-initial.json
    2. Plan-Verifier   → continuity annotation, structural evaluation → plans/{chapterId}.json (final)
    3. Writer           → prose from plan, anti-slop primed → chapters/{chapterId}/v1.md
    4. Slophunter       → 11 targeted AI-pattern hunts → chapters/{chapterId}/v2.md
    5. [Slop-Gate A/B ↔ Slophunter revision loop] → adversarial audit, revision if either pass fails
    6. [Grounder]       → map-driven grounding → chapters/{chapterId}/v2g.md + grounding-map.json
    7. [Grounding-Gate ↔ Grounder revision loop] → adversarial grounding audit, revision if fail
    8. [Expander]       → intimate/emotional scene expansion → chapters/{chapterId}/v3.md
    9. Style-Editor     → 7 quality checks, voice polish → chapters/{chapterId}/v4.md
   10. [Style-Auditor]  → adversarial style-guide enforcement → chapters/{chapterId}/v4b.md
   11. Final-Slophunter → polish-mode slophunter → chapters/{chapterId}/v5.md
   12. Memory-Keeper    → 5-pass continuity catalog → plans/memory/{category}/{entity}.json + .md
   Assembly: cp v5.md → final.md
```

## Reference Files

Read the reference file for your current task. Each contains the full domain knowledge you need.

| Task | Reference file | When to read |
|------|---------------|-------------|
| Understand the architecture | `references/architecture.md` | First time working on the pipeline, or need a refresher on how agents connect |
| Edit or understand a specific agent | `references/agents.md` | Modifying agent behavior, adding checks, changing what an agent reads/writes |
| Work with config.json | `references/config.md` | Adding config fields, understanding what fields mean, changing project settings |
| Understand the memory/continuity system | `references/memory-system.md` | Working with continuityStatus, memoryRef, requiredMemory, or the memory-keeper |
| Add a new agent to the pipeline | `references/adding-agents.md` | Creating a new agent and integrating it into the dispatch chain |
| Troubleshoot a pipeline failure | `references/troubleshooting.md` | Pipeline crashed, agent failed, status.json issues, crash recovery |
| Run the pipeline | `references/running.md` | Starting the pipeline, monitoring progress, understanding completion |

## How to Use

1. Identify which task you're doing from the table above.
2. Read that reference file.
3. If your task spans multiple areas (e.g., "add a new agent that reads memory files"), read both relevant reference files.
4. When editing agent files, always verify cross-agent consistency afterward — changes to one agent's output format affect all downstream agents that read it.
