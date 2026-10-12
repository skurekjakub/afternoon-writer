---
name: prose-slop-elimination
description: "Systematic anti-slop workflow for fiction prose in this repo. Use whenever writing, slop-editing, expanding, style-editing, or final-auditing prose that risks sounding AI-generated, over-explained, clinical, repetitive, or emotionally flat. Also use when the user says 'remove the AI slop', 'clean this up', 'fix the prose', 'sounds robotic', 'too many filters/hedges', 'too repetitive', 'cut the filler', or points at references/slop-hitlist.md or references/ai-quirks/."
---

# Prose Slop Elimination

This skill turns the raw anti-slop corpus under `references/` into an ordered pass system. The source files stay where they are; this skill tells you which subset to load, in what order, and what kind of failure each pass is meant to catch.

| Phase | Reference file | Summary |
|---|---|---|
| 1. Scope the pass | `references/1-scope-and-source-map.md` | Pick the current job (writer, slop editor, expander, style editor, final audit) and load only the relevant source files. |
| 2. Run the micro pass | `references/2-micro-pass.md` | Hunt sentence-level and paragraph-level tics: filler actions, hedging, filters, opener monotony, white-room drift, and rhythm problems. |
| 3. Run the macro pass | `references/3-macro-pass.md` | Check scene-wide emotional architecture, tonal range, thought/action balance, conflict friction, and metaphor integrity. |
| 4. Verify the prose | `references/4-verification.md` | Re-read against the hard caps, run targeted searches, and exit only when the draft is clean enough to ship. |

## How to use

1. Start at Phase 1 and choose the pass profile that matches the task.
2. Read the source files that profile requires.
3. Run the micro pass before the macro pass unless you are doing a scene-level-only audit.
4. End with the verification phase so the fixes do not reintroduce other failures.
