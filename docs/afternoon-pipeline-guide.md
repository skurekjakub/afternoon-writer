# Afternoon Fiction Pipeline — User Guide

How to set up, configure, run, and troubleshoot the afternoon fiction pipeline.

**Updated:** 2025-07-14

---

## Table of Contents

1. [What This Pipeline Does](#what-this-pipeline-does)
2. [Prerequisites](#prerequisites)
3. [Setting Up a New Story](#setting-up-a-new-story)
4. [Writing the Story Overview](#writing-the-story-overview)
5. [Creating Chapter Outlines](#creating-chapter-outlines)
6. [Configuring the Pipeline](#configuring-the-pipeline)
7. [Running the Pipeline](#running-the-pipeline)
8. [Monitoring Progress](#monitoring-progress)
9. [Reading the Output](#reading-the-output)
10. [Common Workflows](#common-workflows)
11. [Troubleshooting](#troubleshooting)

---

## What This Pipeline Does

You give it beat outlines. It gives you polished fiction chapters.

The pipeline runs up to twelve AI agents in sequence. The first two validate and enrich your outline with research and continuity annotations. The third writes a raw first draft. The next agents edit and verify that draft — hunting AI patterns, verifying the slop hunt was thorough, grounding the prose in world-specific detail, expanding intimate scenes, polishing voice, and enforcing your style guide. The last agent catalogues everything that happened so future chapters stay consistent.

You don't interact with the pipeline while it runs. You set it up, start it, and come back to finished chapters.

## Prerequisites

- **Copilot CLI** with agent support (`copilot` command available)
- **Claude Opus 4.6** access (all agents use this model)
- A story idea with at least one chapter outlined

## Setting Up a New Story

### Step 1: Create the working directory

```bash
mkdir -p .afternoon/outlines
```

### Step 2: Write the story overview

Create `.afternoon/overview.md` with your story's arc, characters, themes, and destination. The pipeline won't start without this file. See [Writing the Story Overview](#writing-the-story-overview) for what to include.

### Step 3: Create chapter outlines

Write beat plans in `.afternoon/outlines/chapter-1.md`, `chapter-2.md`, etc. You can write these by hand or use the **outline-builder** agent interactively. The recommended shape is the normalized structured chapter beatplan schema: chapter header, `Meta info`, open-state knowledge ledger, chapter-exit knowledge summary, `## Arc position` with chapter-operational arc fields, cast/handoff rules, scene blocks, and chapter close / handoff, with `Disclosure provenance` added on any beat where the source of a reveal matters.

### Step 4: Set up the style target

Pick a piece of published fiction (or your own prior work) that matches the tone you want. Save it or reference its path. This becomes `priming.styleTarget` in your config.

### Step 5: Create character voice sheets

Create a directory with one file per major character, describing their vocabulary, cadence, verbal tics, what they notice, what they avoid saying. Reference this directory as `characters.voiceSheets` in config.

### Step 6: Write the config

Create `.afternoon/config.json`. See [Configuring the Pipeline](#configuring-the-pipeline) for the full schema.

### Step 7: Run

```bash
./afternoon-start.sh
```

## Writing the Story Overview

The story overview is the single most important document you write for the pipeline. Every content-producing agent reads it before doing its job. A vague overview produces vague prose.

### What to include

**Premise** — One paragraph. The situation, not the plot. Who are these people, what do they want, what's in the way?

**Characters** — For each POV and major supporting character:
- Name and role in the story
- What they pursue and what they fear
- Their core misbelief → the growth truth the story pressures toward
- Key relationships and how those shift

**Arc Shape** — The emotional trajectory of the whole story. Not chapter-by-chapter, but the broad strokes. What's the engine? Where does it turn? Where does it land?

**Threads** — Ongoing subplots, mysteries, recurring motifs. For each: what it is, when it surfaces, how it resolves.

**Themes** — What the story asks, not what it answers. Questions, not thesis statements.

**World Notes** — Setting details that persist across chapters. Geography, magic, politics, cultural norms.

**Tone and Register** — What should this feel like to read? Name published works that hit the target.

### What NOT to include
- Chapter-by-chapter synopses (that's what outlines are for)
- Prose samples (that's what the style target is for)
- Character dialogue examples (that's what voice sheets are for)

The overview tells agents WHERE THE STORY IS GOING and holds the stable character canon. The outlines tell them WHAT HAPPENS IN THIS CHAPTER and operationalize that canon into chapter pressure, tests, and shifts. The style target tells them HOW TO WRITE IT. Keep these concerns separate.

## Creating Chapter Outlines

### By hand

Create `.afternoon/outlines/chapter-1.md` in the normalized planner-facing schema:

```markdown
# Chapter 1: [Title]

**POV:** [character] (limited third, absolute)
**Timeline position:** [where this chapter sits]
**Open location:** [specific place]
**Transport:** [how the cast is moving]
**Active cast at open:** [named list]
**Immediate objective:** [what the POV is trying to do right now]

## Meta info

- **Worldbuilding references:** [Doc](path/to/doc.md)
- **Character references:** [Profile](path/to/profile.md), [Voice sheet](path/to/voice.md)

**What [POV] knows at open**
- ...

**What [POV] does NOT know at open**
- ...

**Must not be implied yet**
- ...

**What the cast knows leaving the chapter**
- ...

## Arc position

### [POV]
- **Current stance at open:** ...
- **Surface objective:** ...
- **Pressure source:** ...
- **Misbelief manifestation:** ...
- **Chapter test:** ...
- **Forced choice:** ...
- **End-state shift:** ...
- **Carry-forward residue:** ...

### [Key character] through [POV]'s POV
- **Visible function:** ...
- **POV misread at open:** ...
- **Correction earned here:** ...

## Scene 1: [Name]

**Scene function:** [why this scene exists]
**Cast in scene:** [who is present]
**Knowledge at scene start:** [what the cast know entering it]
**Arc pressure:** [optional - only if this scene carries the chapter's main stance test]

### Beat 1 — Scene: [brief label]
- **Goal:** ...
- **Conflict:** ...
- **Outcome:** **yes-but** — ...
- **Value shift:** trust -> doubt
- **New on-page information:**
  - ...
- **Still unknown after beat:**
  - ...
- **Sensory anchors:**
  - ...
- **Transition intent:** ...

### Beat 2 — Sequel: [brief label]
- **Emotion:** ...
- **Dilemma:** ...
- **Decision:** ...
- **Value shift:** doubt -> resolve
- **New on-page information:**
  - ...
- **Still unknown after beat:**
  - ...
- **Sensory anchors:**
  - ...
- **Transition intent:** ...
```

Story-level character canon lives in the overview. The chapter outline's `## Arc position` translates that canon into the operational pressures for this specific chapter. Scene beats follow **Goal → Conflict → Disaster/Outcome**. Sequel beats follow **Emotion → Dilemma → Decision**. Alternating between them creates natural narrative rhythm.

### Using the outline-builder

The outline-builder is an interactive agent that helps you create outlines through conversation:

```
Ask the outline-builder: "Help me outline chapter 3 of the-cetra-road"
```

It will:
1. Read your story overview, materials, and existing memory
2. Research genre conventions via web search
3. Enter an elicitation loop (up to 5 rounds) asking you about chapter stance, pressure, forced choices, conflicts, and beats
4. Build the outline in the normalized structured chapter beatplan schema and write it to `.afternoon/outlines/`

For maintainers: the schema source of truth lives in `.github/skills/structured-chapter-beatplan-workflow/`.

## Configuring the Pipeline

### Minimal config

```json
{
  "project": "my-story",
  "pov": "limited-third",
  "storyOverview": ".afternoon/overview.md",
  "characters": {
    "voiceSheets": "path/to/voices/"
  },
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
    "styleTarget": "path/to/style-target.md"
  },
  "completionMarker": "===AFTERNOON DONE==="
}
```

### Optional fields

**`materials`** — Array of additional reference file paths. Character indexes, world documents, supplementary voice files.

**`agents.expander.enabled`** — Set to `false` to skip the scene expansion step. The pipeline copies v2g.md to v3.md and proceeds directly to the style-editor. Use this for stories that don't need intimate scene expansion.

**`agents.grounder.enabled`** — Set to `false` to skip the world-specificity grounding step. The pipeline copies v2.md to v2g.md and proceeds to the expander. Use this for stories that already have highly specific prose from the writer.

**`agents.slopGate.enabled`** — Set to `false` to skip the slop verification gate. The slophunter's v2.md passes unchecked to the grounder (or expander if grounder is also disabled, or style-editor if both are disabled). Default `true`.

**`agents.slopGate.maxIterations`** — Maximum number of slophunter revision → gate re-audit cycles before the pipeline halts. Default `5`. Increase if your resource guides are strict and the slophunter needs more passes.

### Choosing a style target

The style target is a piece of prose the agents try to match in register, rhythm, sentence length, dialogue tag density, and paragraph shape. Pick something that sounds like what you want your story to sound like.

Good style targets are 3,000-10,000 words — long enough to establish a pattern, short enough to fit in context.

For full config documentation, see the [config reference](../.github/skills/afternoon-pipeline/references/config.md).

## Running the Pipeline

### Start

```bash
./afternoon-start.sh
```

The start script:
1. Verifies `.afternoon/config.json` exists
2. Verifies outlines exist in `.afternoon/outlines/`
3. Creates `logs/afternoon/` for output logs
4. Dispatches the orchestrator
5. Watches for the completion marker
6. Retries up to 3 times on failure

### What happens during a run

For each chapter (in filename order):
1. **Planner** validates beats and enriches with web research → `{chapterId}-initial.json`
2. **Plan-Verifier** annotates continuity and writes transitions → `{chapterId}.json`
3. **Writer** writes the chapter → `v1.md`
4. **Slophunter** eliminates AI patterns → `v2.md`
5. **Slop-Gate** audits v2.md against all resource guides, writes suggested fixes per KILL (if enabled) → pass/fail; on fail, slophunter applies gate's suggestions and gate re-audits (up to 5 iterations)
6. **Grounder** adds world-specific detail — named geography, factions, mechanics, materials, cultural voice (if enabled) → `v2g.md`
7. **Expander** expands scenes (if enabled) → `v3.md`
8. **Style-Editor** polishes voice and continuity → `v4.md`
9. **Style-Auditor** enforces the style guide (if `style-guide.json` exists) → `v4b.md`
10. **Final-Slophunter** runs a polish-mode slop pass → `v5.md`
11. Orchestrator copies `v5.md` → `final.md`
12. **Memory-Keeper** catalogues everything for future chapters

Then the next chapter begins, with access to all memory from prior chapters.

### Expected time and cost

- **Time:** 15-30 minutes per chapter, depending on length and complexity
- **Tokens:** ~500K-1M tokens per chapter across all agents
- **Disk:** ~100KB of artifacts per chapter

## Monitoring Progress

While the pipeline runs:

### Which chapter and agent is active?

```bash
cat .afternoon/manifest.json | python3 -c "
import json, sys
m = json.load(sys.stdin)
p = m.get('progress', {})
print(f\"{m.get('currentChapter','?')} / {m.get('currentAgent','?')} — {p.get('chaptersCompleted',0)}/{p.get('chaptersTotal','?')} done\")
"
```

### Latest output files

```bash
ls -lt .afternoon/chapters/*/v*.md 2>/dev/null | head -10
```

### Agent completion status

```bash
for f in .afternoon/agents/*/status.json; do
  agent=$(echo "$f" | cut -d/ -f3)
  status=$(python3 -c "import json; print(json.load(open('$f'))['status'])" 2>/dev/null || echo "no-status")
  echo "$agent: $status"
done
```

### Logs

```bash
tail -50 logs/afternoon/*.log 2>/dev/null
```

## Reading the Output

### Final chapters

```
.afternoon/chapters/chapter-1/final.md   # The finished chapter
.afternoon/chapters/chapter-2/final.md
```

### Draft progression

To see how the prose evolved through the pipeline, read the versions in order:
- `v1.md` — Raw writer output (longest, most AI-patterned)
- `v2.md` — After slophunter (shorter, cleaner)
- `v2g.md` — After grounder (immersive world-enrichment: named geography, material texture, institutional specificity, world-register dialogue)
- `v3.md` — After expander (longer again if expansion ran)
- `v4.md` — After style-editor (voice polish)
- `v4b.md` — After style-auditor (style-guide enforcement; absent if no style-guide.json)
- `v5.md` — After final-slophunter (polish-mode slop pass)

### Editor notes

Each editor's notes JSON shows what they found and fixed:
- `slophunter-notes.json` — Before/after word counts, hitlist violations found, flagged scenes
- `slop-gate-notes.json` — KILL findings only with `suggestedFix` per KILL (absent if gate disabled). `slop-gate-scratchpad.md` — all KEEP decisions with reasoning for human post-hoc audit (absent if gate disabled)
- `grounder-notes.json` — Per-scene enrichment log, wordcount growth (absent if grounder disabled)
- `expander-notes.json` — Which beats were expanded, at what level, what was added
- `style-notes.json` — Results of 7 quality checks, fixes applied
- `style-auditor-notes.json` — Per-dimension audit against style-guide.json (absent if no style-guide)
- `final-slophunter-notes.json` — Polish-mode before/after counts

## Common Workflows

### Add a chapter to an existing story

1. Write the outline in `.afternoon/outlines/chapter-N.md`
2. Make sure the story overview still covers this chapter's arc position
3. Run the pipeline — it detects unprocessed outlines automatically

### Re-run a single chapter

1. Delete the chapter's directory: `rm -rf .afternoon/chapters/chapter-N/`
2. Delete the chapter's agent status files: `rm -f .afternoon/agents/*/status.json` (or just the ones for this chapter)
3. Reset `manifest.json`: set `"status": "in-progress"`, remove this chapter from completed lists
4. Run the pipeline

### Disable the expander

Set `agents.expander.enabled` to `false` in config.json. The orchestrator will `cp v2g.md v3.md` and skip the expander dispatch entirely.

### Disable the grounder

Set `agents.grounder.enabled` to `false` in config.json. The orchestrator will `cp v2.md v2g.md` and skip the grounder dispatch entirely.

### Change the style target mid-story

Update `priming.styleTarget` in config.json. The new target applies to all chapters processed after the change. Already-completed chapters are not re-processed.

### Run only specific chapters

Move outlines you don't want processed out of `.afternoon/outlines/` temporarily. The orchestrator processes whatever outlines are present.

### Fresh start

```bash
rm -rf .afternoon/manifest.json .afternoon/plans/ .afternoon/chapters/ .afternoon/agents/
```

This preserves your config, overview, and outlines but clears all pipeline output. Run the pipeline from scratch.

## Troubleshooting

### Pipeline won't start — "FATAL: Story overview missing"

The orchestrator requires `config.storyOverview` to point to an existing file. Check:
1. The `storyOverview` field exists in config.json
2. The referenced file exists on disk
3. The path is relative to the repository root

### Pipeline won't start — "No outlines found"

The start script checks for `.afternoon/outlines/chapter-*.md` files. Make sure:
1. The outlines directory exists
2. Files follow the `chapter-*.md` naming pattern
3. Files aren't empty

### Chapter marked "blocked"

A chapter gets blocked after two consecutive agent failures. Check:
1. The failing agent's status.json for error details
2. Logs for the specific error
3. Whether input files for that agent exist and are valid

To retry: delete the blocking agent's status.json and the chapter's directory, reset the manifest, and run again.

### Slop-gate halted the pipeline

The gate couldn't get the slophunter's output clean within the max iteration limit. Check:
1. Read the last `slop-gate-notes-r{N}.json` to see remaining violations
2. Either fix the prose manually, increase `maxIterations`, or disable the gate temporarily

### Slophunter reporting high violation counts

This is normal for the first few runs with a new style target. The writer calibrates to the target over time. If counts stay persistently high, your style target may contain patterns that conflict with the slop hitlist — check for overlap.

### Memory-keeper errors on chapter 2+

Usually a merge conflict — the memory-keeper found an entity file that doesn't match expected schema. Check:
1. The `_index.json` files in each memory category
2. Individual entity files for malformed JSON
3. Whether entity slugs match between index and files

### Orchestrator stuck in crash recovery loop

The manifest shows `"status": "in-progress"` but the agent it's trying to resume keeps failing. Reset:
1. Check which agent is failing and why
2. Fix the underlying issue (missing files, invalid JSON)
3. Delete the failing agent's status.json
4. Run again — crash recovery will re-dispatch that agent

For comprehensive troubleshooting, see the [troubleshooting reference](../.github/skills/afternoon-pipeline/references/troubleshooting.md).
