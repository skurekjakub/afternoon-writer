# Grounding Investigation Log

## Scope

Investigate how to refine the afternoon pipeline's grounding quality without making code changes yet.

Primary problem statement:
- The current slop removal is doing decent work.
- The grounding pass still leaves holes.
- Dialogue grounding appears under-served.
- Grounding may weaken toward the end of longer chapters.
- A future grounding gate or multi-pass loop is on the table, but prompt architecture is still open.

Benchmark note from user:
- `chapter12/final-grounded-gpt-negative.md`
- `chapter12/final-grounded-gpt-negative-v2.md`

These are currently considered the highest-quality grounding variants.

---

## Local Context Ingested

Files read so far:
- `external-resources/ai-prose-grounding-primer.md`
- `.github/skills/prose-grounding-framework/SKILL.md`
- `.github/agents/afternoon-grounder.agent.md`
- `.github/skills/afternoon-pipeline/references/architecture.md`
- `.github/skills/afternoon-pipeline/references/agents.md`
- `.github/skills/afternoon-pipeline/references/config.md`
- `.github/skills/afternoon-pipeline/references/memory-system.md`
- `docs/afternoon-pipeline-architecture.md`
- `docs/afternoon-pipeline-technical.md`
- `.github/agents/afternoon-orchestrator.agent.md`
- `.github/skills/afternoon-pipeline/references/running.md`
- `.github/skills/afternoon-pipeline/references/troubleshooting.md`

Chapter artifact inventory checked:
- `.afternoon/chapters/chapter12/`

Observed experiment outputs in `chapter12/`:
- `final-grounded-gpt-negative.md`
- `final-grounded-gpt-negative-v2.md`
- `final-grounded-opus-negative.md`
- `final-grounded-gemini-negative.md`

Grounder notes inspected:
- `grounder-notes.json`
- `grounder-notes-gpt-negative.json`
- `grounder-notes-gpt-negative-v2.json`

Word counts captured:
- `v2.md`: 5069
- `final.md`: 3972
- `final-grounded-gpt-negative.md`: 4654
- `final-grounded-gpt-negative-v2.md`: 4019
- `final-grounded-opus-negative.md`: 4188
- `final-grounded-gemini-negative.md`: 4318

---

## Current Understanding of the Pipeline Surface

- Grounder sits after slophunter/slop-gate and before expander.
- Current grounder prompt is exemplar-driven, not rubric-driven.
- The grounding framework already carries strong negative constraints:
  - protect rhythm
  - protect subtext
  - avoid wiki dialogue
  - passive reality only
  - invisible verb rule
  - contact rule
- The skill also already mentions useful extensions:
  - sensory rotation
  - wear-and-tear / palimpsest
  - temporal and ecological anchoring
  - institutional friction
  - action-driven dialogue tags

This means the next improvement likely is not "invent grounding from scratch," but tighten:
- coverage
- enforcement
- passage selection
- dialogue-specific instructions
- long-text reliability
- evaluation loops

---

## Initial Observations

1. The framework already knows many of the right things, but its enforcement is soft.
2. The current architecture relies on a single grounding pass with self-audit; there is no adversarial verification stage equivalent to slop-gate.
3. The skill warns against front-loading grounding, which matches the user's observation that later sections may degrade.
4. The highest-quality variants appear to be relatively surgical, which suggests that "more detail" is not the real goal; better placement and better scene-selection probably matter more.
5. Dialogue grounding is explicitly mentioned in the skill, but only as one rule among many. It may need dedicated prompt space or a dedicated audit dimension.

---

## Working Hypotheses To Test

1. The grounding prompt needs a stronger scene-by-scene coverage contract, not just exemplar absorption.
2. Dialogue needs its own grounding checklist so world specificity enters speech-adjacent action beats and shared shorthand naturally.
3. Long chapters may need chunked grounding or explicit end-of-chapter audits to prevent attention drop-off.
4. A grounding gate may help, but only if it audits concrete failure modes instead of giving vague "more grounded" feedback.
5. The best future design may be a hybrid:
   - better grounding skill structure
   - targeted passage-level grounding rubric
   - optional grounding gate / revision loop
   - chapter-length-aware chunking

---

## Open Questions For User

