# Afternoon Pipeline Changelog

New entries are appended at the top.

---

## 2026-04-07 — Split fake simplification out into its own pass-B guide

**Problem:** Fake simplification was buried as Pattern P5 inside `phantom-concreteness-guide.md` and treated in pass B as an extra sweep on that guide. That made the failure mode easy to underweight even after it had proved important in chapter16-style exchanges.

**Root cause:** Fake simplification is adjacent to phantom concreteness, but it is not the same audit problem. Phantom concreteness asks whether a line sounds precise without evidence; fake simplification asks whether a translation setup actually produced usable speech. Packing both into one guide blurred the boundary and made the workflow describe the translation check as an add-on instead of a first-class pass-B concern.

**Changes:**

| File | Change |
|---|---|
| `resources/fake-simplification-guide.md` | New dedicated pass-B guide for lines that claim to simplify or translate but still withhold usable payload. |
| `resources/phantom-concreteness-guide.md` | Removed fake-simplification coverage so the guide stays focused on abstract specificity failures. |
| `.github/skills/afternoon-slop-gate-workflow/references/1-read-workspace.md` | Added `fake-simplification-guide.md` to the locked pass-B guide pack. |
| `.github/skills/afternoon-slop-gate-workflow/references/2-build-false-positive-filter.md` | Updated the dialogue-defense wording to name fake simplification as its own speech-level guide surface. |
| `.github/skills/afternoon-slop-gate-workflow/references/3b-pass-b-guides.md` | Reworked pass B routing so fake simplification is audited as its own guide, not as a phantom-concreteness sub-sweep. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Updated the pass-B guide list and split the old phantom-concreteness sweep note into separate phantom and fake-simplification responsibilities. |
| `docs/afternoon-pipeline-technical.md` | Updated the technical description so pass B now explicitly owns separate phantom-concreteness and fake-simplification guides. |
| `docs/afternoon-pipeline-architecture.md` | Updated the user-facing slop-gate summary to describe fake simplification as its own pass-B guide. |
| `docs/afternoon-pipeline-guide.md` | Updated the user-facing notes-artifact description to mention separate fake-simplification kills in pass B. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** Pass B now audits fake simplification as a first-class guide file. Exchanges that claim to simplify into plain or street-level speech no longer rely on phantom concreteness to catch them indirectly.

---

## 2026-04-07 — Teach the pipeline to kill fake simplification in dialogue

**Problem:** The chapter16 gate exchange still sounded vague even after multiple slophunter and slop-gate passes. The prose used a few place labels and trade nouns, but the "plain speech" translation never became actionable. Worse, the slophunter notes praised the exchange as a success.

**Root cause:** The pipeline was catching abstract slogan lines and prestige compression, but it still over-credited generic logistical shorthand once it carried a couple proper nouns. It had no explicit rule for fake simplification: dialogue that claims to put something in smaller words or street terms while still hiding the usable payload.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-slophunter.agent.md` | Expanded the dialogue-register hunt so it now kills fake simplification in quoted speech and added the same check to revision-mode self-audit. |
| `resources/phantom-concreteness-guide.md` | Added explicit fake-simplification coverage, a new P5 pattern, anti-rationalization guidance for place-name camouflage, and new calibration examples. |
| `.github/skills/afternoon-slop-gate-workflow/references/2-build-false-positive-filter.md` | Clarified that dialogue defense does not protect replies that are supposed to simplify or translate a thought into usable speech. |
| `.github/skills/afternoon-slop-gate-workflow/references/3b-pass-b-guides.md` | Added a dedicated pass-B sweep question for fake simplification in dialogue. |
| `.github/skills/prose-grounding-framework/SKILL.md` | Taught the grounding framework that plain-language dialogue must cash out into usable local targets, routes, objects, or triggers. |
| `.github/skills/prose-grounding-framework/references/before-dialogue-2.md` | Added a new bad exemplar showing a fake-simplification tactical exchange. |
| `.github/skills/prose-grounding-framework/references/after-dialogue-2.md` | Added the corrected grounded rewrite, with usable street-level targets and triggers. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Synced the slophunter hunt description and slop-gate phantom-concreteness responsibilities to the new fake-simplification rule. |
| `docs/afternoon-pipeline-technical.md` | Updated the slophunter and slop-gate technical summaries to describe fake simplification as a live failure mode. |
| `docs/afternoon-pipeline-architecture.md` | Updated the user-facing slophunter and slop-gate summaries to describe the new rule and corrected the slop-gate cross-check wording. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The pipeline now treats "plain speech" dialogue as a concrete delivery problem, not just a voice problem. If a line claims to translate into smaller words or street terms but another character still could not act on it immediately, slophunter should rewrite it and slop-gate pass B should kill it.

---

## 2026-04-07 — Make slop-gate pass prompts self-contained

**Problem:** The new phased slop-gate workflow still carried stray cross-pass language. A pass-local invocation could be told to think about the other pass's guides or to validate fixes against both pass packs, which blurred the isolation the split was supposed to create.

**Root cause:** The workflow-skill refactor preserved old cross-pass wording from the pre-slim prompt instead of rewriting Phase 4 and the pass route files as strictly pass-local instructions.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-slop-gate.agent.md` | Reworded the phase summary so Phase 4 validates fixes against the current pass guide pack, not all slop-gate guides. |
| `.github/skills/afternoon-slop-gate-workflow/references/1-read-workspace.md` | Rewrote pass selection language to stay neutral and pass-local instead of referring to "the other pass." |
| `.github/skills/afternoon-slop-gate-workflow/references/3a-pass-a-guides.md` | Reworded the pass A route to describe only its own guide pack and scope. |
| `.github/skills/afternoon-slop-gate-workflow/references/3b-pass-b-guides.md` | Reworded the pass B route to describe only its own guide pack and scope. |
| `.github/skills/afternoon-slop-gate-workflow/references/4-suggest-and-decide.md` | Changed suggestion validation from cross-pass guide checking to current-pass guide-pack checking, and narrowed `crossChecked` accordingly. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Updated the slop-gate technical reference to describe pass-local fix validation. |
| `docs/afternoon-pipeline-technical.md` | Updated the user-facing technical summary to describe pass-local fix validation instead of cross-pass validation. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The orchestrator loop is unchanged, but each slop-gate invocation is now described as a self-contained pass. A pass reads only its own guide pack and validates fixes only against that same pack.

