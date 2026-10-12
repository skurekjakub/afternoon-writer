# The Plague Road: Continuity and Internal-Consistency Audit (pipeline inputs)

Scope: `.afternoon/outlines/chapter1.md` to `chapter25.md` (canonical), `stories/the-plague-road/plans/story-arc.md`, `stories/the-plague-road/characters/*.md` and `characters/voice-sheets/*` (facts only), `stories/the-plague-road/locations/*.md`, `.afternoon/overview.md`. This audit does not cover `plans/chapters/` or the other plan files. Every input file was left unchanged.

Citation key:
- `chN.md:L` means `.afternoon/outlines/chapterN.md`, line L.
- `arc:L` means `stories/the-plague-road/plans/story-arc.md`.
- `loc-lordaeron:L`, `loc-silvermoon:L` and `loc-scholo:L` mean the files in `stories/the-plague-road/locations/`.
- `char-<name>:L` means `stories/the-plague-road/characters/<name>.md`.
- `overview:L` means `.afternoon/overview.md`.

Severity:
- **BREAKS**: the story does not work as written.
- **VISIBLE**: a reader would notice.
- **MINOR**: a small slip, or a gap the pipeline should know about.

Counts: **BREAKS 3**, **VISIBLE 11**, **MINOR 34**. Total 48.

---

## BREAKS

### B1. Arthas reaches Capital City before the pair, although they left him behind in the cave
- ch21.md:195: "Arthas, behind them in the cavern with Frostmourne"
- ch21.md:86: "Arthas burned most of his own fleet after landing"
- ch22.md:4: "Opens hours after Chapter 21's retreat from the Frostmourne cavern"
- ch22.md:150, while the pair are still at Daggercap Bay: "They send everything they can by bird, stone, and relay. It still fails in practice. Antonidas confirms the one fact that matters most: Arthas is already in Capital City."
- ch22.md:157: "The return crossing is faster because the source no longer bothers to oppose them directly"
- ch22.md:39: "Arthas has been in Capital City for four days before the formation reaches the walls."
- loc-lordaeron:91: Daggercap Bay is "the last exit point that still exists". loc-lordaeron:93: "S&J keep a retreat Arthas destroyed."

The pair leave Arthas in the cavern and walk out first. They take the only intact ship and sail immediately, and Jaina drives that ship faster than the northbound voyage. Yet by the time they reach the bay, Arthas is already in Capital City, and he has been in the palace four days when they reach the walls. No outline gives him a route, a ship or a mode of travel that could do this. The whole endgame hangs on the line "he got home first."

### B2. Arthas is "three weeks ahead", and the pair still reach the cave while he is claiming the blade
- ch18.md:172: the relay arrives at dusk on the day of the Culling: "Arthas is not riding home. He is taking ships north."
- ch19.md:4: "One day after Chapter 18." Ch19 ends riding to the coast. ch20.md:182: "after four days of deck motion".
- ch20.md:199: "Arthas is already inland and practically three weeks ahead." See also ch20.md:42 and ch21.md:16: "Arthas passed through Daggercap Bay weeks ago".
- ch21.md:143: "the race becomes measured in hours and half-days"
- ch21.md:165: "Inside the main chamber, the target is already transformed. Arthas stands with Frostmourne in hand, surrounded by soldiers who look alive at first glance and wrong at second."
- loc-lordaeron:113: "Arthas's selected men already look half-lost by the time S&J reach the chamber."

By the stated dates, Arthas can be at most a few days ahead. He was at Stratholme on the day of the Culling, and the pair sail roughly two or three days later. "Three weeks" is impossible. It also contradicts the next chapter, where the pair catch Arthas in the chamber with his men still mid-transformation. A three-week lead and a same-scene confrontation cannot both hold.

### B3. A face in Mal'Ganis's five-face trail belongs to a courier who dies on-page
- ch9.md:124: "Cyndia kills a fleeing courier and gets a torn dispatch ... The dying courier uses the same farewell phrase again"
- ch9.md:75: "A dying courier can repeat it, but it must stay weak and unresolved."
- ch25.md:141: "The grain trader and the Andorhal contact and the retreating figure and the military aide and the Stratholme-road merchant all resolve into the same enemy"
- char-malganis:24: "Ch 9: retreating figure." char-cyndia:24: "Ch 9: hears the odd road-blessing from the retreating figure."
- char-malganis:19: the farewell is "an ancient Kaldorei fossil he no longer notices he is using."

The tell only works as a hunting tool if the phrase belongs to one being. In Ch9, a courier who is killed on-page says it. There are two readings, and both break the Ch25 payoff. In the first, the courier was a cultist who happened to use the phrase, so the tell is not unique. In the second, the courier was Mal'Ganis, and he is shown dying. Ch25 recovers by renaming him "the retreating figure", a figure that no outline contains. The character files also describe a retreating figure, not a man killed by Cyndia.

---

## VISIBLE

### V1. Chapters 11 and 12 are declared simultaneous, but their spans cannot match
- ch11.md:4: "Runs parallel to Chapter 12. While Jaina is already inside Scholomance after Chapter 10's descent, Sylvanas and Cyndia ride south from the Chapter 9 split to brief Arthas, then turn north again when Jaina's trail goes dark."
- ch12.md:4: "Runs parallel to Chapter 11. It opens after Jaina's descent at the end of Chapter 10 and ends when Sylvanas's approach reaches the deep levels of Scholomance."
- ch12.md:6: "seated in the sanctum at chapter start." Ch12 is one continuous conversation.
- ch14.md:89: "the world outside Caer Darrow feels too ordinary after hours underground"

In Ch11, Sylvanas rides hard south, gets through the camp machinery, briefs Arthas, watches the march leave, receives a dispatch, and rides hard north to Caer Darrow. Ch12 is a single seated conversation that Ch14 measures in hours. Either the Ch12 conversation lasts days, or the Ch11 rides take hours. The outlines specify neither.

