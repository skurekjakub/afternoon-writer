"""tools/rhythm_scorer and the sentence splitter it uses (tools/skeleton_strip/splitter.py).

The calibrator measures the human corpora with this scorer and the gates read
its JSON, so these tests pin both the numbers and the report shape.
All fixture prose is original.
"""

import json
import math
import os
import random
import tempfile
import unittest

from tools.tests import support
from tools.mannered_checker import calibrate as cal
from tools.rhythm_scorer import constants as C
from tools.rhythm_scorer import score
from tools.rhythm_scorer.analyze import analyze_rhythm, report_from_json_targets
from tools.rhythm_scorer.formatters import format_json, report_dict
from tools.rhythm_scorer.rhythm import compute_mattr, count_punctuation, opener_stats
from tools.rhythm_scorer.texture import (
    balanced_texture_score,
    classify_sentence_texture,
    dimension_score,
    find_telegram_runs,
    find_texture_deserts,
    texture_verdict,
)
from tools.skeleton_strip.splitter import split_paragraphs, split_sentences

SCORE_PY = os.path.join("tools", "rhythm_scorer", "score.py")

# Four sentences in three paragraphs; every metric below is worked out by hand.
#   lengths 6, 4, 22, 2 -> short (<=6) 3/4, long (>=20) 1/4, mean 8.5
#   one-sentence paragraphs: 2 of 3; one ', Ving' (", whistling"); one comma
#   openers the, she, tomas, she -> 3 distinct, entropy 1.5 bits
PASSAGE = (
    "The mare stood in the yard. She would not move.\n\n"
    "Tomas came out of the barn with a rope over his shoulder and a bucket "
    "of oats in his other hand, whistling.\n\n"
    "She ate.\n"
)


def texts(sentences):
    return [s.text for s in sentences]


class SplitSentencesTest(unittest.TestCase):
    def test_abbreviations_do_not_split(self):
        text = "Mr. Hale opened the gate. Dr. Venn followed him in. St. Agnes was shut."
        self.assertEqual(texts(split_sentences(text)),
                         ["Mr. Hale opened the gate.", "Dr. Venn followed him in.", "St. Agnes was shut."])

    def test_ellipses_never_end_a_sentence(self):
        self.assertEqual(texts(split_sentences("She waited... Then she knocked. Nobody came.")),
                         ["She waited... Then she knocked.", "Nobody came."])
        self.assertEqual(texts(split_sentences("Wait… She left.")), ["Wait… She left."])

    def test_question_and_exclamation_end_sentences(self):
        self.assertEqual(texts(split_sentences("Was it late? It was! They ran.")),
                         ["Was it late?", "It was!", "They ran."])

    def test_lowercase_after_period_does_not_split(self):
        self.assertEqual(texts(split_sentences("He paused. then he spoke again.")),
                         ["He paused. then he spoke again."])

    def test_decimal_numbers_do_not_split(self):
        self.assertEqual(texts(split_sentences("It cost 3.5 coins. Fine.")), ["It cost 3.5 coins.", "Fine."])

    def test_opening_quote_starts_a_sentence(self):
        sents = split_sentences('She went. "Now?" he asked.')
        self.assertEqual(texts(sents), ["She went.", '"Now?" he asked.'])
        self.assertEqual([s.is_dialogue for s in sents], [False, True])

    def test_closing_quote_after_punctuation_still_splits(self):
        self.assertEqual(len(split_sentences('"Go home." She went.')), 2)
        self.assertEqual(len(split_sentences("He said “Stop.” Then he left.")), 2)

    def test_closing_quote_stays_with_its_sentence(self):
        # Regression: the split regex used to consume the closing quote as part of the
        # delimiter, so the sentence text lost it ('"Go home.' instead of '"Go home."').
        self.assertEqual(texts(split_sentences('"Go home." She went.')), ['"Go home."', "She went."])

    def test_offsets_point_at_the_sentence(self):
        text = "Mr. Hale opened the gate. Was it late? It was! Then, slowly, he sat."
        for s in split_sentences(text):
            self.assertEqual(text[s.start_char:s.end_char], s.text)

    def test_offsets_include_char_offset(self):
        sents = split_sentences("One. Two.", paragraph_index=4, char_offset=100)
        self.assertEqual([(s.start_char, s.end_char, s.paragraph_index) for s in sents], [(100, 104, 4), (105, 109, 4)])
        self.assertEqual([s.index for s in sents], [0, 1])

    def test_blank_text(self):
        self.assertEqual(split_sentences(""), [])
        self.assertEqual(split_sentences("   \n "), [])


