# Continuity fix decisions — The Plague Road

Source findings: `research/input-audit/continuity.md` (B = BREAKS, V = VISIBLE, M = MINOR) and `research/input-audit/plans-vs-outlines.md`.
Canonical files: `.afternoon/outlines/chapterN.md`. They win over the plan files, and over the character and location files unless a decision below says otherwise.

## Editing rules (all agents)

- Edit only what a decision requires. Keep every other line word for word.
- Write in the outline register of the surrounding bullets: plain declarative sentences, one event per sentence.
- No similes. No "rather than", "not X but Y" or "stops being X and becomes Y". No counting devices. No "she let it".
- Where a decision changes a fact, update every line in your assigned files that states the old fact, including the "They do not know", "Do not" and carry-forward bullets.
- Record every change in your log file: file, line, before, after, and the decision code.

---

## 1. Mal'Ganis thread (pivotal)

### Principle

Mal'Ganis appears five times before Ch25. Each time he wears a different ordinary disguise that suits a place the plague is hitting. He is not a trader by trade. Each sighting has four layers:

1. **First read:** an ordinary, useful local, forgettable.
2. **Observation:** a concrete beat where he looks at the affected place or people. On a first read it is idle. On a second read it is a man checking that his work is going to plan.
3. **Covert contact with Cult of the Damned personnel.** On a first read it is small talk or routine business. On a second read it is a report taken or an order given. Each contact is with someone the outlines identify as cult, or who is clearly part of the cult's machinery elsewhere.
4. **The farewell**, "May the stars keep your road", spoken from habit. It is his unconscious tell (an ancient Kaldorei phrase, per `characters/malganis.md`).

Nobody unmasks him before Ch25. The outlines may add a short "Second read:" note to each sighting so the writer knows what to plant. The prose must not explain it.

### The five sightings

| Ch | Place | Disguise | Observation | Covert contact | Farewell heard by |
|---|---|---|---|---|---|
| 3 | The Millhaven road | An old carter with an empty wagon | He looks back down the road toward Millhaven while they talk. | As local gossip, he asks whether they passed "the young grain-man" on the road. The survivor girl mentioned a newer grain seller, who is the cult's distributor. On a second read he is checking on his agent, and he learns from the party what the survivor told them. | Sylvanas |
| 6 | The road just outside Andorhal | A granary tally-man walking out of the city with a ledger satchel | He has just come from Andorhal, where the sickness is spreading. He glances back at the granary roofs. | His directions into Andorhal send the party to Havel's post. Havel is cult-paid (Ch7–8). On a second read, he routes them to his own man. | Sylvanas |
| 9 | The edge of the Ch9 fight, during the retreat | A robed figure among the fleeing cultists who does not run | He stands at the edge of the fight like an overseer before he turns and walks away. | The courier Cyndia kills had just come from him. The torn dispatch, tying cult watchers to Hearthglen and Arthas's troop movement, is his order. The dying courier does NOT say the farewell. | Cyndia (per `characters/cyndia.md`) |
| 15 | Arthas's war camp at Hearthglen | A quartermaster's aide | He watches the column form up for Stratholme. | He hands a sealed manifest to a carter "for the Stratholme granaries". On a second read, he is dispatching grain and orders into the city before the army arrives. | Cyndia hears it clearly (existing beat) |
| 17 | Stratholme's service lane | A carter with an empty wagon, leaving | He looks back at the wall as he goes. | He gives the trio the wall route. In the same lane, a sick-looking acolyte moves off on his nod. On a second read, he is pulling his people out before the Culling, and he steers the trio to a place where they will witness it. | Sylvanas and Jaina |

### Required changes

- **Ch3:** rewrite the sighting to match the table. Rename "old grain seller" to "old carter" throughout Ch3.
- **Ch6:** the disguise becomes the tally-man, and his directions lead to Havel's post. Read Ch7 first to name the right post or gate.
- **Ch9 (B3):**
  - Remove the dying courier's farewell at `ch9.md:124`.
  - Rewrite `ch9.md:75` to name the retreating figure as the sighting.
  - Add the retreating-figure beat.
  - Keep the courier's death and the dispatch.
