# Fix log: Jaina's Kel'Thuzad trades (Ch12) and the confession at sea

Research: `research/voice-canon/jaina-young-confessions.md`.
Method: I re-read each file immediately before editing. Each edit was an exact-string replacement that aborted if the target string was not found exactly once. No whole-file rewrites. No `- Inside:` bullet was removed. One Inside bullet was updated (Ch19 B6, below).

## Part 1: The three trades rewritten

**Why.** The author flagged the old lines as cynical, manipulative and cold. Young Jaina is earnest. Each new line is a sincere admission that costs her because it is tender, proud or frightened. She would still hide each one from Sylvanas, and each would still shame her read aloud in court.

| Trade | Old | New |
|---|---|---|
| Antonidas (resonance) | "I love him, and he's too slow. I stopped waiting for his leave a long time ago. I still call him first, so he won't know." | "I didn't ask his leave, because he'd have said no and I'd have stayed. I want him to be proud of me. I want that more than I want to be right." |
| Arthas / Alterac (trigger, preserved layer) | "At Alterac I saw what he would do with a hard choice. I left him instead of staying to stop it, and I was glad to go." | "I left him over Alterac, and I let everyone believe it was my studies. I still think that if I'd stayed, he would have listened to me." |
| The knowledge (Lich King, Legion) | "I'd keep your notes. I want to watch it work once before I stop it." | "I'd learn the rest of it, even the parts I'll never need to stop it. I've been happy at this table. You teach me as fast as you can talk, and I keep up." |

### Edits

| File | Place | Before (short) | After (short) | Why |
|---|---|---|---|---|
| `.afternoon/outlines/chapter12.md` | End of chapter state, three quoted trades | old three lines | new three lines | Master copy of the trades |
| chapter12.md | Scene 2 B3 | old Antonidas line | new Antonidas line | Same |
| chapter12.md | Scene 2 B5 (mirror) | "she stopped waiting for Antonidas's leave, and so did he. The same institution made them both." | "she went out without Antonidas's leave to bring back something he would be proud of, and so did he, once. The same master made them both." | Kel'Thuzad's mirror now uses the new trade. Antonidas trained them both (`characters/antonidas.md`). |
| chapter12.md | Scene 3 B6 | "Jaina tries the public version, and he waits." + old Alterac line | "Jaina tries the public version, that they parted for her studies and his duties, and he waits." + new line | The canon breakup reason becomes the public story, which reconciles the AU's Alterac ruling with canon |
| chapter12.md | Scene 4 B9 | old last line | new last line | Same. Beat 8's refusals of easier answers are unchanged. |
| chapter12.md | Scene 4 B9 "They do not know" | "whether the wish is the room talking" | "whether the gladness is the room talking" | The new trade has no wish to use the spell |
| chapter12.md | Handoff, "What carries into Chapter 13" | "what she hides from Antonidas, why she left Arthas after Alterac, and that she would keep the notes and wants to watch it work once" | paraphrase of the three new trades | Consistency |
| `.afternoon/outlines/chapter14.md` | Starting position | "keep the notes and wants to watch the spell work once" | paraphrase of the new trades | Consistency |
| chapter14.md | Scene 1 B3 (the decision to report the product and keep the price) | "Antonidas, Alterac, and the wish to watch the spell work once stay with her" | "Antonidas's pride, Alterac and the studies, and how happy she was at his table stay with her" | Consistency |
| chapter14.md | Chapter close | "about wanting to watch the spell work once" | "about being happy at his table" | Consistency |
| `.afternoon/outlines/chapter18.md` | Pair's starting position | "she left Arthas instead of staying to stop him, and she was glad to go. Sylvanas does not know this." | "she left Arthas over it, let everyone believe it was her studies, and still thinks he would have listened to her if she had stayed. Sylvanas does not know this yet." | New Alterac trade |
| chapter18.md | Scene 1 B2 | "Years ago she left him instead of staying to stop him." | "She told Kel'Thuzad that Arthas would have listened to her if she had stayed. Today she was at his side, and he listened." | The Alterac sentence coming back "word for word" at the wall now turns on her concretely |
| chapter23.md | Scene 3 B8 | old three quotes | new three quotes | Ashcombe reads the master copy |
| `stories/the-plague-road/characters/voice-sheets/kelthuzad-voice.md` | "The mirror" sample line | "You stopped waiting for his leave. So did I. We were taught in the same rooms." | "You left without his leave, to bring him back something he would be proud of. So did I. We were taught in the same rooms." | The sample line quoted the old trade. This is not the jaina-voice sheet the other agent owns. |

