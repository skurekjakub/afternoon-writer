# Phase 1: Read Context and Sources

This phase establishes what the chapter is, where it sits, and which source files deserve to be linked inside the plan.

## Read the chapter context first

Before touching the schema, read the materials that establish the chapter's continuity and job:

1. The story overview / long-arc summary
2. The current chapter draft if you are refining an existing plan
3. The immediately previous and next chapter plans if handoff or transition continuity matters
4. Relevant materials / world docs / faction notes / setting references
5. Relevant character profiles
6. Relevant voice sheets
7. Existing memory or continuity artifacts if the current workflow uses them
8. User-specified hard requirements, scene wants, exclusions, and withheld information

If this is a refinement pass on an existing plan, treat the current plan as source material to normalize rather than something to casually overwrite. Preserve established canon unless the user explicitly changes it.

## Decide which links belong in `## Meta info`

The `## Meta info` section is for the load-bearing references the next agent actually needs.

### Worldbuilding references

Link the location, world, faction, or mount docs that actively shape the chapter.

Good worldbuilding links:

- the chapter's main location reference
- travel / transport docs if movement matters
- special setting packets that explain a key cultural or magical element

Do not dump every world file in the repo. Link the ones that matter for this chapter.

### Character references

At minimum, link:

- the POV character's profile
- the POV character's voice sheet (if one exists)

Then link the other load-bearing references:

- co-lead profile + voice sheet if the co-lead meaningfully shapes the chapter
- key supporting-character profile(s)
- a supporting compendium file when secondary characters do not have standalone profiles

Use repo-root-relative markdown links:

- `stories/the-plague-road/characters/jaina.md`
- `stories/the-plague-road/characters/voice-sheets/jaina-voice.md`

## Decide what continuity must be locked up front

Before moving on, be able to answer:

- Who is physically present at chapter open?
- What does the POV concretely know at chapter open?
- What does the POV not know yet?
- What facts must not be implied before they are earned?
- Which characters or clues are being handed in from the previous chapter?
- Which characters, clues, or route choices must be carried into the next one?

If you cannot answer those questions, keep reading before you start the schema.

## Before moving to Phase 2

You should have:

- The small set of worldbuilding links that belong in this chapter's `## Meta info`
- The profile / voice-sheet links that belong in `## Meta info`
- A clear map of the POV's knowledge state at chapter open
- The active cast at chapter open and the intended handoff state at chapter close
