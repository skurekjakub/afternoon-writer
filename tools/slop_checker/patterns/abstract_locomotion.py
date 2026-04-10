"""Pattern definitions for: abstract_locomotion"""

PATTERNS = [
    {
        "name": "abstract_locomotion",
        "category": "abstract_locomotion",
        "regex": r'\b(?:memory|certainty|recognition|grief|fear|realization|understanding|dread|panic|shame|guilt|anger|rage|longing|relief|hope|despair|awareness|comprehension|knowledge|doubt|suspicion|disbelief|horror|fury|disgust|pity|tenderness|affection|warmth|coldness|regret|gratitude|sadness|sorrow|joy|resentment|confusion|anxiety|resignation)\s+(?:surfaced|moved|settled|crawled|crept|flooded|pooled|threaded|bloomed|washed|swept|rippled|rolled|spread|seeped|bled|slid|traveled|raced|rushed|hit|struck|slammed|crashed|surged|swelled|rose|climbed|descended|sank|dropped|fell|flickered|flared|burned|blazed|tightened|loosened|coiled|unwound|snaked|pulsed|throbbed|radiated)\b',
        "cap": 0,
        "description": "Abstract noun + movement verb \u2014 emotional labeling dressed in kinetic clothes",
    },
]

COMBINED_CAP = None
