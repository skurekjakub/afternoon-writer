"""Shared fixtures for the tool tests.

Nothing here writes outside a temporary directory. TempRepo points the mannered
checker and the calibrator at a throwaway repo layout, so tests never touch the
real calibration.json, gram cache or .afternoon/style-guide.json (a live pipeline
may be reading them). The guard in tools/tests/__init__.py fails the run if they
change anyway.

All fixture prose is original, written for these tests.
"""

import contextlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tools.mannered_checker import calibrate as cal  # noqa: E402
from tools.mannered_checker import check as mc  # noqa: E402

# Files a live pipeline reads; tests must leave them alone.
PROTECTED = [
    os.path.join(REPO_ROOT, "tools", "mannered_checker", "calibration.json"),
    os.path.join(REPO_ROOT, "tools", "mannered_checker", "cache"),
    os.path.join(REPO_ROOT, ".afternoon", "style-guide.json"),
    os.path.join(REPO_ROOT, ".afternoon", "config.json"),
]


def protected_state():
    """(path, mtime_ns, size) for every protected file, recursing into directories."""
    state = []
    for p in PROTECTED:
        paths = [p]
        if os.path.isdir(p):
            paths = sorted(os.path.join(p, f) for f in os.listdir(p))
        for q in paths:
            if os.path.exists(q):
                st = os.stat(q)
                state.append((q, st.st_mtime_ns, st.st_size))
    return state


PROTECTED_AT_IMPORT = protected_state()

# A plain, ordinary-English passage for human-corpus fixtures (original text).
HUMAN_PROSE = """\
The rain had stopped by the time the carts reached the bridge. Marten walked beside the lead horse with one hand on the bridle, and the boy followed with the lantern.

At the far end of the bridge the road split. The left fork ran down to the mill, the right climbed toward the farms on the ridge. Marten stopped and looked at both.

"Which way?" the boy asked.

"The ridge," Marten said. "The mill floods in spring."

They took the right fork. The horses leaned into the slope, and the wheels found the old ruts and stayed in them. Halfway up, a dog came out of a gate and barked at them until a woman called it back.

By noon they had reached the first farm. Nobody came out. The yard was swept, the door was shut, and smoke came from the chimney in a thin grey line.
"""

FAMILY = {
    "name": "test_family",
    "description": "A recurring test beat.",
    "regex": r"\bthe kettle sang\b",
    "perChapter": 1,
    "window": 3,
    "perWindow": 1,
}


class ProtectedFilesUntouched(unittest.TestCase):
    """Appended last by tools/tests/__init__.py: fails if any test changed a protected file."""

    def test_protected_files_unchanged(self):
        self.assertEqual(protected_state(), PROTECTED_AT_IMPORT,
                         "a test wrote to calibration.json, the gram cache, config.json or style-guide.json "
                         "(or the pipeline recalibrated while the tests ran; rerun to tell)")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


class TempRepo:
    """A throwaway repo with the mannered checker and calibrator pointed at it.

        with TempRepo(corpora={"samples/a.md": HUMAN_PROSE}) as repo:
            path = repo.chapter(3, "v2.md", text)
            report = mc.check(path)

    corpora: {relpath: text} or {relpath: {"text": ..., "weight": ...}} (a relpath ending
        in "/" with {"files": {name: text}} makes a directory corpus).
    chapters: {n: final.md text} written as .afternoon/chapters/chapter{n}/final.md.
    voice_sheets: {filename: text} under stories/test/voice-sheets/.
    families: refrain families list (default: one test family).
    style_guide: dict written to .afternoon/style-guide.json (default: none).
    """

    def __init__(self, corpora=None, chapters=None, voice_sheets=None, families=None, style_guide=None):
        self.corpora = corpora if corpora is not None else {"samples/human.md": HUMAN_PROSE}
        self.chapters = chapters or {}
        self.voice_sheets = voice_sheets or {}
        self.families = [FAMILY] if families is None else families
        self.style_guide = style_guide
        self._stack = contextlib.ExitStack()

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    def chapter(self, n, name, text):
        return write(self.path(".afternoon", "chapters", f"chapter{n}", name), text)

    def write_config(self, extra=None):
        entries = []
        for rel, spec in self.corpora.items():
            weight = spec.get("weight", 1) if isinstance(spec, dict) else 1
            entries.append({"path": rel.rstrip("/"), "weight": weight})
        cfg = {"priming": {"humanCorpora": entries}}
        if self.voice_sheets:
            cfg["characters"] = {"voiceSheets": "stories/test/voice-sheets"}
        cfg.update(extra or {})
        write(self.path(".afternoon", "config.json"), json.dumps(cfg, indent=2))

    def __enter__(self):
        self.root = tempfile.mkdtemp(prefix="prose-tools-test-")
        self._stack.callback(shutil.rmtree, self.root, ignore_errors=True)
        for rel, spec in self.corpora.items():
            if isinstance(spec, dict) and "files" in spec:
                for name, text in spec["files"].items():
                    write(self.path(rel, name), text)
            else:
                write(self.path(rel), spec["text"] if isinstance(spec, dict) else spec)
        for n, text in self.chapters.items():
            self.chapter(n, "final.md", text)
        for name, text in self.voice_sheets.items():
            write(self.path("stories", "test", "voice-sheets", name), text)
        write(self.path("families.json"), json.dumps({"families": self.families}))
        if self.style_guide is not None:
            write(self.path(".afternoon", "style-guide.json"), json.dumps(self.style_guide, indent=2))
        self.write_config()
        patches = {
            (mc, "REPO_ROOT"): self.root,
            (mc, "CONFIG_PATH"): self.path(".afternoon", "config.json"),
            (mc, "CALIBRATION_PATH"): self.path("calibration.json"),
            (mc, "CACHE_DIR"): self.path("cache"),
            (mc, "FAMILIES_PATH"): self.path("families.json"),
            (cal, "REPO_ROOT"): self.root,
            (cal, "CONFIG_PATH"): self.path(".afternoon", "config.json"),
            (cal, "CALIBRATION_PATH"): self.path("calibration.json"),
            (cal, "STYLE_GUIDE_PATH"): self.path(".afternoon", "style-guide.json"),
        }
        for (module, attr), value in patches.items():
            self._stack.enter_context(mock.patch.object(module, attr, value))
        return self

    def __exit__(self, *exc):
        self._stack.close()
        return False


def run_cli(args, cwd=REPO_ROOT, timeout=120):
    """Run a tool CLI in a subprocess: (returncode, stdout, stderr)."""
    r = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr
