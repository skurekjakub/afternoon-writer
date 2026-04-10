"""Pattern definitions for: body_cliches"""

PATTERNS = [
    {
        "name": "cliche_raised_eyebrow",
        "category": "body_cliches",
        "regex": r'\braised\s+(?:an?\s+)?eyebrow\b',
        "cap": 1,
        "description": "Body cliche: raised an eyebrow",
    },
    {
        "name": "cliche_crossed_arms",
        "category": "body_cliches",
        "regex": r'\bcrossed\s+(?:her|his|their|the)?\s*arms\b',
        "cap": 1,
        "description": "Body cliche: crossed arms",
    },
    {
        "name": "cliche_clenched_jaw",
        "category": "body_cliches",
        "regex": r'\bclenched\s+(?:her|his|their|the)?\s*jaw\b',
        "cap": 1,
        "description": "Body cliche: clenched jaw",
    },
    {
        "name": "cliche_rolled_eyes",
        "category": "body_cliches",
        "regex": r'\brolled\s+(?:her|his|their)?\s*eyes\b',
        "cap": 1,
        "description": "Body cliche: rolled eyes",
    },
    {
        "name": "cliche_heart_pounded",
        "category": "body_cliches",
        "regex": r'\bheart\s+(?:pounded|hammered|raced|thundered|slammed|skipped)\b',
        "cap": 1,
        "description": "Body cliche: heart pounded/hammered/raced",
    },
    {
        "name": "cliche_bit_lip",
        "category": "body_cliches",
        "regex": r'\bbit\s+(?:her|his|their)?\s*(?:lower\s+)?lip\b',
        "cap": 1,
        "description": "Body cliche: bit lip",
    },
    {
        "name": "cliche_stomach_dropped",
        "category": "body_cliches",
        "regex": r'\bstomach\s+(?:dropped|flipped|lurched|churned|knotted|clenched|sank|tightened)\b',
        "cap": 1,
        "description": "Body cliche: stomach dropped/flipped/lurched",
    },
    {
        "name": "cliche_tears_pricked",
        "category": "body_cliches",
        "regex": r'\btears\s+(?:pricked|stung|burned|blurred|welled|threatened)\b',
        "cap": 1,
        "description": "Body cliche: tears pricked/stung/burned",
    },
    {
        "name": "cliche_blood_ran_cold",
        "category": "body_cliches",
        "regex": r'\bblood\s+(?:ran|went|turned)\s+cold\b',
        "cap": 0,
        "description": "Body cliche: blood ran cold (zero tolerance)",
    },
    {
        "name": "cliche_furrowed_brow",
        "category": "body_cliches",
        "regex": r'\bfurrowed\s+(?:her|his|their)?\s*brows?\b',
        "cap": 1,
        "description": "Body cliche: furrowed brow",
    },
    {
        "name": "cliche_smile_tugged",
        "category": "body_cliches",
        "regex": r'\bsmile\s+tugged\b',
        "cap": 1,
        "description": "Body cliche: smile tugged",
    },
    {
        "name": "cliche_knuckles_white",
        "category": "body_cliches",
        "regex": r'\bknuckles\s+(?:white|whitened|went\s+white)\b',
        "cap": 1,
        "description": "Body cliche: knuckles white",
    },
]

COMBINED_CAP = None
