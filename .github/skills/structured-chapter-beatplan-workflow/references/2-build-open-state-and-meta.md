# Phase 2: Build Open State and Meta

This phase writes the chapter scaffold before any scene work begins.

## Write the chapter header exactly first

Use this normalized opening shape:

```markdown
# Chapter {N}: {Title}

**POV:** {character} (limited third, absolute)
**Timeline position:** {where this chapter sits relative to the prior one}
**Open location:** {specific place at chapter open}
**Transport:** {how the cast is moving or not moving}
**Active cast at open:** {named list}
**Immediate objective:** {what the POV is trying to accomplish right now}

## Meta info

- **Worldbuilding references:** [Doc name](repo/root/path.md), ...
- **Character references:** [Profile](repo/root/path.md), [Voice sheet](repo/root/path.md), ...
```

Keep the links repo-root relative. Do not use local `../` paths in this schema.

## Write the knowledge ledger

Immediately after the `## Meta info` block, write:

```markdown
**What {POV} knows at open**
- ...

**What {POV} does NOT know at open**
- ...

**Must not be implied yet**
- ...

**What the cast knows leaving the chapter**
- ...
```

Rules:

- `knows at open` contains only facts already earned on-page or already established before the story starts
- `does NOT know` captures unresolved questions that drive the chapter
- `must not be implied yet` guards against accidental spoiler drift, metagaming, or premature certainty
- `what the cast knows leaving the chapter` is a compact exit-state summary for quick information-flow review; it should restate the chapter's most important earned knowledge gains in 3-6 bullets and stay aligned with the close/handoff facts below
- source-sensitive reveals still need beat-level provenance in Phase 3; do not rely on the top knowledge ledger alone when the speaker or carrier matters

If a fact is not yet earned, it belongs in `does NOT know` or `must not be implied yet`, not in `knows at open`.
If the cast could not safely leave the chapter knowing it, it does not belong in the exit summary.

## Write `## Arc position`

This section tells downstream agents what the chapter is testing and how the POV's current stance behaves under pressure.

Story-level arc canon belongs in the story overview and character references. Keep the stable character material there:

- core misbelief
- growth truth
- core pursuit
- underlying need

In the chapter outline, translate that material into chapter-operational fields that tell the writer what this chapter actually pressures.

Typical pattern:

```markdown
## Arc position

### {POV}
- **Current stance at open:** ...
- **Surface objective:** ...
- **Pressure source:** ...
- **Misbelief manifestation:** ...
- **Chapter test:** ...
- **Forced choice:** ...
- **End-state shift:** ...
- **Carry-forward residue:** ...

### {Key character} through {POV}'s POV
- **Visible function:** ...
- **POV misread at open:** ...
- **Correction earned here:** ...
- **Interaction rule:** ...

### Partnership / team
- **Operating mode at open:** ...
- **Operational change this chapter:** ...
- **Naming/attitude rule:** ...
- **Do-not-overstate rule:** ...
```

Use only the subsections this chapter actually needs, but the arc section must explain:

- what stance the POV is actively operating from at chapter open
- what external pressure makes that stance costly
- how the stance shows up in observable behavior
- what choice or recalibration the chapter forces
- what shift the next chapter should inherit

If a relationship or register shift matters, encode it here instead of leaving it implicit.
Do not restate abstract story-theory labels here unless the label itself is load-bearing on-page; translate them into chapter-operational pressure.

## Write `## Cast and handoff rules`

This section prevents roster drift and transition mistakes.

Use:

```markdown
## Cast and handoff rules

- **{Character}:** {what this character does in the chapter and any restrictions on use}
- ...

**Chapter handoff target:** {what the next chapter should inherit}
```

This is where you lock:

- who exits during or after the chapter
- who remains active
- who may plausibly be sent away, killed, or handed off
- what the next chapter should open with

If a character disappears after this chapter, say so here. If the next chapter inherits the same riding party, say so here.

## Before moving to Phase 3

You should have:

- The full header and `## Meta info` block
- A clean knowledge ledger with no future facts leaked upward
- A compact and accurate chapter-exit knowledge summary
- The arc-position section
- The cast / handoff rules section
- A stable answer to what the chapter opens with and what the next chapter must inherit
