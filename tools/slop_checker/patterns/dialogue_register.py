"""Pattern definitions for: dialogue_register"""

PATTERNS = [
    {
        "name": "dialogue_actionable",
        "category": "dialogue_register",
        "regex": r'\bactionable\s+(?:intelligence|information|data)\b',
        "cap": 0,
        "description": "Dialogue register: 'actionable intelligence/information'",
    },
    {
        "name": "dialogue_diagnostic_network",
        "category": "dialogue_register",
        "regex": r'\bdiagnostic\s+(?:network|assessment|protocols?)\b',
        "cap": 0,
        "description": "Dialogue register: 'diagnostic network/assessment'",
    },
    {
        "name": "dialogue_vector",
        "category": "dialogue_register",
        "regex": r'\bvector\s+(?:of|for)\s+(?:infection|transmission|attack|spread)\b',
        "cap": 0,
        "description": "Dialogue register: 'vector of/for infection'",
    },
    {
        "name": "dialogue_optimal",
        "category": "dialogue_register",
        "regex": r'\boptimal\s+(?:outcome|solution|approach|strategy)\b',
        "cap": 0,
        "description": "Dialogue register: 'optimal outcome/solution'",
    },
]

COMBINED_CAP = None
