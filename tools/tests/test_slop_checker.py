"""tools/slop_checker/check.py: pattern registry, caps, paragraph rules, JSON contract, CLI.

All example prose is original, written for these tests.
"""

import json
import os
import re
import tempfile
import unittest

from tools.tests import support
from tools.slop_checker import check as sc
from tools.slop_checker.patterns import ALL_PATTERNS, COMBINED_CAPS

PATTERN = {p["name"]: p for p in sc._COMPILED}
CHECK_PY = os.path.join("tools", "slop_checker", "check.py")


def hits(name, text):
    return [m.group() for m in PATTERN[name]["compiled"].finditer(text)]


def pattern_result(report, name):
    for cat in report.categories:
        for pr in cat.patterns:
            if pr.name == name:
                return pr
    raise KeyError(name)


def category_result(report, name):
    for cat in report.categories:
        if cat.category == name:
            return cat
    raise KeyError(name)


def paragraphs(*paras):
    return "\n\n".join(paras) + "\n"


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class RegistryTest(unittest.TestCase):
    def test_every_pattern_is_well_formed(self):
        self.assertGreater(len(ALL_PATTERNS), 50)
        for p in ALL_PATTERNS:
            with self.subTest(pattern=p.get("name")):
                for key in ("name", "category", "regex", "cap"):
                    self.assertIn(key, p)
                self.assertIsInstance(p["name"], str)
                self.assertIsInstance(p["category"], str)
                self.assertIsInstance(p["cap"], int)
                self.assertGreaterEqual(p["cap"], 0)
                re.compile(p["regex"], re.IGNORECASE)
                if "cap_per_words" in p:
                    self.assertIsInstance(p["cap_per_words"], int)
                    self.assertGreater(p["cap_per_words"], 0)

    def test_names_are_unique(self):
        names = [p["name"] for p in ALL_PATTERNS]
        self.assertEqual(len(names), len(set(names)))

    def test_combined_caps_name_real_categories(self):
        categories = {p["category"] for p in ALL_PATTERNS}
        for cat, cap in COMBINED_CAPS.items():
            with self.subTest(category=cat):
                self.assertIn(cat, categories)
                self.assertIsInstance(cap, int)
                self.assertGreaterEqual(cap, 0)

    def test_compiled_list_mirrors_registry(self):
        self.assertEqual([p["name"] for p in sc._COMPILED], [p["name"] for p in ALL_PATTERNS])
        for p in sc._COMPILED:
            self.assertTrue(p["compiled"].flags & re.IGNORECASE)


# ---------------------------------------------------------------------------
# Representative patterns: one hit in the positive line, none in the negative
# ---------------------------------------------------------------------------

EXAMPLES = {
    # name: (positive, expected match, negative)
    "filler_nodded": ("Tomas nodded and set the cup down.", "nodded", "The knot in the rope held."),
    "bookism_hissed": ('"Out," she hissed.', "hissed", '"Out," she said.'),
    "bookism_breathed_tag": ('"Look at it," she breathed.', '" she breathed', "She breathed on the cold glass."),
    "adverb_on_tag": ('"Leave it," he said softly.', "said softly", '"Leave it," he said, and went out.'),
    "filter_noticed": ("She noticed the gate was open.", "noticed", "The gate was open."),
    "filter_absorbed": ("He absorbed the news without a word.", "absorbed the", "The cloth absorbed water."),
    "breath_held": ("She held her breath at the door.", "held her breath", "She held the rope at the door."),
    "breath_didnt_know_holding": ("He let out a breath he didn’t know he was holding.",
                                  "breath he didn’t know he was holding", "He let out a long breath."),
    "hedge_something_like": ("There was something like relief in it.", "something like relief",
                             "There was something like a ladder in the barn."),
    "ai_vocab_tapestry": ("The market was a tapestry of noise.", "tapestry of", "She hung the tapestry on the wall."),
    "ai_vocab_testament": ("It was a testament to her patience.", "testament to", "He read from the old testament."),
    "punct_emdash_cluster": ("He came—slowly—with the dog—and the boy.",
                             "He came—slowly—with the dog—", "He came—slowly—with the dog."),
    "punct_colon_narration": ("She knew one thing: the road was gone.", "She knew one thing: t",
                              "She knew one thing. The road was gone."),
    "negation_parallel": ("It was not anger, but grief. Not grief, but something older.",
                          "not anger, but grief. Not grief, but", "It was not late, but the lamps were lit."),
    "permission_tag_let_it_settle": ("He said nothing. Let it settle.", ". Let it settle", "He let the dog out."),
    "verdict_too_x_for": ("The room was too quiet for comfort.", "too quiet for comfort",
                          "The sack was too heavy for her."),
    "inanimate_silence": ("The silence stretched between them.", "The silence stretched", "She kept her silence."),
    "ambient_inversion_came": ("From the yard came the bark of a dog.", "From the yard came the bark",
                               "A dog barked in the yard."),
    "something_vague": ("There was something in her voice.", "something in her voice", "She put the cup in the sink."),
    "simile_like": ("It sat in her chest like a stone.", "like a stone", "She liked the bread."),
    "participial_trailing": ("He stood at the rail, turning the coin over.", ", turning the",
                             "He stood at the rail and turned the coin over."),
    "temporal_after_moment": ("After a moment, he spoke.", "After a moment", "After supper, he spoke."),
    "cliche_raised_eyebrow": ("He raised an eyebrow.", "raised an eyebrow", "He raised the lantern."),
    "melodramatic_devastating": ("The news was devastating.", "devastating", "The news was bad."),
}


