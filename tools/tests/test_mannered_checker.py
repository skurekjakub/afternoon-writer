"""tools/mannered_checker/check.py: detectors, caps, refrains, gram cache and the report contract.

All fixture prose is original. Anything that reads config, corpora, calibration,
cache, families or the style guide runs inside support.TempRepo.
"""

import copy
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tools.tests import support
from tools.tests.support import TempRepo, cal, mc, write


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

P = {p["name"]: p for p in mc._COMPILED}


def hits(name, text):
    """Matches of one compiled pattern on the text, honouring its scope like run_patterns does."""
    p = P[name]
    src = mc.narration_only(text) if p["scope"] == "narr" else text
    return [m.group(0) for m in p["compiled"].finditer(src)]


# One positive and one negative original sentence per detector.
PATTERN_CASES = {
    "bent_idiom_seed": ("He gave the pony its head and let it choose its own feet down the scree.",
                        "He let the pony pick its footing on the scree."),
    "equative_montage": ("The week at the mill had been smoke and a broken wheel and the miller shouting at the sky.",
                         "The week at the mill had been a long one, and nobody slept."),
    "equative_single": ("Then the morning was the long quay.",
                        "Then the morning came up grey over the quay."),
    "list_turn_seed": ("She had a bed, a chair, and nobody knocking.",
                       "She had a bed, a chair and a table."),
    "did_not_know_what_to_do": ("He didn't know what to do with his hands.",
                                "He knew what to do with the rope."),
    "having_nominal": ("He felt foolish about having shouted.",
                       "He felt foolish after he shouted."),
    "comic_recursion_seed": ("The mule tried to bolt and kick at once and managed neither.",
                             "The mule bolted down the lane."),
    "self_hearing": ("She heard herself laugh.",
                     "She heard the gate bang."),
    "involuntary_action": ("Her hand closed on the rail before she meant to.",
                           "Her hand closed on the rail."),
    "blush": ("His ears went red.",
              "His ears were cold."),
    "gloss_which": ("He set the cup down on the far side of the table, which meant he was done.",
                    "He set the cup down, which was chipped."),
    "would_have_to_do_for": ("He nodded once. It would have to do for thanks.",
                             "He nodded once and left."),
    "tautology": ("In the end a boat was a boat.",
                  "In the end a boat was a shelter."),
    "anadiplosis": ("The road was clean, and clean was no use to her.",
                    "The road was clean, and the gate was open."),
    "then_fragment": ("The latch was broken. Bad luck, then.",
                      "The latch was broken, then mended."),
    "second_guess_tag": ("The room went colder, or she thought it did.",
                         "The room went colder, and she shivered."),
    "self_address": ("He missed the step. Lovely work, Jaina.",
                     "He missed the step, and Jaina caught him."),
    "the_way_simile": ("She folded the map, the way a clerk folds a ledger.",
                       "She folded the map and went on the way north."),
}


class PatternTableTest(unittest.TestCase):
    def test_every_pattern_compiles_and_is_well_formed(self):
        names = [p["name"] for p in mc.PATTERNS]
        self.assertEqual(len(names), len(set(names)), "duplicate pattern names")
        for p in mc.PATTERNS:
            re.compile(p["regex"], re.MULTILINE)
            self.assertIn(p["scope"], ("all", "narr"), p["name"])
            self.assertRegex(p["code"], r"^M\d{1,2}$", p["name"])
            self.assertIsInstance(p["cap"], int)
            self.assertTrue(p["description"])

    def test_every_pattern_has_cases(self):
        self.assertEqual(set(PATTERN_CASES), set(P))

    def test_positive_and_negative_sentences(self):
        for name, (pos, neg) in PATTERN_CASES.items():
            with self.subTest(pattern=name):
                self.assertTrue(hits(name, pos), f"{name} missed: {pos}")
                self.assertFalse(hits(name, neg), f"{name} fired on: {neg}")

    def test_narr_patterns_ignore_quoted_speech(self):
        narr_patterns = [n for n, p in P.items() if p["scope"] == "narr"]
        self.assertTrue(narr_patterns)
        for name in narr_patterns:
            pos, _ = PATTERN_CASES[name]
            quoted = f'"{pos}" he said.'
            with self.subTest(pattern=name):
                self.assertTrue(hits(name, pos))
                self.assertFalse(hits(name, quoted), f"{name} fired inside quoted speech")

    def test_all_scope_patterns_see_quoted_speech(self):
        quoted = '"I didn\'t know what to do about the goat," she said.'
        self.assertTrue(hits("did_not_know_what_to_do", quoted))

    def test_the_way_simile_branches(self):
        # Comma branch, with and without an intensifier.
        self.assertTrue(hits("the_way_simile", "She looked at him, just the way she had looked at the dog."))
        # Comma-less branch: generic person or animal after "the way".
        self.assertTrue(hits("the_way_simile", "She stood the way men stand at a grave."))
        self.assertTrue(hits("the_way_simile", "He watched the road the way a hawk watches a hedge."))
        # Directional "the way" after a comma is not a simile.
        self.assertFalse(hits("the_way_simile", "She went, the way through the wood being shorter."))
        self.assertFalse(hits("the_way_simile", "He took the lamp, the way back being dark."))
        # The idioms the lookbehinds exclude, mid-sentence.
        for s in ("they rode on the way a dog came", "he walked all the way a mile",
                  "you can tell by the way a horse stands"):
            with self.subTest(sentence=s):
                self.assertFalse(hits("the_way_simile", s))

    def test_the_way_simile_idiom_exclusions_at_sentence_start(self):
        # Regression: the (?<!on)/(?<!all)/(?<!by) lookbehinds were case-sensitive and the
        # patterns compile without IGNORECASE, so the same idioms at the start of a
        # sentence ("On the way...", "All the way...", "By the way...") are reported.
        for s in ("On the way a dog barked at them.", "All the way a gull followed the boat.",
                  "By the way a horse stands you can tell it is lame."):
            self.assertFalse(hits("the_way_simile", s), s)

    def test_tautology_at_sentence_start(self):
        # Regression: the regex started with lowercase (?:a|an|one) and is case-sensitive, so the
        # guide's own shape at the start of a sentence ("A doe was a doe.") is missed.
        self.assertTrue(hits("tautology", "A boat was a boat."))

    def test_tautology_needs_the_same_word(self):
        self.assertTrue(hits("tautology", "She knew that a rope was just a rope."))
        self.assertFalse(hits("tautology", "She knew that a rope was a ladder."))

    def test_then_fragment_and_self_address_are_sentence_level(self):
        self.assertTrue(hits("then_fragment", "Wrong, then."))
        self.assertTrue(hits("then_fragment", "The cart was gone. Smaller still, then."))
        self.assertFalse(hits("then_fragment", "They ate, then slept."))
        self.assertTrue(hits("self_address", "Brilliant, Jaina."))
        self.assertTrue(hits("self_address", "The ink ran. Well done, mage."))
        self.assertFalse(hits("self_address", "Well done, Marten."))


