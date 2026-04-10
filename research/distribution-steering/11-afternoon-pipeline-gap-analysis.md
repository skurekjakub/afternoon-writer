# Afternoon Pipeline Gap Analysis: What the Research Says You're Missing

*April 2026 — Maps the running afternoon pipeline against the token-distribution research (docs 00–10)*

---

## What You Already Have

The afternoon pipeline is the most sophisticated consumer-harness fiction system I've seen. Let me map it against the tier system from docs 08 and 09 before identifying gaps.

### Tier Coverage

| Research Tier | What It Is | Pipeline Implementation | Coverage |
|---|---|---|---|
| **T0: System prompt priming** | Anti-pattern rules, craft anchors, style target in context | Writer loads `references/slop-hitlist.md`, `ai-quirks/` (17 docs, ~4600 lines), `editor-guide.md`, `author-technique-anchors.md`, style target, voice sheets, memory files. Slophunter reloads all `priming.antiSlop` before each hunt. | **Excellent** — 20K+ tokens of priming, reloaded per-agent |
| **T1: Chunked generation** | Scene/paragraph chunks with re-anchoring | Writer generates full chapter from beat plan in one shot. No intra-chapter chunking. | **Partial** — beat-by-beat plan structures output, but no explicit re-anchoring mid-generation |
| **T2: Best-of-N selection** | Generate N candidates, score, pick best | Not implemented. Every agent produces exactly 1 output. | **Missing** |
| **T3: Multi-pass revision** | Generate → detect → revise → verify loop | Slophunter → slop-gate → revision loop (up to 5 iterations). Style-editor → style-auditor. Grounder → grounding-gate → revision loop. Final slophunter polish. | **Excellent** — this is the pipeline's strongest dimension |
| **T4: Cross-model ensemble** | Different models for generation vs. critique | Writer = Claude Opus 4.6. Slophunter/slop-gate/style-editor/grounder/etc = GPT-5.4. | **Good** — natural cross-model critique, but only 2 families (no third voice) |
| **T5: Reference file architecture** | Dense priming library loaded into context | 6,400 lines in `references/`, 1,882 lines in `resources/`, 11,687 lines in skill references. Agents selectively load what they need. | **Excellent** — probably the densest reference library of any consumer fiction pipeline |

### What the Pipeline Does Well

1. **Adversarial gate loops.** The slop-gate and grounding-gate are genuine adversarial verifiers, not rubber stamps. The manifest shows real convergence failures — ch19 grounding gate exhausted at 3 iterations, ch21 slop-gate exhausted at 5. This means the gates are actually catching problems the hunters miss.

2. **Separation of concerns.** Each agent has one job. The slophunter doesn't ground, the grounder doesn't hunt slop, the style-editor doesn't rewrite plot. This prevents the "whack-a-mole" problem doc 09 warns about — fixing one thing by introducing another.

3. **Cross-model generation/critique.** Claude Opus 4.6 writes, GPT-5.4 hunts slop. Different distributional blind spots. Claude's purple prose tendencies get caught by GPT's instruction-following precision. GPT's mechanical rhythm tendencies get smoothed by the style-editor's Le Guin persona.

4. **Progressive versioning.** v1→v2→v2g→v3→v4→v4b→v5→final is a clean artifact trail. Every agent reads its specific input version and writes its specific output. No state confusion.

5. **Reference volume.** Slop-gate alone reads 7 specialized guide documents (1,882 lines). The writer loads the full anti-slop arsenal plus craft references. This is the reference-file-architecture approach at maximum density.

---

## The Gaps

### Gap 1: No Best-of-N at the Generation Step (High Impact)

The single highest-impact missing intervention. Every doc in the research folder that discusses consumer-harness ceilings identifies BoN as the biggest quality lever.

**The problem:** Claude Opus 4.6 generates v1.md as a single shot. The model's output distribution has variance — on any given generation, it might produce a hedge-word-heavy paragraph *or* a clean one. You're accepting whatever it sampled first.

**What BoN would give you:** Generate 3–5 candidate v1.md files. Score them with a heuristic scorer (the Python code in doc 09). Pick the best. The slophunter then has less work to do, and the final output quality rises because you started from a better point on the distribution.

