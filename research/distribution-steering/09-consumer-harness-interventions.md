# Consumer-Harness Interventions: What You Can Do Without Model Access

*Last updated: April 2026*

## The Constraint

You're working through a consumer harness — Claude Code, Copilot CLI, ChatGPT, or similar. You don't have:

- Model weights (no LoRA, no DPO, no fine-tuning — **exception**: OpenAI now offers DPO-style fine-tuning for GPT-5 via API; see "What Has Changed" below)
- Logit access (no contrastive decoding, no CFG, no DExperts)
- Activation access (no RepEng steering, no SAE feature clamping, no ITI)
- Custom sampling at decode time (no entropy-adaptive branching, no speculative decoding)
- Custom decoding (no beam search variants)

What you *do* have:

- A system prompt / custom instructions field (Claude: `CLAUDE.md`; Copilot: `.github/copilot-instructions.md` + path-specific `.instructions.md` files)
- The ability to load context (reference files, prior chapters, style targets)
- Sampling parameters via raw API: temperature, top_p, top_k (Claude, Gemini), logit_bias (Claude 4.5+, OpenAI), min_p (Claude 4.5+), frequency/presence penalty (Claude 4.5+, OpenAI)
- Limited parameter control in Claude Code via `settings.json` environment variables and hooks
- Multi-turn conversation (memory within a session)
- Tool use (file I/O, code execution, web access)
- The ability to generate, judge, and regenerate (external Best-of-N)
- Access to multiple models (different providers for different tasks)
- Fine-tuning API access (OpenAI GPT-5: SFT + DPO; Anthropic Claude: not available)

This document is about extracting maximum prose quality from this constrained position.

### What Has Changed Since Late 2025

Several items from the original "what changes the picture" list have materialized:

1. **Anthropic added `logit_bias` and `min_p` to the Claude API** (Claude 4.5/4.6 endpoints). This is a significant new lever for consumer-harness users working through the raw API — you can now penalize specific tokens (hedge words, slop phrases) and use min_p to preserve creative vocabulary diversity.
2. **OpenAI now offers DPO-style fine-tuning for GPT-5**. The OpenAI Cookbook includes step-by-step guides for preference-pair fine-tuning. This gives consumer users access to what was previously an open-weight-only intervention — training the model to prefer literary prose over generic output.
3. **Claude Code gained hooks and environment-variable parameter control**. While not full API parameter exposure, you can set temperature via `settings.json` hooks that fire on prompt submission.
4. **LLM-as-Judge research has matured**. Principle-guided judging with adversarial self-reflection now achieves 70-80% alignment with human creative writing evaluation. The EvalPlanner framework (ICML 2025) adds planning phases to judge reasoning.
5. **Multi-agent orchestration frameworks** (Google ADK, MARTI, CAMEL) now provide production-ready generate→critique→revise pipelines with built-in debugging and tracing.
6. **Context windows expanded further**. Claude Opus 4.6 supports 200K input / 128K output. GPT-5.4 supports 1.05M context / 128K output. This makes the reference-file-architecture approach even more powerful — you can load substantially more priming material.

---

## Tier 0: The System Prompt as Distribution Primer

### What it does

The system prompt conditions every token the model generates. It cannot reshape the model's learned distribution, but it can *activate* regions of that distribution that would otherwise be dormant.

Think of it as specifying which library shelf to pull from. The model has read McCarthy, King, O'Connor, Carver — that knowledge is in the weights. The system prompt says "reach for *that* shelf, not the helpful-assistant shelf."

### Why it has a ceiling

The system prompt is hundreds to thousands of tokens. The model's training prior is trillions of tokens. The prior overwhelms the prompt by a factor of ~10 billion. Over long generations, the model's internal patterns reassert themselves — what document 07 calls "mean reversion."

### How to push the ceiling higher

**1. Enumerate anti-patterns explicitly.**

Don't say "write well." Say "never use the word 'seemed.' Never use 'couldn't help but.' Never use 'found herself.' Never open a paragraph with 'After a moment.' Never use filter verbs: noticed, observed, realized, registered, catalogued, processed." The model responds better to specific prohibitions than to positive style instructions, because prohibitions create hard token-level constraints that persist across the generation.

**2. Include style anchors — actual prose excerpts.**

Copy 3-5 paragraphs of target-register prose directly into the system prompt or context window. These function as in-context exemplars, and they're more powerful than descriptions of style because they provide actual token-level patterns for the model to condition on.

Example: rather than "write like Cormac McCarthy," include 500 words of McCarthy and say "match this register, rhythm, and verb density."

The model infers style dimensions from exemplars (sentence length distribution, comma-to-period ratio, adjective density, dialogue tag patterns) implicitly. It's a lossy compression of the full style signal, but it's richer than any verbal description.

**3. Load reference files into context.**

This is the consumer-harness equivalent of "expanding the few-shot window." Tools like Claude Code can read files from disk. Load:
- A slop hitlist (banned words/phrases)
- Sentence-level anti-pattern descriptions
- Paragraph-level anti-pattern descriptions
- An editor guide (what to cut first)
- Craft technique anchors from published authors
- The actual style target (a chapter or passage in the register you want)