### Checks
- I searched the whole repo for the old wording ("glad to go", "keep your notes", "watch it work once", "call him first", "stopped waiting for his leave", "wish to watch", "keep the notes"). It remains only in the frozen `outlines-pre-structural/` copies and in earlier fix logs, which are history and were left alone.
- The new lines were checked against `references/slop-hitlist.md`. They have no negation framing, no document or clinical vocabulary, no epigram cap, no counting, and no aphorism (see `research/voice-canon/jaina.md`, "no aphorisms at this era").
- Ch6 B5 (the Alterac ruling: "she left him over it") is unchanged and consistent. The studies are the cover story, not the reason.

## Part 2: Author decision, the confession at sea (resolution A)

**Decision.** In Ch19 B6, Jaina confesses the trades to Sylvanas. Sylvanas answers practically, with no absolution. Ch14 is unchanged: she still withholds there. At the Ch23 trial the reading shames Jaina and turns the court, but Sylvanas already knows. The spec's open question is resolved as A.

| File | Place | Before (short) | After (short) |
|---|---|---|---|
| `.afternoon/outlines/chapter19.md` | Jaina's starting position | (none) | Added: "Jaina has still not told Sylvanas what she paid Kel'Thuzad. The desk volume is in her bag, unopened." |
| chapter19.md | Hold back | (none) | Added: no absolution or recoil from Sylvanas, no narrated reading of the confession; it stays dialogue |
| chapter19.md | End of chapter state | (none) | Added: Jaina has told Sylvanas the three things in the words she used, and that he wrote in his book after each one. Sylvanas asked one practical question and moved on. The desk volume is unopened. |
| chapter19.md | Character Arcs, Jaina | (none) | Added: she ends the withholding begun on the Ch14 road |
| chapter19.md | Character Arcs, Partnership | (none) | Added: Sylvanas hears the trades from Jaina before anyone else can read them to her. Her answer is practical. |
| chapter19.md | Scene 3 B6, facts bullet | "Jaina says she had stopped asking Antonidas's leave long before she told him she was going north." | Jaina answers Sylvanas's letters admission with the three things she said to Kel'Thuzad, in her own words, and that he wrote in his book after each. Sylvanas asks one question: is that book in Jaina's bag? It is, unopened. She says nothing more. The Arthas line follows as before. |
| chapter19.md | Scene 3 B6 **Inside:** bullet (first clause only) | "said it about the leave, and Sylvanas didn't flinch;" | "said all three, his room's words in the open air, and Sylvanas asked about the book and nothing else;" (the rest of the bullet is unchanged, and it keeps the Inside format) |
| chapter19.md | Handoff, "What carries into Chapter 20" | (none) | Added: Sylvanas knows the three things, from Jaina. The desk volume is unopened. |
| `.afternoon/outlines/chapter14.md` | Hold back | "No confession of the three prices." | Added: "She tells Sylvanas at sea in Chapter 19." (The withholding itself is unchanged.) |
| `.afternoon/outlines/chapter18.md` | Hold back | "Sylvanas learns them in Chapter 23." | "Jaina tells Sylvanas at sea in Chapter 19." |
| chapter18.md | What carries into Ch19 | "Jaina has still not told Sylvanas what she paid Kel'Thuzad." | Added: "She tells her at sea in Chapter 19." |
| chapter18.md | Do not add yet | "Any confession of the Chapter 12 prices." | Added: "It comes at sea in Chapter 19." |
| `.afternoon/outlines/chapter23.md` | Hold back | (none) | Added: no framing of the reading as news to Sylvanas |
| chapter23.md | End of chapter state | "Sylvanas learns in public, from the enemy's hand, what Jaina kept from her." | Jaina is shamed in public with Antonidas in the gallery. Sylvanas heard the words from Jaina at sea, and her look at Jaina is the same after the reading as before. |
| chapter23.md | Character Arcs, Partnership | "The journal passages test it in public, in the enemy's own hand." | The passages shame Jaina and turn the court but do not split the pair. Show it only through Sylvanas's body. |
| chapter23.md | Scene 3 B8 facts | "Sylvanas hears all three in public... what Jaina kept from her after the Scholomance." | "Antonidas hears the first passage, about himself, from the gallery. Sylvanas heard all three from Jaina on the Wolfheart. She is the one person in the hall who looks at Jaina the same way after the reading as before." |
| chapter23.md | Scene 3 B8 "They do not know" | "...or whether Jaina will ever say any of it to Sylvanas herself." | "...or what Antonidas will make of the first passage." |
| chapter23.md | Scene 3 B8 Ground and outcome | "Sylvanas keeping her eyes on Ashcombe..." / "the secret goes off in the worst room it could." | "the whole hall turning to look at Jaina while Sylvanas, already looking at her, keeps the same look and the same still hands" / "The court turns on Jaina. Sylvanas stays where she was." |
| chapter23.md | Chapter close | "Sylvanas heard them in the hall." | "Sylvanas heard them in the hall, after hearing them from Jaina at sea." |
| `.afternoon/outlines/chapter24.md` | Starting position | "neither woman has spoken of them." | "Jaina told Sylvanas the same words at sea, and neither woman has spoken of the reading since." |
| chapter24.md | Chapter close | "The pair have not spoken of them." | "The pair have not spoken of the reading. Sylvanas had the words from Jaina at sea." |
| `research/input-audit/structural-fix-spec.md` | Cross-chapter fact 9 | "Ch24: Ashcombe reads... Sylvanas learns them in public, from the enemy." | Added the verbatim trades. Added Ch19 confession at sea. Ch23 reading shames Jaina and turns the court; Sylvanas already knows. |
| structural-fix-spec.md | Author decisions | "Still open: ... Version B is applied for now." | "Resolved: ... **A: Jaina confesses at sea (Ch19); the trial reading fails to split them.**" |

