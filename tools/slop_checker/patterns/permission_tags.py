"""Pattern definitions for: permission_tags"""

PATTERNS = [
    {
        "name": "permission_tag_she_let_it",
        "category": "permission_tags",
        "regex": r"\b(?:and |but )?(?:she|he|they|I|we|[A-Z][a-z]+) (?:let|lets|had let) (?:it|that|this|them)(?: (?:come|go|pass|settle|stay|sit|take|carry|wash|drift|fade|stand|run|do|have)\b[^.!?]{0,30})?[.,;!?]",
        "cap": 0,
        "description": "Permission tag: 'she let it', 'she let it come and go', 'let it take her weight'. Say what she did, or cut the tag.",
    },
    {
        "name": "permission_tag_let_it_settle",
        "category": "permission_tags",
        "regex": r"(?:^|[.!?]\s+)Let (?:it|that|this|them) (?:settle|pass|go|sit|stand|stay|come|fade|sink)\b",
        "cap": 0,
        "description": "Permission tag as a standalone imperative fragment: 'Let it settle.'",
    },
    {
        "name": "permission_tag_let_feeling_work",
        "category": "permission_tags",
        "regex": r"\blet (?:the )?(?:fear|grief|anger|cold|silence|pain|heat|thought|feeling|ache|thank-you)\b[^.!?]{0,25}\b(?:do its work|settle|pass|wash|come|go|stay|sit|take)\b",
        "cap": 0,
        "description": "Permission tag with a named feeling: 'let the fear do its work'.",
    },
]

COMBINED_CAP = None
