---
name: prose-grounding-audit
description: "Audit packet for grounded prose. Use the references in references/ to judge whether grounding is embodied, distributed, sourced, and not overdone."
---

# Prose Grounding Audit

This skill is for verifiers, especially the grounding-gate. It is not a writing skill. It is the audit surface for judging grounded prose.

## Read order

1. Read `references/failure-taxonomy.md` on every run.
2. If the chapter is dialogue-heavy, read `references/dialogue-grounding.md`.
3. Read `references/distribution-and-tail-audit.md` before final verdict.
4. Use `references/benchmark-deltas.md` only to calibrate whether the pass is too thin, too bloated, or too front-loaded.

## What the files are for

- `failure-taxonomy.md` - shared dimensions, failure classes, and severity shorthand
- `dialogue-grounding.md` - how to judge whether dialogue is embodied
- `distribution-and-tail-audit.md` - how to catch front-loaded grounding and generic endings
- `benchmark-deltas.md` - restraint vs richness lessons from the benchmark chapters

## Core rule

Sweep the prose fresh. Do not trust the grounder's map, notes, or claims about what it fixed.