### V2. Sylvanas learns that Jaina has gone dark, but no channel carries the news
- ch11.md:162: "Then Jaina's line goes silent, and politics loses the argument."
- ch11.md:165: "Sylvanas gets word that Jaina entered Caer Darrow and never came back out."
- ch10.md:7: "Characters: Jaina alone." Jaina's only channel is the Antonidas stone (ch10.md:151), and Sylvanas has no stone.
- ch12.md:28: Jaina herself does not know "Whether Sylvanas is still far south or already turning north."

No outline establishes a line between Jaina and Sylvanas, and nobody watches the lake who could report back. Sylvanas acts on information with no source.

### V3. Arthas is "already moving toward Stratholme", yet Ch15 finds him camped at Hearthglen
- ch13.md:170: "Hearthglen is breaking, and Arthas is moving toward Stratholme."
- ch14.md:160: "Arthas is already moving toward Stratholme." Repeated at ch14.md:196.
- ch15.md:5: "South road into Hearthglen and Arthas's war camp."
- ch15.md:138: "He marches the main column at once." He only marches after the briefing. ch15.md:38: "marches his main force on Stratholme at once."

Two relays say Arthas has left for Stratholme. In the next chapter he is still in his war tent at Hearthglen and decides to march only after the pair brief him.

### V4. Sylvanas refuses the recall twice, and the arc's "hardest turn" lands first in Ch14
- ch14.md:146: "The next Farstrider relay is not field news. It is a formal recall. Lor'themar delivers the Convocation's order, and Sylvanas refuses it by not answering and not slowing down."
- ch14.md:194: "The Convocation recall was ignored"
- ch19.md:37: "Sylvanas refuses the Convocation's recall"
- char-sylvanas:40: "Ch 19: she refuses recall for the first time in her life."
- arc:32: "Hardest turn: she defies the recall and chooses the mission anyway."

Ch19 is built as the moment Sylvanas first breaks with the Convocation, but she already ignored a formal recall in Ch14.

### V5. The POV order in Chapters 23 and 24 breaks the story-arc rule
- arc:5: "POV: Sylvanas odd chapters, Jaina even chapters, with dual exceptions in Ch 22 and Ch 25."
- ch23.md:3: "**POV:** Jaina Proudmoore". Ch23 is odd-numbered.
- ch24.md:3: "**POV:** Sylvanas Windrunner". Ch24 is even-numbered.

The outlines swap the two chapters' POVs with no exception declared. The arc's own exceptions are Ch22 and Ch25 only.

### V6. Stratholme on the page contradicts the location file
- loc-lordaeron:45: "S&J do not witness the opening choice. They arrive too late and watch the last part from above after slipping in through the service side."
- ch15.md:138: "Jaina, Sylvanas, and Cyndia can ride ahead and try the granaries". In Ch16 they work inside the city before Arthas arrives (ch16.md:108).
- ch17.md:4: "Opens the moment after Jaina answers Arthas honestly". At ch17.md:88-95, Arthas gives the Culling order in front of them, and Uther and Jaina refuse it.
- Sub-note: loc-lordaeron:40 says "Main southern gate: formal military approach". In the outlines, Arthas follows the pair down the "North road into Stratholme" (ch16.md:5) and arrives at "Stratholme's main gate" (ch17.md:5).

The outlines have the pair arrive early and witness the opening choice at the gate. The location file says the opposite on both counts.

### V7. Millhaven's sixty dead march on Quel'Thalas, and nothing ever comes of it
- ch3.md:130: "At least sixty reanimated bodies moved north-northeast toward the Quel'Thalas border in rough formation. The threat is immediately upgraded to a direct border warning."
- ch3.md:144: Neral carries the warning north. The last mention is ch4.md:16.

Later dispatches report only on politics and erased evidence (ch9.md:139, ch11.md:158). The Convocation's isolationists even argue that "this was never their war" (ch19.md:117). No outline says whether the column reached the wards, was destroyed, or vanished.

### V8. The pair send warnings from Northrend by relay and birds after the relay network has ended
- ch19.md:41: "The relay network dies at the coast. Everything beyond that is competence, borrowed passage, and whatever Jaina can track through resonance."
- ch20.md:19: "The relay network dies at the harbor. Once they sail, no institution is carrying them."
- ch22.md:151, at Daggercap Bay: "Sylvanas launches the warning through military shorthand and Farstrider signaling while Jaina reopens the Antonidas line"
- ch22.md:153: "carrier pigeons flinging themselves south over frozen water"

No outline sets up the birds, and the Farstrider relay was said to stop at the Lordaeron coast.

### V9. Sylvanas learns twice that arrows do not kill the Frostmourne bearer
- ch21.md:173: "Sylvanas's best opening arrow proves ordinary lethal standards no longer apply". ch21.md:175: "first arrow clattering on ice after Arthas pulls it out"
- ch23.md:129: "Sylvanas's first perfect arrow proves that ordinary killing does not hold here anymore."
- ch23.md:130: "Sylvanas's throat shot fails and gives away their position at once."

In Ch23, Sylvanas gives up concealment for a shot she already knows from Ch21 will fail, and the outline frames the result as a new discovery. char-arthas:35 also places this beat in Ch23 ("first arrow should kill him and does not") without accounting for Ch21.

### V10. The tribunal witnesses arrive faster than the outlines allow
- ch24.md:4: "Opens hours after Chapter 23's arrest and closes after the verdict"
- ch24.md:165: "the ruling the system has been building toward all day"
- ch24.md:39: "Vereesa delivers the Convocation's disavowal in person". ch19.md:155: Vereesa rode home to Silvermoon.
- ch24.md:41: "Lor'themar arrives with three hundred Farstriders and mages"
- ch25.md:4: "Opens the night after Chapter 24's verdict"

The Convocation would have to hear of a regicide, deliberate, and send Vereesa from Silvermoon. Lor'themar's force would have to arrive in the same window. The outlines never put days between the arrest and the trial. As written, the chapter reads as hours.

### V11. Ch25's list of the five faces does not match the five sightings in the outlines

