# The Mean Reversion Problem: Why LLMs Write Generic Prose

## The Problem, Precisely Stated

LLMs generate text by sampling from a learned probability distribution over tokens. This distribution is the weighted average of *all* the text the model has seen during training. The result: **the model's default generation regresses toward the statistical mean of its training data.**

For prose, this means:
- Word choices converge on the most commonly used words in the training distribution
- Sentence structures converge on the most common patterns
- Metaphors, similes, and descriptions converge on the most frequently occurring examples
- Voice, rhythm, and cadence flatten into a "house style" that is nobody's actual voice

This is not a bug. It's the fundamental mechanism of language modeling. The model assigns probability mass proportional to frequency in the training data. The most frequent patterns get the most probability mass. When you sample, you get the most probable tokens most often. The result reads like a competent but generic writer — because it IS the statistical average of many writers.

## Why Prompting Has a Ceiling

Few-shot prompting works by conditioning the distribution: "given these examples, what comes next?" This shifts the distribution toward patterns that are consistent with the examples. But the shift has limits:

### The Prior Is Enormous

The model's training data is trillions of tokens. Your few-shot examples are hundreds of tokens. The prior (training data distribution) overwhelms the evidence (prompt examples) by a factor of ~10 billion. The examples can nudge the distribution, but they can't fundamentally reshape it.

This is why you can prompt "write like Cormac McCarthy" and get output that is *somewhat* more terse and concrete, but still fundamentally reads like an LLM. The model has read McCarthy. It knows what McCarthy's prose looks like. But "McCarthy-like tokens" are a tiny fraction of its training distribution, and the overwhelming mass of "generic tokens" pulls the output back toward the mean.

### High-Dimensional Style Is Hard to Specify

"Write like McCarthy" is a lossy compression of a high-dimensional style signal. What does it actually mean?
- Polysyndeton ("and he rode the horse and the horse was dark and the sky was dark")
- Sparse punctuation (no quotation marks for dialogue)
- Biblical cadence in landscape description
- Specific verb selection patterns
- Extremely rare use of "he said" tags
- Violence described with clinical flatness

Few-shot examples can demonstrate some of these simultaneously, but the model treats them as *correlated* signals from the examples, not as *independent* stylistic dimensions to control. If your example shows polysyndeton AND sparse punctuation, the model doesn't decompose these — it just makes polysyndeton tokens slightly more probable and sparse-punctuation tokens slightly more probable, but the effects are shallow.

### The Attention Budget

In a transformer, the prompt examples compete with the model's parametric knowledge for influence on the output. Each example gets some attention, but the model's own patterns — encoded in billions of parameters — get attention too. The longer the generation continues, the more the model's internal patterns dominate and the less influence the examples have. This is why LLM prose often starts strong (close to examples) and degrades (back to mean) over the course of a long generation.

## The RLHF Amplification

Alignment training (RLHF, DPO for helpfulness/harmlessness) dramatically amplifies mean reversion:

### Safety = Blandness

RLHF reward models are trained on human preferences for "helpful, harmless, and honest" outputs. The reward signal penalizes:
- Unusual or potentially offensive word choices
- Dark, ambiguous, or morally complex content
- Stylistically risky constructions
- Anything that might confuse or unsettle the reader

This creates a strong gradient toward **the safest, most expected, most unexceptionable token at every position**. The alignment tax is a creativity tax.

### The Mode Collapse Effect

RLHF doesn't just flatten the distribution — it concentrates it. The model doesn't become equally likely to produce any bland output; it converges on a *specific* bland output style: the "helpful assistant" voice. This is a form of mode collapse — the output distribution narrows around a single mode rather than maintaining healthy diversity.

Evidence: Ask any RLHF-trained model to "write a story" without specific style guidance, and you'll get remarkably similar prose regardless of the model (GPT-4, Claude, Gemini, Llama). The convergence is not because these models have the same training data — they don't — but because they've been RLHF'd toward the same reward signal (human preference for "helpful" text), which converges on the same bland mode.