### Inside bullets reviewed and left as they are
- Ch12 B2, B5, B7 and B11 Inside bullets do not quote the old trades. "he used her own sentence" (B5) and "the room talking or her" (B11) fit the new trades.
- Ch14 "everything he told her, nothing she told him" still holds.
- Ch11 "Jaina's line, borrowed without leave" refers to the field-version phrase, not the trade.

## Canon grounding: Arthas history

**Decision.** The author wants canon lore only ("if Jaina left him because of her studies then that's that"). The invented "Alterac ruling" is removed everywhere. That supersedes the Part 1 trade 2 and its "public version" reconciliation.

**Canon, verified on warcraft.wiki.gg** (details and quotes are in `research/voice-canon/jaina-young-confessions.md`, section 3a):
- Arthas ended the romance, after the Noblegarden and Hallow's End courtship. Wiki summaries place it at Winter Veil; I could not verify that verbatim.
- His stated reason: she should focus on her studies in Dalaran and he on his commitments to Lordaeron. The Arthas page adds that he "wasn't ready to marry yet".
- "Jaina was very hurt by the decision but did not fight him on it." They agreed to remain friends.
- Jaina did not leave him. The studies were his reason, and she accepted it.

**New trade 2:** "When he ended it, I didn't fight him. Part of me wanted to go back to my books. I still think that if I'd stayed, he would have listened to me."

**New Ch6 memory:** the internment camp night (canon, *Arthas: Rise of the Lich King* ch. 3). On the road to Dalaran, Arthas talked her into slipping past the watchtowers of an orc internment camp. Jaina saw the females and infants and had doubts. Arthas was adamant the camps were necessary. I rejected Invincible's death: Arthas never told anyone the truth of it, so Jaina could not know it.

