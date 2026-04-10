# Practical Stack for Fiction Prose Generation

## The Full Pipeline

This document synthesizes the research into a practical, implementable system for fiction prose generation that maximally resists mean reversion and AI writing patterns.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING-TIME LAYER                       │
│                                                             │
│  Base Model (Llama 3 70B / Mistral Large / etc.)            │
│       ↓                                                     │
│  LoRA SFT on curated literary corpus (2,000-5,000 passages) │
│       ↓                                                     │
│  DPO refinement on preference pairs                         │
│  (published prose preferred, AI prose dispreferred)          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                  ACTIVATION-TIME LAYER                       │
│                                                             │
│  Option A: Activation steering vectors                      │
│  (literary_direction extracted from contrastive pairs)       │
│                                                             │
│  Option B: SAE feature steering                             │
│  (suppress AI-pattern features, amplify literary features)   │
│                                                             │
│  Option C: ITI head-level intervention                      │
│  (shift identified heads toward literary direction)          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                   DECODING-TIME LAYER                        │
│                                                             │
│  Classifier-Free Guidance (γ = 1.5-2.5)                     │
│       +                                                     │
│  Contrastive Decoding (subtract small generic model)        │
│       OR                                                    │
│  DExperts (expert + anti-expert logit combination)           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    SAMPLING LAYER                            │
│                                                             │
│  Min-P sampling (min_p = 0.05-0.1, temperature = 0.9-1.1)  │
│       +                                                     │
│  Light repetition penalty (1.05-1.10)                       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    SELECTION LAYER                           │
│                                                             │
│  Best-of-N (N = 8-16)                                       │
│  Scored by: heuristic metrics + reward model (optional)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Tiers

### Tier 0: Immediate (No infrastructure required)
**What**: Better prompting + Min-P sampling + light logit bias
**When**: Right now, with API or local inference
**Impact**: Modest but measurable

- Switch from top-p to Min-P (min_p=0.07, temperature=0.95)
- Detailed system prompt with anti-pattern instructions
- Token-level logit bias: suppress top 20 worst offender tokens ("seemed", "noticed", "observed", etc.) at -2 to -3
- Manual best-of-3: generate multiple versions, pick the best

### Tier 1: Quick Wins (Days of work)
**What**: Best-of-N with heuristic scoring
**When**: Once you have a scoring pipeline
**Impact**: Significant

Build a heuristic scorer:
```python
def score_prose(text):
    score = 0
    
    # Penalize AI patterns
    HEDGE_WORDS = {'seemed', 'almost', 'slightly', 'somewhat', 'perhaps', 
                   'apparently', 'rather', 'quite', 'simply', 'merely'}
    FILTER_VERBS = {'noticed', 'observed', 'realized', 'registered', 
                    'catalogued', 'processed', 'assessed', 'became aware'}
    BANNED_PHRASES = {'couldn\'t help but', 'found herself', 'found himself',
                      'the weight of', 'hung in the air', 'send shivers',
                      'a beat passed', 'claimed her lips', 'ministrations'}
    
    words = text.lower().split()
    score -= sum(2 for w in words if w in HEDGE_WORDS)
    score -= sum(3 for w in words if w in FILTER_VERBS)
    score -= sum(5 for phrase in BANNED_PHRASES if phrase in text.lower())
    
    # Reward variety
    sentences = text.split('.')
    lengths = [len(s.split()) for s in sentences if s.strip()]
    if lengths:
        length_variance = statistics.variance(lengths) if len(lengths) > 1 else 0
        score += min(length_variance * 0.1, 5)  # reward rhythm variety, cap at 5
    
    # Penalize passive voice (crude approximation)
    passive_indicators = ['was ', 'were ', 'been ', 'being ']
    passive_count = sum(text.lower().count(p) for p in passive_indicators)
    score -= passive_count * 0.5
    
    # Penalize adverbs (words ending in -ly)
    adverb_count = sum(1 for w in words if w.endswith('ly') and len(w) > 4)
    score -= adverb_count * 0.3
    
    return score
```

