"""Approximate Unicode script detection from character names.

This is NOT the Unicode Script property (Scripts.txt). The first word of the
character name (LATIN, CYRILLIC, GREEK, ARABIC, ...) is used as the script.
That is right for the scripts that matter here and cheap to compute without
data files, but it is an approximation: for example, "MODIFIER LETTER" and
"MASCULINE ORDINAL INDICATOR" give odd labels. Only letters are classified;
digits, punctuation and combining marks (Common/Inherited) return None.
"""

import unicodedata

_COMPAT_PREFIXES = ("FULLWIDTH", "MATHEMATICAL")


def script_of(ch):
    """Return an upper-case script label for a letter, or None."""
    if not unicodedata.category(ch).startswith("L"):
        return None
    name = unicodedata.name(ch, "")
    if name.startswith(_COMPAT_PREFIXES):
        folded = unicodedata.normalize("NFKC", ch)[:1]
        name = unicodedata.name(folded, name)
    return name.split(" ", 1)[0] if name else None


def scripts_in(text):
    """Set of script labels of the letters in text."""
    return {s for s in map(script_of, text) if s}


def is_mixed_latin(scripts):
    """True when Latin is mixed with Cyrillic or Greek."""
    return "LATIN" in scripts and bool(scripts & {"CYRILLIC", "GREEK"})
