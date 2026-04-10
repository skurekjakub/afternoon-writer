"""Regex-based interpretive pattern detector.

Catches structural patterns that indicate narrator interpretation, typological
sorting, vague pointing, and other interpretive filter violations. These
patterns can use concrete vocabulary and still fail the Artist Test — the
structural form is the violation, not the word choice.

Layer 2 of the skeleton strip hybrid (Layer 1 = concreteness scoring).
"""

import re
from dataclasses import dataclass


@dataclass
class PatternMatch:
    pattern_name: str
    category: str
    matched_text: str
    start: int
    end: int
    description: str


# Each pattern: name, category, compiled regex (IGNORECASE), description.
_PATTERN_DEFS = [
    # 1. "the expression/look/face of someone who..." — categorical face description
    {
        "name": "expression_of_someone",
        "category": "categorical_face",
        "regex": r"the\s+(?:expression|look|face|eyes|gaze|air|manner)\s+of\s+(?:someone|a\s+\w+)\s+who",
        "description": "Categorizes a face/expression by TYPE instead of describing physical detail",
    },
    # 2. "the kind of [noun] that..." — typological sorting
    {
        "name": "kind_of_noun_that",
        "category": "typological_sorting",
        "regex": r"the\s+(?:kind|sort|type)\s+of\s+\w+\s+that",
        "description": "Sorts into categories instead of describing the specific instance",
    },
    # 3. "something about [noun]" — vague pointing
    {
        "name": "something_about",
        "category": "vague_pointer",
        "regex": r"something\s+(?:about|in|behind)\s+(?:the\s+way|her|his|their|\w+['\u2019]?s?)\b",
        "description": "Points vaguely instead of naming the specific detail",
    },
    # 4. "the way [pronoun] [verb]ed suggested/implied/betrayed..." — action + interpretation
    {
        "name": "way_suggested",
        "category": "narrator_interpretation",
        "regex": r"the\s+way\s+(?:she|he|they|it|\w+)\s+\w+(?:ed|ing|s)?\s+(?:suggested|implied|betrayed|revealed|spoke\s+of|hinted|indicated|conveyed)",
        "description": "Narrates an action then interprets it instead of letting the action speak",
    },
    # 5. Inanimate thing "spoke of / suggested / betrayed / revealed"
    {
        "name": "inanimate_interpretation",
        "category": "personification",
        "regex": r"(?:the\s+)?(?:silence|stillness|darkness|posture|tone|voice|pause|air|gesture|movement|room)\s+(?:spoke\s+of|suggested|betrayed|revealed|announced|proclaimed|whispered\s+of|hinted\s+at)",
        "description": "Inanimate objects performing interpretation — describe what it looks like instead",
    },
    # 6. "as if [pronoun] had decided/chosen/understood..." — appended interpretation
    {
        "name": "as_if_interpretation",
        "category": "appended_interpretation",
        "regex": r"as\s+if\s+(?:she|he|they|it|the\s+\w+)\s+(?:had\s+)?(?:decided|chosen|made|determined|resolved|accepted|understood|realized|known|sensed|felt)",
        "description": "Appends narrator interpretation to a physical image — the image was enough",
    },
    # 7. Forced noun-metaphors: "she was a wall/mask/ghost/shadow..."
    {
        "name": "forced_noun_metaphor",
        "category": "metaphor_label",
        "regex": r"(?:she|he|they|it|I)\s+(?:was|had\s+become|became|felt\s+like)\s+(?:a|an|the)\s+(?:wall|mask|ghost|shadow|statue|stone|island|fortress|armor|furniture|weapon|tool|machine|mirror|anchor|beacon)\b",
        "description": "Labels a person as a metaphor-noun instead of describing their physical state",
    },
    # 8. "with the exact/precise/careful [noun] of" — mechanical process framing
    {
        "name": "mechanical_precision",
        "category": "process_framing",
        "regex": r"with\s+the\s+(?:exact|precise|careful|practiced|deliberate|studied|measured)\s+\w+\s+of",
        "description": "Frames a human action as a mechanical process instead of showing the action",
    },
    # 9. "felt a surge/wave/rush of [emotion]" — canned emotional label
    {
        "name": "emotion_surge",
        "category": "emotional_label",
        "regex": r"felt\s+a\s+(?:surge|wave|rush|flicker|pang|stab|jolt|flash|bloom|twist|knot)\s+of\s+(?:anger|fear|sadness|joy|grief|shame|guilt|pride|love|longing|dread|panic|relief|hope|despair|anxiety|rage|jealousy|envy|tenderness|warmth|cold|heat)",
        "description": "Labels an emotional state with a canned metaphor instead of showing through action",
    },
    # 10. "in a way that suggested/implied/made..." — appended interpretation
    {
        "name": "in_a_way_that",
        "category": "appended_interpretation",
        "regex": r"in\s+a\s+way\s+that\s+(?:suggested|implied|made\s+\w+|felt|seemed|reminded|spoke|hinted)",
        "description": "Appends interpretation to a description via 'in a way that' — cut the interpretation",
    },
    # 11. "the evidence of [abstract noun]" — evidence framing
    {
        "name": "evidence_of",
        "category": "process_framing",
        "regex": r"the\s+(?:evidence|proof|sign|signs|mark|marks|trace|traces)\s+of\s+(?:her|his|their|its|the)\s+(?:\w+tion|\w+ment|\w+ness|\w+ity|grief|fear|anger|exhaustion|effort|pain|struggle|distress)",
        "description": "Frames emotion/state as forensic evidence instead of showing it directly",
    },
    # 12. "not X but Y / not X; Y" dramatic negation
    {
        "name": "dramatic_negation",
        "category": "narrator_interpretation",
        "regex": r"not\s+\w+(?:\s+\w+){0,3}(?:\s*[;,\u2014]\s*|\s+but\s+)(?:\w+\s+){0,3}\w+",
        "description": "Dramatic negation pair — define what the thing IS, not what it isn't",
    },
]

# Compile all patterns once
_COMPILED = [
    {**p, "compiled": re.compile(p["regex"], re.IGNORECASE)}
    for p in _PATTERN_DEFS
]


def find_patterns(text: str) -> list[PatternMatch]:
    """Run all patterns against text. Return matches with positions."""
    matches: list[PatternMatch] = []
    for p in _COMPILED:
        for m in p["compiled"].finditer(text):
            matches.append(PatternMatch(
                pattern_name=p["name"],
                category=p["category"],
                matched_text=m.group(),
                start=m.start(),
                end=m.end(),
                description=p["description"],
            ))

    # Sort by position, dedup overlapping (keep longest)
    matches.sort(key=lambda m: (m.start, -(m.end - m.start)))
    deduped: list[PatternMatch] = []
    last_end = -1
    for m in matches:
        if m.start >= last_end:
            deduped.append(m)
            last_end = m.end
    return deduped


def find_patterns_in_text(text: str, sentence_texts: list[str]) -> dict[int, list[PatternMatch]]:
    """Map pattern matches back to sentence indices.

    Takes the full text and a list of sentence strings. Returns
    {sentence_index: [matches]} for sentences with hits.
    """
    all_matches = find_patterns(text)
    if not all_matches:
        return {}

    # Build sentence offset map
    result: dict[int, list[PatternMatch]] = {}
    offset = 0
    for i, sent in enumerate(sentence_texts):
        start = text.find(sent, offset)
        if start == -1:
            continue
        end = start + len(sent)
        offset = end
        for m in all_matches:
            if m.start >= start and m.end <= end:
                result.setdefault(i, []).append(m)
    return result
