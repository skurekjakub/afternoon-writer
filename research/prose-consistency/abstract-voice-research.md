# Abstract Voice Problem: Research Summary

How to prevent LLMs from writing distanced, interpretive prose instead of concrete sensory detail — and why LLM-as-judge fails to catch it.

---

## The Problem (named)

The user identified a specific LLM failure mode: **the interpretive filter**. Instead of describing what something LOOKS LIKE, the LLM describes what something MEANS.

Examples of the pattern:
- "arranged his face into the expression officials wore when they meant to pass off fear as routine" — TRIPLE abstraction: "the expression" (not what the face looks like), "officials wore" (categorical generalization, not this specific person), "when they meant to pass off fear" (interpreting intent, not showing behavior)
- "the corridor is to be believed" — narrator commenting on reliability of evidence rather than describing what the corridor shows
- "the kind of smile that didn't reach her eyes" — labeling the smile's quality instead of describing what the mouth and eyes are doing
- "something shifted in her expression" — vague pointer to a change without specifying the change

**Why this is the #1 quality problem:** It passes all surface-level checks. The grammar is correct. The sentences are well-formed. The vocabulary is varied. The pacing works. It even SOUNDS literary. But it's empty — the reader can't SEE anything. An artist couldn't draw it.

---

## Why LLMs Do This

### 1. Regression to the Mean (Galton's Law of Mediocrity)
LLMs predict the most probable next token. Creative features — unusual metaphors, stark physical imagery, surprising verbs — are LOW probability. The model's default is the statistical center: competent, fluent, generic. Abstract interpretation is safer than specific description because it's more common in training data.

Source: arxiv 2509.25767 — "Galton's Law of Mediocrity: Why Large Language Models Regress to the Mean"

### 2. Training Data Bias
Modern literary fiction increasingly privileges internal states and interpretation over physical "show don't tell" description. MFA-influenced prose favors the interpretive lens. The LLM absorbed this trend and reproduces it as default register.

Source: OpenAI Community — "The Role of Interpretation in Great LLM Outputs"

### 3. Architectural Bias
Higher/final layers of transformer architectures where summary and abstraction are strongest dominate output generation. Lower layers encode more concrete, detailed representations. The model's output stage is literally the abstraction layer.

Source: arxiv 2408.08769 — "Lower Layers Matter: Alleviating Hallucination via Multi-Layer Fusion"

### 4. Efficient Compression
"She looked afraid" is fewer tokens than describing flushed cheeks, widened pupils, the grip tightening on the steering wheel, breath going shallow. The LLM takes the compression shortcut — abstraction is information-dense but experience-poor.

---

## Why LLM-as-Judge Fails to Catch It

### 1. Same Blind Spot
The judge LLM shares the same training data bias. If interpretive prose is the statistical default in its training corpus, it reads as "normal" and passes review. The judge literally cannot distinguish between "literary" abstraction and lazy abstraction because they use the same patterns.

Source: ACL 2025 — "LLM-as-a-Judge Failures at Automating the Identification of Poor Quality Content"

### 2. Fluency ≠ Quality
LLM judges confuse grammatical correctness and sophisticated vocabulary with storytelling quality. "Arranged his face into the expression officials wore" is grammatically perfect, syntactically complex, and uses varied vocabulary — all positive signals to a judge evaluating surface quality.

### 3. Can't Detect Absence
The judge can detect what IS there (slop patterns, repetition, POV breaks). It struggles to detect what ISN'T there — missing sensory detail is an absence, not a presence. You can't grep for something that should exist but doesn't.

### 4. No Visual Test
Human readers instinctively apply the "can I see this?" test. LLMs process text as token sequences and cannot perform the equivalent visual-cortex check. There's no grounding to a physical world.

Source: IBM Research — "Beyond Blind Spots: Analytic Hints for Mitigating LLM-Based Evaluation Pitfalls" — found that LLM judges alone achieve <50% error coverage on nuanced issues; combined with rule-based analytic tools, >90%.

---

## Mitigation Strategies (ranked by effectiveness)

### A. Negative/Positive Example Pairs in Writer Priming (HIGHEST IMPACT)

Give the writer agent 3-5 bad/good pairs demonstrating the EXACT pattern. Few-shot examples shift token distribution more than rules.

**Pair 1 — Facial expression:**
- BAD: "She arranged her face into the expression people use when they want to seem unbothered."
- GOOD: "She unclenched her jaw. Dropped her shoulders an inch. Held the coffee cup with both hands so they wouldn't shake."

**Pair 2 — Environment:**
- BAD: "The corridor spoke of institutional neglect."
- GOOD: "Water stain on the ceiling tile. One fluorescent tube dead. The fire extinguisher case had a yellowed inspection tag from 2001."