| Sighting in the outlines | What Ch25 calls it (ch25.md:141) |
| --- | --- |
| Ch3, ch3.md:151: "An old grain seller comes up the road pulling an empty wagon" | "The grain trader"? |
| Ch6, ch6.md:137: "a grain trader", met on the road before the city, giving directions into Andorhal | "the Andorhal contact"? No farewell sighting happens in Andorhal itself (Ch7-8). Readers may take "Andorhal contact" to mean Havel or Corin. |
| Ch9, ch9.md:124: a "fleeing courier" whom Cyndia kills | "the retreating figure" (see B3) |
| Ch15, ch15.md:145: "an ordinary aide" | "the military aide" (matches) |
| Ch17, ch17.md:117: "A grain carter with an empty wagon", inside the city's service lane | "the Stratholme-road merchant". char-malganis:26 also has "refugee-road merchant". |

The recognition beat is the book's closing payoff. Its labels should point at scenes the reader actually saw.

---

## MINOR

### Knowledge and setup gaps
- **M1. Ch5's "other silenced witnesses" have no precedent.** ch5.md:113: "Jaina catches the same cold necromantic trace they found on other silenced witnesses." The only earlier silenced witness is the Ch4 initiate, who dies of swallowed poison (ch4.md:163: "he has already swallowed poison meant for capture"). He carries no necromantic trace. The first death-curse is in Ch8 (ch8.md:103).
- **M2. The outlines never show Sylvanas warning Jaina about the army.** ch6.md:102: "which is exactly what Sylvanas warned her it would do". ch6.md:47: "forcing her to accept Sylvanas was right about the army." Ch5 ends only with "They do not know whether Arthas will listen, help, or get in their way" (ch5.md:151).
- **M3. Jaina's cover paperwork has no source.** ch7.md:85: "The party approaches the gate on foot with Jaina's cover paperwork." Ch2 says "No credentials, no backing, no delegation" (ch2.md:95), and "Her map and tools are confiscated" (ch2.md:88). Only her staff is returned (ch2.md:115).
- **M4. Jaina claims Kirin Tor authority she does not have.** ch10.md:85: "She chooses the direct approach under Kirin Tor authority." Compare ch2.md:95 (no credentials) and ch10.md:152: "Jaina cannot count on rescue or sanction."
- **M5. The sending stone appears in Ch9 with no setup.** Its first appearance is ch9.md:74: "Antonidas: Off-page pressure reaching Jaina by sending stone." But ch2.md:94 says "Antonidas only has a note she left behind", and ch2.md:20 says "Antonidas does not know exactly where she is". No outline says she carries a stone, or why she did not use it.
- **M6. The Farstrider voice-relay stone appears late and conflicts with the runners.** ch14.md:70: Cyndia "carries the relay stone". ch14.md:149: "pale green crystal warming in Cyndia's hand, Lor'themar's clipped voice through the stone". Until then, Lor'themar reaches Sylvanas only by runner and handwriting (ch9.md:142: "Lor'themar's tight handwriting"; ch11.md:161). After Ch14 the relay is again riders and dispatch tubes (ch18.md:175).
- **M7. "Ner'zhul" is named with no setup.** ch23.md:37 and ch23.md:207: "tethered to Ner'zhul". Ch12 leaves the Lich King's origin unknown (ch12.md:170: "They do not know what created the Lich King"), and ch24.md:215 forbids "Any direct naming of the larger cosmic enemy." If the name reaches prose in Jaina's POV, it is a knowledge leak.
- **M8. The "Nathrezim thread" pays off something never set up.** ch25.md:79: "the Nathrezim thread active". No outline mentions Nathrezim, and no outline has anyone take Kel'Thuzad's journals (char-kelthuzad:36: "His journals on the Nathrezim are real treasure").
- **M9. The "Alterac ruling" first appears as a callback.** ch18.md:93: "The Alterac ruling now reads as a smaller version of the same gap". Ch6 shows the Jaina/Arthas history only in general terms (ch6.md:115).

### Objects and setups dropped
- **M10. The stolen grimoire disappears after Ch12.** ch10.md:41: "Jaina descends alone carrying a stolen grimoire of the Damned". ch12.md:89: "Kel'Thuzad notices the stolen grimoire at once without asking for it back." It is never mentioned again: not carried out in Ch13, not briefed in Ch14, not seized at the arrest.
- **M11. Jandice's tracking ward on Jaina is never paid off.** ch10.md:107: Jandice offers "a guest ward that lets the house taste and track her arcane signature". At ch10.md:111, "Jaina lets the ward mark her". It never comes up again, either removed or used.
- **M12. Sylvanas's serious Ch9 wound drops out.** ch9.md:117: "taking a serious wound". ch11.md:88: "her healing wound". After that it is unmentioned, including during the solo window climb in Ch13 (ch13.md:97).
- **M13. Kel'Thuzad's expected return as a lich has no in-book payoff.** ch14.md:131: "Kel'Thuzad expected to survive his own death as a lich." ch14.md:38 makes it part of Sylvanas's "full strategic picture". No outline acts on it.
- **M14. No outline says how Jaina's horse was recovered.** ch10.md:6 and ch10.md:88: Jaina rides "a Thalassian horse" to the Barov manor, then takes Jandice's boat (ch10.md:111). ch14.md:98 then shows "three horses". No outline says how her horse came back from a hostile estate.
- **M15. Ch3 miscounts the party.** ch3.md:169: "just the four remaining elves and Jaina". The party is three elves and Jaina (ch3.md:34). ch3.md:168, "the stark absence of the fifth horse": two riders left (ch3.md:64), so the missing horses are the fifth and sixth.
- **M16. Ch19 counts two horses for three riders.** ch19.md:26: "How the line reaches Northrend with two horses, one escort band". Three riders travel together from ch14.md:98 onward ("three horses").
- **M17. The Farstrider escort and the three rangers have no stated origin.** ch19.md:83 lists "Farstrider escort" in camp before Vereesa arrives. Ch18 ends with the trio and one relay rider (ch18.md:190-194). ch20.md:7 introduces "three Farstrider rangers". No outline says whether they come from Lor'themar's "small forward mobilization" (ch19.md:39) or from Vereesa's riders.
- **M18. Ch23 drops one ranger and swaps Sylvanas's bow.** ch23.md:94: "Cyndia takes the retreat route with two rangers while one stays closer to the pair". That ranger never appears again. ch23.md:166: "Sylvanas's reserve bow and last arrow ... a short recurve". The reserve bow is not set up, and the outline never says what happened to her main bow.

