# Activation Steering & Representation Engineering

## Core Concept

Representation Engineering (RepEng) intervenes directly on the internal representations (activations) of a language model during the forward pass. The key insight: **high-level concepts — sentiment, style, honesty, formality — are encoded as linear directions in the model's activation space**. If you can find that direction, you can amplify or suppress it by adding or subtracting a scaled vector from the activations at a target layer.

This is fundamentally different from prompting (which constrains the input) or fine-tuning (which changes the weights). Activation steering modifies what the model *thinks* at a specific computational stage, without the model "knowing" it's being steered.

## How It Works

### Step 1: Identify the Concept Direction

Collect paired inputs that differ only in the target concept. For prose style, this might be:

- **Positive examples**: Passages of published literary fiction (McCarthy, O'Connor, Carver)
- **Negative examples**: LLM-generated prose with typical AI patterns (hedge words, filter verbs, stock metaphors)

Run both sets through the model and record activations at each layer. The **concept vector** is the difference between the mean activations of the positive and negative sets:

```
style_vector = mean(activations_literary) - mean(activations_generic)
```

### Step 2: Apply During Generation

During inference, at the chosen layer(s), add the scaled concept vector to the residual stream:

```
activations_modified = activations_original + α * style_vector
```

Where `α` controls the steering strength. Positive values push toward the concept (more literary); negative values push away.

### Step 3: Tune the Intervention

- **Layer selection**: Different layers encode different types of information. Early layers handle syntactic patterns; middle layers handle semantic/conceptual content; late layers handle surface-level word choice. For prose style, middle-to-late layers are likely most relevant.
- **α tuning**: Too low = no effect. Too high = incoherence. Typical values range from 1.0 to 10.0 depending on the model and concept.
- **Token position**: You can apply steering at specific token positions (e.g., every token, only at sentence boundaries, only during dialogue).

## Foundational Work

### Hendrycks et al., "Representation Engineering" (2023)

The seminal paper establishing that:
1. Concepts are linearly represented in activation space (the "linear representation hypothesis")
2. Simple contrastive methods can extract concept vectors
3. Adding/subtracting these vectors reliably steers model behavior

Demonstrated on: honesty/dishonesty, happiness/sadness, safety/harmfulness. The technique generalizes — any concept that can be expressed as a contrast pair can (in principle) be extracted and steered.

**Paper**: Center for AI Safety (CAIS) research, arXiv
**Key URL**: https://www.alignmentforum.org/posts/3ghj8EuKzwD3MQR5G/

### Li et al., Inference-Time Intervention (ITI) (2023)

Focused specifically on truthfulness. Key finding: **certain attention heads are disproportionately responsible for truthful vs. hallucinatory outputs**. By identifying these heads via probing and shifting their activations along the "truthful direction," model honesty improves dramatically.

The relevance to prose: the same head-level specificity likely exists for stylistic features. Some attention heads may be disproportionately responsible for "safe generic" word choices vs. "distinctive literary" ones.

## Application to Fiction Prose: What Would This Look Like?

### The Ideal Scenario

1. **Curate contrastive datasets**:
   - **Literary set**: 500+ passages from published fiction (King, McCarthy, O'Connor, Carver, Morrison, Denis Johnson, Shirley Jackson)
   - **AI-generic set**: 500+ passages of LLM-generated fiction exhibiting typical AI patterns (matched for topic/genre)

2. **Extract "literary style" vector** at each layer by computing mean activation differences

3. **Test steering at various layers and α values** on held-out prompts, measuring:
   - Reduction in AI-pattern frequency (hedge words, filter verbs, stock metaphors)
   - Increase in sentence length variation, concrete noun density, active verb usage
   - Human evaluation of "does this read like a person wrote it?"

4. **Deploy as inference-time hook**: No model retraining needed. Can be applied/removed/adjusted per-request.

### Practical Challenges

1. **"Literary style" is not a single concept.** It's a constellation of features: verb choice, rhythm, POV discipline, metaphor density, dialogue naturalness. A single vector may capture only a subset.

2. **Interference effects.** Steering toward "literary" may inadvertently shift other qualities (topic, coherence, factual accuracy). The concept vectors are not perfectly orthogonal.

3. **Model access.** Requires access to the model's forward pass and ability to hook into intermediate layers. This works with open-weight models (Llama, Mistral, etc.) but NOT with API-only models (GPT-4, Claude) unless the provider exposes this functionality.

4. **Evaluation difficulty.** How do you objectively measure "this prose is more literary"? The concept is inherently subjective, making automated evaluation hard. Human evaluation is expensive and noisy.

### Multi-Vector Steering

A more sophisticated approach: extract **multiple** style-relevant vectors and apply them simultaneously:

- `concrete_nouns_vector` — pushes away from abstract language toward specific objects
- `active_verbs_vector` — pushes away from passive constructions and weak verbs
- `sentence_rhythm_vector` — pushes toward varied sentence length (if such a concept is linearly encoded)
- `anti_hedge_vector` — pushes away from "seemed," "almost," "slightly," "perhaps"

Each can be tuned independently. This is essentially building a "style equalizer" with per-concept knobs.

## Code & Implementation Resources

- **GitHub**: https://github.com/cma1114/activation_steering — practical examples of activation steering
- **TransformerLens** library — standard tool for hooking into model activations
- **Baukit** (David Bau's lab) — alternative toolkit for intervention experiments
- **nnsight** — newer framework for model internals intervention

## Limitations & Open Questions

1. **Scalability to frontier models**: Most RepEng work has been on 7B–70B parameter models. Whether concept vectors remain as clean and steerable in 400B+ models is unclear.

2. **Compositionality**: Adding multiple vectors simultaneously can produce unexpected interactions. The relationship between concept vectors is not always additive.

3. **Robustness**: Concept vectors extracted from one set of prompts may not generalize perfectly to all generation contexts. The vector for "literary style" extracted from third-person fiction may not help with first-person narration.

4. **The "literary style" decomposition problem**: It's unclear which aspects of prose quality are linearly represented and which require more complex (nonlinear) interventions. Sentence rhythm, for instance, may not have a clean linear direction.

## Assessment for Fiction Prose Steering

**Feasibility**: High for open-weight models. Zero for API-only models.
**Potential impact**: Medium-High. Can meaningfully shift tone and word choice.
**Ceiling**: Unlikely to fully solve the problem alone — prose quality involves too many interacting dimensions.
**Best used as**: One layer in a multi-method stack. Pairs well with DPO fine-tuning (shifts the baseline) and contrastive decoding (further sharpens at output level).
