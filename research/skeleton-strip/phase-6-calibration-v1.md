# Phase 6: Calibration & Testing

**Version**: v1
**Goal**: Run the skeleton strip against known good and known bad prose to calibrate thresholds, verify accuracy, and document expected behavior.
**Dependencies**: Phase 1, 2, 3 (full CLI tool built), Phase 4, 5 (integration points exist)
**Outputs consumed by**: None (terminal phase — produces the calibrated system)

---

## Context

The skeleton strip has multiple tunable thresholds:
- Word-level: CONCRETE_THRESHOLD (4.0), ABSTRACT_THRESHOLD (2.5)
- Sentence-level: density cutoffs for "concrete" / "mixed" / "abstract" verdicts
- Paragraph-level: percentage cutoffs for "grounded" / "drifting" / "abstract"
- Pattern matching: which patterns to include, how to weight pattern matches vs density

These need empirical calibration against prose we've already evaluated: the voice samples (known good), the BAD examples from 18-interpretive-filter.md (known bad), and ideally one or two published prose passages as reference.

---

## Tasks

### 6.1 — Build test fixtures

**New file**: `tools/skeleton-strip/tests/fixtures.py`

Collect known-good and known-bad prose into test fixtures.

**Sources**:
- **Known good**: The 4 voice samples from `stories/hollow-falls/.morgana/voice-samples.md` — user-approved, concrete, grounded
- **Known good**: The GOOD examples from `references/ai-quirks/sentence-level/18-interpretive-filter.md` (20 examples)
- **Known bad**: The BAD examples from the same file (20 examples)
- **Edge cases**: Interior monologue (can be abstract and that's fine), dialogue (patterns inside quotes are character voice), deliberate stylistic abstraction

```python
GOOD_SENTENCES = [
    "She unclenched her jaw. Dropped her shoulders an inch. Held the coffee cup with both hands so they wouldn't shake.",
    "Water stain on the ceiling tile. One fluorescent tube dead. The fire extinguisher case had a yellowed inspection tag from 2001.",
    "Chin up. Steps even. Not looking at anyone. Hands flat at her sides.",
    # ... 17 more from the reference file
]

BAD_SENTENCES = [
    "She arranged her face into the expression people use when they want to seem unbothered.",
    "The corridor spoke of institutional neglect.",
    "She moved with the kind of deliberation that suggested she was very aware of being watched.",
    # ... 17 more from the reference file
]

EDGE_CASES = [
    # Interior monologue — abstract but intentional
    ("I wondered if she'd ever forgive me.", "should_pass"),
    # Dialogue — pattern inside quotes is character voice
    ('"Something about you reminds me of my mother," she said.', "should_pass"),
    # Deliberate metaphor — earned in context
    ("The house was a mouth. It had swallowed three families.", "should_pass"),
]
```

**Acceptance Criteria**:
- [ ] Fixtures include ≥20 known-good sentences
- [ ] Fixtures include ≥20 known-bad sentences
- [ ] Fixtures include ≥5 edge cases with expected verdicts

### 6.2 — Run calibration and adjust thresholds

**File**: `tools/skeleton-strip/tests/test_calibration.py`

A test script (not a unit test framework — just a plain Python script) that runs the full pipeline against all fixtures and reports accuracy.

**Changes**:

1. **Accuracy metrics**:
   - True positive rate: what % of BAD sentences get verdict "abstract"?
   - True negative rate: what % of GOOD sentences get verdict "concrete"?
   - False positive rate: what % of GOOD sentences get incorrectly flagged?
   - Edge case accuracy: do edge cases with "should_pass" actually pass?

2. **Threshold tuning**: If the defaults produce poor accuracy, adjust CONCRETE_THRESHOLD, ABSTRACT_THRESHOLD, and verdict cutoffs in `scorer.py` and `engine.py`. Document the final values and why.

3. **Pattern accuracy**: Which regex patterns fire on BAD examples? Which fire on GOOD examples? Any patterns producing too many false positives should be tightened or removed.

4. **Output**: Print a calibration report:
```
CALIBRATION REPORT
==================
Good sentences: 20 tested, 18 correct (90%), 2 false positives
Bad sentences:  20 tested, 17 correct (85%), 3 false negatives
Edge cases:     5 tested, 4 correct (80%), 1 unexpected

FALSE POSITIVES (good sentences flagged as bad):
  - "The color had gone out of his face." → density 0.33 (threshold issue?)

FALSE NEGATIVES (bad sentences not flagged):
  - "His face wore the look of a man who had seen something he couldn't unsee." → density 0.31 (borderline)

THRESHOLD RECOMMENDATIONS:
  - Current CONCRETE_THRESHOLD=4.0: keep
  - Current ABSTRACT_THRESHOLD=2.5: consider lowering to 2.3
  - Sentence "abstract" cutoff: consider raising from 0.3 to 0.35
```

**Acceptance Criteria**:
- [ ] True positive rate ≥80% (BAD sentences correctly flagged)
- [ ] True negative rate ≥85% (GOOD sentences correctly passed)
- [ ] False positive rate ≤15% (GOOD sentences incorrectly flagged)
- [ ] Edge cases with "should_pass" pass ≥80% of the time
- [ ] Calibration report is printed and thresholds are adjusted if needed

### 6.3 — Run against voice samples (end-to-end paragraph-level test)

**Script**: `tools/skeleton-strip/tests/test_voice_samples.py`

Run the full CLI against the complete voice samples file (not individual sentences — full paragraphs as the writer would produce them).

**Changes**:
1. Run `strip.py --json` against `stories/hollow-falls/.morgana/voice-samples.md`
2. Verify: overall verdict should be "grounded" or at most "mixed" (these are user-approved samples)
3. Check: no paragraphs should be flagged as "abstract" (they were specifically approved for concreteness)
4. If any paragraphs flag: investigate — is it a threshold issue, or did we miss something during the voice sample approval?

**Acceptance Criteria**:
- [ ] Voice samples file produces overall verdict "grounded" or "mixed"
- [ ] Zero paragraphs flagged as "abstract"
- [ ] If any flags trigger, they're investigated and documented as threshold tuning issues (not false system behavior)

### 6.4 — Document thresholds and expected behavior

**New file**: `tools/skeleton-strip/README.md`

Document the tool: what it does, how to use it, what the thresholds mean, expected accuracy, limitations.

**Contents**:
- Purpose and theory (the "frequency space" analogy)
- Installation (`pip install -r requirements.txt` + `python3 download_norms.py`)
- Usage (three CLI modes)
- Thresholds and what they mean
- Known limitations:
  - Function words (the, is, was) aren't scored — this is correct behavior
  - Proper nouns may not be in the norms — treated as neutral
  - Interior monologue can be legitimately abstract — the LLM layer handles this
  - ~5-10% of words won't have scores (neologisms, character names, slang)
- Calibration results from Phase 6 testing

**Acceptance Criteria**:
- [ ] README exists with usage instructions
- [ ] Thresholds are documented with rationale
- [ ] Known limitations are listed
- [ ] Calibration accuracy numbers are included
