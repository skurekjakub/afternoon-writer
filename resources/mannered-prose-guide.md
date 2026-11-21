# Mannered Prose Hunt Guide — LLM Adversarial Edition

## Your role and stance

Passes A and B hunt the named AI tells: negation pivots, agency laundering, narrator seep, phantom concreteness. This pass hunts what survives them. That's prose that *performs* craft: a sentence that sounds literary and, read slowly, says something slightly wrong, says it twice, or says it as a joke the character didn't make.

These survive because they are competent. They have no banned word. Their subjects are real agents, their images are concrete, and their dialogue cashes out. They still read as written by a model, because a human editor would circle them:

- "let the mare choose her own feet": a bent idiom, so the literal sense is off
- "the night in the village had been fire and a cage and Brask's men carrying sacks": a stretch of time summed up as a list of images
- "Yes. It's better there than in a yard. Everything in a yard gets walked over.": an answer, then a reason, then a maxim
- "He stood up when they came in and then didn't know what to do about having stood.": comic narration of a body's self-consciousness that does not survive a plain paraphrase

**Default stance: KILL for the zero-tolerance patterns, COUNT for the capped ones.** Every candidate is guilty until a test clears it.

The prose will be good. That is the camouflage. You are not asking "is this bad writing?" You are asking "would a sharp human editor put a pencil mark here?" One of these per page is a voice. One per paragraph is a machine.

---

## Core definition

**Mannered prose:** a sentence whose main job is to sound like fiction rather than to tell the reader something new, in plain sense, from inside the POV.

It shows up in four ways:

1. **Bent sense.** The words do not literally mean what the sentence wants (M1, M2).
2. **Compression into a figure.** Events become a list, a copula, a maxim or a quip instead of a clause with an actor and a verb (M3, M4, M5, M9, M11).
3. **Narrated self-consciousness.** The prose watches the character watch herself (M6, M7).
4. **Explaining or echoing.** The prose glosses, mirrors or repeats what the page already did (M8, M10, M12, M13).

---

## Decision procedure

Run four tests on every sentence in the chapter, in this order. Detection is sentence by sentence; do not skim.

### Test 1 — Plain paraphrase (catches M2, the most important)

Restate the sentence in flat, literal words, as a witness would in court.

- If the paraphrase is **false, impossible or nonsense**, KILL as M2.
- If it **contradicts the next sentence**, KILL as M2.
- If the paraphrase is **ordinary and true** but the sentence takes a strange route to get there, go on to Test 2.

| Sentence | Plain paraphrase | Verdict |
|---|---|---|
| He stood up when they came in and then didn't know what to do about having stood. | He stood up, then felt awkward. | M2/M6. "What to do about having stood" names no possible action. |
| Every time she thought about anything on that road, she was thinking about the stove. | She kept thinking about the stove. | M2. "Every time she thought about anything" is a paradox dressed as emphasis. |
| Every name so far had been a place. A boy in a loft... A young man with a cart... | (the list that follows is not places) | M2. The claim contradicts the next sentences. |
| It looked like a field the morning after the field had been fought over. | It looked like a battlefield. | M2. The second "field" makes the simile fold on itself. |
| Her eyes lagged behind the light tonight. | Her eyes were slow to adjust. | M2. Eyes cannot lag behind light. Say the plain thing. |
| Without any change in her face she took the vinegar and the slops and the pears. | She smelled them and did not react. | M2. "Took" the smells is not English for smelling. |

### Test 2 — Idiom distance (catches M1)

Ask: **is there a stock phrase this is one or two words away from?**

If yes, say the stock phrase aloud. Then:

- If the bent version **breaks the literal sense** (horses do not choose feet; questions do not go cold), KILL as M1.
- If the bent version is **funnier, sharper and literally true**, it may be a KEEP, but only once per chapter, and only in the POV's own voice.

### Test 3 — Job (catches M3, M5, M8, M10, M12)

Ask: **what new thing does this sentence give the reader?** A fact, an action, a line, a sensation, a choice.

- If the answer is "nothing new; it sums up, explains, caps, mirrors or repeats what is already on the page", KILL under the matching pattern.
- If it adds something, go on to Test 4.

### Test 4 — Count (catches the capped patterns)

Some moves are legitimate once and mechanical at volume: maxims, "the way" similes, self-monitoring beats, quips, rhetorical figures and argument templates. For each capped pattern:

