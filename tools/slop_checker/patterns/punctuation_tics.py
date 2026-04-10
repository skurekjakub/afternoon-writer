"""Pattern definitions for: punctuation_tics"""

PATTERNS = [
    {
        "name": "punct_emdash_cluster",
        "category": "punctuation_tics",
        "regex": r'[^\n.!?]*\u2014[^\n.!?]*\u2014[^\n.!?]*\u2014',
        "cap": 0,
        "description": "Punctuation tic: 3+ em dashes in a single sentence (zero tolerance)",
    },
    {
        "name": "punct_semicolon",
        "category": "punctuation_tics",
        "regex": r';',
        "cap": 1,
        "cap_per_words": 500,
        "description": "Punctuation tic: semicolons in narration (max 1 per 500 words)",
    },
    {
        "name": "punct_ellipsis",
        "category": "punctuation_tics",
        "regex": r'(?:\.\.\.|…)',
        "cap": 1,
        "cap_per_words": 600,
        "description": "Punctuation tic: ellipses (max 1 per 600 words)",
    },
    {
        "name": "punct_colon_narration",
        "category": "punctuation_tics",
        "regex": r'[^"\u201c\u201d\n]{4,}:\s+[a-z]',
        "cap": 1,
        "cap_per_words": 1000,
        "description": "Punctuation tic: colons in narration (max 1 per 1000 words)",
    },
]

COMBINED_CAP = None