class MaximTest(unittest.TestCase):
    def maxims(self, text):
        return [s for _, _, s in mc.maxim_candidates(text, mc.narration_only(text))]

    def test_narration_maxims(self):
        for s in ("A man in a hurry leaves the gate open.",
                  "Nobody trusts a dry well.",
                  "On clay a loaded cart cuts deep.",
                  "It was late, because nobody leaves the mill before dark.",
                  "A ferryman is never early."):
            with self.subTest(sentence=s):
                self.assertTrue(self.maxims(s), s)

    def test_narration_negatives(self):
        for s in ("The glass stands on the sill.",       # noun ending in s, not a generic truth
                  "She kept the bread for later.",
                  "The ferryman was early that morning.",
                  "A ferryman came up the steps.",          # past tense, a particular man
                  "Go."):                                    # under three words
            with self.subTest(sentence=s):
                self.assertFalse(self.maxims(s), s)

    def test_dialogue_maxim_with_full_stop(self):
        text = '"A dry well never fills twice." He said it to the floor.'
        found = mc.maxim_candidates(text, mc.narration_only(text))
        self.assertEqual([s for _, _, s in found], ["A dry well never fills twice."])
        start, end, s = found[0]
        self.assertEqual(text[start:end], s)

    def test_dialogue_maxim_before_a_tag(self):
        # Regression: dialogue sentences were only taken when they ended in . ! or ?, so a maxim
        # followed by a dialogue tag ('..., twice," he said.') is never a candidate.
        text = '"A dry well never fills twice," he said.'
        self.assertTrue(mc.maxim_candidates(text, mc.narration_only(text)))

    def test_quoted_maxim_not_reported_as_narration(self):
        text = '"Nobody trusts a dry well." She filled the bucket anyway.'
        found = mc.maxim_candidates(text, mc.narration_only(text))
        self.assertEqual(len(found), 1, found)  # only the dialogue sweep finds it

    def test_long_sentences_skipped(self):
        long = "Nobody leaves " + " ".join(["the long road"] * 12) + "."
        self.assertFalse(self.maxims(long))


class EchoInsertPolysyndetonTest(unittest.TestCase):
    def test_echo_compliance_with_irregular_past(self):
        text = '"Make it heavy."\n\nHe made it heavy.'
        found = mc.echo_compliance(text)
        self.assertEqual(len(found), 1)
        start, end, label = found[0]
        self.assertEqual(text[start:end], "He made it heavy.")
        self.assertEqual(label, '"Make it heavy." -> He made it heavy.')

    def test_echo_compliance_regular_stem_and_last_quote_sentence(self):
        text = '"We are late. Hold the line."\n\nEveryone held.'
        self.assertEqual(len(mc.echo_compliance(text)), 1)

    def test_echo_compliance_negatives(self):
        for text in ('"Make it heavy."\n\nHe looked at the sky instead.',                       # no shared stem
                     '"Make it heavy."\n\nHe made it heavy, though the rope was rotten through and through.',  # long reply
                     '"Make it heavy."\n\n"Heavy," he said, and made it.',                     # reply is dialogue
                     '"Bring the whole of the barrel up the stairs."\n\nHe brought it.'):     # long command
            with self.subTest(text=text):
                self.assertEqual(mc.echo_compliance(text), [])

    def test_stem(self):
        self.assertEqual(mc._stem("stood"), "stand")
        self.assertEqual(mc._stem("Holding"), "hold")
        self.assertEqual(mc._stem("held"), "hold")
        self.assertEqual(mc._stem("walked"), "walk")
        self.assertEqual(mc._stem("walks"), "walk")
        self.assertEqual(mc._stem("is"), "is")

    def test_insert_candidates(self):
        text = "He sat.\n\nThe moth found the lamp and was gone.\n\nShe slept."
        found = mc.insert_candidates(text, mc.narration_only(text))
        self.assertEqual(len(found), 1)
        start, end, para = found[0]
        self.assertEqual(text[start:end], "The moth found the lamp and was gone.")

    def test_insert_negatives(self):
        for text in ("The moth found the lamp. It burned. It fell. It lay still.",  # several sentences
                     "Marten found the lamp and lit it.",                             # not a small thing
                     '"The moth is back," she said.'):                                 # speech
            with self.subTest(text=text):
                self.assertEqual(mc.insert_candidates(text, mc.narration_only(text)), [])

    def test_polysyndeton_density(self):
        poly = "She ate and drank and sang and slept."
        text = f"{poly} {poly}\n\nHe walked home.\n\n{poly}"
        narr = mc.narration_only(text)
        words = len(text.split())
        res = mc.polysyndeton_density(narr, words)
        self.assertEqual(res["count"], 3)
        self.assertEqual(res["per10k"], round(3 * 10000 / words, 1))
        self.assertEqual(res["densestParagraphs"], [{"line": 1, "count": 2}])
        self.assertIsNone(res["softCapPer10k"])
        self.assertFalse(res["overSoftCap"])

    def test_polysyndeton_soft_cap(self):
        narr = "She ate and drank and sang and slept. " * 2
        words = 10000  # 2 per 10K
        self.assertEqual(mc.polysyndeton_density(narr, words, {"polysyndetonPer10k": 1.0})["softCapPer10k"], 3.0)
        res = mc.polysyndeton_density(narr, words, {"polysyndetonPer10k": 2.5})
        self.assertEqual(res["softCapPer10k"], 2.5 * mc.HEADROOM)
        res = mc.polysyndeton_density(narr, 2000, {"polysyndetonPer10k": 1.0})  # 10 per 10K
        self.assertTrue(res["overSoftCap"])

    def test_polysyndeton_ignores_speech(self):
        text = '"We ate and drank and sang and slept," she said.'
        self.assertEqual(mc.polysyndeton_density(mc.narration_only(text), 10)["count"], 0)