1. Count **every** instance in the chapter, using the tool hits as the floor rather than the ceiling.
2. Rank the instances from strongest (most specific to this POV and this moment) to weakest (generic, decorative, or a repeat of a move made a page earlier).
3. KEEP the strongest up to the cap. KILL the rest, weakest first.

**The character-voice defense does not lift a cap.** A voice sheet licenses a move (Sylvanas's dry asides, Jaina's self-mockery). It does not license making that move eight times a chapter. Defend *which* instances survive with voice; do not use voice to defend the count.

---

## Pattern catalog

Every example below is from this book's own drafts.

### M1 — Bent idiom (zero tolerance) — MODERATE

A stock phrase with one word swapped so it sounds fresh. The swap breaks the literal meaning, or leaves the reader translating it back.

| Bad | Stock phrase it bends | Fix |
|---|---|---|
| Sylvanas kept to the crown of the road and let the mare choose her own feet. | pick her (own) footing / pick her way | Sylvanas kept to the crown of the road and let the mare pick her footing. |
| Jaina had been on her feet before the question was cold. | before the body was cold | Jaina had been on her feet before Sylvanas finished asking. |
| Jaina opened her mouth and had nothing to put in it. | had nothing to say | Jaina opened her mouth and had nothing to say. |
| She wanted to hand it off, badly enough to taste. | so badly she could taste it | She wanted badly to hand it off. |
| She had Windrunner down as maps. | had her down as | She had taken Windrunner for a woman who only knew maps. |

**KEEP:** an idiom used straight ("for any money in Silvermoon"), or a bent idiom that is a character's spoken joke and is literally true.

### M2 — Literal-sense failure (zero tolerance) — SEVERE

A sentence that does not survive Test 1. These are the "complete gibberish" lines: grammatical, rhythmic and meaningless. They come out of the model reaching for an effect and leaving the sense behind.

More shapes to hunt:

- **Self-folding repetition:** "a field the morning after the field had been fought over".
- **Participle stuffed into the wrong slot:** "a cross, meant, that looked like a bird's foot".
- **Dangling adjective tail:** "her fine legs trembling once and quiet".
- **Agency slips that are not intent smear:** "the belly still busy at something without her".
- **Quantifier paradox:** "every time she thought about anything".

**Fix:** write the plain paraphrase from Test 1, in the POV's words. If that loses nothing, use it. If the sentence existed only for its effect, delete it.

### M3 — Equative montage (zero tolerance) — MODERATE

A span of time, a place or an experience equated with a list of images, or with one noun, through "was" or "had been". It sums up instead of narrating.

| Bad | Fix |
|---|---|
| She had not slept since the night before the village, and the night in the village had been fire and a cage and Brask's men carrying sacks. | She had not slept since the night before the village, and in the village she had stood over the burning flour with Brask until dawn. *(or cut the second clause; the reader was there)* |
| After that the night was the river road. | After that they kept to the river road all night. |
| Every breath she spent in this room was a furlong. | Every question she asked in here gave the wagons more road. |

**Test:** can you put an actor and a verb back? If the summary covers events the reader saw on the page, cut it; recapping a list of images is decoration.

**KEEP:** a copula that states a plain physical fact ("The road was mud at the edges").

### M4 — Cadence list with a turn (zero tolerance) — MILD, or MODERATE in a grief or tension beat

A triplet or polysyndetic list whose **last item is the payoff**: the joke, the void, the sigh. The rhythm sets up the turn, and the reader feels the wind-up.

| Bad | Fix |
|---|---|
| She sat on somebody's old wagon bed..., irritated with him, with herself, with the candle for giving her too little light. | She sat on somebody's old wagon bed with the dust under her thumbnail, irritated with him and with herself. |
| She'd want jars. She'd want a great many jars, and a bench, and a lamp, and nobody knocking. | She'd want jars, and a bench, and a lamp. |
| ...at riders on the hill, at strangers, at horses, at nothing. | ...at riders on the hill and at strangers. |
| A man at the end of the road..., with a face, and a hall, and a door. | A man at the end of the road, with a face and a door she could knock on. |
| Damn the old man, and Dalaran, and every tower in it. | Damn the old man. |
| She could stand here and read jugs until dark, the salt box and the bucket and the ladle and the cat. | She could stand here and read jugs until dark. |

