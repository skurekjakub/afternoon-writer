"""tools/prose_core/text.py: offsets, line numbers and paragraph spans."""

import random
import unittest

from tools.tests import support  # noqa: F401  (sets up sys.path)
from tools.prose_core import text as core


def naive_line(text, pos):
    return text[:pos].count("\n") + 1


class LineIndexTest(unittest.TestCase):
    def test_matches_naive_count_everywhere(self):
        rng = random.Random(7)
        for _ in range(50):
            text = "".join(rng.choice("ab \n\n.") for _ in range(rng.randint(0, 300)))
            idx = core.LineIndex(text)
            for pos in range(len(text) + 1):
                self.assertEqual(idx.line(pos), naive_line(text, pos), (text, pos))
                self.assertEqual(core.line_of(text, pos), naive_line(text, pos))

    def test_edges(self):
        self.assertEqual(core.LineIndex("").line(0), 1)
        idx = core.LineIndex("a\nb\n")
        self.assertEqual([idx.line(p) for p in range(5)], [1, 1, 2, 2, 3])
        # A position on the newline itself belongs to the line it ends.
        self.assertEqual(core.LineIndex("\n\n").line(1), 2)


class TransformTest(unittest.TestCase):
    def test_narration_only_keeps_offsets(self):
        text = 'She said, "Go home." He went.\n“Fine,” he said.'
        narr = core.narration_only(text)
        self.assertEqual(len(narr), len(text))
        self.assertNotIn("Go home", narr)
        self.assertNotIn("Fine", narr)
        self.assertEqual(narr.index("He went"), text.index("He went"))
        self.assertEqual(narr.count("\n"), text.count("\n"))

    def test_quotes_do_not_span_lines(self):
        text = '"An unclosed quote\nnext line" stays'
        self.assertEqual(core.narration_only(text), text)

    def test_normalise_quotes_same_length(self):
        text = "It’s ‘fine’"
        self.assertEqual(core.normalise_quotes(text), "It's 'fine'")
        self.assertEqual(len(core.normalise_quotes(text)), len(text))

    def test_strip_headers_keeps_line_count(self):
        text = "# Title\nBody\n## Sub\nMore"
        out = core.strip_headers(text)
        self.assertEqual(out, "\nBody\n\nMore")
        self.assertEqual(out.count("\n"), text.count("\n"))

    def test_drop_headers_removes_lines(self):
        self.assertEqual(core.drop_headers("# Title\nBody\n## Sub\nMore"), "Body\nMore")

    def test_context_window_and_ellipses(self):
        text = "0123456789" * 3
        self.assertEqual(core.context(text, 10, 12, window=2), "...890123...")
        self.assertEqual(core.context(text, 0, 2, window=2), "0123...")
        self.assertEqual(core.context(text, 28, 30, window=2), "...6789")
        self.assertEqual(core.context("a\nb", 0, 3), "a b")


class ParagraphSpansTest(unittest.TestCase):
    def test_spans_point_at_their_own_text(self):
        text = "One.\n\nTwo two.\n  \n\n\nThree.\n"
        spans = list(core.paragraph_spans(text))
        self.assertEqual([b.strip() for _, _, b in spans], ["One.", "Two two.", "Three."])
        for start, end, body in spans:
            self.assertEqual(text[start:end], body)

    def test_repeated_paragraph_gets_its_own_offset(self):
        text = "No.\n\nShe said no.\n\nNo."
        starts = [s for s, _, b in core.paragraph_spans(text) if b.strip() == "No."]
        self.assertEqual(starts, [0, text.rindex("No.")])

    def test_empty(self):
        self.assertEqual(list(core.paragraph_spans("")), [])
        self.assertEqual(list(core.paragraph_spans("\n\n\n")), [])


if __name__ == "__main__":
    unittest.main()
