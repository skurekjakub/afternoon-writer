# Phase 2: Build False-Positive Filter

Before running any guide audit, read the chapter plan (`.afternoon/plans/{chapterId}.json` or `{chapterId}-initial.json`) and build the filter that prevents false positives.

Prime these four contexts:

1. **POV character(s)** and their cognitive profile - how they think, what they notice, what shorthand they use. A trained military mage inventories rooms differently than a farmer. A scholar's internal monologue naturally runs in organized analytical patterns. A spy notices absences tactically, not decoratively.
2. **Subject matter** - what the chapter is actually about. If the chapter is about plague-grain conditioning and tissue-level magical theory, then sentences describing tissue "learning" or "holding" patterns may be literal descriptions of the in-world science, not anthropomorphic writing tics.
3. **Intentional plot dynamics** - where the author is deliberately doing something that might superficially resemble an AI pattern. Cooperative antagonists who want the POV character deeper are not pleasantness bias. A seduction/intellectual-courtship scene that accelerates access is not conflict collapsing.
4. **Dialogue register** - who is speaking, what the line is trying to accomplish, and whether the quoted abstraction is character voice or speech-level slop.

Carry this context into every guide audit as the false-positive filter:

- **Character-voice defense**: If a flagged pattern is consistent with the POV character's established cognitive style (analytical fragment notation for a scholar, tactical absence-inventory for a soldier, sensory-first shorthand for a healer), it is a KEEP, not a KILL. The pattern must be inconsistent with the character to be a genuine violation.
  - **Internal monologue fragments**: Terse one-word or two-word fragments that read as the character's inner assessment ("Wise." / "Never." / "Too even.") are POV thought, not narrator seep. They only become a problem when the narrator is inserting a judgment the character would not make.
  - **Tactical or strategic compression**: Military or political characters compressing a situation into cause-and-effect shorthand ("Hearthglen was overwhelmed, and Stratholme was next") is appropriate register, not B2. Only flag compression that exceeds the character's demonstrated analytical capacity in the scene. This defense does not protect phantom concreteness: if the line sounds tactical while dodging the route behavior, object handling, or other visible carrier that would justify it, kill it.
  - **Concrete observations mislabeled as mood**: If the flagged scene-state declaration refers to something physically observable (soldiers' spacing, a room's temperature, audible silence), it is a concrete observation, not a mood label.
  - **Deliberate fragment pairs for cataloging**: Two or three fragments used for environmental scanning, security assessment, or tactical inventory are character voice doing a job. Do not flag them as F1 unless the prose sustains multi-paragraph monotony.
  - **Not a phantom-concreteness defense**: Analytical register, villain rhetoric, or scholar diction are not enough by themselves. Smart characters still need named specifics or visible evidence. If a line cannot answer "what specifically?" or "by what sign?", character voice does not save it.
- **Subject-matter defense**: If a flagged pattern is the literal subject of the scene (for example tissue retaining conditioning, wards carrying a defined magical behavior, or another named in-world mechanism), it is a KEEP. The guide is trying to catch metaphorical anthropomorphism, not accurate description of the chapter's own topic.
- **Dialogue defense**: Hedges, negations, fragments, and emotional labels inside quotation marks are often character voice. However, dialogue is not exempt when a guide explicitly audits the spoken line itself for sloganized abstraction, phantom concreteness, fake simplification, or other speech-level slop. If the quoted line hides behind prestige abstraction and cannot answer "what specifically?" from the local scene, it is a KILL. This defense also does not protect fake simplification: if one speaker asks for plainer speech, streets, smaller words, or the short version, the reply is being tested for usable payload, not just voice.
- **Intentional-structure defense**: If a flagged pleasantness bias or conflict collapse is an intentional plot beat where a character is deliberately being cooperative, seductive, or manipulative to draw the POV character deeper, it is a KEEP. Ask: is this ease earned by the scene's dynamics, or is the author defaulting to comfort?

Apply the filter actively:

- Every candidate that survives mechanical detection must be tested against these defenses.
- If a defense applies, flip the verdict to KEEP and explain which defense saved it.
- Do not suppress defended candidates. Record them in the scratchpad as KEEPs with the defense documented.

## Before moving to Phase 3

You should have:
- the relevant chapter plan read
- a concrete sense of POV register, subject matter, and scene intent
- the false-positive defenses ready to apply candidate by candidate
