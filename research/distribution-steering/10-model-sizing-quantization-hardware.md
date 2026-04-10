# Model Sizing, Quantization, and Hardware for Fiction Prose

*Last updated: April 2026*

## The Short Answer

**70B dense parameters is the floor for quality prose. MoE models change the math but not the VRAM.** The best open-weight fiction writing in April 2026 comes from:

1. **Qwen 3 235B-A22B** (MoE, 22B active) — best creative writing alignment, Apache 2.0
2. **Llama 4 Maverick** (MoE, 17B active, 400B total) — best long-form continuity, 1M context
3. **Llama 3.3 70B** (dense) — best *runnable-on-consumer-hardware* prose model
4. **Qwen 3 32B** (dense) — surprisingly strong for its size, fits 24GB GPU at Q4
5. **Mistral Small 3.1 24B** (dense) — best dialogue, fits 16GB at Q4

Below 24B dense parameters, prose quality drops off a cliff for anything you'd want to put your name on.

---

## Model Size vs. Prose Quality: The Evidence

### What benchmarks say

EQ-Bench Creative Writing v3, WritingBench, the Lechmazur Creative Story-Writing Benchmark v4, and LLM Arena Creative Writing Elo all converge on the same picture:

| Size Class | Benchmark Range | What it reads like |
|---|---|---|
| **7-8B** | 52-61% | Flat, formulaic, reads like a student assignment. Usable for outlines and brainstorming, not for prose you'd publish. |
| **13-24B** | 65-73% | Decent. Coherent scenes, basic character voice. Falls apart on long-form, subtle style emulation, sustained emotional register. Mistral 24B and Qwen 32B punch above their weight here. |
| **70B+ dense** | 80-82% | Professional-grade. Sustained voice, rich characterization, handles complex narrative structures. Llama 3.3 70B is the gold standard for dense local models. |
| **200B+ MoE** | 83-88% | Frontier. Qwen3-235B and Llama 4 Maverick match or approach Claude Opus / GPT-5 on creative benchmarks. |

### What the numbers miss

Benchmarks measure coherence, originality, character depth, plot structure. They don't measure the specific thing we care about — **resistance to AI prose patterns**. A model can score 82% on EQ-Bench and still produce "She felt a wave of grief wash over her" because that's a coherent, somewhat original, emotionally appropriate sentence. It's just also recognizably AI.

For our use case (manipulating token distributions toward grounded literary prose), model size matters for a different reason: **larger models have more diverse internal representations**. A 70B model has learned more distinct stylistic registers than an 8B model. When you try to steer it (via prompting, LoRA, contrastive decoding, or any other method), there's more to steer *toward*. The literary patterns exist in larger models' weights. In smaller models, they may not be there at all.

### The practical cutoffs

**For prompting/harness-level interventions only:**
- Minimum: **32B dense** or **70B dense** — below this, prompting can't pull the model far enough from its default register
- Ideal: **70B dense** — this is where the style-following ability crosses the threshold from "somewhat" to "reliably"

**For fine-tuning (LoRA + DPO):**
- Minimum: **70B dense** — fine-tuning a 7-13B model on literary prose helps, but the model lacks the capacity to represent the full style space. The fine-tuned model learns surface features (sentence length distribution, vocabulary shift) but can't sustain deep voice or handle complex narrative situations.
- Ideal: **70B+ dense** or **200B+ MoE** — the model has enough capacity that LoRA can shift its distribution without catastrophic forgetting of general capabilities

**For contrastive decoding / DExperts:**
- The "amateur" model should be smaller than your "expert" — using a 7B or 8B as the generic model to subtract from works with any expert model 32B+

---

## The 2026 Landscape: What's Available

### Dense Models (Simpler, More Predictable)