class SplitParagraphsTest(unittest.TestCase):
    def test_blank_line_paragraphs_and_offsets(self):
        text = "One. Two.\n\nThree.\n\n\n\nFour is here."
        paras = split_paragraphs(text)
        self.assertEqual([p.text for p in paras], ["One. Two.", "Three.", "Four is here."])
        self.assertEqual([len(p.sentences) for p in paras], [2, 1, 1])
        self.assertEqual([p.index for p in paras], [0, 1, 2])
        for p in paras:
            self.assertEqual(text[p.start_char:p.end_char], p.text)
            for s in p.sentences:
                self.assertEqual(text[s.start_char:s.end_char], s.text)

    def test_headings_are_skipped(self):
        paras = split_paragraphs("# Chapter One\n\nThe road was wet.\n\n## Part two\n\nIt dried.")
        self.assertEqual([p.text for p in paras], ["The road was wet.", "It dried."])

    def test_frontmatter_is_stripped(self):
        paras = split_paragraphs("---\ntitle: test\nauthor: nobody\n---\nOne. Two.\n\nThree.\n")
        self.assertEqual([p.text for p in paras], ["One. Two.", "Three."])

    def test_hard_wrapped_text_is_unwrapped(self):
        lines = []
        for n in range(20):
            lines += [f"Paragraph {n} begins here and runs on",
                      "across the wrap without stopping until",
                      "it reaches the end of its thought."]
        paras = split_paragraphs("\n".join(lines))
        self.assertEqual(len(paras), 20)
        self.assertEqual(paras[3].text, "Paragraph 3 begins here and runs on across the wrap "
                                        "without stopping until it reaches the end of its thought.")
        self.assertTrue(all(len(p.sentences) == 1 for p in paras))

    def test_short_text_with_single_newlines_is_not_unwrapped(self):
        paras = split_paragraphs("Line one.\nline two.")
        self.assertEqual(len(paras), 1)
        self.assertEqual(paras[0].text, "Line one.\nline two.")

    def test_empty(self):
        self.assertEqual(split_paragraphs(""), [])


def naive_mattr(words, window=50):
    """The direct definition: mean type-token ratio over every window."""
    if len(words) < window:
        return len(set(words)) / len(words) if words else 0.0
    ttrs = [len(set(words[i:i + window])) / window for i in range(len(words) - window + 1)]
    return sum(ttrs) / len(ttrs)


class RhythmHelpersTest(unittest.TestCase):
    @staticmethod
    def random_cases(seed=1234, trials=300):
        rng = random.Random(seed)
        for trial in range(trials):
            vocab = [f"w{i}" for i in range(rng.randint(1, 40))]
            words = [rng.choice(vocab) for _ in range(rng.randint(0, 400))]
            yield trial, words, rng.randint(1, 60)

    def test_mattr_matches_naive_definition(self):
        for trial, words, window in self.random_cases():
            self.assertAlmostEqual(compute_mattr(words, window), naive_mattr(words, window), places=12,
                                   msg=(trial, len(words), window))

    def test_mattr_bit_identical_to_naive_definition(self):
        # Regression: an O(n) version that summed with `total += ...` drifted in the last
        # bits from sum(list), which is compensated since Python 3.12
        # (0.6142533936651582 vs ...584 for 59 words, window 34).
        for trial, words, window in self.random_cases():
            self.assertEqual(compute_mattr(words, window), naive_mattr(words, window), (trial, len(words), window))

    def test_mattr_default_window_and_edges(self):
        words = ("the cat sat on the mat and the dog sat on the log " * 20).split()
        self.assertAlmostEqual(compute_mattr(words), naive_mattr(words, 50), places=12)
        self.assertEqual(compute_mattr([]), 0.0)
        self.assertEqual(compute_mattr(["a", "b", "a"]), 2 / 3)  # shorter than the window
        self.assertAlmostEqual(compute_mattr(["x"] * 60), 1 / 50, places=12)
        self.assertAlmostEqual(compute_mattr([str(i) for i in range(60)]), 1.0, places=12)

    def test_opener_entropy(self):
        distinct, entropy, top = opener_stats(["Alpha one.", "beta two.", "Gamma.", "delta"])
        self.assertEqual(distinct, 4)
        self.assertAlmostEqual(entropy, 2.0, places=12)
        self.assertEqual(len(top), 4)
        distinct, entropy, top = opener_stats(["She ran.", "She hid.", "The dog barked.", "Tomas laughed."])
        self.assertEqual(distinct, 3)
        self.assertAlmostEqual(entropy, 1.5, places=12)
        self.assertEqual(top[0], ("she", 2))

    def test_opener_quotes_are_stripped(self):
        _, _, top = opener_stats(['"Hello there."', "“Hello again.”", "‘Hello’ she said."])
        self.assertEqual(top, [("hello", 3)])

    def test_opener_edge_cases(self):
        self.assertEqual(opener_stats([]), (0, 0.0, []))
        self.assertEqual(opener_stats(["", "   ", '"'])[0], 0)
        self.assertEqual(opener_stats(["Same.", "Same.", "Same."])[1], 0.0)

    def test_count_punctuation(self):
        self.assertEqual(count_punctuation("no punctuation here"), (0, 1))
        self.assertEqual(count_punctuation(""), (0, 1))
        self.assertEqual(count_punctuation("A, b. C! D? E..."), (1, 4))
        self.assertEqual(count_punctuation("What?!"), (0, 1))


