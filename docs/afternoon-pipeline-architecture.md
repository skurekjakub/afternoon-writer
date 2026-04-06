# Afternoon Fiction Pipeline — Architecture

An autonomous multi-agent pipeline that transforms beat-plan outlines into polished prose chapters. Up to twelve specialized agents run sequentially, each reading the previous agent's output and producing input for the next. A pure-router orchestrator coordinates dispatch without ever reading prose content.

**Updated:** 2025-07-14

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [Agent Flow](#agent-flow)
3. [Agent Roles](#agent-roles)
4. [Artifact Versioning](#artifact-versioning)
5. [Directory Layout](#directory-layout)
6. [Data Flow](#data-flow)
7. [Orchestrator Design](#orchestrator-design)
8. [Memory System](#memory-system)
9. [Design Decisions](#design-decisions)

---

## Pipeline Overview

The afternoon pipeline converts user-authored beat outlines into finished fiction chapters. It operates on a simple principle: separate concerns completely. No single agent handles more than one job. The writer writes. The slophunter hunts slop. The style-editor polishes voice. Each agent is an expert at exactly one thing.

The pipeline processes chapters sequentially — chapter 2 cannot start until chapter 1 is fully complete, including the memory-keeper's continuity update. This guarantees that every chapter has access to the full continuity state from all prior chapters.

All agents run on `gpt-5.4`. All prose uses Limited Third Absolute POV. All characters are women or futas (she/her pronouns exclusively).

## Agent Flow

```
User authors:
  .afternoon/overview.md (story arc — mandatory)
  .afternoon/outlines/chapter-N.md (beat plans)
  .afternoon/config.json (project settings)

Pipeline execution (per chapter):

  Planner ─────────→ Plan-Verifier ─────────→ Writer
  (validate beats,    (continuity annotation,   (raw first draft
   web-research        transition bridges,        from verified plan)
   enrichment)         pacing authority)
                                                    │
                                                    ▼
  Style-Editor ←── Expander ←── Grounder ←── Slop-Gate ←── Slophunter ←── v1.md
  (voice polish,    (scene          (world-specificity  (adversarial    (AI pattern
   continuity,       expansion,      grounding,          slop audit,     elimination,
   7 checks)         if enabled)     if enabled)         revision loop)  11 targeted hunts)
       │
       ▼
  Style-Auditor ──→ Final-Slophunter ──→ Memory-Keeper
  (style-guide       (polish-mode          (catalogues what happened,
   enforcement,       slop elimination,     updates per-entity ledgers
   if guide exists)   register pass)        for future chapters)
```

The **Outline-Builder** and **Style-Extractor** sit outside this flow — they're user-invocable, not orchestrator-dispatched. The outline-builder helps the user create beat plans and now writes the normalized structured chapter beatplan schema used for planner-facing refinement work. The style-extractor analyzes prose samples and produces `style-guide.json`.

## Agent Roles

### Orchestrator
**Pure router.** Reads config, manifest, and status files. Never reads prose, plans, or memory. Validates the story overview exists at bootstrap. Dispatches agents one at a time, handles retry (one retry per failure, then marks chapter "blocked"), manages crash recovery via manifest state.

### Planner (Hermione)
**Structure validator and researcher.** Reads the user's normalized outline scaffold, the series meta (cross-invocation planning notes), validates chapter scaffold + beat structure (arc position, cast/handoff rules, scene/sequel typing, value shifts, scene outcomes, beat-level transition intent), and enriches beats with web-researched details — character facts, location geography, cultural customs. Does NOT handle continuity or chapter bridges. Outputs `{chapterId}-initial.json`. After writing, appends structural notes to `series-meta.md`.

### Plan-Verifier (Scheherazade)
**Continuity annotator and craft auditor.** Reads the planner's output, the original outline scaffold, the series meta, plus ALL memory files. Annotates every entity reference with `continuityStatus` (new/callback/evolution), audits `arcPosition` against the beats, verifies beat-level `transitionIntent`, writes `chapterBridge`, and has chapter-level modification authority for pacing and structure. Verifier notes are continuity-only — no prose directives. Outputs the final `{chapterId}.json` that all downstream agents read. After writing, appends continuity/craft notes to `series-meta.md`.

### Writer
**Prose writer.** Reads the verified plan, story overview, priming files (anti-slop + craft), style target, and targeted memory. Writes beat-by-beat, using `continuityStatus` to control description density: "new" gets full sensory treatment, "callback" gets brief anchoring, "evolution" builds on established foundations. Self-audits against the slop hitlist before delivery. Outputs `v1.md`.

### Slophunter
**AI pattern eliminator.** Reads `v1.md` and executes 11 targeted hunts: wordcount reduction, hard caps on overused words, all hitlist items, telegram prose, opener tics, filter words, image repetition, which-meant syndrome, essay paragraphs, biography insertions, and temporal beat transitions. Surgical replacement — never adds content. Outputs `v2.md` plus notes JSON with before/after counts. Also runs in revision mode when the slop-gate fails — applies the gate's pre-validated suggested fixes (with latitude for voice/flow), then runs a rewrite self-audit on changed passages to catch violations introduced by the rewrites.

### Slop-Gate
**Adversarial slop auditor with fix suggestions.** Reads `v2.md` and audits it against every guide in `resources/*.md`. For each KILL finding, writes a concrete `suggestedFix` (replacement text), cross-checked against all audit guides (not just co-triggered ones) to prevent the replacement from violating other rules. Uses iteration-aware conservatism: later iterations prefer deletion and minimal substitution over creative rewrites. Emits pass or fail. On fail, the orchestrator re-dispatches the slophunter in revision mode — the slophunter applies the gate's pre-validated suggestions (with latitude for voice/flow adjustment) rather than improvising fixes. The gate then re-audits. This loop continues up to `maxIterations` (configurable, default 5). On pass, the clean v2.md proceeds to the grounder. Can be disabled per-story via config.

### Grounder
**World-specificity grounding by exemplar.** Reads `v2.md`, the plan, memory files, materials, and a before/after chapter pair that teaches the transformation. Enriches prose with named geography, titled institutions, material texture, world-register dialogue, physical rhythm beats, and POV-filtered technical vocabulary — learned from the exemplar, not from a category taxonomy. Sources all proper nouns from memory, materials, and plan — never invents. Self-audits against anti-slop hitlist after grounding. Wordcount target: 40-70% growth. Can be disabled per-story via config (`agents.grounder.enabled: false`). On failure, orchestrator copies v2.md to v2g.md and proceeds — does not block. Outputs `v2g.md`.

### Expander
**Scene expansion editor.** Reads `v2g.md` and the plan's `expansionLevel` per beat. Expands underwritten intimate and emotional scenes using a 6-question test. Three levels: high (moment-by-moment), medium (add reactions/detail), low (1-2 sensory anchors). Can be disabled per-story via config — orchestrator does `cp v2g.md v3.md` and skips dispatch. Outputs `v3.md`.

### Style-Editor
**Voice and continuity polish.** Reads `v3.md`, story overview, style target, style-guide.json (if available), voice sheets, prior chapter, memory files. Seven quality checks: voice consistency, Limited Third compliance, continuity/anti-reintroduction, sentence variety, beat transitions, slophunter leftovers, and dialogue register. Does not add content or cut beats — only polishes. Outputs `v4.md`.

### Style-Auditor
**Adversarial style-guide enforcement.** Reads `v4.md` against `.afternoon/style-guide.json` and verifies every specification field: sentence rhythm, vocabulary register, metaphor density, paragraph structure, dialogue ratio, per-POV voice fingerprints, and quality floor metrics. Produces `v4b.md`. Requires `style-guide.json` — skipped if absent (orchestrator proceeds to final slophunter with v4.md).

### Final-Slophunter
**Polish-mode slop elimination.** Runs the slophunter in polish mode on `v4b.md` (or `v4.md` if style-auditor was skipped). Register and document-voice pass. 20% wordcount reduction target. Outputs `v5.md`.

### Memory-Keeper
**Continuity librarian.** Reads `v5.md` and the verified plan. Updates per-entity JSON+MD files across five categories: characters, locations, relationships, threads, world. Handles merge logic for entities that appeared in prior chapters. Does NOT read the story overview — it catalogues what was written, not what was planned.

### Outline-Builder (user-invocable)
**Interactive planning assistant.** Not part of the automated pipeline. Reads anti-slop rules, craft references, story overview, materials, and existing memory. Enters an elicitation loop with the user (up to 5 rounds) to build a detailed beat plan with scene/sequel typing, value shifts, sensory anchors, and transition fields. Outputs to `.afternoon/outlines/`.

### Style-Extractor (user-invocable)
**Style-guide extraction.** Not part of the automated pipeline. Reads prose samples from `config.priming.proseSamples`, story overview, voice sheets, and character memory profiles. Extracts abstract patterns (sentence rhythm, vocabulary register, metaphor density, emotional expression, dialogue style, narrative distance, paragraph structure, descriptive approach) and produces `.afternoon/style-guide.json` — a structured specification that the style-auditor, style-editor, and slophunter enforce. Run once per story or when samples change.

## Artifact Versioning

Each chapter produces up to seven draft versions, each improving on the last:

| Version | Agent | What happens |
|---------|-------|-------------|
| `v1.md` | Writer | Raw first draft from the verified beat plan |
| `v2.md` | Slophunter | AI patterns eliminated, wordcount reduced (may include revision iterations via slop-gate) |
| `v2g.md` | Grounder | World-specificity grounding — named geography, factions, mechanics, materials, cultural voice (or copy of v2 if disabled/degraded) |
| `v3.md` | Expander | Intimate/emotional scenes expanded (or copy of v2g if expander disabled) |
| `v4.md` | Style-Editor | Voice/continuity polished |
| `v4b.md` | Style-Auditor | Style-guide enforcement (absent if style-guide.json missing) |
| `v5.md` | Final-Slophunter | Polish-mode slop elimination, register pass |
| `final.md` | Orchestrator | Copy of v5.md (assembly step via `cp`) |

Each editor also produces a notes JSON logging all changes with before/after counts, so you can trace what happened at each stage.

## Directory Layout

```
.afternoon/
├── config.json                    # Project settings (user-authored)
├── overview.md                    # Story overview — arc, themes, destination (mandatory)
├── manifest.json                  # Orchestrator state + crash recovery
│
├── outlines/                      # User-authored beat plans (input)
│   ├── chapter-1.md
│   └── chapter-2.md
│
├── plans/
│   ├── series-meta.md             # Cross-invocation planning notes (planner + verifier append per chapter)
│   ├── chapter-1-initial.json     # Planner output (preserved for comparison)
│   ├── chapter-1.json             # Verified plan (plan-verifier output — downstream reads this)
│   └── memory/                    # Per-entity continuity files
│       ├── characters/
│       │   ├── _index.json
│       │   └── {slug}.json + .md
│       ├── locations/
│       ├── relationships/
│       ├── threads/
│       └── world/
│
├── chapters/{chapterId}/
│   ├── v1.md                      # Writer output
│   ├── v2.md                      # Slophunter output (promoted from v2-rN.md if gate revision loop ran)
│   ├── v2-r*.md                   # Slophunter revision drafts (absent if gate passes first time)
│   ├── v2g.md                     # Grounder output (or cp of v2 if disabled/degraded)
│   ├── v3.md                      # Expander output (or cp of v2g)
│   ├── v4.md                      # Style-editor output
│   ├── v4b.md                     # Style-auditor output (absent if style-guide.json missing)
│   ├── v5.md                      # Final-slophunter output
│   ├── final.md                   # Assembled (cp of v5.md)
│   ├── slophunter-notes.json      # Change log
│   ├── slophunter-revision-r*-notes.json  # Revision change logs (absent if gate passes first time)
│   ├── slop-gate-notes.json       # KILL findings only (absent if gate disabled)
│   ├── slop-gate-notes-r*.json    # Re-audit KILL findings per iteration (absent if gate passes first time)
│   ├── slop-gate-scratchpad.md    # KEEP decisions for human audit (absent if gate disabled)
│   ├── slop-gate-scratchpad-r*.md # Re-audit KEEPs per iteration (absent if gate passes first time)
│   ├── expander-notes.json        # Change log (absent if expander disabled)
│   ├── grounder-notes.json        # Change log (absent if grounder disabled/degraded)
│   ├── style-notes.json           # Change log
│   ├── style-auditor-notes.json   # Change log (absent if style-guide.json missing)
│   └── final-slophunter-notes.json # Change log
│
└── agents/{agent-name}/
    └── status.json                # Per-agent completion status
```

## Data Flow

### Forward flow (each agent feeds the next)

The story overview feeds into all content-producing agents (planner, plan-verifier, writer, slophunter, style-editor) and the outline-builder. It provides story-arc context — where this chapter fits in the whole narrative.

```
overview.md ──→ (read by Planner, Plan-Verifier, Writer, Slophunter, Style-Editor, Outline-Builder)

outlines/{chapterId}.md ──→ Planner ──→ {chapterId}-initial.json ──→ Plan-Verifier
                                                                          │
{chapterId}.json ←───────────────────────────────────────────────────────┘
       │
       ├──→ Writer ──→ v1.md ──→ Slophunter ──→ v2.md ──→ [Slop-Gate ↔ revision loop] ──→ Grounder ──→ v2g.md ──→ Expander ──→ v3.md
       │                                                                                                  │
       └──→ (requiredMemory field tells Writer + Style-Editor which memory files to read)                 │
                                                                                                            │
       Style-Editor ──→ v4.md ──→ [Style-Auditor] ──→ v4b.md ──→ Final-Slophunter ──→ v5.md ──→ final.md ──→ Memory-Keeper
```

### Backward flow (memory system)

After each chapter, the memory-keeper writes per-entity files. Both planners maintain `series-meta.md` — a cross-invocation notebook with running chapter summaries, active threads, chapter-end stance / carry-forward residue notes, and warnings for the next chapter. On the NEXT chapter:
- The **planner** reads `series-meta.md` to understand where the series stands without re-reading all prior outlines and plans
- The **plan-verifier** reads `series-meta.md` plus ALL memory files to annotate continuity and write transition bridges
- The **writer** and **style-editor** read ONLY the entries referenced in `requiredMemory` — targeted reads, not bulk loads

## Orchestrator Design

### Isolation principle
The orchestrator is prose-blind. It reads exactly three things:
1. `config.json` (once, at startup — including `storyOverview` path for bootstrap validation)
2. `manifest.json` (its own state)
3. `agents/{name}/status.json` (completion signals)

It never reads plans, beats, prose, memory, or editor notes. It cannot evaluate content quality — it only knows success or failure.

### Bootstrap gate
At startup, the orchestrator validates that `config.storyOverview` exists as a field AND that the referenced file exists on disk. Missing or empty → FATAL error, pipeline exits with the completion marker so the start script doesn't retry infinitely.

### Dispatch protocol
For each agent dispatch:
1. Check agent's `status.json` — if `"completed"` for this chapterId, skip
2. Dispatch with `prompt: "chapterId: {chapterId}"`
3. Wait for completion (synchronous)
4. Read `status.json` — if completed, proceed; if failed, retry once
5. Second failure → mark chapter "blocked", move to next

### Crash recovery
If `manifest.json` exists with `"status": "in-progress"`:
1. Read `currentChapter` and `currentAgent`
2. Check for active slop-gate loop: if `slopGateLoop` exists in manifest, resume from the loop phase
3. Standard recovery: check that agent's `status.json`:
   - Shows completed for this chapter → manifest wasn't updated → fix manifest, advance
   - Missing or shows different chapter → re-dispatch the agent
4. Continue from that point

Signal source is always `status.json`, never output file existence.

## Memory System

Three-layer continuity architecture:

### Layer 1: Annotation at plan time
The plan-verifier reads all memory files and annotates every entity reference with:
- `continuityStatus`: "new" (first appearance), "callback" (seen before), "evolution" (changing)
- `memoryRef`: path to the entity's memory file
- `requiredMemory`: array of memory file paths the writer needs

### Layer 2: Targeted reads at write time
The writer reads only the memory files listed in `requiredMemory`. This prevents context bloat — a chapter mentioning two characters reads two character files, not the entire memory directory.

### Layer 3: Enforcement at edit time
The style-editor runs anti-reintroduction checks: names, descriptions, geography, timeline, established facts. Passages re-stating established information as fresh get flagged and fixed.

After the chapter is complete, the memory-keeper writes per-entity files, closing the loop for the next chapter.

For full memory system details, see the [memory system reference](../.github/skills/afternoon-pipeline/references/memory-system.md).

## Design Decisions

### Why sequential, not parallel?
Each agent's output is the next agent's input. The slophunter can't hunt slop that hasn't been written yet. The style-editor can't polish voice on unexpanded scenes. Sequential processing is the only correct approach.

### Why a separate plan-verifier?
The planner handles structure and web research. The plan-verifier handles continuity, transitions, and pacing authority. Combining them would create a single agent trying to do two fundamentally different jobs — one creative (enrichment) and one analytical (continuity annotation). Separation lets each agent focus.

### Why doesn't the orchestrator read prose?
Keeps the router simple and deterministic. If the orchestrator could evaluate quality, it would need to make subjective decisions about retries, and its judgment would be unreliable. Binary success/failure via status.json is clean and testable.

### Why per-entity memory instead of a single ledger?
Targeted reads. A chapter about two characters in one location reads ~3 entity files instead of a 50-page master document. This keeps context windows lean and prevents the writer from drowning in irrelevant continuity data.

### Why is the expander optional?
Not every story needs intimate scene expansion. Literary fiction, mystery, or adventure stories may want the tighter prose that comes straight from the grounder. The config kill switch (`agents.expander.enabled: false`) lets the pipeline skip expansion without changing any agent code — the orchestrator copies `v2g.md` to `v3.md`.
