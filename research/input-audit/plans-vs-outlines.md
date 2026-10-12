# The Plague Road: plans vs canonical outlines

Audit date: 2026-10-12. No input file was changed.

## Path key

| Short form | Full path | Role |
|---|---|---|
| `C<n>:<line>` | `.afternoon/outlines/chapter<n>.md` | **Canonical**. The pipeline reads these. |
| `S<n>:<line>` | `stories/the-plague-road/plans/chapters/chapter<n>.md` | **Second outline set** |
| `<plan>:<line>` | `stories/the-plague-road/plans/<plan>.md` | Thread and mechanism plans |

Every finding below quotes both sides. Findings marked "soft" are tensions, not hard contradictions.

## Pipeline context

- **Config.** `.afternoon/config.json:4` feeds only `story-arc.md` as `storyOverview`. Line 8 adds `characters` and `locations` as `materials`.
- **Progress.** `.afternoon/manifest.json:3` shows `"currentChapter": "chapter7"`, and `:15` shows `"chaptersCompleted": 6`. Chapters 1-6 already have prose. Chapter 7 is in progress, and Chapter 7 is where the Havel divergence starts (see a.2).
- **One plan file is still reachable.** Every canonical outline links `plans/plague-mechanism.md` in its References line, for example `C4:12` and `C7:12`. Any agent that follows links still reads that plan today.
- **Three links are broken.**
  - `C2:12`, `C3:12` and `C12:12` link `plans/plague-process.md`, which does not exist.
  - The second set has the same broken link in `S2`, `S3`, `S4`, `S5`, `S6` and `S12`.
- **The second set links the arc plans directly.** `S7` to `S25` have an "Arcs" line at line 14 that links the arc plans and neighbouring `plans/chapters/` files, for example `S24:14` → tribunal-mechanism, frostmourne-aftermath, frostmourne-seeking. Feeding the second set would therefore pull most of the plans back in with it.

---

## (a) Second outline set vs canonical

### a.1 Which set is newer: canonical

Content evidence, strongest first:

1. **A quote-stripping artefact in canonical.**
   - `C17:118` reads: "…and May the stars keep your road surfaces a fifth time and cannot be dismissed as coincidence anymore."
   - `S17:113` reads: "\"May the stars keep your road\" surfaces a fifth time under pressure".
   - The canonical sentence only parses as the second set's text with the quote marks removed.
   - The same stripping appears at `C16:146`, `C17:8`, `C18:50` and `C18:158`, each against a quoted original in S.
2. **Canonical fixes the second set's errors.**
   - Broken links: `C4:12`, `C5:12` and `C6:12` link `plague-mechanism.md`, where `S4`, `S5` and `S6` link the missing `plague-process.md`. Canonical's fixed links are a strict superset of S's.
   - Ch1 contradiction: `S1:68` says Jaina "does not speak on-page until the chapter-ending line", but `S1:148` gives the closing line to Sylvanas: "Start talking." Canonical `C1:66` says she "does not speak on-page in this chapter."
   - Ch4 patrol: `S4:16` cites "the follow-up patrol". No such patrol exists in Ch3. Canonical `C4:16` drops it.
   - Ch4 clue source: `S4:23` says "The old seller and the girl's testimony together produced one weak clue". `C4:22` corrects this to two separate clues, which matches Ch3.
   - Ch9/Ch10 mismatch: `S10:21` says "six minutes … at the Cult of the Damned forward camp", but `S9:118` says "Eight minutes in" at the farmhouse. `C10:18` says "The farmhouse read in Chapter 9".
   - Ch7 POV break: `S7:187` shows Jaina's lab work inside a Sylvanas-POV chapter ("Corin holding his breath while Jaina works through the poison's shape"). `C7:139` turns it into a report at the reunion.
3. **The second set has editing debris and placeholders that canonical does not.**
   - Empty beats: `S7:210-212` and `S7:256-258` are bare "-" bullets.
   - Typos: `S6:63` "hndoff", `S6:147` "useless useless", `S11:144` "full full truth", `S8:139` "the the".
   - Leftover fragments: `S23:146` "**yes** - the arrow passes the seam", `S24:121` "(none are)", `S24:141` "…offered to hold it. guilty on every major count".
   - Mislabelled lists: S's do-not-add lists carry the label "What they don't know" (`S21:176`, `S22:218`, `S23:183`, `S24:178`, `S25:149`).
4. **Canonical's later chapters build on canonical-only changes.**
   - `C11:21` "The dispatch Cyndia recovered points to Hearthglen" only makes sense after `C9:124` "Cyndia kills a fleeing courier and gets a torn dispatch". S9 has no dispatch, and `S11:24` says "Cyndia's Chapter 9 trail".
   - Canonical also keeps residue from S. `C14:124` recalls "hands and jaws still moving in trays", but the jaw image survives only in `S13:119` ("a jaw still moving in a bucket of preservative"). Canonical Ch13 dropped it.
5. **Canonical is formatted for the pipeline planner.**
   - `.github/agents/afternoon-planner.agent.md:51-52` maps "They do not know..." bullets and "Ground the..." bullets to beat fields.
   - Canonical has 204 "They do not know" bullets and 246 "Ground the" bullets. The second set has 0 "Ground the" bullets.
   - One mismatch remains. Canonical scene headers say **The action:** and **Starting point:** (88 occurrences each). The planner maps **What happens** and **Where we start** (`afternoon-planner.agent.md:59-61`), which only the second set uses.

**Counter-signal.** The second set follows the plan files more closely in several places: Ch3's Mal'Ganis label, Ch9's ambush and habits, Ch17/Ch19/Ch21's Arthas-chain lines, and the Ch24 Antonidas motive. This reads as plan-derived detail that the canonical rewrite cut or changed. It does not suggest the second set is newer.

**Git (not content, corroboration only).** `.afternoon/outlines` was last committed 2026-04-14 ("wip waiting for rate limits"). `plans/chapters` was last committed 2026-04-12 ("reformat outline").

