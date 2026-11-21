"""Pattern definitions for: gemini_prose_tics

Gemini 2.5 / 3 Pro creative-writing fingerprints empirically calibrated against
437,435 words of human fantasy prose (style-samples/travel.md: 380,906w;
style-samples/archmage/: 56,529w; 1:2 weighted blend).

Design rules:
- Zero-tolerance (cap: 0) patterns occur <= 0.01 times per 5K-word chapter in the
  human corpora (almost all occur literally 0 times in 437K words).
- Capped (cap: 1) patterns allow one earned instance per chapter while catching
  Gemini's repetitive reliance on the shape.
- COMBINED_CAP = 6 catches chapters that stay under each individual cap while
  accumulating Gemini fingerprints across subcategories.
"""

PATTERNS = [
    # --- 1. Period & em-dash negation pivots (beyond negation_addiction.py) ---
    {
        "name": "gemini_neg_wasnt_period",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(it|that|this|he|she|they)\s+(?:wasn['\u2019]t|weren['\u2019]t|was\s+not|were\s+not)\s+"
            r"(?!sure\b|certain\b|going\b|able\b|ready\b|supposed\b|there\b|here\b|looking\b|listening\b|paying\b)"
            r"[^.!?\n]{2,45}[.]\s+(?:it|that|this|\1)\s+(?:was|were)\b"
        ),
        "cap": 1,
        "description": "Gemini negation pivot: 'It wasn't X. It was Y.' (human blend 0.08/5K; max 1)",
    },
    {
        "name": "gemini_neg_wasnt_emdash",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:it|that|this|he|she|they)\s+(?:wasn['\u2019]t|weren['\u2019]t|was\s+not|were\s+not)\s+"
            r"[^.!?\u2014\n]{2,45}(?:\u2014|--)\s*(?:it|that|this|he|she|they)\s+(?:was|were)\b"
        ),
        "cap": 0,
        "description": "Gemini negation pivot: 'It wasn't X—it was Y.' (1 in 437K human words)",
    },
    {
        "name": "gemini_neg_not_emdash",
        "category": "gemini_prose_tics",
        "regex": (
            r"(?:^|[.!?]\s+)Not\s+(?:a\s+|an\s+|the\s+|just\s+|merely\s+|only\s+|out\s+of\s+)?"
            r"\w+(?:\s+\w+){0,3}\s*(?:\u2014|--)\s*[a-zA-Z]"
        ),
        "cap": 0,
        "description": "Gemini negation pivot: sentence-initial 'Not X—Y' (2 in 437K human words)",
    },
    {
        "name": "gemini_neg_not_merely_out_of",
        "category": "gemini_prose_tics",
        "regex": r"\bnot\s+(?:merely|simply|out\s+of)\s+\w+(?:\s+\w+){0,4},?\s+but\b",
        "cap": 0,
        "description": "Gemini negation pivot: 'not merely/simply/out of X, but Y' (0 in 437K human words)",
    },

    # --- 2. Sensory & atmospheric stock pairs / ozone & copper overload ---
    {
        "name": "gemini_scent_ozone",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:(?:scent|smell|tang|taste|whiff|odor|reek|sharpness)\s+of\s+ozone|ozone\s+and\s+\w+)\b",
        "cap": 1,
        "description": "Gemini sensory stock: ozone smell/taste/pair (0 in 437K human words; cap 1 for arcane magic tell)",
    },
    {
        "name": "gemini_copper_pair",
        "category": "gemini_prose_tics",
        "regex": r"\bcopper\s+and\s+(?:rot|iron|blood|ozone|ash|pine|smoke|salt|rust|wet\s+earth|damp\s+earth|old\s+iron|burnt\s+\w+)\b",
        "cap": 0,
        "description": "Gemini sensory stock: 'copper and [rot/iron/blood/ozone/ash/pine]' (0 in 437K human words)",
    },
    {
        "name": "gemini_metallic_tang",
        "category": "gemini_prose_tics",
        "regex": r"\bmetallic\s+tang\b",
        "cap": 0,
        "description": "Gemini sensory stock: 'metallic tang' (0 in 437K human words)",
    },
    {
        "name": "gemini_thick_with_scent",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:thick|heavy)\s+with\s+(?:the\s+)?(?:scent|smell|stench|odor)\s+of\b",
        "cap": 0,
        "description": "Gemini atmospheric stock: 'thick/heavy with the scent of' (1 in 437K human words)",
    },
    {
        "name": "gemini_bathed_in_light",
        "category": "gemini_prose_tics",
        "regex": (
            r"\bbathed\s+in\s+(?:the\s+)?(?:(?:pale|soft|cold|warm|golden|silver|amber|crimson|eerie|dim|faint|harsh|red|blue|white)\s+)?"
            r"(?:light|shadow|shadows|moonlight|firelight|sunlight|starlight|torchlight|candlelight|glow|darkness)\b"
        ),
        "cap": 0,
        "description": "Gemini atmospheric stock: 'bathed in [light/shadow/moonlight/firelight]' (0 in 437K human words)",
    },
    {
        "name": "gemini_pools_of_shadow",
        "category": "gemini_prose_tics",
        "regex": r"\bpools?\s+of\s+(?:shadow|shadows|darkness|light|moonlight|firelight)\b",
        "cap": 0,
        "description": "Gemini atmospheric stock: 'pools of shadow/darkness/light' (0 in 437K human words)",
    },
    {
        "name": "gemini_cast_long_shadows",
        "category": "gemini_prose_tics",
        "regex": r"\bcast(?:s|ing)?\s+(?:long|deep|stark|jagged|dancing|flickering)\s+shadows?\b",
        "cap": 0,
        "description": "Gemini atmospheric stock: 'cast long/deep/dancing shadows' (0 in 437K human words)",
    },
    {
        "name": "gemini_broken_only_by",
        "category": "gemini_prose_tics",
        "regex": r"\bbroken\s+only\s+by\b",
        "cap": 0,
        "description": "Gemini atmospheric stock: 'broken only by' (1 in 437K human words)",
    },
    {
        "name": "gemini_shattered_silence",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:shattered|pierced|sliced|cut\s+through|split|ruptured|fractured)\s+"
            r"(?:the\s+)?(?:(?:heavy|thick|oppressive|fragile|tense|quiet|still|night|sudden)\s+)?silence\b"
        ),
        "cap": 0,
        "description": "Gemini atmospheric stock: 'shattered/pierced/cut through the silence' (0 in 437K human words)",
    },
    {
        "name": "gemini_deafening_silence",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:deafening|suffocating|oppressive|crushing|stifling|tangible)\s+silence\b",
        "cap": 0,
        "description": "Gemini atmospheric stock: 'deafening/suffocating/oppressive silence' (0 in 437K human words)",
    },

    # --- 3. Abstract-noun 'X of Y' cinematic nominalizations ---
    {
        "name": "gemini_ghost_of_smile",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:a\s+|the\s+)?ghost\s+of\s+(?:a\s+|an\s+)?(?:smile|grin|smirk|laugh|chuckle|frown|thought|memory|doubt|hesitation)\b",
        "cap": 0,
        "description": "Gemini nominalization: 'a ghost of a smile/grin/thought' (0 in 437K human words)",
    },
    {
        "name": "gemini_flicker_of_emotion",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:a\s+|the\s+)?flicker\s+of\s+"
            r"(?:something|emotion|fear|dread|anger|fury|rage|guilt|grief|pain|hurt|doubt|hope|relief|"
            r"warmth|amusement|annoyance|irritation|panic|recognition|understanding|uncertainty|hesitation|"
            r"vulnerability|surprise|shock|concern|alarm|regret|shame|pride|triumph|sympathy|pity|jealousy|"
            r"discomfort|unease|malice|cruelty|respect|admiration|affection|longing|desire|want)\b"
        ),
        "cap": 0,
        "description": "Gemini nominalization: 'a flicker of [emotion]' (0 in 437K human words)",
    },
    {
        "name": "gemini_veneer_facade",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:(?:veneer|facade)\s+of|"
            r"mask\s+of\s+(?:calm|composure|indifference|detachment|civility|politeness|professionalism|"
            r"control|authority|confidence|coldness|aloofness|serenity|normalcy|neutrality|warmth|anger|"
            r"hostility|boredom|amusement|charm))\b"
        ),
        "cap": 0,
        "description": "Gemini nominalization: 'veneer/facade/mask of [state]' (0 in 437K human words)",
    },
    {
        "name": "gemini_symphony_labyrinth",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:symphony|crescendo|kaleidoscope|labyrinth|cacophony|maelstrom|crucible)\s+of\b",
        "cap": 0,
        "description": "Gemini nominalization: 'symphony/crescendo/kaleidoscope/labyrinth of' (3 in 437K human words)",
    },
    {
        "name": "gemini_sheer_weight_of",
        "category": "gemini_prose_tics",
        "regex": r"\bthe\s+(?:sheer|crushing|sudden|quiet|heavy|immense|unbearable|suffocating)\s+weight\s+of\b",
        "cap": 0,
        "description": "Gemini nominalization: 'the sheer/crushing weight of' (1 in 437K human words)",
    },
    {
        "name": "gemini_sliver_of_abstract",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:a\s+|the\s+)?sliver\s+of\s+"
            r"(?:hope|doubt|fear|dread|guilt|relief|warmth|cold|ice|panic|truth|clarity|recognition|"
            r"understanding|memory|hesitation|vulnerability|amusement|satisfaction|triumph|pride|"
            r"mercy|grace|sanity|control|peace)\b"
        ),
        "cap": 0,
        "description": "Gemini nominalization: 'a sliver of [abstract noun]' (0 in 437K human words)",
    },
    {
        "name": "gemini_echo_of_abstract",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:an?\s+|the\s+)?echo(?:es)?\s+of\s+(?:a\s+|the\s+|her\s+|his\s+|their\s+)?"
            r"(?:past|memory|memories|grief|loss|pain|fear|anger|guilt|laughter|promise|threat|violence|war|something)\b"
        ),
        "cap": 0,
        "description": "Gemini nominalization: 'an echo of [grief/past/memory/...]'(0 in 437K human words)",
    },

    # --- 4. Interiority shortcut: 'something in her [body] shifted' ---
    {
        "name": "gemini_something_body_shifted",
        "category": "gemini_prose_tics",
        "regex": (
            r"\bsomething\s+(?:"
            r"(?:(?:deep\s+)?(?:in|inside|within)\s+(?:her|his|their)\s+(?:chest|gut|stomach|ribs|throat|core|belly|mind|head|bones|spine|blood)|"
            r"(?:inside|within)\s+(?:her|him|them))|"
            r"(?:cold|warm|sharp|heavy|tight|hard|hollow|dark|small|fragile|ugly|old|quiet)"
            r")\s+(?:shifted|tightened|snapped|twisted|curled|sank|uncoiled|clenched|cracked|loosened|"
            r"settled|flared|flickered|knotted|dropped|lurched|hardened|softened|hollowed|stilled|broke|coiled|gave\s+way)\b"
        ),
        "cap": 0,
        "description": "Gemini interiority shortcut: 'something in her [chest/gut] shifted/tightened' (0 in 437K human words)",
    },

    # --- 5. Evaluative defining-clause tic ---
    {
        "name": "gemini_the_kind_of_that",
        "category": "gemini_prose_tics",
        "regex": r"\bthe\s+(?:kind|sort)\s+of\s+\w+(?:\s+\w+){0,2}\s+(?:that|who|which)\b",
        "cap": 1,
        "description": "Gemini evaluative clause: 'the kind/sort of [noun] that [verb]' (3 in 437K human words; max 1)",
    },

    # --- 6. Dramatic micro-time, stingers, clinical/predatory modifiers, double-barrel adj ---
    {
        "name": "gemini_micro_time",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:"
            r"(?:for\s+)?(?:a\s+fraction\s+of\s+a\s+second|a\s+split\s+second)|"
            r"for\s+(?:a\s+single|one|two|three|the\s+space\s+of\s+a|a)\s+heartbeats?|"
            r"a\s+heartbeat\s+later"
            r")\b"
        ),
        "cap": 1,
        "description": "Gemini micro-time padding: 'for a fraction of a second / single heartbeat' (3 in 437K human words; max 1)",
    },
    {
        "name": "gemini_one_thing_certain",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:one\s+thing\s+was\s+(?:certain|clear|obvious|sure|undeniable|plain)|"
            r"only\s+one\s+thing\s+(?:remained|mattered)|one\s+truth\s+remained)\b"
        ),
        "cap": 0,
        "description": "Gemini stinger setup: 'one thing was certain / only one thing remained' (0 in 437K human words)",
    },
    {
        "name": "gemini_razor_precision",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:razor[- ](?:sharp|thin)|"
            r"(?:surgical|clinical|deadly|lethal|cold|mechanical|practiced|calculated)\s+precision|"
            r"(?:lethal|predatory|fluid|effortless|feline|deadly)\s+grace)\b"
        ),
        "cap": 0,
        "description": "Gemini stock modifier: 'razor-sharp/thin', 'surgical/clinical precision', 'lethal/predatory grace' (1 in 437K human words)",
    },
    {
        "name": "gemini_clinical_bleed",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:architect(?:ure)?\s+of\s+(?:the|her|his|their|a)\b|"
            r"symbio(?:sis|tic)\b|"
            r"kinetic\s+(?:energy|force|impact|fury|grace)\b|"
            r"calibrated\s+(?:to|for|with|precision|calm|smile|tone|voice)\b|"
            r"clinical\s+(?:detachment|efficiency|calm)\b)"
        ),
        "cap": 0,
        "description": "Gemini clinical/technical register bleed: 'architect of', 'calibrated', 'clinical detachment', 'kinetic' (0 in 437K human words)",
    },
    {
        "name": "gemini_un_adjectives",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:unyielding|unflinching(?:ly)?|unwavering(?:ly)?|unreadable)\b",
        "cap": 1,
        "description": "Gemini stock 'un-' adjectives: unyielding/unflinching/unwavering/unreadable (5 in 437K human words; max 1)",
    },
    {
        "name": "gemini_double_barrel_adj",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:a|an)\s+(?:measured|deliberate|calculated|practiced|controlled|clinical|rhythmic|metronomic|"
            r"predatory|methodical|surgical|sharp|cold|slow|low|flat|hollow|fragile|brittle|taut|stark|visceral|"
            r"jagged|muted|quiet|steady|clipped),\s+"
            r"(?:measured|deliberate|calculated|practiced|controlled|clinical|rhythmic|metronomic|predatory|"
            r"methodical|surgical|sharp|cold|slow|low|flat|hollow|fragile|brittle|taut|stark|visceral|jagged|"
            r"muted|quiet|steady|even|precise|clean|forced|careful|heavy|sudden|quick|brief|faint|thin|clipped|resonant)\s+\w+\b"
        ),
        "cap": 0,
        "description": "Gemini double-barrel adjective pair: 'a measured, clinical <noun>' (0 in 437K human words)",
    },
    {
        "name": "gemini_stinger_paragraph",
        "category": "gemini_prose_tics",
        "regex": (
            r"(?:^|(?<=\n\n))(?:"
            r"Silence|Nothing|Too\s+late|Gone|Finally|Again|Still|Always|Never|Enough|Almost|Wrong|"
            r"Alone|Empty|Darkness|Quiet|Dead|Over|Done|Perfect|Simple|Impossible|Inevitably|Instantly|Suddenly"
            r")[.!](?=\s*(?:\n\n|$))"
        ),
        "cap": 1,
        "description": "Gemini dramatic stinger paragraph: isolated 1-2 word punchline ('Silence.', 'Too late.') (4 in 437K human words; max 1)",
    },

    # --- 7. Slow-burn romance cliche guard ---
    {
        "name": "gemini_romance_breath_hitched",
        "category": "gemini_prose_tics",
        "regex": r"\bbreath\s+hitched\b",
        "cap": 0,
        "description": "Gemini romance cliche: 'breath hitched' (0 in 437K human words)",
    },
    {
        "name": "gemini_romance_pulse_spiked",
        "category": "gemini_prose_tics",
        "regex": r"\bpulse\s+(?:spiked|fluttered|jumped|leaped|leapt|stuttered|quickened|thrummed|pounded|raced|hammered|tripped|kicked)\b",
        "cap": 0,
        "description": "Gemini romance cliche: 'pulse spiked/fluttered/quickened' (0 in 437K human words)",
    },
    {
        "name": "gemini_romance_heat_pooled",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:heat|warmth|desire|want)\s+(?:pooled|bloomed|coiled|curled|flared|unfurled)\b",
        "cap": 0,
        "description": "Gemini romance cliche: 'heat pooled / warmth bloomed' (0 in 437K human words)",
    },
    {
        "name": "gemini_romance_gaze_lips",
        "category": "gemini_prose_tics",
        "regex": r"\b(?:gaze|eyes)\s+(?:dropped|flicked|dipped|drifted|fell|darted)\s+(?:down\s+)?to\s+(?:her|his|their)\s+(?:lips|mouth)\b",
        "cap": 0,
        "description": "Gemini romance cliche: 'gaze/eyes dropped to her lips' (0 in 437K human words)",
    },
    {
        "name": "gemini_romance_magnetic_pull",
        "category": "gemini_prose_tics",
        "regex": (
            r"\b(?:magnetic\s+pull|"
            r"invisible\s+(?:thread|tether|cord|string|wire|pull)\s+between|"
            r"electricity\s+(?:arced|crackled|passed|hummed)\s+between|"
            r"spark\s+(?:passed|jumped|arced|flared)\s+between|"
            r"(?:hyper[- ]aware|acutely\s+aware|painfully\s+aware)\s+of)\b"
        ),
        "cap": 0,
        "description": "Gemini romance cliche: 'magnetic pull', 'invisible thread between', 'hyper-aware of' (0 in 437K human words)",
    },
]

COMBINED_CAP = 6
