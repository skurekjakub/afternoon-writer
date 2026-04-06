

## No Backward Compatibility

When refactoring or removing a concept from the codebase, delete it completely. Never leave behind annotations, comments, "REMOVED" markers, "formerly X" notes, or any other backward-compatibility breadcrumbs. The old concept should vanish as if it never existed. Only preserve backward compatibility if the user explicitly asks for it.

## No Git

Never interact with git. No `git status`, `git diff`, `git stash`, `git commit`, `git log`, `git checkout`, or any other git command. The user manages version control. Agents edit files and nothing else.

## Documentation Maintenance

When modifying agent files, pipeline behavior, config schemas, skill references, or any structural aspect of the pipelines, update ALL affected documentation in the same session. Documentation lives in three layers — all three must stay consistent:

1. **`docs/` directory** — User-facing guides and architecture overviews (`docs/afternoon-pipeline-*.md`, `docs/tuesday-verse-agent-family.md`)
2. **Skill references** — Technical references consumed by agents (`.github/skills/*/references/*.md`)
3. **`copilot-instructions.md`** — Repository-wide rules and pipeline summaries (this file)

When adding a new config field, agent, or pipeline feature: update the relevant agent files, then the skill references that describe those agents, then the docs that explain the pipeline to users, then this file if the pipeline summary section is affected. No partial updates — if you changed the behavior, update every document that describes it.

**Changelogs:** The afternoon pipeline maintains `docs/afternoon-pipeline-changelog.md`. When making structural changes to the afternoon pipeline (new agents, behavior changes, config fields, convergence fixes), append an entry at the top of this file describing the problem, root cause, and per-file changes. New entries go at the top.

## Web Search Fallback

If no dedicated `web_search` tool is available, use `web_fetch` with DuckDuckGo Lite for search queries: `https://lite.duckduckgo.com/lite/?q=your+search+terms`. This returns plain HTML that parses cleanly. Do NOT attempt Google Search URLs — they return JavaScript-heavy pages that cannot be parsed.

## Large File Handling

Agents writing files larger than ~5KB risk Copilot CLI timeouts. Read the **`large-file-handling` skill** (`.github/skills/large-file-handling/SKILL.md`) for the full pattern — it covers the bash heredoc append method, the shell security scanner trap, and the create-tool fallback. Mount this skill on any agent that writes prose, plans, outlines, or memory files.

### Quick summary

- **Always create files sequentially**: Use the `create` tool for new files and `edit` tool for modifications. Do NOT use bash heredocs (`cat << 'EOF'`) — the CLI shell security scanner blocks content containing words like `kill`, `$`, backticks, or other patterns it interprets as shell expansion, even inside single-quoted heredoc delimiters. The `create` and `edit` tools bypass the shell entirely and work reliably for all content.
- **Split large writes**: For files exceeding ~5KB, write in multiple sequential `edit` calls appending sections. Or use Python: `python3 -c "..."` with file writes, which also bypasses shell content scanning.
- **Per-entity splitting**: Files that grow across runs should split into one file per entity (not one monolith). Each entity file stays small (~2-5KB forever). Use `_index.json` for cheap discovery.
- **Targeted reads**: "Lost in the Middle" effect means LLMs attend weakly to mid-context. Read only the files you need, JSON before markdown, indexes before full profiles. Re-read critical rules between passes.

See `.github/skills/large-file-handling/references/patterns.md` for concrete examples (prose chapters, JSON plans, per-entity memory, outlines).

## Todolist-Driven Structured Passes

Worker agents (any agent doing substantive work — writing, editing, analysis, cataloguing) organize execution as **sequential todo-driven passes** tracked via the todolist tool with todo-dependencies. Each pass has one concern. This produces more reliable output than monolithic "do everything" instructions.

Standard pattern: Create todos in order, each depending on the previous. Read inputs → domain-specific passes → self-audit → write output. Mark in-progress before starting, done when complete, query for next ready todo.

Pure routers/orchestrators skip this pattern — they dispatch, they don't do passes.

See the agent-as-function skill (`.github/skills/agent-as-function/SKILL.md`, "Todolist-Driven Structured Passes" section) for the full pattern, common pass sequences by agent type, and design rationale.

---

## Ravencrest Planning

`ravencrest-pusher.agent.md` uses `.github/skills/ravencrest-showrunner-workflow/SKILL.md` as its source of truth. Use that skill whenever planning the next Ravencrest chapter or syncing the Ravencrest Morgana ledgers.

