# homoglyph-check

Find look-alike letters, invisible characters and look-alike domains in text, offline. Python, standard library only, a command line tool and a small API.

```python
from homoglyph_check import check_text, skeleton, is_lookalike_domain

report = check_text("visit https://dem\u0430rkstudio.ca/ now", protect=["demarkstudio.ca"])
[(f.severity, f.kind) for f in report.findings]
# [('high', 'lookalike-domain'), ('high', 'mixed-script-domain')]

skeleton("dem\u0430rkstudio.ca") == skeleton("demarkstudio.ca")    # True
is_lookalike_domain("xn--demrkstudio-0ij.ca", ["demarkstudio.ca"])  # True
```

(`\u0430` is Cyrillic "a", which looks exactly like the Latin one.)

## What it detects

- **Mixed-script words.** A word that mixes Latin with Cyrillic or Greek (`p` + Cyrillic `a` + `y`). Accented Latin (French, Spanish), digits, punctuation and combining marks are not counted, so normal French and Spanish text is not flagged.
- **Confusables.** Cyrillic and Greek letters that look like Latin ones, from a bundled subset of the Unicode confusables table. Fullwidth and mathematical letters are folded with NFKC.
- **Invisible and bidi characters.** U+200B to U+200D, U+2060, U+FEFF (mid-text), U+00AD, U+200E/U+200F, U+202A to U+202E and U+2066 to U+2069, with position, code point and name. A ZWJ inside an emoji sequence, and a ZWNJ/ZWJ between Arabic or Indic letters, is normal and not flagged. Bidi controls are the "Trojan Source" trick.
- **Look-alike domains.** Domains and URLs in the text are extracted, `xn--` labels are decoded, and each one is compared with a protected list. A domain whose skeleton equals a protected one, but which is not that domain, is **high**. A skeleton one edit away is **medium**. The real domain and its subdomains are never flagged.

Severities: `high` (bidi controls, look-alike domain, mixed-script domain label), `medium` (mixed-script word, zero-width characters, 1-edit domain), `low` (soft hyphen, LRM/RLM, fullwidth/math letters).

## Install and use

```
pip install .            # or run from a checkout: python -m homoglyph_check
```

```
python -m homoglyph_check "some text"                     # text as arguments
python -m homoglyph_check --file message.txt              # a file ('-' = stdin)
cat message.txt | python -m homoglyph_check
python -m homoglyph_check --file msg.txt --protect demarkstudio.ca,marvin.demarkstudio.ca
python -m homoglyph_check --file msg.txt --json           # or --markdown
python -m homoglyph_check --file msg.txt --fail-on medium # low | medium | high (default) | never
python -m homoglyph_check --unescape --file examples/lookalikes.txt   # decode \uXXXX in the input
```

Output shows non-ASCII characters as `\uXXXX` escapes, so you can see what is really there. Exit codes: **0** clean (or below `--fail-on`), **1** a finding at or above `--fail-on`, **2** usage or input error. A CI example is in [examples/ci-example.yml](examples/ci-example.yml).

### Python

```python
from homoglyph_check import (
    check_text, normalize, skeleton, is_lookalike_domain, match_protected,
    decode_domain, extract_domains, find_invisible, script_of, scripts_in,
)
```

`check_text(text, protect=())` returns a `Report` with `.findings` (each has `kind`, `severity`, `message`, `index`, `line`, `column`, `codepoint`, `name`, `advice`), `.max_severity()`, `.to_dict()`, `.to_json()`, `.to_markdown()`, `.to_text()`. `normalize(text)` is NFKC. `is_lookalike_domain(domain, protected, distance=False)` is a boolean; `match_protected` tells you which name matched and why.

## How the skeleton works

