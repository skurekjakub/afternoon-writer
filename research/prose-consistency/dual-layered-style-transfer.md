# Dual-Layered Template Extraction for Cross-Chapter Voice Consistency

## Source

Referenced in round 1 search results. The specific paper is:

**"Implementing Long Text Style Transfer with LLMs through Dual-Layered Template Extraction"**
- URL: https://arxiv.org/html/2505.07888v1
- Published: May 2025 (arXiv preprint)
- Confirmed via direct citation in web search results from Latitude.so, ACL research links, and IEEE style transfer surveys

Note: A follow-up search specifically for the paper title returned no *exact* match (the search engine may have struggled with the full title), but the paper URL was directly cited by multiple round-1 and round-3 search results as a primary source. The methodology description below is synthesized from those citations.

## Core Idea

Style transfer for long texts (multi-chapter fiction, extended documents) breaks down when you only operate at one granularity level. The paper proposes extracting style templates at **two layers simultaneously**:

### Layer 1: Sentence-Level Template
- Extracts syntactic patterns: sentence length distribution, clause structure, subordination frequency, coordination patterns
- Captures micro-rhythm: comma density, semicolon usage, fragment frequency, question frequency
- Identifies vocabulary register: formal/informal ratio, technical term density, slang patterns
- Maps attribution patterns: dialogue tag type distribution, action beat placement

### Layer 2: Paragraph-Level Template  
- Extracts macro-rhythm: paragraph length distribution, paragraph-type sequencing (dialogue → reflection → action → dialogue)
- Captures narrative distance patterns: when the prose zooms in tight vs. pulls back
- Identifies scene architecture: beat shape, escalation patterns, turn techniques
- Maps information pacing: exposition density per paragraph position, dialogue-to-narration ratio shifts across scene arc

## Why Two Layers Beat One

The paper's key finding (as cited by multiple sources):

1. **Sentence-only extraction** captures voice but loses pacing. Chapters written from sentence-level templates alone sound right line-by-line but feel wrong at the scene level — the rise and fall of tension, the alternation between dialogue runs and reflection beats, doesn't match the source.

2. **Paragraph-only extraction** captures pacing but loses voice. Chapters match the source's scene shape but individual sentences drift toward the LLM's default register — generic, analytical, hedge-wordy.

3. **Both layers together** produced the highest cross-chapter consistency in blind evaluation. Readers rated dual-layer output as "same author" significantly more often than single-layer output.

## Relevance to Our Pipeline

This validates the approach of combining:
- **Quantitative sentence-level specs** (rhythm ranges, tag ratios, comma density) — Layer 1
- **Scene-level architectural rules** (paragraph length variation, dialogue-to-narration ratio shifts, pacing patterns) — Layer 2
- **Thematic/voice rules** (what the existing `veronica-mars.md` style guide provides) — the "what to say" layer on top

The afternoon pipeline's style extractor already does both layers. Its extraction dimensions map to:
- Layer 1: `sentenceRhythm`, `vocabularyRegister`, `attributionPatterns`, `metaphorDensity`
- Layer 2: `paragraphStructure`, `sceneArchitecture`, `dialogueToNarrationRatio`, `narrativeDistance`, `actionChoreographyStyle`

## Practical Implication

For Hollow Falls (or any story), the optimal style guide combines:
1. **Prose samples** (2-4 representative passages, ~100-300 words each) — the raw material
2. **Extracted Layer 1 + Layer 2 patterns** (structured JSON) — the measurable spec
3. **Thematic voice rules** (like `veronica-mars.md`) — the creative direction
4. **Anti-pattern guardrails** (like `slop-hitlist.md`) — the kill list

The writer agent reads all four. The gate agent checks against the structured spec (layers 1+2) and the kill list.

## Related Research

- ACL 2025 accepted papers on hierarchical LLM text processing and multi-granularity style control
- IEEE 2025: "LLM-Based Text Style Transfer: Have We Taken a Step Forward?" (survey of current approaches)
- ACL 2024: "Customizing Large Language Model Generation Style using Parameter-Efficient Methods" (Aclanthology)
- Latitude.so: "How Examples Improve LLM Style Consistency" (practical validation of few-shot + extracted patterns)
- Instill AI: "The Best Way to Generate Structured Output from LLMs" (format restriction study showing structured specs > free text for consistency)
- Counter-Example Guided In-Context Learning (Springer, 2025): negative examples improve discrimination ability for avoiding LLM-typical patterns
