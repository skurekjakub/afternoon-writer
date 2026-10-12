# Slop-Gate Scratchpad - chapter1 / pass a (iteration 2)

Target: v2-r2.md
Stage: standard

False-positive filter primed from `.afternoon/plans/chapter1.json`:
- POV: Sylvanas, absolute limited third, before her death. Her interior is dry, exact, and tactical. She is a tracker and Ranger-General, so she inventories by absence (casualties, damage, credentials) and sorts hypotheses (spy / envoy / both).
- Subject matter: the ward-stones hum, read, and draw on leylines. That is in-world mechanism, so stones that "read wrong" or "answer hollow" fall under the subject-matter defense.
- Intent: the plan locks a Kirin Tor expectation reversal at the storeroom ("expects a polished Kirin Tor problem ... finds instead a road-worn young mage"), a no-trust constraint, and a hard face-to-face close.
- Dialogue: Lor'themar is dry and courtly, Cyndia is flat and put-upon ("not ranked"), and Theris reports in fragments as trained.

## negation-addiction-hunting-guide.md (21 keeps)

**KEEP** | spatial-precision | condition 2
> the trees thinned to a gap no wider than a hay cart
A measurement idiom that fixes the gap's width, which the shot geometry depends on.

**KEEP** | hard-fact | condition 3
> Then he folded into the bracken and didn't get up.
The negation states the death. "folded into the bracken" alone does not establish that the troll is finished.

**KEEP** | hard-fact | condition 3
> Nobody had gone over the ridge to warn the rest of the warband.
A tactical conclusion from the count. Whether a survivor escaped decides whether the patrol has to pursue. No X-to-Y pivot.

**KEEP** | absence-inventory | condition 3
> No one carried. No one limped.
A casualty check. The absence is the information, and there is no replacement term.

**KEEP** | dialogue / binary | condition 1
> "Not all of them." / "The ones who don't are the ones who make it over the ridge."
A real disagreement about troll behavior that bears on whether escapees get over the ridge. This is a factual rebuttal, not a pivot.

**KEEP** | physical-detail | condition 2
> high gold windows that didn't open
A literal property of the room (sealed, stifling) that supports her claustrophobia memory. No pivot.

**KEEP** | inspection-result | condition 3
> Three weeks had changed nothing. Moss on the north faces. Runes clean. Nothing chipped, nothing leaning.
A ranger's checklist of defects she looked for and did not find. It sets up the later reversal (line 247: "Every one looks as it has for a hundred years"), so the intact look of the stones is a load-bearing plot fact.

**KEEP** | binary-diagnostic | condition 1
> No papers. No seal. No escort. Nothing on her that says who sent her.
Missing credentials are the evidence that separates envoy from trespasser, and both possibilities drive Sylvanas's decision. This is not a hallway to a Y noun.

**KEEP** | decision | condition 1
> No.
Sylvanas rejects the live option of sending the sergeant or Lor'themar south. She acts on it in the next breath ("Take the patrol north").

**KEEP** | decision | condition 1
> It didn't matter which.
She rules that the spy/envoy distinction does not change her action (going south herself), and the next line gives the reason. This is an active decision call, not decorative contrast.

**KEEP** | procedural imperative | Step 1
> Don't give them anything else. We don't have anything else. / "Tell them she said it. Not that it's true."
Orders to Lor'themar about what to report. The claim-versus-fact split is the plan's locked constraint (leylines stay an unverified claim).

**KEEP** | procedural imperative | Step 1
> Small sips at the streams. Nothing more till he's cool.
Horse-care instruction.

**KEEP** | binary-diagnostic chain | condition 1
> was no spy Sylvanas had ever heard of ... Envoys did not come over the rocks in the dark. Envoys did not come alone. ... None of the three told a Farstrider post that the leylines were wrong.
Live hypothesis elimination by a tactical POV. Each negation knocks out a candidate identity with observed evidence (scree, alone, talking about leylines). These are eliminations, not X-then-Y pivots. Watch item: four negations in five lines. They hold only because each one strikes a separate hypothesis.

**KEEP** | hard-constraint | condition 3
> She could not read a leyline.
A capability boundary that drives the plot. It is why she has to hear the mage out. The affirmative list comes first and the negation follows, so there is no reveal structure.

**KEEP** | binary-diagnostic / dialogue | condition 1
> She had two hundred yards on him, General, and she didn't run.
Fleeing versus staying are both real possibilities, and her choice is evidence about the prisoner's intent that Sylvanas is weighing.

**KEEP** | physical-precision | condition 2
> Reads like a cracked stone reads under your palms—only there's not a mark on it.
Liron's reading versus the stone's visible condition. The physical absence of a crack is the anomaly.

**KEEP** | physical-precision | condition 2
> an arrow laid across it but not nocked
Corrects the image: the ranger is ready but not drawn. The distinction changes the threat posture in the room.