### Timeline and travel
- **M19. Ch16's main army keeps pace with hard-ridden horses.** ch16.md:87: "the main army's dust is still visible far enough back to matter". At ch16.md:151, Arthas reaches the gates while the riders are still on their second granary. The riders left camp "within minutes" ahead (ch15.md:146), yet the infantry column barely loses ground.
- **M20. Ch18 has open water ahead on a southbound road.** ch18.md:175: "dusk wind starting to cool with open water somewhere ahead". The trio is riding "south out of the city" (ch18.md:6). Ch19 places the coast north (ch19.md:174-177).
- **M21. Ch24 inflates the investigation to "months".** ch24.md:123: "Months of correct investigation are recast as months of deliberate preparation". The stated and inferred elapsed time from Ch1 to Ch23 is about five to seven weeks (see Appendix A).
- **M22. Ch22's return route is muddled.** ch22.md:5 lands the pair at "Southshore", then Scene 4 is titled "The Road South" (ch22.md:179). Their horses were left at the northern harbor (ch20.md:93), and no outline gives a mode of travel for the "overland race on the King's Road" (ch22.md:6). The outlines never say why the ship lands far from the northern harbor where they sailed from.
- **M23. Jaina's "one last time" stone call is not the last.** ch22.md:151: "Jaina reopens the Antonidas line one last time". A further call follows at ch22.md:200-203. The stone was "already dead" at ch20.md:92 and "cold and mute" at ch20.md:107, and no outline explains how it reopens.
- **M24. Ch20's landfall omits the burned fleet that Ch21 finds.** ch20.md:180 lists only "expanded docks, caches, bootprints, and empty camp traces" and "new timber on dwarven trade docks" (ch20.md:182). ch21.md:85-88: "burned ribs ... charred ship ribs frozen into harbor ice". Jaina's landfall POV misses the most visible thing in the bay.

### Character-file contradictions
- **M25. Cyndia changes flanks.** ch11.md:68: "She now permanently covers the right flank Lyriel used to hold." ch14.md:70 and ch15.md:71: "Holds the left position" / "Holds the left". The line is set at ch13.md:171 as "Jaina center, Sylvanas half a step forward-right".
- **M26. Ch1 names Cyndia in a scene where she is not present.** ch1.md:94: "Not even Cyndia expects a real threat from the south." Cyndia only enters in Scene 3 (ch1.md:64), and this is Sylvanas's limited POV.
- **M27. Antonidas's stone progression does not match the outlines.** char-antonidas:21-25 lists "Ch 2: calm mentor voice", "Ch 7: ... sending useful Cult intel", "Ch 8: Kel'Thuzad's name strips the softness out of him", and "Ch 12: longest silence in the book after Jaina reports the full scale". The outlines have no Antonidas contact in Ch2, Ch7, Ch8 or Ch12 (ch2.md:94: "only has a note"; ch12.md:74: "Present only through shared training"). Jaina reports the full scale in Ch14 (ch14.md:153).
- **M28. Lor'themar's appearances do not match his file.** char-lorthemar:30-32 lists "Ch 3-8: runner messages", "Ch 9: brief appearance to show the cost in his body", and "Ch 17-18: partial win with the scout company". Ch3-8 contain no Lor'themar messages. Ch9 uses only a runner (ch9.md:73). Ch17-18 contain nothing from him; the mobilization first comes via Vereesa in Ch19 (ch19.md:124).
- **M29. The tribunal beats sit in a different chapter from the character files.** char-uther:27, "Ch 25: tells the truth at the tribunal"; char-vereesa:26, "Ch 25: carries the disavowal"; char-antonidas:26, "Ch 25: he arrives, argues". In the outlines, all three happen in Ch24 (ch24.md:136, ch24.md:158, ch24.md:151), and Antonidas arrives in Ch22 (ch22.md:200).
- **M30. Muradin's arc beats changed.** char-muradin:23: "warns him off the blade, gets struck down anyway, and is left behind without a backward glance". char-arthas:34: "abandonment of Muradin". In Ch21, Muradin never confronts Arthas. He fights beside the pair and is hit by "ice-shard blowback" (ch21.md:173), and the pair carry him out (ch21.md:180). Arthas has no chance to abandon him.
- **M31. Antonidas is Kel'Thuzad's peer in one file and his teacher in the outlines.** char-antonidas:17 says he "trained beside Kel'Thuzad", making them peers. ch12.md:154 says "Antonidas trained both Jaina and Kel'Thuzad", and the Kel'Thuzad voice sheet has "Antonidas taught you the same discipline he taught me."

### Lore, geography, premise and pipeline references
- **M32. Hearthglen is staged on-page, against the location file.** loc-lordaeron:25: "Important mostly as offstage proof". Ch15 Scene 1 is set in Hearthglen (ch15.md:81-106). arc:54 ("Hearthglen to Stratholme") supports the outlines, so the location file is the outlier.
- **M33. The overview and story-arc premise disagree with Ch1.** overview:5 says Sylvanas "is investigating anomalies at the Quel'Thalas border — missing Farstrider scouts, dead livestock, villages that stopped sending trade caravans". Ch1 opens on a troll sweep, with the ward network "stable in every formal report" (ch1.md:17) and Sylvanas in the dark about "Anything about the plague" (ch1.md:22). arc:9 says "Sylvanas catches Jaina". In the outlines, Cyndia's post catches her before Sylvanas arrives (ch1.md:108-109).
- **M34. Outline reference links point to files that do not exist, and the compass contradicts canon.**
  - ch2.md:12, ch3.md:12 and ch12.md:12 link `plans/plague-process.md`. Only `plans/plague-mechanism.md` exists.
  - ch16.md:12, ch17.md:12 and ch18.md:12 link `locations/stratholme.md`. Stratholme lives inside `locations/lordaeron-and-northrend.md`.
  - Compass (the location files give no directions, so this is canon only): the outlines put Kel'Thuzad's base and Caer Darrow "north of Andorhal" (ch8.md:155, ch9.md:5) and Hearthglen south of the Eastweald (ch11.md:5). Stratholme is reached by a "North road" from Hearthglen (ch16.md:5), and the "southern supply road into Andorhal" runs through Strahnbrad (ch5.md:149). Canon Warcraft geography reverses most of these.
  - The Imperial Chamber has an "octagonal window" (loc-lordaeron:79) but an "octagonal dome" in ch23.md:125.

