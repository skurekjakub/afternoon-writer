# Afternoon Fiction Pipeline — Technical Reference

Configuration schemas, artifact formats, agent protocols, and operational details for the afternoon pipeline.

**Updated:** 2025-07-14

---

## Table of Contents

1. [Config Schema](#config-schema)
2. [Story Overview](#story-overview)
3. [Beat Outline Format](#beat-outline-format)
4. [Plan JSON Format](#plan-json-format)
5. [Editor Notes Format](#editor-notes-format)
6. [Status JSON Format](#status-json-format)
7. [Memory File Format](#memory-file-format)
8. [Manifest Format](#manifest-format)
9. [Completion Markers](#completion-markers)
10. [Agent Dispatch Protocol](#agent-dispatch-protocol)
11. [Anti-Slop System](#anti-slop-system)
12. [Priming Recipe](#priming-recipe)

---

## Config Schema

Location: `.afternoon/config.json`

```json
{
  "project": "the-cetra-road",
  "pov": "limited-third",
  "storyOverview": ".afternoon/overview.md",
  "characters": {
    "voiceSheets": "stories/awakening/voices/"
  },
  "materials": [
    "external-resources/character-voice-sheets.md",
    "stories/awakening/00-index.md"
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
    "styleTarget": "stories/dramione/dramione-1-original.md"
  },
  "agents": {
    "expander": {
      "enabled": true
    },
    "grounder": {
      "enabled": true
    },
    "slopGate": {
      "enabled": true,
      "maxIterations": 5
    }
  },
  "completionMarker": "===AFTERNOON DONE==="
}
```

### Field reference

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `project` | Yes | string | Project identifier — used in manifest and logs |
| `pov` | Yes | string | POV mode. Currently always `"limited-third"` |
| `storyOverview` | Yes | string | Path to story overview markdown. Orchestrator exits if missing |
| `characters.voiceSheets` | Yes | string | Directory containing per-character voice files |
| `materials` | No | string[] | Additional reference files (indexes, world docs, voice files) |
| `priming.antiSlop` | Yes | string[] | Slop detection resources — files and directories |
| `priming.craft` | Yes | string[] | Craft technique reference files |
| `priming.styleTarget` | Yes | string | Style target file — register, rhythm, and tag density to match |
| `agents.expander.enabled` | No | boolean | `false` skips expander entirely (`cp v2g.md v3.md`). Default `true` |
| `agents.slopGate.enabled` | No | boolean | `false` skips slop-gate entirely (v2.md passes unchecked to grounder). Default `true` |
| `agents.slopGate.maxIterations` | No | integer | Max slophunter revision → re-audit cycles before halt. Default `5` |
| `agents.grounder.enabled` | No | boolean | `false` skips grounder entirely (`cp v2.md v2g.md`). Default `true` |
| `completionMarker` | Yes | string | String the orchestrator prints when done. Start script watches for this |

All paths are relative to the repository root.

For full config documentation, see the [config reference](../.github/skills/afternoon-pipeline/references/config.md).

## Story Overview

Location: referenced by `config.storyOverview` (typically `.afternoon/overview.md`)

A markdown file describing the full story arc. Not a chapter-by-chapter outline — the big picture. Where the story starts emotionally, where it turns, where it lands.

### Required by
- **Orchestrator** — validates it exists (doesn't read content)
- **Planner** — understands where this chapter fits in the arc
- **Plan-Verifier** — context for continuity decisions
- **Writer** — story-level awareness for prose choices
- **Slophunter** — context for replacement word choices
- **Grounder** — world context for grounding proper nouns and named systems
- **Style-Editor** — arc context for voice/pacing decisions
- **Outline-Builder** — helps user plan chapters that serve the arc

### NOT required by
- **Memory-Keeper** — catalogues what happened, doesn't need forward context
- **Expander** — works on scene-level expansion, not story-level

### Recommended sections
Premise, Characters (arcs + Lie/Truth), Arc Shape, Threads, Themes, World Notes, Tone and Register.

## Beat Outline Format

Location: `.afternoon/outlines/{chapterId}.md`

User-authored markdown. The outline-builder can help create these interactively, or you can write them by hand.

### Structure
The normalized planner-facing markdown schema is:

- Chapter header: POV, timeline position, open location, transport, active cast at open, immediate objective
- `## Meta info`: repo-root-relative worldbuilding and character / voice-sheet links
- Open-state knowledge ledger: what the POV knows at open, does NOT know, and must not imply yet
- Chapter-exit knowledge summary: the key facts the cast has earned by chapter close, written near the top for quick information-flow review
- `## Arc position`: chapter-operational arc fields translating story-level character canon into current stance at open, surface objective, pressure source, misbelief manifestation, chapter test, forced choice, end-state shift, and carry-forward residue
- `## Cast and handoff rules`
- Scene blocks: scene function, cast in scene, knowledge at scene start, with optional `Arc pressure` when a scene carries the chapter's main stance test
- Beat blocks: typed Scene / Sequel beats with value shifts, new info, still unknown, sensory anchors, and transition intent
- Optional source-sensitive reveal field: `Disclosure provenance`, naming who says a fact, whether it is stated or inferred, and whether the chapter only gets a limited namedrop
- `## Chapter close / handoff`

Within each beat, include:

- **Type**: Scene (goal → conflict → outcome) or Sequel (emotion → dilemma → decision)
- **Value shift**: What changes — relationship, knowledge, emotional state (entry → exit)
- **Scene outcome label**: `no-and` (fail + worsen), `yes-but` (succeed + cost), or `yes` (clean success), carried inline on the `Outcome` line
- **Transition intent**: How this beat connects to the next (emotional thread, sensory bridge, action continuity, question pressure, or intentional hard cut)

Sensory anchors live at the **beat level**. Scene-level fields carry `sceneFunction`, `castInScene`, `knowledgeAtSceneStart`, optional `arcPressure`, and `enrichment`. The plan-verifier audits beat-level `transitionIntent` and writes the top-level `chapterBridge` — user-specified hard cuts and thread choices are respected.

Story overviews and character references hold the stable character canon (core misbelief, growth truth, core pursuit, underlying need). Chapter outlines should operationalize that canon inside `## Arc position` rather than repeating abstract labels beat-by-beat.

**Writer freedom principle**: Plans describe intent (what happens, what changes emotionally), not prose (how sentences should read). No pre-written dialogue, no half-written sensory sentences, no prose directives in verifier notes.

For the current schema source of truth, see `.github/skills/structured-chapter-beatplan-workflow/`.

## Plan JSON Format

Location: `.afternoon/plans/{chapterId}.json` (verified plan, read by downstream agents)

The plan JSON uses a chapter scaffold plus scene-level structure with beats nested inside scenes. Key fields:

```json
{
  "chapterId": "chapter-1",
  "pov": "Sylvanas",
  "timelinePosition": "same day as the patrol report",
  "openLocation": "Lordamere border post",
  "transport": "horseback patrol returning to post",
  "activeCastAtOpen": ["Sylvanas", "Lor'themar", "mounted patrol"],
  "immediateObjective": "Return to the post and determine why the runner came south",
  "metaInfo": {
    "worldbuildingReferences": [{ "label": "Lordamere Notes", "path": "stories/the-plague-road/world/lordamere.md" }],
    "characterReferences": [{ "label": "Sylvanas Profile", "path": "stories/the-plague-road/characters/sylvanas.md" }]
  },
  "knowledgeLedger": {
    "povKnowsAtOpen": ["The border has been restless all day."],
    "povDoesNotKnowAtOpen": ["Why the human mage crossed the wards."],
    "mustNotBeImpliedYet": ["The full plague mechanism."],
    "castKnowsLeavingChapter": ["The warning is now inside Quel'Thalas's border problem."]
  },
  "arcPosition": {
    "pov": {
      "currentStanceAtOpen": "This is still somebody else's trouble until it reaches Sylvanas's road.",
      "surfaceObjective": "Finish the patrol and stay clear of politics.",
      "pressureSource": "A human mage crosses the wards with a warning that will not stay outside protocol.",
      "misbeliefManifestation": "Sylvanas hears human mage and thinks paperwork and inconvenience.",
      "chapterTest": "The warning lands inside her own command space instead of safely south of it.",
      "forcedChoice": "Leave the prisoner to protocol, or ride back and put her own eyes on the problem.",
      "endStateShift": "By close this is Sylvanas's problem.",
      "carryForwardResidue": "Chapter 2 opens with Sylvanas unable to dismiss the mage."
    }
  },
  "castAndHandoffRules": {
    "entries": [
      { "character": "Lor'themar", "rule": "Present in scenes 1-2. Exits north after the report lands." }
    ],
    "chapterHandoffTarget": "Chapter 2 opens with Sylvanas, Jaina, and Cyndia on the interrogation beat."
  },
  "scenes": [
    {
      "sceneId": 1,
      "title": "The Border at Night",
      "sceneFunction": "Show Sylvanas in her element before the human problem reaches her own road.",
      "castInScene": ["Sylvanas", "Lor'themar", "mounted patrol"],
      "knowledgeAtSceneStart": ["Ordinary frontier work; nothing stranger than trolls."],
      "arcPressure": "The warning will come from the exact kind of outsider Sylvanas is built to dismiss.",
      "enrichment": {
        "detail": "Lordamere Lake: persistent fog, corrupted shoreline post-Scourge.",
        "source": "WoW wiki"
      },
      "beats": [
        {
          "beatId": 1,
          "beatType": "scene",
          "scenePhase": "goal",
          "goal": "Finish the sweep by killing the last troll raider.",
          "conflict": "The final raider breaks cover with an attack already committed.",
          "outcome": { "type": "yes", "summary": "Sylvanas kills him cleanly." },
          "valueShift": "tension -> satisfaction",
          "newOnPageInformation": ["Sylvanas is at ease only on a live patrol."],
          "stillUnknownAfterBeat": ["Why the runner was sent south."],
          "sensoryAnchors": ["wet bowstring", "trampled fern", "blood on cold leather"],
          "transitionIntent": "action-continuation: victory is cut off by a horse coming hard through the trees",
          "continuityStatus": "new",
          "expansionLevel": "low"
        }
      ]
    }
  ],
  "chapterBridge": null
}
```

Optional beat fields: `dialogueGuidance`, `disclosureProvenance`, and `plantedThread`. The verifier may also add `memoryRef`, `verifierNotes`, and `verifierModification` where needed.

### continuityStatus values
- `"new"` — first appearance. Writer gives full sensory treatment.
- `"callback"` — seen before. Writer uses brief anchoring (single detail, familiarity shorthand).
- `"evolution"` — changing. Writer builds on established foundation, then shows what's different.

## Editor Notes Format

Each editing agent produces a notes JSON alongside its output:

| Agent | Notes file | Key fields |
|-------|-----------|------------|
| Slophunter | `slophunter-notes.json` | counts (before/after/caps), changes[], flags, flaggedForExpander, wordCount |
| Expander | `expander-notes.json` | expansions[], skipped[], metrics |
| Grounder | `grounder-notes.json` | per-scene enrichment log (biggest gap, enrichment applied), wordcount growth |
| Slop-Gate | `slop-gate-notes.json` (or `slop-gate-notes-r{N}.json` on re-audit) | Pipeline artifact: KILL findings only, per-guide audit sections with `suggestedFix` per KILL (cross-checked against all audit guides), `cleanReason` for zero-kill guides, verdict, `killsWithFix`/`killsUnfixable` counts. Separate `slop-gate-scratchpad.md` contains all KEEP decisions for human audit. |
| Style-Editor | `style-notes.json` | checks (1-6 results), fixes[], flags |

All notes files follow the same pattern: log what you found, log what you changed, log before/after metrics. Downstream agents may read upstream notes (style-editor reads slophunter-notes and expander-notes for context).

## Status JSON Format

Location: `.afternoon/agents/{agent-name}/status.json`

```json
{
  "status": "completed",
  "chapterId": "chapter-1",
  "timestamp": "2025-07-14T10:30:00Z"
}
```

Status values: `"completed"`, `"failed"`, `"in-progress"`

The slop-gate adds a `verdict` field to its status.json: `"pass"` or `"fail"`. The orchestrator routes on `verdict`, not `status`. A gate that runs successfully but finds violations writes `status: "completed", verdict: "fail"`.

The orchestrator reads ONLY this file to determine agent completion. It never checks output file existence.

## Memory File Format

Location: `.afternoon/plans/memory/{category}/{slug}.json` + `.md`

Each entity has paired files:
- **JSON** — structured data for agent consumption (plan-verifier, writer, style-editor)
- **MD** — human-readable prose summary for human reviewers and browsing

Categories: `characters/`, `locations/`, `relationships/`, `threads/`, `world/`

Each category has an `_index.json` listing all entities and their chapter history.

For full memory system documentation, see the [memory system reference](../.github/skills/afternoon-pipeline/references/memory-system.md).

## Manifest Format

Location: `.afternoon/manifest.json`

```json
{
  "status": "in-progress",
  "currentChapter": "chapter-2",
  "currentAgent": "writer",
  "progress": {
    "chaptersCompleted": 1,
    "chaptersTotal": 3
  },
  "log": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "chapter": "chapter-1",
      "agent": "planner",
      "status": "completed",
      "artifacts": [".afternoon/plans/chapter-1-initial.json"]
    }
  ]
}
```

The orchestrator owns this file exclusively. No other agent reads or writes it. It enables crash recovery — on restart, the orchestrator reads `currentChapter` and `currentAgent` to resume from the point of failure. During the slop-gate revision loop, the manifest also contains a `slopGateLoop` object tracking `iteration`, `phase`, `feedbackPath`, and `targetFile` for precise loop recovery.

Key fields:
- `status`: "in-progress", "completed", "completed-with-blocks", or "halted-flagged"
- `currentChapter` + `currentAgent`: where the pipeline is (for crash recovery)
- `progress`: chapter completion counts
- `log`: per-dispatch entries with timestamps and artifact references

## Completion Markers

The pipeline uses a completion marker string (from `config.completionMarker`) to signal the start script:

- **Normal completion**: Orchestrator prints the marker after all chapters are processed
- **Fatal error**: Orchestrator prints the marker after a FATAL message (e.g., missing story overview) to prevent infinite retry loops
- **Start script**: Watches stdout for the marker. On detection, stops the pipeline. Retries up to 3 times on non-marker exits.

Default marker: `===AFTERNOON DONE===`

## Agent Dispatch Protocol

Most agents are dispatched with a single prompt: `"chapterId: {chapterId}"`. The slophunter in revision mode receives additional parameters: `"chapterId: {chapterId}, mode: revision, iteration: {N}, feedbackPath: {path}"`. The slop-gate on re-audit receives: `"chapterId: {chapterId}, iteration: {N}, targetFile: v2-r{N}.md"`.

Each agent:
1. Reads config.json to find all file paths
2. Reads its specific inputs (varies by agent)
3. Does its work
4. Writes its output files
5. Writes `agents/{name}/status.json` with `"completed"` or `"failed"`

Agents are stateless between dispatches. They carry no memory from one chapter to the next — all cross-chapter context comes from the memory files on disk.

## Anti-Slop System

The slop detection system has three layers:

### Layer 1: Priming (all prose-touching agents)
Before writing or editing, agents read the full anti-slop priming stack:
- `references/slop-hitlist.md` — 40+ banned patterns with hard rate limits
- `references/ai-quirks/sentence-level/` — 7 sentence-level AI traps
- `references/ai-quirks/paragraph-level/` — 4 paragraph-level AI traps
- `editor-guide.md` — what to cut first

### Layer 2: Targeted hunting (slophunter)
The slophunter executes 10 specific hunts with measurable before/after counts. It produces a notes JSON proving what it found and fixed.

### Layer 2.5: Adversarial verification (slop-gate)
The slop-gate reads the slophunter's output and audits it against every guide in `resources/*.md`. For each KILL finding, it writes a concrete `suggestedFix` — a replacement that has been cross-checked against all audit guides to avoid introducing new violations. On later iterations when the loop oscillates, the gate switches to conservative fix strategy (prefer deletion, minimal substitution). On fail, the slophunter is re-dispatched in revision mode to apply the gate's pre-validated suggestions (with latitude for voice/flow adjustment), then runs a **rewrite self-audit** on changed passages to catch violations introduced by the rewrites themselves. This converging feedback loop replaces improvised rewrites with targeted, pre-checked fixes.

### Layer 3: Leftover sweep (style-editor)
The style-editor's check #6 catches any AI patterns the slophunter missed — attribution over-explanation, parallel structure, emotional telling, scene clichés.

### Hard caps
Certain words have per-chapter maximums (defined in slop-hitlist.md): "as if" (1), "pressed" (2), "nodded" (3), "sighed" (2), "smiled" (3), "glanced" (3), "something" (3). The slophunter enforces these and reports before/after counts.

## Priming Recipe

The writer's proven priming order (all other prose-touching agents follow a similar pattern):

1. Story overview (story arc context)
2. Anti-slop files (shift token distribution away from AI patterns)
3. Craft references (author techniques, scene philosophy)
4. Style target (register, rhythm, tag density to match)
5. Voice sheets (character-specific vocabulary and cadence)
6. Materials (world docs, indexes, supplementary references)
7. Prior chapter (continuity)
8. The verified plan (chapter scaffold, scene purpose, beat pressure, and earned knowledge)
9. Targeted memory (entity details needed for this chapter)

The order matters. Anti-slop priming must happen before the style target to establish the negative space (what NOT to do) before showing the positive model (what TO do). The style target then fills that space with the correct register.
