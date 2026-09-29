"""check_text(): run all checks over a piece of text."""

import unicodedata

from .confusables_data import CONFUSABLES
from .domains import decode_domain, extract_domains, match_protected, mixed_script_labels
from .invisible import INVISIBLE, WORD_INVISIBLES, char_name, find_invisible
from .report import Finding, Report, show
from .scripts import is_mixed_latin, script_of, scripts_in

NFKC_ADVICE = "Normalize with NFKC and compare skeletons (UTS #39)."
BIDI_ADVICE = "Reject or strip bidi controls before display or compilation (Trojan Source)."
STRIP_ADVICE = "Strip the character before comparing or storing."


def _pos(text, index):
    line = text.count("\n", 0, index) + 1
    col = index - (text.rfind("\n", 0, index) + 1) + 1
    return line, col


def _make(text, kind, severity, message, index, snippet="", cp="", name="", advice=NFKC_ADVICE):
    line, col = _pos(text, index)
    return Finding(kind, severity, message, index, line, col, show(snippet), cp, name, advice)


def _words(text):
    """Yield (start, word). Letters, marks, digits and in-word invisibles form words."""
    start = None
    for i, ch in enumerate(text + " "):
        cat = unicodedata.category(ch)
        inside = cat[0] in "LMN" or ord(ch) in WORD_INVISIBLES
        if inside and start is None:
            start = i
        elif not inside and start is not None:
            yield start, text[start:i]
            start = None


def _word_findings(text, spans):
    for start, word in _words(text):
        if any(a <= start < b for a, b in spans):
            continue  # domains are handled by the domain check
        scripts = scripts_in(word)
        if is_mixed_latin(scripts):
            odd = [c for c in word if script_of(c) in ("CYRILLIC", "GREEK")]
            hints = ", ".join("U+%04X%s" % (ord(c), " (looks like %r)" % CONFUSABLES[c] if c in CONFUSABLES else "")
                              for c in dict.fromkeys(odd))
            yield _make(text, "mixed-script", "medium",
                        "word %s mixes %s: %s" % (show(word), " and ".join(sorted(scripts & {"LATIN", "CYRILLIC", "GREEK"})), hints),
                        start, word)
        compat = [c for c in word if (unicodedata.name(c, "").startswith(("FULLWIDTH", "MATHEMATICAL"))
                                      and unicodedata.category(c).startswith(("L", "N")))]
        if compat:
            yield _make(text, "compat-alphanumerics", "low",
                        "word %s uses fullwidth or mathematical letters; NFKC gives %s"
                        % (show(word), show(unicodedata.normalize("NFKC", word))), start, word)


def _domain_findings(text, protected):
    spans = []
    findings = []
    for start, raw in extract_domains(text):
        spans.append((start, start + len(raw)))
        decoded, labels, flags = decode_domain(raw)
        for lab in mixed_script_labels(labels):
            findings.append(_make(text, "mixed-script-domain", "high",
                                  "domain %s has a label (%s) mixing Latin with Cyrillic or Greek"
                                  % (show(raw), show(lab)), start, raw))
        m = match_protected(raw, protected) if protected else None
        if m:
            note = " (decoded from punycode: %s)" % show(decoded) if any(flags) else ""
            findings.append(_make(text, "lookalike-domain", m.severity,
                                  "%s%s: %s %s" % (show(raw), note, m.reason, m.protected),
                                  start, raw,
                                  advice="Compare skeletons (NFKC + confusables); only trust %s exactly." % m.protected))
    return spans, findings


def check_text(text, protect=()):
    """Check text and return a Report whose .findings list is sorted by position.

    protect: iterable of domain names to guard, e.g. ["example.com"].
    """
    if isinstance(protect, str):
        protect = [p for p in protect.split(",") if p.strip()]
    spans, domain_findings = _domain_findings(text, list(protect))
    findings = list(_word_findings(text, spans)) + domain_findings
    for i, ch, sev, kind in find_invisible(text):
        cp = "U+%04X" % ord(ch)
        adv = BIDI_ADVICE if kind == "bidi-control" else STRIP_ADVICE
        findings.append(_make(text, kind, sev, "%s %s at offset %d" % (cp, char_name(ch), i), i, ch, cp,
                              char_name(ch), adv))
    findings.sort(key=lambda f: (f.index, f.kind))
    return Report(len(text), findings)
