# Plan: Grounding Pipeline Refinement

## Status: ALIGNED — Phase 1 detailed, Phases 2-5 outlined

## TL;DR
The afternoon pipeline's grounding pass produces good-but-not-great results because of three confirmed issues: (1) attention drift degrades grounding quality toward the end of long chapters, (2) dialogue is structurally under-grounded due to Anti-Wiki constraints preventing the grounder from touching it, and (3) a single grounding pass leaves residual holes that only an adversarial gate loop can catch. The fix is a 3-part improvement: chunk-level processing with re-priming, a dedicated dialogue weaving pass, and a grounding gate convergence loop — plus restructuring the grounding skill to be diagnostic rather than purely exemplar-based.

## Research Findings

### 1. Attention Decay Toward End of Text (CONFIRMED)
- "Lost in the Middle" (Stanford, 2023): LLMs attend weakly to mid-context content
- "Context Rot" (Anthropic, 2025): Every token added depletes the model's "attention budget"
- Attention Drift: LLMs pay 2-4x more attention to recently generated content than source material when generating final portions
- Cascade Error Propagation: small deviations early compound into larger drift later
- Context degradation: pronoun resolution drops from 65%→34% over 5K tokens; entity tracking drops 78%→41%
- **Implication for grounder**: The grounder already writes v2g.md scene-by-scene (good), but the PRIMING STACK (exemplars, materials, rules) sits in the initial context and gets diluted as the agent processes later scenes. The anti-bloat rules, anti-wiki rules, and grounding principles get progressively less attention.

### 2. Dialogue Under-Grounding (CONFIRMED)
- The Anti-Wiki Rule explicitly tells the grounder NOT to inject lore into dialogue
- The Anti-Spoonfeeding Rule prevents adding emotional grounding to dialogue
- The Contact Rule delays material details until physical interaction
- Net effect: the grounder's negative constraints effectively create a "dialogue skip zone"
- The existing `_afternoon-grounder-dialogue.agent.md` (dialogue-action-weaver) already exists but is NOT wired into the pipeline
- The scene-grounding skill's dialogue-pressure packet covers status/leverage but not physical/environmental tethering during conversation

### 3. Single Pass Insufficiency (CONFIRMED)
- Chapter 12 analysis: gpt-negative-v2 (+1.8% surgical) outperformed gpt-negative (+17.2% heavy)
- This means precision matters more than volume — a gate that catches missed spots is more valuable than a pass that over-grounds
- The `_afternoon-grounder-gate.agent.md` (adversarial-grounding-judge) already exists with a 6-point rubric but is NOT wired into the pipeline
- The slop-gate pattern (converging feedback loop) is proven effective in the existing pipeline

### 4. Skill Structure Limitations
- Current prose-grounding-framework is purely exemplar-based (5 before/after pairs)
- No diagnostic routing: same approach for action scenes, dialogue scenes, travel scenes, domestic scenes
- The prose-scene-grounding skill HAS diagnostic packets (action geometry, dialogue pressure, travel texture, magic and wonder) but is NOT mounted on the grounder agent
- Gap: no domestic/household packet, no ritual/sacred-space packet, no grief/aftermath packet

## Decisions Made
- Phase 1 (Grounding Gate Loop) is first focus
- Dialogue weaver runs as separate agent (after grounder, before gate)
- Per-scene subagent calls for grounder (most aggressive, maximally effective)
- Nothing explicitly out of scope

## PHASE 1: Grounding Gate Loop — Detailed Implementation

### Overview
Mirror the slop-gate convergence pattern: grounder → grounding-gate audit → grounder revision mode → re-audit, up to N iterations. The gate uses the existing 6-point adversarial rubric. On pass or exhaustion, proceed to dialogue weaver (Phase 2) then expander.

### File Naming Convention (Mirrors Slop-Gate)

| Iteration | Grounder reads from | Grounder writes | Gate re-audits |
|-----------|-------------------|----------------|---------------|
| Initial   | v2.md             | v2g.md         | v2g.md        |
| 1         | grounding-gate-notes.json | v2g-r1.md | v2g-r1.md |
| 2         | grounding-gate-notes-r1.json | v2g-r2.md | v2g-r2.md |
| N         | grounding-gate-notes-r{N-1}.json | v2g-rN.md | v2g-rN.md |

On pass: `cp v2g-rN.md v2g.md` (promote). On exhaustion: promote last revision anyway, log `groundingGateExhausted` in manifest, continue.

### New/Modified Files