| File | Place | Before (short) | After (short) |
|---|---|---|---|
| `.afternoon/outlines/chapter6.md` | Scene B5, memory bullet | "Jaina remembers the Alterac ruling years ago... she left him over it." | "Jaina remembers a night years ago on the road to Dalaran, when Arthas talked her into slipping past the watchtowers of an orc internment camp to look. He was sure the camps were necessary before they reached the fence, and he was still sure after she had seen the females and the infants. Today he was slow, polite, and just as sure." |
| chapter6.md | B5 **Inside:** (first clause only) | "left him for being too fast, and today he was slow and still wrong;" | "sure before the fence, sure after the infants, and today slow and still sure;" |
| `.afternoon/outlines/chapter12.md` | End of chapter state, trade 2 | "about Arthas and Alterac: \"I left him over Alterac...\"" | "about Arthas: \"When he ended it, I didn't fight him. Part of me wanted to go back to my books. I still think that if I'd stayed, he would have listened to me.\"" |
| chapter12.md | Cast and handoff rules, Arthas | "what Jaina says about Alterac" | "what Jaina says about the end of their romance" |
| chapter12.md | Scene 3 "The action" | "Jaina pays with Alterac" | "Jaina pays with the end of their romance" |
| chapter12.md | Scene 3 B6 | public version "they parted for her studies and his duties" + old line | public version "they parted as friends so she could study and he could serve Lordaeron" + new line |
| chapter12.md | Handoff paraphrase | "let everyone believe she left Arthas for her studies..." | "when Arthas ended their romance she did not fight him because part of her wanted her books, and that she still thinks he would have listened if she had stayed" |
| `.afternoon/outlines/chapter14.md` | Starting position; Scene 1 B3; chapter close | Alterac and studies paraphrases | new paraphrase; "Arthas and her books"; "Arthas and the end of their romance" |
| `.afternoon/outlines/chapter18.md` | Starting position | "the truth about Alterac: she left Arthas over it, let everyone believe it was her studies..." | "the truth about Arthas: when he ended their romance she did not fight him, because part of her wanted her books, and she still thinks he would have listened..." |
| chapter18.md | Scene 1 B2 | "The sentence she gave Kel'Thuzad about Alterac" | "The sentence she gave Kel'Thuzad about Arthas". The payoff line, "She told Kel'Thuzad that Arthas would have listened to her if she had stayed. Today she was at his side, and he listened.", is kept. |
| `.afternoon/outlines/chapter23.md` | Scene 3 B8, trial reading | "About Alterac: \"I left him over Alterac...\"" | "About Arthas: \"When he ended it, I didn't fight him...\"" |
| `.afternoon/outlines/chapter19.md` | B6 confession | (no quote of trade 2) | No change needed. The B6 Inside bullet doesn't quote trade 2. |
| `research/input-audit/structural-fix-spec.md` | Fact 9 | "Arthas and Alterac"; Alterac verbatim line | "Arthas and the end of their romance"; new verbatim line plus a canon note ("There is no Alterac ruling.") |
| `stories/the-plague-road/characters/arthas.md` | Key ties | "Jaina saw the gap in him years before the story and left because of it." | the internment camp night; "Later he ended their romance so she could study and he could serve Lordaeron. She was hurt and did not fight him on it." |
| `stories/the-plague-road/characters/uther.md` | Jaina line | "Uther understands why she left Arthas..." | "Uther understands what Jaina saw in Arthas..." |
| `stories/the-plague-road/characters/voice-sheets/arthas-voice.md` | Register table, "The prince" row | "Ch6, Alterac in memory" | "Ch6, the internment-camp night in memory" |
| `stories/the-plague-road/plans/chapters/chapter18.md` | Beat 2 | "The Alterac ruling now reads as..." | "The internment-camp night, when Arthas was sure before he had looked, now reads as..." |
| `stories/the-plague-road/plans/subplot-jaina-arthas.md` | Core wound; Before the story (invented border-land dispute; "She ends it cleanly"); What Arthas carries | invented history in which Jaina leaves | the canon breakup (Arthas ends it for her studies and his duties; she does not fight it); the internment camp as the diagnostic incident; "what, in his mind, Jaina chose over him" |
| `research/voice-canon/jaina-young-confessions.md` | Section 3 reconciliation; section 8 item 2; section 6 | Alterac reconciliation and line | marked superseded; new section 3a with verified canon and sources; new trade 2 and its grounding |

**Left alone:** the geographic mentions of Alterac (`locations/lordaeron-and-northrend.md` roads; `research/voice-canon/terenas.md`, "decisive in Alterac", which is Terenas's canon Second War politics), the frozen `outlines-pre-structural/` copies, and older fix logs. Part 1 of this log records the superseded Alterac version as history.

**Check:** a repo-wide grep for "alterac", "left him over", "let everyone believe" and "my studies" now finds only the geographic mentions above and the historical notes in this log and the research file.
