"""Pattern definitions for: hedging"""

PATTERNS = [
    {
        "name": "hedge_almost",
        "category": "hedging",
        "regex": r'\balmost\b',
        "cap": 6,
        "description": "Hedging: almost",
    },
    {
        "name": "hedge_seemed",
        "category": "hedging",
        "regex": r'\bseemed\b',
        "cap": 6,
        "description": "Hedging: seemed",
    },
    {
        "name": "hedge_slightly",
        "category": "hedging",
        "regex": r'\bslightly\b',
        "cap": 2,
        "description": "Hedging: slightly",
    },
    {
        "name": "hedge_somewhat",
        "category": "hedging",
        "regex": r'\bsomewhat\b',
        "cap": 1,
        "description": "Hedging: somewhat",
    },
    {
        "name": "hedge_perhaps",
        "category": "hedging",
        "regex": r'\bperhaps\b',
        "cap": 6,
        "description": "Hedging: perhaps",
    },
    {
        "name": "hedge_simply",
        "category": "hedging",
        "regex": r'\bsimply\b',
        "cap": 2,
        "description": "Hedging: simply",
    },
    {
        "name": "hedge_somehow",
        "category": "hedging",
        "regex": r'\bsomehow\b',
        "cap": 2,
        "description": "Hedging: somehow",
    },
    {
        "name": "hedge_seemed_to",
        "category": "hedging",
        "regex": r'\bseemed\s+to\s+\w+',
        "cap": 3,
        "description": "Hedging: 'seemed to [verb]' \u2014 narrator refusing to commit",
    },
    {
        "name": "hedge_appeared_to",
        "category": "hedging",
        "regex": r'\bappeared\s+to\s+\w+',
        "cap": 1,
        "description": "Hedging: 'appeared to [verb]'",
    },
    {
        "name": "hedge_might_have_been",
        "category": "hedging",
        "regex": r'\bmight\s+have\s+been\b',
        "cap": 1,
        "description": "Hedging: 'might have been'",
    },
    {
        "name": "hedge_something_like",
        "category": "hedging",
        "regex": r'\bsomething\s+like\s+(?:a\s+)?(?:relief|anger|fear|sadness|happiness|joy|pride|tenderness|affection|warmth|amusement|recognition|a\s+smile|a\s+laugh|a\s+noise|a\s+sound|comfort|hope|regret)\b',
        "cap": 0,
        "description": "Hedging: 'something like [emotion/expression]' (zero tolerance)",
    },
    {
        "name": "hedge_could_only_be_described",
        "category": "hedging",
        "regex": r'\b(?:could|can)\s+only\s+be\s+described\s+as\b',
        "cap": 0,
        "description": "Hedging: 'could only be described as' (zero tolerance)",
    },
    {
        "name": "hedge_hint_trace_touch_of",
        "category": "hedging",
        "regex": r'\ba\s+(?:hint|trace|touch)\s+of\s+(?:sadness|bitterness|amusement|fear|anger|warmth|coldness|regret|something|color|colour|humor|humour|irony|sarcasm|desperation|madness|panic)\b',
        "cap": 1,
        "description": "Hedging: 'a hint/trace/touch of [emotion]'",
    },
]

COMBINED_CAP = None
