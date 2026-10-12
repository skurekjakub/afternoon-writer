# Config Overview

Pipeline settings live in `.afternoon/config.json`.

## Fields That Matter

| Field | Purpose | Notes |
|---|---|---|
| `project` | human-readable project name | Labels only. |
| `storyOverview` | path to the story bible | Required. The orchestrator fails fast if it is missing or the file does not exist. |
| `pov` | narrator mode | Currently limited third. |
| `characters.voiceSheets` | directory of per-character voice files | Read by writing/planning agents that need voice context. |
| `materials` | extra project references | Optional. |
| `priming.antiSlop` | slop guides and directories | Shared slop-avoidance inputs. |
| `priming.craft` | craft reference files | Used by writing/planning agents. |
| `priming.styleTarget` | main prose sample path | This is the authoritative style sample path. |
| `priming.proseSamples` | sample set for style extraction | Used by `style-extractor`. |
| `agents.grounder.enabled` | enable or skip grounding | If false, orchestrator copies `v2.md -> v2g.md`. |
| `agents.groundingGate.enabled` | enable grounding audit | Defaults off. |
| `agents.groundingGate.maxIterations` | max grounding revision loops | Best-effort cap. |
| `agents.slopGate.enabled` | enable slop-gate | Defaults on. |
| `agents.slopGate.maxIterations` | max slop revision loops | Best-effort cap. |
| `agents.expander.enabled` | legacy field | Currently ignored; expander is not in the live pipeline. |
| `completionMarker` | end-of-run sentinel | Watched by the start script. |
| top-level `styleTarget` | legacy label | Keep it in sync if you want, but agents read `priming.styleTarget`. |

## Rules

- `storyOverview` is mandatory.
- `priming.styleTarget` is the real style target. The top-level `styleTarget` is legacy.
- Gate iteration limits control retry loops, not chapter blocking. Exhaustion promotes the latest revision and continues.
- If you add a field, update every agent that reads it and update this file in the same session.

## Switching Stories

1. Point `storyOverview`, `characters.voiceSheets`, `materials`, and priming paths at the new story.
2. Update `priming.styleTarget`.
3. Update `priming.proseSamples` if you use the style extractor.
4. Clear or archive old `.afternoon/plans/memory/` data if the story changes.