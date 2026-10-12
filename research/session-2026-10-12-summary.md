# Session summary: 12 October 2026

What changed in this repo during one long session, why, and where everything lives. The repo is prepared for a fresh full run of The Plague Road.

---

## 1. Claude Code version of the pipeline

The pipeline was originally written for GitHub Copilot. It now runs in Claude Code, using Claude models only.
- **Agents:** 17 in `.claude/agents/afternoon-*.md`.
  - **Opus:** writer, craft-auditor, craft-reviser, plan-verifier, continuity-gate, slop-gate, grounding-gate and style-extractor.
  - **Sonnet:** the orchestrator, planner, coordinator, slophunter, grounder, memory-keeper and the rest.
- **Skills:** 11 in `.claude/skills/`.
- **Nesting:** subagents can nest up to three levels. The pipeline needs two: orchestrator, then writer-coordinator, then writer and craft agents.
- **Running it:** start a headed session in this repo with the orchestrator agent. When `.afternoon/manifest.json` is missing, the orchestrator builds it from `.afternoon/outlines/`.

## 2. Baseline run (Ch1, isolated copy, before today's changes)

- Ran headless (`claude -p`, bypass permissions) on a throwaway copy, using the rules and outlines as they stood this morning.
- **Result:** completed. The final draft is about 6,100 words, down from the writer's 9,200-word first draft.
  - **Slop gate:** passed after three revision rounds.
  - **Grounding gate:** passed on its last allowed round.
- **Archived at** `_past-runs/12-10-2026-isolated-ch1-baseline/`: the chapter directory with every version and gate note, plus the manifest and run log.
- **Use it as the comparison point for the fresh run.** Every slop pattern flagged later in the day was still in its final draft:
  - "She would have to go and find one."
  - "Without looking, she held her bow out"
  - "let the silence run"
  - "a smell Sylvanas couldn't place, [places it]"
  - "Which left going in herself."
- **Rhythm scorer:** participial joins at 5.4% against a 12% target; 21 flat passages flagged.

## 3. Slop rules added

The author wants judgement-heavy patterns handled by the LLM passes, not by static checkers, because static checkers throw too many false positives. Each new pattern is a section in `references/slop-hitlist.md` plus an example file in `references/ai-quirks/sentence-level/`. The README now says to read files 01–13.

| Pattern | Example | Limit | Quirk file |
|---|---|---|---|
| Permission tags | "and she let it" | zero | 08 |
| Contact verbs with agency | fingers *found*, the ache *settled* | zero | 09 |
| Counting devices | "his first ten strides" | zero | 10 |
| Unplaceable, then placed | "a smell she couldn't place, the air before snow" | zero | 11 |
| Claim, then gloss | "no reason to trust a word… She would have to go and find one." / "Which left going in herself." / "Close enough to reach. Close enough to be reached." | zero | 12 |
| No-look handoff | "Without looking, she held out her bow. Cyndia took it." | 1 per book | 13 |

Other changes to the rules:
- **Good samples flipped:** several ai-quirks files had "good" samples that themselves contained permission tags or contact verbs. Those samples were rewritten (files 01, 04, 05, 08, 09, 11, 12, 14, 17 and others).
- **The negation trap:** the negation guide was producing permission tags and glosses as its *replacements*. `resources/negation-addiction-hunting-guide.md` now has two "replacement trap" sections, one for permission tags and one for claim-then-gloss.
- **Gloss calibration:** the slop gate had kept "go and find one" three times, reasoning that "the second sentence can't stand alone". `resources/gpt-5-prose-issues.md` F4 now says that dependency is evidence of a gloss, never a reason to keep it.
- **Participial joins encouraged:** `style-samples/texture-transformations.md` §7 shows how to merge adjacent short sentences into a main clause plus an absolute phrase ("Her shoulder burned, sweat creeping from her hairline…"). The craft-reviser points to it.
- **Static checker:** `tools/slop_checker/patterns/contact_verbs.py` was reverted to its original 5 patterns. `permission_tags.py` (3 zero-cap patterns) still exists; **the author hasn't decided whether to keep it**.

## 4. Opus quirks study

- The pipeline's pass guide was written for GPT-5 output. An Opus 5.5 agent wrote 10 blind fantasy samples (`research/opus-quirks/samples/`) and audited them (`research/opus-quirks/REPORT.md`).
- The GPT-5 guide is kept. Opus patterns F8–F15 were added to `resources/gpt-5-prose-issues.md`:

| Code | Pattern |
|---|---|
| F8 | Echo exchange |
| F9 | Name-only or vocative lines |
| F10 | Briefing-stack dialogue |
| F11 | Anaphoric runs |
| F12 | Non-action beats |
| F13 | Demonstrative caption |
| F14 | Fenced manner adverb |
| F15 | Dying-fall coda |

- **Model comparison:** the same chapter brief was given to Opus 4.5, 4.6, 5 and 5.5 and Sonnet 4.5, 4.6, 5 and 5.5. The results are in the tuesdays-universe repo (`ten-years-on-model-test/`). The tells differ by generation. "Without looking" appears in every model's output.

