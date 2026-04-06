# Grounder Prompt Redesign Spec

## Intent

Redesign the grounder prompt so it produces:
- richer world-binding
- stronger dialogue grounding
- better final-third reliability
- cleaner alignment with a future grounding gate

This spec is planning-only. It describes what the next prompt should do, not the final wording to ship.

---

## Why The Current Prompt Is Not Enough

The current grounder prompt already has good instincts:
- exemplar-first learning
- anti-bloat rules
- anti-wiki rules
- source discipline
- self-audit

But it still leaves three structural gaps:

1. **Coverage is too soft**
   - The prompt tells the agent what good grounding feels like.
   - It does not force a scene-by-scene coverage contract.

2. **Dialogue grounding is underweighted**
   - Dialogue is mentioned as one principle among many.
   - It does not get its own pass or measurable expectations.

3. **Long-chapter reliability is too implicit**
   - The prompt warns against front-loading.
   - It does not force a final-third or chunk-level audit.

---

## Design Goals

The redesigned prompt should:
- make scene coverage explicit
- make dialogue grounding a dedicated workflow step
- make tail reliability a required audit, not a suggestion
- stay compatible with the current anti-bloat ethos
- use the same failure vocabulary as the evaluation surface

Companion contract:
- `research/copilotcli/grounding-evaluation-surface.md`

---

## Proposed Prompt Architecture

### 1. Role and scope

Keep the role focused:
- single-agent grounding pass
- no subagent delegation
- no direct lore invention
- no prose returned inline

No major change needed here.

### 2. Startup sequence redesign

The startup should be reorganized around decision-making, not just file reads.

#### Proposed startup order

1. Read config
2. Read the grounding skill and reference packets
3. Read the verified plan
4. Read targeted memory and materials
5. Read the source chapter
6. Build a **scene map**
7. Decide **standard mode** or **chunked mode**
8. Build a **gap map** before editing

This is the key change:
- the agent should not move straight from "read inputs" to "ground the chapter"
- it should first map the chapter's risk surface

### 3. Standard mode vs chunked mode

Add an explicit mode decision.

#### Standard mode

Use when the chapter is:
- short
- mobile
- scene count is low
- dialogue runs are limited

#### Chunked mode

Use when one or more are true:
- chapter is over roughly 3500 words
- chapter has 4 or more scenes
- chapter contains long concept-heavy dialogue runs
- benchmark-like tail attenuation risk is present

The exact thresholds can be tuned later, but the prompt should force the decision instead of leaving it implicit.

---

## Required Workflow Passes

The prompt should require these passes in order.

### Pass 0 - Scene map and risk tagging

Before editing, the grounder should map:
- scene boundaries
- dominant location / route
- dialogue density
- concept-density risk
- likely grounding gaps

Risk tags:
- dialogue-heavy
- static-room
- travel-texture
- institution-heavy
- final-pressure
- tail-risk

### Pass 1 - Source map

Before adding specifics, the agent should identify:
- available place nouns
- institutional nouns
- material nouns
- character-memory anchors
- route / infrastructure nouns

This prevents generic fallback and prevents invented specificity.

### Pass 2 - Gap map

For each scene, record likely misses against the evaluation surface:
- D1 spatial/material reality
- D2 POV-bound noticing
- D3 dialogue embodiment
- D4 world / institution binding
- D5 distribution and persistence
- D6 rhythm / subtext protection
- D7 source fidelity

The prompt should require the agent to name the scene's biggest gap **before** revising it.

### Pass 3 - Primary grounding pass

Ground scene by scene, not in one undifferentiated chapter sweep.

For every scene, satisfy the **scene contract** below.

### Pass 4 - Dedicated dialogue grounding pass

Re-read only the dialogue-heavy scenes and long dialogue runs.

Questions:
- where are characters speaking without touching the world?
- where can object handling or position shift carry subtext?
- where is the scene conceptually sharp but physically thin?

This pass should be mandatory, not optional.

### Pass 5 - Final-third audit

Re-read the final third separately.

Check for:
- generic noun fallback
- thinner route / room / object detail
- abstract pressure language
- weaker dialogue embodiment

This is the anti-tail-attenuation pass.

### Pass 6 - Whole-chapter protection audit

Final pass:
- anti-bloat
- anti-wiki
- anti-overgrounding
- source fidelity
- seam check if chunked mode ran

---

## Proposed Scene Contract

Every scene should leave the grounder with explicit answers to these questions.

### Required checks

1. **Place / infrastructure anchor**
   - What specific place, route, threshold, room system, or environment binds the scene?