| Model | Params | VRAM (Q4) | VRAM (Q5) | VRAM (Q8) | Creative Ranking | License |
|---|---|---|---|---|---|---|
| **Llama 3.3 70B Instruct** | 70B | ~38 GB | ~48 GB | ~70 GB | #1 dense local | Llama 3.3 Community |
| **Qwen 3 32B** | 32B | ~18 GB | ~22 GB | ~32 GB | #2 dense local | Apache 2.0 |
| **Mistral Small 3.1 24B** | 24B | ~14 GB | ~17 GB | ~24 GB | Best dialogue | Apache 2.0 |
| **Llama 3.1 8B** | 8B | ~5 GB | ~6 GB | ~8 GB | Best under 16GB | Llama 3.1 Community |

### MoE Models (Better quality, much more VRAM for weights)

| Model | Total / Active | VRAM (Q4) | VRAM (Q5) | Creative Ranking | License |
|---|---|---|---|---|---|
| **Qwen 3.5 397B-A17B** | 397B / 17B | ~200 GB | ~270 GB | #1 open-weight creative | Apache 2.0 |
| **Qwen 3 235B-A22B** | 235B / 22B | ~118 GB | ~162 GB | #2 open-weight creative | Apache 2.0 |
| **Llama 4 Maverick** | 400B / 17B | ~200 GB | ~270 GB | Best long-form | Llama 4 Community |
| **Llama 4 Scout** | 109B / 17B | ~55 GB | ~75 GB | Good all-round | Llama 4 Community |
| **Qwen 3 30B-A3B** | 30B / 3B | ~17 GB | ~21 GB | Best budget MoE | Apache 2.0 |

**Critical note on MoE VRAM**: MoE models only *activate* a fraction of parameters per token (e.g., 17B out of 400B), which means they're fast per token. But **all parameters must be in memory** — you can't load only the active experts. So Qwen 235B needs ~118 GB even though only 22B fires per token. This makes MoE models deceptive: they're fast but hungry for memory.

---

## Quantization: What to Use

### The rule for creative writing

**Q5_K_M is the sweet spot. Q4_K_M is acceptable. Below Q4, don't bother for prose.**

Creative writing is more sensitive to quantization than coding or factual QA because:
- Prose quality depends on subtle probability differences between near-synonyms ("walked" vs. "strode" vs. "shambled")
- Quantization noise scrambles these fine-grained distinctions
- The "creative" tokens are in the probability tail — quantization flattens tails first
- MoE models are *more* sensitive than dense models (rare experts get poor calibration)

### Quality retention by quantization level

| Quant | Bits | Quality Retained | Effect on Prose | Recommendation |
|---|---|---|---|---|
| **FP16** | 16 | 100% (baseline) | None | Only if you have the VRAM |
| **Q8_0** | 8 | ~99% | Near-lossless | Best if VRAM allows |
| **Q6_K** | 6 | ~97-98% | Slight reduction in vocabulary precision | Very good |
| **Q5_K_M** | 5 | ~96% | Occasional awkward word choice under pressure | **Recommended** |
| **Q4_K_M** | 4 | ~93-95% | Noticeable loss of nuance in long-form; hedging increases | Acceptable |
| **Q3_K** | 3 | ~85-90% | Repetition, flat prose, lost voice | Emergency only |
| **Q2_K** | 2 | ~75-80% | Robotic, incoherent long-form | Not for prose |
| **IQ1/Q1.78** | ~1.7 | ~60-70% | Barely functional | No |

### K-quants vs. naive quantization

Always use K-quant variants (Q4_K_M, Q5_K_M, Q6_K) over plain Q4_0 or Q5_0. K-quants use mixed precision — they quantize less-sensitive layers more aggressively and preserve precision in sensitive layers. For creative writing, this matters significantly. The "_M" suffix (medium) is usually the right balance; "_S" (small) saves modest additional memory at a cost; "_L" (large) preserves more quality for a bit more memory.

### Format recommendations