This can put 10,000-50,000 tokens of priming material into context. That's orders of magnitude more conditioning signal than a few-shot prompt, and it shifts the token distribution measurably — though still within the ceiling imposed by the parametric prior.

**4. Use negative examples alongside positive ones.**

Show the model what you *don't* want alongside what you *do* want. "This is AI prose: 'She noticed the way the light seemed to catch his features, almost as if...' This is what I want instead: 'The light hit his face. He looked old.'" Contrastive pairs give the model a gradient: move *away from* this, *toward* that. It's the prompt-level analog of DPO.

### Practical impact

Well-executed system prompting + context loading reduces the worst AI patterns by 30-50%. It's free, immediate, and the baseline that everything else builds on. But it will not eradicate deeply embedded distributional patterns like hedge words, body-part choreography, or the tendency toward purple abstraction under emotional intensity. Those are baked into the weights.

---

## Tier 1: Chunked Generation with Context Anchoring

### The problem with long-form generation

LLMs degrade over long outputs. The system prompt's influence decays as the generation extends. By paragraph 10-15, the model is running on its parametric prior more than on your instructions. This is the "attention budget" problem: the prompt competes with the model's internal patterns for influence, and over thousands of tokens, the internal patterns win.

### The intervention

Generate in chunks — paragraph by paragraph, or scene by scene — with explicit re-anchoring at each step.

**Pipeline:**
```
For each paragraph/scene:
  1. Re-inject: system prompt + style anchors + anti-pattern rules
  2. Include: the last 2-4 paragraphs of generated output (continuity context)
  3. Include: brief scene direction for the next beat
  4. Generate one paragraph/scene
  5. Evaluate output (manual or automated — see Tier 2)
  6. Accept or regenerate
  7. Append to manuscript and loop
```

### Why this helps

Each chunk gets the full force of the system prompt. The style anchors are fresh in the attention window. The model hasn't had 15 paragraphs of its own output to drift back toward the mean. You're resetting the conditioning signal at every step.

### Practical considerations

- **Context window budget**: With 200K token windows (Claude Opus 4.6) or 1.05M tokens (GPT-5.4), you can include substantial reference material + prior output without truncation. The bottleneck is not context length; it's attention quality over that length. Empirically, even with 200K available, the model's attention to priming material degrades past ~40-60K tokens of total context. Front-load the most important reference files.
- **Continuity**: Include enough prior output that the model maintains voice, scene state, and narrative thread. 2-4 prior paragraphs is usually sufficient; the model picks up in-progress rhythms quickly.
- **Granularity tradeoff**: Paragraph-level chunks give maximum style control but fragment narrative flow. Scene-level chunks (500-1500 words) balance control with natural pacing. Experiment.
- **Automation**: In Claude Code / Copilot, this can be semi-automated: a script that reads the last N paragraphs from the manuscript file, constructs the prompt with all reference materials, sends the generation request, and writes the output to file. The human reviews and accepts/rejects.

### Practical impact

Chunked generation with re-anchoring maintains style consistency over long manuscripts where single-shot generation degrades. The improvement is most visible in chapters 2+ of a long work, where single-shot generation has fully reverted to the mean.

---

## Tier 2: External Best-of-N with Heuristic Scoring

### The concept

Generate N candidates for each chunk. Score them. Pick the best. This is the single most powerful intervention available to consumer-harness users.

Best-of-N works because the model's output distribution has variance. On any given generation, the model might produce a hedge-word-heavy paragraph *or* a clean, concrete one. The distribution includes both. BoN selects from the right tail of quality rather than accepting whatever the model samples first.

### The scoring function

