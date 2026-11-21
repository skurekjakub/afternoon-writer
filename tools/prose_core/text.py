"""Text helpers shared by the prose tools (slop checker, rhythm scorer, mannered checker).

Every transform here keeps character offsets stable unless its name says
otherwise, so positions found on transformed text still point at the right
line of the original file.
"""

import bisect
import re

QUOTE_RE = re.compile(r'"[^"\n]*"|“[^”\n]*”')
PARAGRAPH_BREAK_RE = re.compile(r"\n\s*\n")
_NEWLINE_RE = re.compile(r"\n")


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalise_quotes(text: str) -> str:
    """Curly apostrophes to straight ones. Same length, so offsets are kept."""
    return text.replace("’", "'").replace("‘", "'")


def strip_headers(text: str) -> str:
    """Blank out markdown header lines, keeping the line count."""
    return "\n".join("" if line.startswith("#") else line for line in text.split("\n"))


def drop_headers(text: str) -> str:
    """Remove markdown header lines entirely. Changes offsets; use only where line numbers don't matter."""
    return "\n".join(line for line in text.split("\n") if not line.startswith("#"))


def narration_only(text: str) -> str:
    """Blank out quoted speech, keeping offsets and line numbers stable."""
    return QUOTE_RE.sub(lambda m: " " * len(m.group(0)), text)


class LineIndex:
    """1-based line numbers for character offsets in O(log n) per lookup."""

    __slots__ = ("_newlines",)

    def __init__(self, text: str):
        self._newlines = [m.start() for m in _NEWLINE_RE.finditer(text)]

    def line(self, pos: int) -> int:
        return bisect.bisect_left(self._newlines, pos) + 1


def line_of(text: str, pos: int) -> int:
    """One-off line lookup. Build a LineIndex instead when looking up many positions."""
    return text.count("\n", 0, pos) + 1


def context(text: str, start: int, end: int, window: int = 60) -> str:
    """The match plus `window` characters either side, on one line, with ... where it was cut."""
    a, b = max(0, start - window), min(len(text), end + window)
    snippet = text[a:b].replace("\n", " ")
    return ("..." if a else "") + snippet + ("..." if b < len(text) else "")


def paragraph_spans(text: str):
    """Yield (start, end, body) for each non-empty paragraph. body is text[start:end], unstripped."""
    pos = 0
    for block in re.split(r"(\n\s*\n)", text):
        if block.strip() and not PARAGRAPH_BREAK_RE.fullmatch(block):
            yield pos, pos + len(block), block
        pos += len(block)