### The Hedge Word Explosion

Many of the specific AI writing patterns (hedge words, filter verbs, qualification) are *alignment artifacts*, not inherent language modeling failures:

- "seemed" / "appeared" / "as if" — The model hedges because assertive statements can be wrong, and being wrong is penalized by alignment
- "perhaps" / "in a way" / "somewhat" — Qualification makes claims safer
- "couldn't help but" / "found herself" — These distance the character from their own actions, reducing agency (and reducing the chance of describing something objectionable)

A base model (before RLHF) actually produces more stylistically varied prose than its aligned version. The alignment training actively teaches the model to be generic.

## What Fights Mean Reversion

Each intervention pushes back against the gravitational pull of the mean:

### Fine-Tuning (Strongest)
- Permanently shifts the model's prior distribution
- LoRA/DPO can move the baseline from "generic internet text" to "literary fiction register"
- The new distribution still has a mean, but it's the mean of *literary fiction*, not the mean of *all text*
- **Limitation**: You create a new mean to regress toward. McCarthy-fine-tuned models produce "average McCarthy," not peak McCarthy.

### Contrastive Decoding (Strong)
- Actively subtracts the generic baseline at every token
- The amateur model IS the mean — by subtracting it, you're directly countering mean reversion
- **Limitation**: Can over-correct, producing unusual token choices that are distinctive but not *good*

### Activation Steering (Medium)
- Pushes the model's internal computation away from generic patterns
- The concept vector captures *one* dimension of the generic-vs-literary distinction
- **Limitation**: Captures broad direction, not the full high-dimensional style space

### CFG (Medium)
- Amplifies the difference between prompted and unprompted generation
- The stronger your style prompt, the more CFG can amplify its effect
- **Limitation**: Bounded by what the prompt can express

### Sampling (Weak-Medium)
- Min-P allows creative choices at positions where the model is uncertain
- Doesn't fight mean reversion directly — just allows more variance where the model already "wants" to vary
- **Limitation**: If the model's distribution is strongly peaked on generic tokens, no sampling strategy will surface the long-tail creative tokens

### Prompting (Weakest)
- Shifts the distribution slightly via conditioning
- Decays over the course of long generation
- **Limitation**: The prior always wins in the long run

## The Theoretical Limit

Even with all interventions stacked, there's a fundamental limit: **the model can only produce tokens it has learned to produce in the relevant context**. If the model's training data didn't contain a particular literary construction in a particular context, no amount of steering will produce it.

The model's training data does contain vast amounts of published fiction. The constructions exist in the model. The problem is that they're buried under the probability mass of more common patterns. The interventions described in this research folder are all, ultimately, excavation tools — they dig through the layers of generic probability to reach the literary patterns underneath.

The question is not "does the model know how to write like this?" — it almost certainly does. The question is "can we reach the part of the distribution where it writes like this?" That's what all of this research is about.

## The Compounding Advantage

The good news: interventions compound. Each layer of intervention shifts the distribution further from the mean:

1. **LoRA fine-tune** shifts the baseline from "internet text" to "literary fiction"
2. **DPO** further shifts from "average literary fiction" to "preferred literary fiction"
3. **Contrastive decoding** subtracts remaining generic patterns at decode time
4. **CFG** amplifies the prompt's stylistic signal
5. **Min-P** allows creative exploration at high-variance positions
6. **Best-of-N** selects the best realization from multiple samples

Each layer fights a different aspect of mean reversion, and their effects are largely complementary rather than redundant. The stack of interventions is greater than the sum of its parts.

## The Honest Assessment

Will this stack produce prose indistinguishable from published literary fiction? Probably not — at least not consistently. The model's training distribution is a constraint that no amount of inference-time manipulation can fully escape.

But it can produce prose that is **measurably less generic, more concrete, more rhythmically varied, and closer to a specific literary register** than any single intervention alone. The difference between "reads like ChatGPT" and "reads like a competent if somewhat mechanical writer" is achievable with current technology. The difference between that and "reads like a published author with a distinctive voice" is the frontier.
