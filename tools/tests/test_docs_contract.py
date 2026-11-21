"""Every tool command the agent docs tell an agent to run must exist and accept the flags it uses."""

import glob
import os
import re
import unittest

from tools.tests import support

DOC_GLOBS = [".claude/**/*.md", ".agents/**/*.md", "resources/**/*.md"]
COMMAND_RE = re.compile(r"python3?\s+(?:-I\s+)?(tools/[A-Za-z_/]+\.py)([^`\"|)\n]*)")


def documented_commands():
    """{script: {flags}} from every `python3 tools/...py ...` in the docs."""
    found = {}
    for pattern in DOC_GLOBS:
        for doc in glob.glob(os.path.join(support.REPO_ROOT, pattern), recursive=True):
            with open(doc, encoding="utf-8") as f:
                for script, rest in COMMAND_RE.findall(f.read()):
                    flags = set(re.findall(r"(?<![\w-])--[a-z][a-z-]*", rest))
                    found.setdefault(script, set()).update(flags)
    return found


@unittest.skipUnless(os.path.isdir(os.path.join(support.REPO_ROOT, ".claude")), "agent docs not present")
class DocsContractTest(unittest.TestCase):
    def test_docs_mention_tools(self):
        self.assertTrue(documented_commands(), "no tool commands found in the docs; did the doc layout change?")

    def test_every_documented_script_exists_and_accepts_its_flags(self):
        for script, flags in sorted(documented_commands().items()):
            with self.subTest(script=script):
                self.assertTrue(os.path.exists(os.path.join(support.REPO_ROOT, script)), f"{script} is documented but missing")
                code, out, err = support.run_cli([script, "--help"])
                self.assertEqual(code, 0, err)
                for flag in flags:
                    self.assertIn(flag, out, f"docs use {script} {flag}, which its --help doesn't list")


if __name__ == "__main__":
    unittest.main()
