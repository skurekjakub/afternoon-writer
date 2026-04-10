# Afternoon Pipeline: Sorted Remediation Passes

*Ordered by impact × effort. Each pass is self-contained — implement one, test it, then decide on the next.*

---

## Pass 1: Skeleton Strip Tool (Build Phase 1–3)

**What**: The deterministic concreteness analyzer you designed in `research/skeleton-strip/`. Uses Brysbaert psycholinguistic norms (40K words, 1–5 abstract→concrete scale) + regex pattern matching for interpretive filter structures ("the kind of X that Y", "something about the way she Z", narrator interpretation after action).

**Why first**: This is the highest-leverage heuristic tool because it catches what no LLM can reliably self-detect — abstract vocabulary drift and interpretive structures that sound natural to the model but fail the Artist Test. The slop-gate already reads 7 guides; adding pre-computed skeleton strip data as an "analytic hint" (the IBM pattern from phase 4) moves Check 8 from blind scanning to targeted verification. Research shows rule-based + LLM judge combinations improve error detection from <50% to >90%.

**Implementation**: Phases 1–3 of `research/skeleton-strip/` are fully spec'd. ~80 lines of Python total. No heavy deps (pandas for CSV load, regex for patterns, stdlib for everything else). Outputs: skeleton view (human-readable X-ray) and density report (JSON for gate consumption).

**Effort**: 1 day to build and test. Phases 1–3 are independent of the pipeline — pure Python tool.

**Files touched**: New `tools/skeleton-strip/` directory only. No pipeline changes yet.

---

## Pass 2: Skeleton Strip Gate Integration (Phase 4)

**What**: Wire the skeleton strip CLI into the slop-gate's workflow. Before the LLM audits for interpretive filter violations, run the strip and feed the flagged zones as focal points.

**Why second**: The tool is useless if nothing reads its output. This is the "analytic hints" integration — the gate knows WHERE to look instead of scanning blind.

**Implementation**: Phase 4 of `research/skeleton-strip/`. Add a pre-audit step to the slop-gate agent: run `python3 tools/skeleton-strip/strip.py --json {draft}`, read the output, use flagged paragraphs as the focus for pass B's phantom-concreteness audit.

**Effort**: 2–3 hours. One new section in the slop-gate agent, one new skill reference describing how to read the JSON output.

**Files touched**: `.github/agents/afternoon-slop-gate.agent.md`, possibly a new reference in `.github/skills/afternoon-slop-gate-workflow/references/`.

---

## Pass 3: Rhythm Scorer Module

**What**: A Python module measuring sentence-level rhythm: comma-to-period ratio, sentence length variance, coefficient of variation, sentence opener monotony, paragraph length uniformity. All stdlib Python, ~60 lines total across modules 1–3 from `research/skeleton-strip/skeleton-strip-expansion-research.md`.

**Why third**: The skeleton strip catches semantic abstraction. The rhythm scorer catches structural monotony. Together they cover the two deepest distributional problems the research identified: (1) abstract vocabulary/structures and (2) telegram prose / sentence uniformity. Your current pipeline output shows near-zero surface slop but comma:period ratio of 0.26–0.39 against a style guide target of ~1.57 in example sentences.

**Implementation**: The expansion research doc has full specs for 5 modules. Build modules 1 (sentence length + comma density), 2 (opener monotony), and 3 (vocabulary MATTR) first. Package as `tools/rhythm-scorer/score.py` with JSON output.

**Effort**: 1 day. All stdlib, no external deps beyond the skeleton strip's pandas.

**Files touched**: New `tools/rhythm-scorer/` directory.

---

## Pass 4: Telegram-Prose Guide for Slop-Gate

**What**: A new `resources/telegram-prose-guide.md` that the slop-gate reads during pass A or B. Defines: comma-to-period ratio target (0.6–1.6 for this Sanderson-influenced register), detection criteria (flag paragraphs with c:p < 0.5, flag runs of >2 zero-comma sentences, flag >3 sentences starting with same 2-word pattern), and the KILL threshold (>25% of paragraphs below c:p 0.5 = chapter fails).

**Why fourth**: This gives the slop-gate a measurable, deterministic criterion for rhythm quality. Currently all 7 guide documents target semantic or structural patterns. None target rhythm. The rhythm scorer (pass 3) provides the numbers; this guide tells the gate what the numbers mean.

**Implementation**: Write the guide (~150 lines). Add it to the slop-gate's reference loading. Could also have the gate invoke the rhythm scorer via bash and read the JSON, same as the skeleton strip integration.

**Effort**: 2–3 hours.

**Files touched**: New `resources/telegram-prose-guide.md`. Edit `.github/agents/afternoon-slop-gate.agent.md` to reference it.

---

## Pass 5: Style Guide Rhythm Recalibration

**What**: Update `.afternoon/style-guide.json` to add explicit connective-tissue guidance. The current `sentenceRhythmStandards` says "7–14 word sentences" and "two-fifths at 6 words or fewer" — which the LLM interprets as "make everything short." Add: "Even short sentences should frequently carry one internal comma — a subordinate clause, appositive, or participial phrase. Target at least 0.6 commas per sentence terminator. Avoid runs of more than two zero-comma sentences in a row."

