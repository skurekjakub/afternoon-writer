"""tools/prose_check.py: the unified runner gives each tool's own report, isolates failures."""

import argparse
import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest import mock

from tools.tests import support
from tools import prose_check
from tools.mannered_checker import check as mc
from tools.prose_core.text import read_text
from tools.rhythm_scorer.score import score_file
from tools.slop_checker.check import check_prose, report_dict

CHAPTER = """\
# Chapter Three

The kettle sang on the hob while Ada counted the coins twice. She was certain, she noticed, that one was missing. It was a long way to the market, the way a man walks when he is late.

"Count them again," her brother said.

She counted them again. The light was failing, and the shutters knocked, and the dog barked, and the gate swung.

No.

She put the coins back in the jar.
"""


def style_guide():
    return {"textureMetrics": {
        "participial_pct": {"human": 6.0, "target": 7.0, "range": [7.0, 10.0]},
        "compound_pct": {"human": 12.0, "target": 14.0, "range": [11.0, 17.0]},
        "emdash_pct": {"human": 4.5, "target": 5.0, "range": [3.5, 6.5]},
        "semicolon_pct": {"human": 1.2, "target": 1.6, "range": [0.8, 2.3]},
        "short_pct": {"human": 45.0, "target": 41.0, "range": [33.0, 48.0]},
        "texture_score": {"human": 100.0, "target": 100.0, "range": [90.0, 100.0]},
    }}


class RunInProcessTest(unittest.TestCase):
    def test_blocks_equal_each_tools_own_report(self):
        with support.TempRepo(chapters={1: support.HUMAN_PROSE}, style_guide=style_guide()) as repo:
            target = repo.chapter(2, "v2.md", CHAPTER)
            baselines = repo.path(".afternoon", "style-guide.json")
            mc.check(target)  # calibrate the temp repo first, so the next runs don't recalibrate
            report, summaries = prose_check.run(target, baselines=baselines)
            self.assertEqual(report["tools"], ["rhythm", "slop", "mannered"])
            self.assertEqual(report["failed"], [])
            self.assertEqual(report["rhythm"], score_file(target, baselines))
            self.assertEqual(report["slop"], report_dict(check_prose(read_text(target)), target))
            self.assertEqual(report["mannered"], mc.check(target))
            self.assertEqual(set(summaries), {"rhythm", "slop", "mannered"})
            self.assertIn("pattern hits", summaries["mannered"])

    def test_subset_of_tools(self):
        with tempfile.TemporaryDirectory() as d:
            path = support.write(os.path.join(d, "ch.md"), CHAPTER)
            report, summaries = prose_check.run(path, tools=["slop"])
            self.assertEqual(set(report), {"file", "tools", "failed", "slop"})
            self.assertEqual(list(summaries), ["slop"])

    def test_default_baselines_come_from_the_style_guide(self):
        with tempfile.TemporaryDirectory() as d:
            guide = support.write(os.path.join(d, "style-guide.json"), json.dumps(style_guide()))
            path = support.write(os.path.join(d, "ch.md"), CHAPTER)
            with mock.patch.object(prose_check, "DEFAULT_BASELINES", guide):
                report, _ = prose_check.run(path, tools=["rhythm"])
            self.assertEqual(report["rhythm"]["texture"]["baselines"], style_guide()["textureMetrics"])
            with mock.patch.object(prose_check, "DEFAULT_BASELINES", os.path.join(d, "missing.json")):
                report, _ = prose_check.run(path, tools=["rhythm"])
            self.assertNotEqual(report["rhythm"]["texture"]["baselines"], style_guide()["textureMetrics"])

    def test_a_failing_tool_does_not_hide_the_others(self):
        def boom(path, opts):
            raise RuntimeError("detector exploded")

        with tempfile.TemporaryDirectory() as d:
            path = support.write(os.path.join(d, "ch.md"), CHAPTER)
            with mock.patch.dict(prose_check.RUNNERS, {"slop": boom}):
                report, summaries = prose_check.run(path, tools=["rhythm", "slop"])
                self.assertEqual(report["failed"], ["slop"])
                self.assertEqual(report["slop"]["error"], "RuntimeError: detector exploded")
                self.assertIn("Traceback", report["slop"]["traceback"])
                self.assertIn("sentence", report["rhythm"])
                self.assertIn("ERROR", summaries["slop"])
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = prose_check.main(["--json", "--tools", "rhythm,slop", path])
                self.assertEqual(code, 3)
                self.assertEqual(json.loads(out.getvalue())["failed"], ["slop"])


class ParseToolsTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(prose_check.parse_tools("rhythm, slop"), ["rhythm", "slop"])
        self.assertEqual(prose_check.parse_tools("mannered"), ["mannered"])

    def test_invalid(self):
        for bad in ("bogus", "", ",", "rhythm,nope"):
            with self.assertRaises(argparse.ArgumentTypeError):
                prose_check.parse_tools(bad)


class CliTest(unittest.TestCase):
    """Subprocess runs skip the mannered checker: it would read and maybe recalibrate the real repo."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = support.write(os.path.join(self.dir.name, "ch.md"), CHAPTER)

    def tearDown(self):
        self.dir.cleanup()

    def test_json(self):
        code, out, err = support.run_cli(["tools/prose_check.py", "--json", "--tools", "rhythm,slop", self.path])
        self.assertEqual(code, 0, err)
        report = json.loads(out)
        self.assertEqual(report["tools"], ["rhythm", "slop"])
        self.assertNotIn("mannered", report)
        self.assertEqual(report["file"], self.path)

    def test_summary_is_default(self):
        code, out, err = support.run_cli(["tools/prose_check.py", "--tools", "rhythm,slop", self.path])
        self.assertEqual(code, 0, err)
        self.assertIn("== rhythm", out)
        self.assertIn("== slop", out)

    def test_errors(self):
        code, _, err = support.run_cli(["tools/prose_check.py", "--json", os.path.join(self.dir.name, "nope.md")])
        self.assertEqual(code, 1)
        self.assertIn("File not found", err)
        code, _, err = support.run_cli(["tools/prose_check.py", "--tools", "bogus", self.path])
        self.assertEqual(code, 2)
        self.assertIn("unknown tool", err)


if __name__ == "__main__":
    unittest.main()
