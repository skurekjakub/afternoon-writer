# Memory Overview

The continuity system is simple:

1. `plan-verifier` reads memory and annotates beats.
2. prose agents read only the memory files the plan names.
3. auditors catch re-introduction or contradiction.
4. `memory-keeper` writes the new canon after the chapter finishes.

## Key Fields

| Field | Meaning |
|---|---|
| `continuityStatus: "new"` | first appearance on the page |
| `continuityStatus: "callback"` | already established; treat lightly |
| `continuityStatus: "evolution"` | established thing, new turn |
| `memoryRef` | exact memory entity and fields a beat depends on |
| `requiredMemory` | top-level list of memory entities the prose agents should load |

## Who Reads What

- `plan-verifier`: broad read of indexes plus entity files as needed; writes `continuityStatus`, `memoryRef`, and `requiredMemory`.
- `writer` and other targeted prose fixers: read only `requiredMemory`.
- `continuity-gate`: audits prose against plan, memory, and prior canon.
- `memory-keeper`: writes the next state of canon from final prose.
- `planner`: does not use the memory system for continuity annotation.

## Writing Guidance

- `new`: introduce with full enough detail to land.
- `callback`: use shorthand, one anchoring detail, or casual reference.
- `evolution`: briefly ground the old fact, then show what changed.

## Files

Memory lives under `.afternoon/plans/memory/`:

- `characters/`
- `locations/`
- `relationships/`
- `threads/`
- `world/`

Each category has `_index.json` for discovery and per-entity `.json + .md` files.

- `.json` is the agent-facing source of truth.
- `.md` is the human-readable bible entry.

## Merge Rules

- Append arrays.
- Replace singular current-state fields and move the old value into history if needed.
- Leave untouched entities untouched.
- If prose and plan disagree, memory follows the prose that actually made it onto the page.