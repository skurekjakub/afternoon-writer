---
name: scene-knowledge-base
description: "Browse, select, combine, and write from the scene permutation library in omakes/scenes/. Use this skill whenever planning or writing explicit scenes for any chapter in the Tuesday Universe or Zelda expansion. Also use when the user asks to 'pick scenes', 'plan the sex scenes', 'build the scene arc', 'select from the scene library', or mentions intensity pacing, scene combinations, or scene variety across chapters. Covers scene selection (4–8 per chapter), arrangement into an intensity timeline, transitions between scene types, cast adaptation from generic to named characters, and cross-chapter repetition avoidance."
---

# Scene Knowledge Base

A workflow for selecting, sequencing, and writing explicit scenes using the categorized library in `omakes/scenes/`. The library contains ~15,000+ scene entries across 34 categories organized by phase in the scene arc.

## Library Structure

```
omakes/scenes/
├── 1-buildup/           # Pre-sex: setting, tension, discovery, clothing
├── 2-acts/              # Core sexual acts: oral, penetration, anal, etc.
├── 3-modifiers/         # Flavor layered onto acts: fluids, magic, power, etc.
├── 4-resolution/        # Post-sex: aftercare, emotional landing
└── 5-world/             # Universe-specific: zelda, etc.
```

Each category has:
- `{category}/` — base scene files (one per subcategory)
- `{category}-combos/` — combination scene files pairing with other categories

## Scene Selection Workflow

For a chapter with 8–12 scenes:

1. **Pick 2 from buildup** — setting, anticipation, discovery, clothing
2. **Pick 8–10 from acts + modifiers** — core acts layered with modifiers
3. **Pick 2 from resolution** — aftercare, emotional landing
4. **Include at least 5 combos** — for each selected category, check its `-combos/` sibling directory

### How to browse

1. Read `omakes/scenes/README.md` for the full category table
2. Browse phase directories: `ls omakes/scenes/1-buildup/` etc.
3. Read base files for scene entries: `cat omakes/scenes/2-acts/oral/cunnilingus.md`
4. Check combos: `ls omakes/scenes/2-acts/oral-combos/`

### Selection rules

- Read through 5 categories that suit the chapter
- Read through 10+ subcategory files
- Combine creatively to form the scene arc
- Discard the first or second idea — use the next
- Arrange by intensity: build → peak → resolve
- No two scenes from the same subcategory unless the chapter demands it
- Cross-check against recent chapters to avoid repetition

## Notes

- The library is a starting point, not a constraint. If a chapter needs a scene that doesn't exist, write it.
- Combo files combine multiple categories and serve as peak-scene candidates.
- Entries use "the futa" / "her partner" for generality. Adapt to named characters when writing.
- The library is append-only. New entries are welcome; don't delete existing ones.
