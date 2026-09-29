"""normalize() and skeleton(), in the spirit of UTS #39.

https://www.unicode.org/reports/tr39/
"""

import unicodedata

from .confusables_data import CONFUSABLES


def _strip_format(text):
    """Drop invisible/format characters (category Cf, e.g. ZWSP, bidi, BOM) and soft hyphen."""
    return "".join(c for c in text if unicodedata.category(c) != "Cf")


def normalize(text):
    """NFKC-normalize text (folds fullwidth and math alphanumerics to plain letters)."""
    return unicodedata.normalize("NFKC", text)


def skeleton(text):
    """Return a comparison key: two strings that look alike share a skeleton.

    Steps: strip invisible characters, NFKC, NFD, map confusables to their
    Latin prototype, NFD again, lowercase. Uses a subset of the confusables
    table, so it is a best effort, not a full UTS #39 implementation.
    """
    s = unicodedata.normalize("NFD", normalize(_strip_format(text)))
    s = "".join(CONFUSABLES.get(c, c) for c in s)
    return unicodedata.normalize("NFD", s).lower()
