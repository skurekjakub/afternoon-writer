# Afternoon Grounding Refinement Plan

## Objective

Improve the afternoon pipeline's grounding quality with emphasis on:
1. prompt and skill structure
2. dialogue grounding
3. long-chapter reliability
4. optional grounding-gate architecture

This is a planning document only. No pipeline behavior changes are proposed here yet.

---

## Planning Basis

### Benchmarks reviewed

- Chapter12:
  - `final.md`
  - `final-grounded-gpt-negative.md`
  - `final-grounded-gpt-negative-v2.md`
- Chapter14:
  - `final.md`
  - `final-grounded-gpt-negative-v2.md`

### Core findings

- `final-grounded-gpt-negative.md` shows the strongest raw grounding texture.
- `final-grounded-gpt-negative-v2.md` shows stronger discipline and less bloat.
- Chapter12 suggests late-section grounding can thin out, especially when the pass becomes more surgical.
- Chapter14 suggests shorter, more mobile chapters ground more reliably all the way through.
- Dialogue grounding still happens mostly in surrounding beats, not as a dedicated system behavior.

### Design conclusion

The next version should aim for:
- GPT-negative specificity
- GPT-negative-v2 restraint
- explicit dialogue grounding
- stronger final-third coverage
- concrete auditability

---

## Design Principles

1. **Coverage over decoration**
   - The goal is not more nouns.
   - The goal is fewer floating paragraphs and fewer generic pressure beats.

2. **Dialogue must be grounded through nearby action and contact**
   - Do not force lore into speech.
   - Ground through hands, objects, posture, gear, route friction, and shared shorthand.

3. **Late-chapter reliability is a first-class requirement**
   - A grounding pass that weakens in the last quarter is not production-safe.

4. **Any future gate must be concrete**
   - No vague verdicts.
   - Local failure classes and local suggested fixes only.

5. **Quality beats runtime for this workstream**
   - More passes are acceptable if they buy visible gains.

---

## Recommended Phase Order

1. Evaluation surface and benchmark rubric
2. Grounder prompt and skill redesign
3. Long-chapter chunking workflow
4. Grounding gate design
5. Cross-pipeline integration planning
6. Validation and rollout protocol

Reason for this order:
- A grounding gate should come after the system knows what "good grounding" means operationally.
- Otherwise the gate will only formalize fuzzy taste.

---

## Phase 1 - Build the grounding evaluation surface

**Goal:** Turn "feels floaty" into concrete failure classes that can drive both prompt design and any future gate.

Companion spec:
- `research/copilotcli/grounding-evaluation-surface.md`

### Tasks

#### 1.1 - Create a grounding failure taxonomy

Failure classes to define:
- white-room paragraph
- generic noun fallback
- dialogue float
- contact-free dialogue run
- institutional/geographic underbinding
- late-chapter anchor drop
- lore-dump overcorrection
- over-grounding / noun spam

#### 1.2 - Build a benchmark rubric from chapter12 and chapter14

For each benchmark, score:
- opening grounding quality
- dialogue-adjacent grounding quality
- final-third grounding quality
- rhythm preservation
- subtext preservation
- over-grounding risk

#### 1.3 - Define measurable checks

Candidate checks:
- paragraphs with zero concrete object or environmental anchors
- dialogue stretches longer than N lines without physical interruption
- first-third / middle-third / final-third anchor parity
- generic noun hotspots where canon nouns are available
- scenes with no POV-specific noticing anchor

### Acceptance criteria

- The team can diagnose grounding failures without relying on pure vibe.
- The rubric can distinguish chapter12 from chapter14 reliably.
- The rubric can tell richer grounding from bloated grounding.

---

## Phase 2 - Redesign the grounder prompt and skill

**Goal:** Replace soft exemplar-only behavior with an explicit, repeatable grounding workflow.

Companion specs:
- `research/copilotcli/grounder-prompt-redesign-spec.md`
- `research/copilotcli/prose-grounding-framework-redesign-spec.md`

### Tasks

#### 2.1 - Rewrite the grounder prompt around ordered passes

