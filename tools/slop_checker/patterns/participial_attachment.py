"""Pattern definitions for: participial_attachment"""

PATTERNS = [
    {
        "name": "participial_trailing",
        "category": "participial_attachment",
        "regex": r',\s+(?:pulling|pushing|turning|reaching|settling|studying|watching|holding|gripping|pressing|tracing|running|feeling|letting|keeping|making|taking|giving|looking|moving|leaning|lifting|dropping|closing|opening|drawing|wrapping|sliding|shifting|crossing|tucking|rubbing|brushing|catching|scanning|searching|trying|waiting|sending|trailing|leaving|carrying|dragging|fighting|forcing|allowing|ignoring|avoiding|creating|bringing)\s+\w+',
        "cap": 5,
        "cap_per_words": 250,
        "description": "Trailing participial phrase: ', [verb]ing [noun]' \u2014 implies false simultaneity (1 per 250 words)",
    },
]

COMBINED_CAP = None
