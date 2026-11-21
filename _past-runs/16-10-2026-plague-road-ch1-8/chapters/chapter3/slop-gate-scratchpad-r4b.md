# Slop-Gate Scratchpad - chapter3 / pass b (iteration 4)

Target: v2-r4.md

POV CHARACTER: Sylvanas Windrunner
REGISTER SUMMARY: Ranger-General, tracker and field commander. She thinks in ground, prints, sightlines, drills and horses. Her inner voice argues with itself (questions, bad answers, overrules), is dryly contemptuous of humans and magisters, mocks herself in terms of the ranger she would flay, and swears by the sun or with "Damn". She would not think in thematic captions, essay generalities or polished epigrams about meaning.
REGISTER CONFIDENCE: HIGH (voice sheet plus a full chapter of interiority)

False-positive filter sources: chapter3.json (B1-B11, constraints, knowledge ledger), sylvanas-voice.md (inner-voice section), neral-voice.md ("when it comes she says it back in plain words"), jaina-voice.md ("uses titles... 'Ranger-General' early, a little too correct").

## gpt-5-prose-issues.md (37 keeps)

**KEEP** | F3 filter (watched) | L13 | deliberate act
> Sylvanas watched her own mare's ears.
Watching the ears is the deliberate act. She is using the horse as an instrument because her palm cannot read cobbles, and the next paragraph argues with herself about exactly that.

**KEEP** | F3 filter (watched) | L129 | sentry action
> Sylvanas watched the roads, then the mage kneeling with the staff across her thighs, then the roads again.
The sweep order is the content: she is the guard covering a kneeling mage. Without "watched" there is no actor for the sweep.

**KEEP** | F3 hedge (nearly) | L133 | changes the fact
> The mage was very still, the steam of her breath nearly stopped.
"Nearly stopped" and "stopped" are different facts. Stopped would mean she is not breathing.

**KEEP** | F3 hedge (nearly) | L448 | changes the fact
> so still that Sylvanas had nearly forgotten her.
Degree is the fact. She had not forgotten her, and the next line has the mage speak.

**KEEP** | F3 hedge (nearly) | L450 | comparison
> The mage's voice was pitched down nearly as low as Neral's
A comparative measure, not a softener.

**KEEP** | F3 hedge (nearly) | L606 | light level
> Under the hazel it was still nearly night.
A light-level fact at first light, set against the grey at the mouth of the cut.

**KEEP** | F3 hedge (nearly) | L818 | changes the fact
> The mage woke when the mare put her head down to drink and nearly went over it.
She did not fall. That is the fact.

**KEEP** | F3 hedge (nearly) | L822 | precision
> tick on tick so close it nearly ran together into a hum.
Calibrates the crystal against the cut reading. A full hum would be a different reading.

**KEEP** | F3 hedge (as if) | L608 | simile, not hedge
> as if something had dragged a harrow up it with the tines set close.
Tool-flagged (simile_as_if, mapped to pass A). Deleting "as if" breaks the simile. The harrow comes from farm country she has ridden through, and the image cashes out in the next paragraph's measured grooves.

**KEEP** | F3 hedge (as if) | L738 | voice
> the cob stopped as if it had been hoping to
Dry horse humour from a horsewoman. The "as if" carries the joke and is not padding an uncertain perception.

**KEEP** | F3 hedge (might have been) | L626 | toolSignal hedge_might_have_been | uncertainty is the point
> into a long smear that might have been anything.
The eye cannot classify the smear, then "The long smear was heavy". The scene's turn is the staff reading what Cyndia and Sylvanas cannot, so the reader has to share the uncertainty. This matches Cyndia's earlier "Could be a foot. Could be something pulled along. I can't tell you which."

**KEEP** | F3 hedge (a little) | L283 | per-scene allowance
> Cyndia lowered the lantern a little.
A small physical degree on the one object she holds. It is the only "a little" softener in scene 1, which is inside the guide's "one or two per scene is character voice" allowance.

**KEEP** | F3 hedge (a little) | L404 | per-scene allowance
> The whisper had a little more in it now, wet and hoarse.
Degree of recovery in the child's voice. One of two in scene 2.

**KEEP** | F3 hedge (a little) | L524 | per-scene allowance
> She shifted the girl a little on her lap
The second and last in scene 2. Low density. (L434 "a little way" and L726 "a little way from her ears" are distances, not hedges.)

