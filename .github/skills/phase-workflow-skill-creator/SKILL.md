---
name: phase-workflow-skill-creator
description: "Create a dedicated workflow skill for an agent — decompose a monolithic agent prompt into a router SKILL.md with per-phase reference files that enable progressive context disclosure. Use this skill whenever an agent file is too large, an agent prompt contains inline domain knowledge that should be externalized, you need to create a phase-based workflow skill for any agent, or the agent's context window is wasted on instructions it doesn't need yet. Also triggers on: 'this agent is too fat', 'decompose this agent into phases', 'create a workflow skill', 'the agent prompt is too long', 'externalize the domain knowledge', 'progressive disclosure for agent context', 'make a router skill for this agent', 'split agent into phases', 'the agent loads too much at once', or any request to restructure a monolithic agent prompt into a phased skill with reference files."
---

# Agent Workflow Skill Creator

Agent prompts grow organically — schemas get pasted in, domain tables accumulate, negative exemplars pile up. Eventually the agent file is 300+ lines and the model wastes context window on content it doesn't need for its current phase. The fix is structural: extract the domain-heavy content into a **workflow skill** where each phase gets a reference file, and the agent reads only the phase it's currently executing.

This skill walks you through the full decomposition: audit the agent file, identify phase boundaries, create the router skill with reference files, slim the agent prompt, and verify nothing was lost.

## The Pattern

A workflow skill has this structure:

```
.github/skills/<agent-name>-workflow/
├── SKILL.md              ← Router: phase table + how-to-use (small, always loaded)
└── references/
    ├── 1-read-workspace.md   ← Phase 1 domain content (loaded only during Phase 1)
    ├── 2-do-work.md          ← Phase 2 domain content
    ├── 3-produce-output.md   ← Phase 3 domain content
    └── ...
```

The agent file itself becomes thin: role definition, skill mount (pointing to the workflow skill), I/O contract, and hard constraints. Everything else lives in the reference files.

**Why this works:** The agent reads the router SKILL.md at invocation start (~20 lines). It sees a phase table telling it which reference file to read. It reads only the reference for its current phase. When it finishes that phase, it goes back to the router and reads the next reference. At no point does it load all domain content simultaneously.

## Procedure

### Step 1: Audit the Agent File

Read the agent file end-to-end. Identify these categories of content:

**Always-loaded content** (stays in the agent file):
- Role definition (1–3 sentences: what the agent is and isn't)
- Identity constraints (e.g., "you never write prose, only plans")
- Hard rules that apply to ALL phases (e.g., "no male characters in explicit scenes")
- I/O contract (inputs table, output paths)
- Cross-cutting directives (3–5 bullet summary, not full explanations)

**Phase-specific content** (moves to reference files):
- File reading lists / ingestion instructions → Phase 1 (Read Workspace)
- Domain tables (beat density, scoring criteria, scene type definitions)
- Schemas (JSON output formats, file templates)
- Validation checklists
- Negative/positive exemplars
- Detailed multi-step procedures
- Composition principles, creative directives with full explanation

**Heuristic for what moves:** If a section is >15 lines and is only relevant during one phase of the agent's work, it belongs in a reference file.

### Step 2: Identify Phase Boundaries

Almost every agent follows this natural phase structure:

1. **Read Workspace** — ingest skills, read context files, load state
2. **Core Work Phase(s)** — the agent's actual job (1–3 phases depending on complexity)
3. **Produce Output** — write artifacts, update status files

Break the core work into phases based on natural sequential boundaries — points where the agent finishes one kind of work and starts another. Look for:
- Shifts in what the agent reads vs writes
- "Before moving to..." or "Do not proceed until..." language
- Distinct output artifacts (constraint checklist → creative palette → final output)
- Changes in the agent's cognitive mode (divergent retrieval → convergent synthesis → validation)

**Typical phase counts:**
- Simple agents (context-scout, memory-keeper): 2–3 phases
- Medium agents (scene-miner, blueprint-composer): 4 phases
- Complex agents (guide, prose-writer): 4–5 phases

Don't over-decompose. If two sections are always read together and never independently, they're one phase. The test: would the agent ever need Section A without Section B? If not, they're the same phase.

### Step 3: Create the Workflow Skill Directory

```bash
mkdir -p .github/skills/<agent-name>-workflow/references/
```

### Step 4: Write the Router SKILL.md

The router is small and structural. It has three parts:

**1. Frontmatter:**
```yaml
---
name: <agent-name>-workflow
description: "Sequential workflow for the <agent-name> agent. Covers: <phase 1 summary> → <phase 2 summary> → ... → <phase N summary>. Read this skill at the start of every invocation and follow phases in order."
---
```

**2. Phase table:**
```markdown
# <Agent Name> Workflow

This skill routes you through the <task> pipeline phase by phase. Read the reference file for your current phase — each contains full instructions and domain knowledge.

| Phase | Reference file | Summary |
|-------|---------------|---------|
| 1. Read Workspace | `references/1-read-workspace.md` | Ingest skills, context, state files |
| 2. <Core Phase> | `references/2-<name>.md` | <1-line summary> |
| 3. <Core Phase> | `references/3-<name>.md` | <1-line summary> |
| 4. Produce Output | `references/4-<name>.md` | Write artifacts, update status |
```

**3. How to use:**
```markdown
## How to use

1. Start at Phase 1. Read its reference file.
2. Complete the phase.
3. Move to the next phase. Read its reference file.
4. Repeat until the final phase is complete.
```

The router should be under 30 lines (excluding frontmatter). Its job is navigation, not instruction.

### Step 5: Write Reference Files

For each phase, create `references/<N>-<name>.md`. Each reference file:

**Starts with an H1** matching the phase name:
```markdown
# Phase N: <Name>
```

**Contains the full domain content** for that phase — tables, schemas, procedures, exemplars, checklists. Don't summarize; move the content wholesale from the agent file. The whole point is that this content is detailed but only loaded when needed.

**Ends with a transition gate:**
```markdown
## Before moving to Phase N+1

You should have:
- <concrete deliverable or state the agent should have produced>
- <another deliverable>
```

The transition gate tells the agent what it should have accomplished before proceeding. This prevents the agent from skipping ahead before finishing the current phase's work.

**Reference file naming convention:**
- Number prefix for sort order: `1-`, `2-`, `3-`...
- Kebab-case descriptive name: `read-workspace`, `build-outlines`, `palette-assembly`
- Always `.md`

**What goes where — content routing guide:**

| Content type | Goes in... | Reason |
|---|---|---|
| File reading lists, mandatory reads tables | Phase 1 reference | Only needed at start |
| Domain tables (scoring, beat density, scene types) | The phase that uses them | Loaded just-in-time |
| JSON output schemas | The output/final phase reference | Only needed when writing |
| Validation checklists | The phase before output (or output phase) | Gate before writing |
| Negative/positive exemplars | The phase where the mistake could happen | Immediate reinforcement |
| Composition principles, creative rules | The core work phase that applies them | Loaded during creative work |
| Inter-agent contracts (what upstream/downstream expects) | Phase 1 or the I/O phase | Context for reading/writing |

### Step 6: Slim the Agent File

Rewrite the agent file to contain only:

1. **Frontmatter** — unchanged (name, description, model, etc.)
2. **Role** — 1–3 sentences defining what the agent is and isn't
3. **Identity constraints** — hard rules that apply universally (keep these in the agent file because they override everything)
4. **Skill mount** — point to the workflow skill with a brief phase summary:
   ```markdown
   ## Your task and instructions

   Read the **`<agent-name>-workflow`** skill at the start of every invocation.
   It routes you through the N-phase pipeline:

   1. **Phase Name** — 1-line summary
   2. **Phase Name** — 1-line summary
   ...

   Each phase has a reference file with detailed instructions.
   Read the reference file for each phase before doing that phase's work.
   ```
5. **I/O contract** — inputs table and output paths (brief, no schemas)
6. **Cross-cutting directives** — 3–5 bullet summary of principles that span all phases. These are reminders, not full explanations — the full versions live in the reference files.

**Target size:** The slimmed agent file should be 30–60 lines. If it's over 80, you probably left domain content that belongs in a reference file.

### Step 7: Verify Completeness

Diff check — make sure nothing was lost:

1. Read the original agent file (from git or your memory of it)
2. Read the slimmed agent file + all reference files
3. Verify every substantive instruction from the original appears in exactly one place:
   - In the agent file (always-loaded), OR
   - In a reference file (phase-loaded)
4. Check for duplicated content — the same instruction should not appear in both the agent file and a reference file. The agent file may have a brief summary; the reference has the full version.

### Step 8: Update Cross-References

Search for references to the agent file in:
- Documentation (e.g., `docs/` directory)
- Augmentation/family skills that list agent files and their capabilities
- Other agent files that dispatch to this agent

Add the workflow skill name alongside the agent file reference. The agent file is still the agent's identity; the workflow skill is where its detailed instructions live.

## Checklist

Use this to track progress during decomposition:

- [ ] Audit: categorized all content as always-loaded vs phase-specific
- [ ] Phases: identified 3–5 natural phase boundaries
- [ ] Directory: created `.github/skills/<agent-name>-workflow/references/`
- [ ] Router: wrote SKILL.md with phase table (<30 lines)
- [ ] References: wrote one reference file per phase with full domain content
- [ ] Transitions: every reference file ends with a "Before moving to" gate
- [ ] Agent file: slimmed to 30–60 lines (role + skill mount + I/O + hard rules)
- [ ] Completeness: every instruction from the original exists in exactly one place
- [ ] No duplication: content isn't repeated between agent file and reference files
- [ ] Cross-references: docs and family skills updated with workflow skill name

## Common Mistakes

- **Over-decomposing.** Creating 8 phases for a simple agent. If the agent's work has 2 natural stages, use 2 phases + a read-workspace phase. Don't manufacture phases.
- **Under-extracting.** Leaving a 20-line schema in the agent file "because it's important." Important doesn't mean always-needed. If it's only used during the output phase, move it to the output phase reference.
- **Duplicating content in the agent file and reference files.** The agent file gets a brief summary ("it routes you through 4 phases"). The reference file gets the full instructions. Don't put the full instructions in both places.
- **Missing the transition gates.** Without "Before moving to Phase N+1" sections, the agent blasts through phases without verifying it completed each one. The gates are structural pacing — they prevent skipping.
- **Vague phase summaries in the router.** The phase table summary column should be specific enough that the agent knows which phase to read for its current work. "Do the work" is useless; "4-lens retrieval + internet location research" tells the agent exactly what's in that reference file.
- **Forgetting to update the agent file's skill mount section.** The agent must explicitly name the workflow skill and list the phases briefly. Without this, the agent doesn't know to read the skill.
- **Missing large artifact handling in the output phase.** If the agent produces artifacts >5KB (prose, plans, inventories, memory files), the output phase reference must include bash heredoc append instructions. Without this, the agent will attempt a single `create` call and timeout. See `agent-as-function/references/large-artifact-handling.md` for the pattern.