**Note:** polysyndeton itself is not banned. The rhythm anchor uses it ("danced, and drank, and yelled, and sang, and clapped"), and that list has no turn: every item is the same kind of thing. But The reference prose (Sanderson plus the Archmage sample) writes a 3+-"and" sentence about two to four times per 10K words; these drafts do it 12 to 29 times. When the tool's `polysyndeton.overSoftCap` is true, audit its `densestParagraphs` first and kill the lists that end on a turn.

### M5 — Maxim (cap 2 per chapter in narration; 1 per scene in dialogue) — MILD

A generic truth in the present tense ("a man in a hurry leaves the corners"), or a generic past ("A barn was never quiet."). The narrator, or a character, steps out of the scene to deliver a rule of life.

These are the most frequent tic in the book. Chapter 5 has ten in narration alone:

- "A free carter keeps carters' hours, and a slow hunt always runs a day behind."
- "A barn was never quiet."
- "Somebody had swept it, and not in a hurry, because a man in a hurry leaves the corners."
- "On clay a loaded wagon cuts deep."
- "A frightened man doesn't pick what to put in the stove. He puts in the shelf."
- "A man with an empty wagon and nothing to fill it with turns his horse and goes home."
- "Everybody stares at elves too long."

**Which survive (up to the cap):** the maxim is the **premise of a deduction the POV makes from evidence in front of her**, and the next sentence uses it. "A spy ran" followed by "this one had sat down in front of a drawn bow" is tracker logic. Keep the best two of that kind.

**Which die first:**
1. Maxims used as a **cap** after the evidence is already on the page ("Somebody had swept it... because a man in a hurry leaves the corners").
2. Maxims used as a **justification** inside dialogue: the overexplaining tail.
3. Maxims that set up **an image the reader already has** ("A barn was never quiet. There was always a rat, a pigeon...").

**Dialogue overexplanation.** When a line answers a question, it gets **at most one reason, and the reason must be particular, not generic**.

| Bad | Fix |
|---|---|
| "Can you read from the crossing?" / "Yes. It's better there than in a yard. Everything in a yard gets walked over." | "Can you read from the crossing?" / "Yes. Better than in a yard." |
| "Yes. It's better there than in a yard. Everything in a yard gets walked over." | "Yes. The yard's been walked over all day." *(particular, not a rule)* |

**Fix:** cut the maxim and keep the particular evidence. If the deduction needs the premise, make it particular: "Whoever swept this had time; the corners were done."

### M6 — Comic self-consciousness (zero tolerance) — MODERATE

The narration makes a joke out of a character's awareness of her own body, or of a body or animal lagging behind its own action. It is the model's signature comic register, and it lands in tense scenes as often as in light ones.

| Bad | Fix |
|---|---|
| He stood up when they came in and then didn't know what to do about having stood. | He stood up when they came in, and stayed standing, the pen still in his fingers. |
| He tried to salute and breathe at once and managed neither. | He tried to salute and could not get his breath. |
| His mouth went slack first, and then the rest of him caught up. | His mouth went slack. |
| Jaina's jaw ached. She unclenched it and, a little further down, had to again. | Jaina's jaw ached from clenching it. |
| ...and the cob stopped as if it had been hoping to... | ...and the cob stopped, blowing... |
| She got up off her knees, which took a while again. | She got up off her knees, slowly. |
| Her face had gone hot from the collar up, and she was furious with it. | Her face had gone hot from the collar up. |
| She was staying on it. She was trying to. | She stayed on it, just. |
| She caught the chair back and let go of it again before anyone could see her need it, which was pointless, with two rangers in a room the size of a wardrobe. | She caught the chair back, then let go of it. |

**Zero tolerance:** "didn't know what to do about/with [having X / her hands / himself]" and any "having + past participle" turned into the object of a feeling ("about having stood", "of having said it").

**KEEP (one per chapter):** comedy a character makes aloud, or a physical joke that carries plot information.

### M7 — Self-monitoring beats (zero tolerance) — MILD

The prose reports the character catching herself: hearing her own words, acting before she meant to, blushing at her own speech.

