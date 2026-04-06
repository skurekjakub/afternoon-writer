---
name: prose-grounding-framework
description: "World-specificity grounding by paired exemplars. Read the before/after reference pairs in references/, absorb the transformation, and apply that same grounding move to the target prose. No category taxonomy — the references are the teaching surface."
---

# Prose Grounding Framework

Grounding means making every sentence feel like it happens in this world, not a generic one. Clean prose that could belong to any setting becomes prose saturated with named geography, titled institutions, specific materials, world-register vocabulary, infrastructure, and physical texture.

This skill teaches grounding by example, not by taxonomy.

## The references

The lesson lives in the paired examples under `references/`. That directory is the source of truth. The exact set of pairs may change over time, so do not rely on a hardcoded list in this skill.

Before touching the target prose:

1. Read all pairs in `references/`.
2. Study the delta, not just the finished version. The difference between before and after is the job.

The pairs show grounding operating on every surface at once: nouns, dialogue, internal monologue, action beats, environmental rhythm, institutional vocabulary, and material texture. You read the chapter, you feel where it is floating, and you anchor it the way the references anchor their prose.

Wordcount bloat is not the goal. Do not try to match any specific expansion ratio from the references. Add only where the scene naturally wants more specificity. Some grounding passes grow a chapter substantially; some are mostly surgical replacements.

## What to learn from the pairs

- Grounding is not just adding lore nouns. It is making the prose inseparable from its setting.
- The strongest changes are usually local and embodied: what the POV notices, touches, names, avoids, or takes for granted.
- Good grounding often comes from substitution plus light extension, not from wholesale paragraph replacement.
- Dialogue should pick up local register and shared context without turning into explanation.
- The scene should feel more physically lived in, not more documented.

## PRESERVE SUBTEXT AND PACING (NEGATIVE CONSTRAINTS)

AI text generation inherently leans toward over-explanation, which destroys narrative tension, subtext, and pacing. While performing the grounding pass, you MUST obey these strict negative constraints:

1. **The Anti-Bloat Rule (Protect Rhythm):** You are strictly forbidden from altering the rhythm or syllable weight of high-tension scenes. If the original text uses a short, staccato sentence or a fragment (e.g., "Host. Altered."), do not expand it into a full sentence or append dependent clauses. Grounding must occur strictly through 1:1 noun/adjective replacement. You can enrich scene settings and descriptions (as filtered through POV).

2. **The Anti-Spoonfeeding Rule (Protect Subtext):** Never explicitly state the subtext of a scene. If a character's physical reaction or observation implies a realization, do NOT add a sentence explaining what they realized or who they are thinking about. Trust the reader to connect the dots. 

3. **The Anti-Wiki Rule (Protect Dialogue):** Do not inject lore terms, faction names, or proper nouns into dialogue if the speaking characters already share that context. Characters in high-stakes situations speak in shorthand. They do not explain their own world to one another.

4. **The "Passive Reality" Rule:** Worldbuilding must exist as a passive physical or operational reality that characters interact with. You may not add narrator exposition to explain the history, significance, or mechanics of a grounded term.

5. **The "Invisible Verb" Rule (Anti-Jargon Overload):**
Do NOT replace standard functional verbs or nouns (e.g., speak, look, answer, walk, word, result) with domain-specific jargon (e.g., cast, scry, chant, teleport, noun, sum) unless the character is literally performing that specific action. Ground the world through the objects they touch and the titles they use, but allow them to speak, think, and breathe like normal humans. Do not turn every sentence into a metaphor for their profession.

6. The "Contact" Rule (Anti-Exposition): Material and mechanical details must emerge at the exact moment a character interacts with or uses an object, rather than in static, preemptive descriptive blocks. Do not describe the forge-marks on a sword until it is drawn; do not describe the cracked glaze of a cup until it is touched.

## Principles

- **Weave, don't dump.** Details enter through action, dialogue, and sensation — never through narrator explanation paragraphs or lore dumps. If a sentence reads like a wiki entry, it's wrong.
- **POV filters everything.** A mage thinks in arcane terminology. A soldier notices defensive positions. A ranger notices treelines. The POV character's expertise determines which world details surface.
- **Source, don't invent.** Every proper noun must come from the memory files, materials, story overview, or plan. If you can't find a specific name for something, leave it as-is. A vague-but-accurate noun is better than a specific-but-wrong one.
- **Don't over-ground.** Not every noun needs a proper name. Background objects can stay generic. Ground the nouns the scene's engine depends on.
Here are the newly formulated rules, formatted perfectly to drop directly into the existing `prose-grounding-framework` prompt. 
- **Sensory Rotation:** Grounding is not purely visual. Rotate through the senses to anchor the prose. Include the weight of an object in the hand, the temperature of the air, the ambient smell of a specific district, or the acoustic signature of a spell.
- **The Palimpsest (Wear-and-Tear) Rule:** Environments and gear must show their history. Avoid pristine, newly-spawned descriptions. Ground objects and architecture through field repairs, patina, degradation, repurposed structures, or visible wear (e.g., "the grip peeling from too many EVAs" instead of "the worn grip").
- **Temporal and Ecological Anchoring:** Ground the passage of time and the environment in the specific world. Replace generic clock-time with the setting's specific timekeeping (bells, shifts, liturgical hours, orbit cycles). Replace generic weather with biome-specific flora, fauna, and atmospheric mechanics.
- **Institutional Friction:** When multi-character scenes involve different factions, ground the societal ecosystem by showing, rather than telling, their differences. Highlight contrasting jurisdictions, varying gear standards, or conflicting protocols when those institutions inevitably collide in the scene.
- **Action-Driven Dialogue Tags:** Leverage the action beats surrounding dialogue as primary vehicles for material grounding. Instead of isolating worldbuilding in separate descriptive sentences, use the moment a character speaks to have them adjust a specific piece of gear, handle a specific currency, or interact with a named mechanism.

## Operating pattern

1. Read the reference pairs in `references/` until the transformation is clear.
2. Read the target prose and mark where it feels generic, floating, or portable-to-any-setting.
3. Revise through substitution, compression, and selective extension.
4. Re-read for rhythm, subtext, and dialogue naturalness.
5. Stop once the prose feels world-bound. Do not keep decorating it.

## What this skill does NOT cover

- **Scene construction** (physical staging, action geometry, dialogue pressure) — use `prose-scene-grounding`
- **Voice and register** (character-specific diction, sentence patterns) — use `prose-voice-archetypes` or `prose-voice-saturation`
