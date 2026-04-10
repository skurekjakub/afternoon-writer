# SlopSquid / Antislop Data Artifacts

Downloaded from: https://github.com/sam-paech/slop-score
Commit: 289264ab2a0df1358ef81ced3c259610ea709514
License: MIT (primary components)
Date: June 2025

## Contents

| File | Entries | Description |
|---|---|---|
| `slop_list.json` | 1648 | Single words overused in LLM output vs human writing |
| `slop_list_bigrams.json` | 200 | 2-word phrases overused in LLM output |
| `slop_list_trigrams.json` | 430 | 3-word phrases overused in LLM output |

## Format

Each file is a JSON array of single-element arrays: `[["word"], ["word"], ...]`

## Notes

- Many entries in `slop_list.json` are fantasy-specific character names
  (aelara, eldric, grimoire, etc.) that will never appear in our prose.
  A fiction-relevant subset would be ~200-300 words.
- Bigrams and trigrams are more universally useful — "voice barely whisper,"
  "took deep breath," "heart pounding chest" are genre-independent AI tells.
- These lists were derived from statistical comparison of 67 LLM outputs
  against human-written creative fiction baselines (Reddit creative writing
  + Project Gutenberg). See Paech et al. 2025 (arxiv 2510.15061).

## Citation

```bibtex
@misc{paech2025slopScore,
      title={slop-score},
      author={Samuel J. Paech},
      year={2025},
      howpublished={\url{https://github.com/sam-paech/slop-score}},
      note={GitHub repository}
}
```