class CapsTest(unittest.TestCase):
    def test_calibrated_cap_table(self):
        H = mc.HEADROOM
        rows = [
            # default, human rate per 10K, words, expected
            (2, None, 10000, 2),            # no calibration: guide default
            (0, None, 10000, 0),
            (2, 0.4, 10000, 0),             # human rate under ZERO_RELEASE: zero even with a default
            (2, mc.ZERO_RELEASE - 1e-9, 50000, 0),
            (0, mc.ZERO_RELEASE, 10000, math.ceil(mc.ZERO_RELEASE * H)),
            (2, 0.713, 12000, math.ceil(0.713 * 12000 / 10000 * H)),
            (1, 3.0, 5000, math.ceil(3.0 * 5000 / 10000 * H)),
            (5, 1.0, 1000, math.ceil(1.0 * 1000 / 10000 * H)),   # lower than the guide default
        ]
        for default, human, words, expected in rows:
            with self.subTest(default=default, human=human, words=words):
                self.assertEqual(mc.calibrated_cap(default, human, words), expected)

    def test_code_caps_sum_member_rates(self):
        patterns = [
            {"name": "self_hearing", "code": "M7", "count": 1, "humanPer10k": 0.3},
            {"name": "blush", "code": "M7", "count": 2, "humanPer10k": 0.3},
            {"name": "involuntary_action", "code": "M7", "count": 0, "humanPer10k": None},
            {"name": "the_way_simile", "code": "M13", "count": 1, "humanPer10k": 0.1},
            {"name": "gloss_which", "code": "M8", "count": 4, "humanPer10k": 0.0},
        ]
        out = mc.code_caps(patterns, 10000, calib={"patternsPer10k": {}})
        self.assertEqual(set(out), {"M7", "M13"})  # only codes with a combined cap and members
        self.assertEqual(out["M7"]["humanPer10k"], 0.6)
        self.assertEqual(out["M7"]["count"], 3)
        self.assertEqual(out["M7"]["cap"], math.ceil(0.6 * mc.HEADROOM))
        self.assertTrue(out["M7"]["overCap"])
        self.assertEqual(out["M7"]["patterns"], ["self_hearing", "blush", "involuntary_action"])
        self.assertEqual(out["M13"]["cap"], 0)
        self.assertEqual(out["M7"]["guideCap"], mc.CODE_DEFAULT_CAPS["M7"])

    def test_code_caps_without_calibration_use_guide(self):
        patterns = [{"name": "blush", "code": "M7", "count": 3, "humanPer10k": None}]
        out = mc.code_caps(patterns, 10000, calib=None)
        self.assertEqual(out["M7"]["cap"], mc.CODE_DEFAULT_CAPS["M7"])
        self.assertIsNone(out["M7"]["humanPer10k"])

    def test_run_patterns_uses_calibration(self):
        text = "His ears went red. " * 3
        uncal, _, words = mc.run_patterns(text, None)
        blush = next(p for p in uncal if p["name"] == "blush")
        self.assertEqual((blush["count"], blush["cap"], blush["humanPer10k"]), (3, 0, None))
        self.assertTrue(blush["overCap"])
        self.assertEqual(blush["matches"][0]["line"], 1)
        calib = {"patternsPer10k": {"blush": 20000.0}, "polysyndetonPer10k": 1.0}
        cal_res, _, _ = mc.run_patterns(text, calib)
        blush = next(p for p in cal_res if p["name"] == "blush")
        self.assertEqual(blush["cap"], math.ceil(20000.0 * words / 10000 * mc.HEADROOM))
        self.assertFalse(blush["overCap"])
        self.assertEqual(blush["ratioToHuman"], round(blush["per10k"] / 20000.0, 1))

    def test_run_patterns_line_numbers(self):
        text = "Plain line.\nAnother plain line.\nHis ears went red.\n"
        res, _, _ = mc.run_patterns(text)
        blush = next(p for p in res if p["name"] == "blush")
        self.assertEqual(blush["matches"][0]["line"], 3)
        self.assertIn("ears went red", blush["matches"][0]["context"])


# ---------------------------------------------------------------------------
# Refrains
# ---------------------------------------------------------------------------

PLANTED = "the lantern swung like a hanged moth over the black ford"
CH1 = f"""Rain came in off the marsh.

Oskar led the mules down to the water and {PLANTED}, and nobody spoke.

They crossed at dusk.
"""
TARGET = f"""Morning came grey over the reeds.

Halfway across, {PLANTED} again, and Oskar counted the mules twice.

They reached the bank before noon.
"""