- **Ch15:** add the observation and the manifest handoff to the existing aide sighting.
- **Ch17:** add the observation and the acolyte's nod to the existing carter sighting.
- **Ch25 (V11):**
  - Rewrite `ch25.md:141` to name the five sightings as above: the old carter on the Millhaven road, the tally-man walking out of Andorhal, the figure who walked away from the Ch9 fight, the aide in Arthas's camp, and the carter in Stratholme's service lane.
  - Add one bullet: in the recognition, Sylvanas re-sees each covert contact. These are the question about the grain-man, the directions to Havel, the courier's dispatch, the manifest and the nod in the lane. Seeing them, she understands that he was running the cult and watching his work.
- **Clue name in every other chapter:** replace "old seller", "old grain seller" and "old seller / repeated-farewell clue" with "the old carter" and "the repeated-farewell clue". Keep "newer grain-man", which is the cult distributor and a separate person.
- **`characters/malganis.md`:** replace the sightings list with the five sightings: Ch3 old carter, Ch6 tally-man, Ch9 retreating figure, Ch15 quartermaster's aide, Ch17 service-lane carter. Add one line per sighting for his covert contact.
- **`plans/story-arc.md:48`:** make it read that Mal'Ganis sanitizes sites, steers Arthas, watches his work in disguise and directs the cult covertly, and hides behind a repeated road-farewell.

---

## 2. BREAKS

### B1. Arthas reaches Capital City first

- **Ch21:** Arthas burned most of his fleet but kept his own ship in a separate cove. Add one bullet saying so where the bay is described (`ch21.md:86`).
- **Ch22:**
  - The pair sail first on the Wolfheart.
  - Pack ice drives them south, and the crossing costs them days. Replace "faster because the source no longer bothers to oppose them" (`ch22.md:157`).
  - They land at Southshore (M22 is solved by this), buy horses there, and ride north on the King's Road. Rename the "Road South" scene to "The Road North".
  - Arthas sails later, straight for Lordaeron's coast, with a crew that does not rest.
  - At Daggercap Bay, the pair find his ship gone from its cove. Antonidas confirms that Arthas is in Capital City only after they land at Southshore (move `ch22.md:150`).
  - Keep "four days" (`ch22.md:39`).

### B2. "Three weeks ahead"

Arthas is a few days ahead.
- Change `ch20.md:199` and `ch20.md:42` to say days.
- Change `ch21.md:16`, "passed through Daggercap Bay weeks ago", to say days ago.
- Keep `ch21.md:143` and `ch21.md:165`.

### B3

Solved in section 1.

---

## 3. VISIBLE

### V1. Ch11 and Ch12 spans

Ch12's conversation runs across several days of sittings. Jaina is a held guest in Scholomance, and the sittings break for sleep and meals.
- Make `ch12.md` say so at the opening.
- Change `ch14.md:89` from "hours underground" to "days underground".

### V2. How Sylvanas learns Jaina went dark

- **Ch9 split:** a Farstrider runner from Lor'themar's relay stays on the Darrowmere shore as a lake watch.
- **Ch10:** Jaina leaves her horse with the watch before she takes Jandice's boat. M14 is solved by this.
- **Ch11:** the watch rides south and reports that Jaina crossed to Caer Darrow and did not come back (`ch11.md:162-165`).
- **Ch13/14:** her horse is waiting with the watch when they come out.

### V3. Arthas "already moving"

- `ch13.md:170` and `ch14.md:160, 196`: Arthas is breaking camp at Hearthglen to march on Stratholme.
- `ch15` is unchanged.

### V4. Recall twice

- **Ch14:** the relay brings Lor'themar's private warning that the Convocation is moving toward a recall. Sylvanas does not answer and does not slow down.
- `ch14.md:146` and `ch14.md:194`: "The Convocation recall was ignored" becomes "Lor'themar's warning was ignored".
- **Ch19:** keep it as the first formal recall and the first refusal.

### V5. POV swap

