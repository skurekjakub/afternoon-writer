# Afternoon Writer — Workspace Rules

Afternoon is an autonomous multi-agent fiction-writing pipeline that converts chapter outlines into verified plans, drafted prose, audited revisions, grounded chapters, and a structured canon memory ledger.

## Dual Harness Layout

This repository supports two agent harnesses side by side:

- **Claude Code**: `.claude/agents/afternoon-*.md` and `.claude/skills/`
- **Antigravity CLI (`agy`, Gemini models)**: `.agents/agents/afternoon-*.md` with shared skill discovery via `.agents/skills.json` pointing to `.claude/skills`

Do not duplicate skills into `.agents/skills/`; edit skills in `.claude/skills/` and keep `.claude/agents/` intact when modifying `.agents/`.

## Pipeline Invariants

1. **Prose-blind orchestrator**: `afternoon-orchestrator` is a pure router. It reads only `.afternoon/config.json`, `.afternoon/manifest.json`, and `.afternoon/agents/{name}/status.json`. It never reads prose, plans, memory, or audit notes.
2. **`status.json` routing**: Every pipeline worker writes `.afternoon/agents/{name}/status.json`. Routing decisions use `status.json`, never output file existence.
3. **Canonical draft chain**:
   `v0.md -> v0c.md -> v1.md -> v2.md -> v2g.md -> v3.md -> v5.md -> final.md`
   (`v3.md` is currently copied from `v2g.md`; `afternoon-writer-expander` is retained on disk but not dispatched.)
4. **One outline beat = one plan beat**: `afternoon-planner` and `afternoon-plan-verifier` must never merge outline beats.
5. **Audit-only gates**: `afternoon-writer-craft-auditor`, `afternoon-writer-continuity-gate`, `afternoon-slop-gate`, and `afternoon-grounding-gate` emit findings and verdicts only — they never edit prose files.
6. **Tool CLI contract**: Any `python3 tools/...` command documented in agent prompts must match flags accepted by `tools/` (verified by `python3 -m unittest tools/tests/test_docs_contract.py`).

## Running on Gemini (Antigravity CLI)

- **Autonomous full run** (with `--dangerously-skip-permissions`, JSON schema enforcement/validation via `.agents/schemas/orchestrator-result.schema.json`, and crash-recovery restart loop):
  ```bash
  ./afternoon-start-gemini.sh
  ```
  Optional env vars: `AFTERNOON_EFFORT` (default `high`), `AFTERNOON_SKIP_PERMISSIONS` (default `true`), `AFTERNOON_MODE` (optional `--mode` override), `AFTERNOON_MODEL` (optional slug from `agy models`).
- **Interactive orchestrator**:
  ```bash
  agy --agent afternoon-orchestrator
  ```
- **User-invocable prep agents**:
  - `agy --agent afternoon-outline-builder` — build chapter outlines in `.afternoon/outlines/`
  - `agy --agent afternoon-style-extractor` — build `.afternoon/style-guide.json` from prose samples