class RepresentativePatternTest(unittest.TestCase):
    def test_examples_name_real_patterns(self):
        for name in EXAMPLES:
            self.assertIn(name, PATTERN)

    def test_examples_cover_many_categories(self):
        categories = {PATTERN[name]["category"] for name in EXAMPLES}
        self.assertGreaterEqual(len(categories), 18)

    def test_positive_examples_match(self):
        for name, (positive, expected, _) in EXAMPLES.items():
            with self.subTest(pattern=name):
                self.assertEqual(hits(name, positive), [expected])

    def test_negative_examples_do_not_match(self):
        for name, (_, _, negative) in EXAMPLES.items():
            with self.subTest(pattern=name):
                self.assertEqual(hits(name, negative), [])

    def test_matching_ignores_case(self):
        self.assertEqual(hits("filler_nodded", "He NODDED."), ["NODDED"])

    def test_plain_paragraph_trips_nothing(self):
        text = paragraphs(
            "The cart reached the ford at noon. Marten walked the horse across and the boy carried the lamp.",
            "On the far bank the road climbed between two walls. They stopped at the first gate and knocked.",
        )
        report = sc.check_prose(text)
        self.assertEqual(report.total_matches, 0)
        self.assertEqual(report.total_violations, 0)


# ---------------------------------------------------------------------------
# Caps and totals
# ---------------------------------------------------------------------------

class EffectiveCapTest(unittest.TestCase):
    def test_fixed_cap_ignores_length(self):
        p = {"name": "x", "cap": 4}
        for words in (0, 10, 100000):
            self.assertEqual(sc.effective_cap(p, words), 4)

    def test_cap_per_words_scales(self):
        p = {"name": "x", "cap": 1, "cap_per_words": 500}
        self.assertEqual(sc.effective_cap(p, 0), 1)       # no words: the fixed cap
        self.assertEqual(sc.effective_cap(p, 499), 1)     # never below one
        self.assertEqual(sc.effective_cap(p, 1000), 2)
        self.assertEqual(sc.effective_cap(p, 2600), 5)

    def test_real_scaled_pattern(self):
        p = PATTERN["punct_semicolon"]
        self.assertEqual(p["cap_per_words"], 500)
        self.assertEqual(sc.effective_cap(p, 1500), 3)

    def test_report_uses_scaled_cap(self):
        # 600 words with two semicolons: cap max(1, 600 // 500) = 1, so over.
        filler = " ".join(["word"] * 597)
        report = sc.check_prose(f"One; two; three. {filler}\n")
        pr = pattern_result(report, "punct_semicolon")
        self.assertEqual(report.total_words, 600)
        self.assertEqual((pr.count, pr.cap, pr.over_cap), (2, 1, True))
        self.assertTrue(all(m.cap == 1 for m in pr.matches))


