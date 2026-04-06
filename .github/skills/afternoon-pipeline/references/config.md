# Config Schema

The pipeline is configured via `.afternoon/config.json`. All agents read this file at startup.

## Current Fields

```json
{
  "project": "the-plague-road",
  "storyOverview": ".afternoon/overview.md",
  "styleTarget": "stories/dramione/dramione-1-original.md",
  "pov": "limited-third",
  "characters": {
    "voiceSheets": "stories/the-plague-road/characters/"
  },
  "materials": [
    "external-resources/character-voice-sheets.md"
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
  "completionMarker": "===AFTERNOON DONE==="
}
```

## Field Reference

### `project`
**Type:** string
**Used by:** Status messages, log output
**Purpose:** Human-readable project name. Not consumed by any agent for routing — identification only.

### `styleTarget`
**Type:** file path (string)
**Used by:** No agent reads this field directly — all agents use `priming.styleTarget` instead. This top-level field exists as a human-readable label. If you change the style target, update `priming.styleTarget` (that's the one agents actually read).
**Purpose:** Legacy convenience field. The authoritative path is `priming.styleTarget`.

### `pov`
**Type:** string (currently only `"limited-third"`)
**Used by:** All prose agents
**Purpose:** Narrator mode. Every agent enforces Limited Third Absolute based on this.

### `storyOverview`
**Type:** file path (string) — **MANDATORY**
**Used by:** Orchestrator (bootstrap gate), Planner, Plan-Verifier, Outline-Builder, Writer, Slophunter, Style-Editor
**Purpose:** Path to the story overview document (e.g., `".afternoon/overview.md"`). This is the story bible — a markdown file summarizing the entire story arc: what the journey is, where it starts, where it ends, who the characters are becoming, what threads run through all chapters, and what the thematic core is. Every planning and writing agent reads this at startup to understand where each chapter fits in the overall arc.

The orchestrator checks this field at bootstrap. If the field is missing from config.json, empty, or the file doesn't exist, the pipeline exits immediately with an error message. No chapters are processed without a story overview.

**What to put in the overview:**
- Story premise and setting (1-2 paragraphs)
- Character arcs: The Lie → The Truth for each POV character
- Chapter-by-chapter arc summary (1-2 sentences per chapter: what changes, what thread advances)
- Major threads and where they plant/escalate/resolve
- Thematic throughline
- Tone and genre notes
- Any constraints or rules specific to this story

### `characters.voiceSheets`
**Type:** directory path (string)
**Used by:** Planner, Writer, Style-Editor, Outline-Builder
**Purpose:** Directory containing per-character voice files (e.g., `sylvanas.md`, `jaina.md`). Agents read all `.md` files in this directory.

### `materials`
**Type:** array of file paths (strings)
**Used by:** Planner, Writer, Outline-Builder
**Purpose:** Additional reference materials the planning and writing agents should read — character sheets, world bibles, lore dumps, relationship maps, whatever. Just add file paths and they'll be read during startup.

### `priming.antiSlop`
**Type:** array of file/directory paths
**Used by:** Writer (mandatory first read), Slophunter (full arsenal), Style-Editor (for catching leftovers), Outline-Builder (planning awareness)
**Purpose:** The anti-slop priming recipe. All prose-touching agents read these before starting work. Agents reference this array from config — file paths are not hardcoded in agent prompts.

### `priming.craft`
**Type:** array of file paths
**Used by:** Writer, Outline-Builder
**Purpose:** Craft reference files read after anti-slop. Author technique anchors and intimate scene philosophy. Agents reference this array from config — file paths are not hardcoded in agent prompts.

### `priming.styleTarget`
**Type:** file path (string)
**Used by:** Writer (voice calibration), Style-Editor (voice north star), Plan-Verifier (register understanding), Outline-Builder (voice context), Slophunter (voice matching during rewrites)
**Purpose:** The prose file all agents benchmark against. The writer mimics its rhythms, punctuation, paragraph shapes. The style-editor compares output against it. This is the authoritative style target path — all agents read it from here.

### `priming.proseSamples`
**Type:** array of file paths
**Used by:** Style-Extractor (reads all samples to produce style-guide.json)
**Purpose:** Prose sample files the style-extractor analyzes to produce `.afternoon/style-guide.json`. These are the source material for the structured style specification. Run the style-extractor once per story (or when changing samples) to regenerate the style guide. The `styleTarget` field remains the single-file priming sample for agents that read it directly; `proseSamples` can include multiple files for richer extraction.

### `agents.expander.enabled`
**Type:** boolean (default: `true` if field or section absent)
**Used by:** Orchestrator (dispatch gating), Plan-Verifier (skips expansionLevel annotation)
**Purpose:** When `false`, the orchestrator skips the expander dispatch entirely and copies `v2g.md → v3.md` so the style-editor's input contract is satisfied. The plan-verifier also skips its expansion-depth annotation phase (Phase 2e), since the annotations would go unread. All other agents are unaffected — the style-editor always reads `v3.md` regardless, and `expander-notes.json` consumers already handle its absence.

### `agents.grounder.enabled`
**Type:** boolean (default: `true` if field or section absent)
**Used by:** Orchestrator (dispatch gating)
**Purpose:** When `false`, the orchestrator skips the grounder dispatch entirely and copies `v2.md → v2g.md` so the expander's (or style-editor's, if expander also disabled) input contract is satisfied. When `true`, the orchestrator dispatches the grounder between the slop-gate loop and the expander. On grounder failure after retry, the orchestrator degrades gracefully (`cp v2.md v2g.md`) rather than blocking the chapter.

### `agents.slopGate.enabled`
**Type:** boolean (default: `true` if field or section absent)
**Used by:** Orchestrator (dispatch gating)
**Purpose:** When `false`, the orchestrator skips the slop-gate dispatch entirely. The slophunter's `v2.md` passes through unchecked to the grounder (or expander if grounder disabled, or style-editor if both disabled). When `true`, the orchestrator dispatches the slop-gate after the slophunter and enters a revision loop if the gate fails.

### `agents.slopGate.maxIterations`
**Type:** integer (default: `5` if field absent)
**Used by:** Orchestrator (revision loop termination)
**Purpose:** Maximum number of slophunter revision → slop-gate re-audit cycles before the orchestrator halts the pipeline as `"halted-flagged"`. Each iteration dispatches the slophunter in revision mode to fix gate findings, then re-dispatches the gate for re-audit. If the gate still fails after this many iterations, the chapter is considered unfixable and the pipeline stops.

### `completionMarker`
**Type:** string
**Used by:** Orchestrator (outputs it), start script (watches for it)
**Purpose:** Sentinel string the orchestrator prints when all chapters are done. The start script detects this to know the pipeline completed successfully.

## Adding a New Config Field

1. Add the field to `config.json`
2. Update every agent that should consume it:
   - Add a read step in the agent's Startup Sequence
   - Document what the field controls in the agent's behavior
3. Update this reference file with the new field's documentation
4. If the field changes what an agent reads or writes, verify cross-agent consistency (see `references/agents.md`)

## Changing the Style Target

To switch projects or change the voice benchmark:
1. Update `priming.styleTarget` — this is the path all agents read
2. Optionally update the top-level `styleTarget` for human readability (agents don't read it)
2. Update `characters.voiceSheets` to point at the new project's character files
3. Update `materials` to include any project-specific reference docs
4. Clear or archive existing `.afternoon/plans/memory/` files if switching to a different story
