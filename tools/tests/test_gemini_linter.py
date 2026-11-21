"""Gemini prose linter calibration tests: gemini_prose_tics patterns & over-ornate rhythm detection.

All example prose is original, written for these tests.
"""

import os
import tempfile
import unittest

from tools import prose_check
from tools.rhythm_scorer import constants as C
from tools.rhythm_scorer.analyze import analyze_rhythm
from tools.rhythm_scorer.formatters import format_summary, report_dict
from tools.rhythm_scorer.texture import (
    balanced_texture_score,
    find_over_textured_runs,
    texture_interpretation,
    texture_verdict,
)
from tools.slop_checker import check as sc
from tools.slop_checker.patterns import COMBINED_CAPS
from tools.slop_checker.patterns import gemini_prose_tics as gp
from tools.tests import support

PATTERN = {p["name"]: p for p in sc._COMPILED}


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


# Positive match, expected matched substring, and clean negative control for every Gemini pattern.
GEMINI_EXAMPLES = {
    "gemini_neg_wasnt_period": (
        "It wasn't anger. It was colder than that.",
        "It wasn't anger. It was",
        "She wasn't sure what happened. She was ready to leave.",
    ),
    "gemini_neg_wasnt_emdash": (
        "It wasn't a warning—it was a threat.",
        "It wasn't a warning—it was",
        "It wasn't raining—the road stayed dry.",
    ),
    "gemini_neg_not_emdash": (
        "Not mercy—habit guided her hand.",
        "Not mercy—h",
        "She did not wait—he had already gone.",
    ),
    "gemini_neg_not_merely_out_of": (
        "She stepped back not out of fear, but out of discipline.",
        "not out of fear, but",
        "She stepped out of the room and shut the door.",
    ),
    "gemini_scent_ozone": (
        "The sharp scent of ozone lingered near the arch.",
        "scent of ozone",
        "Rain smelled like wet chalk and pine needles.",
    ),
    "gemini_copper_pair": (
        "The ditch reeked of copper and rot.",
        "copper and rot",
        "She counted three copper coins onto the counter.",
    ),
    "gemini_metallic_tang": (
        "A metallic tang coated the back of her tongue.",
        "metallic tang",
        "The kettle had a tin lid and a loose handle.",
    ),
    "gemini_thick_with_scent": (
        "The cellar was thick with the scent of ash.",
        "thick with the scent of",
        "The stew was thick with barley and onions.",
    ),
    "gemini_bathed_in_light": (
        "The yard lay bathed in pale moonlight.",
        "bathed in pale moonlight",
        "She bathed the horse's bruised fetlock in cold water.",
    ),
    "gemini_pools_of_shadow": (
        "Lanterns left deep pools of shadow along the wall.",
        "pools of shadow",
        "Rainwater sat in shallow pools beside the cart ruts.",
    ),
    "gemini_cast_long_shadows": (
        "The gatehouse cast long shadows across the road.",
        "cast long shadows",
        "He cast the line out past the reeds.",
    ),
    "gemini_broken_only_by": (
        "The quiet was broken only by the creak of saddle leather.",
        "broken only by",
        "The axle had broken two miles past the bridge.",
    ),
    "gemini_shattered_silence": (
        "A crow's call shattered the heavy silence.",
        "shattered the heavy silence",
        "The cold glass shattered on the flagstones.",
    ),
    "gemini_deafening_silence": (
        "A deafening silence settled across the hall.",
        "deafening silence",
        "The bell rang loud enough to make her ears ache.",
    ),
    "gemini_ghost_of_smile": (
        "The ghost of a smile touched the captain's mouth.",
        "The ghost of a smile",
        "The sailors swore a ghost walked the drydock.",
    ),
    "gemini_flicker_of_emotion": (
        "A flicker of doubt crossed his face before he spoke.",
        "A flicker of doubt",
        "The candle gave one last flicker and went out.",
    ),
    "gemini_veneer_facade": (
        "Behind her veneer of calm, she counted the exits.",
        "veneer of",
        "The cabinet had a cracked walnut finish.",
    ),
    "gemini_symphony_labyrinth": (
        "The archive was a labyrinth of ledgers and dust.",
        "labyrinth of",
        "She drew a map of the cellar corridors.",
    ),
    "gemini_sheer_weight_of": (
        "Under the sheer weight of the silence, he looked away.",
        "the sheer weight of",
        "The weight of the pack bit into her shoulders.",
    ),
    "gemini_sliver_of_abstract": (
        "A sliver of relief softened her grip on the hilt.",
        "A sliver of relief",
        "A sliver of pine wedged under his thumbnail.",
    ),
    "gemini_echo_of_abstract": (
        "She heard an echo of grief in the old oath.",
        "an echo of grief",
        "Their boots raised a sharp echo in the cistern.",
    ),
    "gemini_something_body_shifted": (
        "Something in her chest tightened as the latch clicked.",
        "Something in her chest tightened",
        "She packed something warm in her saddlebag.",
    ),
    "gemini_the_kind_of_that": (
        "It was the kind of quiet that preceded an ambush.",
        "the kind of quiet that",
        "He was kind to the stable boy.",
    ),
    "gemini_micro_time": (
        "For a fraction of a second, neither rider moved.",
        "For a fraction of a second",
        "They waited three minutes by the milestone.",
    ),
    "gemini_one_thing_certain": (
        "One thing was certain: the bridge would not hold.",
        "One thing was certain",
        "She checked the bridge timbers twice to be sure.",
    ),
    "gemini_razor_precision": (
        "He trimmed the wick with surgical precision.",
        "surgical precision",
        "He cut the twine cleanly with a belt knife.",
    ),
    "gemini_clinical_bleed": (
        "She watched the ambush unfold with clinical detachment.",
        "clinical detachment",
        "She watched the road from behind the low wall.",
    ),
    "gemini_un_adjectives": (
        "His expression remained unreadable across the table.",
        "unreadable",
        "The faded ink was too smudged to make out.",
    ),
    "gemini_double_barrel_adj": (
        "She let out a slow, measured breath and turned back.",
        "a slow, measured breath",
        "She took a breath and stepped onto the porch.",
    ),
    "gemini_stinger_paragraph": (
        "The gate shut behind them.\n\nSilence.\n\nThey walked on.",
        "Silence.",
        "The gate shut behind them. Silence held until the bells rang.",
    ),
    "gemini_romance_breath_hitched": (
        "Her breath hitched when his hand brushed her sleeve.",
        "breath hitched",
        "He hitched the wagon to the bay mare.",
    ),
    "gemini_romance_pulse_spiked": (
        "Her pulse spiked at the sound of his boots on the stair.",
        "pulse spiked",
        "The iron fence was spiked along the top rail.",
    ),
    "gemini_romance_heat_pooled": (
        "Heat pooled low in her belly as he leaned over the map.",
        "Heat pooled",
        "Water pooled beneath the leaking barrel.",
    ),
    "gemini_romance_gaze_lips": (
        "His gaze dropped to her lips before he stepped back.",
        "gaze dropped to her lips",
        "He dropped the key into his coat pocket.",
    ),
    "gemini_romance_magnetic_pull": (
        "She felt an invisible thread between them across the room.",
        "invisible thread between",
        "She pulled a loose thread from her cuff.",
    ),
}


