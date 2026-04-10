"""Pattern definitions for: simile_overload"""

PATTERNS = [
    {
        "name": "simile_like",
        "category": "simile_overload",
        "regex": r'\blike\s+(?:a|an|the)\s+\w+',
        "cap": 3,
        "cap_per_words": 500,
        "description": "Simile: 'like a [noun]' comparison (1 per 500 words)",
    },
    {
        "name": "simile_as_if",
        "category": "simile_overload",
        "regex": r'\bas\s+if\b',
        "cap": 5,
        "description": "Simile: 'as if' construction",
    },
    {
        "name": "simile_as_though",
        "category": "simile_overload",
        "regex": r'\bas\s+though\b',
        "cap": 3,
        "description": "Simile: 'as though' construction",
    },
]

COMBINED_CAP = None