Keep the outlines. Update `plans/story-arc.md:5` to declare Ch23 (Jaina) and Ch24 (Sylvanas) as exceptions alongside Ch22 and Ch25.

### V6. Stratholme

Update `locations/lordaeron-and-northrend.md`:
- They arrive early, work inside the city, and witness the opening choice at the main gate (match Ch15–17).
- Arthas approaches by the east road from Hearthglen.
- In `ch16.md:5`, change "North road" to "East road".

### V7. Millhaven's dead

- Add a dispatch beat in **Ch9** (near `ch9.md:139`): the column of dead reached the outer ward at the Thalassian border and burned on the runestones.
- Silvermoon reads it as proof that the wards hold, which feeds its complacency (story-arc 46–47).
- In **Ch19** at `ch19.md:117`, the isolationists cite it: the dead broke on the wards, so this was never their war.

### V8. Warnings from Northrend

- **Ch22 at Daggercap Bay:** remove the Farstrider signalling and the carrier pigeons (`ch22.md:151-153`).
- The Antonidas stone was dead in Northrend (`ch20.md:92, 107`) and wakes once the ship is clear of the ice. Jaina calls Antonidas from the ship.
- Sylvanas sends Farstrider warnings through the mainland relay after landing at Southshore.
- Remove "one last time" (M23).
- Add one line in Ch20 or Ch22 saying the stone is dead near the source and wakes away from it.

### V9. Arrows

- **Ch23:** Sylvanas knows from Ch21 that an arrow will not kill him. She shoots anyway, at his sword arm, to pull his attention off Terenas. It gives away her position, and she chooses that (`ch23.md:129-130`).
- **`characters/arthas.md:35`:** move "first arrow should kill him and does not" to Ch21.

### V10. Tribunal timing

- `ch24.md:4`: it opens days after the arrest, once Vereesa can ride from Silvermoon and Lor'themar's force can arrive.
- `ch24.md:165`, "all day", refers to the trial day itself.
- `ch25.md:4` is unchanged.

### V11

Solved in section 1.

---

## 4. MINOR

### Knowledge and setup gaps

- **M1:** `ch5.md:113` becomes "a cold necromantic trace Jaina has not met before". Do not refer to earlier witnesses.
- **M2:** add one bullet near the end of **Ch5** where Sylvanas warns Jaina what the army will do. Read `ch6.md:47` and `ch6.md:102` first, and make the warning match what Ch6 says came true.
- **M3:** `ch7.md:85`: the cover paperwork is a Farstrider pass that Sylvanas writes for her under her own seal.
- **M4:** `ch10.md:85`: Jaina bluffs a Kirin Tor authority she does not hold.
- **M5 (Ch2):**
  - Jaina carries a paired sending stone she has kept silent, so Antonidas cannot order her home.
  - When her tools are confiscated, the stone is returned with her staff (`ch2.md:88`, `ch2.md:115`).
  - Keep `ch2.md:20` and `ch2.md:94`.
- **M6 (Ch14):** remove the voice-relay stone (`ch14.md:70`, `ch14.md:149`). Lor'themar's warning arrives by runner, in his handwriting.
- **M7:** `ch23.md:37` and `ch23.md:207`: replace "Ner'zhul" with "something in the far north they cannot name".
- **M9:** read `ch18.md:93`. Either add one line in Ch6 (near `ch6.md:115`) naming the Alterac ruling as a past Jaina/Arthas disagreement with the content Ch18 implies, or cut the callback. Prefer adding the setup.

### M8 and M10: the grimoire and Kel'Thuzad's journals

- **Ch13:** Jaina carries out the stolen grimoire and a bundle of Kel'Thuzad's journals.
- **Ch14:** she briefs them. One journal describes the Nathrezim, demons who wear borrowed faces. Keep it brief. It sets up Ch25 without solving anything.
- **Ch23/24:** the guards seize both at the arrest. The tribunal uses a necromancer's grimoire in their kit as evidence against them.
- **Ch25:79:** the "Nathrezim thread" is now set up. Leave it.

### Dropped objects and wounds

