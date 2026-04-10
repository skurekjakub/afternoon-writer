# Prose Style Guide Research Summary

## Research conducted: April 9, 2026
## Searches: 9 across 3 rounds + 1 targeted follow-up

---

## Question: What format for a prose style guide produces the best LLM fiction output?

## Findings

### 1. Three Approaches Compared

| Approach | Consistency | Voice Nuance | Token Cost | Best For |
|---|---|---|---|---|
| Sample-extracted patterns (structured JSON) | **Highest** | High | Medium (one-time extraction) | Long-form serialized fiction |
| Hand-curated rules (prose/bullets) | Moderate, brittle | Low-medium | Low | Surface-level guardrails |
| Prose sample anchors (few-shot) | High for short runs | **Highest** | High (per-chapter) | Single scenes, voice matching |

### 2. The Hybrid Wins

Every source converged: **combine all three** for optimal results.

1. **Extract patterns from samples → structured spec** (captures subtle multi-level patterns)
2. **Include 2-4 short prose excerpts → voice anchors** (grounds the LLM's actual output rhythm)
3. **Add hand-curated guardrails → kill list** (catches known failure modes)

### 3. Key Research Findings

**Sample extraction beats hand-written rules for cross-chapter consistency:**
- arxiv 2505.07888 (dual-layered template extraction) showed highest "same author" ratings when extracting patterns at both sentence and paragraph levels
- ACL 2024 (parameter-efficient style customization) confirmed that data-driven extraction captures nuances impossible to articulate manually
- IEEE 2025 style transfer survey validated the extraction approach as state-of-the-art

**Few-shot examples are more effective than rules alone:**
- LLM Flash Fiction Studies (lechmazur/writing_styles on GitHub) measured that models prompted with style examples achieved higher diversity and expressiveness in voice and narrative structure
- Latitude.so research showed few-shot examples improved style consistency significantly over instruction-only prompts
- The choice of *which* examples matters enormously — up to 12 percentage point swings in quality based on example selection (Libretto.ai research)

**Negative examples (bad samples) improve output quality:**
- Counter-Example Guided In-Context Learning (Springer, 2025) showed negative examples improve the LLM's discrimination ability
- Particularly effective for subjective/creative tasks where "avoid this" is clearer than "do this"
- Our slop-hitlist already functions as a negative example corpus

**Structured format > free text for consistency, but structured format slightly hampers creativity:**
- HumanLoop: structured output enforcement achieves ~100% schema compliance vs <40% for free text
- But Techolution's LLM Format Restriction Study showed that strict format restrictions can slightly degrade creative reasoning
- Implication: use structured JSON for the *spec*, but present it to the writer as prose-readable guidance, not as a rigid schema to fill

**Optimal sample length for voice matching:**
- 2-4 representative paragraphs (100-300 words total) for few-shot prompting
- Should cover different modes: dialogue, description, action, interiority
- Too little (<50 words) → vague style, model defaults to generic
- Too much (>1000 words in prompt) → attention collapse, diluted style matching
- Hierarchical sampling (sentence + paragraph level) outperforms flat sampling

### 4. What the Afternoon Pipeline Already Does

The afternoon style extractor (`afternoon-style-extractor.agent.md`) implements approach #1:
- Reads prose samples from config
- Extracts 16+ dimensions (sentence rhythm, vocabulary register, metaphor density, dialogue style, narrative distance, paragraph structure, scene architecture, attribution patterns, power dynamics, exposition integration, humor register, subtext density, action choreography, speculative element integration)
- Produces a `style-guide.json` (231 lines for Plague Road) with both abstract patterns and global enforcement rules
- Per-POV calibration sections for character-specific voice fingerprints

### 5. What veronica-mars.md Covers vs What's Missing

**What it has (thematic/structural — the "what"):**
- Core philosophy: sunshine noir, cynical idealist
- Narrative voice: hardboiled voiceover translated to modern teen
- Plot structure: dual-track mystery, case-of-the-week + mythology
- Pacing philosophy: information economy, escalation of danger
- Dialogue mechanics: snappy repartee, authority dynamics, pop culture as weapon
- Thematic pillars: institutional corruption, sins of the fathers, illusion of safety

**What it's missing (quantitative prose craft — the "how"):**
- Sentence length ranges and rhythm standards
- Comma density / subordination frequency
- Dialogue tag ratios (said vs action beats vs untagged)
- Paragraph length distribution
- Metaphor density caps
- Dialogue-to-narration ratios per scene type
- Attribution pattern specs
- Per-POV voice fingerprints with measurable differences

### 6. Recommendation

Build a two-layer style system for Hollow Falls:

**Layer A: `style-guides/veronica-mars.md`** (exists)
- Thematic voice, plot structure, dialogue philosophy
- Read by writer as creative direction

**Layer B: `{story_dir}/.morgana/style-spec.json`** (to build)
- Extracted quantitative patterns: sentence rhythm, tag ratios, paragraph cadence, metaphor density
- Per-POV calibration for Veronica, Dana, etc.
- Read by writer for mechanical calibration and by gate for measurable checking

**Layer C: Prose sample anchors** (to write)
- 2-4 passages (~100-300 words each) demonstrating the target voice in action
- Stored in `{story_dir}/.morgana/voice-samples.md`
- Read by writer as few-shot priming

**Layer D: Anti-pattern guardrails** (exists)
- `references/slop-hitlist.md` + `references/ai-quirks/` corpus
- Read by gate for adversarial checking

---

## Sources

1. arxiv 2505.07888 — Dual-layered template extraction for long text style transfer
2. ACL 2024, Aclanthology — Parameter-efficient LLM style customization
3. IEEE 2025 — LLM-based text style transfer survey
4. Latitude.so — How examples improve LLM style consistency
5. lechmazur/writing_styles (GitHub) — LLM flash fiction style/range mapping
6. Libretto.ai — Few-shot example selection impact research
7. Springer 2025 — Counter-example guided in-context learning
8. HumanLoop — Structured outputs compliance rates
9. Techolution — LLM format restriction study (creativity impact)
10. Noveble.com — Fiction writer's guide to LLM settings
11. Glukhov.org — Writing effective LLM prompts
12. Google Cloud — Prompt engineering guide (few-shot section)
13. Towards Data Science — Smarter prompts and LLM output
14. LessWrong — Creative writing with LLMs (prompting for fiction)
15. NovelCrafter — Fine-tuning AI for authors (sample length)
16. refsmmat.com — LLM writing styles (stylometric analysis)
17. Viktor Bezdek — Definitive guide to LLM writing styles
