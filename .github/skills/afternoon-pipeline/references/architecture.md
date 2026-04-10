# Architecture

## Agent Flow

The pipeline processes chapters sequentially — chapter 2 cannot start until chapter 1 is fully complete (including memory-keeper update). Within each chapter, up to 12 agents run in strict order:

```
Planner → Plan-Verifier → Writer → Slophunter → [Slop-Gate A/B ↔ Slophunter revision] → [Grounder] → [Grounding-Gate ↔ Grounder revision] → [Expander] → Style-Editor → [Style-Auditor] → Final-Slophunter → Memory-Keeper
```

The outline-builder and style-extractor are separate — they're user-invocable, not dispatched by the orchestrator. The outline-builder produces the input beat plans. The style-extractor produces `.afternoon/style-guide.json` (run once per story).

The grounder can be disabled per-story via `config.agents.grounder.enabled: false` — the orchestrator does `cp v2.md v2g.md`, skips the grounder, and skips the grounding-gate. The grounder also degrades gracefully on failure — the orchestrator copies `v2.md` to `v2g.md`, skips the grounding-gate, and proceeds without blocking.

The grounding-gate is optional and currently defaults off via `config.agents.groundingGate.enabled: false`. When enabled, it audits `v2g.md` after grounding and before expansion. On audit failure, the orchestrator enters a best-effort loop: grounder revision → grounding-gate re-audit, up to `agents.groundingGate.maxIterations` (default `3`). If the gate still fails after max iterations, the orchestrator promotes the latest grounded revision and continues anyway.

The expander can be disabled per-story via `config.agents.expander.enabled: false` — the orchestrator does `cp v2g.md v3.md` and skips the expander dispatch. Style-editor always reads v3.md regardless.

The style-auditor requires `.afternoon/style-guide.json`. If the file doesn't exist, the style-auditor reports failed status and the orchestrator skips it — the final slophunter reads v4.md instead of v4b.md.

## Artifact Versioning

Each chapter produces seven primary draft versions, plus optional revision and audit artifacts:

| Version | Agent | Description |
|---------|-------|-------------|
| `v1.md` | Writer | Raw first draft from beat plan |
| `v2.md` | Slophunter | AI patterns eliminated (20% wordcount reduction) |
| `v2g.md` | Grounder | World-specificity grounding (or `cp` of v2 if disabled/degraded) |
| `v3.md` | Expander | Intimate/emotional scenes expanded (or `cp` of v2g if disabled) |
| `v4.md` | Style-Editor | Voice/continuity polished |
| `v4b.md` | Style-Auditor | Style-guide enforcement pass (absent if style-guide.json missing) |
| `v5.md` | Final-Slophunter | Register and slop polish pass (20% wordcount reduction) |
| `final.md` | Orchestrator | Copy of v5.md (assembly step, via `cp`) |

The grounding-gate does not introduce a new canonical prose stage. It audits `v2g.md` and, if needed, forces numbered grounded revisions (`v2g-rN.md`) until one is promoted back to canonical `v2g.md`.

## Directory Layout

```
.afternoon/
├── config.json                              # Project settings (user-authored)
├── style-guide.json                         # Style specification (style-extractor output, optional)
├── overview.md                              # Story overview — arc, themes, destination (user-authored, mandatory)
├── manifest.json                            # Orchestrator state + crash recovery
├── outlines/
│   ├── chapter-1.md                         # User-authored beat plans (input)
│   └── chapter-2.md
├── plans/
│   ├── series-meta.md                    # Cross-invocation planning notes (planner + verifier append per chapter)
│   ├── chapter-1-initial.json                # Planner output (preserved for comparison)
│   ├── chapter-1.json                       # Verified plan (plan-verifier output — downstream agents read this)
│   └── memory/
│       ├── characters/                        # Per-entity files + _index.json
│       │   ├── _index.json
│       │   ├── sylvanas-windrunner.json + .md
│       │   └── jaina-proudmoore.json + .md
│       ├── locations/
│       │   ├── _index.json
│       │   └── millhaven.json + .md
│       ├── relationships/
│       │   ├── _index.json
│       │   └── jaina--sylvanas.json + .md
│       ├── threads/
│       │   ├── _index.json
│       │   └── plague-samples-border.json + .md
│       └── world/
│           ├── _index.json
│           ├── geography.json + .md
│           └── timeline.json + .md
├── chapters/{chapterId}/
│   ├── v1.md                                # Writer output
│   ├── v2.md                                # Slophunter output
│   ├── v2g.md                               # Grounder output (or cp of v2 if disabled/degraded)
│   ├── v2g-r*.md                            # Grounder revision drafts during grounding-gate loop
│   ├── grounding-map.json                   # Grounder execution scaffold
│   ├── grounding-map-r*.json                # Revision grounding maps
│   ├── v3.md                                # Expander output (or cp of v2g if disabled)
│   ├── v4.md                                # Style-editor output
│   ├── v4b.md                               # Style-auditor output (absent if style-guide.json missing)
│   ├── v5.md                                # Final-slophunter output
│   ├── slophunter-notes.json                # Change log
│   ├── slop-gate-notes-a.json               # Pass A KILL findings + suggestedFix (absent if gate disabled)
│   ├── slop-gate-notes-b.json               # Pass B KILL findings + suggestedFix (absent if gate disabled)
│   ├── slop-gate-notes-r*?.json             # Re-audit KILL findings per iteration/pass (e.g. r1a, r1b)
│   ├── slop-gate-scratchpad-a.md            # Pass A KEEP decisions with reasoning (absent if gate disabled)
│   ├── slop-gate-scratchpad-b.md            # Pass B KEEP decisions with reasoning (absent if gate disabled)
│   ├── slop-gate-scratchpad-r*?.md          # Re-audit KEEPs per iteration/pass (e.g. r1a, r1b)
│   ├── v2-r*.md                             # Slophunter revision drafts (absent if gate passes first time)
│   ├── slophunter-revision-r*-notes.json    # Revision change logs (absent if gate passes first time)
│   ├── grounding-gate-notes.json            # Grounding gate KILL findings + suggested fixes (absent if gate disabled/skipped)
│   ├── grounding-gate-notes-r*.json         # Grounding gate re-audit findings per iteration
│   ├── grounding-gate-scratchpad.md         # Grounding gate KEEP decisions (human-audit artifact)
│   ├── grounding-gate-scratchpad-r*.md      # Grounding gate re-audit KEEP decisions
│   ├── expander-notes.json                  # Change log (absent if expander disabled)
│   ├── grounder-notes.json                  # Change log (absent if grounder disabled/degraded)
│   ├── grounder-revision-r*-notes.json      # Revision change logs during grounding-gate loop
│   ├── style-notes.json                     # Change log
│   ├── style-auditor-notes.json             # Change log (absent if style-guide.json missing)
│   ├── final-slophunter-notes.json          # Change log
│   └── final.md                             # Assembled (cp of v5.md)
└── agents/{agent-name}/
    └── status.json                          # Per-agent completion status
```