### a.2 Substantive differences, by chapter

Structure is the same in both sets except where noted. POV headers are identical in all 25 chapters.

**Scene/beat counts that differ (C vs S)**

| Ch | Canonical | Second |
|---|---|---|
| 7 | 3/8 | 3/9 (two beats empty) |
| 9 | 3/7 | 4/11 |
| 10 | 4/8 | 4/11 |
| 11 | 4/9 | 4/11 |
| 12 | 5/12 | 5/13 |
| 13 | 4/9 | 5/12 |
| 14 | 4/10 | 4/11 |

**Ch1**
- Jaina's dialogue, as in a.1 item 2.
- S adds Lor'themar's joke that Cyndia knows where Sylvanas hides (`S1:94`, `S1:107`). C has "Not even Cyndia expects a real threat from the south" (`C1:94`).

**Ch2**
- Dalaran's stance:
  - `S2:93` "no one in Dalaran believed her"
  - `C2:95` "Nobody in Dalaran acted on her warning."
- When Jaina names Sylvanas:
  - `S2:58` "Jaina can think Sylvanas's name easily enough"
  - In C the shift waits until `C4:57`.

**Ch3**
- S tells the writer who the trader is: `S3:67` "Old grain seller: The first time we see Mal'Ganis in disguise." C never names him (`C3:66` "Helpful local source on the road").
- S breaks the naming cue: `S3:56` "When Sylvanas uses Jaina's name internally…". C does not.

**Ch4**
- `S4:184` "What we still don't know: Absolute proof of a Barov family connection." C forbids any Barov link: `C4:195` "Do not add yet: Any Barov connection."
- C links the trader early: `C4:129` "They do not know whether this is the same man from the road". S has no such line.

**Ch5**
- S has a mechanism rung that C lacks: `S5:131` "they still don't understand how it turns people into undead". C Beat 7 (`C5:135-137`) has no mechanism content.

**Ch6**
- How Arthas takes the warning:
  - `S6:137` "treats it as a peasant's rumor"
  - `C6:108` "stays perfectly courteous, and still chooses the orc skirmish"
- Who the trader is:
  - `S6:186` "(hidden cultist)" sits against its own `S6:191` "the exact same being"
  - C has only the same-being line (`C6:139`).
- Andorhal:
  - `S6:203` "already dead"
  - `C6:152` "a living hub instead of a dead one"

**Ch7 and Ch8: Havel (major divergence)**
- C makes Havel a traitor:
  - `C7:73` "…may hide something worse"
  - `C8:40` "Havel was on cult coin and dies when he tries to close the trap on them."
  - `C8:125` "Sylvanas kills him"
- S keeps him an ally:
  - `S7:289` "Corin and Havel are now trusted local allies"
  - `S8:41` "Corin and Havel remain local Andorhal allies"
  - Havel is in S's close cast (`S8:166`) and absent from C's (`C8:171-176`).
- C adds a dead-drop tail and a rooftop stakeout: `C7:124` "Sylvanas spots a worker making a dead drop and tails him through three streets".

**Ch9 (major divergence)**
- S has Jaina's mistake and the ambush:
  - `S9:112` "Jaina needs fifteen minutes"
  - `S9:118` "Eight minutes in, living Cult ambushers aggressively hit the farmhouse"
  - `S9:119` "Sylvanas takes a serious wound pulling Jaina out."
  - C has no ambush: `C9:95` "Sylvanas gives her only a short window … before the pack moves again".
- C moves the wound to Lyriel's death: `C9:117` "The first blast kills Lyriel at once … Sylvanas drags the survivors clear while taking a serious wound."
- New habits are only in S: `S9:151` "Sylvanas begins waiting for Jaina's magical sweep at chokepoints … 'how much time' is now the literal blood-price". C has only `C9:63` "It shows in the change of tempo".
- Source of the Arthas lead:
  - `C9:124` a courier's "torn dispatch", and "The dying courier uses the same farewell phrase again"
  - `S9:164-165` "Cyndia sighting a retreating figure"
- Kirin Tor:
  - `S9:171` "the Kirin Tor formally building the paper case against Jaina"
  - `C9:139` "Antonidas makes Kirin Tor suspicion formal"
- Elapsed time:
  - `S9:4` "several weeks"
  - `C9:4` "hard days"

**Ch10**
- C adds a guest ward: `C10:107` "only if Jaina accepts a guest ward that lets the house taste and track her arcane signature". S has no ward.
- S has Jaina lie to Antonidas: `S10:162` "lies by omission". C does not (`C10:151`).
- S has Jandice hand Jaina the binding answer early:
  - `S10:168` "anchors the victim's soul-echo to their rotting flesh"
  - `S10:191` "the terrible answer of how the dead are bound to service"
  - C keeps it withheld: `C10:41` "still lacking the full answer to how the dead are raised".

**Ch11**
- C puts Uther in the briefing (`C11:129` "Uther hears danger and incompleteness") without updating the Scene 2 cast list (`C11:110`). In S, Uther first appears after the briefing (`S11:146`).
- Only S has Sylvanas compensate for speed: `S11:92` "forces herself to pause at magical chokepoints". C has `C11:85` "She chooses speed."

**Ch12**
- S names Ner'zhul: `S12:151` "Ner'zhul supplied theory". C has the same idea unnamed: `C12:169` "came from beyond anything Dalaran could have taught".
- Only S has `S12:155` "Some plague behaviors belong to the Burning Legion rather than Kel'Thuzad."

**Ch13**
- S adds a standoff scene before the kill (`S13:128-139`) and gives Kel'Thuzad a last line (`S13:79` "gives one last data point"; `S13:184` "the lich-resurrection warning").
- C kills him without a speech: `C13:149` "Kel'Thuzad dies in seconds without a grand speech".
- What Jaina carries out:
  - `S13:41` "the full plague spell, the countermeasure"
  - `C13:41` "the full plague model, the waking trigger" (no countermeasure)