def cls(short=True, texture=False):
    return {"participial": texture, "compound": False, "emdash": False, "semicolon": False,
            "short": short, "word_count": 4 if short else 15}


class TextureTest(unittest.TestCase):
    def test_classify_flags(self):
        c = classify_sentence_texture("She stood, turning back to the fire, and waited.")
        self.assertTrue(c["participial"])
        self.assertTrue(c["compound"])
        self.assertFalse(c["emdash"])
        self.assertFalse(c["semicolon"])
        self.assertFalse(c["short"])
        self.assertEqual(c["word_count"], 9)
        self.assertTrue(classify_sentence_texture("The door—open—stood.")["emdash"])
        self.assertTrue(classify_sentence_texture("The door--open--stood.")["emdash"])
        self.assertTrue(classify_sentence_texture("She waited; he did not.")["semicolon"])
        for conj in ("and", "but", "or", "yet", "so"):
            self.assertTrue(classify_sentence_texture(f"It rained, {conj} they left.")["compound"], conj)
        plain = classify_sentence_texture("The dog slept by the gate.")
        self.assertEqual([plain[k] for k in ("participial", "compound", "emdash", "semicolon")], [False] * 4)

    def test_short_threshold(self):
        eight = " ".join(["word"] * C.SHORT_THRESHOLD) + "."
        nine = " ".join(["word"] * (C.SHORT_THRESHOLD + 1)) + "."
        self.assertTrue(classify_sentence_texture(eight)["short"])
        self.assertFalse(classify_sentence_texture(nine)["short"])

    def test_telegram_run_found_and_extended(self):
        run = [cls() for _ in range(C.TELEGRAM_WINDOW + 2)]
        flagged = find_telegram_runs(run, [f"s{i}." for i in range(len(run))])
        self.assertEqual(len(flagged), 1)
        f = flagged[0]
        self.assertEqual((f["type"], f["start_sentence"], f["end_sentence"], f["sentence_count"]),
                         ("telegram_run", 0, len(run) - 1, len(run)))
        self.assertEqual(f["short_pct_in_run"], 100.0)
        self.assertEqual(f["preview"], "s0. s1. s2.")

    def test_telegram_needs_a_full_window(self):
        self.assertEqual(find_telegram_runs([cls()] * (C.TELEGRAM_WINDOW - 1), ["s."] * 7), [])

    def test_telegram_threshold_and_texture(self):
        n_short = math.ceil(C.TELEGRAM_SHORT_PCT * C.TELEGRAM_WINDOW)
        window = [cls() for _ in range(n_short)] + [cls(short=False) for _ in range(C.TELEGRAM_WINDOW - n_short)]
        self.assertEqual(len(find_telegram_runs(window, ["s."] * len(window))), 1)
        too_few = [cls() for _ in range(n_short - 1)] + [cls(short=False) for _ in range(C.TELEGRAM_WINDOW - n_short + 1)]
        self.assertEqual(find_telegram_runs(too_few, ["s."] * len(too_few)), [])
        textured = [cls() for _ in range(C.TELEGRAM_WINDOW)]
        textured[3] = cls(texture=True)
        self.assertEqual(find_telegram_runs(textured, ["s."] * len(textured)), [])

    def test_texture_deserts(self):
        n = C.DESERT_MIN_SENTENCES
        seq = [cls(short=False) for _ in range(n)] + [cls(texture=True)] + [cls(short=False) for _ in range(n - 1)]
        deserts = find_texture_deserts(seq, [f"s{i}." for i in range(len(seq))])
        self.assertEqual([(d["start_sentence"], d["end_sentence"], d["sentence_count"]) for d in deserts], [(0, n - 1, n)])
        trailing = [cls(texture=True)] + [cls(short=False) for _ in range(n)]
        deserts = find_texture_deserts(trailing, ["s."] * len(trailing))
        self.assertEqual([(d["start_sentence"], d["end_sentence"]) for d in deserts], [(1, n)])
        self.assertEqual(find_texture_deserts([cls(texture=True)] * 30, ["s."] * 30), [])
        self.assertEqual(find_texture_deserts([], []), [])

    def test_dimension_score(self):
        self.assertEqual(dimension_score(10.0, 10.0), 100.0)
        self.assertEqual(dimension_score(10.9, 10.0), 100.0)  # inside the tolerance
        self.assertAlmostEqual(dimension_score(12.0, 10.0), 100 - 25 * math.log(2))
        self.assertAlmostEqual(dimension_score(8.0, 10.0), dimension_score(12.0, 10.0))  # symmetric
        scores = [dimension_score(10.0 + d, 10.0) for d in (1, 2, 4, 8, 16)]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(dimension_score(1e9, 0.0), 0.0)

    def test_balanced_score(self):
        bl = C.DEFAULT_TEXTURE_BASELINES
        on_target = {k: bl[k]["target"] for k in ("participial_pct", "compound_pct", "emdash_pct", "semicolon_pct")}
        overall, details = balanced_texture_score(on_target, bl)
        self.assertEqual(overall, 100.0)
        self.assertEqual(set(details), {"participial", "compound", "emdash", "semicolon"})
        off = dict(on_target, emdash_pct=on_target["emdash_pct"] + 10)
        overall_off, details_off = balanced_texture_score(off, bl)
        self.assertLess(overall_off, 100.0)
        self.assertLess(details_off["emdash"]["score"], 100.0)
        self.assertEqual(details_off["compound"]["score"], 100.0)

    def test_verdict(self):
        bl = C.DEFAULT_TEXTURE_BASELINES
        lo, hi = bl["short_pct"]["range"]
        mid = (lo + hi) / 2
        self.assertEqual(texture_verdict({"texture_score": 95.0, "short_pct": mid}, bl), ("within_target", []))
        self.assertEqual(texture_verdict({"texture_score": 80.0, "short_pct": mid}, bl)[0], "below_target")
        verdict, reasons = texture_verdict({"texture_score": 99.0, "short_pct": hi + 5}, bl)
        self.assertEqual(verdict, "below_target")
        self.assertIn("above ceiling", reasons[0])
        verdict, reasons = texture_verdict({"texture_score": 99.0, "short_pct": lo - 5}, bl)
        self.assertIn("below floor", reasons[0])
        dims = {"emdash": {"actual": 9.0, "target": 3.5, "score": 50.0}}
        verdict, reasons = texture_verdict({"texture_score": 95.0, "short_pct": mid}, bl, dims)
        self.assertEqual(verdict, "within_target")  # a weak dimension is reported, not failed on its own
        self.assertTrue(any(r.startswith("emdash: 9.0% above target") for r in reasons))