Recommended pass order:
1. Read benchmark constraints and sources
2. Build a scene map from the target chapter
3. Mark each scene's grounding gaps before editing
4. Ground scene by scene
5. Run dedicated dialogue-grounding pass
6. Run final-third coverage audit
7. Run full-chapter anti-bloat / anti-wiki audit

#### 2.2 - Add a per-scene grounding contract

Each scene should explicitly check for:
- place / route / infrastructure anchor
- contact or material anchor
- POV-specific noticing anchor
- dialogue-adjacent grounding beat where dialogue exists
- scene-exit anchor if the scene hands off pressure forward

#### 2.3 - Expand the grounding skill structure

Add focused sections or reference material for:
- dialogue grounding
- final-third audit rules
- anchor distribution across scenes
- anti-generic-noun fallback
- long-scene / long-chapter handling

#### 2.4 - Make benchmark deltas part of the prompt logic

The prompt should teach:
- what the original GPT-negative gets right
- what v2 gets right
- how to combine them rather than oscillate between them

### Acceptance criteria

- The prompt tells the agent what to check per scene, not just what good output feels like.
- Dialogue grounding has its own explicit pass.
- The last quarter of the chapter is audited separately before signoff.

---

## Phase 3 - Add a long-chapter chunking workflow

**Goal:** Prevent long-context drift by grounding long chapters in controlled sections.

### Tasks

#### 3.1 - Define chunking triggers

Candidate triggers:
- chapter word count threshold
- scene count threshold
- detected ratio of concept-heavy dialogue to physical action

#### 3.2 - Design the rolling-context method

Per chunk:
- read the chunk plus scene intent
- carry forward a short active-anchor summary
- write immediately
- audit the chunk before moving on

#### 3.3 - Add a final recombination audit

After chunked grounding:
- audit transitions between chunks
- audit last chunk separately
- audit global anchor spread

### Acceptance criteria

- Chunking reduces late-section generic fallback.
- Chunk boundaries do not create visible seams.
- The last chunk is at least as grounded as the opening chunk.

---

## Phase 4 - Design the grounding gate

**Goal:** Create an optional adversarial validator that checks grounding quality without turning into vague taste policing.

Companion spec:
- `research/copilotcli/grounding-gate-schema-spec.md`
- `research/copilotcli/grounding-gate-prompt-literal-blueprint.md`

### Tasks

#### 4.1 - Decide gate placement

Primary options:
- **After grounder, before expander**  
  Best for validating the grounding pass directly.

- **After expander**  
  Best if expansion often reintroduces float.

Recommended starting position:
- after grounder, before expander

Reason:
- cleaner attribution
- easier revision loop
- easier to learn whether grounding itself is improving

#### 4.2 - Define gate failure classes

The gate should look for:
- white-room paragraphs
- dialogue runs without material anchoring
- generic route / room / object nouns where story-specific nouns are available
- front-loaded grounding with weak final-third coverage
- lore-dump intrusions
- object/detail spam that breaks rhythm

#### 4.3 - Define gate outputs

The gate should emit:
- local passage references
- failure category
- severity
- suggested fix
- whether the fix is deletion, substitution, or light extension

#### 4.4 - Define the revision loop

Revision loop requirements:
- max iterations
- revision-mode grounder or grounding-reviser
- passage-local fixes instead of whole-chapter re-grounding where possible
- loop notes preserved per iteration

### Acceptance criteria

- The gate can fail prose for concrete reasons.
- The feedback is actionable enough to drive revision.
- The loop does not collapse into "make it more grounded."

---

## Phase 5 - Cross-pipeline integration plan

**Goal:** Identify the broader pipeline surfaces that would need to change if the grounding improvements are implemented.

### Tasks

#### 5.1 - Agent prompt surfaces

- `.github/agents/afternoon-grounder.agent.md`
- `.github/skills/prose-grounding-framework/SKILL.md`
- optional new grounding gate agent prompt

#### 5.2 - Orchestrator and config surfaces

