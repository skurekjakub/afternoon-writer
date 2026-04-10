# Sampling Strategies: Min-P, Entropix, Best-of-N

## The Sampling Problem for Prose

Standard sampling parameters (temperature, top-k, top-p) are blunt instruments. They control the overall "randomness" of generation but don't distinguish between *good* randomness (creative word choices, surprising but apt verbs) and *bad* randomness (incoherence, non sequiturs, factual errors).

For fiction prose, you want the model to take creative risks with word choice while maintaining narrative coherence. Standard sampling can't optimize for both simultaneously — turning up temperature gives you more creative choices but also more garbage.

Newer sampling strategies address this by making the sampling process **context-aware**: adapting the randomness level based on the model's confidence at each token position.

---

## 1. Min-P Sampling

### The Technique

Traditional top-p (nucleus) sampling uses a **fixed** probability threshold: include tokens until their cumulative probability exceeds p. The problem: at high temperature, the distribution flattens, and top-p includes many low-quality tokens.

Min-P uses a **dynamic** threshold that scales with the model's confidence:

```
threshold = min_p * max_probability
```

Where `max_probability` is the highest-probability token at the current step.

- When the model is confident (max_probability is high): threshold is high → small sampling pool → deterministic-ish
- When the model is uncertain (max_probability is low): threshold is low → large sampling pool → more creative

This matches intuition: when the model "knows" what comes next (function words, common phrases, sentence completions), don't randomize. When the model is choosing between multiple valid continuations (word choice, metaphor selection, narrative direction), allow exploration.

### Key Paper

**"Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs" (2024)**
- arXiv: https://arxiv.org/abs/2407.01082
- **ICLR 2025 oral presentation** — significant recognition
- OpenReview: https://openreview.net/forum?id=FBkpCyujtS

Results:
- Consistent human preference over top-p across creative writing tasks
- Better coherence-creativity tradeoff, especially at high temperature
- Tested on Llama-3 and Mistral (1B to 123B parameters)

### Practical Settings

```
min_p: 0.05 to 0.1 (typical range)
temperature: 0.8 to 1.2 (can go higher with Min-P than with top-p)
```

Min-P is already implemented in:
- HuggingFace Transformers (`min_p` parameter)
- vLLM
- llama.cpp
- Most modern inference frameworks

### Why It Matters for Prose

Min-P naturally encourages the kind of variance that makes prose interesting: surprising but valid word choices at positions where multiple options are legitimate, combined with stability where the grammar or narrative demands a specific continuation. This maps well to the craft principle of varying sentence rhythm — the model is "allowed" to make unusual choices when the text calls for them.

---

## 2. Entropix: Entropy-Adaptive Sampling

### The Technique

Entropix takes the adaptive principle further by considering both **entropy** (overall uncertainty) and **varentropy** (variance of uncertainty) to select different sampling strategies for different situations:

| Entropy | Varentropy | Strategy | Prose Application |
|---------|------------|----------|-------------------|
| Low | Low | **Argmax** (deterministic) | Known continuations, function words |
| Low | High | **Branch** (explore multiple paths) | Plot decision points, word choice |
| High | Low | **Pause/CoT** (clarify before continuing) | Ambiguous narrative situations |
| High | High | **Cautious sampling** (temperature reduction) | Chaotic/confused generation states |

### How Branching Works

When the model detects low entropy but high varentropy (a few strong competing options), Entropix can:
1. Generate multiple candidate continuations in parallel
2. Evaluate each branch (via a reward model, heuristic, or further generation)
3. Select the best branch and continue

This is essentially **speculative generation with quality selection** — generating several possible "next paragraphs" and picking the one that reads best.

### Key Resource

- GitHub: https://github.com/xjdr-alt/entropix
- Emerged in late 2024, open-source, community-driven

### For Prose

Entropix's branching mode is particularly interesting for fiction. At a narrative decision point (does the character turn left or right? does the dialogue escalate or deflect?), the model generates multiple continuations and selects the strongest. This is similar to how authors actually write — trying several versions of a passage and keeping the best one.