---

## 2026-04-07 — Split slop-gate prompt into a phased workflow skill

**Problem:** The slop-gate prompt had become a dense monolith after the pass A/B split, the extra second-sweep rules, and the full output contract. The agent had to load every audit rule, every schema, and every writing instruction at once, even though each part is only needed at one moment in the run.

**Root cause:** The prompt still carried all operational detail inline instead of routing the agent through phased references. That wasted context, made pass-specific rules harder to isolate, and made future edits riskier because the same workflow concepts were spread across one oversized file.

**Changes:**

| File | Change |
|---|---|
| `.github/skills/afternoon-slop-gate-workflow/SKILL.md` | Added a router skill for the slop-gate with five phases: read workspace, build false-positive filter, audit assigned pass, suggest and decide, write artifacts. |
| `.github/skills/afternoon-slop-gate-workflow/references/1-read-workspace.md` | Moved dispatch parsing, pass locking, fresh-sweep prohibitions, output-path resolution, and target-prose loading into Phase 1. |
| `.github/skills/afternoon-slop-gate-workflow/references/2-build-false-positive-filter.md` | Moved chapter-plan priming plus character-voice, subject-matter, dialogue, and intentional-structure defenses into Phase 2. |
| `.github/skills/afternoon-slop-gate-workflow/references/3-audit-assigned-pass.md` | Moved the common per-guide audit loop, anti-laziness rules, scope rules, and notes-vs-scratchpad split into Phase 3. |
| `.github/skills/afternoon-slop-gate-workflow/references/3a-pass-a-guides.md` | Added the pass A route file covering negation, intent-smear, recurring-prose-tics, and the dedicated P5/P6 sweep. |
| `.github/skills/afternoon-slop-gate-workflow/references/3b-pass-b-guides.md` | Added the pass B route file covering gpt-5 prose issues, narrator seep, phantom concreteness, and the dedicated abstract-stand-in sweep. |
| `.github/skills/afternoon-slop-gate-workflow/references/4-suggest-and-decide.md` | Moved cross-validated suggestion rules, iteration-aware fix conservatism, and verdict aggregation into Phase 4. |
| `.github/skills/afternoon-slop-gate-workflow/references/5-write-artifacts.md` | Moved the notes JSON, scratchpad, and status output contracts into Phase 5, including the large-file-handling reminder. |
| `.github/agents/afternoon-slop-gate.agent.md` | Slimmed the agent prompt down to role, workflow mount, dispatch contract, and cross-cutting rules. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Added the slop-gate workflow skill to the pipeline reference and updated the slop-gate phase summary. |
| `docs/afternoon-pipeline-technical.md` | Noted that the slop-gate now loads its operating procedure progressively via `afternoon-slop-gate-workflow`. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** Runtime behavior is unchanged. The slop-gate still runs as a two-pass adversarial audit with pass-specific artifacts and the same verdict rules, but its operational detail now loads phase by phase, with Phase 3 routing by pass.

---

## 2026-04-07 — Split slop-gate into pass A / pass B

**Problem:** The slop-gate had accumulated too many jobs in one audit surface. It was trying to run cheap mechanical hunts, softer register judgments, and suggestion generation in one pass, which made the gate harder to calibrate and easier to overload.

