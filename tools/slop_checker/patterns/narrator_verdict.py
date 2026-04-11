"""Pattern definitions for: narrator_verdict

Catches compressed evaluative fragments — the narrator appending a wry,
thematic, or sardonic judgment to a factual observation. These are
verdict-tag fragments per the narrator-seep guide (A1 pattern).

Shapes caught:
  - "X enough to be Y" (late enough to be decoration)
  - "X enough for Y" (straight enough for respect)
  - "too X for Y" (too fast for indifference)

Broad net — excludes only pronouns and determiners after for/to be.
Human prose triggers ~1 per 18K words; AI prose triggers ~1 per 560
words. The gate LLM reads context and KEEPs legitimate uses. The
tool's job is to surface candidates, not auto-kill.

Cap is 0: every match is surfaced. Combined cap 2 per chapter.
"""

PATTERNS = [
    {
        "name": "verdict_enough_to_be",
        "category": "narrator_verdict",
        "regex": r',\s+\w+\s+enough\s+to\s+be\s+\w+',
        "cap": 0,
        "description": "Verdict tag: ', X enough to be Y' (narrator evaluation appended to action)",
    },
    {
        "name": "verdict_enough_for",
        "category": "narrator_verdict",
        "regex": r'\w+\s+enough\s+for\s+(?!her\b|his\b|him\b|them\b|the\b|a\b|an\b|it\b|this\b|that\b|their\b|my\b|your\b|our\b|its\b|me\b|us\b)\w+',
        "cap": 0,
        "description": "Verdict tag: 'X enough for Y' where Y is not a pronoun/determiner",
    },
    {
        "name": "verdict_too_x_for",
        "category": "narrator_verdict",
        "regex": r'\btoo\s+\w+\s+for\s+(?!her\b|his\b|him\b|them\b|the\b|a\b|an\b|it\b|this\b|that\b|their\b|my\b|your\b|our\b|its\b|me\b|us\b)\w+',
        "cap": 0,
        "description": "Verdict tag: 'too X for Y' where Y is not a pronoun/determiner",
    },
]

COMBINED_CAP = 1