Ravencrest uses an active brief under `{story_dir}/.morgana/`

Ravencrest also uses `{story_dir}/.morgana/story-state.md` as the authoritative event-memory and mini-arc surface. It tracks what changed, who witnessed it, what the current arc still owes, which ecosystems are live, which mainstays are forming, and which POVs are due.
Ravencrest also uses `{story_dir}/.morgana/year-arc.md` for year-level promises and `{story_dir}/.morgana/mini-arcs/arc-XX.md` files for per-arc campaign tracking.
Ravencrest also uses `{story_dir}/.morgana/notes.md` as the freshness/cooldown dashboard, `{story_dir}/spice-meter.md` as the cumulative act/heat ledger, and `{story_dir}/.morgana/status.json` as the machine-readable worker handoff to the orchestrator.
Keep `{story_dir}/characters/_index.json` and `{story_dir}/location/_index.json` as lightweight discovery surfaces, then split reusable cast and worldbuilding docs per entity rather than into a single growing bible.
On a fresh run, bootstrap `notes.md`, `spice-meter.md`, `.morgana/changelog.md`, and `{story_dir}/outlines/` alongside the state boards before choosing Chapter 1.

Ravencrest chapters do not all need to be onstage Taylor-sex chapters. Non-Taylor POV chapters, nonsexual consequence chapters, and chapters where established cast members collide or sleep together while Taylor is offscreen are valid when they materially alter the board Taylor returns to.

The most important rule in that skill is the explicitness rule for outline beats: major erotic sequences must be expanded into longer, mechanically specific mini-scenes with direct body/action language. Do not accept compressed summary beats or tasteful fade-out phrasing in Ravencrest outlines.
For direct explicit-beat rules and the act taxonomy, Ravencrest uses `.github/skills/prose-explicit-prose-craft/`.

Every Ravencrest chapter also needs one real **aftermath / residue engine** - cleanup, leak, mark, witness pressure, clothing disorder, soreness carryover, or another consequence that visibly survives the peak and shapes the coda or reentry.

When Ravencrest scenes use **3+ active bodies**, keep all participants in frame. No body should disappear for more than one beat. If a frontier-bucket scene or group scene still reads thin after the normal Phase 4 hardening pass, use `.github/skills/prose-explicit-scene-detailed/` as the conditional escalation tool.

Ravencrest briefs may contain a `## Mandatory Override Instructions` section. When present, that section outranks the rest of the brief, `initial-pitch.md`, notes momentum, and stale planning habits.

Ravencrest `notes.md` is tiered: **Core Heat**, **Warm Rotation**, **Cooling Bench**, **Freshness Queue**, **Open Thread Budget**, and **Archived / Dormant Threads**. Freshness outranks backlog; do not flatten those tiers back into one overdue list.

Per-character encounter progression in Ravencrest is authoritative in the character profile files via `Progression Tracking With Taylor` and `Frontier Readiness With Taylor` sections. `story-state.md` is the event-memory and mini-arc dashboard. `notes.md` is the freshness/cooldown/pressure dashboard. Do not collapse those jobs back into one file.
When a named woman becomes a real recurring player, create her character profile and voice sheet in the same dispatch. When a room or ecosystem becomes reusable, create its location profile in the same dispatch.

Ravencrest also uses a **15-chapter minimum cooldown** on **non-carrier primary top-level `omakes/scenes/2-acts/` categories** plus the chapter's headline modifier / finish / sequence labels. **Oral**, **penetration**, and **hands-fingers** are carrier acts and are not blanket-banned; they may recur, but the chapter still needs a different novelty driver. Each chapter with a major sexual run must use at least **2 major top-level `2-acts` categories**.

Ravencrest separately uses a **weighted feature-bucket pressure ledger** with **Broad Buckets** and **Frontier / Neglected Library Families**. When the recent field is carrier-heavy, the highest-weight compatible frontier bucket should usually beat an older broad bucket. Reject any Ravencrest chapter concept whose novelty can be described with only oral, penetration, hands-fingers, verbal, instruction-guidance, or silence-stealth.
For harder frontier families, a high global weight is not enough by itself - the relevant lane must be `hard-open` in the character profile. Docking and lighter implements can open earlier; anal stretch/gape, explicit watersports, fisting/stretching, sounding/pumping, throat-breath-risk material, and similar hard-payoff rows should stay locked until the lane has real progression behind it.