**Ch15**
- What Arthas is told:
  - `S15:118` "Lich King chain" named in the briefing
  - `C15:124` "the larger chain behind him"

**Ch16**
- `S16:119` "They break the second store". C: `C16:129` "The second store is worse. It is already half stripped". C never says the store was broken.

**Ch17**
- Only S has the Arthas-chain line: `S17:53` "Sylvanas lit this prince's road back in Chapter 11." C has nothing equivalent.

**Ch18**
- Antonidas's extraction offer:
  - `S18:141` "can offer extraction immediately … because the north answer has not finished forming"
  - `C18:158` "can offer extraction if she asks for it"
- Beat 4:
  - `S18:108` "small enough to dismiss"
  - `C18:114` "small enough to leave"

**Ch19**
- `S19:111` "explicitly threatens exile through military law". C has desertion only (`C19:117`).
- Only S has `S19:52` "she aimed Arthas at this crisis in the first place".

**Ch20**
- `S20:130` "crosses the halfway point". C has no such line (`C20:143`).

**Ch21**
- S gives a number for Arthas's lead: `S21:126` "Arthas left for the blade two days ago". C has none.
- Only S has `S21:52` "Sylvanas helped set this prince on the path".
- S calls the group a "trio" (`S21:116`, `S21:138`, `S21:150`), but both sets give the formation "all seven bodies".

**Ch22**
- When Arthas got home:
  - `S22:140` "Arthas arrived home days ago"
  - `C22:150` "Arthas is already in Capital City"
- Antonidas at the palace:
  - `S22:192` "Antonidas peels off to keep a public lane alive"
  - `C22:230` Antonidas stays "in the palace margins"

**Ch23**
- `S23:146` "takes the eye". C names no target (`C23:168`).
- `S23:59` "the blade still whispering overhead". C never says "whispering".

**Ch24**
- Only S gives Antonidas's motive: `S24:132` "would publicly expose Dalaran's prior warning and failure". C has none (`C24:152`).
- `S24:102` "one terrible verb: looking". C gives no verb (`C24:110`).

**Ch25**
- Different unknown:
  - `S25:29` "How many earlier hands or worlds Frostmourne has already consumed."
  - `C25:26` "How many earlier faces the visitor has already worn"
- `S25:115` "She stands and faces it". C gives Sylvanas no action.

Several of these give one set a plan beat the other lacks. The verdicts in section (b) are for canonical, with S noted where it differs.

---

## (b) Per thread plan

Verdicts: PRESENT, PARTIAL, PRESENT-ELSEWHERE, ABSENT, CONTRADICTED. Only non-PRESENT items are listed in detail. Each plan opens with a one-line tally.

### b.1 story-arc.md (the only plan the pipeline still feeds)

Most beats are present. Four problems:

- **POV rule contradicted in Ch23 and Ch24.**
  - Plan, `story-arc.md:5`: "Sylvanas odd chapters, Jaina even chapters, with dual exceptions in Ch 22 and Ch 25."
  - Outlines: `C23:3` "**POV:** Jaina Proudmoore" and `C24:3` "**POV:** Sylvanas Windrunner". This is the same in S.
  - Ch1-21 alternate strictly. Ch22 (`C22:3`) ends on Sylvanas in Scenes 4-5, so the swap may be deliberate, but the plan does not list it.
  - Knock-on: `C23:33` "No interior access to Sylvanas or Arthas." That blocks `partnership-arc.md:65` and `subplot-sylvanas-arthas.md:18` (see b.6 and b.9).
- **"Save no one who can testify": PARTIAL.**
  - Plan, `story-arc.md:6`: "save no one who can testify".
  - Outlines: Muradin is saved (`C22:249` "Muradin is alive enough to keep at Baelgun's camp"). Cyndia and three rangers survive in custody (`C23:200-201`). Two Kirin Tor magi "can independently feel the blade's wrongness" (`C22:201`). None of them appears in Ch24's witness logic.
- **Who catches Jaina: PARTIAL.**
  - Plan, `story-arc.md:9`: "Sylvanas catches Jaina inside the ward boundary".
  - Outlines: Cyndia's post catches her (`C1:109` "got caught studying the stones"), and Cyndia names her (`C1:146` "Cyndia finally puts a name to the human").
- **"Witty procedural" Ch1-6: PARTIAL.**
  - Plan, `story-arc.md:4`: "Ch 1-6 witty procedural".
  - Outlines: the only humor cue in C1-6 is `C1:93` "Lor'themar gently needles her". A grep for humor, joke, banter or wry in C2-6 finds nothing.
- **Present:** kill, condemnation and the blade staying live (`C23:38-39`, `C24:165`); the recall defiance (`C19:37`); the arc map.

### b.2 investigation-arc.md (Ch1-8)

Most beats are present. Problems:

| Plan | Outline | Verdict |
|---|---|---|
| `:11` "Sylvanas arrives angry, recognizes Jaina Proudmoore" | `C1:146` "Cyndia finally puts a name to the human" | PARTIAL |
| `:42` Ch5 "The old trader and empty wagon from Ch 3 snag retroactively"; `:72` "Mal'Ganis is only retroactively obvious" | `C4:129` "whether this is the same man from the road" (one chapter early; S has no such line) | Pre-empted |
| `:35` watcher "dies by poison" | `C5:113` "the same cold necromantic trace they found on other silenced witnesses". The only earlier witness died of swallowed poison (`C4:163`). | CONTRADICTED (same in S5:110) |
| `:54` "They enter as supply inspectors." | `C7:85` "Jaina's cover paperwork" only | PARTIAL |
| `:55` "Havel gives militia traction." | `C8:40` "Havel was on cult coin and dies when he tries to close the trap on them." | **CONTRADICTED** (S matches the plan) |
| `:67` "the name Kel'Thuzad sends them toward Scholomance" | `C8:155` "somewhere north of Andorhal"; Scholomance becomes the destination only at `C10:4` | PARTIAL |
| `:73` "Humor peaks in Ch 1-6" | see b.1 | PARTIAL |

