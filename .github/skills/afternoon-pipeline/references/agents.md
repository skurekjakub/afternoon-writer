# Agent Contracts

Each agent has a file at `.github/agents/afternoon-{name}.agent.md`. This reference covers what each agent reads, writes, and does — the contracts that must stay consistent when editing any agent.

---

## Orchestrator (`afternoon-orchestrator`)

**File:** `.github/agents/afternoon-orchestrator.agent.md`

**Reads:** config.json (once), manifest.json, status.json files only
**Writes:** manifest.json, final.md (via `cp`)
**Tools:** bash (only `mkdir -p` and `cp`)
**Isolation:** Never reads prose, plans, beats, memory, or notes. Pure router.

**Bootstrap gate:** Reads `storyOverview` field from config.json. If missing, empty, or file doesn't exist → prints fatal error and exits. No chapters processed without a story overview.

**Dispatch order:** planner → plan-verifier → writer → slophunter → slop-gate [↔ slophunter revision loop] → grounder → expander → style-editor → style-auditor → final-slophunter → memory-keeper

**Dispatch mode:** All dispatches are synchronous. Never background mode. Never poll. Never sleep. Dispatch → wait for return → read status.json → route.

**Key constraints:**
- Between dispatches: does NOTHING (no read_agent, no sleep, no polling, no extra file reads)
- Skip logic: checks status.json, not output file existence
- Crash recovery: uses status.json signals, not file existence
- Assembly: `cp v5.md final.md` (bash, not read-then-write)
- Every slop-gate exit (pass, loop-pass, loop-exhaustion, disabled) routes to Grounder, never to Expander directly
- Grounder kill switch: if `config.agents.grounder.enabled` is false, does `cp v2.md v2g.md` and skips grounder dispatch
- Grounder failure: graceful degradation — on failure after retry, does `cp v2.md v2g.md` and proceeds (does NOT block chapter)
- Expander kill switch: if `config.agents.expander.enabled` is false, does `cp v2g.md v3.md` and skips expander dispatch
- Slop-gate revision loop: on fail verdict, alternates slophunter-revision → gate-reaudit up to maxIterations. On pass, promotes v2-rN.md → v2.md and revision notes → slophunter-notes.json. On exhaustion, promotes latest revision and continues — does NOT halt.
- Style-auditor skip: if `.afternoon/style-guide.json` doesn't exist, style-auditor reports `"status": "failed"` — orchestrator treats as skip (proceed to final slophunter), not block

---

## Planner (`afternoon-planner`)

**File:** `.github/agents/afternoon-planner.agent.md`

**Reads:**
- config.json
- Story overview from config → `storyOverview` (the full arc — where this chapter fits)
- `plans/series-meta.md` (cross-invocation planning notes — if it exists)
- outlines/{chapterId}.md (full normalized chapter outline: header, meta info, knowledge ledger, arc position, cast/handoff rules, scenes, beats)
- Character voice sheets from config → characters.voiceSheets
- All files from config → materials

**Does NOT read:** Memory files. Continuity is Scheherazade's (plan-verifier's) domain.

**Writes:**
- plans/{chapterId}-initial.json (validated/enriched plan aligned with the normalized outline scaffold — NO continuity or chapterBridge fields yet)
- agents/planner/status.json
- Appends to `plans/series-meta.md` (chapter summary, key beats, threads opened/advanced, structural notes, enrichments of note, suggestions for next chapter)

**Todos:** Read inputs → Validation pass → Enrichment pass → Write output → Update series meta

**Key responsibilities:**
- Validates the chapter scaffold (`metaInfo`, knowledge ledger, `arcPosition`, `castAndHandoffRules`) before beat-level checks
- Validates beat structure (scene-sequel alternation, value shifts, scene-outcome mix, chapter opening/closing)
- Preserves scene-level `sceneFunction`, `castInScene`, `knowledgeAtSceneStart`, optional `arcPressure`, and `enrichment`
- Preserves beat-level `transitionIntent` plus any load-bearing `dialogueGuidance`, `disclosureProvenance`, and `plantedThread`
- Internet-enriches character, location, and cultural details; keeps `sensoryAnchors` at the beat level
- Enforces writer freedom: no pre-written dialogue, no half-written prose in summaries, no prose directives
- Does NOT produce: `continuityStatus`, `memoryRef`, `requiredMemory`, `chapterBridge` — all belong to verifier

