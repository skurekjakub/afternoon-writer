

## No Backward Compatibility

When refactoring or removing a concept from the codebase, delete it completely. Never leave behind annotations, comments, "REMOVED" markers, "formerly X" notes, or any other backward-compatibility breadcrumbs. The old concept should vanish as if it never existed. Only preserve backward compatibility if the user explicitly asks for it.

## No Git

Never interact with git. No `git status`, `git diff`, `git stash`, `git commit`, `git log`, `git checkout`, or any other git command. The user manages version control. Agents edit files and nothing else.

## Documentation Maintenance

When modifying agent files, pipeline behavior, config schemas, skill references, or any structural aspect of the pipelines, update ALL affected documentation in the same session. Documentation lives in three layers — all three must stay consistent:

1. **`docs/` directory** — User-facing guides and architecture overviews (`docs/afternoon-pipeline-*.md`, `docs/tuesday-verse-agent-family.md`)
2. **Skill references** — Technical references consumed by agents (`.github/skills/*/references/*.md`)
3. **`copilot-instructions.md`** — Repository-wide rules and pipeline summaries (this file)

When adding a new config field, agent, or pipeline feature: update the relevant agent files, then the skill references that describe those agents, then the docs that explain the pipeline to users, then this file if the pipeline summary section is affected. No partial updates — if you changed the behavior, update every document that describes it.

**Changelogs:** The afternoon pipeline maintains `docs/afternoon-pipeline-changelog.md`. When making structural changes to the afternoon pipeline (new agents, behavior changes, config fields, convergence fixes), append an entry at the top of this file describing the problem, root cause, and per-file changes. New entries go at the top.

## Web Search Fallback

If no dedicated `web_search` tool is available, use `web_fetch` with DuckDuckGo Lite for search queries: `https://lite.duckduckgo.com/lite/?q=your+search+terms`. This returns plain HTML that parses cleanly. Do NOT attempt Google Search URLs — they return JavaScript-heavy pages that cannot be parsed.

## Large File Handling

Agents writing files larger than ~5KB risk Copilot CLI timeouts. Read the **`large-file-handling` skill** (`.github/skills/large-file-handling/SKILL.md`) for the full pattern — it covers the bash heredoc append method, the shell security scanner trap, and the create-tool fallback. Mount this skill on any agent that writes prose, plans, outlines, or memory files.

### Quick summary

- **Always create files sequentially**: Use the `create` tool for new files and `edit` tool for modifications. Do NOT use bash heredocs (`cat << 'EOF'`) — the CLI shell security scanner blocks content containing words like `kill`, `$`, backticks, or other patterns it interprets as shell expansion, even inside single-quoted heredoc delimiters. The `create` and `edit` tools bypass the shell entirely and work reliably for all content.
- **Split large writes**: For files exceeding ~5KB, write in multiple sequential `edit` calls appending sections. Or use Python: `python3 -c "..."` with file writes, which also bypasses shell content scanning.
- **Per-entity splitting**: Files that grow across runs should split into one file per entity (not one monolith). Each entity file stays small (~2-5KB forever). Use `_index.json` for cheap discovery.
- **Targeted reads**: "Lost in the Middle" effect means LLMs attend weakly to mid-context. Read only the files you need, JSON before markdown, indexes before full profiles. Re-read critical rules between passes.

See `.github/skills/large-file-handling/references/patterns.md` for concrete examples (prose chapters, JSON plans, per-entity memory, outlines).

## Todolist-Driven Structured Passes

Worker agents (any agent doing substantive work — writing, editing, analysis, cataloguing) organize execution as **sequential todo-driven passes** tracked via the todolist tool with todo-dependencies. Each pass has one concern. This produces more reliable output than monolithic "do everything" instructions.

Standard pattern: Create todos in order, each depending on the previous. Read inputs → domain-specific passes → self-audit → write output. Mark in-progress before starting, done when complete, query for next ready todo.

Pure routers/orchestrators skip this pattern — they dispatch, they don't do passes.

See the agent-as-function skill (`.github/skills/agent-as-function/SKILL.md`, "Todolist-Driven Structured Passes" section) for the full pattern, common pass sequences by agent type, and design rationale.
