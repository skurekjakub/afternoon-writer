# Dialogue Grounding in AI-Generated Fiction

## Summary
AI-generated dialogue tends to "float" — characters speak in a void without interacting with their environment. This "floating heads syndrome" stems from the model's tendency to process dialogue as information exchange rather than embodied conversation between physically present people.

## The Floating Heads Problem

### What It Looks Like
- Long stretches of quoted speech with only "said" tags or no tags
- No physical interaction with setting during conversation
- Characters' bodies disappear while they talk
- Emotional reactions described abstractly ("she felt angry") instead of physically
- Dialogue reads like a screenplay or transcript rather than embodied prose

### Why AI Does This
1. **Training distribution**: Most training data has simpler dialogue attribution than literary fiction
2. **Context-free generation**: The model generates dialogue as a language pattern, not as speech emerging from a physical situation
3. **The grounding constraint paradox**: Anti-wiki and anti-spoonfeeding rules (correctly) prevent the grounder from inserting lore into dialogue — but this creates a "dialogue skip zone" where no grounding agent touches the conversational tissue

### The Anti-Wiki/Anti-Spoonfeeding Trap
The current afternoon pipeline grounder has rules that effectively exclude dialogue from grounding:
- **Anti-Wiki Rule**: "Don't inject lore terms or faction names into dialogue between characters who already share that context"
- **Anti-Spoonfeeding Rule**: "Never explicitly state what a scene's subtext implies"
- **Anti-Jargon Rule**: "Don't replace functional verbs with domain-specific jargon"

These rules are CORRECT for preventing AI over-grounding. But they create a gap: who grounds the *tissue around* dialogue? The grounder skips it. The slophunter cleans it. Nobody enriches it.

## Techniques for Grounding Dialogue

### 1. Action-Driven Dialogue Tags (from prose-scene-grounding's dialogue-pressure packet)
Replace generic tags with physical interaction beats:
- **Before**: "He said" / "she replied" / "he paused"
- **After**: "He folded the map and set it on the table" / "She checked the latch without looking at him" / "He turned the coin over twice before answering"

Key principle: the action beat does THREE jobs simultaneously:
1. Creates the pause/rhythm (replaces "he paused for a beat")
2. Grounds the character in their environment (they're touching real objects)
3. Reveals emotional state through physical behavior (without naming it)

### 2. Contact-Based Emotion (from dialogue-action-weaver agent)
Show emotional reactions through the body's somatic reality:
- **Before**: "He felt betrayed by her words"
- **After**: "His grip slipped on the leather rein" / "Her throat tightened around the next word"

The existing dialogue-action-weaver agent in the repo has this as Rule 3: "Anti-Spoonfeeding: Show the Flinch, Don't Name the Emotion"

### 3. Environment Persistence During Conversation
The setting should remain audible/visible/tactile throughout dialogue:
- Ambient sounds (bells, footsteps, rain, distant shouting)
- Temperature and weather changes
- Light shifts (candle guttering, sun moving, fire dying)
- Other people nearby (servants, guards, passersby)

### 4. Object Continuity (GRRM technique)
Give characters something to handle during conversation:
- A meal being eaten (pace of eating reveals mood)
- A weapon being cleaned or inspected
- A document being reviewed while discussing something else
- A drink being poured, held, not-drunk

Example from A Clash of Kings: Pycelle serves boiled eggs and stewed plums while serving pontifications. The food does setting work AND character work simultaneously.

### 5. Pace-Dependent Choreography (from dialogue-action-weaver)
- **Rapid-fire arguments**: Zero dialogue tags. Let quotes stack to accelerate.
- **Heavy revelations**: Anchor with heavy sensory action beats to force the reader to slow down.
- **Negotiations**: Each reply accompanied by a spatial move (who takes the chair, who stands, who approaches the door)

### 6. Institutional/Status Grounding (from dialogue-pressure packet)
Let institutions speak through objects and procedures:
- Titles, ranks, and forms of address carry world-building without narration
- Documents, badges, seals, uniforms do exposition work inside the conversation
- Who gets the chair, who is offered food, who must stand — these are world-specific

### 7. Cross-Sense Anchoring
Rotate through senses during conversation to prevent visual-only grounding:
- Touch: rough table edge, cold stone through boot-soles, paper texture
- Smell: smoke, preservative spirit, cooking from another room
- Sound: footsteps in another corridor, chair scraping, breath through helmet
- Temperature: lake-cold, forge-warm, evening chill entering through a gap

## Dialogue Grounding Checklist (for Gate Agent)

For each dialogue passage of 5+ exchanges, verify:
1. [ ] At least one physical action beat per 3 quoted lines
2. [ ] Setting remains present (sound, temperature, or visual anchor within last 5 lines)
3. [ ] No "floating heads" stretches longer than 4 consecutive quotes without environmental contact
4. [ ] Emotional reactions shown through body, not named in narration
5. [ ] Characters interact with at least one named object during the conversation
6. [ ] Dialogue tags vary: mix of "said", action beats, and untagged lines
7. [ ] Pace matches scene tension (fast = no tags; slow = heavy beats)

## Implications for Pipeline

### Current Gap
The grounder correctly avoids over-grounding dialogue (anti-wiki, anti-spoonfeeding). But nobody fills the gap — the *tissue around* dialogue (tags, beats, interiority, environmental persistence) gets no grounding attention.

### Solution
A dedicated **dialogue-action-weaver** pass that:
1. Runs AFTER the grounder (dialogue tissue now sits in a grounded environment)
2. Targets ONLY the non-spoken parts: tags, beats, interiority, pauses
3. Does NOT change the spoken words themselves (unless they violate world register)
4. Replaces generic gesture/emotion with world-specific physical interaction
5. Ensures setting persistence through ambient/sensory anchors between quoted lines

### Source: the `_afternoon-grounder-dialogue.agent.md` already implements rules 1-4 above but is not wired into the pipeline.