**Root cause:** The original slop-gate contract treated all resources guides as one undifferentiated audit set. That mixed high-confidence sentence-local policing with slower contextual judgments, while the revision loop still assumed one feedback file and one kill trajectory.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-slop-gate.agent.md` | Split the gate into required `pass: a|b` dispatches. Pass A now owns negation / intent-smear / recurring-tics; pass B owns GPT-5 prose issues / narrator-seep / phantom-concreteness. Added pass-specific artifact naming and per-pass oscillation tracking. Clarified that the slop hitlist stays slophunter-side. |
| `.github/agents/afternoon-slophunter.agent.md` | Revision mode now requires `feedbackPathA` and `feedbackPathB`, merges both pass note sets into one worklist, and keeps the hitlist in revision self-audit after applying both. |
| `.github/agents/afternoon-orchestrator.agent.md` | Reworked slop-gate dispatch and crash recovery for two passes: initial A then B, one slophunter revision, then A and B re-audits. Loop exits only when both passes independently pass. Manifest loop state now tracks `feedbackPathA`, `feedbackPathB`, `targetFile`, `iterationKillsA`, and `iterationKillsB`. |
| `.github/skills/afternoon-pipeline/SKILL.md` | Updated the pipeline-at-a-glance summary to show `Slop-Gate A/B`. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Synced slophunter revision behavior, slop-gate reads/writes, pass ownership, hitlist ownership, and pass-specific loop tracking. |
| `.github/skills/afternoon-pipeline/references/architecture.md` | Updated the flow and artifact tree for pass A / pass B notes and scratchpads, plus split-loop crash recovery phases. |
| `.github/skills/afternoon-pipeline/references/config.md` | Clarified that `agents.slopGate.maxIterations` now counts full A+B revision cycles rather than single re-audits. |
| `.github/skills/afternoon-pipeline/references/troubleshooting.md` | Updated exhaustion and crash-recovery guidance for pass-specific note files. |
| `docs/afternoon-pipeline-architecture.md` | Documented the A/B slop-gate split and pass-specific artifacts. |
| `docs/afternoon-pipeline-technical.md` | Updated notes artifact names, status/manifest fields, and the slop-gate layer description for the split loop. |
| `docs/afternoon-pipeline-guide.md` | Updated user-facing notes file names and troubleshooting guidance for pass A / pass B. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The slop-gate is now a two-pass loop. Pass A and pass B audit the same prose independently, the slophunter fixes both note sets in one revision pass, and the orchestrator only exits the loop when both passes independently return `pass`. The slop hitlist remains enforced by the slophunter and its revision self-audit, not by a separate gate pass.

---

## 2026-04-07 — Teach slop-gate to kill phantom concreteness

**Problem:** The grounding work now teaches concretization, but the slop-gate still had no dedicated way to fail the same pattern in prose. Abstract stand-ins like `it needs to be named` or tactical-prestige summaries like `she knew that shape` could survive because they sounded sharp, and the gate's broad dialogue defense treated quoted gravitas as character voice rather than as a speech-level slop pattern.

**Root cause:** The gate relied on adjacent guides that only partially overlapped with the problem. Negation, narrator-seep, and intent-smear could catch some variants, but none of them owned the full "sounds precise without cashing out" failure mode. The slop-gate prompt also gave dialogue too much blanket protection.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-slop-gate.agent.md` | Narrowed the dialogue defense so quoted speech is no longer auto-protected when a guide explicitly audits speech-level slop. Added a dedicated phantom-concreteness sweep for dialogue-heavy scenes and tactical/inferential paragraphs. |
| `resources/phantom-concreteness-guide.md` | New adversarial guide for abstract stand-ins, sloganized dialogue, tactical-prestige compression, and unanchored interpretive summary. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Synced slop-gate responsibilities to include the dedicated phantom-concreteness sweep and dialogue non-exemption. |
| `docs/afternoon-pipeline-architecture.md` | Documented the new slop-gate hunt for lines that sound precise without naming specifics. |
| `docs/afternoon-pipeline-technical.md` | Added phantom-concreteness to the slop-gate detection surface description. |
| `docs/afternoon-pipeline-guide.md` | Clarified that slop-gate notes can now include abstract-stand-in kills in dialogue as well as narration. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The slop-gate now explicitly hunts fake specificity in both narration and quoted speech. Lines that sound sharp but cannot answer `what specifically?` or `by what sign?` from the local page are supposed to fail, even when their rhythm or diction sounds strong.

---

## 2026-04-07 — Add grounding exemplar for concretizing abstract stand-ins

**Problem:** The grounding skill was still vulnerable to a fake version of specificity: sentences that sounded sharper or more elevated than the source but still did not resolve into anything concretely legible. That taught the wrong lesson — noun enrichment without full concretization.

**Root cause:** Some exemplar material still tolerated prestige abstraction like `it needs to be named` or tactical summary language like `she knew that shape` instead of forcing the prose to cash those claims out into observable cues, object contact, or physically legible inference.

**Changes:**

