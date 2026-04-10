# Sparse Autoencoder Feature Steering

## Core Concept

Sparse Autoencoders (SAEs) are a mechanistic interpretability tool that decomposes a model's activations into **individual, interpretable features**. Unlike raw neurons (which are polysemantic — each neuron fires for many unrelated concepts), SAE features are designed to be **monosemantic**: each feature corresponds to a single, identifiable concept.

The steering application: once you've identified features that correspond to undesirable patterns (e.g., "hedge word usage," "passive voice preference," "stock metaphor generation"), you can **clamp, amplify, or suppress** individual features during inference. This is activation steering with surgical precision — instead of shifting the entire activation space along a single direction, you intervene on specific, identified features.

## How SAEs Work

### Training the SAE

1. Collect activations from a target layer of the LLM across a large, diverse corpus
2. Train a sparse autoencoder: an encoder that maps activations to a **high-dimensional, sparse** latent space, and a decoder that reconstructs the original activations
3. The sparsity constraint forces the autoencoder to learn features where each latent dimension corresponds to a single, coherent concept
4. The result: a "dictionary" of features, each of which fires on a specific type of input and can be individually manipulated

### Feature Identification

After training, each feature can be analyzed:
- **Max-activating examples**: Which inputs cause this feature to fire most strongly?
- **Ablation studies**: What happens to the model's output when this feature is removed?
- **Manual labeling**: Researchers inspect the max-activating examples and assign interpretable labels

Anthropic's 2024 "Scaling Monosemanticity" work extracted features from Claude 3 Sonnet and found interpretable concepts like:
- "San Francisco" / "Golden Gate Bridge"
- "Code syntax errors"
- "Sycophantic agreement"
- "Deceptive reasoning"
- Specific languages, topics, entities, and behavioral patterns

## The Golden Gate Claude Demonstration

In May 2024, Anthropic demonstrated **feature clamping** by finding the "Golden Gate Bridge" feature in Claude 3 Sonnet's SAE and clamping it to maximum activation during generation. The result: Claude became obsessed with the Golden Gate Bridge, inserting it into every response regardless of topic.

This was a vivid proof of concept: **individual features can be clamped to arbitrary values, and the model's behavior changes predictably and dramatically.**

The relevance to prose: if you can find features corresponding to AI writing patterns, you can suppress them. If you can find features corresponding to literary quality markers, you can amplify them.

**Key URL**: https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html

## Application to Fiction Prose

### What Features Would We Need to Find?

**Features to SUPPRESS (AI writing patterns):**
- Hedge word generation ("seemed," "almost," "slightly," "perhaps," "somewhat")
- Filter verb usage ("noticed," "realized," "observed," "registered")
- Stock metaphor patterns ("wall," "armor," "mask" as emotional metaphors)
- Adverb-heavy construction preference
- Passive voice default
- "Not X; Y" dramatic negation structure
- Explanatory narrator voice (telling rather than showing)
- Melodramatic simile generation
- Stacked adjective clusters

**Features to AMPLIFY (literary quality markers):**
- Concrete noun preference
- Active, specific verb selection
- Sentence length variation
- Dialogue naturalness / colloquial speech patterns
- Sensory detail generation
- Subtext in dialogue (characters not saying what they mean)

### The Challenge: Feature Granularity

Anthropic's SAE on Claude 3 Sonnet found ~34 million features. Many are very specific ("mentions of the Eiffel Tower") while others are more abstract ("formal academic register"). The question is whether features at the right level of granularity exist for prose quality:

- **Too specific**: A feature for "uses the word 'seemed'" is trivially useful but insufficient — the problem isn't one word, it's a *pattern* of hedging.
- **Too abstract**: A feature for "good writing" might not exist as a single monosemantic concept — it's too multidimensional.
- **Just right**: A feature for "hedge-word linguistic pattern" or "filter-verb construction" would be ideal, but whether these emerge as monosemantic features is an empirical question.

### Practical Workflow

1. **Train an SAE on your target model** (e.g., Llama 3, Mistral, or another open-weight model you're using for fiction generation)
2. **Identify features** by:
   - Running AI-generated prose through the model and finding strongly activating features
   - Running published fiction through and finding those features
   - Looking for features that activate differentially (high for AI prose, low for literary; or vice versa)
3. **Build a steering profile**: A list of features to clamp/suppress/amplify and by how much
4. **Apply during generation**: Hook into the SAE feature space at the target layer and apply the clamping at each forward pass

### Existing Tools & Resources

- **Anthropic's SAE releases**: Trained SAEs for Claude models, but these require Anthropic API access for the underlying model
- **OpenAI's SAE work**: Similar research direction, limited public tooling
- **EleutherAI / Open-source SAEs**: Community efforts to train SAEs on Llama, Mistral, and other open-weight models
- **SAELens** (by Joseph Bloom): Open-source library for training and analyzing SAEs — https://github.com/jbloomAus/SAELens
- **Google PAIR interactive explainer**: https://pair.withgoogle.com/explorables/sae/

### Key Paper: "Enabling SAEs for Topic Alignment" (OpenReview, 2024)
Demonstrated that SAE-based steering can enforce topic adherence — a simpler problem than style adherence, but proof that the approach works for controlling generation properties.

### Key Paper: "SRPS: Sparse Autoencoder Role-Playing Steering" (2024)
Used SAE features to steer models into maintaining consistent character personas during role-play — directly relevant to fiction, where voice consistency matters.

### Key Paper: "Toward Efficient SAE-Guided Steering for Improved In-Context Learning" (EMNLP 2025)
Addressed efficiency concerns — SAE-based steering adds computational overhead. This paper demonstrates methods to reduce that overhead while maintaining steering effectiveness.

## Limitations

1. **Computational cost of SAE training**: Training an SAE on a large model requires significant compute. For a 70B model, this is a substantial project.

2. **Feature coverage**: Not all concepts may decompose into monosemantic features. Complex, multidimensional concepts like "prose quality" may require combining many features, at which point you're back to the compositionality problem.

3. **Model specificity**: An SAE trained for Llama 3 70B won't work for Mistral Large or any other model. You need a new SAE per model (and potentially per model version/checkpoint).

4. **The "literary quality" decomposition**: It's fundamentally unclear whether the aspects of prose that distinguish literary fiction from AI slop are represented as discrete, steerable features, or whether they're distributed across the model in ways that resist clean SAE decomposition.

5. **No API access**: Like activation steering, this requires forward-pass access to the model. Doesn't work with API-only providers.

## Assessment

**Feasibility**: Medium. Requires significant infrastructure (SAE training, feature analysis, integration).
**Potential impact**: High — if the right features can be found, the control is extremely precise.
**Maturity**: Early. Most SAE work focuses on safety/alignment, not creative quality.
**Best used as**: A research investment. If you're committed to running your own open-weight models for fiction generation, this is the most promising path for fine-grained control.
**Key bottleneck**: The empirical question of whether "AI prose patterns" decompose into steerable SAE features.