class TokenTest(unittest.TestCase):
    def test_doc(self):
        doc = mc.Doc("One two.\nThree four's five")
        self.assertEqual(doc.words, ["one", "two", "three", "four's", "five"])
        self.assertEqual(doc.tokens[2], ("three", 9, True))
        self.assertEqual(doc.line(doc.tokens[2][1]), 2)
        self.assertEqual(doc.line(0), 1)

    def test_as_doc_passes_docs_through(self):
        doc = mc.Doc("a b")
        self.assertIs(mc._as_doc(doc), doc)
        self.assertEqual(mc._as_doc("a b").words, ["a", "b"])

    def test_proper_nouns(self):
        toks = mc.tokenise("Oskar went. Then Oskar came back. The marsh was wide; the marsh was cold. Brenna once.")
        names = mc.proper_nouns(toks)
        self.assertIn("oskar", names)
        self.assertNotIn("marsh", names)   # seen lowercase
        self.assertNotIn("brenna", names)  # only once
        self.assertNotIn("the", names)     # also lowercase

    def test_grams(self):
        words = ["a", "b", "c", "d", "e", "f"]
        self.assertEqual(list(mc._grams(words)), [("a", "b", "c", "d", "e"), ("b", "c", "d", "e", "f")])
        self.assertEqual(list(mc._grams(words[:4])), [])
        self.assertEqual(list(mc._grams(words, 2))[0], ("a", "b"))
        toks = mc.tokenise("a b c d e f")
        self.assertEqual(list(mc.ngrams(toks)), list(enumerate(mc._grams(words))))

    def test_has_content(self):
        self.assertFalse(mc.has_content(("the", "and", "of", "she", "was"), set()))
        self.assertFalse(mc.has_content(("oskar", "and", "the", "she", "was"), {"oskar"}))
        self.assertTrue(mc.has_content(("oskar", "and", "the", "mule", "was"), {"oskar"}))

    def test_story_vocabulary(self):
        docs = ["The mule and the ford.", "A mule at the ford.", "The mule slept.", "A heron."]
        vocab = mc.story_vocabulary(docs, names=set())
        self.assertIn("mule", vocab)       # 3 of 4 docs
        self.assertIn("ford", vocab)       # 2 of 4 docs = (4+1)//2
        self.assertNotIn("heron", vocab)
        self.assertNotIn("the", vocab)     # stopword
        self.assertEqual(mc.story_vocabulary([], set()), set())
        self.assertNotIn("mule", mc.story_vocabulary(docs, names={"mule"}))
        # Docs and plain texts give the same answer.
        self.assertEqual(mc.story_vocabulary([mc.Doc(d) for d in docs], set()), vocab)

    def test_run_is_signature(self):
        self.assertTrue(mc.run_is_signature(["the"] * 8, set(), set()))                       # long
        self.assertTrue(mc.run_is_signature(["the", "heron", "and", "the", "eel"], set(), set()))  # two rare
        self.assertFalse(mc.run_is_signature(["the", "heron", "and", "the", "eel"], set(), {"heron"}))
        self.assertTrue(mc.run_is_signature(["like", "a", "heron", "in", "the"], set(), set()))  # figurative + rare
        self.assertFalse(mc.run_is_signature(["and", "the", "heron", "was", "there"], set(), set()))
        self.assertFalse(mc.run_is_signature(["oskar", "and", "the", "heron", "was"], {"oskar"}, {"heron"}))


class SharedRunsTest(unittest.TestCase):
    def test_finds_planted_run_with_source_position(self):
        doc = mc.Doc(TARGET)
        names = mc.proper_nouns(doc.tokens)
        out = mc.shared_runs(TARGET, doc.tokens, names, set(), mc.GramSet(), [("chapter1/final.md", CH1)])
        self.assertEqual(len(out), 1, out)
        run = out[0]
        self.assertEqual(run["source"], "chapter1/final.md")
        self.assertIn(PLANTED, run["text"])
        self.assertEqual(run["line"], 3)  # line in the target
        self.assertEqual(run["sourceLine"], 3)  # line in the SOURCE text
        src_pos = CH1.index("the lantern")
        self.assertEqual(run["sourceContext"], mc.context(CH1, src_pos, src_pos + 60, 30))

    def test_source_line_comes_from_the_source(self):
        source = "\n\n\n\n\n\n" + CH1  # same run six lines further down in the source
        doc = mc.Doc(TARGET)
        out = mc.shared_runs(TARGET, doc.tokens, set(), set(), mc.GramSet(), [("chapter1/final.md", source)])
        self.assertEqual(out[0]["line"], 3)
        self.assertEqual(out[0]["sourceLine"], 9)

    def test_first_source_wins(self):
        doc = mc.Doc(TARGET)
        out = mc.shared_runs(TARGET, doc.tokens, set(), set(), mc.GramSet(),
                             [("chapter1/final.md", CH1), ("chapter2/final.md", mc.Doc(CH1))])
        self.assertEqual(out[0]["source"], "chapter1/final.md")

    def test_human_grams_drop_ordinary_english(self):
        doc = mc.Doc(TARGET)
        human = mc.GramSet.from_texts([f"Once {PLANTED} in a story."])
        self.assertEqual(mc.shared_runs(TARGET, doc.tokens, set(), set(), human, [("ch1", CH1)]), [])

    def test_name_only_runs_dropped(self):
        source = "Then Marta and Oskar at Brennick, Marta said."
        target = "At dawn Marta and Oskar at Brennick met. Oskar and Marta waved toward Brennick and Brennick waved back."
        doc = mc.Doc(target)
        names = mc.proper_nouns(doc.tokens)
        self.assertTrue({"marta", "oskar", "brennick"} <= names)
        self.assertEqual(mc.shared_runs(target, doc.tokens, names, set(), mc.GramSet(), [("src", source)]), [])

    def test_common_story_words_need_min_rare(self):
        source = "She took the lamp to the ford at night."
        target = "Later she took the lamp to the ford again."
        doc = mc.Doc(target)
        found = mc.shared_runs(target, doc.tokens, set(), set(), mc.GramSet(), [("src", source)])
        self.assertTrue(found)
        common = {"lamp", "ford"}
        self.assertEqual(mc.shared_runs(target, doc.tokens, set(), common, mc.GramSet(), [("src", source)]), [])

    def test_repeated_runs_lines(self):
        phrase = "the heron stood in the reeds like a nail"
        text = f"First, {phrase}.\nNothing else.\nLater, {phrase} again.\n"
        doc = mc.Doc(text)
        out = mc.repeated_runs(text, doc.tokens, set(), set(), mc.GramSet())
        self.assertEqual(len(out), 1, out)
        self.assertEqual(out[0]["lines"], [1, 3])
        self.assertEqual(out[0]["line"], 1)
        self.assertIn("heron stood in the reeds", out[0]["text"])

    def test_repeated_runs_respect_human_grams(self):
        phrase = "the heron stood in the reeds like a nail"
        text = f"First, {phrase}.\nLater, {phrase} again.\n"
        doc = mc.Doc(text)
        human = mc.GramSet.from_texts([phrase])
        self.assertEqual(mc.repeated_runs(text, doc.tokens, set(), set(), human), [])


class PriorChaptersAndFamiliesTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="mc-chapters-")
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.chapters = os.path.join(self.root, "chapters")

    def chapter(self, n, name="final.md", text="x"):
        return write(os.path.join(self.chapters, f"chapter{n}", name), text)

    def test_prior_chapter_files_numeric_order(self):
        for n in (1, 2, 9, 11):
            self.chapter(n)
        self.chapter(3, "v2.md")  # no final.md
        target = self.chapter(10, "v2.md")
        self.chapter(10)  # the target's own final.md is not a prior
        found = mc.prior_chapter_files(target)
        self.assertEqual([n for n, _ in found], [1, 2, 9])
        self.assertEqual(found[-1][1], os.path.join(self.chapters, "chapter9", "final.md"))

    def test_prior_chapter_files_outside_chapter_dir(self):
        path = write(os.path.join(self.root, "notes", "draft.md"), "x")
        self.assertEqual(mc.prior_chapter_files(path), [])

    def test_chapter_number(self):
        self.assertEqual(mc.chapter_number("chapter12"), 12)
        self.assertEqual(mc.chapter_number("/a/chapter-3/v2.md"), 3)
        self.assertEqual(mc.chapter_number("chapter_4"), 4)
        self.assertIsNone(mc.chapter_number("prologue"))

    FAMILIES = [
        {"name": "kettle", "description": "kettle beat", "regex": r"\bthe kettle sang\b",
         "perChapter": 1, "window": 3, "perWindow": 2},
        {"name": "narrow", "description": "window 2", "regex": r"\bthe kettle sang\b",
         "perChapter": 1, "window": 2, "perWindow": 1},
        {"name": "absent", "description": "never used", "regex": r"\bzebra\b"},
    ]

    def test_family_budgets(self):
        self.chapter(1, text="The kettle sang. The kettle sang.")
        self.chapter(2, text="Quiet day.")
        self.chapter(3, text="The kettle sang once.")
        target = self.chapter(4, "v2.md", "Morning.\nThe kettle sang.\n")
        priors = mc.prior_chapter_files(target)
        out = {f["family"]: f for f in mc.family_budgets(read(target), target, priors, families=self.FAMILIES)}

        k = out["kettle"]  # window 3 = chapters 2, 3 and the target
        self.assertEqual((k["countHere"], k["windowTotal"]), (1, 2))
        self.assertFalse(k["overBudget"])
        self.assertEqual(k["bookCounts"], {"chapter1": 2, "chapter3": 1, "target": 1})
        self.assertEqual(k["matches"][0]["line"], 2)
        self.assertEqual(k["code"], "R")

        n = out["narrow"]  # window 2 = chapter 3 and the target: 2 > perWindow 1
        self.assertEqual(n["windowTotal"], 2)
        self.assertTrue(n["overBudget"])

        a = out["absent"]  # defaults: window 1, perChapter 1, perWindow = perChapter
        self.assertEqual((a["window"], a["perChapter"], a["perWindow"], a["countHere"]), (1, 1, 1, 0))
        self.assertFalse(a["overBudget"])
        self.assertEqual(a["bookCounts"], {"target": 0})

    def test_family_over_per_chapter(self):
        target = self.chapter(1, "v2.md", "The kettle sang. Later the kettle sang.")
        out = mc.family_budgets(read(target), target, [], families=self.FAMILIES[:1])
        self.assertTrue(out[0]["overBudget"])  # 2 > perChapter 1, even with an empty window

    def test_family_window_only_counts_when_used_here(self):
        self.chapter(1, text="The kettle sang. The kettle sang. The kettle sang.")
        target = self.chapter(2, "v2.md", "No kettles today.")
        out = mc.family_budgets(read(target), target, mc.prior_chapter_files(target), families=self.FAMILIES[:1])
        self.assertEqual(out[0]["windowTotal"], 3)
        self.assertFalse(out[0]["overBudget"])

    def test_prior_texts_given_or_read_match(self):
        self.chapter(1, text="The kettle sang’s song. The kettle sang.")
        self.chapter(2, text="The kettle sang.")
        target = self.chapter(3, "v2.md", "The kettle sang.")
        priors = mc.prior_chapter_files(target)
        text = read(target)
        from_disk = mc.family_budgets(text, target, priors, families=self.FAMILIES)
        given = mc.family_budgets(text, target, priors, families=self.FAMILIES,
                                  prior_texts={n: mc.normalise_quotes(read(p)) for n, p in priors})
        self.assertEqual(from_disk, given)

    def test_families_case_insensitive_and_file_fallback(self):
        target = self.chapter(1, "v2.md", "THE KETTLE SANG.")
        out = mc.family_budgets(read(target), target, [], families=self.FAMILIES[:1])
        self.assertEqual(out[0]["countHere"], 1)
        with mock.patch.object(mc, "FAMILIES_PATH", os.path.join(self.root, "missing.json")):
            self.assertEqual(mc.load_families(), [])
            self.assertEqual(mc.family_budgets("x", target, []), [])
        bad = write(os.path.join(self.root, "bad.json"), "{not json")
        self.assertEqual(mc.load_families(bad), [])


