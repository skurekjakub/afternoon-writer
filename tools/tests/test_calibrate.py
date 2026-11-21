"""tools/mannered_checker/calibrate.py: corpora, genre stripping, fingerprints, blending and the style-guide sync.

Everything that reads or writes config, corpora, calibration.json or the style
guide runs inside support.TempRepo. All fixture prose is original.
"""

import copy
import hashlib
import json
import os
import unittest
from unittest import mock

from tools.tests import support
from tools.tests.support import TempRepo, cal, mc, write
from tools.tests.test_mannered_checker import STYLE_GUIDE


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write_json(path, data):
    return write(path, json.dumps(data, indent=2))


class GenreFurnitureTest(unittest.TestCase):
    def test_skill_only_paragraph_dropped(self):
        text = "She drew breath.\n\n[Frost Lance]\n\nThe ice cracked."
        self.assertEqual(cal.strip_genre_furniture(text), "She drew breath.\n\nThe ice cracked.")

    def test_several_skills_and_quoted_skill_paragraphs_dropped(self):
        text = "Before.\n\n[Frost Lance] [Ember Step].\n\n“[Ward of Thorns]”\n\n\"[Ward of Thorns]\"\n\nAfter."
        self.assertEqual(cal.strip_genre_furniture(text), "Before.\n\nAfter.")

    def test_inline_skill_keeps_name(self):
        text = "She cast [Frost Lance] at the door, and it held."
        self.assertEqual(cal.strip_genre_furniture(text), "She cast Frost Lance at the door, and it held.")

    def test_long_bracket_inline_kept(self):
        text = "The note said [" + "x" * 50 + "] and nothing more."
        self.assertEqual(cal.strip_genre_furniture(text), text)

    def test_system_lines_dropped(self):
        text = "The wolf fell.\nLevel Up!\nYou are now level 12.\n***\n[Strength +2]\nShe wiped the blade."
        self.assertEqual(cal.strip_genre_furniture(text), "The wolf fell.\nShe wiped the blade.")

    def test_system_lines_case_insensitive(self):
        self.assertEqual(cal.strip_genre_furniture("LEVEL UP!\n\nOn they went."), "On they went.")

    def test_paragraph_of_only_system_lines_dropped(self):
        self.assertEqual(cal.strip_genre_furniture("One.\n\nLevel Up!\n***\n\nTwo."), "One.\n\nTwo.")

    def test_ordinary_prose_untouched(self):
        self.assertEqual(cal.strip_genre_furniture(support.HUMAN_PROSE.strip()), support.HUMAN_PROSE.strip())
        text = "He counted three stars *** and slept."  # *** inside a line is prose
        self.assertEqual(cal.strip_genre_furniture(text), text)

    def test_read_corpus_strips_headers_quotes_and_furniture(self):
        with TempRepo(corpora={"samples/": {"files": {
                "a.md": "# Chapter One\n\nShe cast [Frost Lance].\n\n[Ember Step]\n",
                "b.txt": "It’s done.\n",
                "c.json": "{\"ignored\": true}"}}}) as repo:
            text = cal.read_corpus("samples")
            self.assertNotIn("Chapter One", text)
            self.assertIn("She cast Frost Lance.", text)
            self.assertNotIn("Ember Step", text)
            self.assertIn("It's done.", text)
            self.assertNotIn("ignored", text)


