# Phase 3: Audit Assigned Pass

This phase runs the guide loop for the current pass. Before auditing, read the route file that matches `pass`:

- pass `a` -> `references/3a-pass-a-guides.md`
- pass `b` -> `references/3b-pass-b-guides.md`

Use these audit-wide rules for every guide in the selected pass:

## Anti-laziness rules

1. Cite specific prose text in every finding. No vague scene-level references.
2. Execute each guide's self-check section.
3. Justify clean results. Zero-KILL guides still need a `cleanReason` explaining what candidates were examined and why they survived.
4. Re-read the guide before each guide audit.
5. Re-read the target prose before each guide audit.

## Scope rules

1. **Sentence-level findings only.** Every KILL cites the exact sentence or fragment to replace. Do not flag paragraph ranges or scene-level patterns.
2. **One pattern per finding.** If one sentence violates two guides, record two findings.
3. **The suggested fix must target the cited text.** When you later write suggestions, replace the exact cited sentence or fragment, not the surrounding paragraph.

## Per-guide audit loop

Create one ordered todo per guide in the selected pass:

**Audit: {guide filename}**

For each guide:

1. Read the guide file fresh.
2. Read the prose file fresh.
3. Execute the guide's detection procedure exactly as written:
   - follow the guide's own detection order
   - use the guide's own KEEP and KILL logic
   - use the guide's own finding format
   - include a `pattern` field in every finding; use the guide's pattern ID when provided, otherwise create a short descriptive label
   - run the guide's self-check section
   - apply the guide's own escalation rules
4. Apply the false-positive filter from Phase 2. If a defense applies, flip the candidate from KILL to KEEP and explain why.
5. Split the results into two artifacts in memory:
   - **Notes JSON**: KILL findings only, with guide filename, totalCandidates, kills, keeps, severity markers, dominant pattern, and the KILL findings array. Zero-KILL guides must include `cleanReason`.
   - **Scratchpad markdown**: KEEP findings only, with the full defense or keep rationale.

## Before moving to Phase 4

You should have:
- completed the common audit loop for every guide in the selected pass
- loaded the pass route that matches `pass`
- accumulated KILL findings for notes JSON and KEEP findings for the scratchpad