## 5. Input audit and continuity fixes

The pipeline's input bleeds into its output: the writer imitates the scene plans, voice sheets and rhythm anchor. All of these were audited:
- `research/input-audit/continuity.md`: continuity and consistency across the 25 original outlines.
- `research/input-audit/plans-vs-outlines.md`: the older story plans against the outlines.
- `research/input-audit/register-and-bleed.md`: tells in the inputs that leak into the prose.
- `research/input-audit/fix-decisions.md`, `fix-log-continuity.md`, `fix-log-malganis.md`: 219 continuity fixes. They include:
  - **The compass handoff** between Ch14 and Ch15.
  - **The Arthas timeline:** Culling = C; Daggercap around C+6; Southshore around C+20; the walls around C+23.
  - **Havel** introduced through the tally-man.
  - **The ranger** who carries word to Lor'themar.
- **Mal'Ganis** now appears five times in different disguises. At each sighting he watches his work going to plan, and on a second read he is passing orders to cult personnel:
  - an old carter;
  - a granary tally-man;
  - a robed figure at the Eastweald trap;
  - a quartermaster's aide;
  - a Stratholme carter.
  
  Each sighting has a "Second read" note. The prose must never explain it.

## 6. Structural rework (25 to 24 chapters)

- **Reviews:**
  - `research/input-audit/structural-review.md`: a whole-book review covering plot, climaxes and how the threads are woven.
  - `research/input-audit/pacing-and-quality.md`: a separate audit with the pacing skill and a pressure curve.
- **Decisions and logs:**
  - Binding spec with the author's decisions: `research/input-audit/structural-fix-spec.md`.
  - Logs: `fix-log-structural-1-11.md`, `-12-19.md`, `-20-25.md`, `fix-log-jaina-trades.md`, `fix-log-inside-beats.md`, and `fix-log-thread-docs.md` (the thread docs synced to the new outlines).
- **Snapshot:** the outlines as they stood before the rework are in `research/input-audit/outlines-pre-structural/`.

The main changes, by area:

**Theme acted out, not stated**
- The "being right alone isn't enough" restatements were cut.
- The twin sins are wired into the plot:
  - Sylvanas: she moves before Jaina's read (Ch9, Lyriel dies), and she points Arthas at the war (Ch11).
  - Jaina: she answers Arthas alone, over Sylvanas, with "not cleanly, not now" (Ch16), and he turns it into the Culling.
- On the wall in Ch18, the crack between them closes through shared guilt.
- In the Ch20 cave, Sylvanas holds her shot and waits for Jaina's read, the inverse of Ch9.