- Which lane matters most first: prompt structure, gate design, dialogue grounding, or long-chapter reliability?
- Should chapter12 remain the benchmark comparison set?
- Should the eventual recommendation optimize for absolute quality, runtime cost, or both?

---

## Planned Next Additions

- User-priority clarification
- Five web research rounds on grounding methods, dialogue grounding, long-form revision reliability, and chunking
- Sample-passage inspection from chapter12 beginning vs ending sections
- Refinement options for:
  - grounder prompt
  - grounding framework skill
  - possible grounding gate
  - chunking / sectioned passes

---

## User Preference Lock

User-selected focus:
- Primary lane: prompt and skill structure
- Secondary lane: dialogue grounding
- Benchmark scope: chapter12 GPT-negative variants plus current canonical files
- Optimization target: maximum quality even if runtime grows

---

## Web Research Rounds

### Round 1 - Grounding AI-generated fiction prose

Recurring advice:
- run explicit grounding-only passes instead of trying to fix everything at once
- use white-room checks / white-space passes to find paragraphs with no spatial or sensory anchors
- use reverse outlines or scene sketches to verify that every scene has a concrete location and physical situation
- add microblocking and stage business so people move through space instead of floating in it
- prefer concrete nouns over abstract summary

Useful links:
- https://rephrasely.com/blog/how-to-humanize-ai-text
- https://www.creativindie.com/how-to-humanize-chatgpt-written-content-for-better-fiction-and-to-pass-ai-detection/
- https://plotforge.app/blog/ai-book-editing-tool

### Round 2 - Dialogue grounding

Recurring advice:
- action beats should carry subtext, not just speaker attribution
- dialogue feels grounded when characters handle objects, shift position, or react physically while speaking
- setting interaction should reflect stakes, not random filler business
- shared context should stay implicit; grounding should sit in beats around the speech, not lore explanations inside the speech

Useful links:
- https://www.writersdigest.com/write-better-fiction/using-beats-to-improve-dialogue-and-action-in-scenes
- https://allwritealright.com/action-beats-what-they-are-and-how-to-use-them/
- https://writershelpingwriters.net/2026/03/story-beats/

### Round 3 - White-room syndrome craft guidance

Recurring advice:
- anchor scene location early, then re-weave reminders throughout the scene
- route setting through POV-specific noticing rather than generic description
- use setting as friction, obstacle, and tension source
- rotate senses rather than relying only on visual detail

Useful links:
- https://www.tckpublishing.com/white-room-syndrome-what-it-is-and-how-to-fix-it/
- https://thelittlebookish.com/blogs/news/white-room-syndrome
- https://whisleredits.com/blog/b/erasing-white-room-syndrome-from-your-scenes

### Round 4 - Long-context degradation and chunking

Recurring findings:
- long-context models show primacy and recency bias with weaker utilization of middle or buried detail
- context length alone can hurt quality, even when retrieval succeeds
- practical mitigations include chunking, rolling windows, reranking important material up front, and stepwise "recite-then-solve" style workflows
- for this pipeline, that suggests sectioned grounding with per-section restatement of active needs may beat one monolithic chapter pass

Useful links:
- https://arxiv.org/abs/2307.03172
- https://nickbermingham.com/2025/01/paper-review-lost-in-the-middle-how-language-models-use-long-contexts-november-2023/
- https://arxiv.org/abs/2510.05381

### Round 5 - Critic loops / gate workflows

Recurring findings:
- best results come from clear role separation: generator, critic, optional gate
- critique loops work best when feedback is structured, local, and actionable
- max-iteration loops plus explicit pass criteria are standard
- multi-critic patterns can improve reliability over a single subjective judge

Useful links:
- https://aclanthology.org/2024.findings-emnlp.458/
- https://learn.microsoft.com/en-us/semantic-kernel/frameworks/process/examples/example-cycles
- https://openreview.net/forum?id=tciQfO8S8j

---

## Benchmark Passage Audit - Chapter12

Files spot-checked:
- `final.md`
- `final-grounded-gpt-negative.md`
- `final-grounded-gpt-negative-v2.md`

Areas spot-checked:
- opening section
- mid-dialogue argument section
- ending approach / Sylvanas arrival section

### Opening findings

- Both GPT-negative variants improve the opening materially.
- The original GPT-negative variant is the richest: stronger material texture, more room-specific nouns, sharper institutional carryover.
- The v2 variant is cleaner and more disciplined, but still clearly more grounded than canonical `final.md`.