**Present:** the hard rule on grain (`:70`, kept at `C3:166` "They still don't know grain is the specific carrier"); the Ch4 cult watcher (`C4:163-164`); Barov in Ch5 (`C5:120-121`); the Ch5 naming shift (`C5:136`); the Ch8 mid-sentence death (`C8:103-104`).

### b.3 silvermoon-thread.md

This is the most dropped thread. Of 17 chapter beats, 3 are present, 3 partial, 9 absent and 2 contradicted.

| Plan | Outline | Verdict |
|---|---|---|
| `:7` Ch1 baseline | `C1:86-93` | PRESENT |
| `:8` Ch5 "investigate within current mandate, no new resources" | No hit for mandate or "no new resources" in any C file | ABSENT |
| `:9` Ch6 "Dawnstar starts abstaining" | "Dawnstar" appears in no C file | ABSENT |
| `:10` Ch7 "Lor'themar shifts … to active advocacy" | No Lor'themar in C7 | ABSENT |
| `:11` Ch8 "full expedition vote fails. Recall threat begins." | No vote anywhere. Recall pressure first appears at `C11:158` | ABSENT |
| `:14` Ch9 "Lor'themar appears in person … takes the Scholomance proof" | `C9:73` "Off-page pressure reaching Sylvanas by runner"; Scholomance is first entered at `C10:118` | **CONTRADICTED / impossible** |
| `:15` Ch10 "Jaina becomes the new political weapon" | No hit | ABSENT |
| `:16` Ch12 "delay the recall three weeks" | `C14:146` "It is a formal recall. Lor'themar delivers the Convocation's order, and Sylvanas refuses it" | **CONTRADICTED** |
| `:17` Ch13 "Scholomance evidence cracks the certainty faction" | `C13:34` "No tribunal, debrief, or institutional aftermath." | ABSENT |
| `:20` Ch15 "Vandellor's new counterargument" | "Vandellor" appears in no C file | ABSENT |
| `:21` Ch16 "Stratholme finally shakes even Sunsorrow" | No hit; the Culling is still ahead (`C16:30` "No on-page Culling yet.") | ABSENT, and wrong on timing (see c.4) |
| `:22` Ch17 "scout company, 4-3" | Only `C19:124` "securing a tiny forward mobilization" | PARTIAL, moved to Ch19 |
| `:23` Ch18 "the wedge holds" | `C19:124` "even that small win may not survive the next chamber session" | ABSENT, outline leans against it |
| `:26` Ch19 Vereesa, recall | `C19:117`, `C19:123-126` | PRESENT |
| `:27` Ch20-23 scout reports | No Silvermoon beats in C20-23 | ABSENT |
| `:28` Ch23 "full expedition finally passes" | No vote; `C24:188` "three hundred Farstriders and mages" | ABSENT |
| `:29` Ch24 "one beat late" | `C24:187` "Lor'themar reaches the cells after the verdict" | PRESENT |
| `:30` Ch25 "custody pressure, vault scrutiny" | `C25:7` "Lor'themar and Vereesa off-page pressure only" | PARTIAL |

Two further outline problems:

- **Two recalls, two refusals.** One in Ch14 (`C14:146`), one in Ch19 (`C19:37` "Sylvanas refuses the Convocation's recall"). The plan has one recall, in Ch19. The Ch14 recall is delivered by Lor'themar, the thread's advocate.
- **Unexplained arrival.** 300 troops arrive on the same day as a one-day trial (`C24:4` "Opens hours after Chapter 23's arrest"; `C24:165` "all day"). No outline shows them leaving Silvermoon.

### b.4 kirin-tor-thread.md

| Plan | Outline | Verdict |
|---|---|---|
| `:7` Ch2 "first stone call. Antonidas believes Jaina, asks her home" | `C2:94` "Antonidas only has a note she left behind"; the first sending stone is at `C9:74` | **CONTRADICTED** (S2:93 is harder still: "no one in Dalaran believed her") |
| `:8` Ch4-6 offstage committee | No cue | ABSENT (offstage by design) |
| `:9` Ch7 archive intelligence | No Antonidas in C7. `C7:95` says "granary records Dalaran ignored" | ABSENT |
| `:10` Ch8 "Antonidas loses his qualifiers" | The name is spoken (`C8:154`); no Antonidas reaction | PARTIAL |
| `:3` Antonidas "right", an advocate | `C9:139` "Antonidas makes Kirin Tor suspicion formal"; `C9:171` "Farstrider and Kirin Tor backing are both collapsing" | Soft contradiction |
| `:14` Ch10 Kirin Tor method inverted | `C10:129`, `C10:137`, `C10:139`; no handwriting, no citation habits | PARTIAL |
| `:15` Ch12 "hardest call … Jaina reports the Lich King, the Legion" | No call in C12. The call is at `C14:153` "She gives him the strategic danger, but not the full mechanism" | PRESENT-ELSEWHERE (Ch14), PARTIAL |
| `:16` Ch13-14 "within the week" | No hit | ABSENT |
| `:19` Ch15-17 "monitoring and consultation" | No Antonidas in C15-17 | ABSENT |
| `:20` Ch16 "Stratholme damages the cautious faction" | Culling is Ch17 | ABSENT; wrong on timing |
| `:21` Ch18 extraction "on paper" | `C18:158` "can offer extraction if she asks for it" | PRESENT, softened to a real offer |
| `:24` Ch19 "last real call … not coming back" | `C19:40` | PRESENT, but undercut later (next two rows) |
| `:24` emotional severance in Ch19 | `C14:153` "When he tells her to come home, she refuses." | Pre-empted in Ch14 |
| `:24` "last real call" | `C22:151` "Jaina reopens the Antonidas line one last time" | Undercut in Ch22 |
| `:25-26` Ch21-23 advisory presence, then "Ch 24: he appears in person" | In person already at `C22:201` "come in person" and `C22:215` "Antonidas meets them at the edge of the palace" | CONTRADICTED on sequence |
| `:26` Ch24 time and review, cannot stop the verdict | `C24:152` "observe, object, and ask for continuance … treats unsanctioned blade examination as tampering" | PRESENT |
| `:27` Ch25 "he remains in the city" | 0 hits for "Antonidas" in C25 | ABSENT |