**The Kel'Thuzad trade (Ch12)**
- Each piece of the spell costs Jaina one true sentence, and Kel'Thuzad writes each answer down. The sentences are grounded in canon young Jaina:
  - **About Antonidas:** "I didn't ask his leave, because he'd have said no and I'd have stayed. I want him to be proud of me. I want that more than I want to be right."
  - **About Arthas, per canon (he ended it, and she didn't fight him):** "When he ended it, I didn't fight him. Part of me wanted to go back to my books. I still think that if I'd stayed, he would have listened to me."
  - **The dearest:** "I'd learn the rest of it, even the parts I'll never need to stop it. I've been happy at this table. You teach me as fast as you can talk, and I keep up."
- She carries the journal out without opening it. She withholds the trades in Ch14 and confesses them to Sylvanas at sea in Ch19. At the trial in Ch23 the prosecutor reads them aloud. That shames Jaina in public, but it can't split them, because Sylvanas already knows.

**Canon Arthas history**
- There is no invented "Alterac ruling". In canon, Arthas ended the romance.
- Jaina's Ch6 memory is the orc internment-camp night from Christie Golden's *Arthas: Rise of the Lich King*.

**Throne room (Ch22)**
- The plan breaks at the fire phase. Jaina puts her last fire into Sylvanas's arrowhead, and the arrow carries it through the seam, so the kill is the spell.
- Arthas says "Jaina" once.
- The canon exchange is used as written: "What is this? What are you doing, my son?" / "Succeeding you, Father."
- Arthas's homecoming is a public noon audience, which gives the race a clock.

**Trial (Ch23) and refusal**
- The trial follows the *To Kill a Mockingbird* shape: Uther's testimony lands, then the journals turn the room.
- Lor'themar's three hundred arrive during the trial and buy the commutation.
- Captain Brask's letter from the saved village in Ch4 is ruled irrelevant.
- Captain Marsh is the eyewitness. The prosecution counts four dead guardsmen.
- After the verdict, Lor'themar can open only Sylvanas's door, and she refuses.

**Ch24 stinger**
- The visitor passes through on his way to the blade. He says two lines and the Kaldorei farewell, and he looks past the women toward the vault.
- The book ends on Jaina feeling the pulse move away.

**Mal'Ganis's farewell**
- It stays rare: no innocent character ever says it.
- Every sighting comes while something bigger is on fire, so Sylvanas never has time to chase it.
- In Ch17 she chooses the wall over following the carter.
- Two sightings cause later moves: Lyriel's friendly answer leaks the witness, and the trap in Ch9 is built on the riders' spacing.

**Act 3 compression**
- Old Ch18 and Ch19 are merged into a dual-POV Ch18.
- The return voyage in Ch21 is a jump cut.
- Antonidas's calls and Lor'themar's runners are thinned.

**Investigation variety**
- The Ch4 village is saved.
- The Ch5 overseer lies and costs them a day.
- The Ch9 courier gives a false lead.
- Lyriel gets a life before she dies, including the one-handed bandage knot that Jaina later ties on Sylvanas.

**What the author rejected**
- A running "field version" joke. It's cut, and only one quiet echo of Jaina's Ch6 line remains in Ch11.
- Making the farewell a common blessing.
- Making the Ch9 dispatch a Mal'Ganis plant.
- A courtroom choice for the accused.

**Bookkeeping**
- The POV pattern and arc map in `story-arc.md` are updated for 24 chapters.
- Chapter references in the profiles and thread docs are renumbered.

## 7. Interiority (free indirect thought)

The writer used to be asked only for body tells ("a flinch, a stomach dropping"). Introspection came out as narrator arithmetic: "Waiting was no better than letting her go… Which left going in herself."
- **`afternoon-writer.md`:** a new section, "Let her think in her own words". It asks for her idiom, her questions to herself, self-correction and a contradiction left standing. It tells the writer to end on action, never a verdict. Test: could she mutter it under her breath?
- **`afternoon-writer-craft-auditor.md`:** the interior-moment check now asks for thought in the character's own idiom, not body sensation.
- **`afternoon-planner.md`:** an optional `Inside:` bullet in an outline beat maps to a new `interiority` plan field, written as keyword clauses.
- **`negation-addiction-hunting-guide.md`:** keep condition 4 covers self-argument in free indirect thought. It never protects a following gloss.
- **`narrator-seep-guide.md`:** a note that free indirect thought is not seep.
- **Outlines:** 76 `Inside:` bullets (39 for Sylvanas, 37 for Jaina), giving the argument she's having, not the conclusion. Some read as finished prose, so watch for verbatim copying in the first run.

## 8. Voice sheets (28, every character)

- In `stories/the-plague-road/characters/voice-sheets/`, with canon research in `research/voice-canon/` (sources, era, fit). Sylvanas and Jaina have new "Inner voice" sections.
- **Arthas** has three stages: prince, Stratholme, after Frostmourne. **Mal'Ganis** has one voice per disguise plus his true voice.
- **Files are named the way the outlines name the character** (`havel`, `brask`, `marsh`, `thornton`, `ashcombe`), because the writer looks up sheets by the cast name.
- **The no-verbatim rule for canon lines was removed** at the author's request.
- **Caveats:**
  - Wowpedia was blocked, so the quotes come through warcraft.wiki.gg summaries and haven't been checked against the games or books.
  - Canon is thin for living Sylvanas, Lor'themar, Vereesa, Marwyn, Alexei, Jandice and Baelgun, so parts of those sheets are inferred.
  - The Kaldorei farewell *Anu kal dela ana'diel* is invented.
  - Eressea and Maric appear in no outline beat.

## 9. Repo state for the fresh run

**Archived** to `_past-runs/13-4-2026-plague-road-ch1-7/`:
- the April run's state: `chapters/` (prose for Ch1–7), `plans/` (chapter plans, memory, series-meta), `agents/` (status files) and `manifest.json`;
- copies of `config.json`, `overview.md` and `style-guide.json`;
- the pre-rework outlines;
- the legacy per-chapter story plans (`legacy-story-plans/chapters/`). These used the old 25-chapter numbering and invented history, and nothing in the pipeline read them.

**What is left in `.afternoon/`:** `config.json`, `config.json.sample`, `overview.md`, `style-guide.json` and `outlines/chapter1.md`–`chapter24.md`. There is no manifest, so the orchestrator starts fresh from chapter 1.

**Not committed:** all of today's changes are uncommitted in git.

## 10. Open items

- **Register and bleed fixes (offered, not yet applied):**
  - scene-plan briefing-style wording;
  - the rhythm anchor's tells;
  - the "good" examples in the catalogue;
  - `style-guide.json`;
  - the stock-moment list in the writer prompt.
  
  See `research/input-audit/register-and-bleed.md`.
- **The `permission_tags.py` static detector:** keep it or remove it?
- **Untried ideas:**
  - A dialogue-only pass with full chapter context, using Opus 4.8.
  - An older model as a second auditor; precision needs testing first.
- **Unresolved by the baseline run:**
  - ranger names invented to fill unnamed roles (Theris, Feren, Liron);
  - Jaina's restraint in Ch1 (a chained ring-bolt) against what the Ch2 plan expects (a warded circle).
  
  The fresh run will regenerate both from the new outlines, so check whether they recur.
- **First thing to check in the fresh Ch1:** do the new patterns stay out, does Sylvanas think in her own idiom at the prisoner decision, and do the `Inside:` bullets get copied word for word?