class TotalsTest(unittest.TestCase):
    def test_header_words_not_counted(self):
        report = sc.check_prose("# Chapter One Title Words\n\nThe cart stopped.\n")
        self.assertEqual(report.total_words, 3)

    def test_empty_text(self):
        report = sc.check_prose("")
        self.assertEqual((report.total_words, report.total_matches, report.total_violations), (0, 0, 0))

    def test_pattern_over_cap_counts_one_violation(self):
        text = paragraphs(
            "Ana nodded. Ben nodded. Cal nodded at the door.",
            "Dora nodded, and Ed nodded too. Fen sighed. Gil sighed.",
        )
        report = sc.check_prose(text)
        nodded = pattern_result(report, "filler_nodded")
        self.assertEqual((nodded.count, nodded.cap, nodded.over_cap), (5, 4, True))
        self.assertEqual(pattern_result(report, "filler_sighed").count, 2)
        self.assertEqual(report.total_matches, 7)
        self.assertEqual(report.total_violations, 1)
        self.assertFalse(category_result(report, "filler_actions").over_combined_cap)

    def test_combined_cap_counts_one_violation(self):
        # 16 filler actions, none over its own cap of 4, over the category's combined 15.
        sentences = [f"{who} {verb}." for verb in ("nodded", "sighed", "smiled", "shrugged")
                     for who in ("Ana", "Ben", "Cal", "Dora")]
        report = sc.check_prose(paragraphs(" ".join(sentences[:8]), " ".join(sentences[8:])))
        cat = category_result(report, "filler_actions")
        self.assertEqual(cat.combined_cap, COMBINED_CAPS["filler_actions"])
        self.assertEqual(cat.combined_count, 16)
        self.assertTrue(cat.over_combined_cap)
        self.assertFalse(any(pr.over_cap for pr in cat.patterns))
        self.assertEqual(report.total_violations, 1)
        # Categories over a combined cap sort first.
        self.assertEqual(report.categories[0].category, "filler_actions")

    def test_pattern_and_combined_both_count(self):
        verbs = ["nodded"] * 5 + ["sighed"] * 4 + ["smiled"] * 4 + ["shrugged"] * 3
        # A different opener per paragraph, so no paragraph-structure violation joins in.
        text = paragraphs(*[" ".join(f"{who} {v}." for v in verbs[i:i + 4])
                            for who, i in zip(("Ana", "Ben", "Cal", "Dora"), range(0, 16, 4))])
        report = sc.check_prose(text)
        self.assertEqual(category_result(report, "filler_actions").combined_count, 16)
        self.assertEqual(report.total_violations, 2)

    def test_header_lines_keep_line_numbers(self):
        text = "# Chapter Two\n\nThe rain stopped.\nHe nodded at the gate.\n"
        match = pattern_result(sc.check_prose(text), "filler_nodded").matches[0]
        self.assertEqual(match.line_number, 4)
        self.assertEqual(text.split("\n")[match.line_number - 1], "He nodded at the gate.")


class MatchLocationTest(unittest.TestCase):
    def test_line_numbers(self):
        text = "First line.\nSecond line where he nodded.\n\nThird line.\n\nHe nodded again.\n"
        matches = pattern_result(sc.check_prose(text), "filler_nodded").matches
        self.assertEqual([m.line_number for m in matches], [2, 6])
        self.assertEqual([m.matched_text for m in matches], ["nodded", "nodded"])

    def test_context_window_and_ellipses(self):
        before, after = "a" * 50, "b" * 50
        text = f"{before} nodded {after}"
        m = pattern_result(sc.check_prose(text), "filler_nodded").matches[0]
        start = text.index("nodded")
        self.assertEqual(m.context, "..." + text[start - 40:start + 6 + 40] + "...")

    def test_context_flattens_newlines_and_trims_at_edges(self):
        text = "He nodded.\nShe went out."
        m = pattern_result(sc.check_prose(text), "filler_nodded").matches[0]
        self.assertEqual(m.context, "He nodded. She went out.")
        self.assertEqual(sc._context_snippet(text, 3, 9), "He nodded. She went out.")
        self.assertEqual(sc._line_number(text, text.index("She")), 2)


# ---------------------------------------------------------------------------
# Paragraph opener rules
# ---------------------------------------------------------------------------

def opener_violations(text):
    return {v["name"]: v for v in sc._check_paragraph_openers(text)}


def line_of_paragraph(text, para):
    return text[:text.index(para)].count("\n") + 1


