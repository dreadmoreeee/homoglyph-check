"""Write the ASCII-only example inputs (non-ASCII characters appear as \\uXXXX escapes).

Run:  python examples/make_examples.py
Read them back with:  homoglyph-check --unescape --file examples/lookalikes.txt
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
BS = chr(92)

CYR = {"a": 0x430, "e": 0x435, "o": 0x43E, "p": 0x440, "c": 0x441, "x": 0x445, "y": 0x443, "i": 0x456}


def esc(s):
    out = []
    for c in s:
        o = ord(c)
        out.append(c if o < 128 else BS + ("u%04x" % o if o < 0x10000 else "U%08x" % o))
    return "".join(out)


def cyr(word):
    """Swap every Latin letter that has a Cyrillic look-alike."""
    return "".join(chr(CYR[c]) if c in CYR else c for c in word)


def puny(domain):
    return domain.encode("idna").decode("ascii")


def spam_sample():
    words = ("Hello", "dear", cyr("owner") + ",", "I", "have", "a", cyr("very"), "good", cyr("offer"), "for", "your",
             cyr("business") + ".", "Click", "http://203-0-113-7.sslip.io/offer", "to", cyr("receive"), "your",
             cyr("bonus") + ".", "Fast", cyr("profit") + ",", "no", "risk!")
    zw = "no" + chr(0x200B) + " risk"
    return esc(" ".join(words)) + "\n" + esc("Reply today " + zw + ".") + "\n"


def lookalikes():
    real = ["demarkstudio.ca", "marvin.demarkstudio.ca"]
    a, o, gr = chr(0x430), chr(0x43E), chr(0x3BF)
    variants = [
        "dem" + a + "rkstudio.ca",             # Cyrillic a
        "demarkstudi" + o + ".ca",             # Cyrillic o
        "demarkstudi" + gr + ".ca",            # Greek omicron
        "marvin.dem" + a + "rkstudio.ca",      # Cyrillic a in the parent
        "demark" + chr(0x200B) + "studio.ca",  # zero-width space inserted
        "".join(chr(ord(c) + 0xFEE0) if c.isalpha() else c for c in "demarkstudio.ca"),  # fullwidth
    ]
    lines = ["Controls (the real domains):"] + ["  https://%s/" % d for d in real]
    lines.append("Look-alikes:")
    for v in variants:
        lines.append("  https://%s/" % v)
    lines.append("Punycode forms:")
    for v in variants[:4]:
        lines.append("  https://%s/" % puny(v))
    return esc("\n".join(lines)) + "\n"


def french_spanish():
    fr = "Bonjour, j'ai d\u00e9j\u00e0 termin\u00e9 l'\u00e9tude de la for\u00eat pr\u00e8s de No\u00ebl. \u00c7a va \u00eatre na\u00efvement simple."
    es = "Ma\u00f1ana el ni\u00f1o compr\u00f3 pi\u00f1a y caf\u00e9 en Espa\u00f1a. \u00bfQu\u00e9 tal el a\u00f1o?"
    return esc(fr) + "\n" + esc(es) + "\n"


for name, content in (("spam_sample.txt", spam_sample()), ("lookalikes.txt", lookalikes()),
                      ("french_spanish.txt", french_spanish())):
    with open(os.path.join(HERE, name), "w", newline="\n") as fh:
        fh.write(content)
    print("wrote", name)