**Pair 3 — Emotional state:**
- BAD: "Something in her expression shifted, carrying the weight of years of unspoken grievance."
- GOOD: "Her mouth thinned. She set down the fork — carefully, the way you set things down when what you really want to do is throw them."

**Pair 4 — Body in space:**
- BAD: "She moved with the kind of deliberation that suggested she was very aware of being watched."
- GOOD: "She walked like she had a ruler taped to her spine. Chin up, steps even, not looking at anyone. She was performing for the whole room and the whole room knew it."

**Pair 5 — Reaction:**
- BAD: "The news hit her with the force of something she'd been expecting but hadn't prepared for."
- GOOD: "She sat down. Not in a chair — just down, right there on the kitchen floor, the linoleum cold through her jeans."

### B. Analytic Hints for the Gate Agent (HIGH IMPACT)

Add a specific check to the gate: the **Artist Test**.

> "For every description of a face, body, posture, room, or object — could an artist draw it from the description? If the prose says 'the expression of someone who...' or 'the kind of [X] that...' or 'something about the way she...', it FAILS. The description must land on WHAT IT LOOKS LIKE, not what it communicates."

Concrete flag patterns for the gate:
- "the expression of someone who..." → FLAG
- "the kind of [noun] that..." → FLAG
- "something about [noun]" → FLAG
- "the way [pronoun] [verb]ed suggested..." → FLAG
- "as if [abstract interpretation]" → FLAG (when following a physical description)
- "[noun] spoke of / suggested / betrayed / revealed" → FLAG (inanimate subjects performing interpretation)

### C. Chain-of-Thought Sensory Decomposition (MEDIUM IMPACT)

Before writing a scene, the writer generates a sensory inventory for each beat:
- What does the POV character SEE? (specific objects, colors, textures)
- What do they HEAR? (ambient, specific, volume)
- What do they FEEL? (skin, temperature, weight, pain)
- What do they SMELL? (name the smell)

Then write from the inventory. This forces concrete tokens into the context before prose generation begins.

**Trade-off:** Adds latency and token cost. Works well for key scenes, too expensive for every beat.

### D. Voice Samples as Anchors (MEDIUM IMPACT)

The voice samples just written for Hollow Falls already demonstrate the correct pattern — concrete, specific, grounded. Having these in the writer's context during generation helps steer output toward the demonstrated register.

**Why this works:** The few-shot samples are more powerful than rules because they shift the entire probability distribution. The writer generates text that "continues" the established pattern rather than reverting to its training default.

### E. Post-Hoc Targeted Rewrite Pass (MEDIUM IMPACT)

After generation, run a targeted pass: "Find every sentence where a facial expression, body posture, or room is described through interpretation rather than appearance. Rewrite each one to describe WHAT IT LOOKS LIKE."

This works better than trying to prevent the pattern because it's easier to detect and fix after the fact than to suppress during generation.

### F. Outline-Level Sensory Anchors (ALREADY DONE)

The expanded outline format already includes sensory anchors per beat. This pre-seeds concrete detail into the writer's context. Already implemented for Hollow Falls chapters 1-4.

---

## Recommended Pipeline Changes

### For the Writer Agent (`ravencrest-prose-writer.agent.md`)
1. Add the 5 bad/good pairs to the priming section
2. Add a one-line rule: "The Artist Test: every description of a face, body, or room must be drawable. If you can't draw it, rewrite it."
3. Read `voice-samples.md` before writing (already flagged)

### For the Gate Agent (`ravencrest-prose-gate.agent.md`)
1. Add Check #8: "Interpretive Filter" — the Artist Test with the 6 flag patterns listed above
2. Add the bad/good pairs as calibration examples so the gate knows what it's looking for
3. Weight this check heavily — it's the hardest for the judge to detect, so it needs explicit help

### For the Outline Format
1. Already has sensory anchors — no change needed
2. Consider adding a "Camera" field per beat: "What is the camera showing?" Forces concrete visual thinking at the planning stage

---

## Key Sources

1. arxiv 2509.25767 — Galton's Law of Mediocrity (regression to mean in LLMs)
2. arxiv 2408.08769 — Lower Layers Matter (architectural bias toward abstraction)
3. ACL 2025 — LLM-as-a-Judge Failures (why judges miss nuanced quality problems)
4. IBM Research — Beyond Blind Spots (analytic hints boost judge coverage from <50% to >90%)
5. Google Wordcraft Writers Workshop (professional writers found LLM output "bland" and "formulaic" on sensory detail)
6. HuggingFace 2601.08003 — LLM Review via Blind Peer Review (multi-agent review outperforms single-judge)
7. LessWrong — Creative Writing with LLMs Part 1 (iterative refinement strategies)
