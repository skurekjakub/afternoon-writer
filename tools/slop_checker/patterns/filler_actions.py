"""Pattern definitions for: filler_actions"""

PATTERNS = [
    {
        "name": "filler_nodded",
        "category": "filler_actions",
        "regex": r'\bnodded\b',
        "cap": 4,
        "description": "Filler action: nodded",
    },
    {
        "name": "filler_sighed",
        "category": "filler_actions",
        "regex": r'\bsighed\b',
        "cap": 4,
        "description": "Filler action: sighed",
    },
    {
        "name": "filler_smiled",
        "category": "filler_actions",
        "regex": r'\bsmiled\b',
        "cap": 4,
        "description": "Filler action: smiled",
    },
    {
        "name": "filler_shrugged",
        "category": "filler_actions",
        "regex": r'\bshrugged\b',
        "cap": 4,
        "description": "Filler action: shrugged",
    },
    {
        "name": "filler_glanced",
        "category": "filler_actions",
        "regex": r'\bglanced\b',
        "cap": 4,
        "description": "Filler action: glanced",
    },
    {
        "name": "filler_frowned",
        "category": "filler_actions",
        "regex": r'\bfrowned\b',
        "cap": 4,
        "description": "Filler action: frowned",
    },
]

COMBINED_CAP = 15