---

## Arc-beat delivery check (story-arc.md against the outlines)

| Arc beat (story-arc.md) | Delivered? |
| --- | --- |
| Sylvanas catches Jaina inside the ward boundary (arc:9) | Ch1-2. Cyndia's post makes the catch (M33). |
| Investigation Ch1-8, border to Andorhal (arc:52) | Yes, Ch1-8. |
| Scholomance Ch9-14: split, dark mirror, crack (arc:53) | Yes. The split is Ch9, the mirror Ch12, the crack Ch13-14. |
| Arthas Ch15-18, Hearthglen to Stratholme (arc:54) | Yes. Hearthglen appears on-page (M32), and Stratholme sequencing conflicts with the location file (V6). |
| Hardest turn: defies the recall (arc:32) | Delivered twice, in Ch14 and Ch19 (V4). |
| Endgame Ch19-25: Northrend, return, throne room, condemnation (arc:55) | Yes, but the travel timeline breaks (B1, B2). |
| Kill Arthas seconds after he murders Terenas (arc:11) | Yes, Ch23 (ch23.md:129, 165). |
| Save no one who can testify; condemned anyway (arc:6) | Yes. Ch23 has no witness, and Ch24 brings the verdict. |
| Frostmourne not solved when Arthas dies (arc:49) | Yes (ch23.md:39). |
| Mal'Ganis hides behind a repeated road-farewell (arc:48) | Five sightings delivered, but one is broken (B3) and Ch25's labels do not match them (V11). |
| High elves cannot be reanimated; Silvermoon complacent (arc:46-47) | Implied at ch19.md:117. Never tested on-page: Lyriel's body is not addressed, and the Millhaven column is never resolved (V7). |
| POV rotation with dual Ch22 and Ch25 (arc:5) | Broken in Ch23 and Ch24 (V5). |

---

# Appendix: Fact Ledger

## A. Timeline

Season: autumn throughout. Evidence: loc-lordaeron:12 ("autumn harvest"), ch2.md:152 (crops rotting), ch15.md:88 ("where no one dared finish the harvest"), ch22.md:189 ("wheat stubble and autumn orchards").

| Ch | POV | Stated "When" | Time of day | Elapsed from previous chapter | Running estimate |
| --- | --- | --- | --- | --- | --- |
| 1 | S | Story start | Day; Jaina caught "before dawn" (ch1.md:109); "amber light" (ch1.md:96) | n/a | Day 1 |
| 2 | J | "exact beat where Chapter 1 ends" | Corruption worse than "eight hours ago" (ch2.md:115); arrives Millhaven at "fading light" (ch2.md:183) | 0 | Day 1 evening |
| 3 | S | "Directly after Chapter 2" | Not stated | 0 | Day 1-2 |
| 4 | J | "Two days after Chapter 3" | Ends with "night coughing" (ch4.md:173) | 2 days (stated) | ~Day 3-4 |
| 5 | S | "Directly after Chapter 4" | Evening (ch5.md:91), "midnight stop" (ch5.md:135), "pre-dawn" (ch5.md:152); "hours" at the depot | ~1-2 days (inferred) | ~Day 5-6 |
| 6 | J | "Directly after Chapter 5's route choice" | Road mist; Andorhal sighted | <1 day | ~Day 6-7 |
| 7 | S | "Directly after Chapter 6" | "Late afternoon" (ch7.md:107), evening (ch7.md:136) | 0 | ~Day 7 |
| 8 | J | "The same night as Chapter 7" | Night | 0 | ~Day 7 night |
| 9 | S | "After hard days of Eastweald patrols following Andorhal" | Not stated | Several days (unstated) | ~Day 10-14 |
| 10 | J | "Directly after the Chapter 9 split" | "Cold" (ch10.md:88) | 0 | ~Day 11-15 |
| 11 | S | Parallel to Ch12 | Not stated | Ride south, camp, ride north (days; see V1) | ~Day 12-18 |
| 12 | J | Parallel to Ch11 | Underground | One sitting (see V1) | same |
| 13 | S | "Directly follows Chapter 12" | Ends in daylight and "late light" (ch13.md:167, 173) | 0 | ~Day 15-19 |
| 14 | J | "Directly follows Chapter 13" | "late afternoon sliding toward dusk" (ch14.md:5) | 0 | same day |
| 15 | S | "Directly follows Chapter 14" | Not stated (inferred night) | <1 day | +1 |
| 16 | J | "Directly follows Chapter 15" | Morning ("morning loaves", ch16.md:122) | Overnight ride | Culling day |
| 17 | S | "Directly follows Chapter 16" | Day through the Culling | 0 | Culling day |
| 18 | J | "Directly follows Chapter 17" | "hours later" on the wall (ch18.md:136); relay "At dusk" (ch18.md:172) | 0 | Culling day dusk |
| 19 | S | "One day after Chapter 18" | Day, then evening ride north (ch19.md:177) | 1 day (stated) | C+1 |
| 20 | J | "Directly follows Chapter 19" | Ends "By dawn" at landfall (ch20.md:172) | Coast ride (unstated) + "four days of deck motion" (ch20.md:182) | ~C+6-7 |
| 21 | S | "the morning after Chapter 20's landfall" | Morning onward | 1 night | ~C+8-12 |
| 22 | J/S | "hours after Chapter 21's retreat" | "dawn light" at the palace margin (ch22.md:225) | Return voyage plus the King's Road (unstated) | ~C+15-20 |
| 23 | J | "Directly follows Chapter 22" | "white sun through the octagonal dome" (ch23.md:125) | 0 | same day |
| 24 | S | "hours after Chapter 23's arrest" | Trial "all day" (ch24.md:165) | Hours, then the trial (gap unstated; V10) | ? |
| 25 | J/S | "the night after Chapter 24's verdict" | Night | <1 day | ? |