**KEEP** | F3 temporal (a moment) | L780 | duration is the point
> Cyndia had turned her head after the wagon and held it there a moment before she turned it back to the road.
How long she held it is the signal. The plan has Cyndia register the odd farewell here as corroboration for Ch 15.

**KEEP** | F3 filter (could hear) | L810 | perception is the event
> She kept her face to the road. She could hear it.
She keeps her eyes front and takes the missing horses in by ear. The hearing is the beat, and the colon list after it is what she hears.

**KEEP** | F8 / F10 echo, stacked fragments | L436 | character voice (neral-voice.md)
> "The baby first," Neral said. "Then Mister Pell. Then everybody at the well."
The voice sheet says: "One question at a time. She waits for the answer, and when it comes she says it back in plain words." She "talks to the child... in short sentences." Here she puts the corrected order back to the child to confirm it, and gets a nod.

**KEEP** | F8 echo | L432 | elicits new information
> "Mister Pell."
The one-word repeat draws the correction ("No... Missus Hale's baby"), which is the guide's NOT-F8 case.

**KEEP** | F8 echo | L444 | elicits new information
> "Sweet," Neral said.
The one-word repeat draws "Pears gone brown... We didn't have any pears." NOT-F8.

**KEEP** | F8 echo | L309 | elicits new information
> "Underneath."
Draws "And then I heard it... There's somebody breathing down there." NOT-F8.

**KEEP** | F8 echo | L652 | elicits new information
> "Sixty."
Draws "At least" and the no-turn-off, none-came-back report.

**KEEP** | F8 echo | L750 | shock plus new fact
> "Dead." He turned the hat round in his hands. "Millhaven? I was through here on market day."
A stunned repeat that goes straight on to a new fact (market day).

**KEEP** | F9 vocative (Jaina "Ranger-General" x3 in scene 1) | L35, L161, L211 | character voice (jaina-voice.md)
> "Ranger-General, it's right under us." / "I'm sorry, Ranger-General." / "Ranger-General, a store is where things end up."
The voice sheet fixes "'Ranger-General' early, a little too correct" and "uses titles, and the courtesy stays in place even when she refuses." She is a prisoner addressing her captor's rank.

**KEEP** | F9 name-only | L135-143 | summons is the event
> "Mage." / "Proudmoore." / "*Proudmoore!*"
The plot event is calling her back out of the deep read ("Louder than last time, please"). The escalation is the action.

**KEEP** | F9 name-only | L195 | procedure established
> "Mage."
The same agreed call to bring her up out of a read, and she answers it at once.

**KEEP** | F9 name-only | L257 | call across distance
> "Mage."
A one-time call to the mage at the corner of the wall, after which she comes over.

**KEEP** | F9 name-only | L790 | procedure
> "Ranger-General."
The relay rider reports mounted and ready to her commander. Neral's voice sheet makes the title her only form of address.

**KEEP** | F9 vocatives (rangers) | L29, L91, L101, L291, L301, L552, L614, L650, L680, L794 | procedure
> "Ranger-General."
Field subordinates addressing the commander. This is address that procedure requires. L650 is explicitly a formal report ("the way she had stood to give a report at the Pass").

**KEEP** | F12 non-action | L145 | strongest in scene 1
> The mage did not lift her head.
The scene turns on it. She does not answer the shout, so Sylvanas tears the hand off the frost.

**KEEP** | F12 non-action | L372 | strongest in scene 2
> Neral did not touch the ring.
The child has to draw the bolt herself. The cellar scene turns on that restraint.

**KEEP** | F12 non-action | L734 | strongest in scene 3
> Sylvanas did not draw.
Both rangers have just raised their bows, so the held draw is news and sets up "Hold."

**KEEP** | F2 beat | L476 | specific function
> Neral turned her head.
Neral reacting to the mage breaking her one-question rule with a hard question to a child. It does visible work in the interview. (The "turned her head" tic count belongs to pass A.)

**KEEP** | F2 nods | L438, L488, L550 | specific detail or answer
> The girl nodded, her fist clenched round the scrap of blue... / A nod. / Neral nodded. She had already started to rock the girl.
L438 and L550 carry character-specific physical follow-through. L488 is the child's answer to a question.

**KEEP** | F2 swallowed | L618, L822 | physical symptom
> she swallowed, and swallowed again / She swallowed twice.
Nausea with the greenish face in both places. This is a physical symptom, not an emotion label.

