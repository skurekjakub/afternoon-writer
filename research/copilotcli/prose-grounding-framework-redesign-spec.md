# Prose Grounding Framework Redesign Spec

## Intent

Redesign the `prose-grounding-framework` skill so it teaches grounding more reliably and supports the redesigned grounder prompt.

The current skill should remain exemplar-centered, but it needs stronger structure around:
- dialogue grounding
- distribution across scenes
- long-chapter handling
- shared failure vocabulary with the evaluation surface

This is a planning document only.

---

## What The Current Skill Gets Right

- It teaches by delta, not taxonomy.
- It protects rhythm, subtext, and dialogue from over-explanation.
- It already names several strong grounding principles:
  - contact rule
  - invisible verb rule
  - sensory rotation
  - wear-and-tear
  - institutional friction
  - action-driven dialogue tags

These should be preserved.

---

## What The Current Skill Still Lacks

1. **Dialogue grounding is underdeveloped as a workflow**
   - It is present as a principle.
   - It is not strong enough as a repeatable audit.

2. **Tail coverage is barely formalized**
   - The skill says not to front-load grounding.
   - It does not give the agent a last-third evaluation method.

3. **There is no explicit bridge to benchmark lessons**
   - The skill says "study the delta."
   - It does not force the agent to state which delta moves it is carrying forward.

4. **The skill does not expose a shared failure taxonomy**
   - That makes future generator/gate alignment harder.

---

## Redesign Principles

1. **Keep the exemplars as the teaching center**
2. **Move reusable audits into reference files**
3. **Keep SKILL.md lean enough to route attention**
4. **Teach the same failure vocabulary used by evaluation and future gating**
5. **Give dialogue and final-third reliability dedicated surfaces**

---

## Proposed Skill Package Structure

### Keep

- `SKILL.md` as the router / overview
- exemplar pairs under `references/`

### Add

- `references/pair-delta-workflow.md`
- `references/dialogue-grounding.md`
- `references/distribution-and-tail-audit.md`
- `references/chunking-playbook.md`
- `references/failure-taxonomy.md`
- `references/benchmark-deltas.md`

Optional later:
- `references/source-fidelity.md`

---

## Proposed Role Of SKILL.md

SKILL.md should become the router and contract summary, not the place where every nuance lives.

### Recommended SKILL.md structure

#### 1. Definition

What grounding is and is not.

Tie explicitly to:
- embodied scene reality
- POV-bound noticing
- dialogue embodiment
- distribution across chapter

#### 2. Exemplar rule

Read all pairs first. Study the delta.

But add one more instruction:
- write down the 3 to 5 transformation moves you learned before editing the target

#### 3. Workflow router

Tell the agent which reference packets to read:
- always: pair delta, failure taxonomy
- when dialogue-heavy: dialogue grounding
- when chapter is long: chunking playbook + distribution / tail audit
- always before finish: distribution / tail audit

#### 4. Negative constraints

Keep the current anti-bloat / anti-wiki / contact / invisible-verb rules.

#### 5. Stop condition

Ground until the prose feels world-bound, then stop.
Do not keep decorating it.

---

## Proposed Reference Files

### `pair-delta-workflow.md`

Purpose:
- force the agent to study the before/after examples actively rather than passively

Should include:
- how to list delta moves
- how to identify substitution vs extension
- how to separate real grounding from mere noun inflation

### `dialogue-grounding.md`

Purpose:
- give dialogue grounding its own durable teaching surface

Should include:
- action beats as grounding carriers
- object handling
- posture / distance / blocking
- environmental interruptions
- what does **not** count as useful stage business
- how to preserve shared-context shorthand without lore insertion

### `distribution-and-tail-audit.md`

Purpose:
- stop front-loaded grounding and late-scene generic fallback

Should include:
- opening / middle / final-third parity questions
- final pressure beat checks
- how to detect generic noun return in the last quarter
- how to compare ending density to opening density without bloating

### `chunking-playbook.md`

Purpose:
- teach the agent how to ground long chapters without context drift

Should include:
- chunking triggers
- rolling summary rules
- seam audits
- last-chunk audit

### `failure-taxonomy.md`

Purpose:
- give the generator the same vocabulary the evaluator and gate will use

Should mirror:
- `research/copilotcli/grounding-evaluation-surface.md`

At minimum:
- G1 through G12
- short definitions
- what to self-check before signoff

### `benchmark-deltas.md`

Purpose:
- convert the chapter12 / chapter14 observations into reusable teaching signals

Should teach:
- what richer GPT-negative versions got right
- what the v2 discipline got right
- where chapter12 exposed tail risk
- why chapter14 acts as a control case for shorter mobile chapters

---

## Proposed Skill Workflow

The skill should teach this order:

1. Read exemplar pairs
2. Read pair-delta workflow
3. Read failure taxonomy
4. If dialogue-heavy, read dialogue-grounding
5. If long or high-risk, read chunking-playbook
6. Ground the target
7. Read distribution-and-tail-audit before final signoff

This keeps the workflow progressive instead of loading every rule at once.

---

## Gate Alignment

The skill should explicitly say:
- the generator and future gate use the same failure IDs
- the gate is still a fresh sweep
- the generator's job is to self-audit against those categories before delivery

This creates a clean shared contract without forcing the gate to read prior notes.

---

## What Should Stay Out Of The Skill

Do not overload the skill with:
- giant inline benchmark excerpts
- every possible genre-specific example
- full gate schemas
- implementation-only details better kept in agent prompts

The skill should teach transformation logic and audit logic.
The agent prompt should teach execution order and artifacts.

---

## Acceptance Criteria For The Redesign

The redesigned skill should:
- preserve exemplar-first learning
- make dialogue grounding impossible to ignore
- make final-third audits mandatory in practice
- support chunked grounding when needed
- align with the evaluation surface and future gate categories

If those are not true, the redesign is incomplete.