---

## Repository Overview: Writer Pipelines and Generic Engine

This repo contains three story-bound autonomous multi-agent pipelines plus one generic explicit-book engine. All use the agent-as-function pattern: a pure-router orchestrator dispatches specialized subagents sequentially, communicating via filesystem artifacts (JSON plans, versioned markdown drafts, status files). No orchestrator reads prose directly.

### Shared Resources

All agents share these prose-quality resources:

| Resource | Purpose |
|---|---|
| `references/slop-hitlist.md` | 25+ banned AI writing patterns with hard rate limits |
| `editor-guide.md` | Prose trimming guidelines (what to cut first) |
| `chapter-focus-points.md` | Intimate scene expansion philosophy |
| `external-resources/author-technique-anchors.md` | Author craft reference |
| `external-resources/character-voice-sheets.md` | Character voices and interaction dynamics |
| `.github/skills/prose-scene-grounding/references/` | Non-explicit scene grounding packets for action geometry, dialogue pressure, travel texture, and concrete wonder |
| `.github/skills/prose-voice-archetypes/references/` | Generic archetype voice packets for dialogue posture, social register, wit, and pressure behavior |
| `.github/skills/prose-voice-saturation/references/` | Voice saturation primers, vocabulary anchors, dialogue craft |
| `.github/skills/prose-slop-elimination/references/` | Routed use of `slop-hitlist.md` plus the `ai-quirks/` corpus by pass type |
| `.github/skills/prose-explicit-scene-detailed/references/` | Detailed afterhours sample packets for slower, denser, body-mapped explicit scene writing |
| `omakes/scenes/` | Scene permutation library (buildup → acts → modifiers → resolution → world-specific) |

### Characters

All characters are women or futas (women with cocks). No male characters. All pronouns she/her.

### POV Rule: Limited Third Absolute

Every narration sentence belongs to the current POV character's observation, thought, or inference. No omniscient commentary, no subtext translation, no emotional labels on expressions, no relationship narration. Test: "Who is saying this — the POV character or a narrator?"

---

## Afterhours Pipeline

**Start script:** `afterhours-start.sh` — launches the orchestrator in a retry loop, checks for `===AFTERHOURS DONE===` completion marker.

**Working directory:** `.afterhours/`

### Agent Flow

```
brief.md → PLANNER → WRITER → SLOP-EDITOR → EXPANDER → STYLE-EDITOR → FINAL-EDITOR → final.md
```

The orchestrator dispatches the planner once per chapter, then runs a 5-agent editing pipeline per chunk within each chapter.

### Agents (all gpt-5.4)

| Agent | File | Reads | Produces | Role |
|---|---|---|---|---|
| **Orchestrator** | `afterhours-orchestrator.agent.md` | `brief.md`, `manifest.json`, status files | `manifest.json`, `final.md` | Pure router. Never reads prose. Manages state, dispatches agents, assembles chapters, handles crash recovery. |
| **Planner** | `afterhours-planner.agent.md` | `brief.md`, continuity ledger, scene library, voice sheets | `{chapterId}.json`, `continuity.md`, `continuity.json` | Plans chapter beats using Swain scene-sequel structure and Hayes romance arc (20 beats / 4 phases). Tracks character arcs (Lie/Truth/Want/Need), intimate escalation, hook variety, try-fail outcomes. Bootstrap mode for first chapter, refinement mode after. |
| **Writer** | `afterhours-writer.agent.md` | Plan JSON, continuity, prior chunks, voice saturation files | `v1.md` | Raw first draft. Writes beat-by-beat from plan. Enforces Limited Third, sensory grounding, sentence variety, active verbs. Self-audits for hitlist violations before delivery. |
| **Slop-Editor** | `afterhours-slop-editor.agent.md` | `v1.md`, hitlist, voice refs | `v2.md` + editor notes JSON | AI pattern elimination. Ten specific hunts: telegram prose, opener tics, contact verb monotony, POV filters, image repetition, tempo defaults, verbose constructions, rule-of-three, self-negating descriptions, pattern overuse. Does not add or remove content. |
| **Expander** | `afterhours-expander.agent.md` | `v2.md`, plan's expansion directive, slop-editor flags | `v3.md` + expander notes JSON | Intimate scene elaboration. Uses 6-question expansion test. Three levels: high (moment-by-moment), medium (add reactions/detail), low (1-2 sensory anchors). Adds beats-within-beats, body-specific reactions, environmental integration, receiver agency. |
| **Style-Editor** | `afterhours-style-editor.agent.md` | `v3.md`, prior v4s, editor-guide, voice refs | `v4.md` + style notes JSON | Voice consistency, register polish, Limited Third compliance, editor-guide trimming. Six checks: voice consistency, Limited Third, register, trimming, sentence variety, catch prior-editor misses. |
| **Final-Editor** | `afterhours-final-editor.agent.md` | `v4.md`, plan JSON, voice sheets, dialogue-craft | `v5.md` + final notes JSON | Last gate. Fixes exactly six things: dialogue starvation (target 40-60%), word/phrase repetition (hard caps per 5k words), clinical anatomy in narration, POV-voice contamination, planning vocabulary leaks, fragment-stacking. |

