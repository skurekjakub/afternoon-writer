# Phase 5: Writer Agent Integration

**Version**: v1
**Goal**: Give the writer agent a lightweight self-check using the skeleton strip so it catches the worst concreteness drift before the gate even sees the draft.
**Dependencies**: Phase 3 (CLI tool)
**Outputs consumed by**: Phase 6 (calibration)

---

## Context

The writer agent (Claude Opus 4.6) produces the draft. The gate agent (GPT-5.4) audits it. The skeleton strip gives the writer a "mirror" — a quick check that reveals whether its own prose has drifted into abstraction.

The self-check is deliberately lightweight: sample 5 paragraphs, run the strip, check the summary. If any paragraph is flagged as "abstract", the writer rewrites it before delivering v1.md. This catches the most egregious drift — entire paragraphs of interpretation — without burning significant context or adding a full analysis pass.

The writer does NOT read the full JSON report. It reads the `--summary` output (5-10 lines) and acts on flagged zones only. This keeps the self-check cheap.

---

## Tasks

### 5.1 — Add self-check instructions to writer agent

**File**: `.github/agents/ravencrest-prose-writer.agent.md`

Add a new section after the main writing process but before delivery.

**Changes**:

1. **New section: "Post-Draft Self-Check"**:

```markdown
## Post-Draft Self-Check

After writing the complete draft to v{N}.md, run the skeleton strip:

\`\`\`bash
python3 tools/skeleton-strip/strip.py --summary {draft_path}
\`\`\`

Read the summary output. Focus on:
- **FLAGGED ZONES** — paragraphs with low concreteness density
- **abstract_percentage** — if >25%, the draft has significant interpretation drift

For each flagged zone:
1. Re-read the flagged paragraph(s) in your draft
2. Apply the Artist Test: for each description, could an artist draw it?
3. If the paragraph fails, rewrite it IN PLACE using the `edit` tool — replace abstract interpretation with physical, observable detail
4. Re-run the strip on the corrected paragraph to verify

This self-check catches ~80% of interpretive filter violations before the gate sees the draft. The gate catches the rest.

If the skeleton strip tool is unavailable (command fails), skip this step and deliver the draft as-is. Do NOT let tool failure block chapter delivery.
```

2. **Update the delivery checklist** — Add skeleton strip check between "re-read for AI patterns" and "write status.json":

Current delivery flow:
- Write draft to v{N}.md
- Re-read for AI patterns
- Write writer-status.json

New flow:
- Write draft to v{N}.md
- Run skeleton strip self-check
- Fix any flagged zones
- Write writer-status.json

**Acceptance Criteria**:
- [ ] Writer agent instructions include the skeleton strip self-check
- [ ] Self-check uses `--summary` mode (lightweight)
- [ ] Writer rewrites flagged zones in place before delivery
- [ ] Tool failure does not block delivery (graceful degradation)
- [ ] Delivery flow is: write → strip check → fix → deliver
