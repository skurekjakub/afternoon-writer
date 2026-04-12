# Afternoon Fiction Pipeline — Architecture

An autonomous multi-agent pipeline that transforms beat-plan outlines into polished prose chapters. Up to twelve specialized agents run sequentially, each reading the previous agent's output and producing input for the next. A pure-router orchestrator coordinates dispatch without ever reading prose content.

**Updated:** 2026-04-06

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [Agent Flow](#agent-flow)
3. [Agent Roles](#agent-roles)
4. [Deterministic Analysis Tools](#deterministic-analysis-tools)
5. [Artifact Versioning](#artifact-versioning)
6. [Directory Layout](#directory-layout)
7. [Data Flow](#data-flow)
8. [Orchestrator Design](#orchestrator-design)
9. [Memory System](#memory-system)
10. [Design Decisions](#design-decisions)

---

## Pipeline Overview

The afternoon pipeline converts user-authored beat outlines into finished fiction chapters. It operates on a simple principle: separate concerns completely. No single agent handles more than one job. The writer writes. The slophunter hunts slop. The style-editor polishes voice. Each agent is an expert at exactly one thing.

The pipeline processes chapters sequentially — chapter 2 cannot start until chapter 1 is fully complete, including the memory-keeper's continuity update. This guarantees that every chapter has access to the full continuity state from all prior chapters.

The specialist pipeline agents run on `gpt-5.4`; the orchestrator runs on `claude-sonnet-4.6`. All prose uses Limited Third Absolute POV. All characters are women or futas (she/her pronouns exclusively).

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
  Style-Editor ←── Expander ←── Grounding-Gate ←── Grounder ←── Slop-Gate ←── Slophunter ←── v1.md
  (voice polish,    (scene          (adversarial        (world-specificity  (adversarial    (AI pattern
   continuity,       expansion,      grounding audit,    grounding, map-    slop audit,     elimination,
   7 checks)         if enabled)     optional revision)  driven revision)   revision loop)  11 targeted hunts)
       │
       ▼
  Style-Auditor ──→ Final-Slophunter ──→ Continuity-Gate ──→ Memory-Keeper
  (style-guide       (polish-mode          (adversarial           (catalogues what happened,
   enforcement,       slop elimination,     continuity audit,      updates per-entity ledgers
   if guide exists)   register pass)        revision loop)         for future chapters)
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
**AI pattern eliminator.** Reads `v1.md` and executes 11 targeted hunts: wordcount reduction, hard caps on overused words, all hitlist items, telegram prose, opener tics, filter words, image repetition, which-meant syndrome, essay paragraphs, biography insertions, and temporal beat transitions. Surgical replacement — never adds content. Outputs `v2.md` plus notes JSON with before/after counts. Its dialogue-register hunt also kills fake simplification: dialogue that claims to translate specialist reasoning into plain speech but still stays schematic. Also runs in revision mode when the slop-gate fails — applies both pass A and pass B suggested fixes (with latitude for voice/flow), then runs a rewrite self-audit on changed passages to catch violations introduced by the rewrites. The slop hitlist remains enforced here, not as a separate slop-gate pass.

### Slop-Gate
**Adversarial slop auditor with fix suggestions.** Reads `v2.md` and audits it in two passes. **Pass A** handles the high-confidence mechanical guides (negation, intent smear, recurring prose tics). **Pass B** handles the contextual guides (GPT-5 prose issues, narrator seep, phantom concreteness, fake simplification). For each KILL finding, writes a concrete `suggestedFix` (replacement text), cross-checked against the current pass guide pack to prevent the replacement from violating other rules inside that pass. The gate's detection surface now splits two nearby failures: phantom concreteness covers lines that sound precise or intellectual without cashing out into named specifics, observable carriers, local evidence, or plain claim, while fake simplification covers dialogue pretending to simplify into street terms while still withholding the actionable target. Uses iteration-aware conservatism: later iterations prefer deletion and minimal substitution over creative rewrites. If either pass fails, the orchestrator re-dispatches the slophunter in revision mode, the slophunter applies both note sets, then both passes re-audit the revised file independently. This loop continues up to `maxIterations` (configurable, default 5). Only when both passes pass does the clean `v2.md` proceed to the grounder. Can be disabled per-story via config.

### Grounder
**World-specificity grounding by exemplar.** Reads `v2.md`, the plan, memory files, materials, and the grounding skill's exemplar pairs. Before editing, it writes `grounding-map.json`, then grounds scene by scene. It still runs a dedicated dialogue-grounding pass and a separate final-third audit, but those rules now live in the grounder prompt rather than in the framework skill. Sources all proper nouns from memory, materials, and plan — never invents. Can be disabled per-story via config (`agents.grounder.enabled: false`). On failure, orchestrator copies `v2.md` to `v2g.md`, skips the grounding-gate, and proceeds — does not block. Outputs `v2g.md`, `grounding-map.json`, and `grounder-notes.json`.

### Grounding-Gate
**Adversarial grounding verifier.** Reads `v2g.md`, the verified plan, targeted memory, and the dedicated `prose-grounding-audit` skill. It does not trust the grounder's own map or notes. Instead it runs a fresh sweep for white-room paragraphs, contactless dialogue, generic fallback nouns, tail attenuation, over-grounding, rhythm damage, and unsourced specificity. A few local carrier beats do not clear a long conceptual run, and late generic fallback can still fail even when route logic remains legible. On fail, it writes local `suggestedFix` values and the orchestrator re-dispatches the grounder in revision mode. The loop is best-effort: after `agents.groundingGate.maxIterations` (default `3`), the orchestrator promotes the latest grounded revision and continues. Can be enabled per-story via config (`agents.groundingGate.enabled: true`). Outputs `grounding-gate-notes*.json`, `grounding-gate-scratchpad*.md`, and a verdict-bearing status file.

### Expander
**Scene expansion editor.** Reads `v2g.md` and the plan's `expansionLevel` per beat. Expands underwritten intimate and emotional scenes using a 6-question test. Three levels: high (moment-by-moment), medium (add reactions/detail), low (1-2 sensory anchors). Can be disabled per-story via config — orchestrator does `cp v2g.md v3.md` and skips dispatch. Outputs `v3.md`.

### Style-Editor
**Voice and continuity polish.** Reads `v3.md`, story overview, style target, style-guide.json (if available), voice sheets, prior chapter, memory files. Seven quality checks: voice consistency, Limited Third compliance, continuity/anti-reintroduction, sentence variety, beat transitions, slophunter leftovers, and dialogue register. Does not add content or cut beats — only polishes. Outputs `v4.md`.

**Revision mode (texture enrichment):** Dispatched when the style-auditor's `textureVerdict` is `"fail"`. Reads the auditor's `textureFindings` (flagged zones + enrichment instructions) and adds structural texture — participial phrases, compound clauses, em-dashes, semicolons — in the flagged zones only. Does not re-run the full 7-check process. Outputs `v4-r{N}.md`.

### Style-Auditor ↔ Style-Editor Texture Loop
**Adversarial style-guide enforcement + texture convergence.** Initial pass reads `v4.md` against `.afternoon/style-guide.json`, verifies every specification field (sentence rhythm, vocabulary register, metaphor density, paragraph structure, dialogue ratio, per-POV voice fingerprints, quality floor metrics, and structural texture via rhythm_scorer), and produces `v4b.md`. Emits `textureVerdict: "pass"|"fail"` in status.json — if `"fail"`, the orchestrator enters a texture revision loop (max 5 iterations). In the loop, the auditor is measurement-only (no prose edits) — same pattern as the slop-gate. The style-editor applies structural texture enrichment; the auditor re-measures and reports. On pass or exhaustion, latest editor revision promotes to `v4b.md`. Requires `style-guide.json` — skipped if absent.

### Final-Slophunter
**Polish-mode slop elimination.** Runs the slophunter in polish mode on `v4b.md` (or `v4.md` if style-auditor was skipped). Register and document-voice pass. 20% wordcount reduction target. Outputs `v5.md`.

### Continuity Gate ↔ Final-Slophunter Continuity Loop
**Adversarial continuity verification.** Reads `v5.md` against the beat plan's knowledge ledger, memory files, previous chapters, and cast/handoff rules. Builds a knowledge timeline tracking what the POV character knows at each point, then audits the prose for premature reveals, cast errors, arc violations, and physical continuity breaks. A single hard violation is an automatic fail. Writes findings JSON with structured evidence and suggested fixes. On fail, the orchestrator re-dispatches the final slophunter in continuity-revision mode; the slophunter applies the fixes and the gate re-audits. Loop runs up to 3 iterations. Does NOT read prose-quality materials — only story structure documents.

### Memory-Keeper
**Continuity librarian.** Reads `v5.md` and the verified plan. Updates per-entity JSON+MD files across five categories: characters, locations, relationships, threads, world. Handles merge logic for entities that appeared in prior chapters. Does NOT read the story overview — it catalogues what was written, not what was planned.

### Outline-Builder (user-invocable)
**Interactive planning assistant.** Not part of the automated pipeline. Reads anti-slop rules, craft references, story overview, materials, and existing memory. Enters an elicitation loop with the user (up to 5 rounds) to build a detailed beat plan with scene/sequel typing, value shifts, sensory anchors, and transition fields. Outputs to `.afternoon/outlines/`.

### Style-Extractor (user-invocable)
**Style-guide extraction.** Not part of the automated pipeline. Reads prose samples from `config.priming.proseSamples`, story overview, voice sheets, and character memory profiles. Runs `tools/rhythm_scorer/score.py --json` on the style source to measure 14 metrics (rhythm + texture), then transforms tool output into the style-guide schema. Extracts abstract patterns (sentence rhythm, vocabulary register, metaphor density, emotional expression, dialogue style, narrative distance, paragraph structure, descriptive approach), builds contrastive pairs (bad→good AI failure corrections), anchors prose excerpts, and produces `.afternoon/style-guide.json`. The style guide's `rhythmMetrics` and `textureMetrics` sections provide the single source of truth for all downstream metric targets — no agent hardcodes threshold values. Run once per story or when samples change.

## Deterministic Analysis Tools

Three Python tools in `tools/` provide deterministic prose analysis that complements LLM judgment. All use stdlib only — no heavy NLP dependencies.

### rhythm_scorer

Measures 14 metrics across rhythm and structural texture. Outputs JSON, human-readable summary, or side-by-side comparison.

**Rhythm metrics:** comma:period ratio, sentence mean/CV/short%/long%, opener entropy, one-sentence paragraph %, MATTR.
**Texture metrics:** participial phrase %, compound clause %, em-dash %, semicolon %, short sentence %, composite texture score, verdict (within_target / borderline / below_target), interpretation (agent-actionable fix instructions), flagged passages (telegram runs, texture deserts).

Modes: `--json`, `--summary`, `--compare`. Accepts `--baselines <style-guide.json>` to load `textureMetrics` for verdict calibration, and `--target-json <style-guide.json>` for comparison mode.

**Consumed by:** Style-extractor (measures the style source), Slop-gate Phase 1b (measures each chapter draft), Style-auditor (measures chapter against targets).

### skeleton_strip

Extracts syntactic skeleton and concreteness signals from prose. Uses Brysbaert concreteness norms + 12 regex patterns. Identifies abstract runs, vague verbs, and sensory-deficit zones.

### slop_checker

Pattern-based AI prose detection. 137 patterns across 24 categories plus slopsquid statistical AI-overuse n-grams (122 bigrams + 416 trigrams, zero tolerance). Reports per-category violation counts, cap breaches, and pattern instances with context.

**Consumed by:** Slop-gate Phase 1b (pre-audit signal), human review.

## Artifact Versioning

Each chapter produces seven primary draft versions, each improving on the last, plus optional audit/revision artifacts around the two gates:

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

The grounding-gate does not create a new canonical prose stage. It audits grounded prose and, if needed, forces numbered grounded revisions (`v2g-rN.md`) until one is promoted back to canonical `v2g.md`.

Each editor also produces notes/audit artifacts logging what changed or what was flagged, so you can trace what happened at each stage.

## Directory Layout

```
.afternoon/
├── config.json                    # Project settings (user-authored)
├── overview.md                    # Story overview — arc, themes, destination (mandatory)
├── manifest.json                  # Orchestrator state + crash recovery
├── style-guide.json               # Extracted style specification (style-extractor output)
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
│   ├── v2g-r*.md                  # Grounder revision drafts during grounding-gate loop
│   ├── grounding-map.json         # Grounder execution scaffold
│   ├── grounding-map-r*.json      # Revision grounding maps
│   ├── v3.md                      # Expander output (or cp of v2g)
│   ├── v4.md                      # Style-editor output
│   ├── v4-r*.md                   # Style-editor texture revision drafts during auditor loop
│   ├── v4b.md                     # Style-auditor output (absent if style-guide.json missing)
│   ├── v5.md                      # Final-slophunter output
│   ├── v5-cr*.md                  # Continuity-revision drafts (absent if continuity gate passes first time)
│   ├── final.md                   # Assembled (cp of v5.md)
│   ├── slophunter-notes.json      # Change log
│   ├── slophunter-revision-r*-notes.json  # Revision change logs (absent if gate passes first time)
│   ├── slop-gate-notes-a.json     # Pass A KILL findings only (absent if gate disabled)
│   ├── slop-gate-notes-b.json     # Pass B KILL findings only (absent if gate disabled)
│   ├── slop-gate-notes-r*?.json   # Re-audit KILL findings per iteration/pass (e.g. r1a, r1b)
│   ├── slop-gate-scratchpad-a.md  # Pass A KEEP decisions for human audit (absent if gate disabled)
│   ├── slop-gate-scratchpad-b.md  # Pass B KEEP decisions for human audit (absent if gate disabled)
│   ├── slop-gate-scratchpad-r*?.md # Re-audit KEEPs per iteration/pass (e.g. r1a, r1b)
│   ├── grounding-gate-notes.json  # Grounding-gate KILL findings + suggestedFix (absent if gate disabled/skipped)
│   ├── grounding-gate-notes-r*.json
│   ├── grounding-gate-scratchpad.md
│   ├── grounding-gate-scratchpad-r*.md
│   ├── expander-notes.json        # Change log (absent if expander disabled)
│   ├── grounder-notes.json        # Change log (absent if grounder disabled/degraded)
│   ├── grounder-revision-r*-notes.json
│   ├── style-notes.json           # Change log
│   ├── style-editor-revision-r*-notes.json  # Texture revision change logs (absent if auditor passes first time)
│   ├── style-auditor-notes.json   # Change log + textureFindings (absent if style-guide.json missing)
│   ├── style-auditor-notes-r*.json # Re-audit notes per texture loop iteration
│   └── final-slophunter-notes.json # Change log
│   ├── continuity-findings.json   # Continuity gate findings (absent if gate passes first time)
│   ├── continuity-revision-r*-notes.json  # Continuity revision change logs
│
└── agents/{agent-name}/
    └── status.json                # Per-agent completion status
```

## Data Flow

### Forward flow (each agent feeds the next)

The story overview feeds into all content-producing agents (planner, plan-verifier, writer, slophunter, style-editor) and the outline-builder. It provides story-arc context — where this chapter fits in the whole narrative.

`style-guide.json` feeds metric targets to the writer (texture awareness), slop-gate (Phase 1b tool baselines), style-editor (texture targets), style-auditor (all specifications), slophunter (texture protection), and expander (texture self-audit).

```
overview.md ──→ (read by Planner, Plan-Verifier, Writer, Slophunter, Style-Editor, Outline-Builder)

outlines/{chapterId}.md ──→ Planner ──→ {chapterId}-initial.json ──→ Plan-Verifier
                                                                          │
{chapterId}.json ←───────────────────────────────────────────────────────┘
       │
       ├──→ Writer ──→ v1.md ──→ Slophunter ──→ v2.md ──→ [Slop-Gate ↔ revision loop] ──→ Grounder ──→ [Grounding-Gate ↔ revision loop] ──→ v2g.md ──→ Expander ──→ v3.md
       │                                                                                                                            │
       └──→ (requiredMemory field tells Writer + Style-Editor which memory files to read)                 │
                                                                                                             │
       Style-Editor ──→ v4.md ──→ Style-Auditor ──→ v4b.md ──→ Final-Slophunter ──→ v5.md ──→ [Continuity-Gate ↔ revision loop] ──→ final.md ──→ Memory-Keeper
                                      ↑         │
                                      │  texture │ (if textureVerdict: "fail")
                                      │  loop    ↓
                                      └── Style-Editor (revision) ←── auditor-notes.json
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
5. Second failure → usually mark chapter "blocked", move to next

Important exceptions:
- **Slop-Gate** and **Grounding-Gate** audit failures are not operational failures. They return `status: "completed"` with `verdict: "fail"` and enter their revision loops.
- **Grounder** second failure degrades gracefully (`cp v2.md → v2g.md`) and skips the grounding-gate.
- **Style-Auditor** failure caused by missing `style-guide.json` is treated as a skip, not a block.

### Crash recovery
If `manifest.json` exists with `"status": "in-progress"`:
1. Read `currentChapter` and `currentAgent`
2. Check for active slop-gate loop: if `slopGateLoop` exists in manifest, resume from the loop phase (`awaiting-revision`, `awaiting-reaudit-a`, `awaiting-reaudit-b`, or `awaiting-promote`)
3. Check for active grounding-gate loop: if `groundingGateLoop` exists in manifest, resume from the loop phase
4. Standard recovery: check that agent's `status.json`:
   - Shows completed for this chapter → manifest wasn't updated → fix manifest, advance
   - Missing or shows different chapter → re-dispatch the agent
5. Continue from that point

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