### Artifact Versioning

Each chunk progresses: `v1.md` (raw) → `v2.md` (cleaned) → `v3.md` (expanded) → `v4.md` (polished) → `v5.md` (assembly-ready). The orchestrator concatenates all chunk `v5.md` files into `final.md`.

### Directory Layout

```
.afterhours/
├── brief.md                           # Story brief (user-authored)
├── manifest.json                      # Orchestrator state + crash recovery
├── plans/
│   ├── {chapterId}.json               # Per-chapter beat plan
│   ├── continuity.md                  # Human-readable arc tracking
│   └── continuity.json                # Structured arc tracking
├── chapters/{chapterId}/
│   ├── chunks/{chunkId}/
│   │   ├── v1.md … v5.md             # Progressive drafts
│   └── notes/
│       ├── {chunkId}-slop-editor.json # Editor change logs
│       ├── {chunkId}-expander.json
│       ├── {chunkId}-style-editor.json
│       └── {chunkId}-final-editor.json
├── chapters/{chapterId}/final.md      # Assembled chapter
└── agents/{agent-name}/status.json    # Per-agent completion status
```

### Planning Frameworks

- **Dwight Swain Scene-Sequel**: Scene beats (goal → conflict → disaster) alternate with sequel beats (emotion → dilemma → decision).
- **Gwen Hayes Romancing the Beat**: 20 romance beats across 4 phases (Setup → Falling → Retreating → Fighting for Love).
- **Character Arcs**: Lie/Truth/Want/Need per POV character. Arcs drive through test → glimpse → consequence.
- **Value Shifts**: Track emotional/relational changes per beat (e.g., "trust → doubt"). No three consecutive same-direction shifts.
- **Try-Fail Outcomes**: no-and (fail + worsen), yes-but (succeed + cost), yes (clean success, reserved for finals).
- **Intensity Scales**: Word-based, not numeric — whisper/murmur/simmer/burn/blaze/inferno for intensity; none/subtext/tension/touch/intimate/explicit/consuming for intimacy.

### Key Constraints

- All agents run sequentially, never in parallel
- One retry per agent failure, then mark chunk "blocked" and continue
- Orchestrator uses zero-yap protocol (every response must contain a tool call)
- All agents self-audit against `references/slop-hitlist.md` before delivering artifacts
- Each editor notes JSON logs all changes with before/after counts

---

## Afternoon Pipeline

**Start script:** `afternoon-start.sh` — same retry-loop pattern as afterhours.

**Working directory:** `.afternoon/`

**Documentation:** `docs/afternoon-pipeline-architecture.md`, `docs/afternoon-pipeline-technical.md`, `docs/afternoon-pipeline-guide.md`, `docs/afternoon-pipeline-changelog.md`

### Agent Flow

```
overview.md + outlines/ → PLANNER → PLAN-VERIFIER → WRITER → SLOPHUNTER → [SLOP-GATE ↔ revision loop] → [GROUNDER] → [EXPANDER] → STYLE-EDITOR → [STYLE-AUDITOR] → FINAL-SLOPHUNTER → MEMORY-KEEPER
```

The orchestrator dispatches agents sequentially per chapter. The slop-gate is enabled by default and introduces the pipeline's only cross-agent revision loop — on fail, the slophunter is re-dispatched in revision mode. The grounder is enabled by default and degrades gracefully on failure (copies v2.md to v2g.md). The expander is optional (config toggle). The style-auditor requires `.afternoon/style-guide.json` (produced by the style-extractor). The outline-builder and style-extractor are user-invocable, not dispatched by the orchestrator.