The pause/CoT mode is less directly useful for fiction (you don't want the model to insert "let me think about this" tokens into your prose), but could be useful in a pipeline where the model reasons about narrative structure between generation steps.

### Maturity

Early. Entropix is more of a research prototype than a production tool. The core ideas are sound, but robust implementation and parameter tuning for creative writing are still being worked out.

---

## 3. Best-of-N Sampling with Reward Models

### The Technique

Generate N completions for the same prompt. Score each with a reward model. Return the highest-scoring one.

```
completions = [model.generate(prompt) for _ in range(N)]
scores = [reward_model.score(c) for c in completions]
return completions[argmax(scores)]
```

### Why It's Powerful

Best-of-N converts any reward signal into better generation without modifying the model at all. If you have a reward model that can distinguish good prose from bad prose, you can dramatically improve output quality just by generating more candidates.

**Key insight**: The quality of the best-of-N sample scales as O(log N) with the number of candidates. This means:
- N=4 is much better than N=1
- N=16 is significantly better than N=4
- N=64 is somewhat better than N=16
- Diminishing returns beyond ~64

### The Reward Model Problem

The bottleneck is the reward model. For prose quality, you need a reward model that captures:
- Absence of AI patterns (hedge words, filter verbs, stock metaphors)
- Presence of literary quality markers (concrete nouns, active verbs, varied rhythm)
- Narrative coherence and voice consistency
- Dialogue naturalness

Building such a reward model is itself a research problem. Options:

1. **Train from preference data**: Collect human judgments on prose quality, train a reward model. Best quality, highest cost.
2. **Use heuristic scoring**: Automated metrics (hedge word count, passive voice ratio, sentence length variance). Cheap but captures only surface features.
3. **Use a strong LLM as judge**: Ask GPT-4 or Claude to score prose quality. Moderate cost, reasonable quality, but introduces the same AI biases (the LLM judge may not reliably detect subtle AI patterns in its own kind of output).
4. **Ensemble of heuristics + LLM judge**: Combine automated metrics with LLM evaluation. Most robust, moderate cost.

### Recent Advances

**Regularized Best-of-N (RBoN)** — adds regularization to prevent reward hacking:
- Paper: https://arxiv.org/abs/2502.12668

**MBR-BoN (Minimum Bayes Risk)** — uses risk minimization to select outputs that are robust to reward model errors:
- Paper: https://aclanthology.org/2025.naacl-long.472/

**Speculative Rejection** — accelerates BoN by terminating unpromising generations early:
- NeurIPS 2024: https://deep-diver.github.io/neurips2024/posters/348hfcprus/
- GitHub: https://github.com/Zanette-Labs/SpeculativeRejection
- Achieves 16-32x speedup over naive BoN

### For Prose

Best-of-N is the **simplest method to deploy** and the one most likely to produce immediate improvement. Even with a crude reward model (heuristic-based scoring), generating 8-16 candidates and selecting the best one produces measurably better prose than single-sample generation.

The main cost is latency: generating 16 candidates takes 16x the compute (or 16x the time, if not parallelized). Speculative Rejection mitigates this significantly.

### Practical Recipe

```python
# Pseudo-code for Best-of-N prose generation
def generate_best_prose(prompt, model, reward_model, n=16):
    candidates = [model.generate(prompt, temperature=0.9, min_p=0.05) for _ in range(n)]
    
    scores = []
    for c in candidates:
        # Heuristic component
        hedge_penalty = count_hedge_words(c) * -0.5
        filter_verb_penalty = count_filter_verbs(c) * -0.3
        rhythm_score = sentence_length_variance(c) * 0.2
        concrete_noun_bonus = concrete_noun_ratio(c) * 0.3
        
        # LLM judge component (optional)
        llm_score = judge_model.score_prose_quality(c)
        
        total = hedge_penalty + filter_verb_penalty + rhythm_score + concrete_noun_bonus + llm_score
        scores.append(total)
    
    return candidates[argmax(scores)]
```

---

## 4. Standard Sampling Parameters (Reference)

For completeness, the standard parameters and their effects:

### Temperature
- Controls sharpness of the distribution
- Low (0.1-0.5): Deterministic, safe, repetitive
- Medium (0.6-0.9): Balanced
- High (1.0-1.5): Creative, risky, potentially incoherent
- For prose: 0.8-1.0 is typical. Higher with Min-P.

### Top-k
- Hard cutoff: only consider the top k tokens
- For prose: top_k=50-100 is common. Less relevant when using Min-P.

### Top-p (Nucleus)
- Soft cutoff: include tokens until cumulative probability reaches p
- For prose: top_p=0.9-0.95 is standard
- Superseded by Min-P for creative applications

### Repetition Penalty
- Reduces probability of recently generated tokens
- For prose: 1.05-1.15 range. Too high makes text stilted; too low allows loops.
- Context-window repetition penalty (penalize recent tokens more) is better than global penalty for long-form fiction.

### Frequency / Presence Penalty
- Frequency: Penalizes tokens proportionally to how often they've appeared
- Presence: Flat penalty for any token that has appeared at all
- For prose: light frequency penalty (0.1-0.3) helps vocabulary diversity

---

## Assessment & Recommendations

| Method | Impact | Cost | Complexity | Deploy? |
|--------|--------|------|------------|---------|
| Min-P | Medium | None (parameter change) | Trivial | **Immediately** |
| Best-of-N (heuristic) | Medium-High | N× compute | Low | Yes, for important passages |
| Best-of-N (reward model) | High | N× compute + reward model | Medium | If you build the reward model |
| Entropix | Medium | ~1.5× compute | Medium | Experimental; watch this space |

**Immediate action**: Switch from top-p to Min-P sampling. This is a free improvement.

**Next step**: Implement Best-of-N with heuristic scoring (hedge word count, filter verb count, sentence length variance). This is the highest-impact method with lowest barrier to entry.

**Research investment**: Build a prose-quality reward model trained on human preference data. This unlocks high-quality Best-of-N and can also be used for DPO training data generation.