class CorpusSpecsTest(unittest.TestCase):
    def config(self, repo, cfg):
        write_json(repo.path(".afternoon", "config.json"), cfg)

    def test_string_and_dict_entries(self):
        with TempRepo(corpora={"samples/a.md": "A.", "samples/b.md": "B.", "samples/c.md": "C."}) as repo:
            self.config(repo, {"priming": {"humanCorpora": [
                "samples/a.md",
                {"path": "samples/b.md", "weight": 2},
                {"path": "samples/c.md", "weight": 0},     # weight 0: skipped
                "samples/missing.md",                      # missing: skipped
                {"path": None},                            # no path: skipped
                {"path": "samples/c.md", "weight": -1},    # negative: skipped
            ]}})
            self.assertEqual(cal.corpus_specs(), [("samples/a.md", 1.0), ("samples/b.md", 2.0)])
            self.assertEqual(cal.corpus_paths(), ["samples/a.md", "samples/b.md"])

    def test_default_weight_is_one(self):
        with TempRepo(corpora={"samples/a.md": "A."}) as repo:
            self.config(repo, {"priming": {"humanCorpora": [{"path": "samples/a.md"}]}})
            self.assertEqual(cal.corpus_specs(), [("samples/a.md", 1.0)])

    def test_missing_or_broken_config_falls_back_to_default(self):
        default = cal.DEFAULT_CORPORA[0]
        with TempRepo(corpora={default: "Default corpus."}) as repo:
            os.remove(repo.path(".afternoon", "config.json"))
            self.assertEqual(cal.corpus_specs(), [(default, 1.0)])
            write(repo.path(".afternoon", "config.json"), "{not json")
            self.assertEqual(cal.corpus_specs(), [(default, 1.0)])
            self.config(repo, {"priming": {"humanCorpora": []}})
            self.assertEqual(cal.corpus_specs(), [(default, 1.0)])
            self.config(repo, {})
            self.assertEqual(cal.corpus_specs(), [(default, 1.0)])

    def test_default_missing_on_disk_gives_nothing(self):
        with TempRepo(corpora={"samples/a.md": "A."}) as repo:
            os.remove(repo.path(".afternoon", "config.json"))
            self.assertEqual(cal.corpus_specs(), [])

    def test_corpus_files(self):
        with TempRepo(corpora={"samples/": {"files": {"b.md": "B", "a.txt": "A", "c.json": "{}", "d.md.bak": "x"}},
                               "single.md": "S"}) as repo:
            self.assertEqual(cal.corpus_files("samples"),
                             [repo.path("samples", "a.txt"), repo.path("samples", "b.md")])
            self.assertEqual(cal.corpus_files("single.md"), [repo.path("single.md")])


class FingerprintTest(unittest.TestCase):
    def test_changes_with_weight_size_and_mtime(self):
        with TempRepo(corpora={"samples/a.md": {"text": "Alpha text.", "weight": 1}}) as repo:
            base = cal.fingerprint()
            self.assertEqual(base[0], ["samples/a.md", 1.0])
            self.assertEqual(base[1][0], os.path.join("samples", "a.md"))
            self.assertEqual(cal.fingerprint(), base)  # stable

            repo.corpora["samples/a.md"]["weight"] = 2
            repo.write_config()
            weighted = cal.fingerprint()
            self.assertNotEqual(weighted, base)

            path = repo.path("samples", "a.md")
            st = os.stat(path)
            os.utime(path, (st.st_atime, st.st_mtime + 100))
            touched = cal.fingerprint()
            self.assertNotEqual(touched, weighted)

            mtime = os.stat(path).st_mtime
            write(path, "Alpha text, longer now.")
            os.utime(path, (mtime, mtime))  # same mtime, different size
            self.assertNotEqual(cal.fingerprint(), touched)

    def test_explicit_specs(self):
        with TempRepo(corpora={"samples/a.md": "A.", "samples/b.md": "B."}):
            fp = cal.fingerprint([("samples/b.md", 3.0)])
            self.assertEqual(fp[0], ["samples/b.md", 3.0])
            self.assertEqual(len(fp), 2)

    def test_directory_lists_every_file(self):
        with TempRepo(corpora={"samples/": {"files": {"a.md": "A", "b.md": "B"}}}):
            fp = cal.fingerprint()
            self.assertEqual([row[0] for row in fp[1:]],
                             [os.path.join("samples", "a.md"), os.path.join("samples", "b.md")])

    def test_checker_hash_covers_check_and_core(self):
        from tools.prose_core import text as core_text

        h = hashlib.sha1()
        for path in (mc.__file__, core_text.__file__):
            with open(path, "rb") as f:
                h.update(f.read())
        self.assertEqual(cal.checker_hash(), h.hexdigest()[:12])
        with open(mc.__file__, "rb") as f:
            self.assertNotEqual(cal.checker_hash(), hashlib.sha1(f.read()).hexdigest()[:12])

    def test_checker_hash_changes_when_core_changes(self):
        from tools.prose_core import text as core_text

        real_open = open
        before = cal.checker_hash()

        def fake_open(path, *args, **kwargs):
            if path == core_text.__file__:
                import io
                return io.BytesIO(b"changed")
            return real_open(path, *args, **kwargs)

        with mock.patch("builtins.open", side_effect=fake_open):
            self.assertNotEqual(cal.checker_hash(), before)