#### 1. `afternoon-grounding-gate.agent.md` (NEW — promote from `_afternoon-grounder-gate.agent.md`)

Promote the existing adversarial-grounding-judge from helper to pipeline agent. Key additions:
- Read config.json for project context
- Read verified plan for scene structure and intent
- Read materials/memory for source verification (every proper noun must be sourced)
- Output structured JSON (not just prose critique)
- Iteration awareness: if kill counts plateau across iterations, switch to deletion-first strategy (like slop-gate)
- Cross-validate fixes: ensure suggestedFix doesn't introduce slop (check against slop-hitlist)

**Gate outputs:**
- `grounding-gate-notes.json`: Array of KILL findings, each with `quote`, `violationType`, `indictment`, `suggestedFix`, `fixDifficulty`, `sceneId`
- `grounding-gate-scratchpad.md`: All KEEP decisions with reasoning (for human audit)
- `status.json`: `{verdict: "pass"|"fail", killCount: N, iteration: N}`

**6-Point Rubric** (from existing helper, refined):
1. Rhythm Destruction (bloat from grounding)
2. Subtext Spoon-feeding (psychology made explicit)
3. Wiki-Speak (characters explaining their world)
4. Jargon Fatigue (domain jargon replacing normal verbs)
5. Melodramatic Tropes (over-the-top aesthetic grounding)
6. Preemptive Exposition (material details before contact)

**Additional audit dimensions** (new):
7. Grounding coverage: are there scenes/passages with zero grounding touches?
8. Source verification: every injected proper noun traceable to materials/memory?
9. Sensory rotation: is grounding visual-only or does it use touch/smell/sound/temperature?
10. POV fidelity: are grounded details filtered through POV character's expertise?

#### 2. `afternoon-grounder.agent.md` (MODIFIED — add revision mode)

Add a revision mode parallel to slophunter's:
- Normal mode: read v2.md, apply grounding, write v2g.md
- Revision mode: read grounding-gate-notes.json + current v2g-rN.md, apply pre-validated fixes, write v2g-r{N+1}.md
- Revision mode is more surgical: apply specific fixes from gate findings rather than re-grounding the whole chapter
- Revision mode preserves ALL prose the gate marked KEEP

#### 3. `afternoon-orchestrator.agent.md` (MODIFIED — add grounding gate loop to routing)

Updated routing table:
```
... → 4. Slophunter → 5. Slop-Gate → 6. Grounder → 6b. Grounding-Gate → [6c. Grounder revision ↔ 6b. Gate re-audit] → 7. Dialogue-Weaver → 8. Expander → ...
```

Add to orchestrator:
- Dispatch grounding-gate after grounder completes
- If gate verdict is "fail": dispatch grounder in revision mode with feedbackPath
- Loop up to `config.agents.groundingGate.maxIterations`
- On pass or exhaustion: promote file, proceed to dialogue weaver (or expander if dialogue weaver disabled)

#### 4. `config.json` (MODIFIED — add grounding gate config)

```json
"agents": {
  "groundingGate": {
    "enabled": true,
    "maxIterations": 3
  },
  "dialogueWeaver": {
    "enabled": true
  }
}
```

Default maxIterations: 3 (not 5 like slop-gate — grounding gate fixes are more expensive and finding diminishes faster)

### Per-Scene Processing Model (Grounder)

**The core question: how does the grounder orient itself per-scene when invoked as subagent calls?**

**Approach: Scene extraction from plan structure.**

The verified plan JSON has explicit scene boundaries:
- Each scene has `sceneId`, `title`, `castInScene`, `knowledgeAtSceneStart`, `sceneFunction`
- Each scene's beats have `sensoryAnchors`, `transitionIntent`, `newOnPageInformation`
- Scenes chain via `transitionIntent` at the last beat

**Per-scene grounder invocation receives:**
1. **Full priming stack** (re-loaded fresh each time): exemplars, anti-bloat rules, materials, voice sheets
2. **Scene-specific plan**: just this scene's beats from the verified plan JSON
3. **Scene-specific prose**: extracted from v2.md using scene boundaries
4. **Bridge context**: last 2-3 paragraphs of the PREVIOUS grounded scene (for continuity) + first paragraph of the NEXT ungrounded scene (for transition awareness)
5. **Scene-specific memory**: only the memory files referenced by this scene's beats

