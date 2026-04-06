# Research Comparison: My Findings vs. Copilot CLI Research

## Summary

The copilotcli research is more mature on evaluation architecture and prompt redesign. My web research adds external validation and attention-decay mechanisms. Together they converge on the same design, but disagree on **implementation order** and **dialogue weaver placement**.

---

## Where Copilot CLI Research Is Stronger

### 1. Evaluation Surface (grounding-evaluation-surface.md)
The copilotcli evaluation surface is ready to ship. It defines:
- **7 evaluation dimensions** (D1–D7): spatial/material reality, POV-bound noticing, dialogue embodiment, world/institution binding, distribution/persistence, rhythm/subtext protection, source fidelity
- **12 failure classes** (G1–G12): white-room, generic noun, contactless dialogue, positionless conflict, abstract operational language, institutional underbinding, tail attenuation, lore dump, over-grounding, rhythm damage, POV-misaligned, unsourced specificity
- **3 severity tiers**: MILD, MODERATE, SEVERE
- **Concrete verdict logic**: SEVERE = instant fail; G7 (tail attenuation) = instant fail; G12 (unsourced specificity) = instant fail; 2+ MODERATE G3 in same scene = fail
- **JSON finding format** with findingId, category, severity, excerpt, reason, suggestedFix, sourceCheck
- **Chapter summary format** with dimensionScores, segmentScores, verdict

**My rubric was less developed** — 10 dimensions without severity tiers or verdict logic. The copilotcli evaluation surface should be adopted as-is for the grounding gate.

### 2. Scene Contract (grounder-prompt-redesign-spec.md)
The copilotcli grounder redesign spec defines a per-scene contract with 5 required checks:
1. Place/infrastructure anchor
2. Material/contact anchor
3. POV noticing anchor
4. Dialogue embodiment anchor (if dialogue present)
5. Scene-exit anchor

Plus specific dialogue rules:
- Runs over 6 lines need 1 embodiment beat
- Runs over 12 lines need 2 embodiments
- No filler stage business — beats must reveal pressure/relation/tactic/environment/cost
- Abstract argument needs physical counterweight

**My research didn't formalize a scene contract.** Adopt this one.

### 3. Grounder Workflow Passes (grounder-prompt-redesign-spec.md)
The copilotcli spec defines 7 ordered passes:
- Pass 0: Scene map and risk tagging
- Pass 1: Source map (available nouns)
- Pass 2: Gap map (per-scene weaknesses against D1–D7)
- Pass 3: Primary grounding pass
- Pass 4: Dedicated dialogue grounding pass (INTERNAL)
- Pass 5: Final-third audit
- Pass 6: Whole-chapter protection audit

**My plan skipped the diagnostic passes (0-2) and assumed dialogue as a separate agent.** The copilotcli structure is more thorough for the grounder's own workflow.

### 4. Skill Redesign Architecture (prose-grounding-framework-redesign-spec.md)
Detailed new reference file structure:
- pair-delta-workflow.md
- dialogue-grounding.md
- distribution-and-tail-audit.md
- chunking-playbook.md
- failure-taxonomy.md (mirrors evaluation surface)
- benchmark-deltas.md

**My Phase 4 (diagnostic routing) was thinner.** The copilotcli spec provides a concrete file list.

---

## Where My Web Research Adds Value

### 1. Attention Decay Mechanisms (research-attention-decay.md)
The copilotcli research names "long-context drift" and "tail attenuation" as problems. My research explains WHY:
- Attention drift: 2-4x bias toward recent output over source material
- Context degradation: pronoun resolution 65%→34% over 5K tokens
- Cascade error propagation: token predictability reaches 90-91%, reducing self-correction
- Practical thresholds: degradation starts at 30-50% of max context window