Stated durations that conflict with this ledger:
- Arthas "three weeks ahead" (ch20.md:199). See B2.
- Arthas "four days" in the palace (ch22.md:39). See B1.
- "Months of correct investigation" (ch24.md:123). See M21.
- Backstory durations: the new grain supplier arrived "three months ago" (ch4.md:128; ch7.md:96), Corin has been tracking shipments "for weeks" (ch7.md:96), and Muradin has been warning people "for months" (ch21.md:137).

## B. Travel

| Ch | Start | End | Mode | Duration / notes |
| --- | --- | --- | --- | --- |
| 1 | SE Eversong near the Amani frontier | Cyndia's post at Thalassian Pass | Thalassian horses, ridden hard south | Same day. Lor'themar and the patrol ride north at the fork (ch1.md:115-118). |
| 2 | Thalassian Pass post | Millhaven | Horses, 6 riders | Same day, arriving at dusk. |
| 3 | Millhaven | South road | Horses; Neral, the unnamed ranger and the girl go north | Two-day ride follows (ch3.md:169). |
| 4 | Unnamed sick village south of Millhaven | Grain road southwest | Horses | "Two days" from Millhaven. |
| 5 | Grain road | Southern supply road via Strahnbrad | Horses | Depots, a cleaned depot, a midnight stop, then pre-dawn turn south. |
| 6 | Southern feeder road | Strahnbrad camp, then within sight of Andorhal | Horses | Same stretch. |
| 7-8 | Andorhal gate (horses stabled outside the wall, ch7.md:85) | Corin's hideout | On foot | One afternoon and night. |
| 9 | Andorhal | Eastweald north of Andorhal, a farmhouse, a compound, a ridge | Horses, then on foot | "Hard days". |
| 10 | Ridge (split) | Barov estate, Darrowmere, Caer Darrow, Scholomance depths | Jaina on one horse, then on foot, then rowboat | Unstated. |
| 11 | Ridge | South to Arthas's field camp, then north toward Caer Darrow | Horses, 2 riders | Unstated (V1). |
| 13 | Darrowmere shore | Caer Darrow and back, then onto the south road | Horses, rowboat (Cyndia rows), east-face climb | Same day. |
| 14 | Eastweald road south of the Barov shore | Toward Hearthglen | Horses, 3 riders | Late afternoon to dusk. |
| 15 | South road | Hearthglen and war camp, then ahead of the army toward Stratholme | Horses | Unstated. |
| 16 | North road | Stratholme granaries, then back to the gates | Horses, then on foot | Morning. |
| 17-18 | Main gate | Service lane, inner wall, then south out of the city | On foot, then horses | Culling day to dusk. |
| 19 | Field camp south of Stratholme | North toward the coast | Horses | 1 day, then an evening ride. |
| 20 | Northern Lordaeron harbor (unnamed; loc-lordaeron:54 suggests Seastone Harbor) | Daggercap Bay | Wolfheart schooner; horses left on the quay (ch20.md:93) | 4 days at sea. |
| 21 | Daggercap Bay | Dragonblight, Muradin's camp, Frostmourne cavern, then retreat | On foot | Unstated; last leg in "hours and half-days". |
| 22 | Cavern | Muradin's camp, Daggercap, Wolfheart south, Southshore, King's Road, Capital City palace margin | On foot, ship, then overland (mode unstated) | Voyage faster than northbound; rest unstated. |
| 23 | Palace service door | Imperial Chamber, then custody | On foot | Same day. |
| 24-25 | Dungeon cells and tribunal hall | Cells | Static | Trial day, then night. |

## C. Main characters

### Sylvanas Windrunner
- **Rank and status.** Ranger-General (char-sylvanas:7). Her foreign deployment authority is suspended in Ch19 (ch19.md:117), and she is a deserter in practice from then on (ch19.md:191). In Ch24 she is convicted and given indefinite imprisonment.
- **Location by chapter.**
  - Ch1: Eversong, then the Pass.
  - Ch2-8: with Jaina.
  - Ch9: Eastweald.
  - Ch11: Arthas's camp, then north.
  - Ch13: Scholomance.
  - Ch14-19: with Jaina.
  - Ch20-21: at sea, then Northrend.
  - Ch22: the return.
  - Ch23: Imperial Chamber.
  - Ch24-25: cells.
- **Injuries.**
  - Ch9: "serious wound" (ch9.md:117), bandaged by Jaina (ch9.md:149).
  - Ch11: "healing wound" (ch11.md:88). Not mentioned after that (M12).
  - Ch23: drained by Frostmourne's field and "a real wound" (ch23.md:151); "blood on Sylvanas's forearm" (ch23.md:147).
- **Gear.**
  - Bow throughout.
  - Steel blade (ch1.md:89).
  - Thalassian horse until Ch20.
  - Reserve short recurve in Ch23 (ch23.md:166).
- **What she knows, and when.**
  - Ch1: Jaina's identity.
  - Ch2-3: physical contamination; Millhaven's dead marching north.
  - Ch4: grain is the carrier; a new supplier.
  - Ch5: Barov paper and Andorhal as the hub.
  - Ch6: the farewell is a pattern.
  - Ch7: masked handlers.
  - Ch8: Kel'Thuzad's name.
  - Ch9: the Hearthglen dispatch; a third farewell.
  - Ch11: Jaina has gone dark (no source; V2).
  - Ch13: Jandice's framing; Scholomance work rooms.
  - Ch14: the Lich King, the Burning Legion, resonance, ward failure, Kel'Thuzad's expected return.
  - Ch15: fourth farewell.
  - Ch17: fifth farewell.
  - Ch18: Arthas is sailing north.
  - Ch19: the recall; Lor'themar's cost.
  - Ch21: Frostmourne named by Muradin; arrows do not kill the bearer.
  - Ch22: the three-school plan; Arthas has been home four days.
  - Ch25: the visitor; the five faces resolve.