### Agents (all gpt-5.4)

| Agent | Role |
|---|---|
| **Orchestrator** | Pure router. Bootstrap gate validates story overview. Dispatches agents, manages crash recovery. Never reads prose. |
| **Planner** (Hermione) | Validates beat structure, enriches with web research. Reads and appends to `series-meta.md`. Does NOT handle continuity. |
| **Plan-Verifier** (Scheherazade) | Annotates continuity (continuityStatus, memoryRef, requiredMemory), writes transition bridges, has pacing authority. Reads and appends to `series-meta.md`. |
| **Writer** | Raw first draft from verified plan. Uses proven anti-slop priming recipe. |
| **Slophunter** | AI pattern elimination. Structured hunts with before/after counts. 20% wordcount reduction target. Three dispatch modes: primary (v1→v2), polish (v4b→v5), and revision (applies gate's pre-validated suggested fixes with voice/flow latitude, zero wordcount). |
| **Slop-Gate** | Adversarial slop auditor with fix suggestions. Audits v2.md against all `resources/*.md` guides. For each KILL, writes concrete `suggestedFix` cross-checked against co-triggered guides. Emits pass/fail verdict. On fail, triggers slophunter revision loop (up to `maxIterations`). |
| **Grounder** | World-specificity grounding by exemplar. Reads v2.md, plan, memory, materials, and a before/after chapter pair that teaches the transformation. Enriches prose with named geography, titled institutions, material texture, world-register dialogue, and physical rhythm beats. 40-70% growth expected. Graceful degradation on failure (cp v2.md → v2g.md). |
| **Expander** | Intimate/emotional scene expansion. 6-question test, 3 levels. Optional. |
| **Style-Editor** | Voice polish, continuity enforcement, 7 quality checks including dialogue register. |
| **Style-Auditor** | Adversarial style-guide enforcement. Reads v4.md against `style-guide.json`, verifies every spec field, produces v4b.md. Requires style-guide.json (skipped if absent). |
| **Final-Slophunter** | Slophunter in polish mode. Runs after style-auditor on v4b.md. Register and document-voice pass. 20% wordcount reduction target. Produces v5.md. |
| **Memory-Keeper** | Post-chapter continuity cataloguing. Per-entity JSON+MD files across 5 categories. |
| **Style-Extractor** | User-invocable. Reads prose samples from `config.priming.proseSamples`, extracts abstract patterns, produces `.afternoon/style-guide.json`. Run once per story. |
| **Outline-Builder** | User-invocable planning assistant. Interactive elicitation loop. Uses `structured-chapter-beatplan-workflow` for the normalized planner-facing chapter schema, whose `## Arc position` operationalizes story-level character canon into current stance at open, pressure source, chapter test, forced choice, and end-state shift. |

### Key Differences from Afterhours

- **Story overview** — mandatory `storyOverview` field in config, validated at bootstrap
- **Separate planner and plan-verifier** — afterhours combines these; afternoon splits structure/research from continuity/transitions
- **Per-entity memory** — afterhours uses a single continuity ledger; afternoon uses per-entity files with index-based discovery
- **No chunking** — afternoon processes whole chapters; afterhours splits into chunks
- **6 draft versions** (v1, v2, v2g, v3-v5) with a grounder pass, style-auditor enforcement pass, and a final-slophunter polish pass
- **Style-guide extraction** — user-invocable style-extractor analyzes prose samples and produces a structured style-guide.json that the style-auditor, style-editor, and slophunter enforce
- **Anti-laziness rules** — all editor/reviewer agents have adversarial anti-laziness enforcement: minimum observation counts, meta-audits on clean results, documented evidence per check

### Artifact Versioning

`v1.md` (writer) → `v2.md` (slophunter, verified by slop-gate) → `v2g.md` (grounder or cp) → `v3.md` (expander or cp) → `v4.md` (style-editor) → `v4b.md` (style-auditor) → `v5.md` (final-slophunter) → `final.md` (cp of v5)

---

## Tuesday Pipeline

**Start script:** `tuesday-start.sh` — same retry-loop pattern as afterhours.

**Working directory:** Chapter outputs go to `omakes/`.

### Agent Flow

```
tuesday-guide (interactive planning) → task-graph.json
    ↓
tuesday-writer (orchestrator) → per chapter:
    tuesday-context-scout → continuity summary
    tuesday-scene-miner → creative palette
    tuesday-blueprint-composer → narrative blueprint
    tuesday-writing-coordinator → per chapter:
        tuesday-prose-writer → draft
        tuesday-ai-prose-gate → binary pass/reject
        tuesday-prose-quality-auditor → deep quality audit
        tuesday-style-auditor → voice/style audit
        (revision loop until pass)
    tuesday-line-editor → final polish
    tuesday-memory-keeper → update ledgers
```

### Agents (12 total)

| Agent | Role |
|---|---|
| `tuesday-guide` | Interactive planning agent. Helps user plan chapter batches, produces `task-graph.json`. |
| `tuesday-writer` | Session orchestrator (pure router). Reads task graph, dispatches per-chapter agents. |
| `tuesday-context-scout` | Reads prior chapters + universe context, produces continuity summary. |
| `tuesday-scene-miner` | Mines scene library + internet for creative palette. 4-lens deep retrieval. |
| `tuesday-blueprint-composer` | Transforms palettes + guide beats into rich narrative blueprints. Multi-path generation. |
| `tuesday-writing-coordinator` | Manages prose-writer → 3-agent audit → revision loop for one chapter. |
| `tuesday-prose-writer` | Writes prose drafts beat-by-beat from blueprints. |
| `tuesday-ai-prose-gate` | Binary pass/reject gate. 3+ AI pattern violations = immediate fail. |
| `tuesday-prose-quality-auditor` | Deep audit: verb vitality, metaphor freshness, paragraph pacing, dialogue mechanics. |
| `tuesday-style-auditor` | Voice audit: voice distinction, tactile specificity, humor, sentence variety, register. |
| `tuesday-line-editor` | Final polish pass with full rewrite authority. Writes to `omakes/`. |
| `tuesday-memory-keeper` | Post-chapter memory updates: arc ledgers, character progression, scene history. |

The tuesday pipeline differs from afterhours in using an explicit 3-agent audit gate (AI gate → quality auditor → style auditor) with a revision loop, rather than afterhours' linear 5-editor pass.

---

## Explicit Book Engine

**Working convention:** per-story `{story_dir}/` roots with runtime state under `{story_dir}/.booksmith/`

### Agent Flow

```text
seed.md -> explicit-book-architect -> approval.json
              ↓
      explicit-book-orchestrator -> chapter-planner -> chapter-writer -> slop-editor -> style-editor -> payoff-keeper -> sequel-bootstrapper -> stop
```

### Agents

| Agent | Role |
|---|---|
| **Architect** | Standalone user-invoked bootstrap surface. Reads `seed.md`, generates cold-start canon plus the book scaffold, and stops at awaiting-approval. |
| **Orchestrator** | Pure router after approval. Reads only `approval.json`, manifest, and worker `status.json` files. Never reads prose or plans. |
| **Chapter Planner** | Chooses the next chapter batch from the approved architect package and live payoff surfaces. Writes `outline.md`. |
| **Chapter Writer** | Writes `v1.md` from the approved outline and canon. Raw prose only. |
| **Slop-Editor** | First editor-lane pass. Cleans AI patterns and writes `v2.md` plus notes. |
| **Style-Editor** | Second editor-lane pass. Polishes voice, POV, continuity, and register into `v3.md`, which the orchestrator copies to `final.md`. |
| **Payoff-Keeper** | Recurring routing surface. Updates live promise/continuity files under `.booksmith/` and decides continue / course-correct / finale / complete. |
| **Sequel-Bootstrapper** | Writes `sequel-seed.md` and `sequel-package.json` from final book artifacts, then stops. |

### Key Characteristics

- **Standalone architect first** — the architect is never orchestrator-dispatched.
- **Approval gate** — downstream work starts only after `approval.json` exists with `"approved": true`.
- **Planner/writer split** — macro structure and prose execution stay separate.
- **Dedicated editor lane** — writer -> slop-editor -> style-editor before payoff keeping.
- **Cold-start canon generation** — Book 1 builds cast/world canon from `seed.md`, not from Ravencrest or other existing story continuity.
- **Per-story runtime state** — live status, manifest, promise ledger, and continuity delta live under `{story_dir}/.booksmith/`.