class ParagraphOpenerTest(unittest.TestCase):
    def test_three_consecutive_same_opener(self):
        text = paragraphs("The rain came.", "The road went soft.", "The carts stopped.", "Nobody spoke.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual((v["count"], v["cap"]), (1, 0))
        m = v["matches"][0]
        self.assertEqual(m.matched_text, "3x 'the'")
        self.assertEqual(m.line_number, 1)

    def test_two_consecutive_is_fine(self):
        text = paragraphs("The rain came.", "The road went soft.", "Carts stopped.", "The end.")
        self.assertNotIn("opener_consecutive_repeat", opener_violations(text))

    def test_opener_normalised_for_case_and_punctuation(self):
        text = paragraphs("Still, nothing.", "STILL the rain.", "still.", "Done.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual(v["matches"][0].matched_text, "3x 'still'")

    def test_each_run_reported(self):
        text = paragraphs("A cart.", "A horse.", "A boy.", "Then rain.", "B one.", "B two.", "B three.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual(v["count"], 2)
        self.assertEqual([m.matched_text for m in v["matches"]], ["3x 'a'", "3x 'b'"])
        self.assertEqual(v["matches"][1].line_number, line_of_paragraph(text, "B one."))

    def test_dialogue_opener_is_first_word_inside_quote(self):
        text = paragraphs('"Wait for her," she said.', '“Wait here.”', '"Wait for me," he called.',
                          "They waited.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual(v["matches"][0].matched_text, "3x 'wait'")

    # BUG (tools/slop_checker/check.py, _check_paragraph_openers): the opener is
    # normalised with rstrip(".,;:!?") only, so a closing quote stays attached:
    # '"Wait," she said.' gives 'wait,"' and '“Wait.”' gives 'wait.”', which no
    # longer match 'wait' from '"Wait for me," he called.'
    def test_dialogue_opener_ignores_closing_quote(self):
        # Regression: openers kept their closing quote ('wait,"'), so this run was missed.
        text = paragraphs('"Wait," she said.', '“Wait.”', '"Wait for me," he called.', "They waited.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual(v["matches"][0].matched_text, "3x 'wait'")

    def test_she_density(self):
        text = paragraphs("She ran.", "He followed.", "She stopped.", "It rained.", "She turned.", "She went in.")
        v = opener_violations(text)["opener_she_density"]
        self.assertEqual(v["count"], 1)
        self.assertEqual(v["matches"][0].matched_text, "4/6 'She' openers")
        self.assertNotIn("opener_consecutive_repeat", opener_violations(text))

    def test_three_she_in_six_is_fine(self):
        text = paragraphs("She ran.", "He followed.", "She stopped.", "It rained.", "She turned.", "They went in.")
        self.assertNotIn("opener_she_density", opener_violations(text))

    def test_she_density_reports_worst_window(self):
        paras = ["Rain fell.", "Wind rose.", "She ran.", "She hid.", "She waited.", "She listened.", "She slept.",
                 "Dawn came."]
        text = paragraphs(*paras)
        v = opener_violations(text)["opener_she_density"]
        m = v["matches"][0]
        self.assertEqual(m.matched_text, "5/6 'She' openers")
        # The first window with five starts at paragraph 1 ("Wind rose.").
        self.assertEqual(m.line_number, line_of_paragraph(text, "Wind rose."))

    def test_short_paragraph_reports_its_own_line(self):
        # "No." also appears inside the first paragraph. The run starts at the
        # stand-alone "No." on line 3, not at the earlier occurrence on line 1.
        text = paragraphs("She told him No. twice.", "No.", "No, not today.", "No one came.")
        m = opener_violations(text)["opener_consecutive_repeat"]["matches"][0]
        self.assertEqual(m.matched_text, "3x 'no'")
        self.assertEqual(m.line_number, 3)

    def test_repeated_paragraph_reports_its_own_line(self):
        text = paragraphs("She ran.", "Rain.", "She ran.", "She ran.", "She ran.", "Wind.")
        v = opener_violations(text)["opener_consecutive_repeat"]
        self.assertEqual(v["matches"][0].line_number, 5)

    def test_paragraph_violations_reach_report(self):
        text = paragraphs("The rain came.", "The road went soft.", "The carts stopped.")
        report = sc.check_prose(text)
        cat = category_result(report, "paragraph_structure")
        self.assertIsNone(cat.combined_cap)
        self.assertEqual(cat.combined_count, 1)
        self.assertEqual(report.total_violations, 1)
        self.assertEqual(report.total_matches, 1)

    def test_headers_are_not_paragraphs(self):
        text = "# The Title\n\nThe rain came.\n\nThe road went soft.\n\nCarts stopped.\n"
        self.assertEqual(sc.check_prose(text).total_violations, 0)


# ---------------------------------------------------------------------------
# JSON contract (the slop-gate docs read these keys)
# ---------------------------------------------------------------------------

CONTRACT_TEXT = paragraphs(
    "# Chapter Three",
    "Ana nodded. Ben nodded. Cal nodded. Dora nodded. Ed nodded at the door.",
    "The silence stretched. The room was too quiet for comfort.",
    "The rain came.", "The road went soft.", "The carts stopped.",
)


class JsonContractTest(unittest.TestCase):
    def setUp(self):
        self.report = sc.check_prose(CONTRACT_TEXT)
        self.data = sc.report_dict(self.report, "some/file.md")

    def test_format_json_is_report_dict(self):
        self.assertEqual(json.loads(sc.format_json(self.report, "some/file.md")), self.data)

    def test_top_level_keys(self):
        self.assertEqual(set(self.data), {"file", "total_words", "total_matches", "total_violations", "categories"})
        self.assertEqual(self.data["file"], "some/file.md")
        self.assertEqual(self.data["total_words"], self.report.total_words)
        self.assertEqual(self.data["total_matches"], self.report.total_matches)
        self.assertEqual(self.data["total_violations"], self.report.total_violations)

    def test_category_and_pattern_keys(self):
        self.assertTrue(self.data["categories"])
        for cat in self.data["categories"]:
            with self.subTest(category=cat["category"]):
                has_combined = cat["category"] in COMBINED_CAPS
                expected = {"category", "combined_count", "patterns"}
                if has_combined:
                    expected |= {"combined_cap", "over_combined_cap"}
                self.assertEqual(set(cat), expected)
                for p in cat["patterns"]:
                    self.assertEqual(set(p), {"name", "count", "cap", "over_cap", "matches"})
                    self.assertGreater(p["count"], 0)  # zero-count patterns are omitted
                    self.assertEqual(len(p["matches"]), p["count"])
                    for m in p["matches"]:
                        self.assertEqual(set(m), {"text", "line", "context"})
                        self.assertIsInstance(m["line"], int)

    def test_expected_content(self):
        cats = {c["category"]: c for c in self.data["categories"]}
        nodded = next(p for p in cats["filler_actions"]["patterns"] if p["name"] == "filler_nodded")
        self.assertEqual((nodded["count"], nodded["cap"], nodded["over_cap"]), (5, 4, True))
        self.assertEqual(nodded["matches"][0]["line"], 3)
        self.assertIn("paragraph_structure", cats)
        self.assertNotIn("combined_cap", cats["paragraph_structure"])
        self.assertIn("narrator_verdict", cats)

    def test_empty_categories_omitted(self):
        data = sc.report_dict(sc.check_prose("The cart stopped at the ford.\n"), "x.md")
        self.assertEqual(data["categories"], [])
        self.assertEqual((data["total_matches"], data["total_violations"]), (0, 0))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class CliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="slop-cli-test-")
        cls.path = os.path.join(cls.tmp.name, "chapter.md")
        with open(cls.path, "w", encoding="utf-8") as f:
            f.write(CONTRACT_TEXT)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_json(self):
        rc, out, err = support.run_cli([CHECK_PY, "--json", self.path])
        self.assertEqual(rc, 0, err)
        data = json.loads(out)
        self.assertEqual(data["file"], self.path)
        self.assertEqual(data, sc.report_dict(sc.check_prose(CONTRACT_TEXT), self.path))

    def test_summary_is_default(self):
        rc, out, err = support.run_cli([CHECK_PY, "--summary", self.path])
        self.assertEqual(rc, 0, err)
        self.assertTrue(out.startswith(f"SLOP CHECK: {self.path}"))
        self.assertIn("filler_nodded: 5/4 !!!", out)
        rc2, out2, _ = support.run_cli([CHECK_PY, self.path])
        self.assertEqual(rc2, 0)
        self.assertEqual(out2, out)

    def test_violations(self):
        rc, out, err = support.run_cli([CHECK_PY, "--violations", self.path])
        self.assertEqual(rc, 0, err)
        self.assertTrue(out.startswith(f"SLOP VIOLATIONS: {self.path}"))
        self.assertIn("filler_nodded: 5/4", out)
        self.assertIn("L3:", out)

    def test_missing_file(self):
        missing = os.path.join(self.tmp.name, "nope.md")
        rc, out, err = support.run_cli([CHECK_PY, "--json", missing])
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")
        self.assertIn("File not found", err)

    def test_modes_are_exclusive(self):
        rc, _, err = support.run_cli([CHECK_PY, "--json", "--summary", self.path])
        self.assertEqual(rc, 2)
        self.assertIn("not allowed with", err)


if __name__ == "__main__":
    unittest.main()