**Value**: Validates per-scene processing with concrete numbers. Also suggests that re-priming checkpoints (copilotcli's chunked mode with rolling summary) may not fully work — the model's attention to the re-prime degrades too.

### 2. Multi-Agent Pattern Research (research-multi-agent-patterns.md)
- Fresh-eye principle: gate must NOT read grounder notes (copilotcli says the same)
- Bounded retry with convergence strategies (deletion-first, minimal substitution, promote anyway)
- Evidence from production pipelines (Lee 2025, BidGenie, Google ADK) confirming the pattern

**Value**: External validation of the gate loop pattern. The copilotcli research designed the gate but didn't reference external implementations.

### 3. Dialogue Grounding Taxonomy (research-dialogue-grounding.md)
- 7 techniques (action-driven tags, contact-based emotion, environment persistence, object continuity/GRRM, pace-dependent choreography, institutional grounding, cross-sense anchoring)
- 7-point checklist for gate audit
- Analysis of the Anti-Wiki/Anti-Spoonfeeding trap

**Value**: More granular than the copilotcli dialogue rules. Could feed into the proposed `dialogue-grounding.md` reference file.

### 4. White Room & Sensory Grounding (research-white-room-sensory-grounding.md)
- 7 grounding approaches with concrete examples
- 10-point scene checklist
- Palimpsest rule (wear-and-tear) and institutional friction as grounding surfaces

**Value**: Teaching content for the redesigned skill's reference files.

---

## Key Disagreements

### 1. Implementation Order

**Copilotcli says**: Prompt + skill redesign FIRST, gate SECOND.
> "A gate added too early will only punish an unclear prompt. Better prompt structure and explicit dialogue/final-third checks are the fastest path to quality gains."

**My plan says**: Gate FIRST.
> High impact, mirrors proven slop-gate pattern, existing helper agent is ready to promote.

**Resolution**: The copilotcli reasoning is stronger. A gate evaluating against a well-defined evaluation surface makes sense, but the grounder needs to be REDESIGNED to satisfy that surface first. Otherwise the gate will fail every chapter and the revision loop will be trying to fix systemic prompt problems through passage-level patches.

**Recommendation**: Adopt copilotcli order — redesign grounder prompt + skill FIRST, then add gate. The evaluation surface document can be written first as the shared contract.

### 2. Dialogue Weaver: Internal Pass vs. Separate Agent

**Copilotcli says**: Internal pass inside grounder (Pass 4).
> "Dialogue grounding is tightly coupled to scene grounding. A separate agent would duplicate context. The current problem is under-specification, not role separation."

**User chose**: Separate agent (after grounder, before gate).

**Copilotcli also says**: "Split only if G3/G4 findings stay dominant after redesign. If split, place after expander, before style-editor."

**Resolution**: Start with internal pass. If after prompt redesign, G3/G4 dialogue failures persist, THEN promote to separate agent. This is a cheaper experiment.

### 3. Per-Scene Subagent Calls vs. Chunked Mode

**Copilotcli says**: Chunked mode inside one grounder call with rolling summary.
> Ground one scene at a time, write immediately, carry forward a short rolling summary of active nouns/institutions/dialogue state.

**User chose**: Per-scene subagent calls (separate grounder invocation per scene).

**My research says**: Per-scene subagent calls are more reliable because attention budget is truly reset. Rolling summaries within one call still suffer from attention decay.

**Resolution**: Both approaches should be available:
- **Chunked mode** (copilotcli) as default — cheaper, good enough for shorter chapters
- **Per-scene subagent mode** (my proposal) as escalation for long/complex chapters
- Config-driven: `agents.grounder.processingMode: "standard" | "chunked" | "per-scene"`

---

## Merged Recommendation: Updated Phase Order

1. **Write the evaluation surface** — adopt copilotcli's grounding-evaluation-surface.md as the shared contract (it's already written)
2. **Redesign grounder prompt** — adopt copilotcli's 7-pass workflow with scene map, gap map, dialogue pass, final-third audit
3. **Redesign grounding skill** — add the reference files the copilotcli spec proposes
4. **Add chunked mode to grounder** — copilotcli's rolling-summary approach as default
5. **Test on chapter 12 + 14** — measure whether prompt + skill redesign alone closes the gap
6. **Add grounding gate** — if residual failures persist, promote the existing adversarial judge with the evaluation surface as its rubric
7. **Add per-scene subagent mode** — if chunked mode still shows tail attenuation
8. **Add dialogue weaver agent** — only if G3/G4 failures persist after grounder internal dialogue pass

---

## What To Adopt Whole-Cloth From Copilot CLI Research

- grounding-evaluation-surface.md → becomes the gate's rubric AND the grounder's self-audit contract
- Failure classes G1–G12 → used everywhere
- Severity model (MILD/MODERATE/SEVERE) → gate verdict logic
- Scene contract (5 required checks) → grounder per-scene audit
- Dialogue rules (6-line/12-line thresholds, no filler business, physical counterweight for abstract argument)
- JSON finding format → gate output schema
- Chapter summary format → gate status output
- Verdict logic (pass/pass-with-warnings/fail) → gate decision

## What's New From My Research

- Attention decay MECHANISMS with concrete numbers → justifies per-scene processing
- External multi-agent pipeline validation → confirms gate loop pattern
- Grounding monotony check → new failure class to add (G13?)
- Dialogue grounding taxonomy with 7 techniques → feeds into dialogue-grounding.md reference file
- 7 sensory grounding approaches → feeds into skill reference files