| Format | Best for | Tooling | Notes |
|---|---|---|---|
| **GGUF** | CPU, mixed CPU/GPU, Mac | llama.cpp, Ollama, LM Studio, KoboldCpp | Most flexible, broadest hardware support, best K-quant support |
| **AWQ** | Pure GPU (NVIDIA Ampere+) | vLLM, TGI | Best Q4 quality on modern NVIDIA GPUs; activation-aware quantization preserves creative output better than GPTQ at same bits |
| **GPTQ** | Pure GPU (any NVIDIA) | vLLM, TGI, ExLlamaV2 | Mature, widely available, slightly behind AWQ at Q4 for creative tasks |
| **EXL2** | Pure GPU (NVIDIA) | ExLlamaV2 | Variable bit-width per layer; can be tuned specifically for creative tasks |
| **bitsandbytes** | Quick experiments | HuggingFace Transformers | NF4 quantization; convenient but not optimal for production |

### MoE quantization: extra caution required

MoE models degrade faster under naive quantization than dense models because:
- **Inter-expert imbalance**: Rarely-activated experts get poor calibration → garbled output when they fire
- **Intra-expert imbalance**: Token-expert affinity varies → uneven quantization error

Recent solutions (MoEQuant, ICML 2025; MiLo mixed-precision; per-expert quantization) fix this, but only if your quantized model was prepared with these methods. Standard GGUF downloads from HuggingFace may or may not use MoE-aware quantization — check the model card.

**Practical implication**: For MoE models, prefer Q5_K_M or higher. The quality gap between Q4 and Q5 is larger for MoE than for dense models.

---

## Hardware Configurations (April 2026)

### Consumer Desktop Builds

| Budget | GPU(s) | RAM | Best Model Fit | Notes |
|---|---|---|---|---|
| **Minimum viable** | 1× RTX 4090 (24 GB) | 32 GB | Qwen 3 32B @ Q4, Mistral 24B @ Q5 | Good prose, not great |
| **Sweet spot** | 2× RTX 5090 (32 GB each, 64 GB total) | 64 GB | Llama 3.3 70B @ Q5, Llama 4 Scout @ Q4 | Best cost/quality ratio for prose |
| **High-end** | 2× RTX 5090 + CPU offload | 128 GB | Qwen 3 235B @ Q4 (with offload) | Slow but frontier quality |

### Apple Silicon

| Config | Unified Memory | Best Model Fit | Notes |
|---|---|---|---|
| **M4 Max** | 48-64 GB | Llama 3.3 70B @ Q4, Qwen 32B @ Q6 | Solid prose workstation |
| **M4 Ultra** | 128-192 GB | Llama 4 Scout @ Q5, Qwen 235B @ Q4 (tight) | Best consumer option for large models |
| **M4 Ultra (maxed)** | 512 GB | Qwen 235B @ Q8, Llama 4 Maverick @ Q4 | Frontier local prose — if you have $10K+ |

### Cloud / Rental

| Provider | GPU | Cost (approx) | Best For |
|---|---|---|---|
| RunPod / Vast.ai | 1× A100 80GB | $1-2/hr | Llama 3.3 70B @ Q8, Llama 4 Scout @ Q4 |
| RunPod / Vast.ai | 2× H100 80GB | $4-6/hr | Qwen 235B @ Q5, Llama 4 Maverick @ Q4 |
| Lambda / CoreWeave | 4× H100 | $8-12/hr | Full-precision frontier models |

For fiction writing (batch, not interactive), cloud rental at $2-4/hr is extremely cost-effective. A full novel's worth of generation (200K tokens output) at 70B Q5 takes 2-4 hours.

---

## Recommendations by Use Case

### "I want the best prose possible from open weights"

**Qwen 3 235B-A22B @ Q5_K_M** on 2× H100 or M4 Ultra 192GB. This is the current open-weight creative writing champion. Apache 2.0 license means no commercial restrictions.

Stack with: detailed system prompt + LoRA fine-tune + contrastive decoding (subtract Qwen 3 3B as amateur) + Min-P sampling + Best-of-N.

### "I want the best prose I can run on a single GPU"

