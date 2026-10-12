# Troubleshooting

## First Checks

Look here first:

- `.afternoon/manifest.json`
- `.afternoon/agents/{name}/status.json`
- the current chapter folder under `.afternoon/chapters/`
- `logs/afternoon/`

Remember:

- routing depends on `status.json`, not output-file existence
- loop state lives in `manifest.json`
- gate audit failure is different from operational failure

## Common Problems

| Problem | What usually happened | What to check |
|---|---|---|
| Missing input file | upstream agent failed or wrote the wrong path | upstream `status.json`, expected file path, orchestrator step order |
| Output exists but orchestrator reruns the agent | agent wrote prose but not `status.json` | write or fix the missing status file |
| Chapter is blocked | an agent failed twice | the failing agent's `status.json`, then reset manifest to that chapter/agent |
| Recovery keeps looping | the same failure is still present | manifest `currentAgent`, loop object, and the repeated error |
| Memory facts are wrong | memory-keeper failed or memory is stale | memory-keeper status, affected entity files, prior chapter final prose |
| Slop-gate exhausted | revision loop hit `maxIterations` | latest `slop-gate-notes-r*`, promoted `v2.md`, slop gate config |
| Grounder failed | orchestrator degraded to `v2.md -> v2g.md` | `agents/grounder/status.json` |
| Grounding-gate exhausted | grounding loop hit `maxIterations` | latest grounding-gate notes, promoted `v2g.md`, gate config |

## Reset Patterns

- Fresh run: keep config and outlines, clear generated manifests, statuses, chapter artifacts, and generated plan/memory outputs.
- Single chapter rerun: clear that chapter's generated files and the agent statuses, then point the manifest back at the chapter start.
- Resume from one agent: clear that agent's status plus downstream outputs, then set `currentAgent` to the restart point.

Do not guess from prose files alone. Always verify manifest state and the relevant `status.json` first.