---

## Plan-Verifier (`afternoon-plan-verifier`)

**File:** `.github/agents/afternoon-plan-verifier.agent.md`

**Reads:**
- config.json
- Story overview from config → `storyOverview` (the full arc — where this chapter fits in the thousand nights)
- `plans/series-meta.md` (cross-invocation planning notes — if it exists)
- plans/{chapterId}-initial.json (planner's output — structure + enrichment, no continuity/transitions)
- outlines/{chapterId}.md (original user beats)
- ALL memory `_index.json` files from plans/memory/ (chapter 2+ only), plus individual entity files as needed
- Character voice sheets, style target

**Writes:**
- plans/{chapterId}.json (final plan with ALL fields — downstream agents read this)
- agents/plan-verifier/status.json
- Appends to `plans/series-meta.md` (verdict, craft research, structural modifications, continuity snapshot, active threads, chapter-end stance / carry-forward residue, chapter bridge summary, warnings for next chapter)

**Todos:** Read inputs → Genre research → Structural evaluation → Character evaluation → Continuity annotation → Transition bridge writing → Modifications → Write output → Update series meta

**Key responsibilities:**
- Internet-searches genre conventions, collects 3-5 craft principles
- Evaluates pacing, tension curve, scene-sequel balance, opening/closing strength
- Checks POV consistency, character agency, supporting character distinction
- Audits `arcPosition` against the beats: current stance, pressure source, chapter test, forced choice, end-state shift, and carry-forward residue must all be earned on-page
- **Continuity annotation (PRODUCES, not audits):** Annotates every beat with `continuityStatus` ("new"/"callback"/"evolution"), adds `memoryRef` to callbacks/evolutions, collects top-level `requiredMemory`, runs contradiction and anti-reintroduction checks against memory files
- **Transition verification:** Verifies beat-level `transitionIntent` (coverage, type, coherence), checks scene-boundary carries, writes `chapterBridge` for chapter 2+, checks location/emotional continuity
- **Verifier notes are continuity-only:** No prose directives — no "Writer: open on X" or "the toast is a character beat." Only continuity warnings ("don't re-introduce X", "character doesn't know this name yet")
- **Expansion depth annotation:** Annotates every beat with `expansionLevel` ("high"/"medium"/"low") based on scene type and emotional weight — skipped if expander disabled in config
- Has structural modification authority (beat reorder, scene grouping, beat add/remove, bridge revision after reshaping)
- Cannot change: core plot events, character decisions, voice/personality, new characters/locations, prose-level decisions (how to open, which image to lead with)
- Verdicts: "approved" / "approved-with-modifications" / "flagged"

---

## Writer (`afternoon-writer`)

**File:** `.github/agents/afternoon-writer.agent.md` (134 lines)

**Reads (in this order — the proven priming recipe):**
1. Story overview from config → `storyOverview` (the whole story's arc and destination)
2. All files/directories from config → `priming.antiSlop` (slop-hitlist, ai-quirks, editor-guide)
3. All files from config → `priming.craft` (author-technique-anchors, chapter-focus-points)
4. Style target from config → `priming.styleTarget`
5. Voice sheets from config → `characters.voiceSheets`
6. Materials from config → `materials`
7. Prior chapter's final.md (chapter 2+)
8. plans/{chapterId}.json (the verified plan)
9. Targeted memory `.json` files from plan's `requiredMemory` (chapter 2+) — JSON only, not `.md`

**Writes:**
- chapters/{chapterId}/v1.md
- agents/writer/status.json

**Todos:** Research keywords → Prime context → Write all scenes → Self-audit → Write output

**Key responsibilities:**
- Reads the verified plan from scaffold → scenes → beats and treats it as a pressure map, not as a prose template
- Uses `continuityStatus` to control detail level:
  - "new" → full sensory detail (first encounter)
  - "callback" → brief anchoring reference (single-detail, familiarity shorthand, or drop)
  - "evolution" → build on established foundation, reference then expand
- Hard rules: never re-describe appearance as first-time, never re-reveal known abilities, never reset shifted relationships, never re-explain world facts
- Self-audits hitlist item counts before delivery

---

## Slophunter (`afternoon-slophunter`)

**File:** `.github/agents/afternoon-slophunter.agent.md` (171 lines)

**Reads:**
- config.json
- Story overview from config → `storyOverview` (story context for replacement choices)
- All files/directories from config → `priming.antiSlop` (slop-hitlist, ai-quirks, editor-guide)
- Style target from config → `priming.styleTarget`
- chapters/{chapterId}/v1.md

**Writes:**
- chapters/{chapterId}/v2.md (primary), v5.md (polish), or v2-r{N}.md (revision)
- chapters/{chapterId}/slophunter-notes.json (primary), final-slophunter-notes.json (polish), or slophunter-revision-r{N}-notes.json (revision)
- agents/slophunter/status.json (primary/revision) or agents/final-slophunter/status.json (polish)

**Todos:** Read weapons + target → Research keywords → Hunt 0-10 → Write output (primary/polish) | Read feedback → Apply gate suggestions → Rewrite self-audit → Write output (revision)

**Revision mode behavior:** Reads slop-gate's notes JSON containing KILL findings with `suggestedFix` fields. Applies suggestions with latitude for voice/flow adjustment but preserves the structural fix. For findings where `suggestedFix` is `null` (unfixable), attempts own fix or marks unfixable. After applying all fixes, performs a **rewrite self-audit** — re-reads changed passages against anti-slop resources to catch violations introduced by the rewrites themselves. Self-audit fixes logged with `source: "self-audit"`. Each revision change logged with `source: "gate-suggestion"|"gate-suggestion-adjusted"|"self-authored"|"self-audit"` in the notes JSON. **Vocabulary diversity constraint**: must not default to eye/gaze beats ("looked," "eyes," "gaze") as replacement anchors — prefer action, body position, sound, or environmental detail to avoid pushing Tic 5 over cap.

**11 targeted hunts:**
0. Wordcount reduction (over-explanation, restated observations)
1. Hard caps (as-if, pressed, nodded, sighed, smiled, glanced, something)
2. All 38 hitlist items
3. Telegram prose (3+ consecutive short sentences)
4. Opener tics (2+ paragraphs starting with same word)
5. Filter words (she noticed/felt/saw/heard — max 3 per chapter)
6. Image repetition (identical image/verb within 500 words)
7. Which-meant syndrome (which meant/told/confirmed — max 3)
8. Essay paragraphs (thesis→support→restatement structure)
9. Biography insertions (mid-scene character history)
10. Beat transitions (kill temporal connectors)

**Notes JSON schema:** counts (before/after/caps), changes array, flags, flaggedForExpander (underwritten scenes spotted during hunts), wordCount

---

## Slop-Gate (`afternoon-slop-gate`)

**File:** `.github/agents/afternoon-slop-gate.agent.md`

**Reads:**
- config.json
- All `.md` files in `resources/` directory (dynamic discovery, alphabetical order)
- chapters/{chapterId}/v2.md (or v2-r{N}.md on re-audit)
- plans/{chapterId}.json or plans/{chapterId}-initial.json (for POV character voice and subject-matter priming)

**Writes:**
- chapters/{chapterId}/slop-gate-notes.json (pipeline artifact — KILL findings only, per-guide sections with `suggestedFix`)
- chapters/{chapterId}/slop-gate-notes-r{N}.json (re-audit on iteration N — same format, against v2-r{N}.md)
- chapters/{chapterId}/slop-gate-scratchpad.md (human-audit artifact — all KEEP decisions with reasoning, never read by pipeline)
- chapters/{chapterId}/slop-gate-scratchpad-r{N}.md (re-audit scratchpad)
- agents/slop-gate/status.json (with verdict field)

**Todos:** Read inputs → one audit todo per resource guide (dynamic) → Suggestion phase (cross-validated rewrites) → Aggregate and write status

**Key responsibilities:**
- Dynamically discovers all `.md` files in `resources/` and creates one audit todo per file
- For each guide: reads detection procedures and applies them faithfully to the prose
- Emits KILL/KEEP per finding according to each guide's own criteria. KILL findings go to the notes JSON (pipeline artifact). KEEP findings go to the scratchpad markdown (human-audit artifact).
- **Severity-aware pass threshold**: zero MODERATE/SEVERE kills required for pass. Up to 3 MILD-only kills still pass (pass-with-warnings). Any MODERATE/SEVERE kill or >3 MILD kills = fail verdict.
- **Suggestion phase**: For every KILL, writes a concrete `suggestedFix` (replacement text) and cross-checks it against ALL audit guides (not just guides that flagged the same passage). Marks `suggestedFix: null` with `fixDifficulty: "high"` if no clean rewrite found. Uses iteration-aware conservatism: when prior kill counts show oscillation (from `manifest.slopGateLoop.iterationKills`), switches to conservative fix strategy (prefer deletion, minimal substitution, shorter fixes, lower unfixable threshold).
- Each KILL finding includes `suggestedFix` (string or null), `fixDifficulty` (`"low"` or `"high"`), and `crossChecked` (array of all guide filenames validated against)
- Guides with zero KILLs include a `cleanReason` field in the notes JSON explaining what was checked and why nothing triggered
- Summary includes `killsWithFix` and `killsUnfixable` counts
- **Dedicated P5/P6 sweep** for the intent-smear guide: after normal detection, performs a second targeted pass for subtle anthropomorphism (objects/geography with agency verbs, abstract states settling into body parts, metaphor chains across consecutive sentences)
- Writes accumulating `slop-gate-notes.json` with per-guide sections (crash-resumable)
- Final status.json uses `status: "completed"` + `verdict: "pass"|"fail"` + `totalFindings: N` + `mildFindings: N` (not `status: "failed"` for audit failure). Summary includes `mildKills` and `moderateOrSevereKills` counts. Orchestrator reads `totalFindings` to populate `slopGateLoop.iterationKills`.
- Does NOT edit prose — audits and suggests, but the slophunter applies the fixes

**Config:** `agents.slopGate.enabled` (default true), `agents.slopGate.maxIterations` (default 5)

---

## Grounder (`afternoon-grounder`)

**File:** `.github/agents/afternoon-grounder.agent.md`

**Reads:**
- config.json
- Grounding framework skill (`.github/skills/prose-grounding-framework/`)
- All files/directories from config → `priming.antiSlop`
- Style target from config → `priming.styleTarget`
- Voice sheets from config → `characters.voiceSheets`
- Story overview from config → `storyOverview`
- plans/{chapterId}.json (for requiredMemory and scene context)
- Memory files via `requiredMemory` targeted reads (NOT broad discovery)
- Materials from config → `materials`
- chapters/{chapterId}/v2.md

**Writes:**
- chapters/{chapterId}/v2g.md
- chapters/{chapterId}/grounder-notes.json
- agents/grounder/status.json

**Todos:** Read inputs (including exemplar before/after files) → Ground the chapter → Self-audit → Write output

**Key responsibilities:**
- Mounts `prose-grounding-framework` skill which provides a before/after exemplar pair
- Learns the grounding transformation from the exemplar, not from a category taxonomy
- Enriches prose with named geography, titled institutions, material texture, world-register dialogue, physical rhythm beats, and POV-filtered technical vocabulary
- Sources all proper nouns from memory, materials, and plan — never invents
- Self-audits against anti-slop hitlist after grounding
- Wordcount target: 40-70% growth (immersive enrichment, not noun-swapping)

**Config:** `agents.grounder.enabled` (default true)

**Failure policy:** Graceful degradation — on failure after retry, orchestrator copies v2.md → v2g.md and proceeds. Does NOT block chapter.

---

## Expander (`afternoon-expander`)

**File:** `.github/agents/afternoon-expander.agent.md`

**Reads:**
- config.json
- All files/directories from config → `priming.antiSlop`
- All files from config → `priming.craft`
- Style target from config → `priming.styleTarget`
- Voice sheets from config → `characters.voiceSheets`
- plans/{chapterId}.json (for expansionLevel per beat)
- chapters/{chapterId}/slophunter-notes.json (flaggedForExpander hints)
- chapters/{chapterId}/v2g.md

**Writes:**
- chapters/{chapterId}/v3.md
- chapters/{chapterId}/expander-notes.json
- agents/expander/status.json

**Todos:** Read inputs → Research keywords → Intimacy expansion → Emotional beat expansion → Write output

**Two expansion tests:**
1. **Intimacy Test (6Q):** Physical vocabulary, tactile detail, receiver agency, environmental integration, variation, progression
2. **Emotional Beat Test (6Q):** Body-moments, interiority matching voice, environment participating, progression, reader feeling vs knowing

**Three expansion levels (from plan's `expansionLevel` per beat):**
- **high** — moment-by-moment: unpack every compressed action into constituent sensations
- **medium** — add body-specific reactions, sensory grounding where the writer compressed
- **low** — add 1-2 sensory anchors at most, keep lean

**Config kill switch:** If `config.agents.expander.enabled` is false, the orchestrator does `cp v2g.md v3.md` and skips dispatch entirely. The style-editor always reads v3.md regardless.

---

## Style-Editor (`afternoon-style-editor`)

**File:** `.github/agents/afternoon-style-editor.agent.md` (183 lines)

**Reads:**
- config.json, story overview from config → `storyOverview`, style target, voice sheets
- Prior chapter's final.md (chapter 2+)
- slophunter-notes.json
- expander-notes.json (if expander ran)
- plans/{chapterId}.json (for beat intent + requiredMemory)
- Targeted memory files from plan's requiredMemory
- All files/directories from config → `priming.antiSlop` (slop-hitlist, ai-quirks, editor-guide — to catch slophunter leftovers)
- chapters/{chapterId}/v3.md

**Writes:**
- chapters/{chapterId}/v4.md (final version)
- chapters/{chapterId}/style-notes.json
- agents/style-editor/status.json

**Todos:** Read inputs → Research keywords → Check 1-7 → Apply fixes + write output

**7 quality checks (find-only, then single fix pass):**
1. Voice consistency (punctuation, dialogue tags, rhythm, paragraph shape vs. style target)
2. Limited Third compliance (omniscient leaks, emotional labeling, subtext translation)
3. Continuity + anti-reintroduction (names, descriptions, geography, timeline, established facts — flag passages re-stating established info as fresh)
4. Sentence variety (3+ consecutive same-length)
5. Beat transitions + narrative continuity (causal not temporal, location/emotional/topic continuity between beats, cross-chapter opening coherence for ch2+)
6. Slophunter leftovers (attribution over-explanation, parallel structure, emotional telling, scene clichés)
7. Dialogue register (institutional/clinical/bureaucratic vocabulary in speech — plain-language ceiling per voice sheet)

**Editing rules:** Do not add content. Do not cut beats. Match style target voice. Add bridging prose where transitions require it (Check 5).

**Anti-laziness enforcement:** Minimum 35 specific observations across all 7 checks (5 per check). Meta-audit required if all checks pass cleanly. Reads style-guide.json alongside style target when available.

---

## Style-Auditor (`afternoon-style-auditor`)

**File:** `.github/agents/afternoon-style-auditor.agent.md`

**Reads:**
- config.json, story overview, voice sheets, character memory profiles
- `.afternoon/style-guide.json` (required — fails if absent)
- All files from config → `priming.antiSlop`
- chapters/{chapterId}/v4.md
- chapters/{chapterId}/style-notes.json

**Writes:**
- chapters/{chapterId}/v4b.md
- chapters/{chapterId}/style-auditor-notes.json
- agents/style-auditor/status.json

**Todos:** Read inputs → Audit rhythm → Audit vocabulary → Audit metaphor → Audit paragraph/structure → Audit dialogue ratio → Audit per-POV voice → Audit quality floor → Fix pass → Meta-audit → Write output

**8 audit dimensions (all against style-guide.json):**
1. Global rhythm (sentenceRhythmStandards — default, action, introspection, emphasis)
2. Vocabulary and register (vocabularyStandards — baseline, required qualities, avoid list)
3. Metaphor compliance (metaphorPolicy — density, source domains, forbidden patterns)
4. Paragraph and structure (paragraphLengthGuidelines, sceneTransitionConventions)
5. Dialogue ratio and attribution (dialogueToNarrationRatio, attributionStandards — said-tags, action beats, untagged)
6. Per-POV voice (perPOVCalibration — every fingerprint field incl. humor, power posture, speculative comfort, exposition filter)
7. Quality floor (proseQualityFloor — adverbs, passive voice, show-tell ratio)
8. Scene-level dimensions (exposition integration, power dynamics, scene shape, speculative integration, subtext density, action pacing, humor register)

**Anti-laziness enforcement:** Minimum 40 specific observations across all dimensions. Every style-guide field checked and documented. Meta-audit required on clean results.

**Key constraint:** If `.afternoon/style-guide.json` does not exist, writes status.json with `"status": "failed"` and stops. The orchestrator treats this as a skip.

---

## Style-Extractor (`afternoon-style-extractor`)

**File:** `.github/agents/afternoon-style-extractor.agent.md`

**User-invocable — not dispatched by orchestrator.** Run once per story or when prose samples change.

**Reads:**
- config.json
- All files from config → `priming.proseSamples`
- Story overview from config → `storyOverview`
- Character voice sheets from config → `characters.voiceSheets`
- Per-character memory profiles from `.afternoon/plans/memory/characters/*.md`
- Existing `.afternoon/style-guide.json` (if refining)

**Writes:**
- `.afternoon/style-guide.json`

**Extraction dimensions:** sentenceRhythm, vocabularyRegister, metaphorDensity, emotionalExpression, dialogueStyle, narrativeDistance, paragraphStructure, descriptiveApproach, expositionIntegration, humorAndWitRegister, powerDynamicRendering, sceneArchitecture, speculativeElementIntegration, dialogueSubtextDensity, actionChoreographyStyle, attributionPatterns

**Output schema:** globalStyle (register, cadence, ratio, tense, vocabulary standards, rhythm standards, metaphor policy, paragraph guidelines, transition conventions, exposition policy, humor policy, power dynamic rules, scene shape standards, speculative integration policy, subtext density targets, action pacing standards, attribution standards) + perPOVCalibration (voice fingerprint incl. humor/power/speculative/exposition, specific rules, example sentences, exposition filter) + proseQualityFloor (adverbs, passive voice, show-tell)

**Key constraint:** Every field must be actionable — "moderate" is not actionable, "2-4 metaphors per 1000 words sourced from the POV character's professional domain" is actionable.

---

## Memory-Keeper (`afternoon-memory-keeper`)

**File:** `.github/agents/afternoon-memory-keeper.agent.md` (308 lines)

**Reads:**
- config.json
- plans/{chapterId}.json
- chapters/{chapterId}/v5.md (final prose)
- All existing memory `_index.json` files + entity files for entities in this chapter (for merge, chapter 2+)

**Writes (5 passes, per-entity files):**
- plans/memory/characters/{slug}.json + .md, characters/_index.json
- plans/memory/locations/{slug}.json + .md, locations/_index.json
- plans/memory/relationships/{slug}.json + .md, relationships/_index.json
- plans/memory/threads/{slug}.json + .md, threads/_index.json
- plans/memory/world/{topic}.json + .md, world/_index.json
- agents/memory-keeper/status.json

**Todos:** Research keywords → Pass 1: Characters → Pass 2: Locations → Pass 3: Relationships → Pass 4: Threads → Pass 5: World

**Character profile depth:** physicalDetails, voiceMarkers, beliefs (true/false), goalsAtChapterEnd, emotionalStateAtChapterEnd, decisionsThisChapter, abilitiesDemonstrated, nameUsagePatterns, bodyLanguagePatterns, knowledge, arc (lie/truth/currentPosition)

**Merge rules (chapter 2+):** Append arrays, replace singular fields, move superseded states to history

---

## Outline-Builder (`afternoon-outline-builder`)

**File:** `.github/agents/afternoon-outline-builder.agent.md`

**Workflow skill:** `.github/skills/structured-chapter-beatplan-workflow/`

**User-invocable — not dispatched by orchestrator.**

**Reads:** slop-hitlist, editor-guide, craft refs, style target, story overview from config → `storyOverview`, materials from config, existing memory files, and the `structured-chapter-beatplan-workflow` skill during blueprint assembly

**Writes:** outlines/{chapterId}.md

**Todos:** Read priming → Read style target → Genre research → Elicitation loop (5 rounds) → Build outline via `structured-chapter-beatplan-workflow` → User review → Write output

**Output format:** Normalized structured chapter beatplan schema: chapter header → `## Meta info` → open-state knowledge ledger plus chapter-exit knowledge summary → `## Arc position` with chapter-operational arc fields (current stance at open, surface objective, pressure source, misbelief manifestation, chapter test, forced choice, end-state shift, carry-forward residue) → `## Cast and handoff rules` → scene blocks with Scene/Sequel typed beats (plus optional scene-level `Arc pressure` and `Disclosure provenance` on source-sensitive reveal beats) → `## Chapter close / handoff`. Compatible with planner input and designed for later refinement passes. The workflow skill owns the heading tree and validation rules.
