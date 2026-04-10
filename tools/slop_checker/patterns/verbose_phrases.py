"""Pattern definitions for: verbose_phrases"""

PATTERNS = [
    {
        "name": "verbose_sensation_was",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+sensation\s+was\b',
        "cap": 0,
        "description": "Verbose phrase: 'the sensation was'",
    },
    {
        "name": "verbose_evidence_of",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+evidence\s+of\b',
        "cap": 0,
        "description": "Verbose phrase: 'the evidence of'",
    },
    {
        "name": "verbose_act_of",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+act\s+of\b',
        "cap": 0,
        "description": "Verbose phrase: 'the act of'",
    },
    {
        "name": "verbose_mode_of",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+mode\s+of\b',
        "cap": 0,
        "description": "Verbose phrase: 'the mode of'",
    },
    {
        "name": "verbose_result_was",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+result\s+was\b',
        "cap": 0,
        "description": "Verbose phrase: 'the result was'",
    },
    {
        "name": "verbose_closing_gesture",
        "category": "verbose_phrases",
        "regex": r'\bthe\s+closing\s+gesture\b',
        "cap": 0,
        "description": "Verbose phrase: 'the closing gesture'",
    },
]

COMBINED_CAP = None