**Why it's complicated on Copilot CLI:** The orchestrator dispatches the writer agent once. There's no native mechanism to say "dispatch this 5 times, score the outputs, keep the best." You'd need to:
- Modify the orchestrator to dispatch the writer N times with different output paths (v1-candidate-1.md, v1-candidate-2.md, etc.)
- Add a scorer agent (or a bash-based Python scorer) that reads all candidates and picks the best
- Copy the winner to v1.md

**Cost:** 3–5x the writer's generation cost per chapter. At current Copilot subscription pricing, this is free (you pay for the subscription, not per-token). The cost is wall-clock time — each candidate takes 5–15 minutes.

**Expected improvement:** Doc 09 estimates 40–60% reduction in detectable AI patterns from BoN alone. Your pipeline already handles the easy stuff (hedge words, filter verbs, banned phrases). BoN would target the harder stuff: rhythm, sentence structure variety, metaphor freshness — things the slophunter can catch but can't always fix well.

### Gap 2: No Heuristic Scorer (High Impact, Enables Gap 1)

The pipeline has adversarial LLM judges (slop-gate, grounding-gate, style-auditor) but no deterministic code-based scorer. This matters because:

1. **LLM judges share distributional blind spots.** Doc 09's core argument: the judge model has the same biases as the generator. GPT-5.4 judging Claude Opus 4.6 catches *some* cross-model patterns, but both models share fundamental RLHF-induced tendencies (passive voice default, body-part choreography, emotional labeling).

2. **A heuristic scorer has zero blind spots for what it measures.** If you code "flag any occurrence of 'seemed'" — it will catch every occurrence. Always. An LLM judge might miss it because "seemed" is normal to the model.

3. **Heuristic scoring enables automated BoN.** You can't do BoN without a scorer. The Python scorer from doc 09 (lines 147–226) is a starting point.

**What to measure:**
- Hedge word density (per 1000 words)
- Filter verb count
- Banned phrase count
- Comma-to-period ratio (target: 1.5–2.5)
- Adverb density (-ly words per 1000)
- Sentence length variance (reward variety)
- Passive voice rate
- Paragraph opener pattern variety (first word of each paragraph — flag if >3 start with "The" or "She/He")

**Your current numbers are revealing:**

| Chapter | Hedge/1k | Filter | Banned | Adverb/1k | Comma:Period |
|---|---|---|---|---|---|
| ch1 final | 0.4 | 0 | 1 | 2.4 | 0.32 |
| ch10 final | 0.8 | 0 | 0 | 4.0 | 0.39 |
| ch20 final | 0.8 | 0 | 0 | 1.0 | 0.32 |
| ch25 v5 | 0.5 | 0 | 0 | 1.5 | 0.26 |

The slop metrics are extremely clean — near-zero hedge words, zero filter verbs, zero banned phrases across late chapters. **The pipeline has solved surface-level slop.** But the comma-to-period ratio (0.26–0.39) is far below even the Sanderson source material (0.63) and the style guide's own example sentences (1.57). This is the "telegram prose" signal — short, choppy sentences. The style guide specifies punchy 7–14 word sentences, but even those should carry internal rhythm (subordinate clauses, appositives). The pipeline is defaulting to 6–8 word declaratives with zero commas, undershooting its own style target. The slophunter instructions mention this problem explicitly (the "Anti-Teflon" and "Telegram prose" sections), but the multi-pass revision loop isn't fixing it because:
- The slop-gate audits against specific guide documents, none of which specifically score comma-to-period ratio
- The slophunter's self-audit reads the hitlist, which mentions telegram prose, but the LLM's own judgment of "is this too choppy?" is unreliable because choppy is normal to the model
- A heuristic scorer would flag any passage with comma:period < 1.0 deterministically

### Gap 3: Comma-to-Period Ratio / Telegram Prose (The Deepest Remaining Problem)

This deserves its own section because it's the signature problem the research predicts — and it's visible even when the style target is already punchy.

The Sanderson source material (travel.md — *The Way of Kings*) runs a comma-to-period ratio of **0.63**. Sanderson writes punchy, action-forward prose by literary fiction standards. The style guide extracted from that source has example sentences averaging **1.57** c:p — those are the sentences the pipeline is supposed to emulate. The pipeline's final chapters land at **0.26–0.39**.

