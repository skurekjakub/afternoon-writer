# Fine-Tuning for Style: SFT, LoRA, DPO, RLHF

## The Weight-Modification Approach

Unlike inference-time methods (which leave the model unchanged and intervene during generation), fine-tuning permanently shifts the model's default token distribution. A model fine-tuned on literary fiction will, by default, generate prose that's closer to its training data's style — without any special prompting or decoding tricks.

This is the most powerful lever, but also the most expensive and the one with the highest risk of side effects (capability degradation, overfitting, catastrophic forgetting).

---

## 1. Supervised Fine-Tuning (SFT)

### What It Does

Standard SFT trains the model on (prompt, completion) pairs where the completions exemplify the target style. The model learns to minimize cross-entropy loss against these completions, shifting its entire probability distribution toward the patterns in the training data.

### For Prose Style

**Training data**: Curate a corpus of 1,000–10,000 passages of target-style prose. Each passage is a (context, continuation) pair where:
- Context = preceding paragraphs or a story prompt
- Continuation = the published author's actual text

**What changes**: The model's default word choices, sentence structures, rhythm patterns, and constructions all shift toward the training corpus.

**What doesn't change**: The model doesn't learn *rules* ("don't use hedge words") — it learns *statistical patterns* ("in this register, the probability of 'seemed' is lower and the probability of concrete verbs is higher"). This is both its strength (captures patterns too subtle to articulate as rules) and its weakness (it can also learn surface-level quirks that don't generalize).

### Practical Issues

- **Corpus quality is everything.** Garbage in, garbage out. The training data must represent the target style cleanly — no AI-generated text, no mediocre prose, no stylistically inconsistent selections.
- **Catastrophic forgetting.** Heavy SFT can degrade the model's other capabilities (reasoning, instruction-following, factual knowledge). Mitigation: keep training short, mix in general instruction-following data.
- **Overfitting risk.** Small corpora (< 1,000 examples) risk the model memorizing specific phrases rather than learning general style patterns. Mitigation: more data, regularization, early stopping.

---

## 2. LoRA / QLoRA (Parameter-Efficient Fine-Tuning)

### What It Does

LoRA (Low-Rank Adaptation) doesn't modify the model's full weight matrices. Instead, it trains small, low-rank "adapter" matrices that are added to the model's existing weights. This achieves most of the effect of full fine-tuning while training only 0.1–1% of the total parameters.

**QLoRA** adds quantization: the base model is loaded in 4-bit precision, reducing memory requirements dramatically. A 70B model that normally requires 140GB of VRAM can be QLoRA-tuned on a single 48GB GPU.

### Why LoRA Is Ideal for Style

1. **Multiple adapters**: You can train separate LoRA adapters for different styles (McCarthy-esque, Carver-esque, King-esque) and swap them at inference time. One base model, many style profiles.

2. **Reversibility**: The adapter is a separate file. Remove it, and you're back to the base model. No risk of permanent damage.

3. **Speed**: LoRA training on 5,000 examples takes hours, not days. Iteration cycle is fast enough for experimentation.

4. **Composability** (limited): You can, in theory, merge multiple LoRA adapters. In practice, this is unreliable for subtle style features — the adapters can interfere.

### Practical Recipe

```
Base model: Llama 3 70B (or Mistral Large, or similar)
LoRA rank: 32-64 (higher rank = more capacity, but diminishing returns)
LoRA alpha: 64-128 (scaling factor; typically 2x rank)
Target modules: All attention layers + MLP layers (full coverage)
Training data: 2,000-5,000 (prompt, literary_completion) pairs
Learning rate: 1e-5 to 5e-5
Epochs: 2-3 (more risks overfitting)
Context length: 2048-4096 tokens (long enough for paragraph-level patterns)
```

### The Critical Ingredient: Training Data Curation

The dataset defines the ceiling. Bad data = bad adapter. Key principles:

1. **Homogeneous style.** Don't mix McCarthy with Austen with King. Each adapter should target a coherent register.
2. **Sufficient volume.** 2,000+ examples for basic style transfer. 5,000+ for robust generalization.
3. **Representative contexts.** Include dialogue-heavy passages, description passages, action sequences, interior monologue — all the modes the model will need to generate.
4. **No AI contamination.** Verify that training data is human-written. AI-generated prose in the training data will reinforce exactly the patterns you're trying to escape.

---

## 3. DPO (Direct Preference Optimization)

### What It Does

DPO skips the reward model entirely. Instead, it trains directly on **preference pairs**: (prompt, preferred_completion, dispreferred_completion). The model learns to assign higher probability to the preferred completion and lower probability to the dispreferred one.

The loss function implicitly learns a reward model within the language model's parameters:

```
L_DPO = -log σ(β * (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))
```

Where `y_w` = preferred (winning) completion, `y_l` = dispreferred (losing) completion, `π_ref` = reference model (the base model before training).

### Key paper: Rafailov et al., "Direct Preference Optimization: Your Language Model Is Secretly a Reward Model" (2023)

### Why DPO Is Compelling for Prose Style

DPO is perfect for the case where **you can show examples of better vs. worse prose but can't easily articulate the rules**. This maps exactly to the fiction prose problem:

- **Preferred**: Published literary fiction passage
- **Dispreferred**: AI-generated version of a similar scene (or the same scene rewritten by an LLM)

You don't need to specify "more active verbs" or "fewer hedge words" — the model learns from the preference signal which token-level patterns correlate with human preference.

### The SFT → DPO Pipeline

The standard approach (2024 best practice):

1. **SFT phase**: Fine-tune on target-style prose to establish baseline capability
2. **DPO phase**: Further refine using preference pairs to push distribution away from AI patterns and toward human-preferred patterns

The SFT phase gets the model into the right ballpark. The DPO phase makes the fine adjustments — it's the difference between "writes in a literary register" (SFT) and "writes in a literary register AND avoids the specific AI patterns that SFT didn't fully eliminate" (SFT + DPO).

### Generating Preference Data

The bottleneck is preference pair creation. Options:

1. **Human annotation**: Show two completions to a human reader, ask which is better. Gold standard but expensive.
2. **AI-assisted**: Use a strong model (GPT-4, Claude) to judge quality between a published passage and an AI-generated alternative. Cheaper but introduces the same AI biases you're trying to escape.
3. **Automated heuristics**: Score completions on measurable proxies (hedge word count, sentence length variance, passive voice ratio) and prefer the one that scores better on these metrics. Scalable but only captures measurable aspects.
4. **Published vs. AI contrast**: For any passage of published fiction, generate an AI completion from the same prompt. The published version is always preferred. Simple, scalable, but assumes the published version is always "better" (usually true for well-curated data).

---

## 4. RLHF (Reinforcement Learning from Human Feedback)

### What It Does

The full RLHF pipeline:
1. **Reward model training**: Train a separate model to predict human preference given a (prompt, completion) pair
2. **PPO optimization**: Use the reward model as a reward signal and train the language model with Proximal Policy Optimization to maximize expected reward

### Why It's Less Practical for Prose

RLHF is the most powerful alignment technique but also the most expensive, unstable, and prone to pathologies:

- **Reward hacking**: The model finds patterns that score high on the reward model without actually improving prose quality. Example: the reward model might inadvertently reward longer sentences, so the model generates bloated text.
- **Computational cost**: Training a reward model + running PPO is 5-10x more expensive than DPO.
- **Instability**: PPO training can diverge, requiring careful hyperparameter tuning.
- **The alignment tax**: RLHF-trained models tend toward safe, generic outputs — exactly the problem we're trying to solve. Using RLHF for creative quality requires a reward model specifically trained for literary merit, NOT helpfulness/harmlessness.

### When RLHF Makes Sense

If you need continuous, online improvement: deploy the model, collect human feedback on generated prose, update the reward model, retrain. This iterative loop is RLHF's unique strength — DPO is a one-shot training, while RLHF can iterate.

For most prose-style applications, DPO is sufficient and much more practical.

---

## The Alignment Tax Problem

This is the elephant in the room. Modern LLMs are heavily RLHF-trained for helpfulness and harmlessness. This training:

1. **Flattens stylistic diversity**: The model converges on a "helpful assistant" voice that is competent but unremarkable
2. **Suppresses risk-taking**: Unusual word choices, dark tones, ambiguous narratives are downweighted because they could be "unhelpful" or "harmful"
3. **Encourages hedging**: Safety-trained models hedge everything. "Perhaps," "it seemed," "in a way" — these are alignment artifacts as much as stylistic flaws
4. **Creates mode collapse**: The model's outputs converge on a narrow band of styles and registers, even when prompted for diversity

Any fine-tuning for style must fight against this entrenched alignment. DPO with explicit preference for bold/distinctive over generic/safe prose is the most direct weapon.

---

## Assessment

| Method | Cost | Impact | Practical Difficulty | Recommended? |
|--------|------|--------|---------------------|-------------|
| SFT | Low | Medium | Easy | Yes, as first step |
| LoRA | Low | Medium | Easy | Yes, primary recommendation |
| DPO | Medium | High | Moderate | Yes, as refinement step |
| RLHF | High | High (with good reward) | Hard | Only for iterative improvement |

**The recommended pipeline**: LoRA SFT → DPO refinement → inference-time decoding (CFG or contrastive). This captures the most value at each stage with manageable complexity.
