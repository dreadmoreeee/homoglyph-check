"""Invisible and bidirectional control characters."""

import unicodedata

from .scripts import script_of

# code point -> (severity, kind)
INVISIBLE = {
    0x200B: ("medium", "zero-width"),
    0x200C: ("medium", "zero-width"),
    0x200D: ("medium", "zero-width"),
    0x2060: ("medium", "zero-width"),
    0xFEFF: ("medium", "zero-width"),
    0x00AD: ("low", "soft-hyphen"),
    0x200E: ("low", "bidi-mark"),
    0x200F: ("low", "bidi-mark"),
}
for _cp in (*range(0x202A, 0x202F), *range(0x2066, 0x206A)):
    INVISIBLE[_cp] = ("high", "bidi-control")

# characters that may legitimately sit inside a word
WORD_INVISIBLES = frozenset({0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x00AD})

_LATINISH = {"LATIN", "CYRILLIC", "GREEK"}


def is_emoji(ch):
    cp = ord(ch)
    return (
        0x1F000 <= cp <= 0x1FAFF
        or 0x2600 <= cp <= 0x27BF
        or 0x2300 <= cp <= 0x23FF
        or 0x2B00 <= cp <= 0x2BFF
        or cp in (0x2764, 0x2640, 0x2642, 0x2695, 0x2696, 0x2708)
    )


def _skip_back(text, i):
    """Index of the previous significant char, skipping variation selectors."""
    i -= 1
    while i >= 0 and text[i] in "\ufe0f\ufe0e":
        i -= 1
    return i


def _legit_joiner(text, i):
    """ZWJ/ZWNJ that is normal: inside an emoji sequence or between letters
    of a script that is not Latin, Cyrillic or Greek (Arabic, Indic, ...)."""
    if ord(text[i]) not in (0x200C, 0x200D):
        return False
    p = _skip_back(text, i)
    n = i + 1
    if p < 0 or n >= len(text):
        return False
    if is_emoji(text[p]) and is_emoji(text[n]):
        return True
    sp, sn = script_of(text[p]), script_of(text[n])
    marks = unicodedata.category(text[p]).startswith("M")
    return bool((sp or marks) and sn and sn not in _LATINISH and (sp not in _LATINISH))


def find_invisible(text):
    """Yield (index, char, severity, kind) for each suspicious control char."""
    for i, ch in enumerate(text):
        info = INVISIBLE.get(ord(ch))
        if info is None:
            continue
        if ord(ch) == 0xFEFF and i == 0:
            continue  # byte order mark at the very start
        if _legit_joiner(text, i):
            continue
        yield i, ch, info[0], info[1]


def char_name(ch):
    return unicodedata.name(ch, "U+%04X" % ord(ch))