Likely future surfaces:
- orchestrator dispatch sequence
- config flags for grounding gate enablement
- max iterations
- chunking thresholds or mode switches

#### 5.3 - Documentation surfaces

- `docs/afternoon-pipeline-architecture.md`
- `docs/afternoon-pipeline-technical.md`
- `docs/afternoon-pipeline-guide.md`
- afternoon skill references
- changelog if structural behavior changes

### Acceptance criteria

- No structural change is planned in isolation.
- All affected docs and references are identified up front.

---

## Phase 6 - Validation and rollout protocol

**Goal:** Make sure the new grounding workflow actually improves output and does not just create more prose.

### Tasks

#### 6.1 - Benchmark rerun plan

Re-test on:
- chapter12 benchmark set
- chapter14 benchmark set
- one additional long chapter
- one dialogue-heavy chapter

#### 6.2 - Evaluation dimensions

Score each candidate on:
- opening quality
- dialogue grounding
- final-third grounding
- rhythm preservation
- subtext preservation
- over-grounding risk
- runtime cost

#### 6.3 - Promotion rule

Only promote a new grounding workflow if it visibly improves:
- chapter12 tail coverage
- dialogue grounding
- long-chapter consistency

without unacceptable bloat.

### Acceptance criteria

- The team can say why a new prompt or workflow is better.
- Benchmark wins are visible on the actual target chapters, not just theory.

---

## Recommended Immediate Next Step

If this plan moves forward, start with **Phase 1 plus Phase 2**, not the gate.

Why:
- The biggest current weakness is under-specified grounding behavior.
- A gate added too early will only punish an unclear prompt.
- Better prompt structure and explicit dialogue/final-third checks are the fastest path to quality gains.

After that:
- test whether chunking solves enough of the late-chapter problem
- then decide whether a grounding gate is still needed

---

## Task Graph

Execution artifact:
- `research/copilotcli/task-graph-grounding-refinement-v1.json`

---

## Open Decisions

1. Should the first gate sit after grounder or after expander?
2. Should dialogue grounding remain inside the grounder, or become its own micro-pass or sub-agent later?
3. What chapter-length threshold should trigger chunked grounding?
4. Should the gate revise via the grounder itself, or via a separate revision-mode specialist?
5. How much added runtime is acceptable once the design moves from planning to implementation?

---

## Architecture Note - Should Dialogue Grounding Be A Separate Agent Pass?

### Recommendation

**Not yet.**

For the next design iteration, dialogue grounding should remain a **dedicated internal pass inside the grounder**, not a full standalone pipeline agent.

### Why

1. **Dialogue grounding is tightly coupled to scene grounding**
   - The best dialogue grounding usually comes from nearby objects, posture, route geometry, room systems, and contact surfaces.
   - Those are already the grounder's core materials.

2. **A separate agent would duplicate context and increase latency**
   - It would need the same plan, same memory, same chapter context, and often the same scene map.
   - That is expensive and likely redundant at the current maturity level.

3. **The current problem is under-specification, not role separation**
   - Right now dialogue grounding is weak because it is not enforced strongly enough.
   - That is a prompt / workflow problem first.

4. **There is already nearby agent overlap**
   - Expander touches emotional beats.
   - Style-editor touches dialogue register.
   - A new dialogue-grounding agent risks muddying boundaries before the core grounder is fixed.

### Recommended near-term architecture

- **Grounder**
  - owns the primary dialogue-grounding pass
- **Future grounding gate**
  - audits dialogue embodiment under categories like G3 / G4 / G7
- **Style-editor**
  - remains the final voice / continuity / register sweep, not the main dialogue-grounding engine

### When to revisit the split

Reconsider a separate pass only if, after the Phase 2 redesign lands:
- dialogue-related grounding failures still dominate gate results
- the fixes are passage-local and repeatable
- the extra pass improves benchmark chapters without visible rhythm damage

### If a separate pass is ever created

Best likely placement:
- **after expander, before style-editor**

Reason:
- expansion can introduce fresh dialogue float
- by that point the scene content is closer to final shape
- the pass can target embodiment without having to redo the whole grounding job
