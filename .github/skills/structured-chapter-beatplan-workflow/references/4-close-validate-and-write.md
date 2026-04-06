# Phase 4: Close, Validate, and Write

This phase locks the handoff, reviews the beatplan, validates the structure, and writes the file.

## Write the chapter close exactly

Use:

```markdown
---

## Chapter close / handoff

**Active cast at close**
- ...

**Facts locked for Chapter {N+1}**
- ...

**Facts not yet earned**
- ...
```

This section is where continuity gets pinned down.

- `Active cast at close` prevents next-chapter roster drift
- `Facts locked for Chapter {N+1}` states what the following chapter may safely inherit
- `Facts not yet earned` protects against premature reveals and overconfident downstream writing
- The top-of-file exit-knowledge summary should agree with this section; if these diverge, the close section wins and the summary must be corrected
- If a locked fact depends on a specific speaker, fragmentary carrier, or crumb-level namedrop, the relevant beat must encode that provenance and the close must not upgrade it into ambient setting knowledge

## Review with the user before writing

Walk the user through the assembled beatplan and ask about:

- pacing balance
- missing scenes
- dead weight
- character-arc movement
- information-order integrity
- closing-hook strength
- beats to reorder, expand, or cut

Iterate until the user is satisfied.

## Validation checklist

Before writing, verify all of these:

- [ ] The chapter has the normalized header block
- [ ] `## Meta info` exists and uses repo-root-relative links
- [ ] The POV knowledge ledger is present and logically ordered
- [ ] The chapter-exit knowledge summary is present and agrees with the close/handoff facts
- [ ] `## Arc position` exists
- [ ] `## Cast and handoff rules` exists
- [ ] Every scene has `Scene function`, `Cast in scene`, and `Knowledge at scene start`
- [ ] Every beat has typed fields plus value shift, new info, still unknown, sensory anchors, and transition intent
- [ ] Source-sensitive reveal beats include `Disclosure provenance`, and no downstream fact outruns that provenance
- [ ] No fact appears in `What {POV} knows at open` before being earned in prior continuity
- [ ] Open cast and close cast are both explicit
- [ ] The chapter close locks the next chapter correctly
- [ ] No three consecutive value shifts run the same direction
- [ ] Try-fail outcomes escalate instead of flattening
- [ ] The opening drops the reader into a live situation, not abstract exposition
- [ ] The closing hook creates forward pressure without introducing an unseeded random element

## Writing the file

Follow the caller's output path.

Typical defaults:

- outline-builder default: `.afternoon/outlines/{chapterId}.md`
- story-local refinement workflows may target a story-specific chapter-plan directory instead

Before writing large files, read `.github/skills/large-file-handling/SKILL.md`.

Use sectioned writes:

1. Create the file with the chapter header and opening sections
2. Append scene blocks in order
3. Append `## Chapter close / handoff`
4. Verify the file exists and is complete

Do not use bash heredocs for long markdown artifacts.

## Before completing the workflow

You should have:

- A structurally valid chapter beatplan in the normalized schema
- User-reviewed scene order and hook placement
- Explicit open-state and handoff continuity locks
- The finished file written to the requested path
