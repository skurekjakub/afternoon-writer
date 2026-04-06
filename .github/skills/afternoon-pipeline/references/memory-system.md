# Memory & Continuity System

The afternoon pipeline prevents re-introduction of established information through a three-layer system: annotation at plan time, targeted reads at write time, and enforcement at edit time.

## How It Works

### Layer 1: Annotation (Plan-Verifier)

The plan-verifier reads ALL memory files and annotates every beat with:

**`continuityStatus`** — one of three values:
- `"new"` — this information appears for the first time in the story
- `"callback"` — references information already established in a prior chapter
- `"evolution"` — builds on established information in a new direction

**`memoryRef`** — on callback and evolution beats, specifies exactly what memory entity is relevant:

```json
"memoryRef": {
  "file": "characters/sylvanas-windrunner",
  "fields": ["physicalDetails", "abilitiesDemonstrated"],
  "chapter": "chapter-1"
}
```

The `file` is the entity path relative to `.afternoon/plans/memory/` (without extension — consumers append `.json` or `.md` as needed).

**`requiredMemory`** — top-level field on the plan JSON, collects all unique `memoryRef.file` values across all beats. Each entry is a path relative to `.afternoon/plans/memory/`. This is the writer's and style-editor's shopping list — they load `{entry}.json` for structured data.

### Layer 2: Targeted Reads (Writer + Style-Editor)

The writer and style-editor do NOT read all memory files. They read the verified plan first, orient on the chapter scaffold / scenes / beats, then check the `requiredMemory` field and load ONLY the specified `.json` files. The `.md` files are human-readable production bible entries for human reviewers, not for agent consumption. This prevents context pollution with information irrelevant to the current chapter and keeps memory context costs minimal.

### Layer 3: Enforcement (Plan-Verifier + Style-Editor)

The plan-verifier produces every `continuityStatus` annotation — it reads ALL memory files, annotates each beat, and runs validation:
- Beats marked "new" that contain established info → correct to "callback"
- Beats marked "callback" that reference nothing in memory → correct to "new"
- Beats marked "evolution" that just restate without adding → downgrade to "callback"
- Callback density > 60% of chapter → flag as excessive reminding

The style-editor enforces anti-reintroduction in the final prose:
- Character appearance re-introductions → reduce to single-detail anchor or cut
- Ability "revelations" of known abilities → treat as known
- Relationship dynamic resets without justification → flag
- World-building re-exposition → reference casually or cut
- Location full re-descriptions → trim to one or two anchoring details

## What the Writer Does with continuityStatus

### `"new"` beats
Write with full sensory detail. This is the reader's first encounter. Give enough to build a mental image.

### `"callback"` beats
The reader already knows this. Use one of these techniques:
- **Single-detail anchor:** "the frost burns she'd first noticed at the border"
- **Familiarity shorthand:** "the particular way Jaina's magic tasted of ozone"
- **Evolving perception:** "Lor'themar's scar — she'd stopped noticing it years ago"
- **Casual reference:** just name it and move on
- **Drop entirely:** if the callback serves no current-scene purpose

### `"evolution"` beats
Reference the established foundation briefly, then expand into new territory:
- "The frost burns had faded since the border — new ones, fresher, marked her knuckles now"
- "Jaina's barrier magic, which had been desperate improvisation at the pass, moved now with rehearsed precision"

## Memory-Keeper: The Source of Truth

The memory-keeper runs after each chapter and catalogs everything in 5 passes, producing per-entity files (one `.json` + one `.md` per entity) plus lightweight `_index.json` files for discovery. It uses the verified plan as an intent map and the final prose as canon. If the plan and the prose diverge, memory follows what the chapter actually put on the page:

| Pass | Category | What it tracks |
|------|----------|---------------|
| 1 | Characters | appearance, voice markers, beliefs, goals, emotional state, decisions, abilities, name patterns, body language, knowledge, arc (lie/truth/position) |
| 2 | Locations | sensory profile (sight/sound/smell/touch/atmosphere), established facts, characters present, events |
| 3 | Relationships | current state, power dynamic, interactions, physical dynamics, name usage between characters, history, trajectory |
| 4 | Plot threads | status (open/advanced/resolved), relevant characters, evidence, reader knows vs. POV character knows |
| 5 | World & Timeline | world facts by category (geography/politics/military/magic/culture/economy/religion), timeline per chapter |

### Merge rules (chapter 2+)
- Per-entity file: read existing `{slug}.json`, merge new data, write back (overwrite — each file is one entity)
- Arrays: append new entries
- Singular fields (e.g., `emotionalStateAtChapterEnd`): replace, move old value to history
- Threads: update status, append evidence
- Entities NOT in this chapter: leave untouched

## Files

All memory files live in `.afternoon/plans/memory/`, organized by category with one file per entity:

```
plans/memory/
├── characters/
│   ├── _index.json              # Lightweight roster for discovery
│   ├── sylvanas-windrunner.json + .md
│   └── jaina-proudmoore.json + .md
├── locations/
│   ├── _index.json
│   └── millhaven.json + .md
├── relationships/
│   ├── _index.json
│   └── jaina--sylvanas.json + .md
├── threads/
│   ├── _index.json
│   └── plague-samples-border.json + .md
└── world/
    ├── _index.json
    ├── geography.json + .md
    └── timeline.json + .md
```

Each `_index.json` contains a lightweight roster (name, slug, aliases, firstAppearance, lastAppearance) for scanning without loading full profiles. Individual `.json` files contain the full structured profile. Individual `.md` files are human-readable production bible entries.

## Cross-Agent Memory Flow

```
Chapter N completes:
  Memory-Keeper writes → plans/memory/{category}/{entity}.json + .md, {category}/_index.json

Chapter N+1 starts:
  Planner validates structure + enriches via web research (does NOT read memory)
  Plan-Verifier reads _index.json files → loads entity files as needed → annotates beats with continuityStatus + memoryRef, verifies beat-level transitionIntent, writes chapterBridge
  Writer reads ONLY requiredMemory entity files → uses continuityStatus for detail level
  Style-Editor reads ONLY requiredMemory entity files → enforces anti-reintroduction
```