- **Self-hearing:** "Then Jaina heard what she'd just said." / "He heard himself, and his ears went red." / "She heard herself going faster and went on."
- **Involuntary action:** "before she meant to", "without meaning to", "before she could help it", "before she could stop herself", "before she knew she'd picked it up", "couldn't have said when she'd put it there", "of their own accord", "higher than she meant it to".
- **Blush beat:** "her ears going hot", "ears went red at the tips", "face had gone hot from the collar up". Count these toward the refrain family `blush_ears` as well.

**Fix:** cut the frame and keep the act. "She was drawing it in the air before she meant to" becomes "She drew it in the air, both hands up." If she later notices what she did, show the correction itself ("She put her hands down") without narrating the noticing.

### M8 — Interpreter gloss (zero tolerance) — MODERATE

The narration translates a line, gesture or pattern the reader has just seen. This sits next to F4 and claim-then-gloss, but these shapes are the ones that slip past them.

| Bad | Fix |
|---|---|
| Cyndia said, "Road's good," which was as much as to say the horses would do. | Cyndia said, "Road's good." |
| Cyndia was crossing the yard from the stables at a walk, which meant it would keep a moment. | Cyndia was crossing the yard from the stables at a walk. |
| She gave a short nod. It would have to do for thank you. | She gave a short nod. |
| He was frightened. Sylvanas could see that without a staff. It was in the colour of him and in the hands pressed flat... and in the way he had answered every question before she'd finished asking it. | Keep the evidence and drop the label: "He had no colour at all. His hands lay pressed flat to the wood, and he had answered every question before she finished asking it." |
| Three of them, and every one pointing down this road. | (delete; the three facts were just listed) |
| Sylvanas waited for the lecture. Currents and lines...: three sentences to get to one. | Sylvanas waited for the lecture: currents and lines, what the drag did in the pulse. |

### M9 — House wit (cap 2 per chapter in narration) — MILD

A dry narrator quip: a comparative put-down, a mock-precise understatement, a rhetorical shrug. Every POV and every side character gets the same wry register, so the quips stop sounding like anyone in particular.

- "Sylvanas would very much have liked one of the marks to be wrong."
- "If he had an opinion about grain at all, it would be somewhere below the orcs, and below his horse."
- "Sylvanas had been sized up by trolls with less care."
- "The cat looked better fed than her rangers."
- "There had never been hundreds of anything in Millhaven but hens."
- "...which was more than Lyriel ever did."
- "Jaina, then. It was shorter."
- "Who would steal a granary?"
- "She would not be eating bread for a while."

**Which survive (up to 2):** the quip is in the POV's voice-sheet humour register, *and* it carries information. For Sylvanas that means deadpan, pride in her people, often meaner than it sounds. For Jaina it means dry, aimed at herself. "Men lowered their spears for Antonidas because of the hat" tells us about Antonidas.

**Always KILL:** a quip in a grief, fear or violence beat; two quips in one paragraph; a quip that restates an image already on the page.

Spoken jokes belong to the speaker's voice sheet (Lyriel: "a plain observation followed by one flat, exaggerated comparison... one joke and then gets back to work"). Count a scene's spoken jokes; more than two from one speaker in a scene is a KILL on the weakest.

### M10 — Planted echo insert (zero tolerance) — MODERATE

A one-line paragraph about a small creature or object that mirrors the plot beat it follows. The model plants a symbol and lets it "find" its meaning.

| Bad | Why |
|---|---|
| The wasp found the gap at the top of the pane and was gone. | It lands right after the reveal that the carter has slipped through. A symbol on cue. |
| A moth found it, going round, and round, and in. / At the foot of the candle the moth was in the grease now, still moving. | A trapped thing, then a callback to it. |