# ---------------------------------------------------------------------------
# Gram sets and the cache
# ---------------------------------------------------------------------------

class GramSetTest(unittest.TestCase):
    GRAM = ("the", "lantern", "swung", "over", "the")
    KEY = 8980897196341364321  # blake2b-64 of "the lantern swung over the", little-endian

    def test_gram_key_is_stable(self):
        self.assertEqual(mc.gram_key(self.GRAM), self.KEY)

    def test_gram_key_same_in_another_process(self):
        code = ("import sys; sys.path.insert(0, sys.argv[1]); from tools.mannered_checker import check as mc; "
                "print(mc.gram_key(('the','lantern','swung','over','the')))")
        out = subprocess.run([sys.executable, "-c", code, support.REPO_ROOT], capture_output=True, text=True,
                             env={**os.environ, "PYTHONHASHSEED": "12345"}, timeout=60)
        self.assertEqual(out.stdout.strip(), str(self.KEY), out.stderr)

    def test_membership(self):
        gs = mc.GramSet.from_texts(["The lantern swung over the ford at night."])
        self.assertIn(self.GRAM, gs)
        self.assertNotIn(("lantern", "swung", "over", "the", "river"), gs)
        self.assertEqual(len(gs), 4)  # 9 tokens -> 5 grams; 'the' twice doesn't matter
        self.assertEqual(len(mc.GramSet.from_texts(["too short"])), 0)
        self.assertEqual(len(mc.GramSet()), 0)

    def test_from_texts_accepts_docs(self):
        text = "The lantern swung over the ford at night."
        self.assertEqual(mc.GramSet.from_texts([mc.Doc(text)])._keys, mc.GramSet.from_texts([text])._keys)

    def test_round_trip(self):
        gs = mc.GramSet.from_texts([support.HUMAN_PROSE])
        back = mc.GramSet.from_bytes(gs.to_bytes())
        self.assertEqual(back._keys, gs._keys)
        self.assertEqual(mc.GramSet.from_bytes(mc.GramSet().to_bytes())._keys, set())

    def test_from_bytes_rejects_bad_data(self):
        good = mc.GramSet.from_texts([support.HUMAN_PROSE]).to_bytes()
        for bad in (b"", b"nope", b"XXXXXXXX" + good[8:], good[:-3], good[:-8], good[:12], good + b"\0" * 8):
            with self.subTest(length=len(bad)):
                with self.assertRaises(ValueError):
                    mc.GramSet.from_bytes(bad)

    def test_load_human_grams(self):
        self.assertIn(self.GRAM, mc.load_human_grams(["Then the lantern swung over the gate."]))


class HumanGramCacheTest(unittest.TestCase):
    def cache_files(self, repo):
        d = repo.path("cache")
        return sorted(os.listdir(d)) if os.path.isdir(d) else []

    def test_written_then_loaded(self):
        with TempRepo() as repo:
            paths, grams = mc.human_grams()
            self.assertEqual(paths, ["samples/human.md"])
            files = self.cache_files(repo)
            self.assertEqual(len(files), 1)
            self.assertRegex(files[0], r"^human-grams-[0-9a-f]{16}\.bin$")
            with mock.patch.object(mc.GramSet, "from_texts", side_effect=AssertionError("rebuilt")):
                paths2, grams2 = mc.human_grams()
            self.assertEqual(grams2._keys, grams._keys)
            self.assertEqual(paths2, paths)
            self.assertIn(("the", "rain", "had", "stopped", "by"), grams2)

    def test_corpus_edit_rebuilds_and_prunes(self):
        with TempRepo() as repo:
            mc.human_grams()
            first = self.cache_files(repo)
            path = repo.path("samples", "human.md")
            write(path, support.HUMAN_PROSE + "\nA heron rose from the ditch and flew west.\n")
            st = os.stat(path)
            os.utime(path, (st.st_atime, st.st_mtime + 10))
            _, grams = mc.human_grams()
            second = self.cache_files(repo)
            self.assertEqual(len(second), 1)
            self.assertNotEqual(first, second)
            self.assertIn(("a", "heron", "rose", "from", "the"), grams)

    def test_weight_change_rebuilds(self):
        with TempRepo(corpora={"samples/human.md": {"text": support.HUMAN_PROSE, "weight": 1}}) as repo:
            mc.human_grams()
            first = self.cache_files(repo)
            repo.corpora["samples/human.md"]["weight"] = 2
            repo.write_config()
            mc.human_grams()
            self.assertNotEqual(self.cache_files(repo), first)
            self.assertEqual(len(self.cache_files(repo)), 1)

    def test_corrupt_cache_rebuilt(self):
        with TempRepo() as repo:
            _, grams = mc.human_grams()
            cache = repo.path("cache", self.cache_files(repo)[0])
            write(cache, "garbage")
            real = mc.GramSet.from_texts
            with mock.patch.object(mc.GramSet, "from_texts", side_effect=real) as rebuilt:
                _, again = mc.human_grams()
            self.assertEqual(rebuilt.call_count, 1)
            self.assertEqual(again._keys, grams._keys)
            with open(cache, "rb") as f:
                self.assertEqual(mc.GramSet.from_bytes(f.read())._keys, grams._keys)

    def test_unwritable_cache_dir(self):
        with TempRepo() as repo:
            blocker = write(repo.path("not-a-dir"), "file")
            with mock.patch.object(mc, "CACHE_DIR", os.path.join(blocker, "cache")):
                paths, grams = mc.human_grams()
            self.assertEqual(paths, ["samples/human.md"])
            self.assertGreater(len(grams), 0)

    def test_no_cache_never_writes(self):
        with TempRepo() as repo:
            _, grams = mc.human_grams(use_cache=False)
            self.assertGreater(len(grams), 0)
            self.assertFalse(os.path.exists(repo.path("cache")))

    def test_leftover_tmp_files_kept_and_other_keys_removed(self):
        with TempRepo() as repo:
            write(repo.path("cache", "human-grams-0000000000000000.bin"), "old")
            write(repo.path("cache", "human-grams-x.bin.123.tmp"), "in flight")
            write(repo.path("cache", "unrelated.txt"), "keep")
            mc.human_grams()
            files = self.cache_files(repo)
            self.assertNotIn("human-grams-0000000000000000.bin", files)
            self.assertIn("human-grams-x.bin.123.tmp", files)
            self.assertIn("unrelated.txt", files)


