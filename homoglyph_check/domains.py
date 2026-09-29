"""Find domains in text, decode punycode and compare against protected names."""

import re
from dataclasses import dataclass

from .scripts import is_mixed_latin, scripts_in
from .skeleton import skeleton

_LABEL_CHAR = "[\\w\\-\u0300-\u036f\u00ad\u200b-\u200d\u2060\ufeff]"
_SEP = "[.\u3002\uff0e\uff61]"
DOMAIN_RE = re.compile("%s+(?:%s%s+)+" % (_LABEL_CHAR, _SEP, _LABEL_CHAR))
_SEP_RE = re.compile(_SEP)

MIN_DISTANCE_LEN = 8  # shorter skeletons are too easy to be 1 edit apart


@dataclass
class DomainMatch:
    protected: str
    severity: str  # "high" (same skeleton) or "medium" (1 edit apart)
    reason: str
    skeleton: str


def _decode_label(label):
    if label.startswith("xn--"):
        try:
            return label[4:].encode("ascii").decode("punycode"), True
        except (UnicodeError, ValueError):
            return label, False
    return label, False


def decode_domain(raw):
    """Lowercase, split on dot-like separators and decode xn-- labels.

    Returns (decoded_domain, labels, punycode_flags). Invisible characters
    are kept on purpose so that a padded look-alike is not taken for the real name.
    """
    labels, flags = [], []
    for part in _SEP_RE.sub(".", raw.lower()).split("."):
        text, was_puny = _decode_label(part)
        labels.append(text)
        flags.append(was_puny)
    return ".".join(labels), labels, flags


def extract_domains(text):
    """Return [(start, raw)] for every dotted host-like token in text."""
    found = []
    for m in DOMAIN_RE.finditer(text):
        raw = m.group()
        last = _SEP_RE.split(raw)[-1]
        if len(last) < 2 or not any(c.isalpha() for c in last):
            continue  # 1.2.3, e.g, 10.0.0.1 and similar
        found.append((m.start(), raw))
    return found


def mixed_script_labels(labels):
    """Decoded labels that mix Latin with Cyrillic or Greek."""
    return [lab for lab in labels if is_mixed_latin(scripts_in(lab))]


def _distance_at_most_one(a, b):
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    if len(a) == len(b):
        return a[i + 1:] == b[i + 1:]
    if len(a) > len(b):
        a, b = b, a
    return a[i:] == b[i + 1:]


def _norm_protected(p):
    return p.strip().strip(".").lower()


def match_protected(domain, protected, distance=True):
    """Compare a domain (raw or decoded) against protected names.

    Returns None when the domain IS a protected name (or a subdomain of one)
    or matches nothing; otherwise a DomainMatch. The comparison uses the
    trailing labels of the domain, so www.<lookalike> is caught too.
    """
    decoded, labels, _ = decode_domain(domain)
    prots = [_norm_protected(p) for p in protected if _norm_protected(p)]
    tails = []
    for p in prots:
        n = p.count(".") + 1
        tail = ".".join(labels[-n:])
        if tail == p:
            return None  # the real thing
        tails.append((p, tail))
    for p, tail in tails:
        sk_t, sk_p = skeleton(tail), skeleton(p)
        if sk_t == sk_p:
            return DomainMatch(p, "high", "skeleton equals the protected domain", sk_t)
    if distance:
        for p, tail in tails:
            sk_t, sk_p = skeleton(tail), skeleton(p)
            if len(sk_p) >= MIN_DISTANCE_LEN and _distance_at_most_one(sk_t, sk_p):
                return DomainMatch(p, "medium", "skeleton is 1 edit away from the protected domain", sk_t)
    return None


def is_lookalike_domain(domain, protected, distance=False):
    """True if domain imitates a protected name but is not it.

    By default only an exact skeleton match counts; pass distance=True to
    include skeletons that are one edit away.
    """
    return match_protected(domain, protected, distance=distance) is not None
