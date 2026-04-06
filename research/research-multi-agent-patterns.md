# Multi-Agent Quality Pipeline Patterns for Prose

## Summary
Multi-agent editorial pipelines follow a Generator → Auditor → Reviser convergence loop pattern. The key insight from production systems: specialized agents outperform single monolithic agents, and bounded retry mechanisms prevent infinite loops while ensuring quality convergence.

## Pattern: Generator → Auditor → Reviser Loop

### Core Architecture
```
Generator (writes/edits prose)
    ↓
Auditor (reads prose, identifies violations, suggests fixes)
    ↓
Decision Gate: Pass → proceed | Fail → loop back
    ↓
Reviser (applies auditor's suggestions, re-writes)
    ↓
Auditor (re-audits revised version)
    ↓
Repeat until pass OR max iterations exhausted
```

### Why Three Agents Instead of One
From production experience (Multi-Agent Content Pipeline, Lee 2025):
- Single agent approach failed because "prompt complexity became unmanageable"
- Impossible to optimize for different subtasks (generation ≠ auditing ≠ revision)
- Error attribution was nearly impossible with one agent
- Revision process unreliable when same agent writes AND evaluates

### Bounded Retry Mechanism
Every production system implements max iterations to prevent infinite loops:
- **BidGenie Quality Pipeline**: Score against rubric, iterate with targeted feedback, 3-pass maximum
- **Google ADK Story Pipeline**: LoopAgent performs Critic → Refiner cycles, bounded iterations
- **Afternoon Pipeline Slop-Gate**: Up to 5 iterations, graceful degradation on exhaustion

### Convergence Strategies When Loop Doesn't Converge
When kill counts plateau or oscillate:
1. **Deletion-first**: Remove problematic content rather than trying to fix it creatively
2. **Minimal substitution**: Replace with simplest possible alternative
3. **Promote anyway**: Accept the best revision and continue (graceful degradation)
4. **Flag for human**: Mark chapter as needing human attention

### Key Lessons from the Afternoon Pipeline's Slop-Gate

The existing slop-gate implementation is a clean model:
- Gate NEVER directly edits prose — it audits and suggests
- Suggestions include concrete replacement text (not just "fix this")
- Each suggestion is cross-validated against ALL guides to prevent fixes introducing new problems
- Iteration-aware strategy: early iterations allow creative rewrites; later iterations prefer deletion
- On exhaustion: promote last revision, log warning, continue pipeline (don't block)

## Pattern: Fresh-Eye Principle

### Why the Auditor Must Be a Separate Agent
The auditor (gate) cannot share context with the generator:
- The generator knows WHY it made each choice, which creates blind spots
- The auditor approaches with "fresh eyes" — evaluating outcome, not intent
- If auditor reads generator's notes, it may rationalize the same failures

### Application to Grounding Gate
- Grounding gate should NOT read grounder-notes.json (the grounder's self-report)
- Gate should read only: the prose, the plan, the materials, and the rubric
- This prevents the gate from being biased by the grounder's explanations of its choices

## Pattern: Diagnostic Routing

### Scene-Type Awareness
Different content types need different audit criteria:
- Action scenes: check geometry, material, impact chains
- Dialogue scenes: check floating heads, environment persistence, action beats
- Travel scenes: check route, bodily wear, terrain, ecology
- Intimate scenes: check moment-by-moment progression, sensory rotation

### Implementation
The gate's rubric can be augmented with scene-type-specific checks:
- Read the plan to determine scene types
- Apply the appropriate packet's verification questions
- Weight violations by scene type (bloat in an action scene is worse than in exposition)

## Pattern: Per-Chunk Processing with Reassembly

### The Chunking Approach for Prose Quality
From hallucination research: quality improves dramatically when processing smaller coherent chunks instead of whole documents.

Applied to prose grounding:
- Extract scenes from the chapter using plan boundary markers
- Process each scene independently with full priming
- Reassemble and verify transitions at seams
- Gate audits the full reassembled document

### Handling Cross-Chunk Continuity
- Provide bridge context: last paragraphs of previous chunk + first paragraph of next chunk
- Use consistent terminology register across chunks (loaded from the same materials for each)
- Stitching pass validates:
  - Location names consistent across scenes
  - Character physical state carries forward (wounds, clothing, fatigue)
  - Grounding register doesn't shift abruptly at scene boundaries
  - Transition paragraphs don't get double-grounded or under-grounded

## Sources
- Lee, "Building a Multi-Agent Content Creation Pipeline: Lessons from Production" (Medium, 2025)
- BidGenie Engineering Blog, "The AI Proposal Quality Pipeline" (2026)
- Google ADK Multi-Agent Story Pipeline (GitHub, Arjun1443, 2025)
- Vatsa, "Managing LLM Hallucinations in Long Document Processing" (Medium, 2025)
- WriteBros, "How to Humanize Long AI-Generated Content: 15 Scalable Techniques" (2026)
