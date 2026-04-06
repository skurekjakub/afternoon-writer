# afternoon-pipeline

Autonomous multi-agent fiction writing pipelines built on the [agent-as-function pattern](https://github.com): a pure-router orchestrator dispatches specialized subagents sequentially, communicating exclusively through filesystem artifacts. No orchestrator reads prose content.

This repo contains four pipelines: **Afternoon** (primary), **Afterhours**, **Tuesday**, and the **Explicit Book Engine**.

---

## Afternoon Pipeline

The primary pipeline. Transforms user-authored beat outlines into polished fiction chapters through up to twelve sequential agents.

### How it works

You write a story overview and chapter beat plans. You run the pipeline. You come back to finished chapters.

```
Planner ──→ Plan-Verifier ──→ Writer ──→ Slophunter ──→ Slop-Gate
                                                             │
                                              (revision loop if failed)
                                                             │
                                                         Grounder
                                                             │
                                                         Expander
                                                             │
                                                       Style-Editor
                                                             │
                                                      Style-Auditor
                                                             │
                                                  Final-Slophunter
                                                             │
                                                      Memory-Keeper
```

The **Outline-Builder** and **Style-Extractor** sit outside this flow — user-invocable helpers, not pipeline stages.

### Agent roles

| Agent | Input | Output | Job |
|---|---|---|---|
| **Planner** (Hermione) | User outline, series-meta | `{chapterId}-initial.json` | Validate beat structure, enrich with web research. No continuity. |
| **Plan-Verifier** (Scheherazade) | Planner output, all memory | `{chapterId}.json` | Annotate continuity, write chapter bridge, pacing authority. |
| **Writer** | Verified plan | `v1.md` | Raw first draft, beat-by-beat. |
| **Slophunter** | `v1.md` | `v2.md` | 11 targeted AI-pattern hunts. 20% wordcount reduction target. |
| **Slop-Gate** | `v2.md` | pass/fail + suggested fixes | Adversarial slop audit. On fail: triggers slophunter revision loop (up to `maxIterations`). |
| **Grounder** | `v2.md` | `v2g.md` | World-specificity enrichment by exemplar. Named geography, institutions, material texture. 40–70% growth. Graceful degradation on failure. |
| **Expander** | `v2g.md` | `v3.md` | Intimate/emotional scene expansion. Optional via config. |
| **Style-Editor** | `v3.md` | `v4.md` | Voice polish, Limited Third compliance, 7 quality checks. |
| **Style-Auditor** | `v4.md`, `style-guide.json` | `v4b.md` | Adversarial style-guide enforcement. Skipped if `style-guide.json` absent. |
| **Final-Slophunter** | `v4b.md` or `v4.md` | `v5.md` | Polish-mode slop and register pass. |
| **Memory-Keeper** | `v5.md`, verified plan | per-entity files | Catalogue characters, locations, relationships, threads, world facts. |
| **Outline-Builder** | User conversation | `.afternoon/outlines/chapter-N.md` | Interactive beat plan builder. Not dispatched by orchestrator. |
| **Style-Extractor** | Prose samples | `.afternoon/style-guide.json` | Extracts style patterns for downstream enforcement. Run once per story. |

### Draft versions

Each chapter produces up to seven named drafts, each building on the last:

| File | Agent | What happened |
|---|---|---|
| `v1.md` | Writer | Raw draft from the verified plan |
| `v2.md` | Slophunter | AI patterns eliminated (may include gate revision iterations) |
| `v2g.md` | Grounder | World-specificity grounding (or `cp v2.md` if disabled/degraded) |
| `v3.md` | Expander | Scene expansion (or `cp v2g.md` if disabled) |
| `v4.md` | Style-Editor | Voice and continuity polished |
| `v4b.md` | Style-Auditor | Style-guide enforced (absent if no `style-guide.json`) |
| `v5.md` | Final-Slophunter | Final polish |
| `final.md` | Orchestrator | `cp v5.md final.md` (assembly step) |

Each editor also writes a notes JSON logging all changes with before/after counts.

### Setup

**Step 1 — Create the working directory:**
```bash
mkdir -p .afternoon/outlines
```

**Step 2 — Write the story overview:**
```
.afternoon/overview.md
```
Every content-producing agent reads this. Include: premise, characters (name, want, fear, arc), arc shape, themes, threads, world notes, tone targets. Do NOT include chapter-by-chapter synopses (that belongs in outlines).

**Step 3 — Create chapter outlines:**
```
.afternoon/outlines/chapter-1.md
.afternoon/outlines/chapter-2.md
```
Use the normalized planner-facing schema: chapter header, `Meta info`, open-state knowledge ledger, `## Arc position`, cast/handoff rules, scene blocks, chapter close. Use the **Outline-Builder** agent interactively if you prefer guided elicitation.

**Step 4 — Write the config:**
```
.afternoon/config.json
```

```json
{
  "project": "my-story",
  "pov": "limited-third",
  "storyOverview": ".afternoon/overview.md",
  "characters": {
    "voiceSheets": "stories/my-story/voices/"
  },
  "materials": [
    "stories/my-story/00-index.md"
  ],
  "priming": {
    "antiSlop": [
      "references/slop-hitlist.md",
      "references/ai-quirks/sentence-level/",
      "references/ai-quirks/paragraph-level/",
      "editor-guide.md"
    ],
    "craft": [
      "external-resources/author-technique-anchors.md",
      "chapter-focus-points.md"
    ],
    "styleTarget": "path/to/style-sample.md"
  },
  "agents": {
    "expander": { "enabled": true },
    "grounder": { "enabled": true },
    "slopGate": { "enabled": true, "maxIterations": 5 }
  },
  "completionMarker": "===AFTERNOON DONE==="
}
```

**Step 5 — (Optional) Extract a style guide:**

Run the **Style-Extractor** agent once, pointing it at your prose samples. Produces `.afternoon/style-guide.json` which the style-auditor, style-editor, and slophunter enforce.

**Step 6 — Run:**
```bash
./afternoon-start.sh
```

### Directory layout

```
.afternoon/
├── config.json                     # Project settings
├── overview.md                     # Story overview (mandatory)
├── manifest.json                   # Orchestrator state + crash recovery
├── style-guide.json                # Style spec (optional, user-generated via style-extractor)
│
├── outlines/                       # User-authored beat plans
│   ├── chapter-1.md
│   └── chapter-2.md
│
├── plans/
│   ├── series-meta.md              # Cross-invocation planning notes
│   ├── chapter-1-initial.json      # Planner output
│   ├── chapter-1.json              # Verified plan (all downstream agents read this)
│   └── memory/
│       ├── characters/
│       │   ├── _index.json
│       │   └── {slug}.json + .md
│       ├── locations/
│       ├── relationships/
│       ├── threads/
│       └── world/
│
└── chapters/chapter-1/
    ├── v1.md … v5.md + final.md
    ├── slophunter-notes.json
    ├── slop-gate-notes.json
    ├── grounder-notes.json
    ├── expander-notes.json
    ├── style-editor-notes.json
    └── style-auditor-notes.json
```

### Config field reference

| Field | Required | Description |
|---|---|---|
| `project` | Yes | Project identifier for manifest and logs |
| `pov` | Yes | POV mode. Currently always `"limited-third"` |
| `storyOverview` | Yes | Path to story overview markdown. Orchestrator exits if missing. |
| `characters.voiceSheets` | Yes | Directory with per-character voice files |
| `materials` | No | Additional reference files (world indexes, voice sheets) |
| `priming.antiSlop` | Yes | Slop detection resources — files and directories |
| `priming.craft` | Yes | Craft technique reference files |
| `priming.styleTarget` | Yes | Style target file — register, rhythm, and tag density to match |
| `agents.expander.enabled` | No | `false` skips expander (`cp v2g.md v3.md`). Default `true` |
| `agents.grounder.enabled` | No | `false` skips grounder (`cp v2.md v2g.md`). Default `true` |
| `agents.slopGate.enabled` | No | `false` skips slop-gate entirely. Default `true` |
| `agents.slopGate.maxIterations` | No | Max revision cycles before halt. Default `5` |
| `completionMarker` | Yes | String printed on completion. Start script watches for this. |

All paths are relative to the repository root.

### Design principles

**Separated concerns.** No agent does two jobs. The planner validates structure. The plan-verifier handles continuity. The writer writes. Editors edit.

**Pure-router orchestrator.** The orchestrator never reads prose, plans, or memory — only manifest and `status.json` files from each agent. This keeps the orchestrator's context window small and makes crash recovery reliable.

**Filesystem artifact handoff.** Agents communicate by writing files. The orchestrator reads only status and routing signals. This means any agent can be re-dispatched or replaced without rewriting the orchestrator.

**Adversarial verification.** The slop-gate is an adversarial auditor of the slophunter's output, not a second slophunter. It audits, proposes cross-validated fixes, and emits pass/fail — the slophunter applies specific fixes on revision, not free-form rewrites.

**Per-entity memory.** The memory-keeper writes one file per entity (character, location, relationship, thread, world fact) plus a lightweight `_index.json` for discovery. No monolithic continuity ledger that grows unbounded.

**Crash recovery.** The manifest records every chapter's state. On restart, the orchestrator skips completed work and resumes from the last incomplete chapter.

---

## Other Pipelines

### Afterhours Pipeline

```
brief.md → Planner → Writer → Slop-Editor → Expander → Style-Editor → Final-Editor → final.md
```

Chunk-based pipeline for standalone fiction. The orchestrator dispatches the planner once per chapter, then runs a 5-agent editing lane per chunk. Seven agents total. Start with `afternoon-start.sh` (same retry-loop pattern).

Working directory: `.afterhours/`

### Tuesday Pipeline

```
tuesday-guide → task-graph.json
    ↓
tuesday-writer (orchestrator) → per chapter:
    context-scout → scene-miner → blueprint-composer
        → writing-coordinator:
            prose-writer → ai-prose-gate → quality-auditor → style-auditor
            (revision loop)
        → line-editor → memory-keeper
```

Twelve agents. Uses a 3-agent audit gate (AI gate → quality auditor → style auditor) with a revision loop, rather than a linear editing pass. Outputs to `omakes/`. Start with `tuesday-start.sh`.

### Explicit Book Engine

```
seed.md → Architect (standalone) → approval.json
              ↓ (after approval)
    Orchestrator → Chapter-Planner → Chapter-Writer
        → Slop-Editor → Style-Editor → Payoff-Keeper
        → Sequel-Bootstrapper
```

Cold-start book generation from a seed file. The architect runs once and stops for user approval. The orchestrator picks up after `approval.json` exists with `"approved": true`. Per-story runtime state lives under `{story_dir}/.booksmith/`.

### Ravencrest / Morgana

Story-specific autonomous pushers for the Ravencrest series and Morgana the Weaver iterative plotter. Each runs via a dedicated start script and uses its own skill for showrunner/planning logic.

---

## Repository Structure

```
.github/
├── agents/                         # All agent .agent.md files
├── skills/                         # Domain knowledge skills (loaded by agents at runtime)
│   ├── afternoon-pipeline/         # Afternoon pipeline domain knowledge
│   ├── agent-as-function/          # Multi-agent pattern reference
│   ├── prose-slop-elimination/
│   ├── prose-voice-saturation/
│   └── ...
└── copilot-instructions.md         # Repository-wide rules and pipeline summaries

docs/
├── afternoon-pipeline-architecture.md   # Agent roles, data flow, design decisions
├── afternoon-pipeline-technical.md      # Config schema, artifact formats, protocols
├── afternoon-pipeline-guide.md          # Setup and usage guide
└── afternoon-pipeline-changelog.md      # Structural change history

references/
├── slop-hitlist.md                 # 25+ banned AI writing patterns with hard rate limits
└── ai-quirks/                      # Categorized AI prose failure patterns

resources/
├── intent-smear-agency-laundering-guide.md
├── narrator-seep-guide.md
├── negation-addiction-hunting-guide.md
└── recurring-prose-tics.md

external-resources/
├── author-technique-anchors.md     # Prose craft reference
├── character-voice-sheets.md       # Character voice and interaction dynamics
└── ...

stories/                            # Story-specific files (outlines, characters, voices)
chapter-focus-points.md             # Intimate scene expansion philosophy
editor-guide.md                     # Prose trimming guidelines
```

---

## Shared Resources

All pipelines share these prose-quality resources:

| Resource | Purpose |
|---|---|
| `references/slop-hitlist.md` | Master list of banned AI writing patterns with hard rate limits |
| `editor-guide.md` | What to cut first — prose trimming guidelines |
| `chapter-focus-points.md` | Intimate scene expansion philosophy |
| `external-resources/author-technique-anchors.md` | Author craft reference |
| `external-resources/character-voice-sheets.md` | Character voices and interaction dynamics |
| `.github/skills/prose-slop-elimination/` | Routed slop-hitlist use by pass type |
| `.github/skills/prose-voice-saturation/` | Voice saturation primers and vocabulary anchors |
| `.github/skills/prose-explicit-prose-craft/` | Direct explicit prose craft — vocabulary, scene architecture, act rotation |

---

## Further Reading

- [Architecture](docs/afternoon-pipeline-architecture.md) — agent roles, data flow, orchestrator design, memory system, design decisions
- [Technical Reference](docs/afternoon-pipeline-technical.md) — config schema, artifact formats, agent protocols
- [User Guide](docs/afternoon-pipeline-guide.md) — setup, configuration, running, troubleshooting
- [Changelog](docs/afternoon-pipeline-changelog.md) — structural changes with root cause and per-file descriptions
# afternoon-writer
