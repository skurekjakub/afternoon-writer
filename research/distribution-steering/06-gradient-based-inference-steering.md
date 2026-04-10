# Gradient-Based Inference Steering: PPLM, ITI, InferAligner

## Overview

These methods modify the model's behavior during inference by computing gradients or applying learned perturbations to internal representations. Unlike activation steering (which applies a fixed vector), these approaches can adapt their intervention to the specific generation context.

---

## 1. PPLM (Plug and Play Language Models)

### Paper
Dathathri et al., "Plug and Play Language Models: A Simple Approach to Controlled Text Generation" (ICLR 2020)
- arXiv: https://arxiv.org/abs/1912.02164
- GitHub: https://github.com/uber-research/PPLM

### The Technique

PPLM steers generation using a small **attribute model** that provides feedback on whether the current generation matches a desired attribute. At each token:

1. **Forward pass**: Run the base LLM to get next-token logits and hidden states
2. **Attribute model evaluation**: Score the current hidden states against the attribute model (e.g., "how literary is this text?")
3. **Backward pass**: Compute the gradient of the attribute loss with respect to the hidden states
4. **Perturbation**: Shift the hidden states in the direction that increases the attribute score
5. **Modified forward pass**: Re-run the forward pass with perturbed hidden states to get modified logits
6. **Sample**: Sample the next token from the modified distribution

### The Attribute Model

Can be extremely simple:
- **Bag of Words**: Just a set of target words. The attribute model's score is the log-probability of generating words in this set. Pushes generation toward using these words.
- **Discriminator**: A small classifier (even a single linear layer) trained to distinguish "literary" from "generic" text. More powerful but requires training data.

### For Prose

**BoW approach**: Define a bag of words containing strong, concrete, literary vocabulary (specific verbs, sensory nouns, etc.) and anti-vocabulary (hedge words, filter verbs). The BoW attribute model pushes generation toward the target vocabulary and away from the anti-vocabulary.

**Discriminator approach**: Train a small classifier on (literary passage, AI-generated passage) pairs. During generation, PPLM perturbs hidden states to make the classifier score "literary" higher.

### Advantages

- **No model retraining**: The base model is completely untouched
- **Tiny attribute models**: 100,000× fewer parameters than the base model
- **Plug-and-play**: Swap attribute models for different styles
- **Gradient-based**: Adapts to the specific generation context (unlike fixed activation vectors)

### Disadvantages

- **Slow**: Requires forward + backward + forward passes per token. ~3× slower than standard generation.
- **Fluency degradation**: Strong perturbations can damage coherence. There's a tunable tradeoff between steering strength and fluency.
- **Dated**: PPLM was designed for GPT-2 era models. Scaling to modern 70B+ models is computationally expensive and largely untested.
- **Gradient computation**: Requires full backpropagation access, which rules out API-only models and even some optimized inference frameworks (vLLM doesn't support backprop natively).

### Assessment

PPLM is historically important (it proved gradient-based steering works) but **practically superseded** by newer methods. For the same computational budget, activation steering + contrastive decoding achieves comparable or better results with simpler infrastructure.

---

## 2. ITI (Inference-Time Intervention)

### Paper
Li et al., "Inference-Time Intervention: Eliciting Truthful Answers from a Language Model" (2023)

### The Technique

ITI identifies specific **attention heads** that are most responsible for a target behavior (originally truthfulness) and applies learned **shift vectors** at those heads during inference.

The process:
1. **Probing phase**: Run the model on a dataset of positive/negative examples. Record activations at every attention head.
2. **Head selection**: Identify which heads show the largest activation difference between positive and negative examples (using linear probes or mass mean analysis).
3. **Direction computation**: For each selected head, compute the direction vector that separates positive from negative activations.
4. **Inference-time shift**: During generation, add the direction vector (scaled by α) to the activations at the selected heads.

### Why ITI Is More Targeted Than Full Activation Steering

Standard activation steering adds a vector to the full residual stream at a layer. ITI intervenes only at **specific attention heads**, leaving the rest of the computation untouched. This means:

- **More precise**: Only the relevant heads are modified
- **Less interference**: Other capabilities are better preserved
- **Smaller perturbation**: The total intervention is more localized

### Application to Prose

The truthfulness → prose quality analogy:
- **Truthfulness**: Some heads are responsible for "honest" vs. "hallucinatory" outputs
- **Prose quality**: Some heads may be responsible for "generic safe" vs. "distinctive literary" word choices

**Speculative workflow**:
1. Collect (literary passage, AI-generic passage) pairs
2. Run both through the model, record per-head activations
3. Find heads with maximal separation between literary and generic
4. Compute shift vectors for those heads
5. Apply during generation

This is entirely speculative for prose — ITI has only been demonstrated for truthfulness. But the principle (behavioral properties localizable to specific heads) is likely general.

### Practicality

Moderate. Requires model internals access and a probing phase, but once the heads and vectors are identified, inference-time application is fast (no backward pass, just addition at specific heads).

---

## 3. InferAligner

### Paper
"InferAligner: Inference-Time Alignment for Harmlessness through Cross-Model Guidance" (EMNLP 2024)
- arXiv: https://arxiv.org/abs/2401.11206
- GitHub: https://github.com/Jihuai-wpy/InferAligner

### The Technique

InferAligner decouples the alignment process: train for capability, align at inference. The key innovation is **cross-model guidance**: use a pre-aligned reference model to generate **Safety Steering Vectors (SRVs)** that can be applied to any target model.

1. **From the reference model**: Run harmful and harmless prompts, compute the difference in last-token activations → this is the SRV
2. **Apply to target model**: During inference, shift the target model's activations along the SRV

The SRV transfers the alignment properties of the reference model to the target model without retraining.

### The Cross-Model Transfer Insight

This is remarkable: alignment properties (and potentially, stylistic properties) can be **transferred between models** via activation vectors. If you have a model that generates good prose (however obtained), you could extract "good prose vectors" from it and apply them to a different model.

### Application to Prose

**Speculative**: If you have Model A that writes excellent prose (perhaps a small model heavily fine-tuned on literary fiction) and Model B that is a powerful general-purpose model, you could:

1. Extract "literary style vectors" from Model A by contrasting literary vs. generic generations
2. Apply these vectors to Model B during inference

This would give Model B the prose quality of Model A without any fine-tuning of Model B.

**Caveats**: 
- InferAligner was designed for safety, not style. Whether cross-model style transfer works is untested.
- The activation spaces of different model architectures may not be compatible.
- This might only work between models within the same family (e.g., Llama 7B → Llama 70B).

---

## Comparison

| Method | Precision | Speed Overhead | Backprop Needed | Cross-Model | Maturity |
|--------|-----------|----------------|-----------------|-------------|----------|
| PPLM | Medium | ~3× | Yes | No | Legacy |
| ITI | High (head-level) | ~1.1× | No (at inference) | No | Moderate |
| InferAligner | Medium | ~1.1× | No (at inference) | Yes | Early |

## Recommendation

For fiction prose specifically:

1. **ITI is the most promising** if you're willing to do the probing work to identify prose-relevant attention heads. Once identified, the overhead is minimal and the precision is high.

2. **InferAligner's cross-model transfer** is a fascinating direction for future experimentation: can you extract "writes like a published author" from a fine-tuned small model and inject it into a general-purpose large model?

3. **PPLM is historical reference only**. Its contributions (proving gradient-based steering works, showing tiny attribute models suffice) influenced everything that came after, but it's been superseded.