### Mid-dialogue findings

- The strongest improvements come from dialogue-adjacent narration:
  - cuffs
  - chalk dust
  - shelves
  - sigils
  - roads / village residue
- The spoken lines themselves remain mostly conceptual and adversarial rather than materially grounded.
- This supports the idea that dialogue grounding needs a dedicated prompt lane, not just generic "add world specificity."

### Ending findings

- The original GPT-negative variant keeps stronger late-scene anchors:
  - Darrowmere
  - buried chain under Scholomance
  - iron door
  - road grit
  - specific threshold behavior
- The v2 variant is more surgical, but some late nouns become more generic:
  - `water`
  - `floor`
  - `body`
  - `stone`
- That does not prove long-context degradation by itself, but it does support the user's sense that later sections are at risk of lighter grounding or over-compression.

### Benchmark takeaway

There is a real tradeoff visible already:
- richer grounding prompt -> better environmental texture and more late-scene carry-through
- more surgical prompt -> better rhythm discipline and less bloat, but easier fallback into generic nouns

The next design should probably aim for:
- GPT-negative-level specificity
- v2-level discipline
- stronger late-chapter coverage checks
- a dedicated dialogue-grounding contract

---

## Preliminary Refinement Directions

### 1. Tighten the grounder prompt into explicit scene contracts

Instead of "study the exemplar and ground the chapter," require per scene:
- one place/infrastructure anchor
- one material/contact anchor
- one POV-specific noticing anchor
- one dialogue-adjacent grounding beat where dialogue is present
- one late-scene / scene-exit anchor if the scene hands off into another pressure beat

### 2. Add a dedicated dialogue grounding sub-pass

The current prompt treats dialogue grounding as one rule among many. A stronger structure would force a second pass that asks:
- where are characters speaking without touching the world?
- where can object handling, position shifts, or environmental interruptions carry subtext?
- where is dialogue using abstract conflict language without any material counterweight nearby?

### 3. Add segment-level coverage checks

Potential checks:
- first third / middle third / final third anchor parity
- count paragraphs with no concrete environmental or object anchors
- count dialogue runs longer than N lines without action / object / spatial interruption
- inspect the final 20 percent of the chapter separately before signoff

### 4. Consider sectioned grounding for long chapters

Potential workflow:
- read scene map
- ground scene or chunk
- write immediately
- carry forward only a small rolling summary of active nouns / institutions / dialogue state
- do a final coverage audit over all chunk endings and the last chunk specifically

### 5. If a grounding gate is added, make it concrete

A useful gate should not say "more grounded."
It should audit specific failure classes:
- white-room paragraphs
- dialogue float
- generic noun clusters where canon-specific nouns are available
- late-chapter anchor drop
- lore-dump violations
- over-grounding / wiki spill

The gate should emit local suggested fixes, the same way slop-gate does, or it will create mushy revision loops.

---

## Additional Benchmark - Chapter14

Files spot-checked:
- `final.md`
- `final-grounded-gpt-negative-v2.md`
- `grounder-notes-gpt-negative-v2.json`

Quick profile:
- `final.md`: 2168 words / 321 lines
- `final-grounded-gpt-negative-v2.md`: 2938 words / 339 lines
- reported growth: 35.6 percent

What chapter14 adds to the picture:

1. The pass is stronger all the way through.
   - Opening road texture is materially sharper.
   - Relay scenes pick up institutional and object-contact detail naturally.
   - Final run to Stratholme stays grounded through bells, lather, windows, smoke, lanes, and horse pressure.

2. Dialogue grounding is still mostly beat-adjacent rather than line-internal.
   - This repeats the chapter12 pattern.
   - The dialogue feels better because the surrounding scene is more mobile and object-rich, not because the system has solved dialogue grounding directly.

3. Shorter chapter length appears to help.
   - Chapter14 is about half the size of chapter12 and shows less obvious late-section generic fallback.
   - This supports a chunking or section-audit design for longer chapters.

Control-case takeaway:
- Longer, more static, concept-heavy chapters probably need stronger coverage enforcement.
- Shorter, more mobile chapters can get farther on the current prompt, especially when route, relay, and object nouns are naturally available.