Generate 8-16 candidates, score each, select the best. This alone can dramatically reduce the worst AI patterns.

### Tier 2: Serious Investment (Weeks of work)
**What**: LoRA fine-tuning on curated literary corpus
**When**: Once you've curated a quality dataset
**Impact**: Transformative

**Dataset curation**:
1. Select 20-50 published authors in target register (literary fiction, literary horror, etc.)
2. Extract 100-250 passages per author (2,000-5,000 total)
3. Each passage: 512-2048 tokens, encompassing a complete scene beat or paragraph sequence
4. Clean: no AI-generated text, no OCR artifacts, no formatting issues
5. Structure as (preceding_context, continuation) pairs for training

**Training**:
- Base: Llama 3 70B Instruct (or latest open-weight frontier model)
- LoRA rank: 64, alpha: 128
- Learning rate: 2e-5, cosine schedule
- Batch size: 4 (with gradient accumulation to effective batch 16)
- Epochs: 2-3
- Eval: hold out 10% of data, monitor loss + perplexity

### Tier 3: Research Investment (Months of work)
**What**: DPO refinement + contrastive decoding + reward model
**When**: After Tier 2 is established
**Impact**: Maximum achievable with current technology

**DPO data generation**:
1. For each prompt in your training set, generate a completion from the LoRA model (post-Tier 2)
2. Pair: (prompt, published_continuation=preferred, model_completion=dispreferred)
3. Also generate from base model (pre-LoRA) for additional negative examples
4. Train DPO on top of the LoRA model

**Contrastive decoding setup**:
- Base: Your LoRA+DPO model (70B)
- Amateur: Vanilla Llama 3 8B (or smaller) — represents the "generic" distribution
- At each token: logit_final = logit_70B - 0.5 * logit_8B

**Reward model** (for Best-of-N):
- Architecture: Fine-tuned smaller model (7B) with regression head
- Training data: Human preference judgments on (prompt, completion_A, completion_B) triples
- Can bootstrap: start with heuristic scoring, collect human judgments on edge cases, train reward model, iterate

### Tier 4: Frontier (Active research territory)
**What**: SAE feature identification + surgical feature steering
**When**: When SAE tooling matures for your target model
**Impact**: Potentially highest-precision control

1. Train SAE on your fine-tuned model's residual stream activations
2. Identify features that fire differentially for AI-pattern prose vs. literary prose
3. Build a steering profile: suppress AI-pattern features, amplify literary features
4. Deploy as inference-time hook

This is cutting-edge and requires significant ML engineering infrastructure.

---

## What You Can Do Today with API-Only Models

If you're using GPT-4, Claude, or other API-only models (no weight access, no logit access):

### Available
- Detailed system prompts with anti-pattern instructions
- Few-shot examples of target style
- Manual or automated best-of-N (generate multiple, judge externally)
- Temperature/top-p tuning (limited, but present)
- Iterative refinement (generate, critique, regenerate)
- Structured revision prompts ("rewrite this paragraph, replacing all instances of 'seemed' and 'noticed' with concrete sensory details")

