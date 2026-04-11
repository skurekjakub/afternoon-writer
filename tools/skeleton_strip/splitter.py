"""Prose-aware sentence and paragraph splitter.

Handles abbreviations, dialogue-internal punctuation, ellipses, and em-dashes
without breaking on false sentence boundaries. Designed for fiction prose.
"""

import re
from dataclasses import dataclass, field


@dataclass
class Sentence:
    text: str
    index: int
    paragraph_index: int
    start_char: int
    end_char: int
    is_dialogue: bool


@dataclass
class Paragraph:
    text: str
    index: int
    sentences: list[Sentence] = field(default_factory=list)
    start_char: int = 0
    end_char: int = 0


# Abbreviations that shouldn't trigger sentence splits
_ABBREVS = {
    "mr", "mrs", "ms", "dr", "jr", "sr", "st", "ave", "blvd",
    "gen", "col", "lt", "sgt", "cpl", "pvt", "capt", "cmdr",
    "prof", "rev", "hon", "vol", "dept", "est", "approx",
    "vs", "etc", "inc", "ltd", "corp", "co",
}

# Sentence-ending punctuation followed by space+uppercase or end of string
_SENT_SPLIT = re.compile(
    r'(?<=[.!?])'           # lookbehind: sentence-ending punct
    r'(?:\s*["\u201D])?'    # optional closing quote after punct
    r'\s+'                   # required whitespace
    r'(?=[A-Z\u201C"])'     # lookahead: uppercase or opening quote
)


def _is_abbreviation(text: str, pos: int) -> bool:
    """Check if the period at `pos` belongs to an abbreviation."""
    if pos <= 0 or text[pos] != '.':
        return False
    # Walk backwards to find the word
    start = pos - 1
    while start >= 0 and text[start].isalpha():
        start -= 1
    word = text[start + 1:pos].lower()
    return word in _ABBREVS


def _is_inside_quotes(text: str, pos: int) -> bool:
    """Rough check: is position inside an open quote pair?"""
    # Count quote chars before this position
    before = text[:pos]
    # Smart quotes
    opens = before.count('\u201C') + before.count('\u2018')
    closes = before.count('\u201D') + before.count('\u2019')
    if opens > closes:
        return True
    # Straight double quotes (odd count = inside)
    if before.count('"') % 2 == 1:
        return True
    return False


def _is_ellipsis(text: str, pos: int) -> bool:
    """Check if the period at `pos` is part of an ellipsis."""
    if pos + 2 < len(text) and text[pos:pos+3] == '...':
        return True
    if pos >= 2 and text[pos-2:pos+1] == '...':
        return True
    if pos >= 1 and text[pos-1:pos+2] == '...':
        return True
    # Unicode ellipsis
    if text[pos] == '\u2026':
        return True
    return False


def split_sentences(text: str, paragraph_index: int = 0, char_offset: int = 0) -> list[Sentence]:
    """Split text into sentences with position tracking."""
    if not text.strip():
        return []

    # Pre-pass: protect abbreviations and ellipses by replacing their periods
    protected = list(text)
    for i, ch in enumerate(text):
        if ch == '.':
            if _is_abbreviation(text, i):
                protected[i] = '\x00'  # placeholder
            elif _is_ellipsis(text, i):
                protected[i] = '\x01'
    protected_text = ''.join(protected)

    # Split on sentence boundaries
    raw_parts = _SENT_SPLIT.split(protected_text)

    # Restore protected characters and build sentences
    sentences: list[Sentence] = []
    offset = 0
    sent_idx = 0

    for part in raw_parts:
        # Restore placeholders
        restored = part.replace('\x00', '.').replace('\x01', '.')
        stripped = restored.strip()
        if not stripped:
            offset += len(part)
            continue

        # Find actual position in original text
        start = text.find(stripped[:20], max(0, offset - 5))
        if start == -1:
            start = offset
        end = start + len(stripped)

        has_quotes = (
            '"' in stripped or '\u201C' in stripped or
            '\u201D' in stripped or '\u2018' in stripped or '\u2019' in stripped
        )

        sentences.append(Sentence(
            text=stripped,
            index=sent_idx,
            paragraph_index=paragraph_index,
            start_char=char_offset + start,
            end_char=char_offset + end,
            is_dialogue=has_quotes,
        ))
        sent_idx += 1
        offset = end

    return sentences


_SENT_END_RE = re.compile(r'[.!?]["\u201D\u2019]*\s*$')


def _unwrap_hard_wrapped(text: str) -> str:
    """Join hard-wrapped lines into paragraphs separated by blank lines.

    Detects hard-wrapped prose (zero blank lines, many lines starting
    lowercase) and joins continuation lines with spaces. A paragraph
    break is inserted when the previous line ends with sentence-ending
    punctuation and the next line starts with an uppercase letter or
    opening quote.
    """
    lines = text.split('\n')
    if not lines:
        return text

    result_paragraphs: list[str] = []
    current: list[str] = []

    for i, raw_line in enumerate(lines):
        line = raw_line.rstrip()
        if not line:
            # Blank line — flush current paragraph
            if current:
                result_paragraphs.append(' '.join(current))
                current = []
            continue

        # Skip headings
        stripped = line.lstrip()
        if stripped.startswith('#'):
            if current:
                result_paragraphs.append(' '.join(current))
                current = []
            result_paragraphs.append(stripped)
            continue

        if not current:
            current.append(line)
            continue

        # Decide: paragraph break or continuation?
        prev = current[-1]
        prev_ends_sentence = bool(_SENT_END_RE.search(prev))
        next_starts_upper = bool(
            stripped and (stripped[0].isupper() or stripped[0] in '"\u201C\u2018')
        )

        if prev_ends_sentence and next_starts_upper:
            # Paragraph break
            result_paragraphs.append(' '.join(current))
            current = [line]
        else:
            # Continuation — join with space
            current.append(line)

    if current:
        result_paragraphs.append(' '.join(current))

    return '\n\n'.join(result_paragraphs)


def split_paragraphs(text: str) -> list[Paragraph]:
    """Split text into paragraphs, handling both blank-line-separated and hard-wrapped formats."""
    # Strip markdown frontmatter if present
    content = text
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end + 3:].lstrip('\n')

    # Detect hard-wrapped prose: no blank lines but many lines starting lowercase
    blank_count = sum(1 for l in content.split('\n') if not l.strip())
    line_count = content.count('\n')
    if blank_count < line_count * 0.05 and line_count > 50:
        content = _unwrap_hard_wrapped(content)

    # Split on one or more blank lines
    raw_parts = re.split(r'\n\s*\n', content)

    paragraphs: list[Paragraph] = []
    offset = 0
    para_idx = 0

    for part in raw_parts:
        stripped = part.strip()
        if not stripped:
            offset += len(part) + 2  # account for the split delimiter
            continue

        # Skip markdown headings
        if stripped.startswith('#'):
            offset += len(part) + 2
            continue

        start = content.find(stripped[:30], max(0, offset - 5))
        if start == -1:
            start = offset
        end = start + len(stripped)

        sents = split_sentences(stripped, paragraph_index=para_idx, char_offset=start)

        paragraphs.append(Paragraph(
            text=stripped,
            index=para_idx,
            sentences=sents,
            start_char=start,
            end_char=end,
        ))
        para_idx += 1
        offset = end

    return paragraphs