| File | Change |
|---|---|
| `.github/skills/prose-grounding-framework/SKILL.md` | Added an explicit rule that grounding must not replace vague prose with sharper-sounding vagueness. |
| `.github/skills/prose-grounding-framework/references/after-4.md` | Revised the exemplar so the breach sequence is concretized through ward locks, the dogleg, and Sylvanas's recognizable movement pattern instead of abstract tactical summary language. |
| `.github/skills/prose-grounding-framework/references/before-5.md` | New exemplar source passage showing abstract stand-in dialogue and narration. |
| `.github/skills/prose-grounding-framework/references/after-5.md` | New exemplar rewrite showing how to concretize abstract rhetorical language through desk contact, visible evidence, and plain claim vocabulary. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The grounding framework now teaches a stricter lesson: grounding is not just adding names or heavier diction. It must also convert fuzzy abstraction into something the POV can actually perceive, follow, or materially infer.

---

## 2026-04-07 — Tighten grounding-gate leniency on dialogue and tail drift

**Problem:** A real audit on `chapter12/final-grounded-gpt-negative-v3.md` passed clean even though the middle scholar-duel still had under-embodied dialogue and the ending still showed generic late fallback relative to the stronger v2 tail benchmark.

**Root cause:** The grounding-gate contract let a few strong local carrier beats stand in for whole dialogue runs. It was too easy for the gate to cherry-pick KEEP moments, assume a clean pass early, and treat readable route logic in the final third as proof that tail attenuation was gone.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-grounding-gate.agent.md` | Added anti-leniency rules: no pre-committing pass, no letting one or two carrier beats immunize a long conceptual run, and no treating route legibility alone as enough in the tail. Tightened pass/fail logic accordingly. |
| `.github/skills/prose-grounding-audit/references/dialogue-grounding.md` | Clarified that embodiment must recur inside long dialogue runs and that the featureless-room test applies to the whole run, not a cherry-picked line. |
| `.github/skills/prose-grounding-audit/references/distribution-and-tail-audit.md` | Clarified that tail drift can show up as readable motion plus generic late carriers, and that rhythm protection does not excuse thinning specificity. |
| `.github/skills/prose-grounding-audit/references/benchmark-deltas.md` | Corrected the Chapter 12 benchmark lesson so v3 remains the process benchmark while v2 remains the stronger tail-enrichment benchmark. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Updated the gate contract summary to reflect the stricter anti-leniency behavior. |
| `docs/afternoon-pipeline-architecture.md` | Updated the public grounding-gate description to reflect the stricter reading of long conceptual runs and late generic fallback. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** The gate is still best-effort and schema-compatible, but it is now harder for it to pass a chapter just because a few good moments exist. Long conceptual runs need distributed embodiment, and readable tail motion no longer excuses generic late carriers.

---

## 2026-04-07 — Remove grounder chunking support

**Problem:** The grounder still carried chunked-mode language, dead config fields, and audit references even after the prompt direction had been simplified. That left the repo advertising a feature the live grounder was no longer supposed to use.

**Root cause:** We had stripped parts of the chunking workflow from the prompt surface, but not the surrounding reference surfaces. The agent, audit skill, config docs, and public docs still described chunked grounding as a supported path.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-grounder.agent.md` | Removed chunked-mode instructions and examples. The grounder now has one scene-by-scene grounding flow. |
| `.github/agents/afternoon-grounding-gate.agent.md` | Removed the chunking-playbook read from the gate startup sequence. |
| `.github/skills/prose-grounding-audit/SKILL.md` | Removed chunking-playbook from the audit skill read order and file list. |
| `.github/skills/prose-grounding-audit/references/chunking-playbook.md` | Removed. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Removed grounder chunking behavior and chunking config references. |
| `.github/skills/afternoon-pipeline/references/config.md` | Removed `agents.grounder.chunking.*` from the config schema example and field reference. |
| `docs/afternoon-pipeline-architecture.md` | Removed chunked-mode wording from the grounder description. |
| `docs/afternoon-pipeline-technical.md` | Removed `agents.grounder.chunking.*` from the public config schema example and field table. |
| `docs/afternoon-pipeline-guide.md` | Removed the grounder chunking option from the user-facing config guide. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry and removed stale chunking references from older entries. |

**Behavioral summary:** The grounder still builds a grounding map, grounds scene by scene, runs dialogue grounding, and audits the final third. It no longer exposes a separate chunked mode or chunking thresholds.

---

## 2026-04-07 — Split grounding framework from grounding audit

**Problem:** The `prose-grounding-framework` skill had started doing two jobs at once: teaching the grounder by exemplar and carrying the grounding-gate's audit packets. That made the framework fatter than necessary and left the gate mounted to the wrong skill surface.

**Root cause:** Verifier-facing files (`failure-taxonomy`, `dialogue-grounding`, `distribution-and-tail-audit`, `benchmark-deltas`) had accumulated inside the grounder's exemplar skill instead of living in a dedicated audit skill.

**Changes:**