### b.5 scholomance-arc.md (Ch9-14)

| Plan | Outline | Verdict |
|---|---|---|
| `:9` Ch9 "The Cult ambush hits before she is done." | `C9:95` short window, no ambush; `C9:111` "The lost minutes at the farmhouse" | PARTIAL / ambush ABSENT (S9:118 has it) |
| `:10` Lyriel killed by the trap | `C9:117` | PRESENT |
| `:11` "New habits are born here: Sylvanas waits for sweeps; Jaina asks how long." | `C9:63` "change of tempo, not in speeches" only | ABSENT (S9:151 has it) |
| `:12` split after "breadcrumb and repeated farewell" | `C9:124`, `C9:147`; the farewell comes from a dying cult courier | PRESENT; see c.10 |
| `:18` Ch10 "chooses to go deeper alone instead of reporting out" | `C10:151` Jaina calls Antonidas | PARTIAL |
| `:23` Ch11 "Sylvanas briefs Arthas fully" | `C11:129` "withholds Kel'Thuzad's name and Jaina's position" | PARTIAL |
| `:30` Ch12 "intellectual before it is magical" | No magical duel in C12 | PARTIAL |
| `:39` Ch13 "kill Kel'Thuzad together in seconds" | `C13:149` "dies in seconds without a grand speech" | PRESENT |
| `:43` Ch14 "grain already out" | Not stated; nearest is `C14:162` | PARTIAL |
| `:49` "Mal'Ganis is steering both routes." | Nothing on Jaina's route | ABSENT |
| `:50` "three-way mirror" (Jaina, Kel'Thuzad, Arthas) | Arthas is not invoked in C12 | PARTIAL |

Present: the guardrail at `:5` (entry Ch10, interrupt Ch11, duel Ch12, damage Ch13, road out Ch14); the crack (`C13:54` "She acts correctly on the kill and incorrectly on the meaning"); the fractional delay (`C14:95`).

One unplanned addition: `C14:131` "Kel'Thuzad expected to survive his own death as a lich", with `C14:28` "Whether Kel'Thuzad's return can be stopped". No plan file mentions it, and no outline after Ch15 pays it off.

### b.6 partnership-arc.md

| Plan | Outline | Verdict |
|---|---|---|
| `:9` "security breach in violet robes" | `C1:145` "practical travel gear, worn boots" | Costume CONTRADICTED (minor) |
| `:12` "Sylvanas thinks 'the mage,' never 'Jaina'" (Ch1-4) | Kept in C. S3:56 breaks it. | PRESENT |
| `:21` "Sylvanas catches the register shift and says nothing." | `C2:144` "Sylvanas cuts her off" | ABSENT / inverted |
| `:35` "The Cult hits while she is still studying it. Sylvanas bleeds covering the exit." | `C9:95`, `C9:117`: the wound comes from Lyriel's blast instead | **CONTRADICTED** (S matches the plan) |
| `:37` "Neither apologizes. Both change behavior." | `C9:63` tempo only; Jaina's mistake costs nothing | PARTIAL |
| `:41` "after the Mal'Ganis breadcrumb" | courier dispatch at `C9:124`; no Mal'Ganis presence | PARTIAL |
| `:62` "Sylvanas takes the direct fight and loses it honestly" | `C23:144`, `C23:151` she is wounded but holds the window | PARTIAL |
| `:63` "Jaina invents the answer under pressure" | Invented in Ch22: `C22:164` "Exhaustion strips the thought down until it finally works"; `C22:165` full three-school framework | **CONTRADICTED** (see c.5) |
| `:65` "the qualities Sylvanas first filed under 'dangerous mage' … save her life" | 0 hits; Ch23 is Jaina POV with "No interior access to Sylvanas" (`C23:33`) | ABSENT |
| `:70` "Sylvanas waits for the sweep; Jaina asks how long." | Never planted in C9-11 (`C11:85` "She chooses speed."); S11:92 has it | ABSENT |

Present: Phase 2 (`C5:77-78`, `C7:111`); the Phase 3 split and crack (`C13:141-142`); Phase 4 (`C16:40`, `C17:142`); Muradin noticing the pair (`C21:130` "move like a machine built from two people"); the retreat (`C21:180`).

### b.7 plague-mechanism.md (still linked from every canonical outline)

| Plan | Outline | Verdict |
|---|---|---|
| `:38` Ch2-3 "Cannot yet split carrier, host change, and death trigger" | `C2:174` "The corruption is active in living flesh before death" | Soft: one rung early |
| `:39` Ch4-6 "repeated exposure, and body participation" | `C4:121` "repeated meals matter"; `C6:80` "the body is part of the mechanism" | PRESENT (C5 adds nothing) |
| `:40` Ch7-8 "the loudest signature is not the whole mechanism" | Not stated in C (S7:178 has it) | PARTIAL |
| `:45` "Jaina is still incomplete before Ch 12" | `C10:41`, `C12:18-19` | PRESENT (S10:191 breaks it) |
| `:46` "Kel'Thuzad completes the model; he does not replace it" | `C12:95-96` | PRESENT |
| `:46` (completes, does not replace) and `:9` "Grain carries the outer shell" | `C18:165` "Grain is not the real instrument of the plague. It is an echo, an amplifier, something answering a signal from somewhere else." | **CONTRADICTED** (soft); same in S |
| `:47` diction "answering chamber, … choir" | 0 hits in C | ABSENT (S uses it) |

### b.8 arthas-arc.md (Ch15-18)

| Plan | Outline | Verdict |
|---|---|---|
| `:26` Ch17 "the chain she started by recruiting Arthas becomes visible in full" | No hit in C17 | ABSENT (`S17:53` has it) |
| `:27` Ch17 farewell "now clearly a pattern" | Pre-empted: `C15:146` "the phrase is now a pattern Sylvanas cannot dismiss as coincidence"; also `C17:118` | Pre-empted by two chapters |
| `:34` Ch18 "Stratholme welds shut the Scholomance crack" | Closes twice: `C17:42` "The crack from Scholomance closes in practice", then `C18:37` "Shared witness shuts the crack" | Duplicated |

Present: `:11` "Uther clocks the partnership" (`C15:103`); `:24` the Culling and Uther's break in Ch17 (`C17:88-96`); `:28` "He looks up once" (`C17:146`); `:32` "comprehension rather than fear" (`C18:86`); `:33` direction, not comfort (`C18:136-137`).

### b.9 subplot-sylvanas-arthas.md

| Plan | Outline | Verdict |
|---|---|---|
| `:13` Ch6 "useful but mis-aimed military asset" | `C6:123` "Sylvanas can read Arthas as a military obstacle" | PARTIAL |
| `:14` Ch11 "briefs him fully" | `C11:129` "withholds" | PARTIAL |
| `:17` Ch17 detonation | `C17:88-96` | PRESENT; the causal-weight angle (`:3-4`) is absent in C (S17:53, S19:52 have it) |
| `:18` "Ch 23: Sylvanas closes the same chain with the arrow." | Arrow at `C23:165`; chain framing impossible in Jaina POV (`C23:33`) | PARTIAL |

Present: `:15` (`C15:50-56`) and `:16` (`C16:40`).

### b.10 subplot-jaina-arthas.md

All beats are PRESENT or compatible:
- `:10` diagnostic incident → `C18:93` "Alterac ruling"
- `:20` → `C6:116`
- `:35`-equivalent → `C18:93`

One PARTIAL: `:25` Sylvanas watching Jaina around dangerous men, given only as `C15:120` "Jaina tightening for a fraction".

### b.11 frostmourne-lure.md

| Plan | Outline | Verdict |
|---|---|---|
| `:7` Ch15 "a designer, a northern source, and a target that feels reachable" | `C15:124` "the larger chain behind him"; the target is Stratholme | PARTIAL |
| `:15` "S&J do not know about Frostmourne before the cave" | `C21:136` "Muradin names the weapon" before the cave (`C21:158`); `C20:33` and `C20:201` label "Frostmourne sensitivity" in Ch20 state lines | Soft breach |
| `:17` ship-burning | `C21:54`; Ch20 landfall in the same bay shows no wrecks (`C20:180-182`) | PRESENT, with a continuity gap |
| `:20` "The Lich King pushes sustained headwinds … because she is the threat" | `C20:38` "The source opposes them"; `C20:129` "her own northward probing is what made them legible" | PARTIAL: cause changed, Lich King unnamed |
| `:9` Mal'Ganis "curates real information" | No on-page curation to Arthas | ABSENT |

### b.12 endgame-arc.md (Ch19-25)

| Plan | Outline | Verdict |
|---|---|---|
| `:13` "duty, obedience, … protector becomes the threat" | `C20:136-137` duty only | PARTIAL |
| `:19` "read the same instant to disengage" | `C21:179` "retreats cleanly"; no shared-instant beat | PARTIAL |
| `:24` "Arthas is already home" | `C22:150` and `C22:193` "already been in the palace for four days". But `C21:195` puts Arthas "behind them in the cavern with Frostmourne" with his fleet burned (`C21:86`) | PRESENT, but physically impossible as outlined |
| `:31` "Jaina improvises the three-school seam strike" | Built at `C22:165` and choreographed at `C22:222`; `C23:16` "The anti-blade framework is real" | **CONTRADICTED** |
| `:43` Mal'Ganis appears | Body text says only "the visitor" (`C25:7`, `C25:127`) | PRESENT, unnamed |

Present: `:22-25` (Ch22 read, warnings fail, plan for "three to five seconds", `C22:222`); `:29-30` (`C23:129-132`); `:38` (`C24:165`); `:42` (`C25:97`).

But `:42` "Jaina *finally* names the real lesson" is pre-empted by `C14:175` "being right alone is the road that led Kel'Thuzad where he went".

Timeline issue (shared by S):
- `C18:172` Arthas "is taking ships north" at dusk on the day of the Culling. `C19:4` is "One day after Chapter 18". `C20:182` has "four days of deck motion".
- Yet `C20:199` says "Arthas is already inland and practically three weeks ahead".

### b.13 throne-room-mechanism.md

| Plan | Outline | Verdict |
|---|---|---|
| `:16` "read each other's movement without speaking" | `C23:67` only, generic | PARTIAL |
| `:19` "raw hands" | 0 hits; emptied (`C23:162`), nosebleeds (`C23:122`) and sensitivity (`C23:208`) are present | PARTIAL |
| `:24` "Kel'Thuzad's cross-school logic becomes the weapon" | `C22:167` "in plain field language instead of Scholomance language"; no credit to Kel'Thuzad | PARTIAL |

Present: cycle and seam (`C22:18`); frost, arcane, fire (`C22:165`, `C23:151-158`); "three to five seconds" (`C22:165`); "The deep tether north remains" (`C23:37`).

This file agrees with the outline's pre-planned strike. It disagrees with endgame-arc `:31` (see c.5).

### b.14 tribunal-mechanism.md

| Plan | Outline | Verdict |
|---|---|---|
| `:3` "Martial law" | 0 hits for "martial" | ABSENT (speed present: `C24:4`, `C24:165`) |
| `:5` Dalaran "cannot claim her without admitting it knew" | `C24:152` gives no motive (S24:132 states it) | PARTIAL |
| `:8-13` charges (regicide, espionage, necromancy…) | 0 hits; only "guilty on every major count" (`C24:165`) | ABSENT |
| `:17` "Warnings become alibis" | `C24:21` "recast as premeditation" | PARTIAL |
| `:19` "Defiance becomes proof of outside masters" | No hit | ABSENT |
| `:20` "designed covert team" | No hit | ABSENT |
| defense | No defense advocate exists; Uther testifies (`C24:137`), Antonidas objects (`C24:152`) | Gap |

Present, and exact: `:35-36` (`C24:165` "death commuted to indefinite imprisonment"; `C24:166` "political management rather than mercy"); `:4` and `:27` (`C24:159`, Vereesa carries the disavowal); `:31` (`C24:152` "tampering"); `:21` (`C24:101`).

### b.15 frostmourne-aftermath.md

| Plan | Outline | Verdict |
|---|---|---|
| `:7` "screams when it hits the floor" | `C23:180-181` "what an unheld blade sounds like"; 0 hits for "scream" | PARTIAL |
| `:8` "geometric patterns" | `C23:183` "frost racing through floor grooves like veins" | PARTIAL |
| `:9` "Terenas's soul flashes once to Jaina and is pulled back under" | `C23:181` "soul-echoes flash visibly including Terenas's freshest imprint"; not directed at Jaina, no pull-back | PARTIAL |
| `:14` "whispers, dreams, ward strain, and frightened guards" | Ward strain only (`C24:131`) | PARTIAL; whispers, dreams and guards ABSENT |
| `:25` "whispers, bad sleep" | Absent in C24-25 | PARTIAL |

Present: `:10` (`C23:187-188`); `:13` (`C24:94`); `:16-17` (`C24:107-108`, `C24:117`); `:20` (`C25:127` "the blade will find another hand").

### b.16 frostmourne-seeking.md

| Plan | Outline | Verdict |
|---|---|---|
| `:8` "Hours 6-24: whispers begin" | None in C24-25 | ABSENT |
| `:9` "tailored dreams" | None | ABSENT |
| `:14-16` "Ser Edric Valecrest", "Grieving steward", "Devout initiate" | 0 hits in any C file; `C25:105` "likely vulnerable targets in practical terms" | ABSENT |
| `:11`, `:30` "three to four weeks with no intervention" | `C24:40` "Jaina clocks Frostmourne's acceleration as days rather than weeks."; `C24:180` "the timetable collapses from weeks to days" | **CONTRADICTED** |
| `:21` "learns the wards by resonance" | `C24:130-131` wards degrade | PARTIAL |

Present: `:22` (Kirin Tor access blocked as "tampering", `C24:152`); `:25` (`C24:188`); `:26-27` (`C24:108`, `C24:130`).

### b.17 subplot-craft-research.md

This is a rule file with no beats.

- `:6` "Climax test: it must resolve in the climax, help create it, or be changed by it." The outlines add the Kel'Thuzad lich-return thread (`C14:131`), which fails this test: nothing pays it off.
- `:16` "Do not add: … Stand-alone Jaina backstory track." This conflicts with subplot-jaina-arthas.md (see c.11). The outlines use that backstory only inside Arthas scenes (`C6:116`, `C18:93`), so they comply.

---

## (c) Contradictions between plans

There are 12: 5 hard, 7 soft. "Outlines follow" says which side the canonical outlines take.

1. **Kirin Tor's hardest call (hard).**
   - `kirin-tor-thread.md:15` "Ch 12: hardest call in the book. Jaina reports the Lich King, the Legion".
   - `scholomance-arc.md:32` says Ch12 is when Kel'Thuzad "gives her the final theory" (Jaina is inside the sanctum). `scholomance-arc.md:43` puts the clinical briefing in Ch14.
   - Outlines follow scholomance-arc: the call is at `C14:153`.
2. **Silvermoon's Scholomance proof in Ch9 (hard).**
   - `silvermoon-thread.md:14` "Ch 9: … He takes the Scholomance proof".
   - `scholomance-arc.md:5` "Ch 10 = entry"; `:16` the Ch10 entry.
   - Outlines follow scholomance-arc (`C10:118`).
3. **Scholomance evidence in Ch13 (soft).**
   - `silvermoon-thread.md:17` "Ch 13: Scholomance evidence cracks the certainty faction".
   - `scholomance-arc.md:39` puts the Ch13 kill inside the fortress; `:43` puts the briefing of the evidence in Ch14.
4. **Stratholme reactions in Ch16 vs the Culling in Ch17 (hard).**
   - `silvermoon-thread.md:21` "Ch 16: Stratholme finally shakes even Sunsorrow" and `kirin-tor-thread.md:20` "Ch 16: Stratholme damages the cautious faction".
   - `arthas-arc.md:24` (Ch17) "Arthas answers with the Culling" and `subplot-sylvanas-arthas.md:17` "Ch 17: Stratholme is the detonation".
   - Outlines follow arthas-arc (`C16:30` "No on-page Culling yet.").
5. **Throne-room strike: planned or improvised (hard).**
   - `endgame-arc.md:23,25` "Ch 22 … Jaina finally gets a workable read … They plan the room: Jaina needs a few seconds"; `throne-room-mechanism.md:14` "three to five seconds".
   - `endgame-arc.md:31` "Jaina improvises the three-school seam strike" and `partnership-arc.md:63` "Jaina invents the answer under pressure".
   - Outlines follow the planned version (`C22:165`, `C22:222`).
6. **When the Scholomance crack closes (soft).**
   - `subplot-sylvanas-arthas.md:16` "Ch 16: … starts repairing the Scholomance crack"; `partnership-arc.md:52` "Ch 17-18: Stratholme welds the crack shut".
   - `arthas-arc.md:5` "The Scholomance crack is still live until Stratholme burns it shut" and `:34` (Ch18) welds it.
   - Outlines close it in both Ch17 and Ch18 (`C17:42`, `C18:37`).
7. **Disavowal vs custody leverage (hard).**
   - `tribunal-mechanism.md:4` "Sylvanas has no shield because Silvermoon disavowed her"; `:27` "the very disavowal she carried".
   - `silvermoon-thread.md:30` "Ch 25: the force becomes leverage for Book 2: custody pressure, vault scrutiny". The government that disavowed her is then pressing for her custody, and the thread never records the disavowal.
   - Outlines follow tribunal (`C24:159`) and keep Lor'themar "off-page pressure only" (`C25:7`).
8. **Elves without authority vs elves as leverage (soft).**
   - `frostmourne-seeking.md:25` "Lor'themar's elves … arrive without authority".
   - `silvermoon-thread.md:30` "vault scrutiny" as leverage.
9. **Kirin Tor access (soft).**
   - `frostmourne-seeking.md:22` "Kirin Tor access is blocked".
   - `kirin-tor-thread.md:25-26` "tiny advisory presence in Capital City … asks for expert review".
   - Outlines reconcile the two: present in person, blade access refused as tampering (`C24:152`).
10. **Silvermoon timing vs a fast tribunal (soft).**
    - `silvermoon-thread.md:28-29` has the expedition pass in Ch23 and arrive with the force in Ch24.
    - `tribunal-mechanism.md:3` "fast, harsh, and almost impossible to interrupt" leaves no travel window.
    - Outlines show it as a same-day arrival (`C24:4`, `C24:188`), unexplained.
11. **Jaina's backstory track (soft).**
    - `subplot-craft-research.md:16` "Do not add: … Stand-alone Jaina backstory track."
    - `subplot-jaina-arthas.md` is a Jaina backstory file (`:6-11` "Before the story … Diagnostic incident").
12. **Who can testify (soft).**
    - `story-arc.md:6` "save no one who can testify".
    - `endgame-arc.md:19` "They retreat clean with Muradin". Muradin is a saved witness to Arthas with the blade, and `tribunal-mechanism.md:23-27` never accounts for him.

Checked and compatible, so not counted:
- frostmourne-aftermath `:20` ("one sword line only") vs endgame-arc `:43`.
- frostmourne-lure `:20` (headwinds) vs endgame-arc `:14` (wind magic).
- tribunal `:26` vs silvermoon `:29` (Lor'themar late).
- investigation-arc `:73` vs arthas-arc `:3` (humor fades gradually).

One plan also conflicts with itself: `investigation-arc.md:23` "First dead village … bodies already gone north" vs `:26` "Survivors mention a new grain supplier". The outlines resolve it with a single survivor girl (`C3:122`).

---

## (d) Decisions the author needs to make

1. **Retire or quarantine the second set.**
   - It is older and carries errors that canonical fixed (a.1).
   - It sits inside `plans/`, and its "Arcs" lines (`S7`-`S25`, line 14) link the full plan set.
   - If you keep it, mark it superseded.
2. **Havel: ally or traitor?**
   - Canonical makes him a traitor (`C8:40`). The plan (`investigation-arc.md:55`) and S make him an ally.
   - Chapter 7 is in the pipeline now (`manifest.json:3`), so decide before Ch7 prose is accepted.
3. **Chapter 9's two mistakes.**
   - Option one: restore Jaina's ambush, the wound at the exit and the new habits, as S9 does.
   - Option two: rewrite `partnership-arc.md:35-37,70` and `scholomance-arc.md:9-11` to match canonical.
   - Later "fractional delay" and "waits for the sweep" beats depend on this choice.
4. **The Silvermoon thread.** Either restore the per-chapter political beats or rewrite the plan to the outlines' compressed version. Either way, settle:
   - one recall or two (`C14:146`, `C19:37`);
   - which refusal triggers the disavowal;
   - how 300 troops reach Capital City the same day (`C24:188`).
5. **The Kirin Tor thread.** Pick one version of each:
   - the Ch2 stone call (plan) vs "only has a note" (`C2:94`);
   - the hardest call in Ch12 (plan) vs Ch14 (`C14:153`);
   - the "last real call" in Ch19 vs the reopened line at `C22:151`;
   - Antonidas in person from Ch22 (`C22:215`) vs Ch24 (plan);
   - Antonidas absent from Ch25 (`C25`) vs remaining in the city (plan).
6. **POV for Ch23 and Ch24.** Keep the swap and amend `story-arc.md:5`, or swap back. If you keep it, find a new home for `partnership-arc.md:65` and `subplot-sylvanas-arthas.md:18`.
7. **Throne-room strike.** Keep it pre-planned (canonical) and fix `endgame-arc.md:31` and `partnership-arc.md:63`, or make it improvised and cut `C22:165` and `C22:222`.
8. **Frostmourne after the throne room.** Choose between `C24:40` ("days rather than weeks") and `frostmourne-seeking.md:30` ("three to four weeks"). Also decide whether whispers, dreams and the named candidates belong in Book 1.
9. **Arthas's timeline.** Reconcile the 1-day + 4-day crossing with "three weeks ahead" (`C20:199`). Also reconcile Arthas in the cave at `C21:195` with "already in Capital City" before the pair sail (`C22:150`).
10. **The road-farewell.** Decide whether a cult courier may speak it (`C9:124`). Decide when it becomes undeniable: Ch15 (`C15:146`) or Ch17 (plan). Decide whether the extra Ch15 "Alliance aide" appearance stays.
11. **Unplanned threads and model shifts.**
    - Pay off or cut the Kel'Thuzad lich return (`C14:131`).
    - Decide whether the Ch18 "grain is an amplifier" model (`C18:165`) replaces `plague-mechanism.md:9`. That file is linked from every canonical outline, so whatever it says is still being read.
12. **Tribunal content.** Add martial law, the charges and the prosecution framing to Ch24, or trim `tribunal-mechanism.md:3,8-13,19-20`.
13. **Mechanical fixes.**
    - Point the broken `plague-process.md` links (`C2:12`, `C3:12`, `C12:12`) at `plague-mechanism.md`.
    - Restore the stripped quote marks at `C17:118`.
    - Fix canonical's scene labels (**The action:**, **Starting point:**). The planner maps **What happens** and **Where we start** (`.github/agents/afternoon-planner.agent.md:59-61`).
