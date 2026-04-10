"""Pattern definitions for: clinical_anatomy"""

PATTERNS = [
    {
        "name": "clinical_corona",
        "category": "clinical_anatomy",
        "regex": r'\bcorona\b',
        "cap": 0,
        "description": "Clinical anatomy: corona",
    },
    {
        "name": "clinical_glans",
        "category": "clinical_anatomy",
        "regex": r'\bglans\b',
        "cap": 0,
        "description": "Clinical anatomy: glans",
    },
    {
        "name": "clinical_involuntary",
        "category": "clinical_anatomy",
        "regex": r'\binvoluntary\s+(?:contraction|response|reaction|shudder|twitch|movement)\b',
        "cap": 0,
        "description": "Clinical anatomy: 'involuntary [response]'",
    },
    {
        "name": "clinical_nerve_compound",
        "category": "clinical_anatomy",
        "regex": r'\bnerve[- ](?:cascade|dense|endings?\s+fir(?:ed|ing)|rich)\b',
        "cap": 0,
        "description": "Clinical anatomy: nerve-cascade, nerve-dense, nerve endings firing",
    },
    {
        "name": "clinical_tissue_saturation",
        "category": "clinical_anatomy",
        "regex": r'\btissue\s+saturation\b',
        "cap": 0,
        "description": "Clinical anatomy: tissue saturation",
    },
]

COMBINED_CAP = None