class ChunkAndBlendTest(unittest.TestCase):
    PARA = "one two three four"  # 4 words

    def test_chunks_and_tail_rule(self):
        with mock.patch.object(cal, "CHUNK_WORDS", 10):
            ten = "\n\n".join([self.PARA] * 10)  # 40 words: 3 chunks of 12, tail of 4 < 5 dropped
            chunks = cal.chapter_chunks(ten)
            self.assertEqual([len(c.split()) for c in chunks], [12, 12, 12])
            eleven = "\n\n".join([self.PARA] * 11)  # tail of 8 >= 5 kept
            self.assertEqual([len(c.split()) for c in cal.chapter_chunks(eleven)], [12, 12, 12, 8])
            short = "\n\n".join([self.PARA] * 2)  # shorter than a chunk: one chunk
            self.assertEqual(cal.chapter_chunks(short), [short])
            exact = "\n\n".join([self.PARA] * 3)  # 12 words: exactly one chunk, no tail
            self.assertEqual(len(cal.chapter_chunks(exact)), 1)

    def test_chunks_keep_paragraphs_whole(self):
        with mock.patch.object(cal, "CHUNK_WORDS", 10):
            text = "\n\n".join(f"para {i} " + "w " * 5 for i in range(6))
            for chunk in cal.chapter_chunks(text):
                for para in chunk.split("\n\n"):
                    self.assertTrue(para.startswith("para "))

    def test_mean(self):
        self.assertEqual(cal._mean([(1.0, 1.0), (4.0, 2.0)]), 3.0)
        self.assertEqual(cal._mean([(1.0, 1.0), (None, 5.0), ("x", 1.0), (3, 1.0)]), 2.0)
        self.assertIsNone(cal._mean([(None, 1.0)]))
        self.assertIsNone(cal._mean([]))
        self.assertEqual(cal._mean([(1.0, 3.0), (2.0, 0.0)]), 1.0)
        self.assertEqual(cal._mean([(1 / 3, 1.0)]), 0.333)

    def measured(self, rate, poly, value):
        return {"patternsPer10k": {"blush": rate}, "polysyndetonPer10k": poly,
                "rhythm": {k: value for k in cal.RHYTHM_KEYS}, "texture": {k: value for k in cal.TEXTURE_KEYS}}

    def test_blend_weights(self):
        a, b = self.measured(1.0, 2.0, 10.0), self.measured(4.0, 5.0, 40.0)
        b["patternsPer10k"]["maxim"] = 3.0  # missing in a: counts as 0 there
        out = cal.blend([a, b], [1.0, 2.0])
        self.assertEqual(out["patternsPer10k"]["blush"], 3.0)
        self.assertEqual(out["patternsPer10k"]["maxim"], 2.0)
        self.assertEqual(out["polysyndetonPer10k"], 4.0)
        self.assertEqual(out["rhythm"]["mattr"], 30.0)
        self.assertEqual(out["texture"]["emdash_pct"], 30.0)
        self.assertEqual(sorted(out["patternsPer10k"]), ["blush", "maxim"])

    def test_measure_shape(self):
        m = cal.measure(support.HUMAN_PROSE)
        self.assertEqual(m["words"], len(support.HUMAN_PROSE.split()))
        self.assertEqual(m["chunks"], 1)
        self.assertEqual(set(m["rhythm"]), set(cal.RHYTHM_KEYS))
        self.assertEqual(set(m["texture"]), set(cal.TEXTURE_KEYS))
        self.assertEqual(set(m["patternsPer10k"]), {p["name"] for p in mc.run_patterns("x")[0]})
        for v in list(m["rhythm"].values()) + list(m["texture"].values()):
            self.assertIsInstance(v, float)


