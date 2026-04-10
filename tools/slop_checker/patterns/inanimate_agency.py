"""Pattern definitions for: inanimate_agency"""

PATTERNS = [
    {
        "name": "inanimate_silence",
        "category": "inanimate_agency",
        "regex": r'\b(?:the\s+)?silence\s+(?:pressed|settled|hung|stretched|thickened|fell|draped|wrapped|descended|coiled|deepened)\b',
        "cap": 2,
        "description": "Inanimate agency: silence performing actions",
    },
    {
        "name": "inanimate_darkness",
        "category": "inanimate_agency",
        "regex": r'\b(?:the\s+)?darkness\s+(?:pressed|breathed|closed|swallowed|wrapped|seemed|crept|reached|pooled|gathered|enveloped)\b',
        "cap": 2,
        "description": "Inanimate agency: darkness performing actions",
    },
    {
        "name": "inanimate_tension",
        "category": "inanimate_agency",
        "regex": r'\b(?:the\s+)?tension\s+(?:coiled|hung|crackled|snapped|built|thickened|wound|mounted|stretched|settled|radiated)\b',
        "cap": 2,
        "description": "Inanimate agency: tension performing actions",
    },
    {
        "name": "inanimate_air",
        "category": "inanimate_agency",
        "regex": r'\b(?:the\s+)?air\s+(?:shifted|changed|thickened|crackled|shimmered|went\s+(?:still|cold|tight|electric))\b',
        "cap": 2,
        "description": "Inanimate agency: air performing actions",
    },
]

COMBINED_CAP = 2