### Jaina Proudmoore
- **Age and appearance.** Twenty-three, blonde, blue-eyed (char-jaina:7). The outlines are consistent with this; they show frost-burns and ink (ch1.md:145).
- **Status.**
  - No Kirin Tor sanction (ch2.md:20, 95).
  - Severs the Dalaran line in Ch19 (ch19.md:40).
  - Convicted in Ch24.
- **Location.**
  - Ch1-2: holding cell, then released.
  - Ch2-9: with the party.
  - Ch10-12: Barov estate and Scholomance, alone.
  - Ch13 onward: with Sylvanas.
- **Injuries and body cost.**
  - Ch6: pain behind the eyes near Andorhal.
  - Ch20: blood and the widened channel; the bread-taste becomes constant (ch20.md:144, 146).
  - Ch22: tremor becomes baseline (ch22.md:128); "almost constant nosebleed" (ch22.md:160); collapses at Southshore (ch22.md:172).
  - Ch23: nosebleed; face on the marble; nearly empty (ch23.md:122, 161).
  - Ch24: harmed by the exhibit.
- **Possessions.**

| Item | Where in the outlines |
| --- | --- |
| Staff | Confiscated in Ch1 (ch1.md:138, 148); returned in Ch2 (ch2.md:115). |
| Map and tools | Confiscated (ch2.md:88); never explicitly returned. |
| Cover paperwork | Ch7, no source (M3). |
| Contamination map and notes | Ch8 (ch8.md:147). |
| Spell fragments and Barov transit papers | Ch9 (ch9.md:95). |
| Cyndia's estate notes | Ch9-10. |
| Torn Hearthglen dispatch | Briefly "in Jaina's hand" (ch9.md:127); goes to Sylvanas's thread. |
| Sending stone | First appears Ch9 (M5). Calls in Ch10, 14, 18 and 19. Dark/dead in Ch19-20. Reopened in Ch22 (twice). |
| Stolen grimoire | Ch10-12 only (M10). |
| Jandice's guest ward-mark | Ch10 onward, never resolved (M11). |
| "notes and samples" in her saddlebag | Ch18 (ch18.md:161). |
| Horse | Thalassian horse from Ch2; left on the quay in Ch20. |

- **What she knows, and when.**
  - Ch2: corruption has moved into flesh.
  - Ch4: the ingestion and bread pattern.
  - Ch6: the plague is engineered.
  - Ch8: Kel'Thuzad.
  - Ch10: resonance, and that Antonidas's ciphers shape Kel'Thuzad's work.
  - Ch12: the full awakening model, crude versus preserved dead, the Lich King, the Burning Legion, and Kel'Thuzad's expected continuity.
  - Ch14: Sylvanas's route went through the work rooms.
  - Ch16: node-level spoilage works; it fails at city scale.
  - Ch18: the broadcast and relay model.
  - Ch20: the source opposes the crossing.
  - Ch21: Frostmourne's name (from Muradin) and its seam.
  - Ch22: the three-school framework.
  - Ch24: the blade's acceleration is measured in days.

### Arthas Menethil
- **Ch6.** At Strahnbrad fighting the Blackrock orcs. Hears Jaina's warning and chooses the orcs.
- **Ch11.** At a field camp in the south. Briefed by Sylvanas; marches toward Hearthglen.
- **Ch13-14.** Reported moving toward Stratholme. Contradicted in Ch15 (V3).
- **Ch15.** War camp at Hearthglen, with damaged armor; calls Jaina "Lady Proudmoore" (ch15.md:117). Marches on Stratholme.
- **Ch16-17.** At the Stratholme gates; orders the Culling; afterward has clean hands.
- **Ch18.** Reported "taking ships north".
- **Ch20-21.** "Weeks ahead" (B2). Burned most of his fleet; claims Frostmourne. Light's Vengeance is left outside the cave.
- **Ch22.** In Capital City four days before the pair (B1). Undead guards placed in the palace.
- **Ch23.** Kills Terenas; killed by Sylvanas's second arrow.

## D. Recurring and minor cast

