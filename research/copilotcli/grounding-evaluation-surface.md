# Grounding Evaluation Surface

## Purpose

This document defines the shared evaluation contract for:
- human benchmark review
- future grounding-gate audits
- prompt / skill acceptance testing
- revision-loop feedback

The point is to replace "this still feels floaty" with a stable set of dimensions, failure classes, and verdict rules.

---

## What Counts As Grounding

Grounding is not "more lore."

Grounding means the prose feels inseparable from this world because the scene is bound by:
- place
- route / geometry
- material contact
- institutional reality
- POV-specific noticing
- dialogue-adjacent physical life

Good grounding does **not**:
- explain the world
- inject wiki paragraphs
- flatten subtext
- make everyone speak in lore nouns
- expand high-pressure beats until the rhythm dies

---

## Evaluation Levels

The surface uses four levels at once.

### Level A - Anchor unit

The smallest useful evidence unit:
- a concrete object
- a material/contact cue
- a geographic or institutional noun
- a route / position cue
- a dialogue-adjacent action beat

### Level B - Passage unit

The main finding unit for gate output.

A passage unit is:
- 1 to 5 sentences
- or one uninterrupted dialogue run
- or one short transition beat

### Level C - Scene unit

Used for distribution checks.

Questions:
- does the scene stay grounded all the way through?
- does it drift into portable-to-any-setting prose?
- does dialogue stay embodied?

### Level D - Chapter distribution unit

Used for long-text reliability checks.

The chapter is reviewed by:
- first third
- middle third
- final third

This is where tail attenuation is measured.

---

## Evaluation Dimensions

### D1 - Spatial and material reality

**What good looks like**
- the reader can tell where bodies, objects, and surfaces are
- key objects have contact weight, texture, resistance, or use
- important movement happens through space, not in a void

**What failure looks like**
- generic room / road / corridor language
- action with no surfaces, objects, or route geometry
- abstract staging like "the situation sharpened" with no physical carrier

### D2 - POV-bound noticing

**What good looks like**
- details arise through the POV's expertise and concerns
- what gets named feels like something this person would notice

**What failure looks like**
- neutral narrator worldbuilding
- details that feel pasted in from lore notes rather than perceived
- grounding that could belong to any POV

### D3 - Dialogue embodiment

**What good looks like**
- dialogue runs are interrupted or shaded by meaningful action, objects, position shifts, or environmental response
- speech feels situated in a room, on a road, at a desk, on a horse, at a wall

**What failure looks like**
- talking heads
- concept-vs-concept exchange with no physical counterweight
- dialogue explained by lore instead of grounded by scene behavior

### D4 - World and institution binding

**What good looks like**
- named geography, systems, factions, protocols, or infrastructure appear where they matter
- the scene could not be transplanted to a generic fantasy room without losing force

**What failure looks like**
- portable-to-any-setting phrasing
- generic "city", "road", "order", "magic", "weapon", "authority"
- missed opportunity to use already-established canon nouns

### D5 - Distribution and persistence

**What good looks like**
- grounding is spread across the scene and chapter
- later paragraphs stay as world-bound as early ones

**What failure looks like**
- front-loaded specificity
- late-scene generic fallback
- final-third thinning

### D6 - Rhythm and subtext protection

**What good looks like**
- the pass adds specificity without breaking tension, pace, or implication
- high-pressure passages stay clipped when they need to stay clipped

**What failure looks like**
- grounding that bloats the line
- lore or sensory additions that explain what the reader already understands
- overgrown sentence mass in pressure beats

### D7 - Source fidelity and canon fit

**What good looks like**
- added specifics are traceable to memory, materials, plan, or overview
- no invented lore slips in

**What failure looks like**
- false precision
- made-up titles or mechanics
- canon drift

---

## Failure Classes

Use these IDs consistently in benchmark notes and future gate output.

### G1 - White-room paragraph

A paragraph or short passage lacks enough spatial / material reality to situate the action.

### G2 - Generic noun fallback

A load-bearing noun stays generic even though a story-bound noun is available.

Examples:
- room
- road
- city
- door
- stone
- water
- thing

### G3 - Contactless dialogue run

A dialogue run goes on too long without any action, object, posture, or environmental interruption.

### G4 - Positionless conflict

Conflict intensifies, but the prose does not tell us how bodies are arranged, what they are doing, or what surfaces / tools are in play.

### G5 - Abstract operational language

The prose describes pressure, conflict, travel, or procedure in abstract terms without physical carrier.

### G6 - Institutional or geographic underbinding

The passage talks about power, protocol, command, study, war, or movement without enough named system / place grounding.

### G7 - Tail attenuation

Grounding quality drops visibly in the final third or final pressure sequence.

### G8 - Lore dump / wiki spill

Grounding becomes explanation instead of lived scene reality.

### G9 - Over-grounding / noun spam

The prose piles on specifics without improving embodiment, pressure, or scene clarity.

### G10 - Rhythm damage

Grounding changes damage tension, cadence, or scene momentum.

### G11 - POV-misaligned grounding

The details may be specific, but they do not feel like details this POV would think in.

### G12 - Unsourced specificity