class StyleGuideTest(unittest.TestCase):
    def test_reanchor_shifts_target_and_range(self):
        entry = {"measured": 10.0, "target": 12.0, "range": [9.0, 15.0]}
        self.assertTrue(cal._reanchor(entry, "measured", 11.5))
        self.assertEqual(entry, {"measured": 11.5, "target": 13.5, "range": [10.5, 16.5]})

    def test_reanchor_no_change(self):
        entry = {"human": 5.0, "target": 6.0, "range": [4.0, 7.0]}
        self.assertFalse(cal._reanchor(entry, "human", 5.0))
        self.assertFalse(cal._reanchor(entry, "human", None))
        self.assertFalse(cal._reanchor({"human": "n/a", "target": 1.0}, "human", 3.0))
        self.assertFalse(cal._reanchor({"target": 1.0}, "human", 3.0))
        self.assertEqual(entry, {"human": 5.0, "target": 6.0, "range": [4.0, 7.0]})

    def test_reanchor_without_target_or_range(self):
        entry = {"measured": 1.0, "range": [0.5]}
        self.assertTrue(cal._reanchor(entry, "measured", 2.0))
        self.assertEqual(entry, {"measured": 2.0, "range": [0.5]})

    def blended_from_guide(self, guide):
        rg, tm = guide["rhythmMetrics"]["global"], guide["textureMetrics"]
        return {"rhythm": {k: rg[k]["measured"] for k in cal.RHYTHM_KEYS},
                "texture": {k: tm[k]["human"] for k in cal.TEXTURE_KEYS}}

    def test_drifted(self):
        with TempRepo(style_guide=copy.deepcopy(STYLE_GUIDE)) as repo:
            blended = self.blended_from_guide(STYLE_GUIDE)
            self.assertFalse(cal.style_guide_drifted(blended))
            moved = copy.deepcopy(blended)
            moved["texture"]["emdash_pct"] += 0.5
            self.assertTrue(cal.style_guide_drifted(moved))
            moved = copy.deepcopy(blended)
            moved["rhythm"]["mattr"] = None  # missing blend values don't count as drift
            self.assertFalse(cal.style_guide_drifted(moved))
            write(repo.path(".afternoon", "style-guide.json"), "{broken")
            self.assertFalse(cal.style_guide_drifted(blended))
            os.remove(repo.path(".afternoon", "style-guide.json"))
            self.assertFalse(cal.style_guide_drifted(blended))

    def test_sync_then_not_drifted(self):
        with TempRepo(style_guide=copy.deepcopy(STYLE_GUIDE)) as repo:
            blended = self.blended_from_guide(STYLE_GUIDE)
            blended["rhythm"]["mattr"] = 0.9
            blended["texture"]["emdash_pct"] = 5.5
            per_corpus = [{"rhythm": {"mattr": 0.9}, "texture": {"emdash_pct": 5.5}}]
            changed = cal.sync_style_guide(blended, ["samples/a.md"], per_corpus, [2.0])
            self.assertEqual(changed, ["rhythmMetrics.global.mattr", "textureMetrics.emdash_pct"])
            self.assertFalse(cal.style_guide_drifted(blended))
            guide = json.loads(read(repo.path(".afternoon", "style-guide.json")))
            self.assertEqual(guide["rhythmMetrics"]["global"]["mattr"],
                             {"measured": 0.9, "target": 0.91, "range": [0.88, 0.95]})
            self.assertEqual(guide["textureMetrics"]["emdash_pct"],
                             {"human": 5.5, "target": 6.0, "range": [4.5, 7.5]})
            self.assertEqual(guide["textureMetrics"]["texture_score"], STYLE_GUIDE["textureMetrics"]["texture_score"])
            self.assertIn("samples/a.md (weight 2)", guide["textureMetrics"]["source"])
            self.assertEqual(guide["textureMetrics"]["perCorpus"], {"samples/a.md": {"emdash_pct": 5.5}})
            self.assertEqual(guide["rhythmMetrics"]["perCorpus"], {"samples/a.md": {"mattr": 0.9}})
            # A second sync with the same blend changes no anchors.
            self.assertEqual(cal.sync_style_guide(blended, ["samples/a.md"], per_corpus, [2.0]), [])

    def test_sync_without_style_guide(self):
        with TempRepo() as repo:
            self.assertEqual(cal.sync_style_guide({"rhythm": {}, "texture": {}}, [], []), [])
            self.assertFalse(os.path.exists(repo.path(".afternoon", "style-guide.json")))


