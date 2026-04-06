# Phase 3: Build Scenes and Beats

This phase turns the chapter scaffold into scene blocks and typed beat flow.

## Scene block shape

For each scene, use:

```markdown
---

## Scene {N}: {Name}

**Scene function:** {why this scene exists}
**Cast in scene:** {who is physically present}
**Knowledge at scene start:** {what the POV / cast know entering it}
```

The `Scene function` is mandatory. If you cannot say what the scene does, the scene is probably filler.

Optional scene-level field:

- `**Arc pressure:** ...` when this scene carries the chapter's main stance test, forced choice, or load-bearing recalibration

## Beat block shape

Each beat should use this heading pattern:

```markdown
### Beat {N} — Scene: {Title}
```

or

```markdown
### Beat {N} — Sequel: {Title}
```

Then use the matching field set.

### Scene beat

```markdown
- **Goal:** ...
- **Conflict:** ...
- **Outcome:** **no-and** / **yes-but** / **yes** — ...
- **Value shift:** {from} -> {to}
- **New on-page information:**
  - ...
- **Still unknown after beat:**
  - ...
- **Sensory anchors:**
  - ...
- **Transition intent:** ...
```

### Sequel beat

```markdown
- **Emotion:** ...
- **Dilemma:** ...
- **Decision:** ...
- **Value shift:** {from} -> {to}
- **New on-page information:**
  - ...
- **Still unknown after beat:**
  - ...
- **Sensory anchors:**
  - ...
- **Transition intent:** ...
```

Optional fields are allowed when a beat needs them:

- `**Dialogue guidance:** ...`
- `**Disclosure provenance:** ...`
- `**Planted thread:** ...`

Use them only when they are load-bearing.

## Rules for scene and beat construction

### 1. Every beat changes something

No filler travel notes. No placeholder confrontation. Every beat must shift:

- knowledge
- relationship
- emotional footing
- tactical position
- or physical situation

If removing the beat changes nothing, the beat is dead.

### 2. Information order is sacred

`New on-page information` is the list of facts earned inside that beat.

`Still unknown after beat` protects what the chapter has not yet earned.

Never state a later conclusion earlier in the chapter just because the planner knows where things are going.

When a beat introduces source-sensitive knowledge, add `**Disclosure provenance:** ...`.

Use it when:

- a specific character is the first on-page source for the fact
- the knowledge is pieced together from fragments rather than cleanly confessed
- the reveal is only allowed as a namedrop, crumb, or partial frame rather than a full explanation

The field should state:

- who says it or carries it
- whether the fact is direct statement, stitched inference, or limited namedrop
- any cap on how fully the chapter may explain it

Examples:

- Kel'Thuzad is the first on-page source for the Lich King here; Jaina does not already know the term from Dalaran.
- The Burning Legion enters as Kel'Thuzad's brief top-of-chain namedrop, not a full cosmology lecture.
- Kel'Thuzad's name is stitched from Corin, Havel, and the captive's broken clue, not delivered in one clean confession.

### 3. Scene/Sequel typing matters

Use Swain logic:

- Scene = goal -> conflict -> outcome
- Sequel = emotion -> dilemma -> decision

The chapter does not need rigid 1:1 alternation, but it does need breathing rhythm. A string of action beats with no processing becomes noise. A string of processing beats with no external pressure stalls.

### 4. Value shifts must vary

Do not let three consecutive beats shift in the same emotional direction. Oscillation creates shape.

### 5. Outcomes must escalate

Use mostly:

- `no-and`
- `yes-but`

Reserve clean `yes` outcomes for moments that have actually earned relief.

Put the try-fail label directly on the `Outcome` line:

- `**Outcome:** **no-and** — ...`
- `**Outcome:** **yes-but** — ...`
- `**Outcome:** **yes** — ...`

### 6. Sensory anchors are scene-grounding, not prose-writing

Give tactile, visual, olfactory, or acoustic anchors that tell the writer what makes the space real.

Do not write lyrical filler. Write usable hooks:

- ward-hum cutting off behind them
- cold chimneys
- horses sidestepping the smell

### 7. Beats must be writer-actionable

Good beat note:

- the challenge is getting Sylvanas to admit Jaina's competence without naming it

Bad beat note:

- Sylvanas starts to respect Jaina

The first gives something to show. The second is a diagnosis.

### 8. Chapter arc lives above the beat level

The core story-level arc material belongs in the story overview and `## Arc position`, not in every beat.

Beat notes should show the local pressure, choice, or consequence. If a scene is where the chapter's stance gets tested, either encode it in `Scene function` or use the optional scene-level `Arc pressure` field.

Do not paste abstract character-arc labels into every beat. Operationalize them.

## When to use dialogue guidance

Add a `Dialogue guidance` field when:

- a character's register shift is itself the beat
- a voice collision matters structurally
- the writer needs to know what kind of verbal texture belongs here

Example uses:

- Jaina starts translated-down, then slips into full mage register
- Kel'Thuzad leaves the last inference open and waits to see if Jaina completes it

## Before moving to Phase 4

You should have:

- Every scene block written with function, cast, and knowledge at start
- Every beat written in typed Scene/Sequel form
- Value shifts, new info, still-unknown items, sensory anchors, and transition intent for every beat
- Any load-bearing scene-level arc pressure encoded where it matters
- Any source-sensitive revelations encoded with `Disclosure provenance`
- Any load-bearing voice or dialogue guidance encoded where it matters
