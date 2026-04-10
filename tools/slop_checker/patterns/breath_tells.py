"""Pattern definitions for: breath_tells"""

PATTERNS = [
    {
        "name": "breath_held",
        "category": "breath_tells",
        "regex": r'\bheld\s+(?:her|his|their|a)?\s*breath\b',
        "cap": 3,
        "description": "Breath tell: held breath",
    },
    {
        "name": "breath_caught",
        "category": "breath_tells",
        "regex": r'\bbreath\s+caught\b',
        "cap": 3,
        "description": "Breath tell: breath caught",
    },
    {
        "name": "breath_released",
        "category": "breath_tells",
        "regex": r'(?:released|let\s+out)\s+(?:a\s+)?(?:slow\s+|long\s+|shaky\s+)?breath\b',
        "cap": 3,
        "description": "Breath tell: released/let out breath",
    },
    {
        "name": "breath_sharp_intake",
        "category": "breath_tells",
        "regex": r'(?:sharp|quick|sudden)\s+(?:intake|inhalation)\s+of\s+breath\b',
        "cap": 3,
        "description": "Breath tell: sharp intake of breath",
    },
    {
        "name": "breath_exhaled",
        "category": "breath_tells",
        "regex": r'\bexhaled\s+(?:through|slowly|sharply|hard)\b',
        "cap": 3,
        "description": "Breath tell: exhaled through/slowly",
    },
    {
        "name": "breath_didnt_know_holding",
        "category": "breath_tells",
        "regex": r"breath\s+(?:she|he|they)\s+didn['\u2019]t\s+know\s+(?:she|he|they)\s+(?:was|were|had\s+been)\s+holding",
        "cap": 0,
        "description": "Breath tell: breath she didn't know she was holding (zero tolerance)",
    },
]

COMBINED_CAP = 3