2. **Material / contact anchor**
   - What object, surface, tool, clothing, weather, tack, dust, chalk, door, stone, or other contact point carries the scene physically?

3. **POV noticing anchor**
   - What detail feels specific to this character's expertise or current obsession?

4. **Dialogue embodiment anchor**
   - If dialogue is present, what nearby action / contact / position beat keeps the exchange from floating?

5. **Scene-exit anchor**
   - In the last pressure beat of the scene, what keeps the prose world-bound instead of abstract?

Not every scene needs equal density, but every scene should answer all five questions.

---

## Dialogue Grounding Requirements

This needs to be far more concrete than the current prompt.

### Architectural recommendation

For Phase 2, dialogue grounding should be implemented as a **required internal pass inside the grounder**, not as a separate agent pass.

Rationale:
- it uses the same scene map, source map, and anchor inventory as the main grounding pass
- it is better treated as a second sweep over the same scenes than as a separate pipeline hop
- a future gate can measure whether this is enough before a split is considered

### Proposed rules

#### Rule 1 - Long dialogue runs need embodiment

For any dialogue run over 6 lines:
- add at least one meaningful action / object / posture / environment beat

For any run over 12 lines:
- expect at least two embodiments unless the scene's tension clearly benefits from near-total stillness

#### Rule 2 - No filler stage business

Do not solve dialogue float with random motion.

The beat must do at least one of these:
- reveal pressure
- reveal relation
- reveal tactic
- reveal environment
- reveal cost

#### Rule 3 - Shared context stays implicit

Do not inject lore into speech just to sound grounded.
Ground through:
- what hands are doing
- what bodies are doing
- what equipment is present
- what the room / road / desk / horse / wall is doing to the bodies

#### Rule 4 - Abstract argument needs physical counterweight

If the characters are debating theory, ethics, command, or philosophy, the nearby beats must still carry:
- chalk
- reins
- sleeves
- door straps
- shelves
- relay crystals
- mud
- smoke
- any other live scene carrier

---

## Chunked Mode Design

When chunked mode triggers, the prompt should force this workflow:

1. Ground one scene or chunk at a time
2. Write it immediately
3. Preserve a short rolling summary of:
   - active location / route
   - active institutions
   - active material anchors
   - active dialogue pressure
4. Move to next chunk
5. Audit seams between chunks
6. Audit the final chunk separately

### Why this matters

This directly addresses:
- long-context drift
- tail attenuation
- middle-loss effects

---

## Output Artifact Redesign

The prompt should require better notes, not just general scene summaries.

### Proposed `grounder-notes.json` additions

Add fields like:
- `mode`: `standard` or `chunked`
- `sceneAudits`: array of scene entries with:
  - biggest gap
  - anchors added by type
  - dialogue grounding applied: yes/no
  - final-beat anchor checked: yes/no
- `finalThirdAudit`:
  - risks found
  - fixes applied
  - residual concerns
- `sourceAudit`:
  - all proper-noun sources used
- `coverageSummary`:
  - opening / middle / final-third comments

This makes the pass more debuggable and gives future human reviewers better evidence.

---

## Gate Alignment

The future grounding gate should audit against the same contract the prompt is built to satisfy.

That means the prompt should explicitly self-audit against:
- G1 white-room paragraph
- G2 generic noun fallback
- G3 contactless dialogue run
- G7 tail attenuation
- G8 lore dump
- G9 over-grounding
- G10 rhythm damage
- G12 unsourced specificity

The grounder should not read gate feedback during its primary pass, but it should be designed so a future revision mode could target those same categories cleanly.

### Future split criteria

Dialogue grounding should only be split into its own later pass if:
- G3 / G4 dialogue-related findings stay dominant after the redesign
- the failures are still local enough to fix without broad scene rewrites
- benchmark gains justify the extra latency

If that happens, the most likely placement is:
- after expander
- before style-editor

That is where dialogue-heavy prose will be closest to final shape.

---

## Acceptance Criteria For The Redesign

The redesigned prompt should not be considered ready unless it can plausibly improve:
- chapter12 dialogue embodiment
- chapter12 final-third grounding
- chapter12 generic noun fallback in the ending

while preserving:
- chapter12 tension
- chapter14 mobile cadence
- anti-wiki behavior

---

## Recommended Implementation Order

If this spec is implemented later:

1. add scene map / gap map / mode decision
2. add dialogue grounding pass
3. add final-third audit
4. add chunked mode
5. expand notes artifact

That sequence gets the biggest quality gains before the more complex chunking work lands.
