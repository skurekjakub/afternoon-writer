# Phase 1: Scope the Pass

Start by reading `references/ai-quirks/README.md`. It is the map for the whole corpus and tells you how the repo already expects different agent types to use the files.

Then treat these as the source set behind this skill:

- `references/slop-hitlist.md` — the master hard-cap document
- `references/ai-quirks/sentence-level/01-07`
- `references/ai-quirks/paragraph-level/08-11`
- `references/ai-quirks/scene-level/12-17`

Do **not** load all 17 quirk files by reflex. Pick the profile that matches the job:

| If you are... | Load first | Primary concern |
|---|---|---|
| Slop editor / cleanup pass | `slop-hitlist.md`, sentence-level 01-07, then skim paragraph-level 08-11 | Surgical line cleanup and local rhythm repair |
| Expander | paragraph-level 08-11 first, then scene-level 12-17 near transitions, then sentence-level 01-07 as a back-check | Adding length without adding new quirks |
| Style editor | `slop-hitlist.md` plus all sentence, paragraph, and scene files | Full-spectrum quality control |
| Final editor / macro audit | `slop-hitlist.md`, scene-level 12-17, then a skim of sentence-level 01-07 | Scene architecture, tonal residue, and survivors from earlier passes |

Use the raw files as **evidence libraries**, not as slogans. They are full of bad/good pairs and explanations. Read the ones you need for the current pass, then work with those examples fresh in memory.

Two scoping rules matter:

1. **Micro before macro by default.** A scene full of hedges, filters, and filler gestures cannot be judged cleanly at the emotional-architecture level yet.
2. **Macro only works on whole scenes.** If you only have a paragraph or a short excerpt, stay in the sentence/paragraph layers unless the user specifically wants a scene diagnosis.

## Before moving to Phase 2

You should have:

- chosen the current pass profile
- loaded the relevant source files from `references/`
- named the main failure modes you expect to hunt in this draft