For consumer-harness users, the scorer must be external to the model (you don't have logit access for reward model scoring at decode time). Two approaches:

**A. Heuristic scorer (code-based, deterministic)**

```python
import re
import statistics

def score_prose(text: str) -> float:
    score = 100.0  # start from 100, subtract penalties
    words = text.lower().split()
    word_count = len(words)
    if word_count == 0:
        return 0.0
    
    # === PENALIZE AI PATTERNS ===
    
    # Hedge words (per-1000-word rate)
    HEDGE = {'seemed', 'almost', 'slightly', 'somewhat', 'perhaps',
             'apparently', 'rather', 'quite', 'simply', 'merely',
             'nearly', 'roughly', 'arguably', 'presumably'}
    hedge_count = sum(1 for w in words if w in HEDGE)
    score -= (hedge_count / word_count) * 1000 * 3  # 3 pts per hedge per 1000 words
    
    # Filter verbs
    FILTER_VERBS = {'noticed', 'observed', 'realized', 'registered',
                    'catalogued', 'processed', 'assessed', 'became',
                    'recognized', 'perceived', 'detected', 'sensed'}
    filter_count = sum(1 for w in words if w in FILTER_VERBS)
    score -= filter_count * 5
    
    # Banned phrases
    BANNED = [
        "couldn't help but", "found herself", "found himself",
        "the weight of", "hung in the air", "send shivers",
        "a beat passed", "claimed her lips", "ministrations",
        "the silence stretched", "the air between them",
        "something shifted", "a wave of", "washed over",
        "she wasn't sure", "he wasn't sure", "for some reason",
        "as if the world", "the evidence of", "the sensation of",
        "a flicker of", "a ghost of a smile", "without quite",
        "not unkindly", "not for the first time"
    ]
    text_lower = text.lower()
    for phrase in BANNED:
        if phrase in text_lower:
            score -= 8
    
    # Adverb density (-ly words, crude but effective)
    adverbs = [w for w in words if w.endswith('ly') and len(w) > 4
               and w not in {'only', 'early', 'likely', 'family', 'really',
                             'finally', 'belly', 'lonely', 'holy', 'daily'}]
    adverb_rate = len(adverbs) / word_count * 1000
    if adverb_rate > 15:  # more than 15 per 1000 words
        score -= (adverb_rate - 15) * 0.5
    
    # Passive voice indicators (crude)
    passive_patterns = re.findall(r'\b(was|were|been|being)\s+\w+ed\b', text_lower)
    score -= len(passive_patterns) * 2
    
    # === REWARD GOOD PATTERNS ===
    
    # Sentence length variety
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if len(sentences) > 2:
        lengths = [len(s.split()) for s in sentences]
        variance = statistics.variance(lengths)
        score += min(variance * 0.15, 10)  # reward variety, cap at 10
    
    # Comma-to-period ratio (target: 1.5-2.5)
    periods = text.count('.') + text.count('!') + text.count('?')
    commas = text.count(',')
    if periods > 0:
        ratio = commas / periods
        if 1.5 <= ratio <= 2.5:
            score += 5  # in sweet spot
        elif ratio < 0.8:
            score -= 5  # telegram prose
    
    # Concrete noun bonus (crude: words that aren't in a "vague" list)
    VAGUE = {'thing', 'things', 'something', 'everything', 'anything',
             'stuff', 'way', 'place', 'kind', 'sort', 'type',
             'part', 'bit', 'lot', 'bunch', 'amount'}
    vague_count = sum(1 for w in words if w in VAGUE)
    score -= vague_count * 2
    
    return max(0, score)
```

This scorer is imperfect — it's measuring surface proxies for prose quality. But surface proxies correlate with actual quality, and selecting the best-of-8 by this metric consistently outperforms random single-shot generation.

**B. LLM-as-Judge (model-based, stochastic)**

Use a second LLM call to evaluate each candidate. This catches patterns the heuristic scorer misses (awkward phrasing, tonal inconsistency, purple prose, cliché metaphors).

```
Evaluate this paragraph for prose quality. Score 1-10 on each dimension:
- Sensory grounding (concrete details vs. abstract language)
- Verb vitality (active, specific verbs vs. passive, generic ones)
- Rhythm variety (varied sentence lengths vs. monotonous)
- AI pattern avoidance (no hedge words, filter verbs, or banned phrases)
- Voice consistency (matches the established POV character's register)

Return ONLY the scores as JSON: {"sensory": N, "verbs": N, "rhythm": N, "patterns": N, "voice": N}
```

**The catch with LLM-as-Judge**: The judge model has the same distributional biases as the generator model. It may not detect the patterns you most want to eliminate, because those patterns are "normal" to the model. This is exactly the problem the user identified in the original question — LLM judging can't fully eradicate what LLMs can't fully perceive.

**2026 update — Principle-Guided Judging**: Recent research (Wei et al., EMNLP 2025; EvalPlanner, ICML 2025) has significantly improved LLM-as-Judge for creative writing:

- **Principle-guided judges** use explicit craft rubrics (not just "rate quality 1-10") combined with adversarial self-reflection. The judge first evaluates, then critiques its own evaluation against the rubric, then re-evaluates. This achieves 70-80% alignment with human creative writing judgments — a substantial improvement over naive single-pass judging.
- **Pairwise comparison** outperforms absolute scoring for creative quality. Instead of "score this 1-10," ask "which of these two paragraphs has more concrete sensory detail and fewer hedge words?" Pairwise judgments are more consistent and better-calibrated.
- **EvalPlanner** adds a planning phase before evaluation: the judge model first generates an evaluation plan (what to look for, in what order, what criteria matter most), then executes it. This structured approach catches more subtle issues.
- **Cross-model judging** (using a different model family as judge than as generator) remains essential. Qwen 3 235B-A22B as judge has shown strong creative evaluation capability, partly because its distributional biases differ from both Claude and GPT families.

**Updated mitigation stack**: Use the heuristic scorer as the primary filter (it catches surface-level slop deterministically), a principle-guided LLM judge with pairwise comparison as a secondary filter, and cross-model judging as a tertiary check. The heuristic scorer has zero blind spots for the patterns it's programmed to detect. The LLM judge covers what the heuristic can't measure. Cross-model judging covers what self-judging misses. Together, they approach the quality ceiling of what's possible without logit access.

### Practical parameters

- **N = 4-8** is the sweet spot for consumer harness use. Diminishing returns above N=16; below N=3, you're not sampling enough of the distribution's variance.
- **Cost**: 4-8x the generation cost per chunk. For paragraph-level BoN at current 2026 pricing (Claude Opus 4.6: ~$15/MTok input, ~$75/MTok output; GPT-5.4: ~$10/MTok input, ~$30/MTok output), a 5000-word chapter ≈ 7000 tokens × 8 candidates ≈ 56K output tokens ≈ $1.70-4.20 per chapter depending on provider. Still cheap relative to the quality improvement.
- **Automation**: A script reads candidates, scores them, selects the best, appends to manuscript. The human reviews periodically.

### Practical impact

BoN with heuristic scoring is the single highest-impact intervention for consumer-harness users. It systematically selects from the right tail of the quality distribution. Combined with chunked generation, it maintains quality over long manuscripts. Estimated 40-60% reduction in detectable AI patterns compared to single-shot generation.

---

## Tier 3: Multi-Pass Revision Pipeline

### The concept

Generate → Analyze → Revise → Analyze → Accept.

Instead of (or in addition to) selecting the best candidate from multiple generations, take a single generation and iteratively revise it through targeted passes.

### The pipeline

```
Pass 1: GENERATE
  - Full system prompt + style anchors + scene direction
  - Produce raw draft

Pass 2: PATTERN DETECTION
  - Separate LLM call (or heuristic scan)
  - Identify: hedge words, filter verbs, banned phrases,
    passive constructions, adverb clusters, telegram prose,
    body-part choreography, emotional labeling
  - Output: annotated list of specific problems with line references

Pass 3: TARGETED REVISION
  - Provide original text + identified problems
  - Prompt: "Rewrite this paragraph. Specifically:
    - Replace 'She noticed the crack' with a direct description
    - Replace 'seemed almost angry' with a concrete physical detail
    - Connect the second and third sentences — the prose is too choppy
    - The phrase 'a wave of grief washed over her' is a cliché — 
      find a specific, physical way to show grief"
  - Generate revised version

Pass 4: VERIFICATION
  - Re-run pattern detection on revised version
  - If new problems introduced, loop back to Pass 3
  - If clean (or clean enough), accept

Pass 5 (optional): VOICE CHECK
  - Separate LLM call comparing revised version against style anchors
  - "Does this paragraph match the register, rhythm, and voice
    of the following reference text? Identify any deviations."
```

### Why this works differently from BoN

BoN samples from the model's existing distribution. Revision *pushes beyond* that distribution. When you tell the model "replace 'She noticed the crack' with a direct description," you're giving it a micro-task with a concrete objective. The model is much better at targeted micro-edits than at maintaining quality over long open-ended generation. The distribution for "rewrite this specific sentence to be more concrete" is tighter and higher-quality than the distribution for "write the next paragraph of this story."

### The Constitutional AI connection

Anthropic's Constitutional AI (CAI) framework formalizes this: generate → self-critique against principles → revise. The "constitution" is your craft rules. LangChain implements this as `ConstitutionalChain`. The principles can be:

```python
principles = [
    "No hedge words (seemed, almost, slightly, somewhat, perhaps)",
    "No filter verbs (noticed, observed, realized, registered)",
    "Concrete sensory details instead of emotional labels",
    "Varied sentence length — no three consecutive sentences of similar length",
    "Comma-to-period ratio between 1.5 and 2.5",
    "Every sentence belongs to the POV character's observation or thought",
    "Dialogue tags are 'said' or action beats — nothing else",
]
```

The model critiques its own output against these principles, then revises. Multiple rounds tighten compliance.

### Limitations

- Each revision pass costs an LLM call. A 4-pass pipeline costs 4x per chunk.
- Revision can introduce *new* problems while fixing old ones. The "whack-a-mole" effect is real: the model fixes hedge words but introduces purple prose. Verification passes catch this, but at cost.
- The model may resist revision for deeply embedded patterns. Asking it to replace "She felt a wave of grief" might produce "Grief tore through her like a blade" — which trades one cliché for another. The model's "rewrite" distribution is still conditioned on its training prior.
- Diminishing returns after 2-3 passes. The first revision pass yields the largest improvement. Subsequent passes yield smaller gains and risk over-editing.

### Multi-Agent Frameworks (2026)

Production-ready orchestration frameworks now automate the generate→critique→revise pipeline with built-in debugging and tracing:

- **Google ADK** (Agent Development Kit): Chains specialized agents with memory and state management. An open-source example (Arjun1443/Multi-Agent-Story-Generation-Refinement-Pipeline) implements the full story generation + critique + refinement loop.
- **MARTI** (Multi-Agent Reinforced Training Infrastructure, ICML 2026 submission): Framework for training multi-agent systems where the critic agent's feedback directly improves the generator. More relevant for open-weight setups, but the architecture concepts inform consumer-harness pipeline design.
- **CAMEL**: Multi-agent framework supporting role-playing and debate between agents. Useful for adversarial critique: one agent argues the prose is good, another argues it's bad, and the revision agent incorporates both perspectives.
- **LangGraph**: LangChain's graph-based orchestration. Supports conditional branching (if heuristic score > threshold, skip revision; else, revise), parallel generation (BoN as parallel branches), and human-in-the-loop checkpoints.

These frameworks reduce the engineering burden of building the pipeline from scratch. The core logic remains the same — generate, score, critique, revise, verify — but the plumbing is handled.

### Practical impact

Multi-pass revision catches 50-70% of remaining AI patterns that survived initial generation. Most effective when combined with BoN: generate 4 candidates → select best → revise best through 2 passes → verify.

---

## Tier 4: Cross-Model Ensemble at Application Level

### The concept

Use different models for different tasks. Generation ≠ critique ≠ revision. Each model has different distributional biases, and cross-model evaluation reduces shared blind spots.

### Practical configurations

**Config A: Cross-provider critique**
- Generate with Claude Opus 4.6 (strong narrative, tends toward purple prose under emotional intensity)
- Critique with GPT-5.4 (different blind spots, catches different patterns, strong instruction-following)
- Revise with Claude Opus 4.6 (incorporating GPT-5.4's critique)

**Config B: Specialized roles**
- Generate raw draft with Model A (whichever produces the best first-pass prose for your style)
- Detect AI patterns with heuristic scorer (deterministic, no blind spots for measured patterns)
- Generate targeted revision prompts programmatically from heuristic output
- Execute revisions with Model B (a model that's strong at instruction-following for micro-edits — GPT-5.4 excels here)

**Config C: Adversarial pairing**
- Generate with Model A
- Ask Model B: "Identify every phrase in this text that sounds like it was written by an AI language model. Be specific and ruthless."
- Revise with Model A, incorporating Model B's critique

**Config D: Three-family tribunal (2026 addition)**
- Generate with Claude Opus 4.6
- Judge 1: GPT-5.4 (principle-guided rubric, pairwise comparison)
- Judge 2: Gemini 2.5 Pro (different training data, different blind spots)
- Judge 3: Heuristic scorer (deterministic baseline)
- Aggregate judgments with majority vote or weighted average
- Revise with the generator model, incorporating all three critiques

This three-family approach exploits the fact that Claude, GPT, and Gemini each have *different* distributional biases from their training data and RLHF processes. The intersection of what all three miss is much smaller than what any one misses.

### Why cross-model helps

Each model's distributional biases are *different*. Claude's slop profile is different from GPT-4's slop profile is different from Gemini's. When Model B evaluates Model A's output, it's not blind to the same patterns — it's blind to *its own* patterns, but may readily detect Model A's.

This is the consumer-harness version of contrastive decoding. Instead of subtracting logits, you subtract blind spots.

### Practical impact

Modest but real. Cross-model critique catches patterns that self-critique misses. The improvement is most visible for model-specific tics (Claude's tendency toward certain metaphor patterns, GPT-4's tendency toward certain sentence structures). It does not solve the fundamental shared problem of mean reversion across all RLHF-trained models.

---

## Tier 5: The Reference File Architecture (What This Workspace Does)

### The concept

This is the most sophisticated consumer-harness intervention, and it's what the system prompt of this workspace implements. The idea: don't just tell the model how to write — load a comprehensive library of reference materials that collectively shift the model's token distribution away from its default mode.

### The architecture

```
┌──────────────────────────────────────────────┐
│              CONTEXT WINDOW                   │
│                                               │
│  System Prompt (craft rules, prohibitions)    │
│       +                                       │
│  Slop Hitlist (specific banned patterns)      │
│       +                                       │
│  Sentence-Level Anti-Patterns (7 documents)   │
│       +                                       │
│  Paragraph-Level Anti-Patterns (4 documents)  │
│       +                                       │
│  Editor Guide (what to cut first)             │
│       +                                       │
│  Author Technique Anchors (craft from masters)│
│       +                                       │
│  Style Target (actual prose in target register)│
│       +                                       │
│  Prior Chapters (continuity context)          │
│       +                                       │
│  Scene Direction (what to write next)         │
│                                               │
│  Total: 20,000 - 80,000 tokens of priming    │
└──────────────────────────────────────────────┘
```

### Why this is more than "just prompting"

Standard prompting: 200-2000 tokens of instructions.
Reference file architecture: 20,000-80,000 tokens of conditioning material.
With GPT-5.4's 1.05M context window, you can theoretically load 200,000+ tokens of reference material alongside a full novel's worth of prior chapters. Attention quality degrades long before the window fills, but the practical ceiling is much higher than it was in 2024-2025.

The difference is not just quantitative — it's qualitative. At 20K+ tokens of reference material, the model is operating in a substantially different conditional distribution than at 200 tokens. The reference files don't just tell the model what to do; they activate a specific region of the model's learned space by providing dense exemplars of the target distribution.

Each reference file serves a different function:
- **Slop hitlist**: Hard token-level constraints (suppresses specific words/phrases)
- **Anti-pattern documents**: Shift attention away from common AI patterns by making them salient (the model is less likely to produce a pattern it's been explicitly shown as an error)
- **Style target**: Provides actual token-level patterns to condition on (the strongest signal)
- **Author technique anchors**: Activates craft-level knowledge the model already has but wouldn't reach by default
- **Prior chapters**: Maintains narrative-level conditioning (voice, character, plot state)

### The "mandatory priming" principle

This workspace's system prompt requires reading ALL reference files before writing any prose. This is not administrative overhead — it's the intervention. The act of processing 30,000 tokens of craft-focused reference material shifts the model's conditional distribution away from "helpful assistant writing a story" toward "fiction writer applying specific craft principles."

Whether this fully works is an empirical question. The hypothesis: priming with enough reference material can approximate (weakly) what fine-tuning does — shifting the model's effective distribution for the current generation toward a target register. The approximation is weak because the shift is temporary (context-window-only) and shallow (doesn't modify weights). But it's the strongest version of what's available without model access.

### How to build a reference file library

1. **Slop hitlist**: Compile from AI writing critique communities. The r/writingcirclejerk subreddit, AI writing criticism threads, and published analyses of AI prose patterns are good sources. Organize by category: hedge words, filter verbs, banned phrases, structural patterns.

2. **Anti-pattern documents**: Write detailed descriptions of each AI writing failure mode. Include examples of the bad pattern and examples of the corrected version. Make them vivid and specific — the model needs to understand not just *what* to avoid but *why* it fails and *what replaces it*.

3. **Style target**: Select 2000-5000 words of published prose in the exact register you're targeting. This is your north star. The model conditions on this more strongly than on any verbal description of style.

4. **Author technique anchors**: Compile craft observations from writing instruction (King's *On Writing*, Gardner's *The Art of Fiction*, Burroway's *Writing Fiction*) and from close readings of your target authors. Focus on *specific techniques* with examples, not general advice.

5. **Editor guide**: Write revision priorities specific to AI prose. What to cut first, what to look for, what substitutions to make. This primes the model's self-editing behavior during generation.

### Practical impact

The reference file architecture, combined with chunked generation and BoN, is the strongest configuration available to consumer-harness users. It does not approach what LoRA + DPO + contrastive decoding can achieve (see documents 04, 03), but it's the practical maximum within the consumer constraint.

Estimated impact: 50-70% reduction in detectable AI patterns when all tiers are stacked (reference files + chunked generation + BoN + multi-pass revision). The remaining 30-50% are patterns too deeply embedded in the model's parametric prior for context-level interventions to reach.

---

## The Honest Assessment

### What consumer-harness interventions can do

- Eliminate the *worst* AI patterns (obvious slop, hedge word clusters, banned phrases)
- Maintain style consistency over long manuscripts (via chunking and re-anchoring)
- Select from the right tail of quality (via BoN)
- Catch and fix specific problems (via targeted revision)
- Shift the overall register toward a literary target (via reference file priming)
- **NEW (2026)**: Directly suppress specific tokens via `logit_bias` on Claude 4.5+/OpenAI API — this is a genuine distribution-level intervention, not just prompt-level
- **NEW (2026)**: Fine-tune GPT-5 via DPO for style preference — consumer users can now train OpenAI's frontier model to prefer literary prose

### What they cannot do

- Fundamentally reshape the model's full token distribution (logit_bias affects individual tokens; the parametric prior still dominates the overall distribution)
- Eliminate deeply embedded distributional biases that span multi-token sequences (passive voice tendency, body-part choreography default, emotional labeling instinct)
- Prevent the model from *wanting* to produce certain patterns — they can only catch and fix them after the fact (logit_bias helps here but only for single-token patterns)
- Access activations, SAE features, or representation-level steering
- Match the quality of a well-fine-tuned open-weight model running with contrastive decoding + CFG + Min-P + custom sampling

### The gap (2026 update)

The gap has narrowed since late 2025, primarily due to Claude API gaining logit_bias/min_p and OpenAI offering GPT-5 DPO fine-tuning. But it remains significant:

| Configuration | AI Pattern Reduction | Prose Reads As |
|---|---|---|
| Single-shot generation, no interventions | 0% (baseline) | Obvious AI prose |
| Good system prompt + style anchors | 30-50% | Better, but still identifiably AI |
| + Chunked generation + re-anchoring | 40-60% | Consistent, but tells remain |
| + BoN (N=8) with heuristic + LLM judge | 55-70% | Competent, occasional AI tells |
| + Multi-pass revision (2 passes) | 65-80% | Could pass in many contexts |
| + Cross-model 3-family critique | 70-85% | Most readers wouldn't flag it |
| + API logit_bias (suppress slop tokens) | 75-88% | **New ceiling** — measurably cleaner |
| + GPT-5 DPO fine-tuning for style | 80-90% | **New ceiling** — approaching open-weight quality |
| **Open-weight: LoRA + DPO + contrastive + BoN** | **85-95%** | **Distinctive register, rarely flagged** |

The consumer-harness ceiling has risen from ~70-85% to ~80-90% for users willing to invest in both API-level logit_bias and GPT-5 fine-tuning. The gap to open-weight full-stack is now ~5-10 percentage points rather than ~15-25 points.

### What further changes the picture

- **Anthropic offering fine-tuning**: If/when Claude fine-tuning becomes available, consumer users gain the final major lever. Claude's base creative capability is arguably stronger than GPT-5's, so fine-tuning Claude could close the remaining gap.
- **Better heuristic scorers**: The scoring function above is crude. A more sophisticated scorer — incorporating NLP-level analysis (dependency parsing, semantic role labeling, coreference resolution) — could catch subtler patterns. This is buildable today with spaCy/stanza + custom rules. See the enhanced scorer below.
- **Reward model APIs**: If a service offered "score this prose for literary quality" as an API, BoN would become dramatically more powerful. The Fireworks RFT API with Qwen3-235B as judge is the closest current option but is not purpose-built for prose quality.
- **Consumer-harness exposure of min_p and temperature in Claude Code / Copilot**: Currently only available via raw API or settings.json hacks. Native UI exposure would make these interventions accessible to non-technical writers.

---

## Quick-Start for Claude Code / Copilot Users

### Minimum viable setup (30 minutes)

1. **Create a reference folder** with:
   - A slop hitlist (banned words and phrases)
   - 2000-5000 words of target-register prose (your style target)
   - A short craft guide (your most important rules)

2. **Write a system prompt** that:
   - Requires reading all reference files before generating prose
   - Lists the top 20 banned patterns explicitly
   - Sets POV discipline rules
   - Specifies dialogue craft rules
   - For Claude Code: put this in `CLAUDE.md` at the project root
   - For Copilot: put this in `.github/copilot-instructions.md`

3. **Generate in chunks**: Ask for one scene or paragraph at a time. After each chunk, the full reference material is fresh in context.

4. **Manual BoN**: Generate 2-3 versions of each chunk. Pick the best.

### Intermediate setup (a few hours)

5. **Build the heuristic scorer**: Implement the Python scorer above. Run it on each candidate to make BoN selection objective.

6. **Build a revision pass**: After selecting the best candidate, run a targeted revision prompt that fixes whatever the heuristic scorer flagged.

7. **Automate the pipeline**: A script that reads the last N paragraphs from the manuscript, constructs the full prompt with all reference materials, generates N candidates, scores them, presents the top 2 for human selection, and appends the chosen one.

### Advanced setup (days of work)

8. **Build a comprehensive reference library**: Full slop hitlist, multiple anti-pattern documents, author technique anchors, style targets for different registers.

9. **Cross-model critique**: Use a second model (or two — see Config D above) to evaluate and critique before revision.

10. **NLP-enhanced scorer**: Add spaCy-based analysis for dependency patterns, sentence structure variety, semantic density, and other features the word-level heuristic can't measure.

### Power user setup (requires raw API access)

11. **logit_bias token suppression**: Build a Python script that calls the Claude or OpenAI API directly with `logit_bias` to suppress slop tokens and `min_p` to preserve creative vocabulary. This is the single highest-impact new intervention available in 2026.

12. **GPT-5 DPO fine-tuning**: Curate 500-2000 preference pairs (published literary prose preferred, generic AI prose dispreferred). Fine-tune GPT-5 via OpenAI's DPO API. Use the fine-tuned model as your generator. This is the most powerful consumer-accessible intervention — it modifies the model's actual weights toward your style preference.

13. **Multi-agent orchestration**: Use LangGraph or Google ADK to build a full generate→score→critique→revise→verify pipeline with automated looping and human-in-the-loop checkpoints.

---

## Key References

### Papers
- Bai et al., "Constitutional AI: Harmlessness from AI Feedback" (2022) — the self-critique framework
- "Revision or Re-Solving? Decomposing Second-Pass Gains in Multi-LLM Pipelines" (HuggingFace, 2025) — when revision helps vs. when re-generation helps
- "Regularized Best-of-N Sampling" (NAACL 2025) — BoN with regularization to prevent reward hacking
- "Mining Intrinsic Rewards from LLM Hidden States" (SWIFT, 2025) — lightweight BoN scoring
- "A Survey on LLM-as-a-Judge" (arXiv 2411.15594, 2025) — comprehensive survey of model-based evaluation
- Wei et al., "Igniting Creative Writing in Small Language Models: LLM-as-a-Judge versus Multi-Agent Refined Rewards" (EMNLP 2025) — principle-guided judging for creative writing, 70-80% human alignment
- "EvalPlanner: Learning to Plan & Reason for Evaluation with Thinking-LLM-as-a-Judge" (ICML 2025) — structured evaluation planning
- "MoEQuant: Enhancing Quantization for MoE LLMs" (ICML 2025, arXiv:2505.03804) — expert-balanced quantization
- OpenAI, "Fine-tuning with Direct Preference Optimization" (OpenAI Cookbook, 2025) — DPO for GPT-5 style transfer

### Frameworks and Tools
- **LangChain ConstitutionalChain**: Automates the generate → critique → revise loop with programmable principles
- **LangGraph**: Graph-based orchestration for multi-step pipelines with conditional branching and human-in-the-loop
- **Google ADK** (Agent Development Kit): Multi-agent orchestration with state management and tracing
- **CAMEL**: Multi-agent framework supporting role-playing and adversarial debate
- **spaCy / stanza**: NLP pipeline for building sophisticated prose scorers
- **tiktoken / anthropic tokenizer**: Tokenizer libraries for logit_bias token ID mapping
- **Evidently / DeepEval / Langfuse**: LLM evaluation frameworks with LLM-as-Judge support
- **Fireworks RFT API**: Reinforcement fine-tuning with model-as-judge (supports Qwen3-235B as judge)

### API Parameters (What's Actually Exposed — April 2026)

| Provider | temperature | top_p | top_k | logit_bias | min_p | freq/presence penalty | stop_sequences | fine-tuning |
|---|---|---|---|---|---|---|---|---|
| **Anthropic API** (Claude 4.5/4.6) | ✅ | ✅ | ✅ | ✅ (new) | ✅ (new) | ✅ (new) | ✅ | ❌ |
| **OpenAI API** (GPT-5.x) | ✅ | ✅ | ✅ (new) | ✅ | ✅ (new) | ✅ | ✅ | ✅ SFT + DPO |
| **Google Gemini API** | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ |
| **Claude Code** | ⚠️ (via hooks) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | N/A |
| **Copilot CLI** | ❌ (fixed) | ❌ (fixed) | ❌ | ❌ | ❌ | ❌ | ❌ | N/A |

**Key changes from 2025:**
- Anthropic's Claude API now exposes `logit_bias`, `min_p`, and `frequency_penalty`/`presence_penalty` on Claude 4.5+ endpoints. This is a major upgrade for consumer-harness users who can write to the API directly.
- OpenAI added `top_k` and `min_p` across GPT-5 models. DPO fine-tuning is available via API.
- Google Gemini still lacks `logit_bias` — the most-requested missing feature on their developer forum.
- Claude Code has limited parameter control via `settings.json` environment variables and `UserPromptSubmit` hooks, but this is fragile and not officially supported for creative parameter tuning.
- Copilot CLI exposes nothing. You get the provider's defaults.

**Practical implication for prose quality:** If you're willing to write Python scripts that call the raw API instead of using Claude Code / Copilot's UI, you now have access to `logit_bias` + `min_p` on Claude and `logit_bias` + `min_p` + DPO fine-tuning on OpenAI. This is a significant capability uplift that makes the consumer-harness→raw-API transition worth the engineering investment for serious fiction work.

### Using logit_bias for Prose Quality (New Section)

`logit_bias` lets you adjust the probability of individual tokens at generation time. For prose quality, the highest-impact uses:

**1. Suppress slop tokens:**
```python
import anthropic

# Map banned words to token IDs (use the model's tokenizer)
# Negative bias suppresses; -5 to -10 strongly discourages without hard-blocking
slop_bias = {
    token_id("seemed"): -8,
    token_id("noticed"): -8,
    token_id("observed"): -8,
    token_id("realized"): -8,
    token_id("slightly"): -6,
    token_id("somewhat"): -6,
    token_id("perhaps"): -4,  # lighter touch — sometimes legitimate
    token_id("ministrations"): -100,  # hard block
    token_id("evidently"): -6,
}

response = client.messages.create(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": prompt}],
    logit_bias=slop_bias,
    min_p=0.03,  # preserve creative tail vocabulary
    temperature=0.85,  # slightly above default for creative variation
)
```

**2. Boost concrete vocabulary:**
```python
# Gently encourage sensory/concrete tokens
concrete_bias = {
    token_id("asphalt"): 1,
    token_id("gravel"): 1,
    token_id("rust"): 1,
    token_id("sweat"): 1,
    # ... (build per-scene based on setting)
}
```

**Caveats:**
- `logit_bias` operates on individual tokens, not phrases. You can suppress "seemed" but not "couldn't help but" as a unit.
- Over-aggressive bias creates bizarre outputs. Start with -3 to -5 and increase if needed. Never go past -10 except for absolute hard-blocks on words that have zero legitimate use in your prose.
- The token ID mapping is model-specific. Build a utility function that maps words to token IDs using the model's tokenizer.
- Combine with `min_p` (0.02-0.05) to prevent the model from collapsing to safe, generic tokens after you've suppressed its favorites.

---

## Document Index

This is document 09 of the research folder. Related documents:
- **00**: Master overview and taxonomy
- **03**: Contrastive and guided decoding (what you *can't* do from consumer harness, but could with open weights)
- **05**: Sampling strategies (Min-P, Entropix — now partially accessible via Claude/OpenAI API `min_p`)
- **07**: The mean reversion problem (why these interventions are necessary)
- **08**: Full practical stack (includes consumer-inaccessible tiers)
- **10**: Model sizing, quantization, and hardware (if you're considering switching to open-weight local models)
