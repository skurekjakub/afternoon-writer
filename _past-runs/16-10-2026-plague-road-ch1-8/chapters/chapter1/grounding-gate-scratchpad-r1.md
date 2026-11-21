# Grounding Gate Scratchpad: chapter1, iteration 1 (v2g-r1.md)

I swept v2g-r1.md fresh and diffed it against v2g.md. The revision changed exactly three lines: L251 (where the letter goes), L257 (cell blocking: "behind the chair") and L273 (the mage's turn toward the stone). The rest of the text is identical to v2g.md. I re-swept the whole chapter anyway, against D1 to D7, G1 to G12.

## Prior findings: verification

### G4-001 (cell-stone blocking). RESOLVED
- L257 now reads "Across from the door, behind the chair, a ward-stone ... at the height of a seated head". L265 (she is looking at Sylvanas in the doorway) and L279 (boots planted, facing out) put the chair facing the door, so the stone is directly behind her head.
- L273 "twisted round in the chair toward the ward-stone behind her head" / "twisted back to face Sylvanas" / "went round to the stone once more" matches that geometry.
- L275 (Sylvanas on the threshold), L291 (Sylvanas stops in front of the chair, and the mage tips her head back) and L293 ("The stone hummed in the wall") all agree. The closing image now has the stone humming behind the prisoner's head while Sylvanas stands over her, which is legible.

### G6-002 (compass error on the letter). RESOLVED
- L251: "a sharp letter from Silvermoon to Dalaran." This names the destination, and the direction no longer conflicts with L175 (Silvermoon lies north of the fork). Dalaran is sourced (locations/scholomance-and-dalaran.md, plans/kirin-tor-thread.md) and is already named at L245, so it adds no new proper noun.

## New KEEP decisions (iteration 1)

### K-r1-1. G11 / G4: "She frowned, a small crease between the brows, gone at once." (L273, after the twist)
- Risk checked: the revision turns the mage's face away from the doorway. Can Sylvanas still see a crease between the brows?
- Defense: the detail is still within what she can perceive. A seated person twisting round to look at something just behind her head ends in a three-quarter or profile view to someone in a doorway. The brow drawing down shows in profile. The cell is "barely wider than" the door, so the distance is a few feet, and the POV has a ranger's eyes. "Frowned harder, head cocked" on the second turn reads from any angle.
- Why it survived: a reader doesn't stumble here. The hound-at-a-rustle simile still lands. Recommendation for the human reviewer only: if a later pass wants it airtight, "a crease drawing down her brow" reads better in profile. Not a KILL.

### K-r1-2. G10: rhythm of the revised L273
- Risk checked: did "twisted round / twisted back / went round" lengthen the silent beat or make it read mechanically?
- Defense: the sentence count hasn't changed, and each turn still lands as its own short sentence. "Went round to the stone once more" is a little plain, but that's a style matter for the slop gates, not grounding damage.
- Why it survived: the cadence of the silent beat (Beat 9, no Jaina dialogue) is intact.

### K-r1-3. G9: "behind the chair" added to the cell description (L257)
- Risk checked: noun pile-up in an already itemised room description.
- Defense: it's two words, and they're load-bearing. They fix the spatial relation that the key beat depends on.
- Why it survived: it improves D1 without padding.

## Carried-forward KEEPs (re-checked, unchanged text)

The iteration-0 KEEPs K1 to K14 (see grounding-gate-scratchpad.md) cover text that is byte-identical in v2g-r1.md. I re-read each passage, and every defense still applies:
- K1 Eversong blossom (L17)
- K2 fine-boned head (L51)
- K3 Sunfury Spire (L35)
- K4 to K6 dialogue runs in Scene 1 (L25-L53, L73-L89, L95-L115, L125-L173): embodiment recurs inside the runs.
- K7 Cyndia's report (L197-L217): room established, hand near the quiver, closed and opened palm. The short-line tail is under 6 lines.
- K8 rack and satchel inventory (L219-L221): the POV is reading evidence, not a lore dump.
- K9 to K12 minor sourced or inferred specifics (violet-drying ink, lord admiral's daughter, split cap, horses bred for speed). These are flagged as inferred, not quoted from source.
- K13 interior deliberation (L281-L287)
- K14 final pressure beat (L289-L295)

## Distribution by thirds (re-checked)

- Opening (L3-L93): strong. Bracken, ferns, the ash and the boulder, the knife, the mare, moss and gold runes on the stone, the glove.
- Middle (L95-L193): strong. The runner's lathered horse, the fist with cold in it, the fork, the switchbacks, the gate bar, Cyndia's quiver strap.
- Final (L195-L295): the densest third. Stew skin, the damper plate, the ash staff, the map's thumbprint, the file turned a quarter round, the pegs, the stone behind the chair, frost-nip, a cup set down. No G7.

## Verdict

PASS. Both iteration-0 KILLs are resolved, the revision introduced no new violations, and the fresh full-chapter sweep found no G1-G12 KILLs.
