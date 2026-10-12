# Input register audit and tell bleed: The Plague Road, chapter 1

Scope: the prose register of the pipeline's inputs, and which tells in chapter 1 (`v0.md` is the writer's draft, `v2.md` is the slophunter's output) have a precursor in those inputs. Every file listed was read only. Continuity and plot are out of scope.

Run directory: `/tmp/claude-1000/-home-jakubs-repositories-tuesdays-universe/a12a7cb7-0c3c-4f5a-ae88-c224785a8bd7/scratchpad/afternoon-ch1/.afternoon/`

## 0. Read paths: what each stage actually sees

Precursor links only count if the agent that produced the tell could have read the precursor. I checked the agent prompts and `config.json` in the run directory:

| Stage | Reads (per its prompt and config) | Does not read |
|---|---|---|
| **Writer** (`afternoon-writer.md`, makes v0) | `scene-N-plan.json`; the voice sheets for `castInScene` (Sylvanas in all three scenes, Jaina in scene 3 only; Lor'themar, Cyndia and the runner have no sheet); the end of the previous v0; `style-samples/writer-rhythm-anchor.md` ("YOU MUST WRITE LIKE THIS"); its own agent prompt | The outlines, the character `.md` files, `story-arc.md`, `overview.md`, `chapter1.json`, slop-hitlist, ai-quirks. Its prompt says "Do not read any other files". |
| **Planner** (makes `chapter1.json`) | The outline, `story-arc.md`, the character files and locations (config `materials`) | n/a |
| **Scene plans** | Copies of `chapter1.json` with `verifierModification`, `enrichment`, `arcPressure` and `continuityStatus` removed. `plannerWarning`, `constraints`, `arcPosition`, `newOnPageInformation` and `stillUnknownAfterBeat` are kept. | The verifier's craft research (for example "Characters should talk around facts, interrupt, and withhold") is removed, so the writer never sees it. |
| **Between v0 and v2** (`v0c.md`, `v1.md`, made by the craft reviser and continuity agents) | The craft reviser also reads `style-samples/texture-transformations.md` and `.afternoon/style-guide.json` | n/a |
| **Slophunter** (makes v2) | `slop-hitlist.md` (config `priming.antiSlop`), the rhythm anchor, all three voice sheets, `story-arc.md`, `editor-guide.md`, `external-resources/author-technique-anchors.md`, the gpt-5, intent-smear and narrator-seep guides, `style-guide.json` | n/a |

So outline and character-file tells reach the writer only when the planner copies them into a scene plan. Most of them do get copied. Kel'Thuzad's voice sheet is not on chapter 1's read path. Its tells are listed for chapters 10 to 12.

Three files outside the brief turned out to sit on the read path and to carry tells: the **writer agent prompt**, **`style-guide.json`** and **`texture-transformations.md`**. Their tells are listed in §a.8.

---

## (a) Tells per input file

Catalogue codes: **HL** = `slop-hitlist.md` section; **F1 to F7** = gpt-5-prose-issues; **NA-Pn** = negation-addiction pattern n; **IS-Pn** = intent-smear pattern n; **NS-xx** = narrator-seep; **PC-Pn** = phantom-concreteness; **Tic n** = recurring-prose-tics; **AQ-nn** = ai-quirks file. **NEW** = not in any catalogue.

### a.1 Voice sheets (highest priority)

#### `voice-sheets/sylvanas-voice.md` (on the writer's path in all three scenes)

The sheet's own instruction prose is written in the negation-pivot register it is meant to keep out of the dialogue. It also prescribes three physical tells that the catalogues ban.

| # | Quote | Catalogue |
|---|---|---|
| S1 | "Fingers touch the bowstring when she is assessing risk." | Prescribes a body-part beat. The output turns it into "Sylvanas's fingers found the bowstring…": HL Contact Verbs with Agency; IS-P8 |
| S2 | "A longer exhale often stands in for visible emotion." | Prescribes HL Breath as Universal Tell; F2 kill list "exhaled" |
| S3 | "She angles herself toward useful ground without thinking about it." | Body acts before mind: the source of the "before she had decided" construction (IS-P8 exception wording) |
| S4 | "Stillness means concentration, not calm." | NA-P1 |
| S5 | "Brevity is a weapon, not a metronome." | NA-P1 plus metaphor |
| S6 | "She speaks in finished judgments, not exploratory thought." | NA-P1. It also licenses the aphorism habit (see b.22) |
| S7 | "some of that comes through smoothness, not just shortness." / "Under stress, she gets quieter, not louder." / "longer lines should feel like a blade drawn out slowly, not like hesitation" | NA-P1/P4 (×3); HL Simile |
| S8 | "Proof first. Theory after." (sample line) | NS-A2 thesis-fragment pair. It is the same shape as the NS-A2 calibration example "War first. The visible wound first." and the PC-P1 example "Truth first. Mercy later.", both always-kill |
| S9 | "You sent a budget answer to a plague question. I noticed." | NS-A1 verdict tag on a quip |
| S10 | "You may call it a border matter if that helps you sleep. The dead will not." | Epigram (PC-P1 slogan rhythm). NEW: conditional epigram |
| S11 | "If you intended to run, you chose the wrong road." / "If the route keeps bending southwest, someone is steering it." / "If they move the patrol line again, we stop asking why and start asking who benefits." | NEW: "If X, [aphorism]" conditional epigram. Three of the sheet's samples use it |
| S12 | "You are mistaking distance for safety." | NEW (same-mouth across sheets): the same frame as Kel'Thuzad's "You mistake comprehension for surrender." Fails the F2 same-mouth test |
| S13 | "Take the breach. I'll take what follows it." and "Hold the breach for two breaths and I'll clear what follows it." | NEW (same-mouth): the same frame as Jaina's "You take the door. I'll take whatever comes through it first." |
| S14 | "Her eyes clear exits, cover, and bodies before the scene's social meaning." | IS-P8 body part as actor |
| S15 | "so used to command that half her sentences assume the order has already been understood" | Cues the repeated "without being told" in the output (b.34) |
| S16 | POV filter list "exits, cover, approach lines, silence, gait, fatigue, and readiness" | Cues the inventory paragraph (F6 inventory) |
| S17 | "If the line sounds like it could pin someone to the wall in six words, or cut them cleanly in fourteen" | Quip register used as the voice test itself |
| S18 | Default word field includes "useful", "dead" | Lexical. "useful" shows up as "whatever's useful" and "could be used" |
| S19 | The audience table has a row for how she speaks *to* Farstriders ("Command shorthand… 'Left ridge. Two ahead.'") and no row for how they speak *to her* | NEW (gap): no subordinate register exists, so the subordinates copy hers. See §b.3 |

#### `voice-sheets/jaina-voice.md` (on the writer's path in scene 3 only; Jaina does not speak in chapter 1)

| # | Quote | Catalogue |
|---|---|---|
| J1 | "No. That isn't proof. That's residue pretending to be proof." | **NA-P5b negated anthropomorphic redefinition**, the "That isn't sleep. That's cavalry lying to itself." pattern that has "zero legitimate uses". It is offered as a *good sample shape* |
| J2 | "The wards are taking damage from the south. Not weather. Deliberate damage." | NA-P2 fragment pivot (the sheet labels it "slightly over-translated" on purpose, but it is still a model line) |
| J3 | Syntax rule: "She self-corrects in motion: 'No--that's not the problem. The problem is...'" | NA-P1 taught as a syntax rule |
| J4 | "I'm not guessing. I'm ruling out the comfortable explanations one by one." / "I am explaining the situation. I am not asking whether it exists." | NA-P5 preamble negation; paired parallel declaratives (the shape of "Theris says what she says. This is me.") |
| J5 | "If the ward lattice is carrying the corruption intact, then someone taught it how to survive transit." | IS-P5 (the corruption is taught and survives); "transit" is document register (HL Dialogue Register) |
| J6 | "The lines are wrong. Something dead keeps answering through them." / "Something deeper is waiting for the body to finish the work." | HL "Something" as vague intensifier; PC-P3 "the work"; IS-P5 |
| J7 | "it should hit like a snapped wire" | HL Simile |
| J8 | "When frightened, she gets more exact, not more vague." / "they should feel **built**, not rambled" | NA-P1 |
| J9 | "I am being polite. That should not be mistaken for uncertainty." | Epigram/quip; "mistaken for" is the same frame as S12 |
| J10 | Default word field: "pressure", "pattern", "answer", "wrongness", "residue" | PC-P3 placeholder nouns (the guide lists `pressure` and `answer` by name) |
| J11 | "Humor is dry, brief, and usually arrives when the situation is bad enough to deserve none." | Abstraction given arrival (IS-P9-adjacent) |
| J12 | Voice test: "precise, humane, and slightly too fast for the room" | Triplet. "the room" as stand-in |

#### `voice-sheets/kelthuzad-voice.md` (not on chapter 1's read path; matters for chapters 10 to 12)

| # | Quote | Catalogue |
|---|---|---|
| K1 | "He does not sound like a cackling villain. He sounds like the most brilliant lecturer in the room, and that is what makes him monstrous." | NA-P5 plus F7 closer |
| K2 | "Calm, exact, almost collegial." / "speaks as if the method is already proven" / "he knows it almost immediately" | F3 hedge ("almost" ×2, "as if") |
| K3 | "No shouting. No pleading. No hurry." | NEW: "No X. No Y. No Z." stack (the chapter 1 output has the same shape from another source, b.16) |
| K4 | "He does not snap. He refines." / "He does not simplify for her. He escalates." / "not to search for the truth, but to demonstrate it" / "Magical-academic, not scientific-modern." / "chalkboard magic, not physics class" / "Measured rather than rushed." | NA-P1/P5 (×6) |
| K5 | "Not operatic. Not frothing. Not gleefully chaotic. Not metaphor-drunk." | NA-P7 chained negation |
| K6 | "The plague is not a poison. Poison enters, spends itself, and is done. This listens, settles, and waits for the body to provide the final answer." | NA-P1; two triplets; IS-P5 (the plague listens and waits); "settles" (HL contact verb) |
| K7 | "A village fed together dies together. A village that dies together does not rise as a collection of accidents. It rises as a choir. Even unguided, a choir seeks its own note." | Anadiplosis chain; NA-P1; IS-P5 |
| K8 | "You are objecting to consequence before you have disproven method. That is understandable. It is not persuasive." | NS-A1 verdict fragments |
| K9 | "He simply lost his nerve when the conclusions offended the room." | F3 "simply"; IS-P4/P7 (the room is offended) |
| K10 | "teaches the body the shape of its own ending" / "the pattern acquires a... second instrument" | PC-P3 "shape"; HL "shape (of)" |
| K11 | "He assigns mental labor the way other men assign chores." / "should feel like a seminar from hell" / "should read like intellectual recognition weaponized" | Simile ×3 |
| K12 | "Those completions should feel terrible, clean, and inevitable." / "patient, lucid, and ruinously reasonable" | Triplets |

### a.2 Character files (on the planner's path; reach the writer only through plan text)

| File | Tells (exact quotes) and catalogue |
|---|---|
| `sylvanas.md` | "Duty is not one part of her identity. It is the frame holding the rest together." (NA-P2, PC-P3) · "Farstrider armor worn like second skin" (cliché simile) · "another fact the room can react to" (IS-P10 room) · "Moves like someone who has spent centuries choosing where to stand before anyone else knows a choice exists" (simile; the "before she decides" construction) · "rooms, people, roads, silences, all read for use or threat" · "the threat that ignores the wall ignores the politics that built the wall" (chiasmus; IS-P5) · "the partnership is not convenience but structure" (NA-P1) · "Keep her self-aware, not self-explanatory." · "She does not monologue about her feelings. She shows them in choices, timing, and what she refuses to leave alone." (NA-P5 plus triplet) |
| `lorthemar.md` | "the Silvermoon political war made human" · "wit used like a knife" (simile) · "built to land one sentence at a time" · "When the humor dies, he is nearly spent." · "He counts votes the way a ranger counts angles." (simile) · "Two good advocates, two failing systems, same wall." (NS-A2 slogan stack) |
| `cyndia.md` | "grief turned into formation discipline" · "her body keeps checking the missing partner's slot" / "the body has already decided Jaina counts" (IS-P8 body deciding) · "volunteers good field observations" (this is her only dialogue cue, and it reads as report register) · "Keep the grief physical, not confessional." (NA-P1) · "She mourns by continuing the work until the work itself becomes the shape of the mourning." (PC-P3 "the work", "shape"; chiasmus) |
| `jaina.md` | "brilliant enough to see the truth early, young enough to believe seeing it should be enough" (balanced antithesis) · "Truth: brilliance without trust is just Kel'Thuzad with better intentions." (quip) · "The institutions fail her. The partnership does not." (NS-A2) · "should feel expensive, not effortless" (NA-P1) · "when she trusts the room" |
| `antonidas.md` | "silences that say more than the words" (IS-P7) · "worn as office, not costume" · "the institution proves it still has value" (IS-P4) · "Kel'Thuzad's name strips the softness out of him" (IS-P9) · "His tragedy is not disbelief. It is belief without speed." (NA-P2 plus PC-P1 slogan) · "That is what makes the failure hurt." (F7) |
| `arthas.md` | "a hero-shaped man destroyed by certainty" · "the blade speaks for him" (IS) · "He does not fall because he is stupid. He falls because true facts hit a mind that cannot bear not to act." (NA-P3 source swap) · "Stratholme proves the math can be sound and the act still monstrous" (IS-P10 place proves) |
| `jandice.md` | "What she wants from Jaina is not approval but recognition." (NA-P1; nearly identical to the PC-P1 KILL calibration "The answer is not permission. It is recognition.") · "Her blind spot is not stupidity. It is selective attention: method in one room, consequence in another." (NA-P2) · "Alexei Barov made a bargain. Jandice made a choice." (antithesis) · "The tour is a chess game." |
| `kelthuzad.md` | "Lecturer's cadence, not villain theater." · "Antonidas speaks to. / Kel'Thuzad speaks at. / Jandice speaks for." (NS-A2 slogan triplet) · "a greater library, not as a master" · "dies calm, as if finishing a theorem" |
| `malganis.md` | "He is not the plague's inventor or the Cult's builder. He is the thing making sure no one reaches either in time." (NA-P1) · "good investigation keeps arriving one step late" (IS-P9) · "Patient, amused, professionally contemptuous." (triplet) |
| `muradin.md` | "profanity used like punctuation" (simile) · "Gruff warmth instead of softness." · "Came north for discovery, not power" · "His usefulness comes from clarity, not from speeches." (NA-P1 ×3) |
| `supporting.md` | "**devastating** because he **simply** reports what the room looked like" (HL Melodramatic Intensifiers: banned outright; F3 "simply") · "Smart enough to build the wrong case beautifully. Does not lie. He arranges true facts into a cleaner false story." (NA-P5) · "Proves the institution can still produce useful people" (IS-P4) |
| `uther.md` | "sees the **trajectory**" (HL Academic-Discipline ban) · "'Boy' is not insult; it is paternal anguish stripped raw." (NA-P1) · "He does not lose faith. He runs headfirst into its limits." (NA-P5) · "hope kept him in the teacher's role too long" (IS-P9) · "faith proven in practice rather than theology" |
| `vereesa.md` | "blood can do what bureaucracy cannot: make the order hurt" · "Their argument is not really about the recall. It is about…" (NA-P2) · "Sylvanas keeps answering as commander. Vereesa keeps speaking as sister. That mismatch is the wound." (NS-A2 plus F7 closer) |

### a.3 `plans/story-arc.md` and `.afternoon/overview.md`

- story-arc: "Every solved problem reveals a bigger, faster, less containable one." (triplet; IS-P5) · "the border is political fiction once the threat ignores it" (IS) · "intelligence without trust turns monstrous fast" · "The partnership is what keeps her from their shape." (PC-P3 "shape") · "good men losing to systems built to delay" · "That fact makes Silvermoon complacent, not safe." (NA-P1, arguably a hard-constraint keep) · "This file is the signpost."
- overview: "witness Arthas Menethil's descent into madness" (stock phrase) · "There are no witnesses to Arthas's crime. Only two foreign women standing over two royal corpses with weapons drawn." (NS-A1 fragment closer). Otherwise mostly pointer lines; light.

### a.4 Style target: `style-samples/writer-rhythm-anchor.md` (writer's path, read last, "YOU MUST WRITE LIKE THIS")

Yes, the target carries tells. These are real Sanderson excerpts, and the catalogues would flag them on sight:

| Quote | Catalogue |
|---|---|
| "like a quartet of thumping hearts" · "like the hottest part of a smith's fire" · "dancing like a fluttering insect" · "as if they were dead" · "as if expecting Kaladin to be angry" | HL Simile Overload: 3 `like` and 2 `as if` in about 1,350 words. The HL cap is 3 of each *per chapter* |
| "danced, and drank, and yelled, and sang, and clapped" (the section header names it "polysyndeton") | HL "triple and chaining" |
| "Shin were easy to ignore. Most out here in the East thought Szeth's kind were docile and harmless. They were generally right." / "Windspren often played pranks like that." / "Windspren were devious spirits who had a penchant for staying where they weren't wanted." | NS-A7 generalizing about a kind; NS-A1 verdict tag ("They were generally right.") |
| "as Kaladin tried to toss his wooden bowl aside, he found that it stuck to his fingers" | HL Contact Verbs: **discovery-wrapper `found`** (banned) |
| "Shallan noted" ×2 · "he replied" · "Amaram demanded" · "asked softly" · "said softly" | Tic 7 said-avoidance; AQ-06 adverb-on-tag |
| "Shallan nodded, rising." · "He smiled." · "She smiled." · "shrugging" · "He hesitated" · "He cocked his head." | F2 generic-beat kill list |
| "for a moment it seemed red to him" | F3 hedge plus temporal padding in one sentence = KILL SEVERE |
| "the hills seemed endless" | F3 hedge |
| "Everything felt wrong." | NS-A5 scene-state declaration |
| "Oddly, Kaladin wasn't surprised. Just exhausted." | NA-P2 fragment pivot |
| "Szeth did not sway to the drums, drink the sapphire wine, or stand to dance." | NA-P7 triple negation |
| "walked away, emotionally exhausted, tears on his cheeks" / "looking ashamed" | Emotion labels (AQ-13, F4) |
| "Stained with Dallet's blood. Toorim's blood. The blood of the men who had been alive just moments before." / "Shash, the last glyph read. Dangerous." | NS-A1/A2 fragment verdicts; anaphoric fragment triplet |
| "the Blade's pitiless metal" | Personification |
| Dialogue: "'Take it, Kaladin,' Coreb said. … 'Take it,' Coreb said again." · "'Jam.' … 'You asked what I was fond of. Jam.'" · "'Is he dead?' … 'He is,'" | NEW: echo exchange (a line repeated back by the next speaker or on the next beat) |
| The section header itself teaches "gut-punch short sentences after long ones" | Explicit instruction to produce one-line punch paragraphs (b.44) |

The style target directly contradicts the antiSlop list the slophunter enforces: polysyndeton against "triple and chaining", the simile density against the cap, and "found that" against the contact-verb ban. The writer is told to copy the target, and the slophunter is told to delete what the target taught.

### a.5 "Good" examples inside `references/slop-hitlist.md` (slophunter's path)

Several fixes carry the tell their own section bans, or a tell banned elsewhere in the same file:

| Line | "Good" example | Tell it carries |
|---|---|---|
| L152 | "her hips moved before she told them to" | Body-part agency (HL Actor Demotion, IS-P8). The output has the same "before she had decided to" construction (b.23) |
| L117 | "Almost a smile." · "The corner of her mouth moved, and stopped." | F3 "almost"; Tic 1 corner-of-mouth. `recurring-prose-tics.md` lists "One corner of her mouth moved. Almost a smile." as a *bad* example |
| L270 | "A stillness spreading from the jaw?" | HL Abstract-Noun Locomotion, the very section it sits in |
| L151 | "a sharpness that bloomed outward" | Abstract-noun locomotion; AQ-05 false-poetic "bloomed" |
| L158 | "The certainty she'd carried for twenty years buckled." | Abstract-noun agency (IS-P9) |
| L193 | "The air between them went taut." · "Her voice dropped half a register." | NS-A5 scene-state; "register" is banned in L76 |
| L73 | "let the pieces collect" | HL Permission Tags (`let [it/them] …`) |
| L74 | "her gaze swept the room" | IS-P8 gaze as actor; Tic 5 |
| L78 | "she saw it," | HL POV Distance filter word "she saw" (banned in L144) |
| L22 / L84 | "the real words, not the careful ones" | NA-P1 |
| L63 | "what the body does without asking permission" / "The pull, the weight, the pressure" | Body agency; PC-P3 "pressure"; Tic 6 weight |
| L68 / L70 | "Who moved first. Who didn't move at all." · "Who stepped back. Who stepped in." | NS-A2 slogan-fragment stacks |
| L18 | "too little to kill quickly, too much to leave clean" | Balanced antithesis (PC-P1 slogan rhythm) |
| L226 | "She couldn't hear anything but her own pulse" | AQ-02 heartbeat cliché. The output has "She could hear her own heartbeat" |
| L262 | "The silence had an edge." | Inanimate-subject atmosphere |
| L109 | "Only cavalry would call it that." | Still makes a category the speaker (IS-P4-adjacent) |

**More serious:** the *bad* examples in HL Permission Tags (L203) and HL Contact Verbs (L216 to L218) are sentences from this same chapter, harvested from earlier runs: "A bead of sweat crept toward her eye, and she let it." · "Sylvanas's fingers found the bowstring before she had decided to reach for it." · "He tried to salute and found his hand still wrapped in the reins." · "…until the old ache settled back into the joint." All four are verbatim in v2 (see b.53). The slophunter's priming file contains the chapter it is about to edit, with its tells in place.

Other catalogues' good examples: `recurring-prose-tics.md` Tic 2 offers "logged, read, clocked, **filed**" as alternatives (HL bans "filed") and Tic 4 offers "Amusement flickered and died." (abstract-noun locomotion). Phantom-concreteness KEEPs "Method. Cost. Result." (slogan triplet). Narrator-seep KEEPs "Hope carried a bruise under it."

### a.6 Outlines

#### `chapter1.md` (copied almost verbatim into `chapter1.json` and the scene plans)

| Quote | Catalogue |
|---|---|
| "Lor'themar sees right through it—the politics are already dragging at her." / "before duty catches up" | IS-P5/P9 |
| "He is the only one who can **absorb** her irritation" / "there's no one to **absorb** Sylvanas's temper" | HL Academic-Discipline ban "absorbed"; IS-P9 (temper as an object) |
| "They don't know the day is about to crack open." / "The next conversation changes everything they thought they knew about the border." | NS-B3 thematic awareness; F7 cliché |
| "with the kind of report that ruins the whole patrol" | NS-A7 "the kind of" |
| "cutting the easy rhythm in half" / "The shift from deep woods to border stone changes the entire ride." | IS-P5 |
| "doesn't fit a standard spy box" / "Sylvanas turns the problem over" | Leads straight into the v0 "She turned the word over and couldn't make it fit" |
| "drowning in a problem of her own making" | Stock phrase |
| "**arrogant, terrified, or completely correct**" / "spy, diplomat, or both" / "hostile, reckless, or drowning" / "exhausted, furious, and very far from court" / "stones, roads, or riders" | Triplet habit (five in one outline) |
| "completely shatters her read of a pampered, court-trained nuisance" / "completely impossible" / "completely correct" / "definitely don't" | Intensifiers |
| "This isn't just a border trespass anymore. It's a high-stakes diplomatic and magical incident." | NA-P2 |
| "The ward-stones read **as if** they were malfunctioning because of something inside them." | F3 "as if" |
| "her staff propped uselessly" / "the raw exhausted anger she's projecting" / "rangers standing in exhausting, stiff alert posture" | Emotion labels; stacked adjectives |
| "a suffocating silence right before someone breaks it" | IS-P7 silence; stock |
| "One woman is in custody, and the other decides how hard the door stays shut." | Epigram |
| "Without Lor'themar, there's no one to absorb Sylvanas's temper as she rides hard south." | Abstraction as object |

#### `chapter7.md`, `chapter13.md`, `chapter19.md`, `chapter25.md` (full read)

- **Negation pivots, dense:** ch7 "They are not softened. They are simply harder to pull apart" (NA-P5 plus "simply"), "The masked crew are not protecting themselves from dust. They are protecting themselves from the grain." (NA-P2), "purely by skill, not rank"; ch13 "engaged rather than captive", "containment instead of obstruction", "spacing and silence instead of argument", "part of the defense rather than scenery"; ch19 "It is not where the next real answer lives.", "notification, not negotiation", "something chosen, not just something that works", "no longer a theory lane but the next operational target"; ch25 "The problem is delivery, not theory.", "The point is not a lore dump. The point is that…", "the partnership, not solitary intelligence".
- **Rooms and abstractions as actors (IS-P5/P10):** ch13 "what rooms reveal under pressure", "before the room found a way to shape the answer", "refuses to give the room another second to keep talking", "the room comes with them", "Sylvanas judges the room she sees, not the argument she missed"; ch25 "The room stops belonging to known threats."; ch7 "the city closes around the problem", "the grain district is already watching itself harder than it should"; ch19 "Home arrives to contest the road.", "The institution turns into a personal weapon."
- **Beat-closing captions (NS-A2, F7):** ch25 "The blade becomes the real night." "The book's truth is named." "The board is redefined." "Impossible recognition becomes possible."; ch19 "North becomes chosen fact." "The investigation fully becomes pursuit."; ch7 "The conspiracy is visible at last."; ch13 "The target is down, and the real damage begins after success."
- **Banned document vocabulary (HL Dialogue Register / Academic-Discipline):** "vector" (ch18 L74, ch19 L95), "ingestion" (ch4 L121, ch7 L25, L139), "operational" (ch17, ch18, ch19 ×2, ch25), "trajectory" (ch18 L115), "geometry" (ch9, ch13 L148), "shape of" (ch8, ch12, ch15, ch18).
- **Anaphora and parallel pairs:** ch7 "Too many clerks, too many rules, too many mages, too much grain"; "Havel knows the street truth… Corin knows the paper truth"; ch25 "easy through stone, easy through fear, easy through scale".
- **Hedges and similes:** ch7 "workers who move like soldiers", "two fingers held flat like a knife"; ch19 "as if she has found a track"; ch13 "Jaina's silence heavier than her footsteps" (Tic 6).

#### Skim of the other 20 outlines (repeats only)

Counts across all 25 outlines (about 58k words): "rather than" 74, "instead of" 103, ", not" 81 (about **258 contrast pivots**, roughly one every 225 words); "the room" 101; "becomes/turns into" 99; "lands/landing" 52; "finally" 47; "truth" 37; "settl-" 21; "shape" 20; banned document vocabulary 17. Short slogan beat-closers (eight words or fewer) appear in 17 of 25 outlines (for example "The hunt stops looking local.", "The first real success lands."). The register is uniform: the outlines are written in the voice the catalogues ban.

### a.7 Planner output: `plans/chapter1.json` and `scene-0/1/2-plan.json`

The scene plans are identical to `chapter1.json` for every field the writer gets, minus the verifier notes. The planner copies outline phrasing and adds its own:

| Quote (field) | Catalogue |
|---|---|
| "she **absorbs** the irritation by riding rather than answering" (B3 conflict) | HL "absorbed"; NA-P1 |
| "Irritation hardening into command; the loss of the day sits under it." (B5 emotion) | Abstract-noun locomotion |
| "Temper shoved down; anger turned to cold assessment." (B9 emotion) / "the name turns her irritation into a temper the stakes no longer allow. Beat 9 opens with her pushing it down." (B8 transitionIntent) | Abstract-noun locomotion; HL "assessment" |
| "Sylvanas reads the woods like her own hand" (B1 outcome) | Simile |
| "Leylines are an unverified claim relayed second-hand, not a known fact." / "(an unverified claim, not an established fact)" | NA-P1 |
| "It is not an anomaly and it is not a sign of the danger." / "is the normal living border **grid**" (constraint) | NA-P1; tech register ("grid") |
| "Lor'themar reads her excuse as an excuse." / "sees through it and lets it stand" (B2) | Tautology; permission-tag family ("lets it stand") |
| "Whether she is arrogant, terrified, or correct." (B7) / "spy, a diplomat, or both, and the leyline claim does not fit any of those" (B6) / "exhausted, furious, and very far from court" (arcPosition) / "stones, roads, or riders" (arcPosition) | Triplets carried over from the outline |
| "Her fury that nobody believes her shows in her body and how she holds herself." (B8) | F4: emotion named, then the body asked to show it |
| "Somebody has to ride south and somebody has to ride north, and Beat 5 is that call." (B4 transitionIntent) | Narratable sentence in a planner field |
| "A human mage is in a holding cell. No verified identity. No trusted warning." (scene 3 knowledgeAtSceneStart) | NEW: "No X. No Y." stack |
| "Beat 4 and Beat 7 are both report beats. Beat 7 must not replay the runner's account" (B7 plannerWarning) / "worked out after the runner had left the post" (constraint) | Meta-instruction. The output voices it as dialogue (b.13) |
| "One woman is in custody, and the other decides how hard the door stays shut." (team arc) | Epigram |
| sensoryAnchors "clipped shorthand", "tired breathing", "suffocating silence", "cold ward-light on her face", "blue ward-light on boots" | Leads straight into specific output lines |
| `newOnPageInformation` and `stillUnknownAfterBeat` written as full declarative sentences and question lists | NEW: each list item becomes one line of dialogue (b.14, b.17) |
| `"beatType": "scene"/"sequel"`, `valueShift`, "The Lie" (arcPressure) | Planning vocabulary. None leaked into prose |

### a.8 Inputs on the read path that the brief did not name

- **Writer agent prompt** (`.claude/agents/afternoon-writer.md`): "Include at least one involuntary interior moment: a flinch, a memory surfacing, **a stomach dropping, a heartbeat suddenly noticed**." This prescribes two AQ-02 body-language clichés. Also "Keep the POV character embodied: … old injuries" and "Join related actions… semicolons" (AQ-07 says semicolons in narration are a tic; `style-guide.json` says "Semicolons almost never").
- **`.afternoon/style-guide.json`** (slophunter and craft agents): "Where another character might think 'she was afraid,' Sylvanas narration says '**her hand found the bowstring**.'" (prescribes HL Contact Verbs) · example sentence "Jaina was still talking. **Sylvanas let her.**" (permission tag) · "She said it the way you report a bridge out. Fact, not feeling." (NS-A1 plus NA-P1) · "She counted the sentries without stopping her horse. Two on the gate, one on the roof…" (counting device) · "Anger: clipped commands, fingers tightening on reins" (gives v2's "Her fingers closed on the reins").
- **`style-samples/texture-transformations.md`** L119 (craft reviser): "Her shoulder burned. A bead of sweat crept from her hairline toward her left eye." This is chapter 1's own sentence fed back as a model. `v0c.md` rewrote v0's sentence into this form. v2 then added "and she let it".

---

## (b) Output tells with an input precursor

Stage: **W** = present in v0 (the writer's choice); **R** = introduced between v0 and v2 (v0c or v1); **S** = introduced by the slophunter (v2). "v2 Lnn" is the line number in `v2.md`. Link: **STRONG** = same construction or phrase; **LIKELY** = same habit.

### b.1 Planner text voiced as narration or dialogue (scene plans → writer)

| # | Output (stage) | Input precursor | Tell | Link |
|---|---|---|---|---|
| 1 | "Sylvanas could make three women out of that: one arrogant, one frightened, and one who'd simply been right in the wrong country." (W; v2 L257) | B7 stillUnknown "Whether she is arrogant, terrified, or correct." (outline: "arrogant, terrified, or completely correct") | Triplet; planner residue; F3 "simply" | STRONG |
| 2 | "A spy, then… An envoy, then… Or both." + "None of the three told a Farstrider post that the leylines were wrong." (W; v2 L207 to L211) | B6 "Her working guess is a Kirin Tor spy, a diplomat, or both, and the leyline claim does not fit any of those." | F6 claim→claim→conclusion; planner residue | STRONG |
| 3 | "Her ring. Her stones. Her rangers had put the irons on." (W; v2 L159) | arcPosition "unless it touches her stones, roads, or riders" | NS-A2 anaphoric fragment triplet | STRONG |
| 4 | "Whatever this was, it hadn't come from any court." (W; v2 L291) | arcPosition "a road-worn young mage who looks exhausted, furious, and very far from court" | F7 paragraph closer | STRONG |
| 5 | v0 "She was furious and she was exhausted" · "Nobody had believed her. It was in the set of her shoulders…" (W; cut in v2) | B8 "Her fury that nobody believes her shows in her body and how she holds herself." | F4 emotion label; NS-A6 | STRONG |
| 6 | "Waiting was no better than letting her go. It only looked more careful." (W; v2 L321) | B9 "Stalling the interrogation is judged as risky as releasing her." | NS-A1 aphoristic closer | STRONG |
| 7 | "what remained was cold and clear and could be used" (W; v2 L317); v0 "The temper came up in her all at once… It wanted somewhere to go." | B9 "Temper shoved down; anger turned to cold assessment."; B8 "Beat 9 opens with her pushing it down"; Sylvanas sheet word field "useful" | Abstract-noun locomotion (v0); polysyndeton | STRONG |
| 8 | v0 "The irritation came up in her like heat off a forge, and she didn't answer it. She touched her heels… instead"; v2 "Instead of answering, she touched her heels to the mare's sides." (W; R rewrote it, keeping "instead of answering") | B3 "she absorbs the irritation by riding rather than answering" | Abstract-noun locomotion; NA-P1 | STRONG |
| 9 | "He knew she would make him ride rather than make herself talk… Most people, when she put her heels in, fell behind." (W; v2 L91) | B3 "Lor'themar is the only person who can take her irritation without slowing her." | NS-A7 "Most people"; chiasmus | STRONG |
| 10 | "Which left the space beside her stirrup empty." (W; v2 L201) | B6 anchor "the empty riding position beside her; the runner falls in behind, not beside" | NS-A1 "Which…" fragment | STRONG |
| 11 | "That was how the Pass was meant to feel." (v0 "That was right. That was how it was meant to feel at the Pass."); v0 "It was fed off the **grid** like every lamp" (W; "grid" cut in v2) | Constraint: "is the normal living border grid… It is not an anomaly" | HL Planner Shorthand; tech register | STRONG |
| 12 | v0 "Nobody down there was expecting trouble from the south any more than she was." → v2 "Nothing at that post would want anything from her—nothing there ever did." (W; S made it an intent smear) | B3 "nobody down there expects trouble from the south either" | Planner residue; IS-P5 (v2) | STRONG |
| 13 | "I have Theris's version… Give me yours." / "**Theris says what she says. This is me.**" (W; v2 L229, L247); v0 "Theris told me that." / "What he wouldn't know, because Feren hadn't come back yet when I sent him…" | B7 plannerWarning "Beat 4 and Beat 7 are both report beats. Beat 7 must not replay the runner's account"; constraint "worked out after the runner had left the post"; Jaina sheet paired declaratives "I am explaining the situation. I am not asking whether it exists." | NEW: planner instruction spoken as dialogue; tautology | STRONG |
| 14 | Cyndia's briefing (v2 L231 to L255): track-back, "She stood up and asked him to wait", "reads like the trouble's inside it, not on the face", "Staff, pack, and a belt full of pouches" | B7 newOnPageInformation, in order: "reached the second ring" / "argued to stay and work" / "read as if malfunctioning from something inside them" / "staff and gear are in lockdown"; goal "Get the raw facts of the arrest from Cyndia" | Report-shaped dialogue (HL Document Voice; F2) | STRONG |
| 15 | "He gave it in pieces, as Farstriders were taught when they had no breath to spare." + "One human. A woman. A mage." Breath. … "Kneeling at a stone." (W; v2 L115 to L117) | B4 anchors "clipped shorthand", "tired breathing" (outline: "clipped patrol shorthand from tired breathing") | Fragment-chain report dialogue | STRONG |
| 16 | "No papers. No seal. No escort. Nothing on her that says who sent her." (W; v2 L121) | Scene 3 "No verified identity. No trusted warning."; B4 "without credentials" | NEW: "No X. No Y." stack | STRONG |
| 17 | "Her name." / "She hasn't given one." / "Who sent her?" / "Won't say." / "she doesn't know what the woman is or whether any of it means anything" (W; v2 L133 to L139) | B4 stillUnknown "The mage's identity. / Who sent her. / Whether the warning means anything." | NEW: checklist interrogation (unknowns list read out) | STRONG |
| 18 | "Tell them she said it. Not that it's true." (W; v2 L165) | Constraint "an unverified claim relayed second-hand, not a known fact"; Sylvanas sheet "Proof first. Theory after." | NA-P2 | STRONG |
| 19 | "It was a short **window**. The shot was the easy part." (W; v2 L35) | B1 conflict "the window is a heartbeat wide" | Correction pivot | STRONG |
| 20 | "He let it sit exactly as long as it took her to know that he knew, and to know that he knew she knew." (S; v0 "he just looked at her… for exactly as long as") · v0 "That was fair, and Sylvanas **let it stand**." (W) | B2 "Lor'themar sees through it and **lets it stand**"; "reads her excuse as an excuse" | Permission-tag family; recursive tautology | STRONG |
| 21 | "Two roads, and a body needed on each. Someone had to ride south… Someone had to ride north…" (W; v2 L155) | B4 transitionIntent "Somebody has to ride south and somebody has to ride north" | Planner residue | STRONG |
| 22 | "Either the old man had let his one apprentice walk out… or he had no idea where she was." (W; v2 L311) | B8 stillUnknown "Why Antonidas let her walk out alone. / Whether Antonidas knows where she is." | Planner residue | STRONG |
| 23 | "She had no reason to trust a word the woman said. She would get none standing in the doorway." (W; v2 L325) | B9 "interrogating without any reason to trust her is its own risk"; "Any reason to trust her." | NS-A1 aphoristic pair | STRONG |
| 24 | "She had expected violet… Every Kirin Tor she had met… had worn that face. This one hadn't." (W; v2 L275) | B8 "does not match the polished Kirin Tor type she expected"; arcPosition "expects a polished Kirin Tor problem" | NA-P5 cousin: expectation, then reversal | STRONG |
| 25 | "Sylvanas called up the watch-file from memory." … "*Worth watching.*" (W; v2 L301) | Constraint "checks it against the Farstrider watch-file she already carries in her head"; knowledgeLedger "one of the names worth watching" | Planner mechanism narrated | STRONG |
| 26 | v0 "not the easy walk of patrol traffic, nor the trot of a supply rider… but a single horse at a full gallop" (W; S cut) | B3 transitionIntent "hoofbeats coming in too fast for routine traffic" | NA-P7 | STRONG |
| 27 | "the mage" / "the woman" / "the human" / "the stranger" / "the prisoner" rotating for one person (W; v2 throughout) | Constraint "Jaina is 'the mage', 'the human', or 'the prisoner' in Sylvanas's head" | HL Elegant Variation (mandated by the plan) | STRONG |
| 28 | "The ward-light came down cold on her face and found nothing soft in it." (W; v2 L281) | B8 anchor "cold ward-light on her face" | The image comes from the plan; the `found` agency was added by the model | STRONG (image) |
| 29 | "The ward-light slid up over the toes of her boots" (W; v2 L329) | B9 anchor "blue ward-light on boots" | Inanimate agency | STRONG (image) |
| 30 | "This was the part of the day she liked best: the quiet after the kill…" (S) · v0 "Not the kill itself. The quiet after it" (W) | B1 transitionIntent "the quiet she wants to stretch"; outline "proves exactly why Sylvanas would rather stay out here" | Thesis line (F6); NA-P2 in v0 | LIKELY |
| 31 | "let the silence run until it belonged to her" + "Nobody spoke… Then that stopped too." (W; v2 L329, L335) | B9 anchor "suffocating silence"; IS guide L351 bad example "The silence held because she let it." (slophunter's path, kept) | IS-P7 / permission tag | LIKELY |
| 32 | "There would not be several letters. There would be dozens" (W; v2 L309); v0 "Not a clerk who'd lost her letters. Not one of the hundred violet hangers-on…" (W; S cut) | B8 outcome "has just become diplomatic and magical, not just a trespass" (outline "This isn't just a border trespass anymore. It's…") | NA-P5 / NA-P2 escalation | LIKELY |
| 33 | Density of contrast pivots: v0 has 14 ", not / Not …" constructions; v2 has 6 | Plan 16; Sylvanas sheet 10; outlines about 258 | Negation addiction | LIKELY |

### b.2 Voice-sheet habits (Sylvanas sheet, all scenes; Jaina sheet, scene 3)

| # | Output (stage) | Input precursor | Tell | Link |
|---|---|---|---|---|
| 34 | "Sylvanas's fingers found the bowstring before she had decided to reach for it." (W; v2 L105) | Sylvanas sheet "Fingers touch the bowstring when she is assessing risk." + "She angles herself toward useful ground without thinking about it."; also `style-guide.json` "her hand found the bowstring"; it is the HL L216 bad example word for word | HL Contact Verbs; IS-P8 | STRONG |
| 35 | v2 "She breathed out through her teeth" (L203); v0 "She let her breath out long and slow through her nose" ×2 | Sylvanas sheet "A longer exhale often stands in for visible emotion." | HL Breath as Universal Tell | STRONG |
| 36 | v2 "choosing footholds before she'd consciously seen them. That root would hold. That slab would slide."; v0 "her body picked the footholds before her eyes had finished finding them… She didn't think about any of it." | Sylvanas sheet "without thinking about it"; B1 "Sylvanas's read of footing, range, and openings is effortless" | Body-before-mind construction; IS-P8 (v0) | STRONG |
| 37 | "Sylvanas took the room first, as she always took a room. One door… A slit window… A ranger in the far corner…" (W; v2 L273) | Sylvanas sheet POV filter "exits, cover, approach lines…"; "Her eyes clear exits, cover, and bodies before the scene's social meaning." | F6 inventory paragraph; NS-A7 "as she always" | STRONG |
| 38 | "She could read a trail, a treeline, the set of a man's shoulders the moment before he lied… She could not read a leyline." (W; v2 L213) | Sylvanas sheet "when someone's body contradicts their words" / "whether magic changes the battlefield or only the explanation of it" | Anaphoric antithesis | STRONG |
| 39 | Command-fragment dialogue: "Report." "Her name." "Inside. Tell me as we go." "Open it." "Eyes south." "Give me yours. **Start before dawn.**" (W) | Sylvanas sheet "Questions often function as orders." "More commands than explanations"; samples "Again." "You crossed my ward line alone. **Start there.**" | F2 same-shape lines | STRONG |
| 40 | Sylvanas's Convocation quips: "The Convocation always wants to have known first. It's the knowing that tires them." · "Then he can paint the trolls too, and they can fight it out on the parchment." · "I told him the trolls would be grateful for his support." · "Tell him to paint a mage on his map." (W) | Sylvanas sheet Convocation samples "You sent a budget answer to a plague question. I noticed." / "You may call it a border matter if that helps you sleep. The dead will not." | Epigram/quip; NS-A7 in dialogue | STRONG |
| 41 | "He looked back. They always look back." / "The ones who don't are the ones who make it over the ridge." (W) | Sylvanas sheet "She speaks in finished judgments"; sample "Don't chase the noise. Kill what's making it." | Aphorism; NS-A7 | LIKELY |
| 42 | Lor'themar in the same shape: "I don't enjoy it. I'm *good* at it. There's a difference, and it's mostly that I've stopped expecting anyone to listen." · "Possibly a great many things." (W) | No Lor'themar sheet on the path. The only voice model loaded in scene 1 is the Sylvanas sheet, whose prose pivots on "X, not Y" (S4 to S7) | NA-P5; F2 same-mouth | LIKELY |
| 43 | "The muscles at the base of her skull drew tight, and she went very still." (R; v0 "she found she was standing very still") | Sylvanas sheet "Stillness means concentration, not calm."; Jaina sheet "Goes visibly still when the pattern clicks." | Stock stillness beat; Tic 3 | LIKELY |
| 44 | "The rangers moved without being told" · "fell back into file on their own" · "took the chestnut's reins unasked" · "Someone did." (W; ×3 or more) | Sylvanas sheet "half her sentences assume the order has already been understood" | Repetition tic | LIKELY |

### b.3 Style target (rhythm anchor → writer)

| # | Output (stage) | Input precursor | Tell | Link |
|---|---|---|---|---|
| 45 | Simile density: v0 has 11 `like` and 9 `as if/as though` ("like a cleaver going into a side of pork", "like dropped cutlery", "as though it had insulted her family", "as though the ground owed them money"…). v2 has 3 and 4 | Anchor: 3 `like` and 2 `as if` in about 1,350 words, plus "YOU MUST WRITE LIKE THIS" | HL Simile Overload | STRONG |
| 46 | "Trolls always ran as though the ground owed them money." · "Envoys did not come over the rocks in the dark. Envoys did not come alone." · "Dalaran had them; everyone did." · v0 "the woods went quiet in the way woods did…" (W) | Anchor "Shin were easy to ignore… They were generally right." / "Windspren often played pranks like that." | NS-A7 generalizing about a kind | STRONG |
| 47 | "He tried to salute and found his hand still wrapped in the reins." (W; v2 L111) | Anchor "as Kaladin tried to toss his wooden bowl aside, he found that it stuck to his fingers" | HL discovery-wrapper `found` (same "tried to / found / hand stuck" frame) | STRONG |
| 48 | Polysyndeton: "lilies and lamp oil and warm velvet", "honey and sap and the peppery bite", "pine and juniper and twisted thorn", "tired and stubborn and not budging", "cold and clear and could be used" (W) | Anchor "danced, and drank, and yelled, and sang, and clapped" (header: "polysyndeton") | HL triple and chaining | STRONG |
| 49 | One-line punch paragraphs: "No." (v0 ×2, v2 ×1), "She was sitting up straight.", "Start talking." (W) | Anchor header "gut-punch short sentences after long ones"; "Everything felt wrong." / "He walked back to the warcamp alone."; Jaina sheet "it should hit like a snapped wire" | F7 / NS-A1 punch | STRONG |
| 50 | "Her face went hot. At the human for coming. At Dalaran for… At six stones on her hillside…" (W as a comma list; R split it into fragments; v2 L317) | Anchor "Stained with Dallet's blood. Toorim's blood. The blood of the men…" | Anaphoric fragment triplet | LIKELY |
| 51 | "A scribe's hand. A student's." · "Kul Tiran. The coat's ship's-officer cut… The fair hair coming down. The ink." · "Good." · "Eight." (W) | Anchor "Shash, the last glyph read. Dangerous." | NS-A1 verdict fragment | LIKELY |
| 52 | Echo exchanges: "…set something down." / "The book." / "The book." · "Kneeling." (echoing the runner) · "Possibly." / "Possibly a great many things." · "Several letters." → "There would not be several letters." (W) | Anchor "'Take it, Kaladin'… 'Take it,' Coreb said again." / "'Jam.' … 'Jam.'"; Sylvanas sample "Again." | NEW: echo exchange | LIKELY |
| 53 | "'I was about to observe,' he said mildly" (W) | Anchor "said softly", "asked softly", "Shallan noted" | AQ-06 adverb-on-tag | LIKELY |
| 54 | Triplets in dialogue: "Could be her, could be there before her, could be nothing but his hands are tired." · "Staff, pack, and a belt full of pouches" · "No papers. No seal. No escort." (W) | Plan triplets (b.1 #1 to #3); anchor "beatings, deprivation, and brutality" | Triplet habit | LIKELY |

### b.4 Pipeline prompts and catalogues (writer prompt → v0; craft reviser and slophunter priming → v2)

| # | Output (stage) | Input precursor | Tell | Link |
|---|---|---|---|---|
| 55 | "Her stomach dropped—a short, ugly lurch, like missing a stair in the dark. She could hear her own heartbeat…" + "For an instant she was five years old…" (W; kept in v2 L305, L123) | Writer prompt "a flinch, a memory surfacing, **a stomach dropping, a heartbeat suddenly noticed**"; HL good example "She couldn't hear anything but her own pulse" (slophunter kept it) | AQ-02 "Stomach dropped", "Heart pounded" | STRONG |
| 56 | "the old ache she'd brought home from a winter spent lying on a frozen ridge above Zul'Aman" (W) → v2 "until the old ache settled back into the joint" (R, v0c) | Writer prompt "old injuries"; v2's wording is the HL L218 bad example word for word | HL Contact Verbs (sensation settles) | STRONG |
| 57 | Semicolons in narration: "That was Cyndia, word for word; Sylvanas could hear her", "Dalaran had them; everyone did." (W) | Writer prompt lists "semicolons" as connective tissue | AQ-07 semicolons in narration | STRONG |
| 58 | "A bead of sweat crept from her hairline toward her left eye, **and she let it**." (S; v0 had "She didn't blink it away.") | HL L203 bad example "A bead of sweat crept toward her eye, and she let it." and IS guide L224, word for word; `texture-transformations.md` L119 (adopted at v0c). Slophunter note: before "She didn't blink it away." → after "and she let it." | HL Permission Tags. **The slophunter's fix is its own catalogue's bad example.** | STRONG |
| 59 | "Her fingers closed on the reins." (R: v0c, replacing v0's forge simile) | `style-guide.json` (read by the craft reviser) "Anger: clipped commands, fingers tightening on reins" | Prescribed emotion-signature beat | STRONG |

**(b) totals: 59 links. STRONG 44 (#1 to 29, 34 to 40, 45 to 49, 55 to 59). LIKELY 15 (#30 to 33, 41 to 44, 50 to 54).**

---

## (c) Output tells with no precursor (the model's own)

These have no matching construction or phrase on the read path of the stage that produced them.

| # | Tell (stage) | Examples | Catalogue |
|---|---|---|---|
| C1 | **"General" vocative on almost every subordinate line** (W, all kept) | 14 in v2: Theris "Hands on it, General." "No, General." "She said it a great many times, General."; Cyndia "Before dawn's the trouble, General." "She had two hundred yards on him, General," "Six since noon, General," "I'm not ranked for that kind of talk, General," "Not where she can hear it, General." "That's the name in it, General."; the ranger "Yes, General." | NEW: vocative rank tag as rhythm filler. No input models subordinates addressing her. **Gap:** no voice sheet exists for Cyndia, Theris or Lor'themar, and `cyndia.md` (off the writer's path) says only "crisp, professional, volunteers good field observations" |
| C2 | Counting devices (W) | The troll tally "Two in the creekbed… Three along the deer track… One… One… And this one… Eight. The sign at the creek had said eight."; "She had counted the windows, then the panes… the pearls" | Repo skills ban "counting devices"; not in the listed catalogues. `style-guide.json` models it, but the writer does not read that file |
| C3 | Body-part and inanimate agency (W/S) | "legs that hadn't heard yet" · "Her back teeth knew when she passed a ward-stone" · "a timber palisade huddled behind it" · "grey boulders shouldering up" · "within ten breaths the woods had gone back to their business" · "until the trees folded over the sound" · v0 "the woods had decided the killing was over" | IS-P5/P6/P8; HL Inanimate-Subject Agency |
| C4 | Stock body-language beats (W) | Cyndia "arms folded across her chest" and "arms tightening over her chest" · "A muscle jumped along her jaw." · "Her jaw locked, and her fingers tightened on the bow grip" · "He frowned" · "He swallowed." | AQ-02 crossed arms and clenched jaw; Tic 3; F2 kill list |
| C5 | Corner-of-mouth micro-expression (W) | "That got a twitch at one corner of his mouth, there and gone before she'd properly seen it." | Tic 1. The slophunter's HL good example (L117) then endorses it, so it survives |
| C6 | Gaze contest (W/S) | "This time she held it and did not look away first." · "The mage had to tip her head back to meet her, and she did." | Tic 5 |
| C7 | Quip closers at paragraph ends (W) | "She didn't know which was worse. She suspected she was going to find out." · "So much for the post that never wanted anything from her." · "They were all fine." · "Somebody would have to scrape that pot." · "It had never entirely left." | F7 "And somehow, that was worse" family |
| C8 | Chiasmus and anadiplosis in narration (W) | "Close enough to reach. Close enough to be reached" · "Tomorrow would be worse. Tomorrow was the frontier allotment, and the frontier allotment meant her." · "She knew the cloak before she knew the face" · "room enough to sit up straight… / She was sitting up straight." | NEW: rhetorical-figure density (closest: NS-B1 sentence too polished) |
| C9 | "the kind of" (W) | "the kind of thin, freckled face that would still look nineteen when he was two hundred" (the plan has no "kind of"; the outline does, but the writer never sees the outline) | NS-A7 |
| C10 | Stacked descriptors (W/R) | "the same patient, far-too-knowing face" · "Lean and scout-built, young for a post commander" · "heavy blue-grey wool, double-breasted and buttoned to the throat, cut like a ship's officer's coat and stiff with dried mud" | HL Stacked Descriptor Clusters |
| C11 | Emotion as temperature (W/R) | "Her breastbone went cold." · "Her face went hot." · v0 "Something went cold and small under Sylvanas's breastbone" | NEW (with HL "Something" in v0) |
| C12 | Filter verbs (W) | "Sylvanas watched it go in and stay there" · "before she'd properly seen it" · "She knew that look, too." | F3; HL POV Distance |
| C13 | Permission tag in v0 (W) | "He let that sit for a few strides." | HL Permission Tags (nothing on the writer's path; v2's second instance traces to the plan, b.1 #20) |
| C14 | Negated clichés (W, cut by S) | v0 "He didn't raise an eyebrow, or sigh, or point out…" · "Cyndia didn't quite roll her eyes." | AQ-02 cliché plus NA-P5. The writer does not read the catalogue that lists these clichés, so this is its own reflex |

**(c) total: 14 tell families.**

---

## Dialogue in v2: what cues the briefing register

The question was whether the voice sheets or the scene plans cue report-shaped briefings, the "General" tag, echo exchanges, triplets and tautologies. Most of it comes from the plan, then the Sylvanas sheet, then the rhythm anchor.

1. **Report-shaped briefings: the scene plan, STRONG.** Beats 4 and 7 are framed as report beats ("Receive the runner's report", "Get the raw facts of the arrest from Cyndia", plannerWarning "Beat 4 and Beat 7 are both report beats"). Their content is given as `newOnPageInformation` lists of declarative sentences and `stillUnknownAfterBeat` question lists. The writer turns each list item into one line, in list order (b.14, b.17). The verifier's research note "Characters should talk around facts, interrupt, and withhold" exists in `chapter1.json` but is **removed from the scene plans**, so the writer never sees the one instruction that argues against briefings. The anchor "clipped shorthand" adds the runner's fragment style (b.15).
2. **"General" as a tag: no precursor.** Nothing on the path models how subordinates address Sylvanas. The Sylvanas sheet's audience table gives only her register *toward* Farstriders. With no Cyndia, Theris or Lor'themar sheet, the model falls back on a stock military-subordinate voice. This is a gap, not a bleed (C1).
3. **Echo exchanges: LIKELY from the anchor.** Its dialogue section repeats "Take it" and "Jam" across turns. The Sylvanas sheet's one-word samples ("Again.") support it (b.52).
4. **Triplets: STRONG from the plan, LIKELY from the anchor.** The plan hands over five ready-made triads (b.1 #1 to #3, #16, #17), and the anchor models polysyndeton and fragment triplets.
5. **Tautologies: STRONG from the plan.** "Theris says what she says. This is me." and "I have Theris's version. Give me yours." act out the plannerWarning that Beat 7 must not replay Beat 4. "He let it sit… that he knew she knew" amplifies the plan's own tautology "Lor'themar reads her excuse as an excuse." The Jaina sheet (loaded in scene 3) adds the paired-declarative model "I am explaining the situation. I am not asking whether it exists."
6. **Quips everywhere, same mouth: STRONG from the Sylvanas sheet.** Its samples are nearly all epigrams. Because it is the only sheet loaded in scenes 1 and 2, Lor'themar and Cyndia borrow its shape: "I'd like very much to have." · "He wants a magister. I told him he could have one when I did."

---

## (d) Input changes that would remove the most bleed, ranked

1. **Change what the scene plans hand the writer** (removes most of b.1, 33 links, plus the briefing register).
   - Write `newOnPageInformation`, `stillUnknownAfterBeat`, `emotion`, `transitionIntent` and `constraints` as terse keyed facts: no sentences, no triads, no "X, not Y", no emotion names.
   - Move `plannerWarning` and the constraint rationales ("must not replay", "is not an anomaly", "watch-file she carries in her head", "the mage/the human/the prisoner") out of the writer's copy and into a checker-only field.
   - For report beats, add a dialogue-mode line ("facts arrive out of order, withheld, argued over; the speaker does not use a title per line") and keep the verifier's "talk around facts" research in the scene plan instead of stripping it.
   - Fix the planner prompt so it does not copy outline triads ("arrogant, terrified, or correct") and abstraction-motion lines ("Temper shoved down; anger turned to cold assessment") verbatim.
2. **Rewrite `sylvanas-voice.md` and add voice sheets for Lor'themar, Cyndia and a generic Farstrider runner** (removes b.2, 11 links, plus C1 and the same-mouth quips).
   - Delete the three prescribed physical tells: "Fingers touch the bowstring", "A longer exhale often stands in for visible emotion", "without thinking about it".
   - Rewrite the sheet's own prose without "X, not Y" pivots.
   - Cut the quip samples to one or two, flagged as rare. Drop "Proof first. Theory after." (it matches an always-kill calibration).
   - Remove the shared "You mistake X for Y" and "You take X. I'll take Y." frames across the three sheets.
   - The new subordinate sheets should state: rank or name at most once per exchange, reports partial and out of order, interruptions and disagreement allowed.
   - In `jaina-voice.md`, replace "That isn't proof. That's residue pretending to be proof." (NA-P5b, zero legitimate uses) and the "No--that's not the problem" syntax rule.
3. **Replace or annotate the style target `writer-rhythm-anchor.md`** (removes b.3, 10 links).
   - The writer is ordered to "WRITE LIKE THIS". The target holds 5 similes in 1,350 words, labeled polysyndeton, generalizations about a kind ("They were generally right."), a discovery-wrapper `found`, said-bookisms and adverb tags, generic nod/smile beats, echo dialogue, and an explicit "gut-punch short sentence" instruction.
   - Either pick excerpts without these, or add a short "copy the sentence-length variation only; do not copy similes, 'and… and' chains, generalizations, 'found that', or repeated lines" header.
   - The anchor and the slop-hitlist currently contradict each other.
4. **Purge chapter 1's own sentences from the catalogues and fix the "good" examples** (removes the bleed after the writer, b.4 #56, #58, #59, plus the survival of #34, #47, #55 and C5).
   - The HL bad examples for permission tags and contact verbs, `texture-transformations.md` L119, and `style-guide.json` ("her hand found the bowstring", "Sylvanas let her.") are this chapter's own sentences. The slophunter wrote the HL bad example "and she let it" into v2 as a *fix*.
   - Use out-of-domain examples.
   - Correct the good examples that carry tells: "her hips moved before she told them to", "Almost a smile", "The corner of her mouth moved", "A stillness spreading from the jaw", "bloomed outward", "The certainty… buckled", "The air between them went taut", "let the pieces collect", "her gaze swept the room", "she saw it", "the real words, not the careful ones".
   - Also fix the alternative "filed" in Tic 2.
5. **Edit the writer agent prompt** (removes b.4 #55 to #57).
   - Replace "a flinch, a memory surfacing, a stomach dropping, a heartbeat suddenly noticed" with a non-enumerated instruction, or with a list of *banned* stock moments. The current list produced the chapter's stomach-drop and heartbeat lines.
   - Drop "semicolons" from the connective-tissue list (`style-guide.json` says "Semicolons almost never").
6. **Clean the outlines upstream** (lowers the plan bleed at its source, for all 25 chapters).
   - About 258 contrast pivots ("rather than", "instead of", ", not").
   - 101 instances of "the room", often as an actor.
   - Slogan beat-closers in 17 of 25 outlines.
   - Banned vocabulary: "vector" (ch18, ch19), "ingestion" (ch4, ch7), "trajectory" (ch18), "geometry" (ch9, ch13), "operational" (×6).
   - Emotion labels ("exhausted, furious").
   - Triad hypothesis lists.
7. **Character files (lowest; off the writer's path).**
   - Fix "devastating… simply" (`supporting.md`), "trajectory" (`uther.md`), "not approval but recognition" (`jandice.md`, near-identical to a PC-P1 kill calibration), and the body-decides lines in `cyndia.md`.
   - These only matter where the planner quotes them into `enrichment`, which the scene-plan split strips anyway.
   - **Prediction:** `kelthuzad-voice.md` is not used in chapter 1, but its "No X. No Y. No Z.", NA-P7 chains, IS-P5 "the plague listens… waits" samples and completion-echo device will bleed into chapters 10 to 12 when Kel'Thuzad enters a scene's `castInScene`. Fix it before those chapters run.

### Verdict on the theory

Supported, with one change. The writer imitates the register of the **files it actually reads**:

- the scene plans (33 links);
- the Sylvanas and Jaina voice sheets (11);
- the rhythm anchor (10);
- its own prompt (3).

The editing stages imitate **their priming files**: the craft reviser adopted `texture-transformations.md` and `style-guide.json` wording (#56, #59), and the slophunter wrote its own catalogue's bad example into v2 (#58) and kept several others. The outlines and character files bleed only through the planner's copy. Fourteen tell families have no precursor. Of those, the "General" tag and counting are the most visible, and both trace to a missing input (subordinate voice sheets) rather than a bad one.
