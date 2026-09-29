import pytest

from homoglyph_check import check_text, normalize, skeleton
from homoglyph_check.invisible import INVISIBLE

CYR_A, CYR_O, GRK_O = "\u0430", "\u043e", "\u03bf"


def kinds(report):
    return [f.kind for f in report.findings]


def test_mixed_script_word_flagged():
    r = check_text("please p" + CYR_A + "y now")
    assert kinds(r) == ["mixed-script"]
    assert r.findings[0].severity == "medium"
    assert "U+0430" in r.findings[0].message


def test_greek_mixed_flagged():
    assert kinds(check_text("hell" + GRK_O)) == ["mixed-script"]


def test_pure_cyrillic_or_greek_word_not_flagged():
    assert check_text("\u043f\u0440\u0438\u0432\u0435\u0442 \u03b1\u03b2\u03b3").ok


def test_french_and_spanish_not_flagged():
    fr = "Ceci est une d\u00e9monstration, \u00e0 l'\u00e9cole: \u0153uvre, na\u00efve, ma\u00eetre, \u00e7a va."
    es = "Ma\u00f1ana el ni\u00f1o compr\u00f3 pi\u00f1a y caf\u00e9 en Espa\u00f1a. \u00bfQu\u00e9 tal?"
    assert check_text(fr).ok
    assert check_text(es).ok
    assert check_text("cafe\u0301 nin\u0303o").ok  # decomposed accents


def test_emoji_zwj_sequence_not_flagged():
    family = "\U0001F468\u200d\U0001F469\u200d\U0001F467"
    heart = "\U0001F468\u200d\u2764\ufe0f\u200d\U0001F468"
    assert check_text("Hi " + family + " and " + heart).ok


def test_zwj_between_latin_letters_flagged():
    r = check_text("pay\u200dpal")
    assert kinds(r) == ["zero-width"]


def test_arabic_zwnj_not_flagged():
    assert check_text("\u0645\u06cc\u200c\u062e\u0648\u0627\u0647\u0645").ok


@pytest.mark.parametrize("cp", sorted(INVISIBLE))
def test_each_invisible_char_reported(cp):
    text = "ab" + chr(cp) + "cd"
    if cp == 0xFEFF:
        text = "ab" + chr(cp) + "cd"
    r = check_text(text)
    hits = [f for f in r.findings if f.codepoint == "U+%04X" % cp]
    assert len(hits) == 1
    f = hits[0]
    assert f.index == 2 and f.column == 3 and f.line == 1
    assert f.name and f.severity == INVISIBLE[cp][0]


def test_bom_at_start_ignored_but_mid_text_flagged():
    assert check_text("\ufeffhello").ok
    assert kinds(check_text("hel\ufefflo")) == ["zero-width"]


def test_trojan_source_rlo():
    src = "access = 'user\u202e \u2066// admin only\u2069 \u2066';"
    r = check_text(src)
    bidi = [f for f in r.findings if f.kind == "bidi-control"]
    assert {f.codepoint for f in bidi} == {"U+202E", "U+2066", "U+2069"}
    assert r.max_severity() == "high"


def test_line_and_column():
    r = check_text("one\ntw\u200bo")
    f = r.findings[0]
    assert (f.line, f.column) == (2, 3)


def test_nfkc_fullwidth_and_math():
    assert normalize("\uff50\uff41\uff59\uff50\uff41\uff4c") == "paypal"
    assert normalize(chr(0x1D5D5) + chr(0x1D602) + chr(0x1D606)) == "Buy"
    r = check_text("click \uff42\uff55\uff59 now")
    assert kinds(r) == ["compat-alphanumerics"]
    assert "buy" in r.findings[0].message


def test_skeleton_maps_confusables():
    assert skeleton("p" + CYR_A + "yp" + CYR_A + "l") == "paypal"
    assert skeleton("PAYPAL") == skeleton("paypal")
    assert skeleton("pay\u200bpal") == "paypal"
    assert skeleton("\uff50aypal") == "paypal"
    assert skeleton("\u00e9") == skeleton("e\u0301")
    assert skeleton("\u00e9") != skeleton("e")  # accents are kept