| Source | Comma:Period | Notes |
|---|---|---|
| Pipeline final chapters | 0.26–0.39 | 5x below style guide examples |
| Sanderson source (travel.md) | 0.63 | Already punchy for fiction |
| Style guide example sentences | 1.57 | The actual target voice |
| Literary fiction (McCarthy, Le Guin) | 1.5–2.5 | Reference range |

The pipeline is not undershooting "literary fiction" — it's undershooting its own style target. Even though the style guide says "center the prose in 7–14 word sentences" and "two-fifths at 6 words or fewer," that punchy target still uses subordinate clauses, appositives, and compound structures within those sentence lengths. A 14-word sentence with two commas is still punchy — it just has internal rhythm. The pipeline is defaulting to 6–8 word sentences with zero commas, which reads as telegram prose even within a punchy register.

Doc 07 ("The Mean Reversion Problem") explains why: LLMs trained on internet text default to short declarative sentences because internet text is predominantly short declarative sentences. The RLHF process reinforces this because short sentences are "clear" and "helpful." The model's parametric prior for sentence structure is overwhelmingly biased toward Subject-Verb-Object periods. The explicit "short sentences for snap" instruction in the style guide may compound the problem — the model hears "short" and truncates even harder than asked.

**This is not something multi-pass revision can fully fix.** The slophunter rewrites sentences to remove slop, but its rewrites are themselves generated by an LLM that defaults to short sentences. Asking GPT-5.4 to "connect choppy sentences" produces sentences that are slightly longer but still fundamentally in the short-declarative register.

**What can fix it:**
1. **Heuristic scorer flagging** passages with c:p < 0.5 and requiring regeneration (BoN selects candidates with higher c:p). The threshold here is lower than for literary fiction — 0.5–0.8 is a reasonable target for this Sanderson-influenced register.
2. **Specific prompting for connective tissue** — adding a measurable constraint: "Target at least 0.6 commas per sentence terminator. Use subordinate clauses, participial phrases, and compound sentences to add internal rhythm even within short sentence lengths."
3. **logit_bias** suppressing the period token (token ID for ".") by -1 to -2, making the model slightly less eager to end sentences. This is only available via raw API, not through Copilot CLI.
4. **Rebalancing the style guide's rhythm instructions** — the "two-fifths at 6 words or fewer" guideline may be over-indexing the model toward fragments. Consider raising the floor to "one-quarter at 6 words or fewer" to reduce choppiness while keeping snap.

### Gap 4: No Sampling Parameter Control (Copilot CLI Limitation)

**What Copilot CLI gives you:** Nothing. Temperature is fixed. Top-p is fixed. No logit_bias. No min_p. No frequency/presence penalty. You get the provider's defaults and nothing else.

**What matters for prose quality:**
- `temperature 0.85–0.95` — slightly above default for creative variation
- `min_p 0.03–0.05` — preserves creative tail vocabulary (unusual verbs, specific nouns) while cutting nonsense
- `logit_bias` on slop tokens — deterministic suppression at the token level, before the model even considers them
- `frequency_penalty 0.1–0.3` — discourages within-chapter repetition

**The API params table from doc 09:**

| Feature | Copilot CLI | Claude Code | Raw Anthropic API | Raw OpenAI API |
|---|---|---|---|---|
| temperature | ❌ fixed | ⚠️ via hooks | ✅ | ✅ |
| logit_bias | ❌ | ❌ | ✅ (Claude 4.5+) | ✅ |
| min_p | ❌ | ❌ | ✅ (Claude 4.5+) | ✅ (GPT-5.x) |
| freq/presence penalty | ❌ | ❌ | ✅ (Claude 4.5+) | ✅ |
| Model selection per agent | ✅ (frontmatter) | ✅ (config) | ✅ | ✅ |
| Multi-agent orchestration | ✅ (task tool) | ✅ (subprocesses) | Manual | Manual |
| File I/O in-agent | ✅ (create/edit/view) | ✅ (native) | Manual | Manual |
| Tool use | ✅ (bash/grep/glob) | ✅ (bash/etc) | Via function calling | Via function calling |

**The stark implication:** Copilot CLI's strongest advantage is orchestration (the `task` tool, agent definitions, skill mounts, hook system). Its weakest point is generation-time parameter control — zero access. The pipeline already maxes out what Copilot CLI can do at the orchestration layer. The remaining quality gains require parameters Copilot CLI cannot expose.

