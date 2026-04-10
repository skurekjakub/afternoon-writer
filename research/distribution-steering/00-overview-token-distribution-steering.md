# Manipulating LLM Token Generation Distributions: Research Overview

## The Core Problem

Large language models generate text by sampling from a probability distribution over tokens at each step. This distribution is shaped by:

1. **Pre-training data** — billions of tokens of internet text, which establishes a statistical "center of gravity"
2. **RLHF/alignment tuning** — which further narrows the distribution toward safe, helpful, generic outputs
3. **The softmax bottleneck** — which compresses the model's internal representations into a fixed vocabulary distribution

For fiction prose specifically, this creates a devastating problem: the model's token distribution is **weighted toward the statistical mean of all writing it has seen**. Distinctive prose — the kind with grain, idiosyncrasy, and a specific author's fingerprint — lives in the tails of that distribution. The model can *represent* it (it's in the training data), but its default sampling behavior actively regresses toward the mean.

Few-shot prompting helps but hits a ceiling: the examples shift the distribution *somewhat*, but the sheer mass of generic training data creates a gravitational pull back toward bland, "safe" token choices. The model "knows" what Cormac McCarthy prose looks like, but its prior over next-token probabilities still favors the statistically typical over the stylistically distinctive.

## The Research Landscape: A Taxonomy

Approaches to manipulating the token distribution fall into **three broad categories** based on *when* and *where* the intervention happens:

### Tier 1: Training-Time Methods (Weight Modification)
These permanently alter the model's parameters to shift its default distribution.

| Method | Mechanism | Effort | Access Required |
|--------|-----------|--------|-----------------|
| **SFT (Supervised Fine-Tuning)** | Retrain on curated style corpus | Medium | Model weights |
| **LoRA / QLoRA** | Low-rank adapter matrices for efficient fine-tuning | Medium | Model weights |
| **DPO (Direct Preference Optimization)** | Train directly on preference pairs (good/bad prose) | Medium-High | Model weights |
| **RLHF** | Reward model + PPO to optimize for style reward | High | Model weights + reward model |
| **CTRL-style control codes** | Special tokens prepended during training that condition generation | High | Full pre-training |

### Tier 2: Inference-Time Activation Interventions (Representation Manipulation)
These modify the model's internal computations during generation without changing weights.

| Method | Mechanism | Effort | Access Required |
|--------|-----------|--------|-----------------|
| **Representation Engineering / Activation Steering** | Add/subtract concept vectors from intermediate activations | Medium | Forward pass access |
| **SAE Feature Steering** | Clamp sparse autoencoder features to amplify/suppress concepts | Medium-High | SAE trained on model + forward pass |
| **ITI (Inference-Time Intervention)** | Shift activations at specific attention heads toward target direction | Medium | Forward pass access |
| **PPLM (Plug and Play Language Models)** | Gradient-based perturbation of hidden states using small attribute model | Medium | Forward pass + backprop |
| **InferAligner** | Cross-model safety steering vectors applied at inference | Medium | Forward pass + reference model |

### Tier 3: Decoding-Time Methods (Output Distribution Manipulation)
These modify the final token probability distribution (logits) or the sampling process itself.

| Method | Mechanism | Effort | Access Required |
|--------|-----------|--------|-----------------|
| **Classifier-Free Guidance (CFG)** | Amplify conditioned vs. unconditioned logit differences | Low | Logit access |
| **Contrastive Decoding** | Subtract amateur model's logits from expert model's | Low-Medium | Two models' logits |
| **DExperts** | Expert + anti-expert logit combination | Medium | Expert/anti-expert models |
| **GeDi** | Generative discriminator guides token selection via Bayes' rule | Medium | CC-LM discriminator |
| **Min-P Sampling** | Dynamic nucleus threshold scaled by model confidence | Low | Logit access |
| **Entropix** | Entropy/varentropy-adaptive sampling strategy | Low-Medium | Logit access |
| **Best-of-N + Reward Model** | Generate N candidates, select best via reward model | Low-Medium | Reward model |
| **Logit Bias (API-level)** | Directly add/subtract bias values on specific token logits | Low | API with logit_bias |
| **Grammar-Constrained Decoding** | Restrict valid next tokens to a formal grammar | Low | Logit access |

## Which Approaches Are Most Promising for Fiction Prose?

The problem with fiction prose is that **the target is high-dimensional and hard to specify**. Unlike "be more positive" or "avoid toxicity" — which map to relatively clean concept vectors — "write like published literary fiction and not like an LLM" involves:

- Sentence rhythm and length variation
- Verb vitality and concrete noun preference
- Absence of hedge words, filter verbs, and stock metaphors
- Dialogue that sounds spoken rather than written
- POV discipline and narrative distance control
- Paragraph-level pacing

No single method will solve this. The most promising approach is likely a **stack**:

1. **LoRA/DPO fine-tune** on a curated corpus of target-style prose (establishes a shifted baseline distribution)
2. **Activation steering** to suppress identified "AI writing" features (if SAE features for these patterns can be isolated)
3. **Contrastive decoding or CFG** at inference to further amplify the distance from generic output
4. **Min-P or Entropix sampling** to maintain creative diversity without incoherence
5. **Best-of-N with a style-specific reward model** as a final quality filter

See the detailed documents in this folder for deep dives on each approach.

## Document Index

| File | Topic |
|------|-------|
| `01-activation-steering-and-representation-engineering.md` | RepEng, concept vectors, steering at intermediate layers |
| `02-sparse-autoencoder-feature-steering.md` | SAE features, monosemanticity, feature clamping |
| `03-contrastive-and-guided-decoding.md` | CFG, contrastive decoding, DExperts, GeDi |
| `04-fine-tuning-dpo-rlhf-for-style.md` | SFT, LoRA, DPO, RLHF for stylistic control |
| `05-sampling-strategies.md` | Min-P, Entropix, Best-of-N, temperature/top-p |
| `06-gradient-based-inference-steering.md` | PPLM, ITI, InferAligner |
| `07-the-mean-reversion-problem.md` | Why LLMs regress to generic prose and what fights it |
| `08-practical-stack-for-fiction-prose.md` | Combining methods for maximum effect |
| `09-consumer-harness-interventions.md` | What you can do without model access (API/Claude Code/Copilot) |
| `10-model-sizing-quantization-hardware.md` | Min model size, quantization tradeoffs, hardware configs for prose |
| `11-afternoon-pipeline-gap-analysis.md` | Maps the running afternoon pipeline against research; enrichments, harness comparison, recommended interventions |
| `12-remediation-passes-sorted.md` | Sorted implementation passes — skeleton strip → rhythm scorer → gate integration → BoN → hybrid API |

## Key Papers & Resources

- Hendrycks et al., "Representation Engineering" (2023) — foundation for activation steering
- Anthropic, "Scaling Monosemanticity" (2024) — SAE features in Claude 3 Sonnet
- Sanchez et al., "Stay on Topic with Classifier-Free Guidance" (2023) — CFG for LLMs
- Li et al., "Contrastive Decoding Improves Reasoning in LLMs" (2022) — contrastive decoding
- Dathathri et al., "PPLM: A Simple Approach to Controlled Text Generation" (ICLR 2020)
- Liu et al., "DExperts: Decoding-Time Controlled Text Generation" (2021)
- Krause et al., "GeDi: Generative Discriminator Guided Sequence Generation" (EMNLP 2021)
- Keskar et al., "CTRL: Conditional Transformer Language Model" (Salesforce, 2019)
- Rafailov et al., "DPO: Direct Preference Optimization" (2023)
- "Turning Up the Heat: Min-p Sampling" (2024) — ICLR 2025 oral
- Entropix project (2024) — entropy-adaptive sampling
- "Controllable Text Generation for LLMs: A Survey" (arXiv:2408.12599, 2024)
- "Beyond Prompt Engineering: Robust Behavior Control via Steering" (ACL 2025)