- **M11:**
  - **Ch12:** Kel'Thuzad says he felt her coming through Jandice's guest ward.
  - **Ch13:** Jaina burns the ward off before the escape.
- **M12:** **Ch13** window climb (`ch13.md:97`): the half-healed Ch9 wound pulls. Mention it once.
- **M13:** add Kel'Thuzad's expected return as a lich to Ch25's open threads.
- **M14:** solved by V2.

### Headcounts and kit

- **M15 (Ch3):**
  - `ch3.md:169`: "three remaining elves and Jaina".
  - `ch3.md:168`: "the two empty places in the horse line".
- **M16:** `ch19.md:26`: three horses.
- **M17:**
  - `ch19.md:83`: the escort comes from Lor'themar's forward mobilization.
  - `ch20.md:7`: the three rangers come from that escort.
- **M18:**
  - **Ch23:** the ranger who stays near the pair slips away when the guards come and carries word to Cyndia.
  - **Ch21:** Sylvanas's main bow cracks in the ice fight.
  - **Ch22:** she takes a short recurve from the Wolfheart's stores. This sets up `ch23.md:166`.

### Timeline and travel

- **M19:** `ch16.md:87`: the dust behind them is Arthas's mounted vanguard. The infantry follow later.
- **M20:** `ch18.md:175`: replace "open water somewhere ahead" with a plain dusk detail that fits a southbound road.
- **M21:** `ch24.md:123`: "Months" becomes "Weeks".
- **M22:** solved by B1.
- **M23:** solved by V8.
- **M24:** `ch20.md:180`: add the burned ship ribs frozen into the harbor ice to the landfall list.

### Character-file contradictions

- **M25:** `ch11.md:68`: Cyndia covers the left flank.
- **M26:** `ch1.md:94`: "Sylvanas doubts even Cyndia expects a real threat from the south."
- **M27:** update `characters/antonidas.md`'s stone progression to the outlines' actual contacts. Check Ch2, Ch9, Ch14, Ch20 and Ch22. He arrives in person in Ch22.
- **M28:** update `characters/lorthemar.md`'s appearances to the outlines: runners from Ch9, the warning in Ch14, the mobilization in Ch19, the 300 at the tribunal in Ch24.
- **M29:** the tribunal beats for `characters/uther.md`, `vereesa.md` and `antonidas.md` move to Ch24.
- **M30 (Ch21):** keep canon.
  - Before the claiming, Muradin warns Arthas off the blade.
  - The ice-shard blowback strikes Muradin down, and Arthas walks on without looking back.
  - The pair carry Muradin out (existing beat).
  - Make `characters/muradin.md` and `characters/arthas.md` match.
- **M31:** `characters/antonidas.md:17`: Antonidas trained Kel'Thuzad.

### Lore, geography, premise and references

- **M32:** `locations/lordaeron-and-northrend.md`: Hearthglen is on the page in Ch15.
- **M33:**
  - `.afternoon/overview.md`: the premise opens on a troll sweep, and Cyndia's border post catches Jaina inside the first ward.
  - `plans/story-arc.md:9`: "Sylvanas's border post catches Jaina".
- **M34 links:**
  - `plans/plague-process.md` becomes `plans/plague-mechanism.md` (Ch2, Ch3, Ch12).
  - `locations/stratholme.md` becomes `locations/lordaeron-and-northrend.md` (Ch16, Ch17, Ch18).
- **M34 compass:** align with Warcraft canon.
  - Caer Darrow lies east of Andorhal across Darrowmere (`ch8.md:155`, `ch9.md:5`).
  - Hearthglen lies northwest of the Eastweald (`ch11.md:5`).
  - The road from Hearthglen to Stratholme runs east (V6).
  - Leave Strahnbrad.
- **M34 window:** `ch23.md:125`: "octagonal dome" becomes "octagonal window".

### Plans

- **`plans/plague-mechanism.md`:** the outlines still link it. Where it conflicts with `ch18.md:165` ("Grain is … an amplifier"), change the plan file to match the outline. Do not change other plan files.