# ---------------------------------------------------------------------------
# check() end to end
# ---------------------------------------------------------------------------

STYLE_GUIDE = {
    "rhythmMetrics": {
        "purpose": "test",
        "source": "test",
        "global": {
            "comma_period_ratio": {"measured": 0.7, "target": 0.75, "range": [0.6, 0.9]},
            "sentence_length_mean": {"measured": 11.0, "target": 12.0, "range": [10.0, 14.0]},
            "sentence_length_cv": {"measured": 0.6, "target": 0.65, "range": [0.55, 0.75]},
            "short_sentence_pct": {"measured": 30.0, "target": 28.0, "range": [21.0, 35.0]},
            "long_sentence_pct": {"measured": 12.0, "target": 13.0, "range": [8.0, 18.0]},
            "opener_entropy": {"measured": 6.5, "target": 6.6, "range": [6.1, 7.1]},
            "one_sentence_paragraph_pct": {"measured": 22.0, "target": 21.0, "range": [17.0, 26.0]},
            "mattr": {"measured": 0.84, "target": 0.85, "range": [0.82, 0.89]},
        },
    },
    "textureMetrics": {
        "purpose": "test",
        "source": "test",
        "participial_pct": {"human": 6.0, "target": 7.0, "range": [7.0, 10.0]},
        "compound_pct": {"human": 12.0, "target": 14.0, "range": [11.0, 17.0]},
        "emdash_pct": {"human": 4.5, "target": 5.0, "range": [3.5, 6.5]},
        "semicolon_pct": {"human": 1.2, "target": 1.6, "range": [0.8, 2.3]},
        "short_pct": {"human": 45.0, "target": 41.0, "range": [33.0, 48.0]},
        "texture_score": {"human": 100.0, "target": 100.0, "range": [90.0, 100.0]},
    },
}

CH2 = """The ferry was late.

Oskar sat on the bollard and the kettle sang on the brazier behind him.

Nobody came for an hour.
"""

TARGET3 = f"""# Chapter 3

The kettle sang. Oskar did not look up.

His ears went red, and he heard himself laugh.

Halfway across, {PLANTED}, and the boatman spat into the black water twice.

The way back was long.
"""

VOICE_SHEET = """# Oskar

Shape example: *the boatman spat into the black water twice for luck.*
"""

REPORT_KEYS = {"target", "words", "calibration", "patterns", "patternsOverCap", "codeCaps", "codesOverCap",
               "polysyndeton", "refrains", "summary"}
CALIBRATION_KEYS = {"corpora", "generatedAt", "recalibratedNow", "stale", "headroom"}
PATTERN_KEYS = {"name", "code", "count", "cap", "guideCap", "overCap", "per10k", "humanPer10k", "ratioToHuman",
                "description", "matches"}
REFRAIN_KEYS = {"priorChapters", "humanCorpora", "crossChapter", "crossChapterCount", "voiceSheet",
                "voiceSheetCount", "withinChapter", "withinChapterCount", "families", "familiesOverBudget"}
SUMMARY_KEYS = {"patternHits", "patternsOverCap", "codesOverCap", "crossChapterRuns", "voiceSheetRuns",
                "withinChapterRuns", "familiesOverBudget", "polysyndetonPer10k"}


def repo_for_check():
    return TempRepo(chapters={1: CH1, 2: CH2}, voice_sheets={"oskar-voice.md": VOICE_SHEET},
                    style_guide=copy.deepcopy(STYLE_GUIDE))


