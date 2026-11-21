# Grounding Gate Scratchpad: chapter4, iteration 0 (v2g.md)

Verdict: FAIL with 2 KILLs (G12-001 MODERATE at line 5, G9-002 MILD at line 970). Both are in sentences the grounder added. The rest of the chapter, including the v2 prose it kept, holds up under a fresh sweep.

I diffed v2.md against v2g.md. There are six grounder edits, at lines 5, 45, 141, 692 and 970, plus a paragraph break before 47. Then I swept the whole chapter fresh.

## KEEP decisions

### Scene grounding sweep (D1/D2/D4)

- **G1/G4, lane standoff (49-117).** Excerpt: "His hands on the ash shaft were brown and cracked across the knuckles..." Defense: the staging is explicit. The spear lies across the lane between a wall and a water butt, Sylvanas walks up until the shaft lies across her coat, and the pump, the egg stall and the herring barrel all serve as reaction points. It survives because every body has a position and the tension sits in the thumb on the ash.
- **G1, chapel interior (143-147).** Excerpt: "cots, a box bed with its doors taken off, a child's truckle bed with an old man on it..." Defense: dense materials that also carry social meaning (each family sends its own bedding). This is not noun spam because each object comes back later as a place (door-bed, truckle bed, box bed).
- **G1, staff reads (185-239).** The ash, the crystal, the cheek against the wood and the brown-ink image. Defense: the magic always has a physical carrier, and the cost shows up as cold in her teeth and hand.
- **G2/G6, horseshoe over the lintel (45).** Grounder addition. Source: world/culture.md and culture.json (Ch3), where humans nail a horseshoe over the lintel with the points down. It survives because it is sourced, it is a single clause inside an existing list, and it is quietly ironic over a barred sick-house. A port-raised outsider like Jaina would plausibly notice it.
- **G2, mares at the yard rail (141).** Grounder addition: "where they stood with their heads high and their nostrils working at the smell". Defense: this matches Ch3's established horse response to contamination (the mare backs and pins her ears at Millhaven). It is short, sourced, and fits the POV as she walks in.
- **G12, "foreign script" (692).** The grounder swapped it in for the unsourced "Zandalari". This is a slightly generic noun, but that is the right trade. A cargo tag in a Kul Tiran warehouse needs no named script, and naming one would create new G12 risk.
- **G6/G12, Boralus mill fire (642), Tiragarde reefs (696), Boralus cathedral reliquary (726), Kul Tiran gunners' breeching ropes (323).** These were in v2 already. Jaina is Kul Tiran (jaina.md), Tiragarde appears in dagny-voice.md, and Boralus is canon for her home port. Defense: POV-bound home-world analogies, each a single clause, none of them lore spill. Low canon risk.
- **G6, village and institution names (Joss, Hob, Nan, Piers, Aldon boys, Hallams, Mother Haw, Cooper's Lane, Chapel Lane).** Writer-local names for an unnamed village (the plan keeps the village unnamed). Defense: small-scale local naming that the plan's freedom allows. No canon collision.
- **G2/G12, Andorhal stencil (982-988).** The plan (B11a continuityNote) requires an in-world source for Andorhal. The stencilled sacking plus Brask's grain-road knowledge meets that requirement exactly.
- **G7, final third (590-1026).** The granary, the loft, the lamp on its bail, the jar, the frost, the shell, the cage, the key, the torch, the yard fire through the bubbled glass, rain on the roof, the ledger with its ink horn, and the grain-road ruts. The tail is denser than the opening. There is no generic drift at the exit: the staff leans toward the ruts, and the road is named.
- **G5, Jaina's reasoning passages (255, 379, 467, 487, 878).** These are abstract thinking, but each one is tied to a carrier (the jug, Tobin's slate, the doorframe flour, the staff across her knees). They survive because the thinking is the scene's work and it never floats free of an object.

### Dialogue grounding sweep (D3)

- **G3, lane standoff run (67-99).** Thumb on ash (75, 79, 97), the boy moved back by elbow (83), heads turned to the pump and the stall (89). Embodiment recurs inside the run.
- **G3, Tobin runs (149-165, 241-271).** Basin, apron, the slopped basin set down hard, the jug and its glaze. Embodied throughout.
- **G3, diet round (399-427).** Spoon, bowl, the elbow in the box bed, Hew's thumb over his wife's knuckles, Col's open shirt. Each speaker is placed in a bed. This passes.
- **G3, the join run (533-570). The closest call.** Excerpt: "Cyndia reported standing, weight even." From the grey glove at 531 to the brazier tick at 568, the chapel's cots and sick vanish from the page. Embodiment inside the run: Jaina looks at the grey glove instead of speaking (535), Cyndia's posture (547), Ellen's loaf carried up to Garran's cottage (549), Sylvanas's mouth (553), Neral's collar at Millhaven (559). Then a hard landing on the brazier, Garran's breath and the silver wire printed through her bodice (568), followed by the hand on the bowstring (570). Fewer than 12 spoken lines, with at least two meaningful beats inside the run. Defense: deliberate stillness for a report beat, with the physical counterweight landing exactly on "On purpose". It survives, narrowly. If a later revision lengthens this run, it needs another chapel beat in the middle.
- **G3, loft and Tam (724-750).** Torch, the lamp taken off the sack, the blue shell, the stair. Embodied.
- **G3, cage interrogation (770-790).** Cold bars on her face, the staff light over the straw, the foam, the key. Embodied.
- **G3/G4, shutdown negotiation (822-862).** The torch held low and lit from below, the thumb stopping on the handle, Brask turning in the cage door to give named orders. This is the strongest echo of the spear scene, well staged.
- **G3, Sylvanas at the threshold (908-922).** Doorframe, the glow of the yard behind her, the smell of scorched flour. Short run, anchored.
- **G3, ledger (974-1010).** Book against the chest, ink horn on a cord, the stopper spat into his hand, spelling aloud. Embodied.

### Over-grounding sweep (G8/G9/G10)

- **G8.** No lore spill. The death-currents passage (696) stays inside Jaina's memory (the locked shelf, the grille) and is not exposition.
- **G10.** The paragraph break before "Then the horses stopped." (47) helps the rhythm and is kept.
- **Non-grounding observation (not a KILL).** At 563-564, "...with its barley rotted in the field." and "\"Somebody is selling it to them,\"" have no blank line between them. This is a formatting glitch carried over from v2. It is worth fixing during the revision pass while that region is being touched.