## Data Flow Between Agents

### What flows forward (each agent's output feeds the next):

```
overview.md ──→ (read by Planner, Plan-Verifier, Outline-Builder, Writer, Slophunter, Style-Editor)
                 (provides story arc context — where this chapter fits in the whole)

outlines/{chapterId}.md ──→ Planner ──→ plans/{chapterId}-initial.json ──→ Plan-Verifier
                                                                              │
plans/{chapterId}.json ←──────────────────────────────────────────────────────┘
         │
         ├──→ Writer ──→ v1.md ──→ Slophunter ──→ v2.md ──→ [Slop-Gate A/B ↔ revision loop] ──→ Grounder ──→ [Grounding-Gate ↔ revision loop] ──→ v2g.md ──→ Expander ──→ v3.md
         │                                                                                                                            │
         └──→ (requiredMemory field tells Writer + Style-Editor which memory files to read)                 │
                                                                                                              │
          Style-Editor ──→ v4.md ──→ [Style-Auditor] ──→ v4b.md ──→ Final-Slophunter ──→ v5.md ──→ final.md
                                                                                                        │
         Memory-Keeper ───────────────────────────────────────────────────────────────────────────┘
              │
              └──→ plans/memory/{category}/{entity}.json + .md (available to Planner + Plan-Verifier on NEXT chapter)
```

### What flows backward (memory system):

The memory-keeper writes after each chapter. Both planners maintain `plans/series-meta.md` — a cross-invocation notebook with running chapter summaries, active threads, chapter-end stance/residue notes, and warnings for the next chapter. On the NEXT chapter:
- The **planner** reads `series-meta.md` to understand where the series stands without re-reading all prior outlines and plans
- The **plan-verifier** reads `series-meta.md` plus ALL memory files to annotate continuityStatus, verify beat-level `transitionIntent`, write chapterBridges, and run anti-reintroduction checks
- The **writer** and **style-editor** read ONLY the memory entries referenced in the plan's `requiredMemory` field — targeted reads, not bulk loads

## Orchestrator Isolation

The orchestrator is a pure router. It reads exactly three things:
1. `config.json` (once, at startup — including `storyOverview` path for bootstrap validation)
2. `manifest.json` (its own state)
3. `agents/{name}/status.json` (completion signals)

**Bootstrap gate:** At startup, the orchestrator validates that `config.storyOverview` exists as a field AND that the referenced file exists on disk. If either check fails → FATAL error, pipeline exits with completion marker. The orchestrator reads the path but NEVER reads the file's content (it's prose-blind).

Between dispatches, the orchestrator does nothing — no polling, no monitoring, no `read_agent`, no `sleep`, no `bash` (except `mkdir -p` and `cp`).

## Dispatch and Retry

For each agent dispatch:
1. Read agent's `status.json` — if already `"completed"` for this chapterId, skip
2. Dispatch agent with `prompt: "chapterId: {chapterId}"`
3. Wait for completion (synchronous, no polling)
4. Read agent's `status.json`
5. If `"completed"` → proceed to next agent
6. If `"failed"` → retry once with same prompt
7. If second failure → mark chapter "blocked", move to next chapter

Important exceptions:
- Slop-gate and grounding-gate audit failures are not operational failures. They return `status: "completed"` with `verdict: "fail"` and enter their respective revision loops.
- Grounder second failure degrades gracefully (`cp v2.md → v2g.md`) and skips the grounding-gate instead of blocking.
- Style-auditor `status: "failed"` with missing style guide is treated as a skip, not a block.

## Crash Recovery

If `manifest.json` exists with `"status": "in-progress"`:
1. Read `currentChapter` and `currentAgent` from manifest
2. Check for active slop-gate loop: if `slopGateLoop` exists in manifest, resume from the loop phase (awaiting-revision, awaiting-reaudit-a, awaiting-reaudit-b, or awaiting-promote)
3. Check for active grounding-gate loop: if `groundingGateLoop` exists in manifest, resume from the loop phase (awaiting-revision, awaiting-reaudit, or awaiting-promote)
4. Standard recovery: Read that agent's `status.json`:
    - Shows `"completed"` for this chapterId → manifest wasn't updated → update it, proceed to next agent
    - Missing or shows different chapterId → re-dispatch the current agent
5. Continue from that point forward

Signal source is ALWAYS `status.json` — never check output file existence.