**Scene extraction method:**
- Orchestrator (or grounder in its first pass) reads v2.md and the verified plan
- Uses scene titles and beat sensory anchors to locate scene boundaries in prose
- Writes extracted scenes to temporary files: `v2-scene-1.md`, `v2-scene-2.md`, etc.
- Each grounder subagent call processes one scene file
- After all scenes grounded, stitching pass reassembles into v2g.md
- Stitching validates transitions between grounded scenes didn't break

**Why this works:**
- Each scene call gets full attention budget on ~1-2K words (not 4-8K)
- Priming stack is fresh — no attention decay
- Sensory anchors and grounding principles get maximum attention
- Scene boundaries come from an authoritative source (the verified plan)

**Risk: cross-scene continuity.**
- Mitigated by bridge context (previous scene's tail + next scene's head)
- Grounder must not ground transition paragraphs differently than the scene they belong to
- Stitching pass can catch seam artifacts

### Verification Steps

1. **Convergence test**: Run grounding gate on existing chapter 12 v2g.md — does it produce useful KILLs or mostly false positives? Validates the rubric.
2. **Per-scene extraction test**: Extract scenes from chapter 12 v2.md using plan boundaries. Validate all prose is accounted for (no gaps, no overlaps).
3. **Re-priming effectiveness**: Ground a test chapter both ways (single pass vs. per-scene) and compare grounder-notes.json touch distribution (touches per scene should be more even in per-scene mode).
4. **Gate loop convergence**: Run full loop on a test chapter. Verify kill count decreases across iterations and loop terminates within maxIterations.
5. **Dialogue weaver handoff**: After grounding gate passes, run dialogue-action-weaver on v2g.md. Count action beats before/after. Verify no grounding violations introduced.
6. **End-to-end**: Run full pipeline on a fresh chapter with all changes. Compare final.md against a chapter processed with the old pipeline.

---

## PHASE 2: Dialogue Weaving Pass — Outline

**Agent**: Promote `_afternoon-grounder-dialogue.agent.md` to `afternoon-dialogue-weaver.agent.md`
**Position**: After grounding gate passes, before expander
**Reads**: v2g.md (grounded), verified plan, voice sheets, materials, prose-scene-grounding dialogue-pressure packet
**Writes**: v2g.md (in-place) or v2gd.md (new version — TBD based on versioning cleanliness)
**Scope**: Dialogue tags, action beats, and internal monologue surrounding quotes ONLY. Does not change spoken words (unless they violate world-specific register). Does not touch non-dialogue prose.

Key additions to existing helper:
- Mount prose-scene-grounding dialogue-pressure packet
- Source verification: action beats must use objects/settings from materials and plan
- Voice sheet compliance: character-specific action beats (a mage handles different objects than a soldier)
- POV filtering: action beats visible through POV character's lens

---

## PHASE 3: Per-Scene Re-Priming — Outline

Covered above in Phase 1's per-scene processing model. The grounder processes scenes independently with full priming re-loaded per scene. This is the primary mitigation for attention decay.

Additional consideration: should the grounding GATE also process per-scene? Probably not — the gate needs to see the full chapter to catch cross-scene consistency issues (e.g., grounding a location name differently in scene 1 vs. scene 5).

---

## PHASE 4: Diagnostic Skill Routing — Outline

Restructure `prose-grounding-framework/SKILL.md` to add a diagnostic routing table:

| Scene type | Primary grounding surface | Secondary | Exemplar pairs to read |
|-----------|--------------------------|-----------|----------------------|
| Action/confrontation | Geometry, material, impact chains | Sound, temperature | Pair 1 (ward breach) |
| Dialogue-heavy | Environment, action beats, objects-in-hand | Institutional friction | Pair 2 (argument), Pair 5 (grain yards) |
| Travel/movement | Route, terrain, bodily wear, ecology | Weather, infrastructure | Pair 3 (road south) |
| Investigation/discovery | Material close-read, document texture | Light, smell | Pair 4 (phylactery) |
| Intimate/emotional | Body, temperature, texture | Sound, breath | (NEW — needs exemplar pair) |
| Domestic/rest | Routine objects, food, comfort/discomfort | Sound, light | (NEW — needs exemplar pair) |

Mount prose-scene-grounding packets on the grounder for each scene type.

---

## PHASE 5: Chapter Length Analysis — Outline

Gather data from existing chapters:
- Word count at each version (v1 through final)
- Grounder-notes.json: touches per scene, distribution across chapter
- Grounding-gate audit: would violations cluster in later scenes?

If degradation confirmed: recommend max chapter target (e.g., 5K words) or automatic scene-level splitting in the planner.