**KEEP:** the creature does something the POV acts on (the cat's coat is clean, so it has been eating; the dog follows them, so the farm is alive), or the object is practical (the kettle ticks, so time passes). Ask whether the paragraph would be cut if it did not mean anything. If yes, KILL.

**Fix:** delete. If the scene needs a pause, use an action by a person in the room.

### M11 — Stylised figures (zero tolerance) — MILD

Classical rhetorical figures used for shine. The reference novels don't use them this way; in a draft they read as a writing exercise.

- **Zeugma:** "He made it sound a long way off, and to blame." / "It took the staff and the post and a while." / "the boots and the people were gone."
- **Anadiplosis:** "The King's road was clean, and clean was no use to her." / "every sickroom in the village boiled down to a spoonful, and the spoonful was here at her feet."
- **Chiasmus:** "where a hand could reach it at a gallop and a branch could not." / "go a shade greyer each time and come back a shade less." / "She could read every letter of it and not one word."
- **Tautology punchline:** "A doe was a doe." / "one deer was one deer." / "I stood in that road... and it was a road." / "They would ask what she meant by cold. She would say cold."

**Fix:** state it once, plainly. "He made Dalaran sound far off and to blame" becomes "'Dalaran,' he said, as if it were the far side of the sea."

### M12 — Argument templates (caps per shape) — MILD

Inner-voice shapes the voice sheets license, used so often they become a template:

| Shape | Example | Cap |
|---|---|---|
| Hypothesis ladder ending on the true answer | "Arrogance, then. ... Or she'd been frightened... Or she was right." / "Fled, then. ... Taken, then. ... Or they had got up and walked out." | 1 per chapter |
| "X, then." deduction fragment | "Bad luck, then." / "Wrong, then." / "Smaller, then." / "Millhaven, then." | 0 |
| Second-guess tag | "Under the glove her palm went cold, or she only thought it did." / "There was colour in her face again, or the candle was putting it there." | 0 |
| Sarcastic self-address | "Brilliant, Jaina." / "Grinning over a breach, Ranger-General." / "Lovely. Write that in the report." | 0 |
| Self-imperative fragment | "Open the doors." / "Don't. Find out." / "Leave it." / "Not yet. ... Start there." / "No. Slower." | 2 per chapter |
| Echo-compliance | "Make it heavy." / "Sylvanas made it heavy." — "Hold." / "Everyone held." — "Dickon went." | 0 |

**Fix:** where the cap is above 0, keep the strongest of each shape. Convert the rest into action (the voice sheet itself says "she ends the argument with an action, not a conclusion"), or cut them.

### M13 — "The way" simile (zero tolerance) — MILD

", the way a man lays down a tool he means to pick up again", ", the way cattle go over a gateway in a wet spring", ", the way paper goes when a man crams in too much at once and shuts the door on it and doesn't stay to see it through". Sanderson uses this construction about once per 50K words, and the Archmage chapters about once per 55K. These drafts use up to eight a chapter. "The way everyone did" / "the way they all did" is also a refrain (see the refrain guide).

**Fix:** cut the simile, or replace it with a plain "like" and one noun from the POV's own trade or past (Jaina's ships, Sylvanas's hunting and her rangers).

---

## Caps summary

The caps come from human prose. `tools/mannered_checker/check.py` measures each detector on the human reference corpora (`priming.humanCorpora`: Way of Kings plus 23 Archmage chapters, about 437K words) and reports this chapter's caps as each pattern's `cap` and in `codeCaps`. **Use the checker's caps.** A pattern the reference prose uses under 0.5 times per 10K words gets 0. The rest get twice the human rate at this chapter's length. The human prose almost never trips these detectors: a chapter-sized slice of it has 0-3 hits, where pipeline chapters have 12-36. So almost every cap is 0, and the only detector that measures above zero is the maxim (2 per chapter).

The table matches the checker at a typical chapter length. Rows marked *guide* have no detector: the gate judges them and these caps apply as written.

| Code | Pattern | Cap per chapter | Severity of each KILL |
|---|---|---|---|
| M1 | Bent idiom | 0 | MODERATE |
| M2 | Literal-sense failure | 0 | SEVERE |
| M3 | Equative montage | 0 | MODERATE |
| M4 | Cadence list with a turn | 0 | MILD (MODERATE in a grief or tension beat) |
| M5 | Maxim | 2 in narration, 1 per scene in dialogue | MILD |
| M6 | Comic self-consciousness | 0 | MODERATE |
| M7 | Self-monitoring beats | 0 | MILD |
| M8 | Interpreter gloss | 0 | MODERATE |
| M9 | House wit | 2 in narration (*guide*) | MILD |
| M10 | Planted echo insert | 0 | MODERATE |
| M11 | Stylised figures | 0 | MILD |
| M12 | Argument templates | 0, except hypothesis ladder 1 and self-imperative fragment 2 (*guide*) | MILD |
| M13 | "The way" simile | 0 | MILD |

---

## Cluster rules

- **3+ KILLs from this guide in one paragraph** raise every KILL in that paragraph to MODERATE. The paragraph is performing.
- **The same move twice within five paragraphs** (two maxims, two quips, two "the way" similes) means KILL the second even when the chapter is under the cap.
- **A capped pattern at 3× its cap or more** makes the weakest excess instance MODERATE. The habit is structural.
- **Any M2 in a scene** sends you back to re-read that scene word by word. Sense failures come in pairs.

---

## Tool signals

`tools/mannered_checker/check.py` reports pattern hits by code. Every hit is a candidate you must rule on.

| Tool pattern | Code |
|---|---|
| `bent_idiom_seed` | M1 |
| `equative_montage`, `equative_single` | M3 |
| `list_turn_seed`, plus `polysyndeton.densestParagraphs` | M4 |
| `maxim` | M5 |
| `did_not_know_what_to_do`, `having_nominal`, `comic_recursion_seed` | M6 |
| `self_hearing`, `involuntary_action`, `blush` | M7 |
| `gloss_which`, `would_have_to_do_for` | M8 |
| `planted_insert` | M10 |
| `tautology`, `anadiplosis` | M11 |
| `then_fragment`, `second_guess_tag`, `self_address`, `echo_compliance` | M12 |
| `the_way_simile` | M13 |

The tool's seeds catch shapes already seen in this book. Your reading has to catch the new ones. **M1, M2 and M9 have almost no tool coverage.** They depend on you reading every sentence.

---

## Fix rules

- **Prefer deletion.** Most of these sentences are additions to a scene that already works.
- **Plain beats clever.** The fix is the sentence a tired, good human writer would have written first.
- **Do not trade one tic for another.** Do not replace a maxim with a "the way" simile, a quip with a blush, or a gloss with a negation pivot. Before you write a fix, run it through all four tests and through the pass A and pass B pattern names you know: negation pivots, permission tags, body-part agency, narrator verdicts.
- **Keep the fact.** If the mannered sentence carries the only statement of a plot fact (the mage said *old* before seeing the book), the fix must keep that fact in plain words.
- **Stay in the POV's register.** The fix still sounds like Sylvanas or Jaina, just plainer.

---

## Output format

Each KILL finding in the notes JSON:

```json
{
  "id": "C-M5-3",
  "line": 305,
  "text": "Somebody had swept it, and not in a hurry, because a man in a hurry leaves the corners.",
  "pattern": "M5 - maxim",
  "test": "Test 4 (count): 10 maxims in narration, cap 2; this one caps evidence already on the page",
  "verdict": "KILL",
  "severity": "MILD",
  "reason": "The swept corners are already described in the previous paragraph; the maxim restates them as a rule.",
  "suggestedFix": "Somebody had swept it, corners and all, and had not hurried.",
  "fixDifficulty": "low",
  "crossChecked": ["mannered-prose-guide.md", "refrain-guide.md"],
  "toolSignal": "maxim"
}
```

The guide summary in the notes JSON adds `capCounts`, listing each capped pattern's count, its cap and the line numbers of the KEEPs, so the next iteration can see which instances were chosen to survive.

---

## Adversarial self-check

1. Did you run Test 1 on **every** sentence, including dialogue and the ones you liked?
2. For each capped pattern, did you count past the tool's hits? The tool is a floor.
3. Did you KEEP anything only because "it's her voice"? Voice picks *which* instances survive, not *how many*.
4. Did any suggested fix introduce another pattern from this guide, or a pass A/B pattern?
5. Did you check the densest polysyndeton paragraphs for lists with a turn?
6. Did you read the dialogue for answer + reason + maxim stacks?
7. Is there a one-line paragraph about an animal or object right after a plot reveal? (M10)
8. Would a sharp human editor mark anything you KEPT? If you hesitate, KILL it.

---

## Calibration: KEEP examples from this book

- "on straw that smelled of other people's horses": concrete, particular and in-POV.
- "Somebody had drawn a horse in charcoal on the plaster above it, and somebody after him had given it a fifth leg.": an observed detail with a human trace; whimsical, but true.
- "Grain don't come this way now. I'd know. Grain pays.": the toll-keeper's only maxim, in his own grammar, and it is evidence.
- "Sheep, all over everything.": a tracker's fragment with a real referent.
- "'He put a loop on the seven,' she said, when she could. 'On the seven.'": spoken comedy that belongs to the moment.
- "A spy ran. Any spy worth his pay would have been halfway to Lordaeron...": a maxim as the premise of a live deduction (one of the two allowed).