class AnalyzeRhythmTest(unittest.TestCase):
    def test_hand_computed_passage(self):
        r = analyze_rhythm(PASSAGE)
        self.assertEqual(r.sentence_count, 4)
        self.assertEqual(r.mean_sentence_length, 8.5)
        self.assertEqual(r.short_sentence_pct, 0.75)
        self.assertEqual(r.long_sentence_pct, 0.25)
        self.assertEqual(r.paragraph_count, 3)
        self.assertAlmostEqual(r.one_sentence_paragraph_pct, 2 / 3)
        self.assertAlmostEqual(r.mean_paragraph_sentences, 4 / 3)
        self.assertEqual((r.commas, r.periods), (1, 4))
        self.assertEqual(r.cp_ratio, 0.25)
        self.assertEqual(r.opener_count, 3)
        self.assertAlmostEqual(r.opener_entropy, 1.5)
        self.assertEqual(r.participial_pct, 25.0)
        self.assertEqual(r.compound_pct, 0.0)
        self.assertEqual(r.texture_short_pct, 75.0)  # 6, 4 and 2 words are all <= 8
        lengths = [6, 4, 22, 2]
        stdev = math.sqrt(sum((n - 8.5) ** 2 for n in lengths) / 4)
        self.assertAlmostEqual(r.stdev_sentence_length, stdev)
        self.assertAlmostEqual(r.cv_sentence_length, stdev / 8.5)

    def test_empty_text_returns_zeros(self):
        for text in ("", "   \n\n  ", "# Only a heading\n"):
            r = analyze_rhythm(text)
            self.assertEqual(r.sentence_count, 0)
            self.assertEqual(r.mean_sentence_length, 0.0)
            self.assertEqual(r.mattr, 0.0)
            self.assertEqual(r.texture_score, 0.0)
            report_dict(r, "empty.md")  # formatting must not divide by zero either

    def test_baselines_default(self):
        self.assertEqual(analyze_rhythm(PASSAGE).texture_baselines, C.DEFAULT_TEXTURE_BASELINES)
        custom = json.loads(json.dumps(C.DEFAULT_TEXTURE_BASELINES))
        custom["participial_pct"]["target"] = 25.0
        r = analyze_rhythm(PASSAGE, texture_baselines=custom)
        self.assertEqual(r.texture_dimension_scores["participial"]["score"], 100.0)


