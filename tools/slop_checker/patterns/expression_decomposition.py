"""Pattern definitions for: expression_decomposition"""

PATTERNS = [
    {
        "name": "expression_precursor",
        "category": "expression_decomposition",
        "regex": r'\b(?:precursor|predecessor|preliminary|groundwork)\s+(?:to|for|of)\s+(?:a\s+)?(?:smile|grin|frown|surprise|anger|recognition|amusement|laugh)\b',
        "cap": 0,
        "description": "Expression decomposition: naming the phase of an expression",
    },
    {
        "name": "expression_direction_of",
        "category": "expression_decomposition",
        "regex": r'\bin\s+the\s+direction\s+of\s+(?:a\s+)?(?:smile|grin|frown|amusement|surprise|laugh|anger)\b',
        "cap": 0,
        "description": "Expression decomposition: 'in the direction of a smile'",
    },
]

COMBINED_CAP = None
