# Adding a New Agent

How to add a new agent to the afternoon pipeline.

## Step 1: Create the Agent File

Create `.github/agents/afternoon-{name}.agent.md` with this structure:

```markdown
---
description: "One-line description of what this agent does in the pipeline."
model: gpt-5.4
tools:            # only if the agent needs web access
  - web_search
  - web_fetch
---

# Afternoon {Name}

{What this agent does, in 2-3 sentences. Who dispatches it. What it produces.}

## Startup Sequence

When dispatched with `chapterId: {chapterId}`:

1. Read `.afternoon/config.json` for project settings
2. {Read whatever inputs this agent needs — list each file/directory explicitly}

## Work Process: Todolist-Driven {Verb}

You work in **structured passes**, tracked via the todolist tool with todo-dependencies.

Create these todos in order, with each depending on the previous:

1. **Read inputs** — {list what to read}
2. **{Main work step 1}** — {description}
3. **{Main work step 2}** — {description}
4. **Write output** — {what to write + status.json}

Process one todo at a time. Mark in-progress before starting, mark done when complete, query for the next ready todo.

## {Main sections describing the agent's work}

{Detailed instructions for each phase of work}

## Output

Write {output file} to `.afternoon/{path}`.

Then write `.afternoon/agents/{name}/status.json`:

\```json
{
  "agent": "{name}",
  "chapterId": "{chapterId}",
  "status": "completed",
  "artifacts": [".afternoon/{path-to-output}"],
  "summary": "{brief description of what was done}"
}
\```

If you cannot complete, write status.json with `"status": "failed"`.
```

## Step 2: Register the Agent Directory

Add the agent's status directory to the `.afternoon/agents/` structure:

```bash
mkdir -p .afternoon/agents/{name}
```

## Step 3: Insert Into Orchestrator Dispatch Chain

Edit `.github/agents/afternoon-orchestrator.agent.md`:

1. **Update the pipeline diagram** (near top of file) to show the new agent in the correct position
2. **Add a dispatch section** following the pattern of existing dispatches:
   - Check status.json for this agent (skip if already completed for this chapterId)
   - Dispatch with `agent_type: "afternoon-{name}"` and `prompt: "chapterId: {chapterId}"`
   - Wait for completion
   - Read status.json
   - Retry once on failure
3. **Update manifest tracking** if the new agent changes what `currentAgent` values are valid

## Step 4: Verify Cross-Agent Consistency

Check that:

1. **Input availability:** Does the agent's input exist by the time it's dispatched? (e.g., if it reads v2.md, it must run after slophunter)
2. **Output consumers:** Does any downstream agent need this agent's output? If so, verify they read it.
3. **Memory interaction:** If the agent reads memory files, does it use the targeted `requiredMemory` pattern (writer/style-editor) or the full-read pattern (planner/verifier)?
4. **Status.json contract:** The orchestrator expects `"status": "completed"` or `"status": "failed"` with the correct `chapterId`.

## Step 5: Update Supporting Files

1. **This skill's references:** Update `references/agents.md` with the new agent's contract
2. **architecture.md:** Update the pipeline diagram and data flow
3. **start script:** If the new agent changes pre-flight requirements, update `afternoon-start.sh`

## Patterns to Follow

### Todolist-driven workflow
Every agent uses the todolist tool with todo-dependencies. Create all todos upfront with dependencies, process one at a time.

### Internet research step
All agents have a "Research keywords" todo that internet-searches character/location/world terms from the chapter. Add this to new agents if they work with prose content.

### Status.json contract
Every agent writes status.json on completion or failure. The orchestrator uses this as the sole signal — never output file existence.

### Memory file access patterns
- **Full read:** Planner and plan-verifier read ALL memory files (they annotate continuity)
- **Targeted read:** Writer and style-editor read ONLY what `requiredMemory` specifies
- **No read:** Slophunter doesn't read memory files (works purely on prose patterns)
- **Write:** Only the memory-keeper writes memory files

## Where to Insert in the Pipeline

Common insertion points:

| Position | After | Before | Use case |
|----------|-------|--------|----------|
| After plan-verifier | plan-verifier | writer | Additional plan processing (e.g., scene library mining) |
| After slophunter | slophunter/slop-gate | grounder | Additional prose processing (e.g., dialogue enrichment) |
| After grounder | grounder | expander | Additional world-building passes |
| After expander | expander | style-editor | Additional quality gates (e.g., AI detection, beta reader simulation) |
| After style-editor | style-editor | memory-keeper | Post-editing quality gates |
| After memory-keeper | memory-keeper | (end) | Post-chapter analysis (e.g., metrics, reports) |
