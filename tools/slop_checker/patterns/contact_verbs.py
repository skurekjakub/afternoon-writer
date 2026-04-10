"""Pattern definitions for: contact_verbs"""

PATTERNS = [
    {
        "name": "contact_pressed",
        "category": "contact_verbs",
        "regex": r'\bpressed\b',
        "cap": 6,
        "description": "Contact verb: pressed",
    },
    {
        "name": "contact_settled",
        "category": "contact_verbs",
        "regex": r'\bsettled\b',
        "cap": 6,
        "description": "Contact verb: settled",
    },
    {
        "name": "contact_traced",
        "category": "contact_verbs",
        "regex": r'\btraced\b',
        "cap": 6,
        "description": "Contact verb: traced",
    },
    {
        "name": "contact_brushed",
        "category": "contact_verbs",
        "regex": r'\bbrushed\b',
        "cap": 6,
        "description": "Contact verb: brushed",
    },
    {
        "name": "contact_found",
        "category": "contact_verbs",
        "regex": r'\bfound\s+(?:the|her|his|a)\b',
        "cap": 6,
        "description": "Contact verb: found [the/her/his]",
    },
]

COMBINED_CAP = None