| File | Change |
|---|---|
| `.github/skills/prose-grounding-framework/SKILL.md` | Simplified back to an exemplar-only grounding skill. Kept the before/after workflow and concise grounding principles; removed the audit-packet router. |
| `.github/skills/prose-grounding-audit/SKILL.md` | New skill. Owns the audit packets for the grounding-gate and defines a minimal read order for audit passes. |
| `.github/skills/prose-grounding-audit/references/failure-taxonomy.md` | Moved here from `prose-grounding-framework`. |
| `.github/skills/prose-grounding-audit/references/dialogue-grounding.md` | Moved here from `prose-grounding-framework`. |
| `.github/skills/prose-grounding-audit/references/distribution-and-tail-audit.md` | Moved here from `prose-grounding-framework`. |
| `.github/skills/prose-grounding-audit/references/benchmark-deltas.md` | Moved here from `prose-grounding-framework`. |
| `.github/agents/afternoon-grounder.agent.md` | Updated startup instructions so the grounder uses `prose-grounding-framework` as an exemplar library only. |
| `.github/agents/afternoon-grounding-gate.agent.md` | Mounted the new `prose-grounding-audit` skill and updated the audit reference paths. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Updated the grounder/gate contract docs to reflect the split between exemplar skill and audit skill. |
| `docs/afternoon-pipeline-architecture.md` | Updated the public architecture description so the grounder uses exemplar pairs and the grounding-gate uses the dedicated audit skill. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**Behavioral summary:** No pipeline routing changed. The split is about skill ownership only: the grounder keeps the exemplar skill, and the grounding-gate now owns the audit skill.

---

## 2026-04-06 — Grounding map + grounding gate overhaul

**Problem:** The grounding pass improved noun specificity but still let floaty prose survive, especially in dialogue-heavy scenes and the final third of longer chapters. The pipeline had no adversarial grounding check comparable to the slop-gate, so weak grounding could slide downstream as long as the grounder produced *something*. Documentation also still described the old straight-through flow.

**Root cause:** The old grounder contract was too monolithic and under-instrumented. It had no required scene map, no explicit dialogue-grounding pass, no final-third audit, and no independent verifier re-sweeping the prose from plan + source context. That made late-chapter drift and contactless dialogue easy to miss, and it left the pipeline without a shared grounding failure vocabulary.

**Changes:**

| File | Change |
|---|---|
| `.github/agents/afternoon-grounder.agent.md` | Replaced the old grounder contract with a map-first design: writes `grounding-map.json`, grounds scene-by-scene, runs a dedicated dialogue pass, audits the final third separately, and supports revision mode with `feedbackPath` + `targetFile`. |
| `.github/agents/afternoon-grounding-gate.agent.md` | New adversarial verifier inserted after grounding. Fresh-sweeps `v2g.md` against the shared grounding evaluation surface, emits pass/fail, and writes local `suggestedFix` values for grounder revision mode. |
| `.github/agents/afternoon-orchestrator.agent.md` | Added the grounding-gate dispatch step and revision loop, grounded crash-recovery state in `groundingGateLoop`, clarified grounder degradation semantics, and fixed canonical promotion so `v2g-rN.md`, `grounding-map-rN.json`, and `grounder-revision-rN-notes.json` promote together. |
| `.github/skills/prose-grounding-framework/SKILL.md` | Expanded the grounding skill from exemplar-only routing into a packetized framework that always loads failure taxonomy and can route dialogue grounding, tail audit, and benchmark calibration refs. |
| `.github/skills/prose-grounding-audit/references/failure-taxonomy.md` | New shared grounding dimensions / failure classes (`D1`-`D7`, `G1`-`G12`) used by both the grounder and grounding-gate. |
| `.github/skills/prose-grounding-audit/references/dialogue-grounding.md` | New runtime packet for embodied dialogue grounding and anti-float beats. |
| `.github/skills/prose-grounding-audit/references/distribution-and-tail-audit.md` | New runtime packet for distribution checks and final-third/tail attenuation audit. |
| `.github/skills/prose-grounding-audit/references/benchmark-deltas.md` | New calibration packet capturing chapter12/chapter14 benchmark lessons on restraint vs richness. |
| `.github/skills/afternoon-pipeline/SKILL.md` | Updated the at-a-glance pipeline summary to include grounding-gate and corrected stale slophunter hunt counts. |
| `.github/skills/afternoon-pipeline/references/agents.md` | Updated orchestrator routing contract, expanded the grounder section, added a full grounding-gate section, and clarified expander input after gate promotion. |
| `.github/skills/afternoon-pipeline/references/architecture.md` | Updated the flow diagram, artifact/versioning model, directory layout, data-flow diagram, dispatch exceptions, and crash-recovery notes for the new gate loop. |
| `.github/skills/afternoon-pipeline/references/config.md` | Added `agents.groundingGate.enabled` and `agents.groundingGate.maxIterations`; aligned slop-gate/grounder semantics with best-effort continuation. |
| `.github/skills/afternoon-pipeline/references/running.md` | Updated expected artifacts and runtime notes for grounding-map / grounding-gate outputs. |
| `.github/skills/afternoon-pipeline/references/troubleshooting.md` | Added grounding-gate exhaustion, crash-recovery, and promotion guidance; updated grounder degradation/reset instructions and directory reset commands. |
| `.github/skills/afternoon-pipeline/references/adding-agents.md` | Added new insertion-point guidance around the grounding-gate slot. |
| `docs/afternoon-pipeline-architecture.md` | Updated the public architecture doc to describe the new grounding stage, optional grounding verifier, revised artifact layout, and crash-recovery semantics. |
| `docs/afternoon-pipeline-technical.md` | Updated public config schema, notes/status/manifest formats, and dispatch protocol for the grounding revision loop. |
| `docs/afternoon-pipeline-guide.md` | Updated setup/config/running/output/troubleshooting guidance for the optional grounding-gate. |
| `docs/afternoon-pipeline-changelog.md` | Added this entry. |