### Not Available
- Fine-tuning (only via OpenAI's fine-tuning API, with limited control)
- Activation steering, SAE steering, ITI (no internal access)
- Contrastive decoding (no logit access for combining with other models)
- CFG (requires dual forward passes)
- Min-P (most APIs don't expose this; OpenAI/Anthropic use proprietary sampling)
- Logit bias (OpenAI supports, Anthropic does not, limited utility)

### The Honest Assessment for API Users

If you're constrained to API-only models, your most powerful tools are:
1. **Extremely detailed system prompts** that enumerate banned patterns and target patterns
2. **Best-of-N with external judgment** (generate 3-5 versions, score/select)
3. **Multi-pass revision** (generate → identify AI patterns → prompt to revise → repeat)
4. **Human-in-the-loop editing** (generate draft → human editor fixes AI patterns → this IS the workflow most professional AI-assisted fiction uses)

The brutal truth: **API-only users cannot access the most powerful technical interventions**. The best approaches (LoRA, DPO, contrastive decoding, activation steering) all require model weight access. API-only users are limited to prompt engineering, external scoring, and iterative refinement — which is still valuable but operates at a fundamentally different power level.

---

## Key Dependencies & Tools

### Open-Weight Models
- **Llama 3** (Meta): Strong base, most community LoRA support
- **Mistral / Mixtral**: Good alternative, strong prose quality
- **Qwen 2.5**: Competitive, multilingual strengths
- **Command R+** (Cohere): Less community tooling but strong base

### Training Infrastructure
- **Unsloth**: Fast LoRA training (2-5× speedup over standard)
- **HuggingFace TRL**: DPO training library
- **Axolotl**: Comprehensive fine-tuning toolkit
- **LLaMA-Factory**: Chinese-origin, broad model support

### Inference Infrastructure
- **vLLM**: Production inference server, supports custom samplers
- **llama.cpp**: CPU/GPU inference, supports Min-P, CFG
- **HuggingFace Transformers**: Flexible, supports all interventions
- **SGLang**: Fast inference with programmable control flow

### Interpretability & Steering
- **TransformerLens**: Intervention hooks for activation steering
- **SAELens**: SAE training and analysis
- **nnsight**: Model internals toolkit
- **Baukit**: David Bau's intervention toolkit

---

## Timeline & Priority

| Priority | Action | Time | Prerequisites |
|----------|--------|------|---------------|
| **P0** | Switch to Min-P sampling | 5 min | Min-P support in inference framework |
| **P0** | Build heuristic scorer for Best-of-N | 1-2 days | Python environment |
| **P1** | Curate literary training corpus | 1-2 weeks | Access to published fiction texts |
| **P1** | LoRA fine-tune on corpus | 2-3 days | GPU (1× A100 or equivalent), training data |
| **P2** | Implement CFG for generation | 1-2 days | Logit access |
| **P2** | Set up contrastive decoding | 2-3 days | Two models (large + small) |
| **P3** | Generate DPO preference data | 1 week | LoRA model + base model |
| **P3** | DPO training | 2-3 days | DPO data + GPU |
| **P4** | Train prose reward model | 2-4 weeks | Human preference data |
| **P5** | SAE training + feature analysis | 1-3 months | Significant GPU + ML eng time |

---

## Expected Outcomes

### Tier 0-1 (Prompting + Sampling + Heuristic BoN)
- **Reduction in worst AI patterns**: 30-50%
- **Prose reads as**: "Competent, with occasional AI tells"
- **Effort**: Days

### Tier 2 (LoRA fine-tuning)
- **Reduction in AI patterns**: 60-80%
- **Prose reads as**: "Stylistically coherent, occasionally mechanical"
- **Effort**: Weeks

### Tier 2-3 (LoRA + DPO + Contrastive Decoding + BoN)
- **Reduction in AI patterns**: 80-95%
- **Prose reads as**: "Distinctive register, could pass as human-written in many passages"
- **Effort**: Months

### Tier 4 (Full stack with SAE steering)
- **Theoretical reduction**: 90-99%
- **Prose reads as**: "Consistently literary, with precision control over style dimensions"
- **Effort**: 6+ months of research engineering
- **Caveat**: Tier 4 is speculative; no one has demonstrated this for prose quality specifically

---

## Key Research Gaps

1. **No established benchmark for "prose quality" in the LLM evaluation sense.** We need a MMLU equivalent for literary merit.

2. **No publicly available SAE analysis of prose-relevant features.** All current SAE work focuses on safety, truthfulness, and factual knowledge.

3. **Cross-model style transfer** (InferAligner-style) is completely unexplored for creative writing.

4. **The interaction between multiple interventions** (LoRA + contrastive + CFG + Min-P) is poorly characterized. Does each additional layer help? Are there interference effects?

5. **Long-form coherence under intervention.** Most evaluation is on short passages. Whether interventions maintain quality over 5,000+ word chapters is unknown.

These are all tractable research questions that could be addressed with moderate resources.