| Character | First appearance | Status and location trail |
| --- | --- | --- |
| Lor'themar | Ch1 (present) | Rides north to Silvermoon (ch1.md:62). Runners and dispatches in Ch9, Ch11, Ch14 (voice relay), Ch19 (via Vereesa). Arrives with 300 Farstriders in Ch24; outside the cells in Ch24-25. |
| Cyndia | Ch1, Scene 3 | Escort lead. With Sylvanas in Ch9-25. Starts the empty-flank check in Ch9, extends cover to Jaina by Ch22 (ch22.md:229). In custody at Ch23 close. |
| Lyriel | Ch2 | Right-flank escort. Killed in Ch9, Scene 2 (ch9.md:117). |
| Neral | Ch2 | Rides north with the survivor girl and the dispatch in Ch3. Off-board after that. |
| Unnamed fourth ranger | Ch2 | Rides north with Neral in Ch3. |
| Survivor girl | Ch3 | Taken north by Neral. |
| Old grain seller (Mal'Ganis face 1) | Ch3 | Farewell; wagon rolling north. |
| Ch4 village cast: militia captain, medic, granary keeper, cult initiate | Ch4 | The initiate dies of poison. |
| Dead depot overseer | Ch5 | Killed magically before the pair arrive. |
| Grain trader (face 2) | Ch6 | Road into Andorhal; "May the stars keep your road" (ch6.md:137). |
| Corin | Ch7 | Stays in Andorhal (ch8.md:73). |
| Captain Aldric Havel | Ch7 | Cult-paid; killed by Sylvanas's arrow in Ch8 (ch8.md:125). |
| Captured cultist | Ch8 | Killed by a death-curse. |
| Kel'Thuzad | Named Ch8; on-page Ch12 | Killed by Sylvanas in Ch13. |
| Courier (face 3?) | Ch9 | Killed by Cyndia (B3). |
| Lord Alexei Barov | Ch10 | At the estate; no further mention. |
| Jandice Barov | Ch10 | Escapes in Ch13; loose end. |
| Captain Falric | Ch11 | Ch11, 15, 16, 17. |
| Uther | Ch11 | Ch11 at the camp; Ch15 at Hearthglen; Ch17 breaks with Arthas; Ch18 rides west to Capital City; Ch22-23 in the palace; Ch24 testifies. |
| Aide or quartermaster (face 4) | Ch15 | Farewell in the camp. |
| Cult handler | Ch16 | Pinned by Sylvanas's arrow. |
| Grain carter (face 5) | Ch17 | Gives them the wall route and the farewell. |
| Vereesa | Ch19 | Delivers the recall and rides north. Delivers the disavowal in Ch24 and stays in the city. |
| Farstrider escort / three rangers | Ch19 / Ch20 | With the line through Ch23; in custody. |
| Captain Dagny Ironhull and the Wolfheart crew | Ch20 | Both voyages; last seen at Southshore. |
| Muradin | Ch21 | Wounded; left with Baelgun in Ch22. |
| Baelgun | Ch22 | Keeps Muradin at the camp. |
| Antonidas | Voice from Ch9 | In person from Ch22: at the palace margin, then in the tribunal gallery. |
| Two Kirin Tor magi | Ch22 | Palace margin; Ch24 gallery. |
| Terenas | Ch23 | Murdered; his soul is trapped in Frostmourne. |
| Thornton, Ashcombe | Ch24 | Judge and prosecutor. |
| The visitor (Mal'Ganis, unnamed) | Ch25 | Loose in the city. |

Supporting cast in character files who never appear in the outlines: Magistrix Eressea, Apprentice Maric, Lieutenant Marwyn, Captain Gavren Marsh (the file says he "arrests S&J", but the outlines use unnamed palace guards), and Ser Edric Valecrest (Book 2 seed).

## E. Relationship states

| Pair | Ch1-3 | Ch4-8 | Ch9-12 | Ch13-14 | Ch15-18 | Ch19-21 | Ch22-25 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sylvanas and Jaina | Custody, then specialist | Working alignment; first names by Ch4-5; full-speed partnership by Ch8 | Lyriel's death; split by necessity | Sanctum misread; Sylvanas verifying, rides half a step forward | Repair through work (Ch16) and shared witness (Ch17-18); the verification pause is gone | Chosen over both institutions (Ch19); honesty at sea; "one word" (Ch20); Muradin names them as a unit | Named combat partner; through-the-wall channel; Jaina names the truth (Ch25) |
| Sylvanas and Lor'themar | Easy, dry trust | Off-page | Pressure via runner | Recall via relay | n/a | Cost reported by Vereesa | Hands across the bars (Ch24) |
| Sylvanas and Vereesa | n/a | n/a | n/a | n/a | n/a | Recall refused; sisters part (Ch19) | Disavowal; Vereesa stays in the city |
| Jaina and Antonidas | A note left behind | n/a | Caution and delay (Ch9-10) | Partial truth; refuses to come home (Ch14) | Offers extraction (Ch18) | She closes the line (Ch19) | Reopened (Ch22); muzzled at the tribunal (Ch24) |
| Jaina and Arthas | n/a | Former lovers (ch17.md:98); he is courteous and dismissive (Ch6) | n/a | n/a | "Lady Proudmoore" (Ch15); she says "no" at the gate; she refuses the Culling | n/a | She scars the blade; he dies |
| Arthas and Uther | n/a | n/a | Uther names the flaw (Ch11) | n/a | Fear (Ch15); break at the gate (Ch17); Uther rides west | n/a | Near miss; testimony dismissed |
| Cyndia and Lyriel, then Jaina | Paired | Paired | Lyriel dies; the flank check begins | Checks the empty right flank | Relay and route | Shipboard discipline | Protective sweep covers Jaina (Ch22) |

## F. Factions and named objects

### Factions

| Faction | First appearance |
| --- | --- |
| Farstriders | Ch1 |
| Convocation | Ch1 (budget session) |
| Kirin Tor / Dalaran | Ch1 |
| Amani trolls | Ch1 |
| Cult of the Damned | Organized cult from Ch4; named in Ch9 (ch9.md:18) |
| Barov family | Paperwork in Ch5; estate in Ch10 |
| Lordaeron army and the Silver Hand | Ch6 |
| Blackrock orcs | Ch6 |
| The Lich King | Ch12 |
| Burning Legion | Ch12 |
| Ner'zhul | Ch23, no setup (M7) |
| Dwarven expedition | Ch21 |
| Nathrezim | Ch25, no setup (M8) |

### Objects and places

| Object or place | First appearance and fate |
| --- | --- |
| Ward-stones and the anchor stone | Ch1-2 |
| Dispatch tube | Ch3 (Neral) |
| Plague concentrate | Ch4, a clay vessel |
| Barov papers | Ch5 (paper trail); Ch9 (transit papers) |
| Spell fragments | Ch9 |
| Hearthglen dispatch | Ch9 |
| Guest ward-mark | Ch10 |
| Stolen grimoire | Ch10 |
| Sending stone | Ch9 |
| Farstrider relay stone | Ch14 |
| Recall document | Ch19 (red wax); disavowal in Ch24 (gold wax) |
| The Wolfheart | Ch20 |
| Light's Vengeance | Ch21; left in the snow outside the cave |
| Frostmourne | Ch21. Unheld from Ch23; in a lead-lined chest at the Ch24 trial; in the evidence vault in Ch25. |
| "May the stars keep your road" | Spoken in Ch3 (text first given in Ch6), Ch9, Ch15, Ch17; ancient Kaldorei original in Ch25 |
