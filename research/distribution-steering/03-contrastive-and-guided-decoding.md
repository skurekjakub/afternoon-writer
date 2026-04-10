# Contrastive & Guided Decoding Methods

## Overview

These methods operate at the **output distribution level** — they modify the logits (pre-softmax scores) or the sampling process to bias token selection without touching the model's weights or internal activations. They're the most accessible interventions because many require only logit access, which even some API providers expose.

The core insight: **you can reshape the next-token distribution at every generation step by combining, contrasting, or modulating logit values from different sources.**

---

## 1. Classifier-Free Guidance (CFG) for LLMs

### The Technique

Borrowed from diffusion models (text-to-image generation), CFG amplifies the difference between conditioned and unconditioned generation. For LLMs:

```
log P_guided(w_i) = log P(w_i) + γ * (log P(w_i | prompt) - log P(w_i))
```

Where:
- `P(w_i)` = probability of token w_i with no conditioning (empty/null prompt)
- `P(w_i | prompt)` = probability with the actual prompt
- `γ` (guidance scale) = how much to amplify the prompt's influence

At `γ = 1.0`, you get normal generation. At `γ > 1.0`, tokens that the prompt makes more likely are boosted further; tokens that are likely regardless of the prompt are relatively suppressed.

### Why It Matters for Prose

If your system prompt specifies "write in the style of Cormac McCarthy with concrete nouns and active verbs," CFG amplifies the tokens that the prompt makes uniquely more likely compared to the model's unconditioned defaults. This means:

- Tokens characteristic of the requested style get boosted
- Generic, default tokens (the ones the model would produce regardless) get relatively suppressed
- The guidance scale `γ` acts as a "style adherence knob"

### Key Paper

**Sanchez et al., "Stay on Topic with Classifier-Free Guidance" (2023)**
- arXiv: https://arxiv.org/abs/2306.17806
- ICML 2024 publication: https://proceedings.mlr.press/v235/sanchez24a.html
- Project page: https://vermeille.github.io/cfg-llm/

Results:
- LLaMA-7B with CFG achieved SOTA on LAMBADA, surpassing PaLM-540B
- 75% human preference for CFG-enhanced outputs in assistant tasks
- Effectively doubles model capacity for prompt adherence
- Already implemented in HuggingFace Transformers and llama.cpp

### Practical Notes

- **Requires two forward passes per token** (conditioned + unconditioned), so ~2x inference cost
- **γ = 1.5 to 3.0** is typically the sweet spot. Above ~5.0, outputs become repetitive/degenerate
- **Negative prompting** is possible: specify what you *don't* want, and CFG steers away from it
- **Combinable** with other sampling methods (temperature, top-p, Min-P)

---

## 2. Contrastive Decoding

### The Technique

At each generation step, compute logits from two models: a strong "expert" model and a weaker "amateur" model. The final distribution favors tokens that the expert considers likely but the amateur does not:

```
score(w_i) = log P_expert(w_i) - log P_amateur(w_i)
```

Tokens where both models agree (generic, common continuations) get cancelled out. Tokens where only the expert is confident (more sophisticated, context-appropriate choices) get boosted.

### Why It Matters for Prose

If the expert is a large, capable model and the amateur is a small, generic model, contrastive decoding naturally suppresses the "lowest common denominator" token choices. The small model embodies exactly the statistical mean you're trying to escape — it's a proxy for "generic writing." Subtracting it forces the output toward what only the large model can produce: more nuanced, contextually aware language.

### Variants (2024-2025)

**Classic Contrastive Decoding** — Li et al. (2022)
- Expert: large LLM. Amateur: smaller LLM (same family or different).
- OpenReview: https://openreview.net/forum?id=SzV37yefM4

**Speculative Contrastive Decoding (SCD)** — ACL 2024
- Uses the amateur model for both speculative acceleration AND contrastive quality. One small model serves dual purpose, reducing overhead.
- Paper: https://aclanthology.org/2024.acl-short.5.pdf

**Active Layer-Contrastive Decoding (ActLCD)** — EMNLP 2025
- Applies contrast across *layers within the same model* rather than between two models. A learned policy selects which layers to contrast at each step.
- Reduces hallucinations in long-form generation.
- Project page: https://actlcd.github.io/

**Confidence-Driven Contrastive Decoding (CCD)** — 2026
- Selectively applies contrastive intervention only on "low-confidence" tokens. Saves compute and avoids over-intervention on tokens where the expert is already confident.
- arXiv: https://arxiv.org/abs/2602.18232

**Contrastive Decoding with Abstention (CDA)** — 2024
- Adds an abstention mechanism: the model can decline to generate when it lacks sufficient information.
- HuggingFace: https://huggingface.co/papers/2412.12527

### For Fiction Prose

The most promising variant is **classic contrastive decoding with a deliberately weak amateur**. Train (or select) a small model that embodies "generic AI writing." The contrastive subtraction then specifically removes AI-typical token preferences.

