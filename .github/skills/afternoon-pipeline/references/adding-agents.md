# Adding An Agent

## Checklist

1. Create `.github/agents/afternoon-{name}.agent.md`.
2. Give it a clear startup read list, a small ordered pass list, explicit outputs, and a `status.json` contract.
3. Add `.afternoon/agents/{name}/` for its status file.
4. Insert it into `.github/agents/afternoon-orchestrator.agent.md` in the right place.
5. Update the short docs: `SKILL.md`, `references/agents.md`, and `references/architecture.md`.

## Minimum Agent Contract

Your agent file should answer these points fast:

- What dispatch prompt it expects
- What it reads
- What it writes
- Whether it edits prose or only audits
- What success and failure `status.json` look like

## Wiring Rules

- Make sure the new agent's inputs exist before it runs.
- Make sure downstream agents read its output if they need it.
- Use the established memory access pattern: broad read for continuity/planning agents, targeted `requiredMemory` reads for prose agents.
- The orchestrator only cares about `status.json`; do not invent alternate completion signals.

## Common Insertion Points

| Position | Typical use |
|---|---|
| after `plan-verifier` | extra plan processing |
| after `slophunter` / slop-gate | prose transformation before grounding |
| after `grounder` | extra grounding helper |
| after `grounding-gate` | QA gate before final polish |
| after `final-slophunter` | post-edit metrics or checks |
| after `memory-keeper` | reporting only |