**KEEP** | F4 / F7 | L51 | adds factual connection
> He had not come back for it.
It hinges the intention clause ("means to pick up again after he has eaten") to the outcome and sets up the next paragraph's question about drills. That is a factual connection, not an emotion gloss.

**KEEP** | F14 fenced comparative | L640 | changes the fact
> The mage went along with the staff, slower now, leaning on it.
Progressive fatigue, which the plan requires. It is a change from her earlier pace, not padding.

**KEEP** | F13 / F11 | L838-840 | intentional structure (plan B11)
> That was not the same as following the mage. / It was not the same.
The plan wants her to tell herself it is the trail and not the mage. The repeat is her insisting, and it is meant to read as self-persuasion. (L710 "That was true, and very convenient" carries new content too: she suspects her own motive.)

Scene-level checks (recorded for completeness, no separate count): F1. The telegram runs fall almost entirely in dialogue exchanges and tactical scans, and no narration stretch repeats one shape across 3+ paragraphs. The rhythm and texture deficits are carried in the notes summary. F5. Jaina's refusal at the granary, the carter's ordinariness and Lyriel's warmth are all plan beats, and Cyndia's raised bow keeps the tension. F6. No thesis-opening paragraphs. F15. Scene endings (L295 walking up the lane, L598 hand off the string, L672 glove on, L852 dog barking) end on action or image with no "for a while" coda. F7. L17 "It had not done the door much good." and L830 "There never was." are dry inner asides she could mutter, not emotional summaries. F11. L73 "Fled, then... Taken, then." is a hypothesis list (plan B2), L253 "If he's drunk. If he's mad. If he's—" breaks off mid-thought, L810 "no bay... no grey... no fourth ranger" lists absences where each item is its own fact, and L836 "On a human's read. On a prisoner's." is the self-argument her voice sheet describes. Pass A routing: L426 "Neral did not ask again." and L584 "Sylvanas did not sleep." each have a positive pivot after them, so they belong to the negation guide. L446 ", very matter of fact" sits on a speech verb (adverb-on-tag), which is pass A.

## narrator-seep-guide.md (34 keeps)

**KEEP** | A7 | L5 | operational baseline
> It was the hour when a village this size should be banking its fires...
Her baseline for reading a village, used right away against "every chimney was cold".

**KEEP** | A7 | L9 | operational knowledge
> A horse bred at the wards sidestepped once at a stone, thought about it, and stood like a post...
Ward-horse training she knows, used to read this mare's refusal as a signal.

**KEEP** | A7 / A1 | L15 | inner voice
> Any ranger who took her reports from a horse's ears would walk the outer ring for a month. Well; the horse had the better ears tonight.
Self-mockery in terms of punishing a ranger, which is on her voice sheet.

**KEEP** | A7 / F7 | L17 | dry contempt for humans
> humans hung them so when they wanted their luck to pour out... It had not done the door much good.
Her voice sheet: "short with... humans and their roads." She could mutter it.

**KEEP** | A1 | L19 | tracker inference
> No rot under it, and she liked that no better.
No rot means no bodies, which is the next problem. Active assessment.

**KEEP** | A7 | L51 | evidence-based inference
> the way a man lays down a tool he means to pick up again after he has eaten.
Reading the drawknife like sign. She uses it to infer intent to return.

**KEEP** | A1 | L57 | dry linkage
> Here it was again with more chairs.
Ties Cyndia's farmhouse report to this house. Deadpan aside.

**KEEP** | A7 | L73 | operational elimination
> People who flee take the coat, and the bread and the cow and the child's toy...
A tracker rule used to strike "fled" from the list of three hypotheses (plan B2).

**KEEP** | A2 | L77 | inner self-correction
> A doe was a doe. A wheelwright was something else.
She refuses to extrapolate from the doe, and it reappears as the explicit imperative at L317 ("Don't. A doe is a doe. Find out."). She can say it under her breath, and it is part of her method.

**KEEP** | B1 | L85 | deadpan humour
> The cat looked better fed than her rangers and did not care in the least...
Her humour per the voice sheet: dry and dismissive.

**KEEP** | A7 | L87 | voice and practical reason
> carved by somebody who had never studied a horse... because things on floors get trodden on in the dark
Elven horse snobbery plus a field habit.