**Why fifth**: Zero-effort intervention that aligns the explicit priming with the implicit target. The style guide's own example sentences average 1.57 c:p. Making the rhythm target measurable prevents the LLM from over-indexing on "punchy = choppy."

**Implementation**: Edit 2–3 fields in the style guide JSON.

**Effort**: 30 minutes.

**Files touched**: `.afternoon/style-guide.json`. Possibly `sentenceRhythmStandards.default` and a new `connectiveTissue` field.

---

## Pass 6: Connective-Tissue Hunt in Slophunter

**What**: Add a new structured hunt to the slophunter's pass sequence. The hunt runs the rhythm scorer on the current draft, identifies paragraphs with c:p < 0.5 or runs of >2 zero-comma sentences, and provides specific rewrite guidance for each: "Connect sentences 2 and 3 with a participial phrase. Merge sentences 4 and 5 into a compound sentence."

**Why sixth**: The slophunter currently has 6 hunt passes targeting: hedge words, filter verbs, banned phrases, dialogue register, body-part choreography, and pattern repetition. None target sentence rhythm. Adding a rhythm hunt means the slophunter actively fixes the problem in v2.md instead of leaving it for the gate to flag.

**Implementation**: Add a new hunt section to the slophunter agent. The hunt calls the rhythm scorer via bash, reads the JSON, and uses the per-paragraph flags to guide rewrites.

**Effort**: 2–3 hours.

**Files touched**: `.github/agents/afternoon-slophunter.agent.md`.

---

## Pass 7: Writer Self-Check (Skeleton Strip Phase 5)

**What**: Give the writer agent a lightweight post-draft self-check: run the skeleton strip on 5 sampled paragraphs, check the summary, rewrite any flagged-as-abstract paragraphs before delivering v1.md.

**Why seventh**: Catching the worst concreteness drift at generation time means less work for every downstream agent. The self-check is deliberately cheap — sample 5 paragraphs, not the whole chapter.

**Implementation**: Phase 5 of `research/skeleton-strip/`. Add a post-draft section to the writer agent.

**Effort**: 1–2 hours.

**Files touched**: `.github/agents/afternoon-writer.agent.md`.

---

## Pass 8: Best-of-N at Writer Step

**What**: Modify the orchestrator to dispatch the writer N times (3–5 candidates), score each with both the skeleton strip and rhythm scorer, pick the best. The slophunter then starts from a higher baseline.

**Why eighth**: BoN is the single biggest quality lever from the distribution research (doc 09 estimates 40–60% reduction in detectable AI patterns). But it requires the scorers (passes 1 + 3) to exist first, and it 3–5x's the writer's wall-clock time per chapter.

**Implementation**: Modify orchestrator dispatch logic. Add a new scorer agent or bash-based selection step. New config fields: `agents.writer.candidates` (default 1 = no change).

**Effort**: 1 day.

**Files touched**: `.github/agents/afternoon-orchestrator.agent.md`, `.afternoon/config.json`, possibly a new `afternoon-selector.agent.md`.

---

## Pass 9: Hybrid Raw-API Writer

**What**: Replace the writer's direct prose generation with a Python script that calls the Anthropic API (or OpenAI API) with `logit_bias` suppressing slop tokens, `min_p=0.03` preserving creative vocabulary, `temperature=0.85`, and `frequency_penalty=0.15`. Keep the entire post-generation pipeline on Copilot CLI.

**Why ninth**: This is where the remaining quality gains live — token-level parameter control that Copilot CLI cannot expose. But it requires an API key, external dependency, and changes the writer's generation flow. Higher effort, higher ceiling.

**Implementation**: A Python script (~200 lines) that takes a prompt file path, calls the API, writes the response. The writer agent calls this via bash instead of generating prose directly. Config field: `agents.writer.useRawApi: true`.

**Effort**: 1–2 days.

**Files touched**: New `tools/raw-writer/generate.py`. Edit `.github/agents/afternoon-writer.agent.md`. Edit `.afternoon/config.json`.

---

## Pass 10: GPT-5 DPO Fine-Tuning

**What**: Fine-tune GPT-5 via OpenAI's DPO API using preference pairs: (plan + prompt → v1.md = dispreferred, final.md = preferred). Your 25 chapters provide 25 ready-made preference pairs. Supplement with published prose excerpts.

**Why last**: Highest-ceiling intervention — modifies the model's actual weights toward your style. But highest effort, requires API costs, and is the furthest departure from the current pipeline.

**Effort**: 3–5 days including dataset curation.

**Files touched**: External (OpenAI API). New config field for fine-tuned model ID.

---

## Cross-Cutting Note: The Skeleton Strip and Rhythm Scorer Are Complementary

The skeleton strip (passes 1–2) and rhythm scorer (pass 3) attack different failure modes:

| Tool | What it catches | Layer |
|---|---|---|
| Skeleton strip | Abstract vocabulary, interpretive filter structures | Semantic |
| Rhythm scorer | Telegram prose, sentence monotony, opener repetition | Structural |

Both feed into the gate (passes 2 + 4) and can feed into the slophunter (pass 6) and writer (pass 7). Building them first enables everything downstream.

The skeleton strip research (`research/skeleton-strip/`) has fully spec'd phases 1–6. The rhythm scorer draws from the expansion research doc in the same directory. Both are stdlib Python with minimal deps.
