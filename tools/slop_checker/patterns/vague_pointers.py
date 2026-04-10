"""Pattern definitions for: vague_pointers"""

PATTERNS = [
    {
        "name": "something_vague",
        "category": "vague_pointers",
        "regex": r'\bsomething\s+(?:in|about|behind|between|within|like|close\s+to)\s+(?:the\s+|her\s+|his\s+|their\s+)?\w+',
        "cap": 2,
        "description": "Vague pointer: 'something in/about [noun]'",
    },
    {
        "name": "there_was_something",
        "category": "vague_pointers",
        "regex": r'\bthere\s+was\s+something\b',
        "cap": 2,
        "description": "Vague pointer: 'there was something'",
    },
]

COMBINED_CAP = 3