**KEEP** | A1 | L163 | prejudice, fact-bearing
> It was a straight answer, at least, and Sylvanas had not had many of those from a mage in her life.
It adds her history with magisters and is the first arc step toward listening (plan B3).

**KEEP** | A1 | L213 | arc turn with carrier
> It was the right answer. The ground in a clearing that was trampled deepest was where the herd had milled about...
Her own field rule is the basis, given in the next sentence.

**KEEP** | A7 | L251 | operational inference
> Nobody with feeling in his feet walks out of his clog in autumn mud and keeps going.
A tracking rule used to read the abandoned clog.

**KEEP** | B1 | L279 | inner argument
> Call it north and be wrong... And what would she be calling it on? A clog and a feeling.
The question-then-bad-answer shape from the voice sheet.

**KEEP** | B4 | L285 | ranger metaphor
> that somebody was the only clean track she was going to get.
"Track" comes from her own domain.

**KEEP** | A2 | L317 | inner imperative
> Don't. A doe is a doe. Find out.
An action-ending argument with herself.

**KEEP** | B3 | L357 | inner question
> What kind of man tells his child that and then goes out of his own door into the dark?
This is about the man, not the story's significance. It works as inference (he knew what he would become).

**KEEP** | B1 | L366 | tactical projection
> She'd be in the far corner of it, all teeth. Let Neral do it.
A decision in progress.

**KEEP** | A7 | L468 | operational dismissal
> Every village south of the Pass had a new man with a cart once a season...
The plan needs the grain-seller to stay a weak, unconnected clue, and this is her reason to shelve it.

**KEEP** | A1 | L482 | credibility assessment
> A shaving glass. A frightened child didn't make that up.
She is weighing the witness for a dispatch. Active.

**KEEP** | A1 | L516 | skeptical assessment
> There had never been hundreds of anything in Millhaven but hens.
Deadpan. She checks the child's count against the village size.

**KEEP** | A1 | L532 | owning a fault
> Too late to take it back.
Voice sheet: "She owns tactical fault fast and flat."

**KEEP** | B1 | L546 | self-aware bias
> pointed north, because she wanted it to.
Callback to L279. She is suspicious of her own pull north.

**KEEP** | A5 | L586 | concrete source named
> she had not known it would be so loud. The race.
The source (the mill race) is named right away. This is physics, not a mood label.

**KEEP** | B1 | L596 | grudging recognition
> She sat there waiting for the sun like Sylvanas, so she could go and look at something.
POV inference about the mage, and it leads straight into "Go to bed, mage."

**KEEP** | A1 | L604 | decision in progress
> A living man's hand, some morning before all this. It meant nothing. She went through.
Dismissed and then acted on.

**KEEP** | B1 | L634 | evidence-based realization
> They had passed each other with the whole hill between.
Comes straight out of the road-vs-cut geography laid out in the same paragraph.

**KEEP** | A1 | L708 | practical acceptance
> It would have to do.
The blurred seal is accepted and the action continues.

**KEEP** | A7 generic "you" | L710 | the one allowed use
> you did not hand a Kirin Tor apprentice to a relay rider with a child on her saddle.
The only generic "you" in the chapter. It is her own operational rule, which the guide allows once.

**KEEP** | B2 | L744 | plan constraint
> It was a face she would not have known again in a crowd
The plan requires the carter to read as forgettable, and the specifics follow straight after.

**KEEP** | A1 | L762 | tactical evaluation with reason
> It was what she had wanted from him, given plainly, and it was no use to her at all. Millhaven had been busy as you like on market day.
Plan B9: the information is real but too normal to flag anything. The reason is given.

**KEEP** | A1 / A7 | L780 | plan B10
> or nothing at all, which was likeliest. Some hill saying, a carter's grandmother's. It had caught on her...
The farewell snags and she does not build a case. That is exactly the planned beat.

**KEEP** | A1 | L830 | bitter aside
> Nothing in the hide or the bones of her hand. There never was.
Callback to L15 and L177. Her own frustration that her palm cannot read what the mage reads.

Also screened and kept, without separate entries: A8 openers L19 ("from some kitchen" + named milk), L341 ("Down in the lane the mill race" names its source) and L734 (she hears the wagon before it crests the bridge, and the bows come up on the sound). L804 "Human country. Fat and flat..." and L812 / L832 are tactical disdain and her voice-sheet line "Duty against the trail".

## phantom-concreteness-guide.md (17 keeps)

