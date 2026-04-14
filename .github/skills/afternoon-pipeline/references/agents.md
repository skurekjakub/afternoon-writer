# Agent Overview

All agent prompts live in `.github/agents/afternoon-{name}.agent.md`.

Shared rules:

- Every agent writes `.afternoon/agents/{name}/status.json`.
- The orchestrator routes by `status.json`, not by checking whether output files exist.
- Core prose chain: `v0.md -> v0c.md -> v1.md -> v2.md -> v2g.md -> v3.md -> v5.md -> final.md`.
- `slop-gate` and `grounding-gate` audit only. They never edit prose directly.
- `expander` stays on disk but is not part of the live pipeline.

## Main Pipeline Agents

| Agent | File | Main I/O | Job |
|---|---|---|---|
| Orchestrator | `.github/agents/afternoon-orchestrator.agent.md` | `config + manifest + status -> manifest + final.md` | Pure router. Never reads prose. |
| Planner | `.github/agents/afternoon-planner.agent.md` | `outline -> plans/{chapterId}-initial.json` | Turns outline prose into structured beats and research. |
| Plan-Verifier | `.github/agents/afternoon-plan-verifier.agent.md` | `initial plan + memory -> plans/{chapterId}.json` | Owns structure, continuity annotation, and chapter transitions. |
| Writer-Coordinator | `.github/agents/afternoon-writer-coordinator.agent.md` | `plan -> scene plans + final writer status` | Splits scenes, dispatches writer, runs craft and continuity loops. |
| Writer | `.github/agents/afternoon-writer.agent.md` | `scene plan -> v0.md` | Writes scene prose from the verified plan. |
| Craft-Auditor | `.github/agents/afternoon-craft-auditor.agent.md` | `v1.md + plan -> craft-audit-findings.json` | Judges craft quality only. |
| Craft-Reviser | `.github/agents/afternoon-craft-reviser.agent.md` | `craft findings + v1.md -> v1.md` | Applies targeted craft fixes in place. |
| Continuity-Gate | `.github/agents/afternoon-continuity-gate.agent.md` | `plan + memory + prior canon + target prose -> continuity-findings.json` | Fails prose that breaks knowledge, beat order, cast logic, or canon. |
| Continuity-Writer | `.github/agents/afternoon-continuity-writer.agent.md` | `continuity findings + v1.md -> v1-crN.md` | Applies only continuity fixes. |
| Slophunter | `.github/agents/afternoon-slophunter.agent.md` | `v1.md -> v2.md`, `v3.md -> v5.md`, `v2/v2-r -> v2-rN.md` | Removes AI prose patterns, including revision mode from gate feedback. |
| Slop-Gate | `.github/agents/afternoon-slop-gate.agent.md` | `v2/v2-r -> slop-gate notes` | Two-pass adversarial slop audit with suggested fixes. |
| Grounder | `.github/agents/afternoon-grounder.agent.md` | `v2.md -> v2g.md` | Adds world-specific grounding and keeps a grounding map. |
| Grounding-Gate | `.github/agents/afternoon-grounding-gate.agent.md` | `v2g/v2g-r -> grounding-gate notes` | Audits grounding, tail strength, and source fidelity. |
| Memory-Keeper | `.github/agents/afternoon-memory-keeper.agent.md` | `plan + v5.md -> plans/memory/*` | Updates canon memory after each chapter. |

## User-Invocable / Special Agents

| Agent | File | Main I/O | Job |
|---|---|---|---|
| Outline-Builder | `.github/agents/afternoon-outline-builder.agent.md` | `inputs -> outlines/{chapterId}.md` | Interactive outline creation. |
| Style-Extractor | `.github/agents/afternoon-style-extractor.agent.md` | `prose samples -> .afternoon/style-guide.json` | Builds the style guide once per story or when samples change. |
| Expander | `.github/agents/afternoon-expander.agent.md` | not dispatched | Retained on disk only; current pipeline copies `v2g.md -> v3.md` instead. |

## Ownership Notes

- `planner` must preserve one-to-one outline-beat-to-plan-beat mapping; never merge beats.
- `plan-verifier` owns structure and continuity annotation. Must not merge outline beats.
- `writer` writes prose; `writer-coordinator` manages loops.
- `slophunter` edits style, not substance.
- `memory-keeper` is the canonical writer for `plans/memory/`.

If you change an agent's inputs, outputs, or status format, check every downstream consumer before you stop.