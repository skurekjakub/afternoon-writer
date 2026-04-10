"""Pattern definitions for: temporal_padding"""

PATTERNS = [
    {
        "name": "temporal_after_moment",
        "category": "temporal_padding",
        "regex": r'\b[Aa]fter\s+a\s+(?:long\s+)?(?:moment|beat|pause|silence)\b',
        "cap": 2,
        "description": "Temporal padding: 'After a moment/beat/pause'",
    },
    {
        "name": "temporal_finally",
        "category": "temporal_padding",
        "regex": r'(?:^|\.\s+)[Ff]inally[,\s]',
        "cap": 3,
        "description": "Temporal padding: 'Finally' as sentence opener",
    },
    {
        "name": "temporal_a_beat",
        "category": "temporal_padding",
        "regex": r'\b[Aa]\s+beat\s+(?:passed|of\s+silence)\b',
        "cap": 1,
        "description": "Temporal padding: 'A beat passed/of silence'",
    },
]

COMBINED_CAP = None