**KEEP** | P5 | L105 | anchored shorthand
> Nothing to read, then. Fine; the mage.
"The mage" is the well read she put off at L37-41 ("Then it will still be here when we've opened the doors"), and it happens in the next lines. Inner semicolon shape from the voice sheet.

**KEEP** | P3 | L109 | anchored shorthand
> so she made it better.
Cashed out in the same paragraph: Lyriel on the gallery, Cyndia at the smithy corner, the handcart moved for the bridge sightline.

**KEEP** | P5 | L215 | anchored shorthand
> Damn her, then. The hand.
The next line is "Close it." and the grey palm is in the paragraph before.

**KEEP** | P3 | L279 | evidence-based
> A clog and a feeling.
The clog is on the page (L249) and the feeling is named (her pull north).

**KEEP** | P4 | L285 | evidence-based inference
> that somebody was the only clean track she was going to get.
The window/door/gap-in-a-wall logic is in the same sentence.

**KEEP** | P4 | L313 | evidence-based inference
> Five days at the most.
Fur grown over the dregs, in the same sentence.

**KEEP** | P3 | L596 | anchored
> so she could go and look at something.
The referent (the cow way at first light) is set at L558 and L592.

**KEEP** | P3 | L604 | anchored
> It meant nothing.
"It" is the rope loop she has just studied.

**KEEP** | P5 | L656 | named objects
> A drover's print; a horse's.
Names exactly what she is hunting for.

**KEEP** | P5 | L706 | named evidence
> She had sixty in a cow way.
Sixty counted tracks in a named place.

**KEEP** | P5 | L752 | evidence-based inference
> Empty going up, full coming down.
Grain dust packed in the plank cracks is the sign, in the sentence before.

**KEEP** | P3 | L838 | intentional structure, carrier shown
> The read was the trail; it was the only trail there was.
"The read" is cashed out at L836 ("a click in a crystal, a human mage's face turning green"). Planned B11 self-deception.

**KEEP** | P3 | L77 | anchored
> A wheelwright was something else.
The inference she refuses (the doe carried it while alive, so did the people?) is in the same paragraph, and L255 says it outright.

**KEEP** | P1 | L211 | operational distinction
> a store is where things end up... I can hear how much of it is here, and that's all I can hear.
Concrete mechanism: a store collects a village's goods. The quantity-vs-origin distinction changes the scene's action.

**KEEP** | P1 | L225 | operational distinction
> How much is here, you've told me. Which way it went, you can't.
It splits what the mage has given from what is missing, and that sends Sylvanas to the lane.

**KEEP** | P1 | L331 / L620 | defined measure
> It's loud... The whole street is. / The whole cut's soaked in it.
"Loud" is the chapter's defined magical measure, calibrated against the bank, the prints and the hare.

**KEEP** | P1 | L826 | anchored shorthand
> It's not a knot, the way Millhaven was... A stain in a cloth that's been wet through.
Two staff placements back it, and it ends in a usable direction ("Down the road").

## fake-simplification-guide.md (7 keeps)

There are no explicit plain-speech setups. Disambiguation exchanges were audited as candidates.

**KEEP** | usable target | L532-538
> "Which is the north road?" ... The girl... pointed... at the back wall... "Past Pell's... Up the cow way."
A pointed direction plus a named route that Sylvanas walks at first light.

**KEEP** | usable target | L496-502
> "Ask her how she knows which way." / "The little window,"
Leads straight to a barred cellar light at dog's-nose height on the lane.

**KEEP** | usable trigger | L616-626
> "Can you tell her which marks are which?" / "Heavy. Light. Light. Heavy."
A per-mark field sign Cyndia can count inside her switch box.

**KEEP** | usable target | L165-169
> "Where's it worst?" / "Down there. And under us... a cellar under the inn."
The staff turned toward the bridge and mill, then the inn cellar trapdoor.

**KEEP** | honest limit | L159-161
> "Which is it?" / "I don't know."
A plain answer backed by the lag evidence. Nothing pretends to be simplified.

**KEEP** | usable target | L824-826
> "Well?" / "It's ahead of us, Ranger-General. Down the road."
The staff is turned to the willows, so the direction can be acted on.

**KEEP** | intentional (plan B9) | L758-762
> "What's it like down there? Who's still trading?" / "They had the market at the ford yesterday... Smoke in every chimney"
Concrete (the ford market, chimneys, barley price). It is meant to be real and useless to her, and her next line says so.