**KEEP** | binary-diagnostic / intentional-structure | condition 1
> Every Kirin Tor she had met ... had worn that face. This one hadn't.
The expectation stated affirmatively is the envoy hypothesis from line 209, which Sylvanas is actively testing. The observation rules it out. The plan's arcPosition requires this reversal. Self-check: deleting it would lose a concrete POV-bias fact (what she expected Kirin Tor to look like).

**KEEP** | dialogue
> "She isn't what I expected."
Sylvanas's terse, withholding answer to Cyndia's "Well?". There is no Y half to cut. It echoes line 275, but it is spoken to Cyndia, who needs the information, so it is not a narration/dialogue pivot leak.

**KEEP** | binary-diagnostic | condition 1
> Waiting was no better than letting her go. It only looked more careful.
Release and wait-for-a-magister are both options laid out in the paragraph before. Her ruling decides the action ("Which left going in herself"). The deletion test fails because the second sentence cannot stand alone. Note for pass B: the aphoristic second sentence may be a narrator-wisdom candidate there.

**KEEP** | hard-constraint | condition 3
> She had no reason to trust a word the woman said. She would have to go and find one.
The plan locks the no-trust state. The deletion test fails because "find one" needs its antecedent. The line motivates the walk into the light.

## intent-smear-agency-laundering-guide.md (22 keeps)

Second P5/P6 sweep is documented in the notes JSON (`secondSweepP5P6`). Keeps:

**KEEP** | literal | condition 3
> The woods had gone quiet around something large deciding whether to run.
The woods went quiet (birdsong stopped) as literal sound. "something large deciding" is the troll, an animate agent.

**KEEP** | POV physical sensation | condition 2
> until the old ache settled back into the joint ... It had never entirely left.
The ache is a physical sensation located in the joint it describes. No command, judgment, or deception. This is not the "abstract state settling into a body part" case, because the ache is the body. Tool: contact_settled (13), unmapped, audited here.

**KEEP** | literal contact | condition 3
> where a thrown axe had kissed her on its way into a birch
The axe is the literal agent of the contact, and "kissed" encodes a light graze. No intention, desire, or cognition moves from a person to the axe, and no actor is demoted (the troll thrower is legible in "thrown"). Borderline: this is a wry contact metaphor, not laundering.

**KEEP** | collective actor | condition 1
> within ten breaths the woods had gone back to their business
The birds (thrush, second bird, third) are established in the sentence before and are the ones doing the "business." This is analogous to "the camp moved on."

**KEEP** | literal
> The light through the leaves had deepened from white to amber.
Physics of afternoon light.

**KEEP** | collective actor | condition 1
> A groan went along the patrol.
Sound travelling down a file of established people. They are the ones groaning.

**KEEP** | subject-matter | condition 3
> the ward-stones hummed under all of it ... a faint pressure just below hearing that came up through the mare's hooves and into her spine
The wards' hum is the chapter's defined in-world mechanism.

**KEEP** | no agency transfer
> Three weeks had changed nothing.
Time as the measure of an unchanged state. No human intention, command, or cognition verb, and no hidden actor.

**KEEP** | literal / agent adjacent
> Their reports came up every ten days without fail
Dispatches literally carried up the chain. The post's commander is named in the clause just before ("Cyndia never did"), so the actor stays legible.

**KEEP** | involuntary body response | P8 exception
> Her breastbone went cold.
An involuntary physical shock. The involuntariness is the point.

**KEEP** | collective actor / dialogue | condition 1
> The Convocation will want to have known first. / The Convocation always wants to have known first. Then it wants us to handle her.
A deliberative assembly of people who literally want and vote. Its members (Saltheril, the treasury magister, the pearl-necklace woman) are on the page at lines 43 and 63. Spoken political register.

**KEEP** | literal geography
> North of it the road ran broad and soft ... ground to pale dust by a century of supply carts. South it narrowed ... climbing steep and straight toward the Pass.
Standard "the road led" geography verbs. The real agent of the dust, the supply carts, is named.

**KEEP** | literal | condition 3
> The honey smell went out of the air. Resin and stone dust replaced it, and under both a cold mineral bite pouring down off the peaks ahead.
Smells changing with altitude and the source (the peaks) is named. Atmospheric-inversion judgment belongs to pass B.

**KEEP** | physics | condition 3
> It pushed at Sylvanas's left side until she was leaning into it.
Wind pushing.

**KEEP** | subject-matter | condition 3
> The hum in her back teeth stopped being a hum and became a pulse ... until it beat through the saddle.
Ward mechanism felt as stone density increases.

**KEEP** | literal mechanism | condition 3
> A ranger on the wall shouted down into the yard, and the gate began to swing.
Gates swing. The shouting ranger is named as the cause, and the hands on the gate are out of POV sight.

**KEEP** | subject-matter | condition 3
> He says it reads wrong ... Like knocking on a cask you know is full and hearing it answer hollow.
Ward-reading is the in-world mechanism. The cask is inside a dialogue simile with "you" as the actor.

**KEEP** | involuntary body response | P8 exception
> The muscles at the base of her skull drew tight, and she went very still.
Involuntary tension, and the character is the subject of the second clause.