class CalibrateTest(unittest.TestCase):
    def repo(self):
        return TempRepo(corpora={"samples/human.md": {"text": support.HUMAN_PROSE, "weight": 1},
                                 "samples/more/": {"files": {"one.md": support.HUMAN_PROSE.replace("Marten", "Ilse")}}},
                        style_guide=copy.deepcopy(STYLE_GUIDE))

    def test_writes_calibration_in_temp_repo(self):
        with self.repo() as repo:
            repo.corpora["samples/more/"]["weight"] = 2
            repo.write_config()
            data = cal.calibrate(update_style_guide=True, quiet=True)
            on_disk = json.loads(read(repo.path("calibration.json")))
            self.assertEqual(on_disk, data)
            self.assertEqual(set(data), {"_doc", "generatedAt", "headroom", "zeroRelease", "fingerprint",
                                         "checkerHash", "corpora", "blend"})
            self.assertEqual(data["headroom"], mc.HEADROOM)
            self.assertEqual(data["zeroRelease"], mc.ZERO_RELEASE)
            self.assertEqual(data["checkerHash"], cal.checker_hash())
            self.assertEqual(data["fingerprint"], cal.fingerprint())
            self.assertEqual([(c["path"], c["weight"]) for c in data["corpora"]],
                             [("samples/human.md", 1.0), ("samples/more", 2.0)])
            for c in data["corpora"]:
                self.assertEqual(set(c), {"path", "weight", "words", "chunks", "patternsPer10k",
                                          "polysyndetonPer10k", "rhythm", "texture"})
            self.assertEqual(set(data["blend"]), {"patternsPer10k", "polysyndetonPer10k", "rhythm", "texture"})
            a, b = data["corpora"]
            self.assertAlmostEqual(data["blend"]["rhythm"]["mattr"],
                                   round((a["rhythm"]["mattr"] + 2 * b["rhythm"]["mattr"]) / 3, 3), places=3)
            self.assertFalse(cal.style_guide_drifted(data["blend"]))

    def test_rerun_is_idempotent_for_style_guide(self):
        with self.repo() as repo:
            cal.calibrate(quiet=True)
            first = json.loads(read(repo.path(".afternoon", "style-guide.json")))
            data = cal.calibrate(quiet=True)
            second = json.loads(read(repo.path(".afternoon", "style-guide.json")))
            self.assertEqual(first, second)
            self.assertFalse(cal.style_guide_drifted(data["blend"]))

    def test_no_style_guide_update(self):
        with self.repo() as repo:
            cal.calibrate(update_style_guide=False, quiet=True)
            self.assertEqual(json.loads(read(repo.path(".afternoon", "style-guide.json"))), STYLE_GUIDE)
            self.assertTrue(os.path.exists(repo.path("calibration.json")))

    def test_no_corpora_exits(self):
        with TempRepo(corpora={}) as repo:
            with self.assertRaises(SystemExit):
                cal.calibrate(quiet=True)
            self.assertFalse(os.path.exists(repo.path("calibration.json")))

    def test_furniture_not_measured(self):
        furniture = "\n\n".join(["[Frost Lance]", "Level Up!", "***"] * 40)
        with TempRepo(corpora={"samples/plain.md": support.HUMAN_PROSE,
                               "samples/litrpg.md": support.HUMAN_PROSE + "\n\n" + furniture}):
            data = cal.calibrate(update_style_guide=False, quiet=True)
            plain, litrpg = data["corpora"]
            self.assertEqual(plain["words"], litrpg["words"])
            self.assertEqual(plain["rhythm"], litrpg["rhythm"])

    def test_verbose_output(self):
        with self.repo():
            with mock.patch("builtins.print") as printed:
                cal.calibrate(quiet=False)
            lines = " ".join(str(c.args[0]) for c in printed.call_args_list)
            self.assertIn("calibrated from 2 corpora", lines)
            self.assertIn("style-guide.json", lines)


class CliTest(unittest.TestCase):
    def test_help(self):
        code, out, _ = support.run_cli(["tools/mannered_checker/calibrate.py", "--help"])
        self.assertEqual(code, 0)
        self.assertIn("--no-style-guide", out)


if __name__ == "__main__":
    unittest.main()


class AtomicWriteTest(unittest.TestCase):
    def test_write_replaces_whole_file_and_leaves_no_temp(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.json")
            cal._write_json_atomic(path, {"a": 1})
            cal._write_json_atomic(path, {"b": [1, 2]})
            with open(path, encoding="utf-8") as f:
                self.assertEqual(json.load(f), {"b": [1, 2]})
            self.assertEqual(os.listdir(d), ["out.json"])

    def test_failed_write_keeps_the_old_file(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.json")
            cal._write_json_atomic(path, {"a": 1})
            with self.assertRaises(TypeError):
                cal._write_json_atomic(path, {"bad": object()})
            with open(path, encoding="utf-8") as f:
                self.assertEqual(json.load(f), {"a": 1})
            self.assertEqual(os.listdir(d), ["out.json"])