def dig(d, path):
    for k in path:
        d = d[k]
    return d


class FormatterContractTest(unittest.TestCase):
    def setUp(self):
        self.report = analyze_rhythm(PASSAGE)
        self.d = report_dict(self.report, "passage.md")

    def test_json_is_the_dict(self):
        self.assertEqual(json.loads(format_json(self.report, "passage.md")), self.d)

    def test_keys_the_calibrator_reads(self):
        for key, path in cal.RHYTHM_KEYS.items():
            self.assertIsInstance(dig(self.d, path), (int, float), key)
        for key in cal.TEXTURE_KEYS:
            self.assertIsInstance(self.d["texture"][key], (int, float), key)

    def test_keys_the_gates_read(self):
        self.assertEqual(self.d["file"], "passage.md")
        self.assertIsInstance(self.d["comma_period_ratio"], float)
        for k in ("count", "mean_length", "stdev_length", "cv_length", "short_pct", "long_pct"):
            self.assertIn(k, self.d["sentence"])
        for k in ("distinct_count", "entropy", "top_5"):
            self.assertIn(k, self.d["openers"])
        for k in ("count", "mean_sentences", "stdev_sentences", "one_sentence_pct"):
            self.assertIn(k, self.d["paragraph"])
        for k in ("mattr", "unique_words", "total_words"):
            self.assertIn(k, self.d["vocabulary"])
        for k in ("participial_pct", "compound_pct", "emdash_pct", "semicolon_pct", "short_pct", "texture_score",
                  "dimension_scores", "verdict", "verdict_reasons", "interpretation", "baselines", "flagged_passages"):
            self.assertIn(k, self.d["texture"])
        self.assertIn(self.d["texture"]["verdict"], ("within_target", "below_target"))
        self.assertIsInstance(self.d["texture"]["interpretation"], str)
        self.assertEqual(self.d["openers"]["top_5"][0], {"word": "she", "count": 2})

    def test_percentages_are_reported_as_percent(self):
        self.assertEqual(self.d["sentence"]["short_pct"], 75.0)
        self.assertEqual(self.d["sentence"]["long_pct"], 25.0)
        self.assertEqual(self.d["paragraph"]["one_sentence_pct"], 66.7)


class ScoreModuleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rhythm-test-")
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))
        self.prose = support.write(os.path.join(self.tmp, "draft.md"), PASSAGE)

    def test_load_texture_baselines(self):
        self.assertIs(score.load_texture_baselines(None), C.DEFAULT_TEXTURE_BASELINES)
        custom = {"participial_pct": {"human": 1.0, "target": 2.0, "range": [1.0, 3.0]}}
        with_tex = support.write(os.path.join(self.tmp, "with.json"), json.dumps({"textureMetrics": custom}))
        self.assertEqual(score.load_texture_baselines(with_tex), custom)
        without = support.write(os.path.join(self.tmp, "without.json"), json.dumps({"rhythmMetrics": {}}))
        self.assertIs(score.load_texture_baselines(without), C.DEFAULT_TEXTURE_BASELINES)

    def test_score_file_equals_cli_json(self):
        guide = support.write(os.path.join(self.tmp, "guide.json"),
                              json.dumps({"textureMetrics": C.DEFAULT_TEXTURE_BASELINES}))
        for baselines in (None, guide):
            args = [SCORE_PY, "--json", self.prose] + (["--baselines", baselines] if baselines else [])
            code, out, err = support.run_cli(args)
            self.assertEqual(code, 0, err)
            self.assertEqual(score.score_file(self.prose, baselines), json.loads(out))

    def test_report_from_json_targets(self):
        guide = {
            "rhythmMetrics": {"global": {
                "comma_period_ratio": {"target": 0.7, "measured": 0.5},
                "sentence_length_mean": {"measured": 11.0},
                "sentence_length_cv": {"human": 0.6},
                "short_sentence_pct": {"target": 30.0},
                "long_sentence_pct": 12.0,
                "opener_entropy": {"target": 6.5},
                "one_sentence_paragraph_pct": {"target": 20.0},
                "mattr": {"target": 0.85},
            }},
            "textureMetrics": {"participial_pct": {"target": 7.0}, "emdash_pct": {"human": 5.0}},
        }
        path = support.write(os.path.join(self.tmp, "guide.json"), json.dumps(guide))
        r = report_from_json_targets(path)
        self.assertEqual(r.cp_ratio, 0.7)  # target wins over measured
        self.assertEqual(r.mean_sentence_length, 11.0)  # measured when there is no target
        self.assertEqual(r.cv_sentence_length, 0.6)  # human as the last fallback
        self.assertEqual(r.short_sentence_pct, 0.30)  # percent -> fraction
        self.assertEqual(r.long_sentence_pct, 0.12)  # bare numbers are accepted
        self.assertEqual(r.one_sentence_paragraph_pct, 0.20)
        self.assertEqual((r.opener_entropy, r.mattr), (6.5, 0.85))
        self.assertEqual((r.participial_pct, r.emdash_pct, r.compound_pct), (7.0, 5.0, 0))
        self.assertEqual((r.texture_score, r.texture_verdict), (100.0, "stored_target"))
        self.assertEqual(r.texture_baselines, guide["textureMetrics"])


class ScoreCliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="rhythm-cli-")
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))
        self.prose = support.write(os.path.join(self.tmp, "draft.md"), PASSAGE)

    def test_json(self):
        code, out, err = support.run_cli([SCORE_PY, "--json", self.prose])
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["file"], self.prose)
        self.assertEqual(d["sentence"]["count"], 4)

    def test_summary_is_the_default(self):
        code, explicit, _ = support.run_cli([SCORE_PY, "--summary", self.prose])
        self.assertEqual(code, 0)
        self.assertTrue(explicit.startswith("RHYTHM & TEXTURE:"))
        code, default, _ = support.run_cli([SCORE_PY, self.prose])
        self.assertEqual(code, 0)
        self.assertEqual(default, explicit)

    def test_headers_are_ignored(self):
        headed = support.write(os.path.join(self.tmp, "headed.md"), "# Chapter 1\n\n" + PASSAGE + "\n## End\n")
        _, out, _ = support.run_cli([SCORE_PY, "--json", headed])
        _, plain, _ = support.run_cli([SCORE_PY, "--json", self.prose])
        a, b = json.loads(out), json.loads(plain)
        a.pop("file"), b.pop("file")
        self.assertEqual(a, b)

    def test_compare(self):
        other = support.write(os.path.join(self.tmp, "other.md"), "It rained. It stopped. They left the barn, and the dog came too.\n")
        code, out, err = support.run_cli([SCORE_PY, "--compare", self.prose, "--target", other])
        self.assertEqual(code, 0, err)
        self.assertIn(other, out)
        code, _, err = support.run_cli([SCORE_PY, "--compare", self.prose])
        self.assertEqual(code, 1)
        self.assertIn("--compare requires", err)

    def test_missing_file(self):
        code, out, err = support.run_cli([SCORE_PY, "--json", os.path.join(self.tmp, "nope.md")])
        self.assertEqual(code, 1)
        self.assertIn("File not found", err)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