**Llama 3.3 70B Instruct @ Q4_K_M** on RTX 5090 32GB, or **@ Q5_K_M** on A100 80GB.

This is the proven workhorse. Dense model, well-understood quantization behavior, massive community fine-tune ecosystem (Midnight-Rose-70B and others push creative quality further).

### "I have a single RTX 4090 (24 GB)"

**Qwen 3 32B @ Q4_K_M** (~18 GB). Surprisingly good prose for its size — better than many 70B models from 2024. Or **Mistral Small 3.1 24B @ Q5_K_M** (~17 GB) if you value dialogue quality.

Add the full consumer-harness intervention stack from document 09 to compensate for the smaller model.

### "I want to fine-tune for prose style"

Start with **Llama 3.3 70B** (best LoRA ecosystem: Unsloth, Axolotl, TRL all have excellent support). Fine-tune with:
- LoRA rank 64, alpha 128
- 2000-5000 curated literary passages
- Then DPO with preference pairs (published prose preferred, model output dispreferred)

**Don't fine-tune below 32B for prose.** The capacity isn't there to learn the full style space. A fine-tuned 8B model learns surface patterns (vocabulary, sentence length) but can't sustain voice over long generations or handle novel situations.

### "I want to run contrastive decoding"

- Expert: Llama 3.3 70B (or your LoRA-tuned version)
- Amateur: Llama 3.1 8B (represents the "generic" distribution)
- logit_final = logit_70B - α × logit_8B, where α ≈ 0.5-1.0
- Both models must be in VRAM simultaneously: ~38 GB (70B Q4) + ~5 GB (8B Q4) = ~43 GB total → fits 2× RTX 4090 or 1× A100

---

## The Key Tradeoff: Model Size vs. Intervention Stack

Bigger models need less external intervention to produce decent prose. Smaller models need more intervention to compensate. But:

**A 70B model with full intervention stack (LoRA + DPO + contrastive decoding + BoN) will produce substantially better prose than a 235B model with no interventions.**

The interventions described in documents 01-08 are multiplicative with model capacity, not additive. A good model + good interventions compounds. The 70B sweet spot exists because:
- It's large enough that the literary patterns exist in the weights
- It's small enough to run locally on prosumer hardware
- It has the best fine-tuning ecosystem
- It can pair with an 8B amateur model for contrastive decoding within reasonable VRAM
- Community fine-tunes (Midnight-Rose, Fimbulvetr) already push creative quality beyond base

If you can only pick one investment — bigger model OR better intervention stack — **pick the intervention stack on a 70B base**. The stack's impact on prose quality exceeds the marginal gain of going from 70B to 235B with no interventions.

---

## Document Index

This is document 10 of the research folder. Related:
- **04**: Fine-tuning details (LoRA, DPO hyperparameters, dataset curation)
- **08**: Full practical stack architecture
- **09**: Consumer-harness interventions (for when you can't run local models)
- **03**: Contrastive decoding and DExperts (the most powerful decoding-time intervention)
- **05**: Sampling strategies (Min-P settings, Entropix)

## Key References

- EQ-Bench Creative Writing v3 Leaderboard (eqbench.com)
- Lechmazur LLM Creative Story-Writing Benchmark V4 (GitHub)
- LLM-Stats Creative Writing Rankings (llm-stats.com)
- LLM Arena Creative Writing Elo (arena.ai)
- MetriLLM Local LLM Leaderboard (metrillm.dev)
- MoEQuant: Enhancing Quantization for MoE LLMs (ICML 2025, arXiv:2505.03804)
- MoQE: Complementary Effect of Low-bit Quantization and Robustness (Microsoft Research, 2025)
- MiLo: Efficient Quantized MoE Inference with Mixture of Low-Rank Compensators (2025)
- PromptQuorum: Best Local LLMs for Creative Writing (promptquorum.com)
- BenchLM: Best LLM for Writing 2026 (benchlm.ai)