**New config fields:** `agents.groundingGate.enabled` (default `false`), `agents.groundingGate.maxIterations` (default `3`).

**Behavioral summary:** After the slop-gate passes (or exhausts), the pipeline now runs Grounder → optional Grounding-Gate → Expander. If the grounder fails operationally, the orchestrator degrades gracefully (`v2.md` copied to `v2g.md`) and skips the grounding-gate. If the grounding-gate exhausts its loop, the latest grounded revision is promoted and the pipeline continues.

---

## 2026-07-14 — Grounder redesigned: exemplar-based, no category taxonomy

**Problem:** The grounder agent produced minimal noun-swapping output (4 replacements, 0.4% growth) instead of the immersive world-enrichment expected. Root cause: the prompt's "replace, don't pad" rule (stated 3x), "same grammatical slot" constraint, "no new sentences" ban, and ≤25% growth cap combined to define grounding as find-and-replace when the actual job is full-immersion enrichment across every prose surface.

**Solution:** Replaced the 5-category diagnostic taxonomy with an exemplar-based approach. The grounder now learns what grounding means by studying a before/after chapter pair, then applies the same transformation by feel — not by following a category checklist.

**Changes:**

| File | Change |
|---|---|
| `afternoon-grounder.agent.md` | Removed "replace, don't pad" framing. Removed all 5-category references and per-category todolist passes (9 todos → 4 todos). Replaced with: read exemplar → ground by vibes → self-audit → write. Raised wordcount target from ≤25% to 40-70%. Added self-audit check #8: compare density against exemplar. |
| `.github/skills/prose-grounding-framework/SKILL.md` | Stripped category routing table, diagnostic questions, diagnosis table, scoping rules. Replaced with: read `references/before-grounding.md` and `references/after-grounding.md`, study the diff, apply the same transformation. Kept 4 universal principles (weave/POV/source/over-ground). |
| `.github/skills/prose-grounding-framework/references/before-grounding.md` | New file — ungrounded chapter (Chapter 14, 2168 words). |
| `.github/skills/prose-grounding-framework/references/after-grounding.md` | New file — same chapter after grounding (3699 words, 70% growth). |

**Category reference files removed:** The 5 category packets (`1-spatial-reality.md` through `5-cultural-voice.md`) are no longer in the references directory and are no longer referenced by the grounder agent or SKILL.md.

---

## 2026-04-06 — Grounder agent added to pipeline

**New agent:** `afternoon-grounder` — world-specificity grounding agent that reads clean `v2.md` and replaces vague placeholders with world-specific proper nouns, named systems, factions, mechanics, materials, and cultural voice. Produces `v2g.md`. Slots between the slop-gate loop and the expander.

**New skill:** `.github/skills/prose-grounding-framework/` — craft methodology for the grounder (SKILL.md + 5 reference files covering spatial, societal, mechanics, material, and cultural grounding categories).

**Changes:**

| File | Change |
|---|---|
| `afternoon-grounder.agent.md` | New agent file (gpt-5.4). Mounts `prose-grounding-framework` skill, diagnoses 2-3 of 5 grounding categories per chapter, sources all proper nouns from memory/materials/plan, self-audits against anti-slop hitlist, soft ≤25% wordcount growth cap. |
| `afternoon-orchestrator.agent.md` | New section 6 (Grounder Dispatch) between slop-gate (section 5) and expander (now section 7). Sections renumbered through 11. Grounder disabled: `cp v2.md v2g.md`. Grounder failure: graceful degradation (`cp v2.md v2g.md`), does NOT block chapter. Expander disabled: now `cp v2g.md v3.md` (was `cp v2.md v3.md`). |
| `afternoon-expander.agent.md` | Now reads `v2g.md` instead of `v2.md`. |
| Skill ref `agents.md` | New Grounder section. Updated orchestrator dispatch order and kill switch descriptions. Updated Expander reads and kill switch. |
| Skill ref `architecture.md` | Updated agent flow (12 agents), artifact versioning (v2g.md row), directory layout (v2g.md + grounder-notes.json), data flow diagram. |
| Skill ref `troubleshooting.md` | Added grounder failure/degradation scenarios. Updated reset commands. |
| Skill ref `adding-agents.md` | Updated insertion points table. |
| Skill `SKILL.md` | Updated agent count (11→12), pipeline diagram, numbering. |
| `docs/afternoon-pipeline-architecture.md` | Updated agent count, flow diagram, agent roles, artifact versioning, directory layout, data flow, design decisions. |
| `docs/afternoon-pipeline-technical.md` | Updated config schema (grounder.enabled), config example, editor notes table. |
| `docs/afternoon-pipeline-guide.md` | Updated agent count, dispatch order, draft progression, editor notes, config options, workflows. |
| `copilot-instructions.md` | Updated agent flow diagram, agents table, artifact versioning, key differences. |

