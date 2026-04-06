# Grounding Gate Schema Spec

## Short Answer

**Yes, the grounding gate is still a go.**

But it should not "consume the grounder's map" in the sense of trusting the grounder's self-audit as the basis for verdicts.

It should:
- audit against the **same evaluation surface**
- use the **same scene / category vocabulary**
- build its **own fresh audit map from the prose and plan**

That keeps the gate aligned with the generator without turning it into the generator's echo.

---

## Core Design Rule

### Shared contract, fresh sweep

The grounding gate should share:
- the same dimension model (`D1`-`D7`)
- the same failure classes (`G1`-`G12`)
- the same scene segmentation contract

But it should still:
- re-read the target prose fresh
- re-read the plan fresh
- rebuild its own audit map
- ignore prior gate findings during re-audit

This mirrors the strongest part of the slop-gate architecture:
- same rulebook
- fresh eyes every time

---

## What It Should Read

### Required inputs

1. `.afternoon/config.json`
2. `.afternoon/plans/{chapterId}.json`
3. target prose:
   - initial audit: `.afternoon/chapters/{chapterId}/v2g.md`
   - re-audit: `.afternoon/chapters/{chapterId}/v2g-r{N}.md`
4. targeted memory files from `requiredMemory`
5. plan-linked source refs needed for source fidelity checks

### Optional context inputs

Use sparingly:
- story overview
- plan meta references

These are for source-fidelity and expectation-setting, not for rewriting the prose in the gate's head.

### What it should NOT read

- `grounder-notes.json`
- `grounder-revision-r*.json`
- prior `grounding-gate-notes*.json`
- prior `grounding-gate-scratchpad*.md`

Reason:
- fresh-sweep principle
- avoid bias
- avoid inherited blind spots

---

## What "Same Grounding Map" Should Mean

If you want a shared map, use the **plan scene map**, not the grounder's self-report.

### Good shared map

- scene IDs from the verified plan
- scene titles from the verified plan
- dialogue-heavy scene flags derived from the plan + prose
- first / middle / final-third segmentation derived from target prose length

### Bad shared map

- grounder's own notes about where it thinks it succeeded
- grounder's self-labeled coverage claims

Reason:
- the gate should not grade the generator using the generator's own explanation of its work

---

## Recommended Placement

### Primary recommendation

Put the grounding gate:
- **after grounder**
- **before expander**

### Why this placement

1. It verifies the grounding pass directly.
2. It keeps attribution clean.
3. It lets the gate decide whether grounding itself is sufficient before later agents touch the prose.

### Known downside

Expander may later introduce fresh dialogue float or generic language.

Mitigation:
- style-editor should still catch residual issues
- if expansion reintroduces grounding problems consistently, consider a later lightweight grounding audit after expander

---

## Audit Phases

The gate should run in ordered sweeps.

### Phase 0 - Build fresh audit map

From plan + prose:
- identify scenes
- identify dialogue-heavy scenes
- segment chapter into first / middle / final third
- build source bank from required memory and plan refs

### Phase 1 - Scene grounding sweep

Audit against:
- D1 spatial / material reality
- D2 POV-bound noticing
- D4 world / institution binding

Primary findings:
- G1 white-room paragraph
- G2 generic noun fallback
- G4 positionless conflict
- G6 institutional / geographic underbinding
- G11 POV-misaligned grounding

### Phase 2 - Dialogue grounding sweep

Audit dialogue-heavy passages for:
- G3 contactless dialogue run
- G4 positionless conflict
- G5 abstract operational language

Questions:
- does the dialogue live in the room / road / saddle / desk / threshold?
- are the action beats meaningful rather than filler?
- is the physical counterweight strong enough?

### Phase 3 - Final-third sweep

Dedicated audit of:
- final third
- final scene
- final pressure sequence

Primary target:
- G7 tail attenuation

Secondary targets:
- G2 generic noun fallback
- G5 abstract operational language

### Phase 4 - Over-grounding and rhythm protection sweep

Audit for:
- G8 lore dump / wiki spill
- G9 over-grounding / noun spam
- G10 rhythm damage

### Phase 5 - Source fidelity sweep

Audit for:
- G12 unsourced specificity

This should be treated as a hard failure class.

### Phase 6 - Suggestion phase

For every KILL finding:
- give a local suggested fix
- classify fix mode:
  - delete
  - substitute
  - light insert
  - light swap
