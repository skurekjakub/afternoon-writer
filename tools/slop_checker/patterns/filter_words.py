"""Pattern definitions for: filter_words"""

PATTERNS = [
    {
        "name": "filter_noticed",
        "category": "filter_words",
        "regex": r'\bnoticed\b',
        "cap": 3,
        "description": "Filter word: noticed",
    },
    {
        "name": "filter_realized",
        "category": "filter_words",
        "regex": r'\brealized\b',
        "cap": 3,
        "description": "Filter word: realized",
    },
    {
        "name": "filter_observed",
        "category": "filter_words",
        "regex": r'\bobserved\b',
        "cap": 3,
        "description": "Filter word: observed",
    },
    {
        "name": "filter_watched",
        "category": "filter_words",
        "regex": r'\bwatched\b',
        "cap": 3,
        "description": "Filter word: watched",
    },
    {
        "name": "filter_decided",
        "category": "filter_words",
        "regex": r'\bdecided\b',
        "cap": 3,
        "description": "Filter word: decided",
    },
    {
        "name": "filter_wondered",
        "category": "filter_words",
        "regex": r'\bwondered\b',
        "cap": 3,
        "description": "Filter word: wondered",
    },
    {
        "name": "filter_registered",
        "category": "filter_words",
        "regex": r'\bregistered\b',
        "cap": 3,
        "description": "Filter word: registered (sensor-array verb)",
    },
    {
        "name": "filter_catalogued",
        "category": "filter_words",
        "regex": r'\bcatalogu(?:ed|ing)\b',
        "cap": 3,
        "description": "Filter word: catalogued/cataloguing",
    },
    {
        "name": "filter_absorbed",
        "category": "filter_words",
        "regex": r'\babsorbed\s+(?:the|her|his|their|its|this|that|what)\b',
        "cap": 3,
        "description": "Filter word: absorbed the implication/information",
    },
    {
        "name": "filter_filed",
        "category": "filter_words",
        "regex": r'\bfiled\s+(?:the|that|this|it|away)\b',
        "cap": 3,
        "description": "Filter word: filed the observation",
    },
    {
        "name": "filter_assessed",
        "category": "filter_words",
        "regex": r'\bassess(?:ed|ment)\b',
        "cap": 3,
        "description": "Filter word: assessed/assessment",
    },
]

COMBINED_CAP = 7
