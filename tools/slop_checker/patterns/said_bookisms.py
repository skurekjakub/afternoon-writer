"""Pattern definitions for: said_bookisms"""

PATTERNS = [
    {
        "name": "bookism_exclaimed",
        "category": "said_bookisms",
        "regex": r'\bexclaimed\b',
        "cap": 2,
        "description": "Said bookism: exclaimed",
    },
    {
        "name": "bookism_declared",
        "category": "said_bookisms",
        "regex": r'\bdeclared\b',
        "cap": 2,
        "description": "Said bookism: declared",
    },
    {
        "name": "bookism_murmured",
        "category": "said_bookisms",
        "regex": r'\bmurmured\b',
        "cap": 2,
        "description": "Said bookism: murmured",
    },
    {
        "name": "bookism_breathed_tag",
        "category": "said_bookisms",
        "regex": r'["\u201d]\s+(?:she|he|they|[A-Z]\w+)\s+breathed\b',
        "cap": 2,
        "description": "Said bookism: breathed (as dialogue tag)",
    },
    {
        "name": "bookism_hissed",
        "category": "said_bookisms",
        "regex": r'\bhissed\b',
        "cap": 2,
        "description": "Said bookism: hissed",
    },
    {
        "name": "bookism_growled",
        "category": "said_bookisms",
        "regex": r'\bgrowled\b',
        "cap": 2,
        "description": "Said bookism: growled",
    },
    {
        "name": "bookism_intoned",
        "category": "said_bookisms",
        "regex": r'\bintoned\b',
        "cap": 2,
        "description": "Said bookism: intoned",
    },
    {
        "name": "bookism_retorted",
        "category": "said_bookisms",
        "regex": r'\bretorted\b',
        "cap": 2,
        "description": "Said bookism: retorted",
    },
    {
        "name": "bookism_stammered",
        "category": "said_bookisms",
        "regex": r'\bstammered\b',
        "cap": 2,
        "description": "Said bookism: stammered",
    },
    {
        "name": "bookism_bellowed",
        "category": "said_bookisms",
        "regex": r'\bbellowed\b',
        "cap": 2,
        "description": "Said bookism: bellowed",
    },
    {
        "name": "bookism_conceded",
        "category": "said_bookisms",
        "regex": r'\bconceded\b',
        "cap": 2,
        "description": "Said bookism: conceded",
    },
    {
        "name": "adverb_on_tag",
        "category": "said_bookisms",
        "regex": r'\b(?:said|asked|exclaimed|declared|murmured|hissed|growled|breathed|intoned|stammered|whispered|replied|added|continued|called|snapped|muttered)\s+(?:softly|firmly|quietly|loudly|nervously|angrily|happily|sadly|reluctantly|gently|urgently|thoughtfully|carefully|slowly|sharply|bitterly|wearily|dryly|flatly|curtly|coolly|warmly|absently|mildly|drily|tightly|lightly|stiffly|briskly|hoarsely|breathlessly)\b',
        "cap": 3,
        "description": "Adverb on dialogue tag \u2014 the dialogue should convey the tone",
    },
]

COMBINED_CAP = 5
