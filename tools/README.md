# Prose tools

Deterministic checks the pipeline's agents run on chapter prose. Run everything from the repo root.

| Tool | What it reports | Who runs it |
|---|---|---|
| `tools/prose_check.py` | All three below in one process, one JSON report | slop-gate (Phase 1b) |
| `tools/rhythm_scorer/score.py` | Sentence rhythm and texture against the style guide's targets | craft-auditor, slop-gate, style-extractor |
| `tools/slop_checker/check.py` | Known AI word and phrase tics, with per-chapter caps | slop-gate |
| `tools/mannered_checker/check.py` | Mannered prose (pass C) and refrains across chapters, with caps calibrated on human prose | slop-gate pass C, slophunter |
| `tools/mannered_checker/calibrate.py` | Re-measures the human corpora and re-anchors the style guide | runs itself when needed; style-extractor |

Every tool takes `--json` or `--summary`. Summary is the default.

## The runner

```
python3 tools/prose_check.py --json FILE                      # rhythm + slop + mannered
python3 tools/prose_check.py --json --tools rhythm,slop FILE   # a subset
python3 tools/prose_check.py FILE                             # text summaries
```

The report is `{"file", "tools", "failed", "rhythm", "slop", "mannered"}`. Each tool's block is exactly what that tool prints with `--json` on its own. Rhythm baselines default to `.afternoon/style-guide.json`. If a tool crashes, its block is `{"error", "traceback"}`, its name goes in `failed`, the other blocks are still reported, and the exit status is 3.

Exit status for every tool: 0 ok, 1 file not found, 2 bad arguments (3 for a failed tool in the runner).

## Calibration and the cache

The mannered checker's caps come from the human corpora in `.afternoon/config.json -> priming.humanCorpora`. `calibration.json` records a fingerprint of those corpora (paths, weights, sizes, mtimes) and a hash of the checker and `tools/prose_core/text.py`. When either changes, the next run recalibrates by itself and re-syncs `.afternoon/style-guide.json`.

The refrain check drops any 5-word run that occurs in the human corpora. Those runs are cached as 64-bit hashes in `tools/mannered_checker/cache/` (about 3.5 MB, git-ignored), keyed the same way, so a warm run doesn't re-read the 437K-word corpus. Delete the folder at any time; the next run rebuilds it. `--no-cache` skips it.

## Layout

- `prose_core/text.py`: helpers shared by the tools: line index, context snippets, quote and header handling, paragraph spans. All of them keep character offsets stable.
- `skeleton_strip/splitter.py`: the prose-aware sentence splitter the rhythm scorer uses.
- `slop_checker/patterns/`: one module per category; each exports `PATTERNS` and `COMBINED_CAP`.
- `mannered_checker/refrain_families.json`: recurring signature beats and their budgets.

## Tests

```
python3 -m unittest discover -s tools/tests -t .
```

Standard library only. Fixture prose is written for the tests. Tests that need config, corpora or calibration run in a temporary repo (`tools/tests/support.py: TempRepo`). The last test fails the run if anything touched the real `calibration.json`, cache, config or style guide. If the pipeline recalibrates while the tests run, that test can trip, so rerun once it's done.

`test_docs_contract.py` reads every `python3 tools/...` command in `.claude/` and `resources/`, and checks the script exists and accepts each flag the docs use.