class GeminiPatternsTest(unittest.TestCase):
    def test_every_gemini_pattern_has_an_example(self):
        defined = {p["name"] for p in gp.PATTERNS}
        self.assertEqual(set(GEMINI_EXAMPLES), defined)

    def test_positive_and_negative_controls(self):
        for name, (positive, expected, negative) in GEMINI_EXAMPLES.items():
            with self.subTest(pattern=name):
                self.assertEqual(hits(name, positive), [expected])
                self.assertEqual(hits(name, negative), [])

    def test_stinger_paragraph_line_numbers_and_adjacent_matches(self):
        text = "They crossed the yard.\n\nSilence.\n\nToo late.\n\nThe lantern went out.\n"
        report = sc.check_prose(text)
        pr = pattern_result(report, "gemini_stinger_paragraph")
        self.assertEqual(pr.count, 2)
        self.assertTrue(pr.over_cap)
        self.assertEqual([m.matched_text for m in pr.matches], ["Silence.", "Too late."])
        self.assertEqual([m.line_number for m in pr.matches], [3, 5])

    def test_capped_patterns_allow_one_and_flag_two(self):
        one = "It wasn't rain. It was sleet. The road stayed empty.\n"
        rep1 = sc.check_prose(one)
        pr1 = pattern_result(rep1, "gemini_neg_wasnt_period")
        self.assertEqual((pr1.count, pr1.cap, pr1.over_cap), (1, 1, False))

        two = "It wasn't rain. It was sleet. That wasn't fog. That was smoke.\n"
        rep2 = sc.check_prose(two)
        pr2 = pattern_result(rep2, "gemini_neg_wasnt_period")
        self.assertEqual((pr2.count, pr2.cap, pr2.over_cap), (2, 1, True))

    def test_combined_cap_catches_accumulated_under_cap_hits(self):
        # 7 hits across distinct patterns (none over individual cap 1 except cap-0s if any —
        # here we use 6 cap-1 patterns plus 1 extra hit to verify COMBINED_CAP = 6).
        self.assertEqual(COMBINED_CAPS["gemini_prose_tics"], 6)
        text = (
            "It wasn't sleet. It was hail. "
            "The taste of ozone lingered. "
            "It was the kind of quiet that warned scouts. "
            "For a fraction of a second he paused. "
            "Her face stayed unreadable. "
            "The ditch smelled of copper and rot.\n\n"
            "Silence.\n"
        )
        report = sc.check_prose(text)
        cat = category_result(report, "gemini_prose_tics")
        self.assertEqual(cat.combined_count, 7)
        self.assertEqual(cat.combined_cap, 6)
        self.assertTrue(cat.over_combined_cap)


