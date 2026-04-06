# Afternoon Pipeline Changelog

New entries are appended at the top.

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