**KEEP** | literal containment | condition 3
> It kept the post's salt pork and flour and lamp oil, and the stone held the mountain's chill.
Room-as-container and stone thermal mass. No cognition or intention verb.

**KEEP** | involuntary body response | P8 exception
> Her own heartbeat thudded loud over the whine of wind through the slit.
Involuntary.

**KEEP** | involuntary, then volitional reversal | P8 exception
> Her face went hot. ... Her jaw locked, and her fingers tightened on the bow grip until the wrapping creaked. She made herself unclench them one at a time.
The next sentence makes the involuntariness the point ("She made herself unclench them"). The body-part subjects mark the loss of control she then overrides.

**KEEP** | agent explicit
> The ward-light slid up over the toes of her boots as she crossed into the circle. / Cold came up off the flagstones and into her shins. / and let the silence run.
The mover is named in the same clause ("as she crossed"), cold off stone is physics, and "let the silence run" has Sylvanas as the explicit agent, as in "The silence held because she let it."

Non-candidates checked (person or animal subjects): "Trolls always ran as though the ground owed them money" (the subject is trolls, and the ground sits inside a simile), "The mare settled into the long, rolling walk" (contact_settled at 57, animal), "found his hand still wrapped in the reins" (contact_found at 111, person), "Sylvanas found the first ring on the map" (contact_found at 237, person), "The mare had been waiting all afternoon for permission" (animal), "Dalaran had them" / "Dalaran kept those by the dozen" (polity possession, no intent verb).

## recurring-prose-tics.md (12 keeps)

**KEEP** | tic1 | within cap (1/1)
> That got a twitch at one corner of his mouth, there and gone before she'd properly seen it.
The only corner-of-mouth beat in the chapter. Lor'themar's suppressed amusement at "paint a mage on his map" is specific to him.

**KEEP** | tic3-tightened | physical (1/3)
> her fingers tightened on the bow grip until the wrapping creaked
A physical grip with an audible result.

**KEEP** | tic3-eased | physical (2/2)
> eased back when the trail began to climb / the ranger at the door eased it to
Riding pace and a door. Both physical.

**KEEP** | tic5 | character-specific (gaze 1 of 4 kept)
> because Lor'themar was watching her do it
His scrutiny is the pressure behind her pretext of checking stones she already signed off. It is specific to their dynamic.

**KEEP** | tic5 | character-specific (gaze 2 of 4 kept)
> She faced the doorway with the look Sylvanas had seen on rangers ordered to stand down from a fight they knew they could win.
A military-specific comparison filtered through Sylvanas's experience.

**KEEP** | tic5 | character-specific (gaze 3 of 4 kept)
> She took in Sylvanas once, fast—the bow, the road-grey leathers.
Names what was looked at. It is an assessment, not a generic stare.

**KEEP** | tic5 | character-specific (gaze 4 of 4 kept)
> she kept them on Sylvanas, though the staff and the open door were both a turn of the head away
A tactical read: Sylvanas notes that the prisoner is not checking escape routes or her staff. This is the strongest gaze beat on the page, so the kill went to line 327 instead.

**KEEP** | tool: filter_decided (1/3)
> Sylvanas had two fingers on the bowstring before she had decided to reach for it.
The filter word does real work. Reflex runs ahead of decision, and that is the meaning of the sentence.

**KEEP** | tool: filler_nodded (1/4)
> He waited a moment longer, then nodded once and turned the gelding north.
The nod is Lor'themar's assent to "I'll leave her whatever's useful," and it closes their parting. It does a job, and it is under cap.

**KEEP** | tool: filler_frowned (1/4)
> He frowned, hunting for the report word and not finding it.
Specific: a junior ranger reaching for drilled report vocabulary. Under cap.

**KEEP** | tool: simile_overload (7 hits, all under caps: like 3/12, as if 2/5, as though 2/3)
> Trolls always ran as though the ground owed them money. (7) / scowled at it as though it had insulted her family (19) / he went on as if she had (63) / as if this were what he'd intended all along (91) / Reads like a cracked stone ... / reads like the trouble's inside it (247, dialogue, subject-matter) / cut like a ship's officer's coat (277, a literal tailoring comparison that plants the Kul Tiran clue)
Watch item: the two wry "as though" similes on page 1 (7, 19) share a comic shape. Two is under cap.

**KEEP** | tool: participial_attachment + punctuation_tics (under caps)
> participial_trailing at 111, 173, 181, 189, 193, 199, 227, 315, 323 (281 is folded into kill A-IS-1, and its fix keeps the participial) / punct_semicolon 9/12 at 19, 141, 201, 203, 207, 277, 283, 299x2 / punct_colon_narration 6/6 at 25, 43, 95, 257, 275, 309
All under or at cap. The participials are needed, because texture participial_pct is 5.8% against a 12% target. The semicolons and colons are list or clause joins. The colon count is at its 6/6 cap: do not add another colon in revision.

Observation outside the listed tics: the "held out X without looking" handoff gesture appears twice (225 with the mare's reins, 323 with the bow). It is not a guide tic and not flagged, but the slophunter should not add a third.
