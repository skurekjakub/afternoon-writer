"""Pattern definitions for: ambient_inversion"""

PATTERNS = [
    {
        "name": "ambient_inversion_came",
        "category": "ambient_inversion",
        "regex": r'(?:^|[.!?]\s+)(?:from|across|over|through|beyond|outside|below|above|under|along)\s+[^.!?]{0,60}?\bcame\s+(?:the\s+)?(?:bark|knock|sound|smell|heat|rattle|clang|cry|shout|glow|light|reek|scent)\b',
        "cap": 2,
        "description": "Front-loaded atmospheric inversion that delays a simple source",
    },
    {
        "name": "ambient_inversion_drifted",
        "category": "ambient_inversion",
        "regex": r'(?:^|[.!?]\s+)(?:across|over|through|along|around)\s+[^.!?]{0,60}?\b(?:drifted|rolled|rose|spread)\s+(?:the\s+)?(?:smell|heat|sound|light|glow|reek|scent)\b',
        "cap": 2,
        "description": "Stage-managed ambience with delayed sensory noun subject",
    },
]

COMBINED_CAP = 0