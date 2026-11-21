"""Mannered-prose and refrain checker — deterministic hints for slop-gate pass C.

Two jobs:

1. Mannered shapes. Surfaces the "literary competence" tics that survive
   passes A and B: bent idioms, equative montage ("the night had been fire and
   a cage and..."), comic self-consciousness ("didn't know what to do about
   having stood"), maxims, interpreter glosses, "the way" similes, self-hearing
   and involuntary-action beats, and so on. Pattern codes (M1-M13) match
   resources/mannered-prose-guide.md.

2. Refrains. Finds wording and signature beats the book has already used:
   - cross-chapter: 5-word runs shared with earlier chapters' final.md
   - within-chapter: 5-word runs repeated inside the target
   - voice sheets: 5-word runs lifted from voice-sheet example lines
   - families: recurring signature beats with per-chapter and rolling budgets
     (tools/mannered_checker/refrain_families.json)
   Shared runs that also occur in the reference corpora are dropped as
   ordinary English.

Caps are calibrated. The human reference corpora (`priming.humanCorpora` in
.afternoon/config.json) are measured by calibrate.py into calibration.json.
For each pattern the cap is HEADROOM times the blended human rate scaled to
the chapter's length. A pattern the reference prose uses under ZERO_RELEASE
times per 10K words gets a cap of zero: human prose doesn't do it, so neither
should the book. The guide defaults apply only when there is no calibration.
When the corpora change (a sample added, removed or edited), the next run
recalibrates automatically.

The tool surfaces candidates. The gate reads context and decides KILL/KEEP.

Usage:
    python3 tools/mannered_checker/check.py --json .afternoon/chapters/chapter5/v2.md
    python3 tools/mannered_checker/check.py --summary .afternoon/chapters/chapter5/v2.md
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys
from array import array
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
FAMILIES_PATH = os.path.join(os.path.dirname(__file__), "refrain_families.json")
CALIBRATION_PATH = os.path.join(os.path.dirname(__file__), "calibration.json")
CONFIG_PATH = os.path.join(REPO_ROOT, ".afternoon", "config.json")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

from tools.prose_core.text import (  # noqa: E402  (needs REPO_ROOT on sys.path)
    QUOTE_RE,
    LineIndex,
    context,
    line_of,
    narration_only,
    normalise_quotes,
    paragraph_spans as paragraphs,
    read_text,
    strip_headers,
)

NGRAM = 5
MAX_LISTED = 40
HEADROOM = 2.0       # a chapter may run up to twice the human rate before a pattern is over cap
ZERO_RELEASE = 0.5   # per 10K words; human use above this turns a zero-tolerance pattern into a capped one

# Guide caps that apply to a whole code rather than one detector.
CODE_DEFAULT_CAPS = {"M4": 1, "M5": 2, "M7": 2, "M11": 1, "M13": 2}

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

# QUOTE_RE, normalise_quotes, strip_headers, narration_only, line_of, context and
# paragraphs come from tools.prose_core.text (imported above).


def sentence_spans(text: str):
    """Yield (start, end) for each sentence, roughly."""
    for m in re.finditer(r"[^.!?\n]+(?:[.!?]+[\"”]?|\n|$)", text):
        if m.group(0).strip():
            yield m.start(), m.end()


# ---------------------------------------------------------------------------
# Mannered patterns
# ---------------------------------------------------------------------------

# scope: "all" = whole text, "narr" = quoted speech blanked out
PATTERNS = [
    # M1 bent idiom — regression seeds only; the guide owns detection.
    {"name": "bent_idiom_seed", "code": "M1", "scope": "all", "cap": 0,
     "regex": r"\bchoose (?:her|his|its|their) own feet\b|\bbefore the (?:question|word|order|answer) was cold\b|\bhad nothing to put in it\b|\bbadly enough to taste\b|\bdown as maps\b",
     "description": "Known bent idiom. Say the idiom straight or say the thing plainly."},
    # M3 equative montage
    {"name": "equative_montage", "code": "M3", "scope": "narr", "cap": 0,
     "regex": r"\b(?:night|day|morning|evening|afternoon|week|month|summer|winter|spring|autumn|road|ride|journey|march|village|town)\b[^.!?;\n]{0,30}\b(?:had been|was|were)\s+(?!a\b|an\b|the\b|not\b|over\b|still\b|long\b|cold\b|dark\b|quiet\b|hot\b|warm\b|clear\b|wet\b|going\b|coming\b|nearly\b|almost\b|already\b|young\b|late\b|early\b|bright\b|grey\b|gone\b|done\b|empty\b|full\b|out\b|up\b)[a-z]+[^.!?;\n]{0,60}\band\b[^.!?;\n]{0,50}\band\b",
     "description": "A stretch of time or a place summed as a list of images ('the night had been fire and a cage and...')."},
    {"name": "equative_single", "code": "M3", "scope": "narr", "cap": 0,
     "regex": r"\b(?:After that|Then|By then|Now) the (?:night|day|morning|world|journey|ride) was the \w+(?: \w+)?\.|\bEvery (?:breath|word|moment|step|hour|minute) (?:she|he|they) (?:spent|wasted|took)[^.!?\n]{0,30} was an? \w+\.",
     "description": "Copula metaphor: 'the night was the river road', 'every breath was a furlong'."},
    # M4 cadence list with a turn
    {"name": "list_turn_seed", "code": "M4", "scope": "narr", "cap": 0,
     "regex": r",? and (?:nobody|no one|nothing) \w+ing\b|\b(?:at|with) (?:horses|strangers|him|her), (?:at|with) [^,.!?\n]{1,30}, (?:at|with) (?:nothing|nobody|the \w+)\b|,? and (?:the cat|a while|nobody knocking)\b",
     "description": "List whose last item is the joke, the void or the sigh ('and a lamp, and nobody knocking')."},
    # M5 maxims — see maxim_candidates() for the heuristic sweep.
    # M6 comic self-consciousness
    {"name": "did_not_know_what_to_do", "code": "M6", "scope": "all", "cap": 0,
     "regex": r"\b(?:didn'?t|did not) know what (?:else )?to do (?:about|with)\b",
     "description": "'didn't know what to do about/with X' — comic awkwardness narration."},
    {"name": "having_nominal", "code": "M6", "scope": "all", "cap": 0,
     "regex": r"\b(?:about|of|at|for|with) having (?:\w+ed|stood|said|been|done|gone|come|spoken|seen|thought|sat|run|risen|got|made|let)\b",
     "description": "An action just done turned into an object of feeling ('about having stood')."},
    {"name": "comic_recursion_seed", "code": "M6", "scope": "narr", "cap": 0,
     "regex": r"\bat once and managed neither\b|\bthe rest of (?:him|her|them) caught up\b|\bas if (?:it|she|he) had been hoping to\b|\b(?:furious|cross|annoyed) with it\b|\bwhich took a while(?: again)?\b|\bShe was trying to\.|\bHe was trying to\.",
     "description": "Comic narration of a body or animal lagging its own action."},
    # M7 self-monitoring
    {"name": "self_hearing", "code": "M7", "scope": "all", "cap": 0,
     "regex": r"\b(?:heard|hears|hearing) (?:herself|himself|themselves|myself)\b|\bheard what (?:she|he|they|I)(?:'d| had)? (?:just )?said\b",
     "description": "'She heard herself' — the character auditing her own speech."},
    {"name": "involuntary_action", "code": "M7", "scope": "all", "cap": 0,
     "regex": r"\bwithout meaning to\b|\bbefore (?:she|he|they|I) (?:could help it|could stop (?:herself|himself|themselves)|meant to|knew (?:it|she|he|they) had)\b|\bof (?:its|their|her|his) own accord\b|\bcouldn'?t have said when\b|\b(?:higher|louder|sharper) than (?:she|he) meant(?: it)?(?: to)?\b",
     "description": "Involuntary-action beat: 'before she meant to', 'of their own accord'."},
    {"name": "blush", "code": "M7", "scope": "all", "cap": 0,
     "regex": r"\b(?:ears|face|cheeks|neck) (?:went|going|had gone|were going|was going|had begun to go|came up) (?:red|hot|pink|scarlet)\b|\bwent red (?:to|at|right)\b",
     "description": "Blush beat (ears/face went red or hot)."},
    # M8 interpreter gloss
    {"name": "gloss_which", "code": "M8", "scope": "narr", "cap": 0,
     "regex": r",\s*which (?:meant|was as much as to say|was to say|was (?:more|less|worse|better|pointless|low|unfair|fair|something|nothing|likeliest|the point)\b)",
     "description": "', which meant...' — narration translating what the reader just saw."},
    {"name": "would_have_to_do_for", "code": "M8", "scope": "narr", "cap": 0,
     "regex": r"\bwould have to do for \w+\b|\bwas as good as (?:a|an) \w+\b",
     "description": "Gesture translated into its meaning ('It would have to do for thank you')."},
    # M10 planted echo inserts — see insert_candidates().
    # M11 stylised figures
    {"name": "tautology", "code": "M11", "scope": "all", "cap": 0,
     "regex": r"\b(?:[Aa]|[Aa]n|[Oo]ne) (\w+) (?:was|is) (?:a|an|one|just a) \1\b",
     "description": "Tautology punchline ('A doe was a doe')."},
    {"name": "anadiplosis", "code": "M11", "scope": "narr", "cap": 0,
     "regex": r"\b(\w{4,}), and \1 (?:was|is|had|did|would)\b",
     "description": "Anadiplosis flourish ('was clean, and clean was no use to her')."},
    # M12 argument templates
    {"name": "then_fragment", "code": "M12", "scope": "narr", "cap": 1,
     "regex": r"(?:^|[.!?]\s+)[A-Z][a-z']+(?: [a-z']+){0,3}, then\.",
     "description": "'Bad luck, then.' / 'Wrong, then.' — deduction fragment."},
    {"name": "second_guess_tag", "code": "M12", "scope": "narr", "cap": 0,
     "regex": r",\s*or (?:she|he|they|I) (?:only )?(?:thought|imagined) (?:it|so|it did)\b|,\s*or the \w+ (?:was|were) (?:putting|making|giving) it\b",
     "description": "'..., or she only thought it did' — second-guess tag."},
    {"name": "self_address", "code": "M12", "scope": "narr", "cap": 1,
     "regex": r"(?:^|[.!?]\s+)(?:[A-Z][a-z']+(?: [a-z']+){0,3}), (?:Jaina|Ranger-General|[Mm]age|Proudmoore|Sylvanas|Windrunner)\.",
     "description": "Sarcastic self-address in free indirect thought ('Brilliant, Jaina.')."},
    # M13 "the way" simile habit
    {"name": "the_way_simile", "code": "M13", "scope": "narr", "cap": 2,
     "regex": r",\s+(?:just |exactly |much )?the way (?!to\b|back\b|out\b|in\b|down\b|up\b|through\b|home\b|north|south|east|west|of\b|forward\b|ahead\b|over\b|across\b|along\b)\w+|(?<!,)(?<![Oo]n)(?<![Aa]ll)(?<![Bb]y) the way (?:a|an|any|every|some|people|men|women|children|horses|cattle|sheep) \w+",
     "description": "', the way a man does X when Y' simile."},
]

_COMPILED = [{**p, "compiled": re.compile(p["regex"], re.MULTILINE)} for p in PATTERNS]

_VERB_BASES = """
keep run leave turn go take get do stop swear hop dig stare follow cut hold know want come stay make put
pick walk drag sit stand look say tell give find think need mean break buy sell pay eat drink sleep ride
lay sift fill pour burn rot spoil drain sink float wait watch listen hear smell taste feel learn forget
remember trust lie cheat steal hide fight flee bolt shy kick bite bark bleed heal grow die live work
pull push throw catch carry try cry hurry worry bury marry fly dry fry deny copy reach teach fetch wash
wish brush rush push miss pass cross kiss press dress guess toss mix fix fax box
""".split()


def _third_person(base: str) -> str:
    if base.endswith("y") and base[-2] not in "aeiou":
        return base[:-1] + "ies"
    if base.endswith(("s", "sh", "ch", "x", "z")) or base in ("go", "do"):
        return base + "es"
    return base + "s"


PRESENT_VERB = r"(?:" + "|".join(sorted({_third_person(b) for b in _VERB_BASES}, key=len, reverse=True)) + r")"
PRESENT_AUX = r"(?:doesn't|does not|don't|isn't|aren't|can't|won't|is never|is always|was never|was always|were never|were always|never|always)"
GENERIC_NP = (
    r"(?:(?:A|An|Any|Every|No) (?!one\b)(?:[a-z']+ ){0,2}[a-z']+"
    r"|Nobody|Everybody|Everyone|Everything|Nothing|No one|People|Men|Women|Humans|Elves|Children|Sheep|Deer|Horses|Dogs|Cattle|Spies|Rangers|Soldiers|Mages|Clerks|Carters)"
    r"(?: (?:in|with|on|at|from|without|of) (?:a|an|the|his|her|this|that) (?:[a-z']+ )?[a-z']+)?"
)
ADVERB = r"(?: (?:always|never|only|just|still|usually|all|ever))?"
MAXIM_START = re.compile(
    r"^(?:On \w+,? |In \w+,? |At \w+,? )?" + GENERIC_NP + ADVERB + r" (?:" + PRESENT_VERB + r"|" + PRESENT_AUX + r")\b",
    re.IGNORECASE,
)
MAXIM_AFTER_CONJ = re.compile(
    r"\b(?:because|since|for|as|and|but|so|when|if) " + GENERIC_NP + ADVERB
    + r" (?:" + PRESENT_VERB + r"|" + PRESENT_AUX + r")\b",
    re.IGNORECASE,
)
MAXIM_COPULA = re.compile(r"^(?:A|An) [a-z']+(?: [a-z']+)? (?:was|is) (?:never|always) \w+")


def maxim_candidates(text: str, narr: str):
    """Generic present-tense truths in past-tense narration and their dialogue cousins. Heuristic."""
    hits = []
    for a, b in sentence_spans(narr):
        sent = narr[a:b].strip()
        if not 3 <= len(sent.split()) <= 34:
            continue
        if MAXIM_START.search(sent) or MAXIM_AFTER_CONJ.search(sent) or MAXIM_COPULA.search(sent):
            hits.append((a, b, sent))
    for m in QUOTE_RE.finditer(text):
        quote = m.group(0)[1:-1]
        # A quoted sentence ends in . ! ? or, when a dialogue tag follows, in a comma
        # at the end of the quote ('"A dry well never fills twice," he said.').
        for sm in re.finditer(r"(?:^|(?<=[.!?] ))([^.!?]{3,120}(?:[.!?]|,(?=\s*$)))", quote):
            s = sm.group(1).strip()
            if MAXIM_START.search(s):
                start = m.start() + 1 + sm.start(1)
                hits.append((start, start + len(s), s))
    return hits


SMALL_THINGS = r"(?:wasp|moth|fly|flies|beetle|spider|bird|birds|crow|rook|rooks|jay|jays|finch|cat|dog|candle|flame|leaf|leaves|swallow|swallows|mouse|rat|kettle|clock|bell)"
INSERT_RE = re.compile(r"^(?:The|A|An|At the foot of [^,]+, the) " + SMALL_THINGS + r"\b[^\n]{0,140}[.!?]$")


def insert_candidates(text: str, narr: str):
    """One-sentence narration paragraphs about a small creature or object."""
    hits = []
    for a, b, body in paragraphs(narr):
        para = body.strip()
        if "\n" in para or len(re.findall(r"[.!?]", para)) > 2:
            continue
        if INSERT_RE.match(para):
            off = a + body.find(para)
            hits.append((off, off + len(para), para))
    return hits


IRREGULAR = {"held": "hold", "made": "make", "went": "go", "got": "get", "came": "come",
             "took": "take", "gave": "give", "sat": "sit", "stood": "stand", "said": "say",
             "ran": "run", "rode": "ride", "drew": "draw", "kept": "keep", "left": "leave"}


def _stem(word: str) -> str:
    w = IRREGULAR.get(word.lower(), word.lower())
    for suffix in ("ing", "ed", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[: -len(suffix)]
    return w


def echo_compliance(text: str):
    """A short spoken command followed by a short narration line doing exactly it."""
    hits = []
    paras = list(paragraphs(text))
    for i, (a, b, body) in enumerate(paras[:-1]):
        for qm in QUOTE_RE.finditer(body):
            sentences_in_quote = [s for s in re.split(r"(?<=[.!?])\s+", qm.group(0)[1:-1].strip()) if s]
            cmd = sentences_in_quote[-1] if sentences_in_quote else ""
            cmd_words = re.findall(r"[A-Za-z']+", cmd)
            if not cmd_words or len(cmd_words) > 4:
                continue
            na, nb, nbody = paras[i + 1]
            nxt = nbody.strip()
            if QUOTE_RE.search(nxt) or len(nxt.split()) > 7:
                continue
            stems = {_stem(w) for w in cmd_words if len(w) > 2}
            if stems & {_stem(w) for w in re.findall(r"[A-Za-z']+", nxt) if len(w) > 2}:
                off = na + nbody.find(nxt)
                hits.append((off, off + len(nxt), f'"{cmd}" -> {nxt}'))
    return hits


def polysyndeton_density(narr: str, words: int, calib=None):
    """Narration sentences carrying three or more 'and's."""
    spans = [(a, b) for a, b in sentence_spans(narr) if len(re.findall(r"\band\b", narr[a:b])) >= 3]
    per10k = round(len(spans) * 10000 / words, 1) if words else 0.0
    by_para = defaultdict(int)
    para_index = [(a, b) for a, b, _ in paragraphs(narr)]
    for a, _ in spans:
        for pa, pb in para_index:
            if pa <= a < pb:
                by_para[(pa, pb)] += 1
                break
    lines = LineIndex(narr)
    dense = [{"line": lines.line(pa), "count": n} for (pa, pb), n in sorted(by_para.items()) if n >= 2]
    human = (calib or {}).get("polysyndetonPer10k")
    soft_cap = round(max(3.0, human * HEADROOM), 1) if human is not None else None
    return {"count": len(spans), "per10k": per10k, "humanPer10k": human, "softCapPer10k": soft_cap,
            "overSoftCap": soft_cap is not None and per10k > soft_cap, "densestParagraphs": dense[:MAX_LISTED]}


def calibrated_cap(default: int, human_per10k, words: int) -> int:
    """The human rate decides: HEADROOM x that rate at this chapter length, and zero for a pattern
    the reference prose uses under ZERO_RELEASE per 10K words. The guide default applies only
    when there is no calibration."""
    if human_per10k is None:
        return default
    if human_per10k < ZERO_RELEASE:
        return 0
    return math.ceil(human_per10k * words / 10000 * HEADROOM)


def run_patterns(text: str, calib=None):
    """Run every detector. calib is the calibration blend (None during calibration itself)."""
    narr = narration_only(text)
    words = len(text.split())
    rates = (calib or {}).get("patternsPer10k", {})
    lines = LineIndex(text)  # narr has the same offsets as text
    results = []

    def add(name, code, default_cap, desc, spans):
        matches = [{"line": lines.line(a), "text": t.strip()[:200], "context": context(text, a, b)}
                   for a, b, t in spans]
        human = rates.get(name) if calib else None
        cap = calibrated_cap(default_cap, human, words)
        here = round(len(matches) * 10000 / words, 2) if words else 0.0
        results.append({"name": name, "code": code, "cap": cap, "guideCap": default_cap, "count": len(matches),
                        "overCap": len(matches) > cap, "per10k": here, "humanPer10k": human,
                        "ratioToHuman": round(here / human, 1) if human else None,
                        "description": desc, "matches": matches[:MAX_LISTED]})

    for p in _COMPILED:
        src = narr if p["scope"] == "narr" else text
        spans = [(m.start(), m.end(), m.group(0)) for m in p["compiled"].finditer(src)]
        add(p["name"], p["code"], p["cap"], p["description"], spans)

    add("maxim", "M5", 2, "Generic present-tense truth ('a man in a hurry leaves the corners').",
        maxim_candidates(text, narr))
    add("planted_insert", "M10", 0, "One-line paragraph about a small creature or object; check it is not mirroring the plot.",
        insert_candidates(text, narr))
    add("echo_compliance", "M12", 1, "Command followed by a one-line narration doing exactly it ('Make it heavy.' / 'Sylvanas made it heavy.').",
        echo_compliance(text))

    return results, polysyndeton_density(narr, words, calib), words


def code_caps(patterns, words: int, calib=None):
    """Combined caps for the guide codes that cap a whole family of detectors."""
    out = {}
    for code, default in CODE_DEFAULT_CAPS.items():
        members = [p for p in patterns if p["code"] == code]
        if not members:
            continue
        count = sum(p["count"] for p in members)
        human = round(sum(p["humanPer10k"] or 0 for p in members), 3) if calib else None
        cap = calibrated_cap(default, human, words)
        out[code] = {"count": count, "cap": cap, "guideCap": default, "humanPer10k": human,
                     "overCap": count > cap, "patterns": [p["name"] for p in members]}
    return out


# ---------------------------------------------------------------------------
# Refrains
# ---------------------------------------------------------------------------

STOPWORDS = set("""
a an the and or but if then so as of in on at to for from by with without into onto out up down over under
off about after before again once here there when where why how all any both each few more most other some
such no nor not only own same than too very can will just don't should now she he it they them her him his
hers its their theirs we us our you your i me my was were is are be been being have has had having do does
did doing would could might must shall may that this these those what which who whom whose while until
one two three back still even ever never always away round through across along like yet also too
said say says went go going came come got get made make took take looked look turned turn
""".split())

TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def tokenise(text: str):
    """Return [(lower_token, start_offset, is_capitalised)]."""
    return [(m.group(0).lower(), m.start(), m.group(0)[0].isupper()) for m in TOKEN_RE.finditer(text)]


class Doc:
    """A text with its tokens, built once and shared by every refrain check."""

    __slots__ = ("text", "tokens", "words", "_lines")

    def __init__(self, text: str):
        self.text = text
        self.tokens = tokenise(text)
        self.words = [t for t, _, _ in self.tokens]
        self._lines = None

    def line(self, pos: int) -> int:
        if self._lines is None:
            self._lines = LineIndex(self.text)
        return self._lines.line(pos)


def _as_doc(d) -> Doc:
    return d if isinstance(d, Doc) else Doc(d)


def proper_nouns(tokens):
    """Tokens capitalised away from a sentence start — names and titles."""
    caps = defaultdict(int)
    lows = defaultdict(int)
    for tok, _, cap in tokens:
        (caps if cap else lows)[tok] += 1
    return {t for t in caps if caps[t] >= 2 and lows.get(t, 0) == 0}


def _grams(words, n=NGRAM):
    """Every n-word run of a word list, in order."""
    return zip(*(words[i:] for i in range(n)))


def ngrams(tokens, n=NGRAM):
    """Yield (index, gram) for every n-token run. tokens: tokenise() output."""
    return enumerate(_grams([t for t, _, _ in tokens], n))


FIGURATIVE = {"like", "though", "way", "enough", "than", "if"}


def has_content(gram, names) -> bool:
    return any(t not in STOPWORDS and t not in names for t in gram)


def story_vocabulary(docs, names):
    """Content words that recur across most chapters — the book's ordinary nouns (staff, mare, road).
    docs: texts or Doc objects."""
    if not docs:
        return set()
    seen_in = defaultdict(int)
    for doc in docs:
        for tok in set(_as_doc(doc).words):
            seen_in[tok] += 1
    need = max(2, (len(docs) + 1) // 2)
    return {t for t, n in seen_in.items() if n >= need and t not in STOPWORDS and t not in names}


def run_is_signature(run_tokens, names, common, min_rare=2) -> bool:
    """A shared run is worth reporting if it is long, figurative, or carries rare wording."""
    if len(run_tokens) >= 8:
        return True
    rare = {t for t in run_tokens if t not in STOPWORDS and t not in names and t not in common}
    if len(rare) >= min_rare:
        return True
    return bool(rare) and bool(FIGURATIVE & set(run_tokens))


# ---------------------------------------------------------------------------
# Human n-grams: ordinary English, never a refrain
# ---------------------------------------------------------------------------

def gram_key(gram) -> int:
    """Stable 64-bit key for an n-gram. Python's hash() changes between runs, so it can't be cached."""
    return int.from_bytes(hashlib.blake2b(" ".join(gram).encode("utf-8"), digest_size=8).digest(), "little")


class GramSet:
    """A set of n-grams stored as 64-bit keys: about 8 bytes per gram, cheap to save and load.
    A false match needs a 64-bit collision, which at a million grams is about 1 in 10^13."""

    _MAGIC = b"MCGRAMS1"

    def __init__(self, keys=()):
        self._keys = set(keys)

    @classmethod
    def from_texts(cls, texts, n=NGRAM):
        keys = set()
        for t in texts:
            keys.update(gram_key(g) for g in _grams(_as_doc(t).words, n))
        return cls(keys)

    def __contains__(self, gram) -> bool:
        return gram_key(gram) in self._keys

    def __len__(self) -> int:
        return len(self._keys)

    def to_bytes(self) -> bytes:
        body = array("Q", sorted(self._keys))
        return self._MAGIC + len(body).to_bytes(8, "little") + body.tobytes()

    @classmethod
    def from_bytes(cls, data: bytes):
        """Raises ValueError on a truncated or foreign file."""
        if data[:8] != cls._MAGIC or len(data) < 16:
            raise ValueError("not a gram cache")
        count = int.from_bytes(data[8:16], "little")
        body = array("Q")
        body.frombytes(data[16:])
        if len(body) != count:
            raise ValueError("truncated gram cache")
        return cls(body)


def load_human_grams(texts):
    """Every 5-word run in the reference corpora: ordinary English, never a refrain."""
    return GramSet.from_texts(texts)


def _gram_cache_path():
    from tools.mannered_checker import calibrate as cal

    key = json.dumps({"corpora": cal.fingerprint(), "checker": cal.checker_hash(), "n": NGRAM}, sort_keys=True)
    return os.path.join(CACHE_DIR, f"human-grams-{hashlib.sha1(key.encode()).hexdigest()[:16]}.bin")


def human_grams(use_cache=True):
    """(corpus paths, GramSet) for the configured human corpora.

    The grams are cached under CACHE_DIR, keyed by the corpus fingerprint (paths,
    weights, sizes, mtimes) and the checker hash, so a changed sample or detector
    rebuilds the cache. A missing, corrupt or unwritable cache only costs a rebuild.
    """
    from tools.mannered_checker import calibrate as cal

    paths = cal.corpus_paths()
    path = _gram_cache_path() if use_cache else None
    if path:
        try:
            with open(path, "rb") as f:
                return paths, GramSet.from_bytes(f.read())
        except (OSError, ValueError):
            pass
    grams = GramSet.from_texts(cal.read_corpus(p) for p in paths)
    if path:
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = f"{path}.{os.getpid()}.tmp"
            with open(tmp, "wb") as f:
                f.write(grams.to_bytes())
            os.replace(tmp, path)
            for name in os.listdir(CACHE_DIR):
                old = os.path.join(CACHE_DIR, name)
                if name.startswith("human-grams-") and old != path and not name.endswith(".tmp"):
                    os.remove(old)
        except OSError:
            pass
    return paths, grams


# ---------------------------------------------------------------------------
# Runs
# ---------------------------------------------------------------------------

def merge_runs(hits):
    """Merge consecutive n-gram hits (by token index) into runs."""
    runs = []
    for idx, payload in sorted(hits, key=lambda h: h[0]):
        if runs and idx <= runs[-1]["end"] + 1:
            runs[-1]["end"] = idx
            runs[-1]["payloads"].append(payload)
        else:
            runs.append({"start": idx, "end": idx, "payloads": [payload]})
    return runs


def span_text(text, tokens, start, end):
    a = tokens[start][1]
    last = tokens[min(end + NGRAM - 1, len(tokens) - 1)]
    return text[a:last[1] + len(last[0])]


def chapter_number(path: str):
    m = re.search(r"chapter[-_]?(\d+)", path)
    return int(m.group(1)) if m else None


def prior_chapter_files(target: str):
    """final.md of every chapter numbered before the target, oldest first."""
    chapters_dir = os.path.dirname(os.path.dirname(os.path.abspath(target)))
    target_n = chapter_number(os.path.dirname(os.path.abspath(target)))
    found = []
    if target_n is None or not os.path.isdir(chapters_dir):
        return found
    for name in os.listdir(chapters_dir):
        n = chapter_number(name)
        final = os.path.join(chapters_dir, name, "final.md")
        if n is not None and n < target_n and os.path.exists(final):
            found.append((n, final))
    return sorted(found)


def voice_sheet_files():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            vs = json.load(f).get("characters", {}).get("voiceSheets")
    except (OSError, ValueError):
        return []
    if not vs:
        return []
    vs = os.path.join(REPO_ROOT, vs)
    if os.path.isdir(vs):
        return sorted(os.path.join(vs, f) for f in os.listdir(vs) if f.endswith(".md"))
    return [vs] if os.path.exists(vs) else []


def run_tokens(tokens, run):
    return [t for t, _, _ in tokens[run["start"]:min(run["end"] + NGRAM, len(tokens))]]


def shared_runs(text, tokens, names, common, human, sources, min_rare=2):
    """Runs of the target that also occur in any source. sources: [(label, text or Doc)].

    Only each source gram's first position is indexed; its line number and context
    are worked out for the runs that get reported, not for every gram.
    """
    docs = [(label, _as_doc(src)) for label, src in sources]
    index = {}
    for si, (_, doc) in enumerate(docs):
        for ti, g in enumerate(_grams(doc.words)):
            if g not in index:
                index[g] = (si, ti)
    hits = [(i, index[g]) for i, g in enumerate(_grams([t for t, _, _ in tokens]))
            if g in index and g not in human and has_content(g, names)]
    lines = LineIndex(text)
    out = []
    for run in merge_runs(hits):
        if not run_is_signature(run_tokens(tokens, run), names, common, min_rare):
            continue
        si, ti = run["payloads"][0]
        label, doc = docs[si]
        pos = doc.tokens[ti][1]
        out.append({"line": lines.line(tokens[run["start"]][1]),
                    "text": span_text(text, tokens, run["start"], run["end"])[:200],
                    "source": label, "sourceLine": doc.line(pos), "sourceContext": context(doc.text, pos, pos + 60, 30)})
    return out


def repeated_runs(text, tokens, names, common, human):
    positions = defaultdict(list)
    for i, g in enumerate(_grams([t for t, _, _ in tokens])):
        if g not in human and has_content(g, names):
            positions[g].append(i)
    hits = [(i, g) for g, idxs in positions.items() if len(idxs) >= 2 for i in idxs]
    lines = LineIndex(text)
    out = []
    seen = set()
    for run in merge_runs(hits):
        if not run_is_signature(run_tokens(tokens, run), names, common):
            continue
        phrase = span_text(text, tokens, run["start"], run["end"])
        run_lines = sorted({lines.line(tokens[i][1]) for i in positions[run["payloads"][0]]})
        key = (re.sub(r"\W+", " ", phrase.lower()).strip(), tuple(run_lines))
        if key in seen:
            continue
        seen.add(key)
        out.append({"line": lines.line(tokens[run["start"]][1]), "text": phrase[:200], "lines": run_lines})
    return out


def load_families(path=None):
    try:
        with open(path or FAMILIES_PATH, encoding="utf-8") as f:
            return json.load(f)["families"]
    except (OSError, ValueError, KeyError):
        return []


def family_budgets(text, target, priors, prior_texts=None, families=None):
    """priors: [(n, path)]. prior_texts: {n: text} if already read. families: list, default the JSON file."""
    families = load_families() if families is None else families
    if not families:
        return []
    target_n = chapter_number(os.path.dirname(os.path.abspath(target))) or 0
    if prior_texts is None:
        prior_texts = {n: normalise_quotes(read_text(p)) for n, p in priors}
    lines = LineIndex(text)
    out = []
    for fam in families:
        rx = re.compile(fam["regex"], re.IGNORECASE)
        here = [{"line": lines.line(m.start()), "text": context(text, m.start(), m.end(), 50)}
                for m in rx.finditer(text)]
        window = fam.get("window", 1)
        per_window = fam.get("perWindow", fam.get("perChapter", 1))
        book = {n: len(rx.findall(t)) for n, t in prior_texts.items()}
        in_window = {n: c for n, c in book.items() if target_n - n < window}
        window_total = sum(in_window.values()) + len(here)
        over = len(here) > fam.get("perChapter", 1) or (len(here) > 0 and window_total > per_window)
        out.append({"family": fam["name"], "code": "R", "description": fam["description"],
                    "perChapter": fam.get("perChapter", 1), "window": window, "perWindow": per_window,
                    "countHere": len(here), "windowTotal": window_total,
                    "bookCounts": {**{f"chapter{n}": c for n, c in sorted(book.items()) if c}, "target": len(here)},
                    "overBudget": over, "matches": here[:MAX_LISTED]})
    return out


def run_refrains(text, target, corpora=None, human=None, human_paths=None):
    """Refrain blocks for the target text.

    corpora: [(path, text)] of human reference prose, or pass `human` (a GramSet,
    e.g. from human_grams()) and `human_paths` instead.
    """
    if human is None:
        corpora = corpora or []
        human = GramSet.from_texts(t for _, t in corpora)
        human_paths = [p for p, _ in corpora]
    doc = Doc(text)
    tokens = doc.tokens
    names = proper_nouns(tokens)
    priors = prior_chapter_files(target)
    prior_texts = {n: normalise_quotes(read_text(p)) for n, p in priors}
    prior_sources = [(f"chapter{n}/final.md", Doc(prior_texts[n])) for n, _ in priors]
    sheet_sources = [(os.path.relpath(p, REPO_ROOT), Doc(normalise_quotes(read_text(p)))) for p in voice_sheet_files()]
    common = story_vocabulary([d for _, d in prior_sources] + [doc], names)
    cross = shared_runs(text, tokens, names, common, human, prior_sources)
    # Voice-sheet lines are short and deliberate: any two content words shared with a sheet count,
    # even if they are ordinary words in this book.
    sheets = shared_runs(text, tokens, names, set(), human, sheet_sources, min_rare=2)
    within = repeated_runs(text, tokens, names, common, human)
    fams = family_budgets(text, target, priors, prior_texts)
    return {
        "priorChapters": [label for label, _ in prior_sources],
        "humanCorpora": list(human_paths or []),
        "crossChapter": cross[:MAX_LISTED], "crossChapterCount": len(cross),
        "voiceSheet": sheets[:MAX_LISTED], "voiceSheetCount": len(sheets),
        "withinChapter": within[:MAX_LISTED], "withinChapterCount": len(within),
        "families": fams,
        "familiesOverBudget": [f["family"] for f in fams if f["overBudget"]],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_calibration(recalibrate=True):
    """calibration.json, regenerated first if the configured corpora have changed since it was written."""
    from tools.mannered_checker import calibrate as cal

    data = None
    if os.path.exists(CALIBRATION_PATH):
        try:
            with open(CALIBRATION_PATH, encoding="utf-8") as f:
                data = json.load(f)
        except ValueError:
            data = None
    stale = data is None or data.get("fingerprint") != cal.fingerprint() \
        or data.get("checkerHash") != cal.checker_hash() \
        or data.get("headroom") != HEADROOM or data.get("zeroRelease") != ZERO_RELEASE
    if stale and recalibrate:
        data = cal.calibrate(update_style_guide=True, quiet=True)
        data["_recalibratedNow"] = True
    elif data and recalibrate and cal.style_guide_drifted(data["blend"]):
        # style-guide.json was rewritten (e.g. by the style-extractor) since the last calibration.
        cal.sync_style_guide(data["blend"], [c["path"] for c in data["corpora"]], data["corpora"],
                             [c.get("weight", 1.0) for c in data["corpora"]])
        data["_recalibratedNow"] = True
    return data, stale


def check(target: str, recalibrate=True, use_cache=True):
    calibration, stale = load_calibration(recalibrate)
    calib = calibration["blend"] if calibration else None
    human_paths, human = human_grams(use_cache)
    text = normalise_quotes(strip_headers(read_text(target)))
    patterns, poly, words = run_patterns(text, calib)
    codes = code_caps(patterns, words, calib)
    refrains = run_refrains(text, target, human=human, human_paths=human_paths)
    over = [p["name"] for p in patterns if p["overCap"]]
    return {
        "target": os.path.relpath(os.path.abspath(target), REPO_ROOT),
        "words": words,
        "calibration": {
            "corpora": [c["path"] for c in calibration["corpora"]] if calibration else [],
            "generatedAt": calibration.get("generatedAt") if calibration else None,
            "recalibratedNow": bool(calibration and calibration.get("_recalibratedNow")),
            "stale": stale and not (calibration and calibration.get("_recalibratedNow")),
            "headroom": HEADROOM,
        },
        "patterns": patterns,
        "patternsOverCap": over,
        "codeCaps": codes,
        "codesOverCap": [c for c, v in codes.items() if v["overCap"]],
        "polysyndeton": poly,
        "refrains": refrains,
        "summary": {
            "patternHits": sum(p["count"] for p in patterns),
            "patternsOverCap": len(over),
            "codesOverCap": [c for c, v in codes.items() if v["overCap"]],
            "crossChapterRuns": refrains["crossChapterCount"],
            "voiceSheetRuns": refrains["voiceSheetCount"],
            "withinChapterRuns": refrains["withinChapterCount"],
            "familiesOverBudget": len(refrains["familiesOverBudget"]),
            "polysyndetonPer10k": poly["per10k"],
        },
    }


def summary_text(report) -> str:
    s = report["summary"]
    out = [f"{report['target']}  ({report['words']} words)",
           f"  pattern hits {s['patternHits']}, over cap {s['patternsOverCap']}: {', '.join(report['patternsOverCap']) or '-'}"]
    cal = report["calibration"]
    note = " (recalibrated now)" if cal["recalibratedNow"] else (" (STALE)" if cal["stale"] else "")
    out.append(f"  calibrated against {', '.join(cal['corpora']) or 'nothing'}{note}")
    for code, c in report["codeCaps"].items():
        if c["count"]:
            flag = " OVER" if c["overCap"] else ""
            out.append(f"    {code:4s} {'(combined)':26s} {c['count']:3d} (cap {c['cap']}){flag}")
    for p in report["patterns"]:
        if p["count"]:
            flag = " OVER" if p["overCap"] else ""
            out.append(f"    {p['code']:4s} {p['name']:26s} {p['count']:3d} (cap {p['cap']}){flag}")
    poly = report["polysyndeton"]
    out.append(f"  polysyndeton {poly['per10k']}/10k (human {poly['humanPer10k']}, soft cap {poly['softCapPer10k']})")
    r = report["refrains"]
    out.append(f"  refrains: cross-chapter {r['crossChapterCount']}, voice-sheet {r['voiceSheetCount']}, within-chapter {r['withinChapterCount']}")
    for f in r["families"]:
        if f["countHere"] or f["overBudget"]:
            flag = " OVER" if f["overBudget"] else ""
            out.append(f"    R    {f['family']:26s} here {f['countHere']}, last {f['window']} ch {f['windowTotal']} (budget {f['perWindow']}){flag}")
    return "\n".join(out)


def print_summary(report):
    print(summary_text(report))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="chapter prose file, e.g. .afternoon/chapters/chapter5/v2.md")
    ap.add_argument("--no-recalibrate", action="store_true", help="use calibration.json as is even if the corpora changed")
    ap.add_argument("--no-cache", action="store_true", help="rebuild the human n-gram set instead of using tools/mannered_checker/cache/")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="full JSON report")
    mode.add_argument("--summary", action="store_true", help="short text summary (default)")
    args = ap.parse_args()
    if not os.path.exists(args.target):
        sys.exit(f"no such file: {args.target}")
    report = check(args.target, recalibrate=not args.no_recalibrate, use_cache=not args.no_cache)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_summary(report)


if __name__ == "__main__":
    main()