**Key artifact invariant:** After the grounder section completes (regardless of path), both `v2.md` and `v2g.md` always exist. All downstream agents read `v2g.md` or later — never `v2.md` directly. Pipeline now dispatches up to 12 agents per chapter (was 11).

**Config:** `agents.grounder.enabled` (default `true`). Set to `false` to skip grounding entirely.

---

## 2026-04-05 — Slop-gate pass threshold + slophunter vocabulary diversity

**Problem:** Chapter 14 convergence data showed the zero-tolerance pass threshold (0 kills required) was too strict — chapters reaching 3 borderline MILD kills still failed, triggering loop exhaustion after 5 iterations. Additionally, the slophunter's revision mode defaulted to eye/gaze beats as replacement vocabulary, causing a Tic 5 explosion (0→6 kills) that wasted a full iteration.

**Changes:**

| File | Change |
|---|---|
| `afternoon-slop-gate.agent.md` | Severity-aware pass threshold: ≤3 MILD-only kills = pass-with-warnings. Any MODERATE/SEVERE kill still = fail. Added `mildKills` / `moderateOrSevereKills` to notes JSON summary and `mildFindings` to status.json. |
| `afternoon-slophunter.agent.md` | Added vocabulary diversity constraint to revision mode: must not default to eye/gaze beats as replacement anchors. Prefer action, body position, sound, environmental detail. |
| Skill ref `agents.md` | Updated gate verdict logic description and slophunter revision mode behavior. |

**Impact:** Chapters converging to ≤3 MILD borderline findings will now pass instead of exhausting the loop. Slophunter revisions should produce fewer tic regressions.

---

## 2026-04-05 — Resource guide improvements (research-driven)

**Problem:** The 5 resource guides in `./resources/` had gaps identified through web research against current AI prose detection literature, stylometry, and fiction craft criticism.

**Changes:**

| File | Change |
|---|---|
| `gpt-5-prose-issues.md` | Added **temporal padding** sub-section to F3 — 13 time-padding phrases (`for a long moment`, `in that moment`, etc.) with deletion test. Updated stacking rule and verdict logic. |
| `intent-smear-agency-laundering-guide.md` | Added **Pattern 8: Body-part personification** and **Pattern 9: Nominalized verbs given agency**. Updated output format to Patterns 1-9. Added 4 calibration examples. |
| `narrator-seep-guide.md` | Added **psychic distance** diagnostic section (Gardner 5-level zoom). Added **A7: Generalizing constructions** as Tier A pattern with trigger phrase list. Updated references to A1-A7. Added 3 calibration examples. |
| `recurring-prose-tics.md` | Added **Tic 5: Eye/gaze repertoire exhaustion** (cap 4/ch), **Tic 6: Weight/heaviness emotional metaphor** (cap 2/ch), **Tic 7: Dialogue tag avoidance of "said"** (cap 3/ch). Updated self-check. |
| `negation-addiction-hunting-guide.md` | No changes — guide already comprehensive. |

**Impact:** All agents that read `./resources/` files (slop-gate, slophunter, writer anti-slop priming) now have broader detection surface. No agent file changes required — the resource files are consumed dynamically.

---

## 2026-04-05 — Convergence fixes for slop-gate revision loop

**Problem:** The gate/slophunter revision loop oscillated instead of converging. Kill counts across 6 iterations: 43 → 21 → 17 → 25 → 17 → 28. ~98% of findings each iteration were brand new — the slophunter fixed what was flagged but its rewrites introduced fresh violations. The gate's own suggested fixes were getting re-flagged in subsequent iterations (e.g., an F4 fix introduced P5, a P5 fix introduced negation).

**Root causes:**
1. Gate cross-checked suggestedFix only against co-triggered guides (guides that flagged the same passage), not all guides. A fix that cleared F4 could introduce P5 undetected.
2. Slophunter revision mode skipped all anti-slop self-audit — it applied gate suggestions but never checked its own rewrites for new violations.
3. No feedback signal — the gate wrote identical-quality fixes regardless of iteration count, even when the loop was clearly oscillating.

**Changes:**