`skeleton(text)` gives a key that is equal for strings that look alike, following the idea in [UTS #39, Unicode Security Mechanisms](https://www.unicode.org/reports/tr39/):

1. strip invisible (format) characters;
2. NFKC (folds fullwidth and math letters; UTS #39 itself starts at NFD);
3. NFD, then map each character through the confusables table to its Latin prototype;
4. NFD again and lowercase.

Names are compared by skeleton, not by eye. Every finding suggests the same fix: normalize with NFKC and compare skeletons. A domain is compared on its last N labels (N = labels in the protected name), so `www.<look-alike>` is caught too.

## Limitations

- **The confusables table is a subset.** About 55 hand-picked entries (Cyrillic, Greek, and 0/1/dotless i), not the full Unicode `confusables.txt`. Anything outside it is missed. The Unicode License v3 notice is in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) and in the data file.
- **Scripts are approximated.** The script comes from the first word of the character name (LATIN, CYRILLIC, ...), not from the Unicode Script property. Good enough for Latin/Cyrillic/Greek; odd for exotic characters.
- **A word made only of look-alikes is not "mixed".** A fully Cyrillic `\u0440\u0430\u0443\u0440\u0430\u04cf` looks like "paypal" but is one script. Only the protected-domain comparison catches that case, and only for names you list.
- **Legitimate mixing exists.** Greek text with a Latin unit, or Cyrillic text with a Latin brand name, is reported (medium).
- **Text only.** It does not fetch, resolve or crawl anything, and it does not know about registry IDN policies.
- **Not a spam filter by itself.** It reports suspicious characters; deciding what to do with a message is up to you.

## Pairs with form-spam-guard

form-spam-guard is my spam filter for website contact forms. This tool adds the look-alike and invisible-character checks: run a submitted message through `check_text` and treat `medium` or `high` findings as one more signal.

## Measured result

Real, unedited output of the finished CLI. Inputs are generated by [examples/make_examples.py](examples/make_examples.py) as ASCII files with `\uXXXX` escapes and read back with `--unescape`.

**(a) Spam-style message.** This is a *representative sample I wrote*, not the original fixture from form-spam-guard: Latin-alphabet words with Cyrillic look-alike letters, a zero-width space and a documentation-range sslip.io link. It has only medium findings, so the exit code is 0 with the default `--fail-on high`. A link to an arbitrary domain is not a look-alike unless you protect the name it imitates.

```
$ python -m homoglyph_check --unescape --file examples/spam_sample.txt
homoglyph-check: 8 finding(s) (high 0, medium 8, low 0)
[MEDIUM] mixed-script  line 1, col 12
    word \u043ewn\u0435r mixes CYRILLIC and LATIN: U+043E (looks like 'o'), U+0435 (looks like 'e')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 28
    word v\u0435r\u0443 mixes CYRILLIC and LATIN: U+0435 (looks like 'e'), U+0443 (looks like 'y')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 38
    word \u043eff\u0435r mixes CYRILLIC and LATIN: U+043E (looks like 'o'), U+0435 (looks like 'e')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 53
    word bus\u0456n\u0435ss mixes CYRILLIC and LATIN: U+0456 (looks like 'i'), U+0435 (looks like 'e')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 106
    word r\u0435\u0441\u0435\u0456v\u0435 mixes CYRILLIC and LATIN: U+0435 (looks like 'e'), U+0441 (looks like 'c'), U+0456 (looks like 'i')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 119
    word b\u043enus mixes CYRILLIC and LATIN: U+043E (looks like 'o')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] mixed-script  line 1, col 131
    word \u0440r\u043ef\u0456t mixes CYRILLIC and LATIN: U+0440 (looks like 'p'), U+043E (looks like 'o'), U+0456 (looks like 'i')
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[MEDIUM] zero-width  line 2, col 15
    U+200B ZERO WIDTH SPACE at offset 161
    fix: Strip the character before comparing or storing.
Escapes like \u0430 show the real code points. Guidance: NFKC + skeleton, https://www.unicode.org/reports/tr39/
(exit code 0)
```

**(b) Look-alikes of demarkstudio.ca and marvin.demarkstudio.ca** (Cyrillic a, Cyrillic o, Greek omicron, a Cyrillic a in the parent, a zero-width space, fullwidth, and three punycode forms), with the two real domains on lines 2 and 3 as controls (not flagged). Also saved as [examples/sample_report.json](examples/sample_report.json) and [examples/sample_report.md](examples/sample_report.md).

```
$ python -m homoglyph_check --unescape --file examples/lookalikes.txt --protect demarkstudio.ca,marvin.demarkstudio.ca
homoglyph-check: 19 finding(s) (high 18, medium 1, low 0)
[HIGH] lookalike-domain  line 5, col 11
    dem\u0430rkstudio.ca: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 5, col 11
    domain dem\u0430rkstudio.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 6, col 11
    demarkstudi\u043e.ca: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 6, col 11
    domain demarkstudi\u043e.ca has a label (demarkstudi\u043e) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 7, col 11
    demarkstudi\u03bf.ca: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 7, col 11
    domain demarkstudi\u03bf.ca has a label (demarkstudi\u03bf) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 8, col 11
    marvin.dem\u0430rkstudio.ca: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 8, col 11
    domain marvin.dem\u0430rkstudio.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 9, col 11
    demark\u200bstudio.ca: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[MEDIUM] zero-width  line 9, col 17
    U+200B ZERO WIDTH SPACE at offset 234
    fix: Strip the character before comparing or storing.
[HIGH] lookalike-domain  line 10, col 11
    \uff44\uff45\uff4d\uff41\uff52\uff4b\uff53\uff54\uff55\uff44\uff49\uff4f.\uff43\uff41: skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] lookalike-domain  line 12, col 11
    xn--demrkstudio-0ij.ca (decoded from punycode: dem\u0430rkstudio.ca): skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 12, col 11
    domain xn--demrkstudio-0ij.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 13, col 11
    xn--demarkstudi-1nj.ca (decoded from punycode: demarkstudi\u043e.ca): skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 13, col 11
    domain xn--demarkstudi-1nj.ca has a label (demarkstudi\u043e) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 14, col 11
    xn--demarkstudi-ifi.ca (decoded from punycode: demarkstudi\u03bf.ca): skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 14, col 11
    domain xn--demarkstudi-ifi.ca has a label (demarkstudi\u03bf) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
[HIGH] lookalike-domain  line 15, col 11
    marvin.xn--demrkstudio-0ij.ca (decoded from punycode: marvin.dem\u0430rkstudio.ca): skeleton equals the protected domain demarkstudio.ca
    fix: Compare skeletons (NFKC + confusables); only trust demarkstudio.ca exactly.
[HIGH] mixed-script-domain  line 15, col 11
    domain marvin.xn--demrkstudio-0ij.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek
    fix: Normalize with NFKC and compare skeletons (UTS #39).
Escapes like \u0430 show the real code points. Guidance: NFKC + skeleton, https://www.unicode.org/reports/tr39/
(exit code 1)
```

**(c) False-positive check** on a short French and a short Spanish text with accents:

```
$ python -m homoglyph_check --unescape --file examples/french_spanish.txt
homoglyph-check: nothing suspicious found (152 characters checked)
(exit code 0)
```

Test suite:

```
$ python -m pytest -q -p no:cacheprovider --import-mode=importlib homoglyph-check
56 passed in 0.11s
```

## Tests

```
python -m pytest -q -p no:cacheprovider --import-mode=importlib homoglyph-check
```

Needs `pytest`; no network. Coverage: mixed-script detection, no false positives on French/Spanish or emoji ZWJ sequences, every invisible/bidi character, a Trojan Source RLO string, punycode round trips of Cyrillic and Greek look-alikes of demarkstudio.ca against a protected list (real domain not flagged), NFKC fullwidth and math cases, JSON and Markdown output, and CLI exit codes.

Marvin Palencia, founder of [DeMark Studio](https://demarkstudio.ca), Miramichi, New Brunswick, Canada. Portfolio: [marvin.demarkstudio.ca](https://marvin.demarkstudio.ca)

MIT License.