class GeminiOverOrnateRhythmTest(unittest.TestCase):
    @staticmethod
    def _cls(emdash=False, participial=False, compound=False, semicolon=False, short=False):
        return {
            "participial": participial,
            "compound": compound,
            "emdash": emdash,
            "semicolon": semicolon,
            "short": short,
            "word_count": 4 if short else 22,
        }

    def test_find_over_textured_runs_emdash_cluster(self):
        seq = [self._cls(emdash=(i < 4)) for i in range(C.ORNATE_WINDOW)]
        runs = find_over_textured_runs(seq, [f"Sentence {i}." for i in range(len(seq))])
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["type"], "over_textured_run")
        self.assertTrue(any("em-dash" in t for t in runs[0]["triggers"]))

    def test_find_over_textured_runs_participial_cluster(self):
        seq = [self._cls(participial=(i < 5)) for i in range(C.ORNATE_WINDOW)]
        runs = find_over_textured_runs(seq, [f"Sentence {i}." for i in range(len(seq))])
        self.assertEqual(len(runs), 1)
        self.assertTrue(any("participial" in t for t in runs[0]["triggers"]))

    def test_find_over_textured_runs_dense_stacked_markers(self):
        # 5 sentences with 2 markers each = 10 markers in 6 sentences, below single-feature thresholds
        seq = [
            self._cls(participial=True, compound=True),
            self._cls(emdash=True, compound=True),
            self._cls(participial=True, semicolon=True),
            self._cls(emdash=True, compound=True),
            self._cls(participial=True, compound=True),
            self._cls(),
        ]
        runs = find_over_textured_runs(seq, [f"Sentence {i}." for i in range(len(seq))])
        self.assertEqual(len(runs), 1)
        self.assertTrue(any("markers" in t for t in runs[0]["triggers"]))

    def test_find_over_textured_runs_ignores_balanced_prose(self):
        seq = [
            self._cls(compound=True),
            self._cls(short=True),
            self._cls(participial=True),
            self._cls(short=True),
            self._cls(emdash=True),
            self._cls(short=True),
        ]
        self.assertEqual(find_over_textured_runs(seq, ["S."] * 6), [])

    def test_interpretation_over_textured_vs_under_textured_vs_mixed(self):
        bl = C.DEFAULT_TEXTURE_BASELINES

        # Pure over-ornate (Gemini failure mode)
        over_m = {
            "participial_pct": 26.0,
            "compound_pct": 9.0,
            "emdash_pct": 18.0,
            "semicolon_pct": 1.0,
            "short_pct": 25.0,
        }
        over_score, over_dims = balanced_texture_score(over_m, bl)
        over_m["texture_score"] = over_score
        verdict, reasons = texture_verdict(over_m, bl, over_dims)
        self.assertEqual(verdict, "below_target")
        interp = texture_interpretation(over_m, bl, verdict, reasons, over_dims)
        self.assertTrue(interp.startswith("OVER-TEXTURED"))
        self.assertIn("Cut excess", interp)
        self.assertIn("Too dense/over-long", interp)

        # Pure under-textured (GPT-5 telegram failure mode)
        under_m = {
            "participial_pct": 1.0,
            "compound_pct": 1.0,
            "emdash_pct": 0.0,
            "semicolon_pct": 0.0,
            "short_pct": 75.0,
        }
        under_score, under_dims = balanced_texture_score(under_m, bl)
        under_m["texture_score"] = under_score
        u_verdict, u_reasons = texture_verdict(under_m, bl, under_dims)
        u_interp = texture_interpretation(under_m, bl, u_verdict, u_reasons, under_dims)
        self.assertTrue(u_interp.startswith("UNDER-TEXTURED"))

        # Mixed (em-dash spam + participial deficit)
        mixed_m = {
            "participial_pct": 1.0,
            "compound_pct": 8.0,
            "emdash_pct": 18.0,
            "semicolon_pct": 1.0,
            "short_pct": 50.0,
        }
        m_score, m_dims = balanced_texture_score(mixed_m, bl)
        mixed_m["texture_score"] = m_score
        m_verdict, m_reasons = texture_verdict(mixed_m, bl, m_dims)
        m_interp = texture_interpretation(mixed_m, bl, m_verdict, m_reasons, m_dims)
        self.assertTrue(m_interp.startswith("MIXED TEXTURE IMBALANCE"))

    def test_end_to_end_ornate_gemini_passage_in_prose_check(self):
        ornate_prose = (
            "The hall—narrow and cold—stretched ahead, bathed in pale moonlight, casting long shadows across the floor. "
            "She halted—her fingers gripping the pommel—watching the stairwell, listening for boots on the stone. "
            "It wasn't fear—it was a flicker of doubt behind her veneer of calm, coiling tight in the quiet. "
            "The air—heavy with the scent of ozone—hung still, broken only by the distant bell, echoing down the nave. "
            "Her breath hitched—a slow, measured breath—and something in her chest tightened with surgical precision. "
            "One thing was certain—the ward had failed—leaving only a sliver of hope in the labyrinth of dark arches.\n\n"
            "Silence.\n\n"
            "Too late.\n"
        )
        r = analyze_rhythm(ornate_prose)
        d = report_dict(r, "ornate.md")
        summary = format_summary(r, "ornate.md")
        self.assertTrue(any(fp["type"] == "over_textured_run" for fp in d["texture"]["flagged_passages"]))
        self.assertIn("[ABOVE]", summary)
        self.assertIn("ACTION:", summary)

        with tempfile.TemporaryDirectory() as tmp:
            path = support.write(os.path.join(tmp, "ornate.md"), ornate_prose)
            report, _ = prose_check.run(path, tools=["rhythm", "slop"])
            self.assertEqual(report["failed"], [])
            slop_cats = {c["category"]: c for c in report["slop"]["categories"]}
            self.assertIn("gemini_prose_tics", slop_cats)
            self.assertTrue(slop_cats["gemini_prose_tics"]["over_combined_cap"])
            self.assertGreaterEqual(slop_cats["gemini_prose_tics"]["combined_count"], 10)


if __name__ == "__main__":
    unittest.main()