A proper noun, title, mechanic, or material detail appears without source support.

---

## Required Sweeps For A Future Grounding Gate

### Sweep 1 - Scene grounding sweep

For every scene:
- inspect the opening beat
- inspect one middle beat
- inspect the scene exit or final pressure beat

Questions:
- is the scene world-bound?
- does the scene stay world-bound?
- does the exit stay grounded?

### Sweep 2 - Dialogue grounding sweep

For every dialogue-heavy scene:
- inspect each dialogue run longer than 6 lines
- flag G3 if there is no meaningful embodiment nearby
- distinguish meaningful embodiment from filler stage business

### Sweep 3 - Final-third sweep

Read the final third separately and compare against the opening third.

Questions:
- did generic nouns return?
- did route / room / object detail thin out?
- did action become more abstract?

### Sweep 4 - Over-grounding sweep

Look specifically for:
- lore explanations
- noun spam
- overlong sentences created by grounding
- pressure beats turned into documentation

### Sweep 5 - Source fidelity sweep

Check that added specifics are sourced from:
- plan
- memory
- materials
- overview

Unsourced precision is an automatic major problem.

---

## Severity Model

### MILD

Local missed opportunity.

Examples:
- a single generic noun in an otherwise grounded paragraph
- one dialogue beat that could use an object interaction

### MODERATE

The passage noticeably floats or loses scene pressure because grounding is missing or mishandled.

Examples:
- a dialogue exchange reads as talking heads
- a transition beat becomes generic
- a scene exit loses environmental specificity

### SEVERE

The failure breaks the passage's usability or trustworthiness.

Examples:
- a whole scene becomes portable to any setting
- the final pressure sequence loses grounding badly
- the pass invents canon
- grounding turns a pressure beat into a lore dump

---

## Proposed Finding Format

For a future grounding gate, findings should be passage-local, not vague.

```json
{
  "findingId": "G3-014",
  "category": "G3",
  "dimensionRefs": ["D3", "D5"],
  "severity": "MODERATE",
  "scope": "dialogue-run",
  "scene": "Scene 2 - Mechanism argument",
  "lines": "181-196",
  "excerpt": "\"You built an atrocity and then taught yourself to say it cleanly.\" ...",
  "reason": "The exchange carries conceptual pressure but has too little object/contact embodiment around it. Voices are grounded by conflict, but not enough by room, posture, or handling.",
  "expectedSurface": "One or two action or contact beats tied to chalk, shelf, desk, sleeve, stone, or body position would bind the exchange to the room without slowing it.",
  "suggestedFix": "Jaina's fingers left a chalk print on the shelf. \"You built an atrocity and then taught yourself to say it cleanly.\"",
  "sourceCheck": {
    "status": "supported",
    "backing": ["plan", "chapter text", "memory"]
  }
}
```

KEEP decisions should go to a human scratchpad, mirroring the slop-gate pattern.

---

## Proposed Chapter Summary Format

```json
{
  "chapterId": "chapter-12",
  "targetFile": "v2g.md",
  "verdict": "fail",
  "dimensionScores": {
    "D1": 2,
    "D2": 3,
    "D3": 1,
    "D4": 3,
    "D5": 1,
    "D6": 2,
    "D7": 3
  },
  "segmentScores": {
    "openingThird": 3,
    "middleThird": 2,
    "finalThird": 1
  },
  "summary": {
    "totalKills": 6,
    "mildKills": 2,
    "moderateKills": 4,
    "severeKills": 0,
    "dominantFailures": ["G3", "G7", "G2"]
  }
}
```

---

## Verdict Logic

This should stay strict enough to matter, but not so strict it punishes local misses as total failure.

### Pass

- no SEVERE failures
- no G7 tail attenuation failure
- no dialogue-heavy scene with unresolved G3
- no unsourced specificity
- only a small number of local MILD misses

### Pass with warnings

- no SEVERE failures
- no G7 tail attenuation
- dialogue grounding broadly holds
- some MILD and limited MODERATE misses remain, but they are local and fixable

### Fail

Any of the following:
- one SEVERE failure
- one G7 tail attenuation failure
- one G12 unsourced specificity failure
- two or more MODERATE G3 dialogue-float failures in the same scene
- a scene that remains portable to any setting
- grounding that clearly damages rhythm in a key pressure beat

---

## How The Surface Should Be Used

### Use 1 - Benchmark review

Human reviewer uses:
- dimensions
- failure classes
- severity
- segment scores

### Use 2 - Prompt acceptance

A new grounder prompt should not be accepted unless it improves:
- D3 dialogue embodiment
- D5 distribution / persistence
- final-third score on chapter12

while preserving D6 rhythm / subtext.

### Use 3 - Future grounding gate

The future gate should:
- read this surface first
- audit passages against it
- emit KILL / KEEP findings with suggested fixes
- use the same category IDs so results compare cleanly across runs

---

## Immediate Recommendation

Treat this evaluation surface as the contract first.

Then rewrite:
- the grounder prompt
- the grounding skill
- any future grounding gate

against this contract.

That keeps the generator and gate from drifting into two different ideas of what "grounded" means.