### Gap 5: No Fine-Tuning (The Biggest Theoretical Lever)

Doc 09 identifies OpenAI's GPT-5 DPO fine-tuning as the single most powerful consumer-accessible intervention. It modifies the model's actual weights toward your style preference.

Your pipeline generates with Claude Opus 4.6, which Anthropic does not offer fine-tuning for. But you could:
- Fine-tune GPT-5 via OpenAI's DPO API with preference pairs (published literary prose preferred, generic AI prose dispreferred)
- Switch the writer to the fine-tuned GPT-5 model
- Keep the rest of the pipeline on standard models for cross-model critique

**The dataset would be straightforward to build:** Take your 25 chapters' v1.md (AI prose the model tends to produce) and the corresponding final.md (your pipeline-polished prose). That's 25 preference pairs already generated. Supplement with published literary prose as additional "preferred" examples.

**Cost:** OpenAI fine-tuning pricing is opaque but estimated at $5–25 per training run for small datasets. A 500-pair DPO dataset is small.

**Catch:** This requires leaving Copilot CLI for the generation step, running it through the raw OpenAI API, then pulling the result back into the Copilot pipeline.

### Gap 6: Single-Family Critique (Moderate Impact)

The pipeline uses two model families: Claude (writer) and GPT (everything else). Doc 09's "Config D: Three-family tribunal" suggests adding a third family as judge:

- **Gemini 2.5 Pro** has different training data and different distributional blind spots than both Claude and GPT
- **Qwen 3 235B** is the creative writing leader on benchmarks and has yet another bias profile

Adding a third judge family to the slop-gate or style-auditor would catch patterns that Claude and GPT both miss. The intersection of what all three miss is smaller than what any two miss.

**On Copilot CLI:** You can set `model:` in agent frontmatter to any available model. If Copilot exposes Gemini or Qwen models, you could add a third verification pass with a different model. Currently Copilot CLI offers Claude and GPT families.

---

## Copilot CLI Enrichments (What You Can Do Without Leaving)

### 1. Add a Python Heuristic Scorer Agent

Create a new agent `afternoon-scorer.agent.md` that:
1. Reads v1.md (or any version)
2. Runs the Python heuristic scorer via bash
3. Writes a score report JSON
4. The orchestrator reads the score and decides whether to accept or regenerate

This doesn't require any API access — it runs deterministic Python in a bash shell, which Copilot CLI supports perfectly.

The scorer script lives in the repo. The agent calls `python3 scripts/score-prose.py .afternoon/chapters/{chapterId}/v1.md` and reads the output.

### 2. Add Best-of-N at the Writer Step

Modify the orchestrator to:
1. Dispatch the writer 3 times (different output filenames: v1-a.md, v1-b.md, v1-c.md)
2. Dispatch the scorer on each candidate
3. Pick the highest-scoring candidate
4. Copy it to v1.md
5. Continue the pipeline

This 3x's the writer's wall-clock time per chapter but should measurably improve the starting point for all downstream editors.

### 3. Add a Telegram-Prose Hunt to the Slophunter

The slophunter's current hunts target: hedge words, filter verbs, banned phrases, dialogue register, body-part choreography. Add a dedicated "connective tissue" pass:

- Calculate comma-to-period ratio per paragraph
- Flag any paragraph with c:p < 0.8
- For each flagged paragraph, provide a specific rewrite instruction: "Connect sentences 2 and 3 with a participial phrase. Merge sentences 4 and 5 into a compound sentence."

This is a new hunt the slophunter can run via its existing structured-passes architecture. The detection is heuristic (Python counts commas and periods); the rewrite is LLM-driven but targeted.

### 4. Add Connective-Tissue Metrics to the Slop-Gate

The slop-gate currently audits against 7 guide documents. Add an 8th: a `telegram-prose-guide.md` in `resources/` that:
- Defines the comma-to-period ratio target (1.5–2.5)
- Defines detection: flag any paragraph with c:p < 0.8, any three consecutive sentences under 10 words, any passage with >3 sentences starting with the same syntactic pattern
- Defines the KILL threshold: if >20% of paragraphs are below c:p 0.8, the chapter fails the gate

This gives the adversarial gate a deterministic, measurable criterion for rhythm quality.

### 5. Diversify Model Families in Existing Agents

