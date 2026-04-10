# Phase 4: Gate Agent Integration

**Version**: v1
**Goal**: Wire the skeleton strip CLI into the gate agent's Check 8 workflow so the LLM gate receives pre-computed concreteness data as an "analytic hint" before judging the draft.
**Dependencies**: Phase 3 (CLI tool)
**Outputs consumed by**: Phase 6 (calibration will tune thresholds based on gate behavior)

---

## Context

This is the IBM "Analytic Hints" pattern applied to fiction prose. Research showed that combining rule-based analysis with LLM judges improves error detection from <50% to >90%. The skeleton strip provides the rule-based layer; the gate agent provides the LLM judgment layer.

The gate currently runs 8 checks. Check 8 (Interpretive Filter) is the hardest — the gate must detect prose that passes every surface check but fails the Artist Test. The skeleton strip pre-computes the data that makes the invisible visible.

**Integration flow:**
1. Orchestrator dispatches gate as usual
2. Gate reads the draft, then runs the skeleton strip CLI via bash
3. Gate reads the JSON output — it now knows which paragraphs are flagged, which sentences are abstract, which patterns triggered
4. Gate runs Check 8 with the flagged zones as focal points instead of scanning the entire draft blind
5. Gate report includes skeleton density data for transparency

This means the gate doesn't have to "discover" the abstract zones — they're pre-identified by deterministic analysis. The gate's job narrows from "find all interpretive filter violations" to "verify flagged zones and determine if defenses apply."

---

## Tasks

### 4.1 — Add skeleton strip invocation to gate agent

**File**: `.github/agents/ravencrest-prose-gate.agent.md`

The gate agent needs new instructions: before running Check 8, invoke the skeleton strip tool and read its output.

**Changes**:

1. **New section before Check 8** — "Pre-Check 8: Skeleton Strip Analysis":

```markdown
### Pre-Check 8: Skeleton Strip Analysis

Before running Check 8, invoke the skeleton strip tool to pre-identify abstract zones:

\`\`\`bash
python3 tools/skeleton-strip/strip.py --json {draft_path}
\`\`\`

Read the JSON output. It provides:
- `overall.abstract_percentage` — what % of sentences are abstract (>20% is concerning)
- `overall.total_pattern_matches` — how many structural patterns triggered
- `flagged_zones` — specific paragraph ranges with low concreteness density

Use this data to FOCUS Check 8. Instead of scanning every paragraph blind:
1. Start with the flagged zones — these are the highest-probability violations
2. For each flagged sentence, apply the Artist Test: could an artist draw it?
3. Check if a defense applies (character voice, dialogue, intentional structure)
4. Then do a quick scan of non-flagged paragraphs to catch anything the tool missed

The skeleton strip is a high-recall pre-filter. It catches ~90% of interpretive filter violations mechanically. Your job is the precision layer — confirming true positives and filtering false positives.
```

2. **Update Check 8 instructions** — Change from "Scan for:" to "Using the skeleton strip output, verify:". The check patterns stay the same, but the gate now has specific paragraphs to focus on.

3. **Update gate report schema** — Add skeleton data to the `interpretive_filter` check:

```json
"interpretive_filter": {
    "count": 3,
    "skeleton_data": {
        "abstract_percentage": 16.2,
        "mean_density": 0.41,
        "pattern_matches": 7,
        "flagged_zone_count": 3
    },
    "findings": [...]
}
```

**Acceptance Criteria**:
- [ ] Gate agent instructions include the skeleton strip bash invocation
- [ ] Gate reads JSON output before running Check 8
- [ ] Gate report includes `skeleton_data` in the `interpretive_filter` check
- [ ] Gate focuses on flagged zones first, then scans remainder
- [ ] Existing Check 8 patterns (the 7 flags) remain unchanged
- [ ] Gate can still run Check 8 if the skeleton strip tool fails (graceful degradation — log warning, fall back to blind scan)

### 4.2 — Add skeleton strip dependency check to orchestrator

**File**: `.github/agents/ravencrest-pusher-orchestrator.agent.md`

The orchestrator needs to verify the skeleton strip tool is available before dispatching the gate.

**Changes**:

1. **Pre-flight check** — Before the prose pipeline loop, verify:
   ```bash
   python3 tools/skeleton-strip/strip.py --help
   ```
   If this fails, log a warning but continue — the gate can fall back to blind Check 8.

2. **Pass tool availability to gate prompt** — Add a note to the gate dispatch:
   ```
   Skeleton strip tool available: yes/no
   ```

**Acceptance Criteria**:
- [ ] Orchestrator checks for skeleton strip tool before prose pipeline
- [ ] Gate dispatch prompt includes tool availability flag
- [ ] Pipeline continues even if tool is unavailable (degraded mode)