| File | Change |
|---|---|
| `afternoon-slop-gate.agent.md` | **Full cross-check**: every suggestedFix now validated against ALL audit guides, not just co-triggered ones. `crossChecked` array now contains all guides. |
| `afternoon-slop-gate.agent.md` | **Iteration-aware fix conservatism**: gate reads `manifest.slopGateLoop.iterationKills` during suggestion phase. When kills plateau or increase, switches to conservative strategy (prefer deletion over rewrite, minimal word substitution, shorter fixes, lower unfixable threshold at 2 attempts instead of 3). Does not affect detection strictness — only fix strategy. |
| `afternoon-slop-gate.agent.md` | **`totalFindings` in status.json**: added structured field so orchestrator can read kill counts without parsing the notes JSON. |
| `afternoon-slophunter.agent.md` | **Rewrite self-audit**: new step 4 in revision mode workflow. After applying all gate suggestions, re-reads changed passages against anti-slop resources (hitlist, intent-smear, narrator-seep, negation guides). Catches violations introduced by rewrites before writing output. Logged with `source: "self-audit"` in revision notes. |
| `afternoon-orchestrator.agent.md` | **`iterationKills` tracking**: orchestrator reads `totalFindings` from gate status.json, populates `slopGateLoop.iterationKills` array in manifest. Initialized on first fail, appended after each re-audit. |
| `references/agents.md` | Updated slop-gate suggestion phase, crossChecked description, status.json schema, slophunter revision mode todos and behavior. |
| `docs/afternoon-pipeline-architecture.md` | Updated gate and slophunter descriptions. |
| `docs/afternoon-pipeline-technical.md` | Updated feedback loop description. |

---

## 2026-04-05 — Gate loop exhaustion: continue instead of halt

**Problem:** Pipeline halted entirely when the gate failed after `maxIterations` iterations, printing `===AFTERNOON DONE===`.

**Change:** Loop exhaustion now promotes the latest revision to `v2.md` and continues the pipeline. Logs `slopGateExhausted` warning in manifest. Downstream agents (style-editor, style-auditor, final-slophunter) catch remaining issues.

| File | Change |
|---|---|
| `afternoon-orchestrator.agent.md` | Loop exhaustion: promote + continue instead of halt |
| `references/troubleshooting.md` | Updated "Slop-gate fails after max iterations" section |
| `references/agents.md` | Updated loop description |

---

## 2026-04-05 — Gate quality improvements

**Problem:** False positive rate at ~28% (7/25 in chapter 13 iter 3). Three systematic issues: F1 misapplication to fragment pairs, character-voice filter too weak on internal monologue, gate's own suggested fixes sometimes worse than originals.

**Changes:**

| File | Change |
|---|---|
| `resources/gpt-5-prose-issues.md` | **F1 rewrite**: scope changed from page-level to chapter-level sustained stretches. Added "What is NOT F1" section with exact false-positive examples. Severity thresholds changed to paragraph-stretch measurement. |
| `afternoon-slop-gate.agent.md` | **Character-voice defense expansion**: 4 specific sub-cases that MUST be defended — internal monologue fragments, tactical/strategic compression, concrete observations mislabeled as mood, deliberate fragment pairs for cataloging. |

---

## 2026-04-05 — Fresh-sweep rule for re-audits

**Problem:** Risk of anchoring bias when gate re-audits revised prose — could unconsciously look for the same patterns it flagged before.

**Changes:**

| File | Change |
|---|---|
| `afternoon-slop-gate.agent.md` | Added "Every Audit Is a Fresh Sweep" core rule — explicit zero-memory policy. Added startup step 4 — file-level prohibition against reading any prior gate/revision artifacts. |

---

## 2026-04-05 — Initial slop-gate implementation

**New agent:** `afternoon-slop-gate` — adversarial verification gate that audits slophunter output against every guide in `resources/`. Emits pass/fail verdict. On fail, orchestrator enters revision loop re-dispatching slophunter with gate's pre-validated suggested fixes.

| File | Change |
|---|---|
| `afternoon-slop-gate.agent.md` | New agent file (claude-opus-4.6) |
| `afternoon-orchestrator.agent.md` | Section 5: gate dispatch + revision loop. Crash recovery for slopGateLoop state. |
| `afternoon-slophunter.agent.md` | Revision mode: feedback-driven fixes, zero wordcount reduction |
| `.afternoon/config.json` | `agents.slopGate` section with `enabled` and `maxIterations` fields |
| `references/agents.md` | Gate contract documentation |
| `references/architecture.md` | Data flow and directory layout updates |
| `references/config.md` | slopGate config fields |
| `references/troubleshooting.md` | Gate failure scenarios |
| `docs/afternoon-pipeline-architecture.md` | Gate in pipeline overview |
| `docs/afternoon-pipeline-technical.md` | Gate in artifact and flow docs |
| `docs/afternoon-pipeline-guide.md` | Gate in user guide |
| `copilot-instructions.md` | Pipeline summary updated |
| `resources/gpt-5-prose-issues.md` | FLAG→KILL standardization |
| `resources/narrator-seep-guide.md` | FLAG→KILL standardization |