- cross-check against:
  - the grounding evaluation surface
  - anti-bloat / anti-wiki constraints

### Phase 7 - Aggregate verdict

Write:
- notes JSON
- scratchpad markdown
- status.json

---

## False-Positive Filters

The gate needs explicit defenses or it will over-flag.

### Defense 1 - Deliberate pressure minimalism

High-tension beats can stay sparse if the sparsity is doing real work.

Do not flag a clipped beat just because it is short.
Flag it only if it becomes generic or portable.

### Defense 2 - Shared-context dialogue

Characters with shared history do not need lore stuffed into speech.

Flag only when the dialogue floats physically, not when it uses believable shorthand.

### Defense 3 - POV withholding

If the POV does not know the proper noun yet, generic language may be correct.

Do not force naming ahead of earned knowledge.

### Defense 4 - Functional abstraction under motion

During very fast movement, some abstraction is acceptable.

Flag only when the abstraction dominates and no material anchors remain.

---

## Finding Schema

The gate should emit passage-local findings.

```json
{
  "findingId": "G3-007",
  "category": "G3",
  "dimensionRefs": ["D3", "D5"],
  "severity": "MODERATE",
  "scope": "dialogue-run",
  "sceneId": 2,
  "sceneTitle": "Mechanism, ethics, and scale",
  "lines": "181-196",
  "excerpt": "\"You built an atrocity and then taught yourself to say it cleanly.\"",
  "reason": "The exchange is conceptually sharp but physically under-embodied for too long.",
  "suggestedFix": "Jaina's fingers left a chalk print on the shelf. \"You built an atrocity and then taught yourself to say it cleanly.\"",
  "fixMode": "light insert",
  "sourceCheck": "supported"
}
```

KEEP findings should go to scratchpad with reasoning, mirroring slop-gate style.

---

## Verdict Model

Use the evaluation surface as the authority.

### Pass

- no SEVERE failures
- no G7 tail attenuation
- no G12 unsourced specificity
- no unresolved dialogue-float pattern in a dialogue-heavy scene
- only small local MILD misses

### Pass with warnings

- no SEVERE failures
- no G7
- no G12
- limited local MILD / MODERATE misses

### Fail

Any of:
- one SEVERE failure
- one G7 tail attenuation failure
- one G12 failure
- repeated MODERATE G3 dialogue failures in the same scene
- a scene still portable to any setting
- clear rhythm damage in a key pressure passage

---

## Revision Loop Design

### Recommendation

Yes, give the gate a revision loop.

### But revise with whom?

Not a separate dialogue-grounding pass.

Use:
- **grounder revision mode**

Why:
- same context
- same source bank
- same scene contract
- less pipeline sprawl

### Proposed loop

1. Grounder writes `v2g.md`
2. Grounding gate audits `v2g.md`
3. If fail:
   - grounder revision mode reads `grounding-gate-notes.json`
   - writes `v2g-r1.md`
4. Gate re-audits fresh
5. Loop up to `maxIterations`

### Proposed file pattern

- `grounding-gate-notes.json`
- `grounding-gate-notes-r1.json`
- `grounding-gate-scratchpad.md`
- `grounding-gate-scratchpad-r1.md`
- `v2g-r1.md`
- `grounder-revision-r1-notes.json`

### Exhaustion policy

Recommended initial policy:
- promote latest revision
- continue with warning

Reason:
- grounding quality is important, but this gate will have more taste / coverage judgment than slop-gate
- hard halts are likely too brittle at first

---

## Relationship To Dialogue Grounding

The gate should absolutely check dialogue grounding.

But that does **not** mean dialogue grounding needs its own agent today.

Instead:
- grounder owns the dialogue grounding pass
- gate audits whether that pass succeeded
- split later only if benchmark evidence says the internal pass is not enough

---

## Relationship To The Evaluation Surface

The gate should be built directly on:
- `research/copilotcli/grounding-evaluation-surface.md`

That document defines:
- dimensions
- failure classes
- severity
- verdict logic

The gate schema is the workflow and artifact layer built on top of that contract.

---

## Recommended Immediate Next Step

If this moves forward in planning:

1. keep the gate aligned to the evaluation surface
2. keep it as a fresh-sweep verifier
3. keep dialogue grounding inside grounder revision mode
4. only later decide whether a post-expander dialogue pass is needed