Even better: use a model fine-tuned on AI-generated prose as the amateur. This creates a targeted anti-pattern:

```
score(w_i) = log P_main(w_i) - β * log P_ai_slop_model(w_i)
```

Where `β` controls how aggressively you subtract the AI patterns.

---

## 3. DExperts (Decoding-Time Controlled Text Generation)

### The Technique

Liu et al. (2021) formalized the expert/anti-expert pattern. At each step:

```
P_final(w_i) ∝ P_base(w_i) * P_expert(w_i)^α / P_anti_expert(w_i)^α
```

Or equivalently in log-space:
```
logit_final = logit_base + α * (logit_expert - logit_anti_expert)
```

- **Expert model**: Fine-tuned on desired attribute (e.g., literary prose)
- **Anti-expert model**: Fine-tuned on undesired attribute (e.g., generic AI output)
- **α**: Controls steering strength

### Why It's Compelling for Prose

DExperts lets you define both what you want AND what you don't want, independently. For fiction:

- **Expert**: Small model fine-tuned on published literary fiction
- **Anti-expert**: Small model fine-tuned on AI-generated prose (collected from various LLMs)
- **Base model**: Your primary generation model (e.g., Llama 3 70B)

The expert nudges toward literary patterns. The anti-expert nudges away from AI patterns. Both are small (7B or even 1-3B) and cheap to train. The base model provides the core generation capability.

### Practical Advantages

- The expert and anti-expert can be very small (even 1B parameter models work)
- Training is just standard fine-tuning on curated corpora — much simpler than RLHF
- Plug-and-play: same base model can be paired with different expert/anti-expert combos
- Inference cost: ~3x (three models' logits combined), but the small models are fast

---

## 4. GeDi (Generative Discriminator Guided Sequence Generation)

### The Technique

Krause et al. (EMNLP 2021) use a class-conditional language model (CC-LM) as a generative discriminator. At each step, the CC-LM computes the probability that the next token belongs to the desired class vs. the undesired class, using Bayes' rule:

```
P(class | token, context) ∝ P(token | context, class) * P(class)
```

This probability is used to reweight the base model's next-token distribution.

- Paper: https://arxiv.org/abs/2009.06367
- GitHub: https://github.com/salesforce/GeDi

### Relevance to Prose

GeDi's CC-LM approach is efficient (no gradient computation, just forward passes) and generalizes zero-shot to new topics/attributes. For prose, you could train a CC-LM on two classes: "literary fiction" and "AI-generated fiction." The GeDi mechanism would then discriminatively guide token selection toward the literary class.

### Limitation

GeDi was designed for coarser attribute control (sentiment, topic). Whether it has sufficient granularity for the subtle stylistic differences between good and mediocre prose is an open question.

---

## 5. Logit Bias (API-Level)

The simplest form of logit manipulation. APIs like OpenAI's expose a `logit_bias` parameter:

```python
logit_bias = {
    token_id_for_seemed: -5,     # suppress
    token_id_for_noticed: -5,    # suppress
    token_id_for_realized: -5,   # suppress
    token_id_for_slightly: -5,   # suppress
}
```

### Severe Limitations

- Operates on **individual tokens**, not patterns. You can't suppress "she noticed the..." as a construction — you can only reduce the probability of the token "noticed" everywhere, including where it's appropriate.
- Token-level bias doesn't understand context. Suppressing "seemed" also suppresses it in dialogue where a character might naturally say "seemed."
- Limited number of biases (typically 300 tokens max).
- Blunt instrument for a nuanced problem.

**Verdict**: Useful for crude vocabulary steering (suppress a handful of the worst offenders), but fundamentally insufficient for the prose quality problem. A band-aid, not a solution.

---

## Comparison Matrix

| Method | Precision | Cost | Access Needed | Best For |
|--------|-----------|------|---------------|----------|
| CFG | Medium | 2x inference | Logit access | Overall style adherence |
| Contrastive Decoding | Medium-High | 2x inference | Two models | Suppressing generic patterns |
| DExperts | High | 3x inference | Three models | Dual push/pull on style |
| GeDi | Medium | 1.5x inference | CC-LM | Attribute-level control |
| Logit Bias | Very Low | None | API | Individual word suppression |

## Practical Recommendation

For fiction prose, **DExperts is the most promising decoding-level approach**. It explicitly models both the target style (via expert) and the anti-target (via anti-expert), providing the strongest lever for shifting the distribution away from AI patterns and toward literary ones. Combined with **Min-P sampling** (see sampling strategies document) and upstream **LoRA fine-tuning** of the base model, this creates a three-layer intervention stack.

CFG is the easiest to deploy (already in standard toolchains) and provides meaningful improvement for minimal effort — it should be the first thing to try.

Contrastive decoding is a strong middle option if you don't want to train separate expert/anti-expert models and can instead just pair a large model with a small one from the same family.