If Copilot CLI exposes additional model families (check what's available), assign the style-auditor or a new verification agent to a third family. Even within the GPT family, using a different model version (e.g., GPT-5.2-Codex for analysis) might expose different blind spots.

### 6. Recalibrate Style Guide Rhythm Instructions

The style guide currently says: "Center the prose in 7-14 word sentences. Let roughly two-fifths of sentences land at 6 words or fewer." This instruction, combined with the action pacing guidance ("Cut to 3-9 words for impact chains"), may be compounding the LLM's natural tendency toward short declaratives.

The style guide's own example sentences average 1.57 commas per period — complex, connected clauses even within a punchy register. Consider adding explicit connective-tissue guidance:
- "Even short sentences should frequently use one internal comma — a subordinate clause, an appositive, or a participial phrase"
- "Avoid runs of more than two zero-comma sentences in a row"
- "Target at least 0.6 commas per sentence terminator across any given page"

This makes the rhythm target explicit and measurable, rather than leaving it to the model's interpretation of "punchy" (which defaults to "choppy").

---

## What Switching Harnesses Would Give You

### Claude Code

**Gains:**
- `settings.json` hooks for temperature control (fragile, unofficial, but functional)
- `CLAUDE.md` system prompt (equivalent to copilot-instructions.md — no material difference)
- Native bash/file I/O (equivalent to what you have)
- Sub-agent dispatching via the task tool (equivalent)

**Losses:**
- No agent definition files with frontmatter (model selection, description, agent-to-agent references)
- No skill mounting system (you'd need to restructure reference file loading)
- No hook system for subagent context injection
- No `task` tool with named custom agent types — Claude Code's subprocesses are generic
- You'd have to rebuild the entire orchestration architecture

**Net assessment:** Claude Code gives you temperature control (one parameter, fragile) at the cost of your entire orchestration infrastructure. **Not worth it for the pipeline.**

### Raw API (Anthropic or OpenAI) — Hybrid Approach

This is the high-impact option. Keep the pipeline on Copilot CLI for orchestration, but replace the writer's generation step with a raw API call.

**How it would work:**
1. The orchestrator dispatches a modified writer agent
2. The writer reads the plan, priming files, and style target
3. Instead of generating prose directly, the writer constructs a prompt and calls a Python script
4. The Python script calls the Anthropic API (or OpenAI API) with:
   - `logit_bias` suppressing slop tokens
   - `min_p=0.03` preserving creative vocabulary
   - `temperature=0.85`
   - `frequency_penalty=0.15`
5. The script writes the API response to v1.md
6. The writer agent reads v1.md and continues normally (self-audit, status file)

**What this unlocks:**
- Token-level slop suppression before the model even considers those tokens
- min_p preserving rare, specific vocabulary (the "gravel," "tannin," "sluiceway" words that make prose vivid)
- Temperature tuning for creative variation
- Frequency penalty discouraging within-chapter repetition

**What it doesn't change:** The entire post-generation pipeline (slophunter, slop-gate, grounder, style-editor, etc.) stays on Copilot CLI. You're only replacing the generation step.

**Engineering cost:** A Python script (~200 lines) that:
- Takes a prompt file path as input
- Reads the prompt
- Calls the API with prose-optimized parameters
- Writes the response to an output path
- Handles retries, rate limits, output length

The writer agent would call this via bash instead of generating prose directly. Everything else in the pipeline stays the same.

### Raw API + BoN — The Full Upgrade

Combine the hybrid approach with Best-of-N:

1. The Python script generates N=5 candidates via raw API (with logit_bias + min_p)
2. Each candidate is scored by the heuristic scorer
3. The best candidate is selected
4. The best candidate is written to v1.md
5. The pipeline continues

This stacks the two biggest missing interventions (BoN + sampling parameters) into a single script change. The orchestrator still runs on Copilot CLI. The slophunter/gate/grounder/style pipeline is unchanged.

### Raw API + DPO Fine-Tuning — The Nuclear Option

If you're willing to invest a few days:

1. Curate preference pairs from your existing 25 chapters: (plan + v1.md prompt, v1.md = dispreferred, final.md = preferred)
2. Supplement with published prose excerpts as additional preferred examples
3. Fine-tune GPT-5 via OpenAI's DPO API
4. Use the fine-tuned model as the generator in the hybrid approach
5. Keep the rest of the pipeline on standard models (cross-model critique)

This is the only consumer-accessible intervention that modifies the model's actual weights. Doc 09 estimates it closes 80–90% of the gap to open-weight quality.

---

## Ranking by Impact × Effort

| Intervention | Impact | Effort | Requires Leaving Copilot? |
|---|---|---|---|
| **1. Recalibrate style guide rhythm targets** | Medium | 30 minutes | No |
| **2. Add heuristic scorer agent + script** | High | 1 day | No |
| **3. Add telegram-prose guide to slop-gate** | Medium | 2 hours | No |
| **4. Connective-tissue hunt in slophunter** | Medium | 2 hours | No |
| **5. Best-of-N at writer step** | High | 1 day | No (adds wall-clock time) |
| **6. Hybrid raw-API writer with logit_bias + min_p** | High | 1–2 days | Partially (generation step only) |
| **7. Raw API + BoN (5 candidates)** | Very High | 2 days | Partially |
| **8. GPT-5 DPO fine-tuning** | Very High | 3–5 days | Partially (training via OpenAI API) |
| **9. Three-family tribunal (add Gemini/Qwen judge)** | Moderate | 1 day | Only if model not available on Copilot |

**Recommended order:** 1 → 2 → 3 → 4 → 6 → 5 → 7 → 8

Start with the zero-effort style target fix. Then build the heuristic scorer (it enables everything else). Add the telegram-prose guide and hunt. Then go hybrid for the generation step — that's where the remaining gains live.

---

## The Honest Ceiling

Your pipeline currently operates at roughly Tier 3.5 of the doc 09 scale — excellent multi-pass revision and cross-model critique, dense reference architecture, but no BoN and no sampling parameter control. The measured output is very clean on surface-level slop (near-zero hedge words, filter verbs, banned phrases) but has the deeply embedded rhythm problem (comma-to-period ratio of 0.26–0.39 vs. target 1.5–2.5).

With the recommended interventions:

| Configuration | Estimated Ceiling | What Changes |
|---|---|---|
| Current pipeline | ~70–80% AI pattern reduction | Surface slop eliminated, rhythm problems persist |
| + Style target + telegram-prose guide | ~73–83% | Rhythm slightly improved from better priming |
| + Heuristic scorer + BoN (N=3) | ~80–88% | Starting from better v1.md, scorer catches rhythm |
| + Hybrid raw API (logit_bias + min_p) | ~83–90% | Token-level suppression, creative vocab preserved |
| + DPO fine-tuning on GPT-5 | ~87–93% | Model's base distribution shifted toward target |
| **Open-weight LoRA+DPO+contrastive+BoN** | **~90–95%** | **Full stack, but requires ML infrastructure** |

The gap between your fully-upgraded pipeline (~87–93%) and the open-weight theoretical maximum (~90–95%) is 2–8 percentage points. That remaining gap is the difference between "most readers wouldn't flag it" and "distinctive register that reads like a specific author." For most fiction projects, the upgraded consumer-harness pipeline is sufficient. For prose that needs to be indistinguishable from a specific published author's voice, open weights are still the answer.

---

## Related: Skeleton Strip Research

The user's `research/skeleton-strip/` directory contains a fully spec'd but not-yet-built deterministic concreteness analyzer using the Brysbaert psycholinguistic norms (40K words rated 1–5 on abstract↔concrete). This is a more sophisticated version of the "heuristic scorer" recommended above — it targets the **semantic concreteness** layer rather than just surface metrics like comma counts or hedge word frequency.

Combined with the rhythm scorer from the expansion research, the skeleton strip covers both failure modes:
- **Skeleton strip** → catches abstract vocabulary drift and interpretive structures ("the kind of X that Y")
- **Rhythm scorer** → catches telegram prose, sentence monotony, and opener repetition

The implementation-ordered remediation passes are detailed in doc 12: `12-remediation-passes-sorted.md`.

## Document Index

This is document 11 of the research folder. Related:
- **08**: Full practical stack with all tiers (consumer + open-weight)
- **09**: Consumer harness interventions (the tier system this document maps against)
- **10**: Model sizing and quantization (if considering open-weight route)
- **07**: The mean reversion problem (why these gaps exist in the first place)
