"""Pattern definitions for: negation_addiction"""

PATTERNS = [
    {
        "name": "negation_parallel",
        "category": "negation_addiction",
        "regex": r'\bnot\s+\w+(?:\s+\w+){0,3},?\s+but\s+\w+(?:\s+\w+){0,3}[.;]\s*[Nn]ot\s+\w+(?:\s+\w+){0,3},?\s+but\b',
        "cap": 0,
        "description": "Negation: parallel 'Not X but Y. Not A but B' pairs",
    },
    {
        "name": "negation_not_x_semicolon_y",
        "category": "negation_addiction",
        "regex": r'(?:^|[.!?]\s+)Not\s+\w+(?:\s+\w+){0,3}\s*;\s*\w+',
        "cap": 0,
        "description": "Negation: 'Not X; Y' dramatic negation (sentence-initial)",
    },
]

COMBINED_CAP = None
