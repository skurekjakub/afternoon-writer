
## Large File Handling

Agents writing files larger than ~5KB risk Copilot CLI timeouts. Read the **`large-file-handling` skill** (`.github/skills/large-file-handling/SKILL.md`) for the full pattern — it covers the bash heredoc append method, the shell security scanner trap, and the create-tool fallback. Mount this skill on any agent that writes prose, plans, outlines, or memory files.

### Quick summary

- **Bash heredoc append**: Split large writes into multiple `cat << 'EOF' >> file` calls. Single-quoted delimiter is mandatory. First call uses `>`, subsequent use `>>`.
- **Shell security scanner**: The CLI blocks heredocs containing `$`, `` ` ``, or `${...}` in content, even inside single-quoted heredocs. Use the create-tool + cat-append fallback for sections with those characters.
- **Per-entity splitting**: Files that grow across runs should split into one file per entity (not one monolith). Each entity file stays small (~2-5KB forever). Use `_index.json` for cheap discovery.
- **Targeted reads**: "Lost in the Middle" effect means LLMs attend weakly to mid-context. Read only the files you need, JSON before markdown, indexes before full profiles. Re-read critical rules between passes.

See `.github/skills/large-file-handling/references/patterns.md` for concrete examples (prose chapters, JSON plans, per-entity memory, outlines).