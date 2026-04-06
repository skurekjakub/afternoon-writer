# Attention Decay & Context Rot in LLM Prose Generation

## Summary
LLMs exhibit systematic quality degradation as context length increases. This directly impacts any agent processing long chapters — grounding instructions, style rules, and exemplar patterns receive progressively less attention as the model generates more text.

## Key Findings

### "Lost in the Middle" (Stanford, Liu et al., 2023)
- LLMs attend strongly to the beginning and end of their context window, but weakly to the middle
- Performance on multi-document QA and key-value retrieval degrades significantly when relevant information is in the middle of the context
- GPT-4 and Claude 2.1 both showed worse needle-in-a-haystack performance as context grew — especially for needles placed in the middle of the document
- Effect worsens with harder tasks: when retrieval requires reasoning "hops" (e.g., connecting two facts), accuracy drops even faster with longer context

### Context Rot (Anthropic Engineering Blog, 2025; Chroma Research, 2025)
- "Context must be treated as a finite resource with diminishing marginal returns"
- Every new token added depletes the model's "attention budget"
- Context rot = LLMs become less effective as context grows, because attention is stretched thin
- The transformer architecture's fundamental design (every token attends to every other token) creates this tension between context size and attention focus
- Anthropic recommends "context engineering" — carefully curating which tokens enter the context window

### Six Mechanisms of Long-Document Quality Degradation (Vatsa, 2025)

1. **Attention Drift**: LLMs pay 2-4x more attention to recently generated content than source material when generating later text. Bias coefficients of 2.1–3.8 across major architectures.

2. **Memory Constraints**: Quadratic computational complexity (O(n²)) with sequence length. At 32K tokens, attention computation alone requires ~156GB memory, forcing shortcuts.

3. **Positional Bias ("Lost in the Middle")**: Causal masking mechanisms inherently bias attention toward earlier positions. RoPE and ALiBi positional encodings compound this effect.

4. **Cascade Error Propagation**: Small deviations early compound into larger drift later. Token predictability increases to 90-91% as context accumulates, reducing the model's flexibility to self-correct.

5. **Context Degradation**: Over 5K tokens, pronoun resolution accuracy drops from 65% to 34%. Entity tracking consistency drops from 78% to 41%. Cross-reference validation drops from 82% to 29%.

6. **Computational Complexity**: Quadratic attention cost forces models into approximations that reduce accuracy, especially for longer sequences.

### Practical Thresholds
- Performance degrades noticeably above 30-50% of max context window
- Multi-hop reasoning (connecting facts that require inference) degrades faster than simple retrieval
- Adobe research (2025): GPT-4o accuracy drops from 99% to 70% going from short to 32K token context; Claude 3.5 Sonnet drops from 88% to 30%

## Implications for the Afternoon Pipeline Grounder

### Problem
The grounder currently processes an entire chapter in a single agent call. The priming stack (exemplars, anti-bloat rules, source-verification principles, materials) sits at the beginning of the context. As the grounder processes later scenes:
- Grounding rules receive diminishing attention
- The model increasingly references its own recent output rather than the priming exemplars
- Sensory rotation, POV filtering, and source verification become less disciplined
- The model may default to high-probability generic patterns instead of world-specific substitutions

### Evidence
- Chapter 12 analysis: grounding density is highest in Scene 1 (14 touches) and Scene 2 (28 touches) but drops in Scene 3 (10 touches), despite Scene 3 being the climactic revelation
- The grounder-notes.json for chapter 14 shows 70% word growth overall, but the distribution across scenes varies significantly

### Mitigation: Per-Scene Processing
Break chapter processing into per-scene subagent calls, each receiving the full priming stack fresh. This resets the attention budget for every scene.

Trade-offs:
- **Cost**: More API calls (3-5 per chapter instead of 1)
- **Continuity risk**: Cross-scene transitions may have seam artifacts
- **Benefit**: Each scene gets ~1-2K words of focused grounding with fresh priming, eliminating attention decay

### Mitigation: Re-Priming Checkpoints (Alternative)
If per-scene calls are too expensive, insert explicit "re-read these rules now" checkpoints between scenes within a single agent call. Less reliable (the model may not truly refresh attention) but cheaper.

## Sources
- Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (arxiv.org/abs/2307.03172, 2023)
- Anthropic, "Effective Context Engineering for AI Agents" (anthropic.com/engineering, 2025)
- Chroma Research, "Context Rot" (research.trychroma.com/context-rot, 2025)
- Vatsa, "Managing LLM Hallucinations in Long Document Processing" (Medium, 2025)
- Lee, "Context Rot: The Emerging Challenge" (understandingai.org, 2025)
- Adobe Research, Multi-hop reasoning in long contexts (arxiv.org/abs/2502.05167, 2025)