class CheckEndToEndTest(unittest.TestCase):
    def test_report_contract(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            report = mc.check(target)

            self.assertEqual(set(report), REPORT_KEYS)
            self.assertEqual(report["target"], os.path.join(".afternoon", "chapters", "chapter3", "v2.md"))
            self.assertEqual(set(report["calibration"]), CALIBRATION_KEYS)
            self.assertEqual(report["calibration"]["corpora"], ["samples/human.md"])
            self.assertEqual(report["calibration"]["headroom"], mc.HEADROOM)
            for p in report["patterns"]:
                self.assertEqual(set(p), PATTERN_KEYS, p["name"])
                for m in p["matches"]:
                    self.assertEqual(set(m), {"line", "text", "context"})
            names = [p["name"] for p in report["patterns"]]
            self.assertEqual(names, [p["name"] for p in mc.PATTERNS] + ["maxim", "planted_insert", "echo_compliance"])
            for c in report["codeCaps"].values():
                self.assertEqual(set(c), {"count", "cap", "guideCap", "humanPer10k", "overCap", "patterns"})
            self.assertEqual(set(report["polysyndeton"]),
                             {"count", "per10k", "humanPer10k", "softCapPer10k", "overSoftCap", "densestParagraphs"})
            self.assertEqual(set(report["refrains"]), REFRAIN_KEYS)
            self.assertEqual(set(report["summary"]), SUMMARY_KEYS)
            json.dumps(report)  # serialisable

            # Detectors see the text with the header blanked, so line numbers match the file.
            by = {p["name"]: p for p in report["patterns"]}
            self.assertEqual(by["blush"]["matches"][0]["line"], 5)
            self.assertEqual(by["self_hearing"]["count"], 1)
            self.assertIn("blush", report["patternsOverCap"])

            r = report["refrains"]
            self.assertEqual(r["priorChapters"], ["chapter1/final.md", "chapter2/final.md"])
            self.assertEqual(r["humanCorpora"], ["samples/human.md"])
            self.assertEqual(r["crossChapterCount"], 1)
            self.assertEqual(r["crossChapter"][0]["source"], "chapter1/final.md")
            self.assertEqual(r["crossChapter"][0]["line"], 7)
            self.assertEqual(r["voiceSheetCount"], 1)
            self.assertEqual(r["voiceSheet"][0]["source"], os.path.join("stories", "test", "voice-sheets", "oskar-voice.md"))
            fam = r["families"][0]
            self.assertEqual(fam["family"], "test_family")
            self.assertEqual(fam["countHere"], 1)
            self.assertEqual(fam["bookCounts"], {"chapter2": 1, "target": 1})
            self.assertTrue(fam["overBudget"])  # window 3 total 2 > perWindow 1
            self.assertEqual(r["familiesOverBudget"], ["test_family"])
            self.assertEqual(report["summary"]["familiesOverBudget"], 1)
            self.assertEqual(report["summary"]["crossChapterRuns"], 1)
            self.assertEqual(report["summary"]["patternHits"], sum(p["count"] for p in report["patterns"]))

    def test_recalibrates_when_stale_then_settles(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            self.assertFalse(os.path.exists(repo.path("calibration.json")))
            first = mc.check(target)
            self.assertTrue(first["calibration"]["recalibratedNow"])
            self.assertFalse(first["calibration"]["stale"])
            self.assertTrue(os.path.exists(repo.path("calibration.json")))
            self.assertIsNotNone(first["calibration"]["generatedAt"])
            guide = json.loads(read(repo.path(".afternoon", "style-guide.json")))
            self.assertIn("perCorpus", guide["textureMetrics"])

            second = mc.check(target)
            self.assertFalse(second["calibration"]["recalibratedNow"])
            self.assertFalse(second["calibration"]["stale"])
            self.assertEqual(second["calibration"]["generatedAt"], first["calibration"]["generatedAt"])

            # Editing a corpus makes the calibration stale again.
            path = repo.path("samples", "human.md")
            write(path, support.HUMAN_PROSE + "\nThe heron was gone by morning.\n")
            st = os.stat(path)
            os.utime(path, (st.st_atime, st.st_mtime + 10))
            third = mc.check(target)
            self.assertTrue(third["calibration"]["recalibratedNow"])

    def test_style_guide_drift_resynced(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            mc.check(target)
            write(repo.path(".afternoon", "style-guide.json"), json.dumps(STYLE_GUIDE))  # e.g. style-extractor rewrite
            report = mc.check(target)
            self.assertTrue(report["calibration"]["recalibratedNow"])
            data = json.loads(read(repo.path("calibration.json")))
            self.assertFalse(cal.style_guide_drifted(data["blend"]))

    def test_no_recalibrate_without_calibration(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            report = mc.check(target, recalibrate=False)
            self.assertFalse(os.path.exists(repo.path("calibration.json")))
            c = report["calibration"]
            self.assertEqual((c["corpora"], c["generatedAt"], c["recalibratedNow"], c["stale"]), ([], None, False, True))
            by = {p["name"]: p for p in report["patterns"]}
            self.assertEqual(by["the_way_simile"]["cap"], P["the_way_simile"]["cap"])  # guide default
            self.assertIsNone(by["the_way_simile"]["humanPer10k"])
            guide = json.loads(read(repo.path(".afternoon", "style-guide.json")))
            self.assertEqual(guide, STYLE_GUIDE)  # untouched

    def test_no_recalibrate_keeps_stale_calibration(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            mc.check(target)
            before = read(repo.path("calibration.json"))
            repo.corpora["samples/human.md"] = {"text": support.HUMAN_PROSE, "weight": 3}
            repo.write_config()
            report = mc.check(target, recalibrate=False)
            self.assertTrue(report["calibration"]["stale"])
            self.assertFalse(report["calibration"]["recalibratedNow"])
            self.assertEqual(report["calibration"]["corpora"], ["samples/human.md"])
            self.assertEqual(read(repo.path("calibration.json")), before)

    def test_corrupt_calibration_is_regenerated(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            write(repo.path("calibration.json"), "{broken")
            report = mc.check(target)
            self.assertTrue(report["calibration"]["recalibratedNow"])
            json.loads(read(repo.path("calibration.json")))

    def test_summary_text(self):
        with repo_for_check() as repo:
            target = repo.chapter(3, "v2.md", TARGET3)
            report = mc.check(target)
            text = mc.summary_text(report)
            self.assertTrue(text.startswith(report["target"]))
            self.assertIn("pattern hits", text)
            self.assertIn("test_family", text)
            self.assertIn("recalibrated now", text)
            with mock.patch("builtins.print") as printed:
                mc.print_summary(report)
            printed.assert_called_once_with(text)

    def test_first_chapter_has_no_priors(self):
        with TempRepo(style_guide=copy.deepcopy(STYLE_GUIDE)) as repo:
            target = repo.chapter(1, "v2.md", "A short first chapter. Nothing repeats here at all.")
            r = mc.check(target)["refrains"]
            self.assertEqual((r["priorChapters"], r["crossChapterCount"]), ([], 0))


class CliTest(unittest.TestCase):
    def test_help(self):
        code, out, _ = support.run_cli(["tools/mannered_checker/check.py", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("--no-recalibrate", out)
        self.assertIn("--no-cache", out)

    def test_missing_file(self):
        code, _, err = support.run_cli(["tools/mannered_checker/check.py", "--no-recalibrate", "no/such/file.md"])
        self.assertNotEqual(code, 0)
        self.assertIn("no such file", err)


if __name__ == "__main__":
    unittest.main()
