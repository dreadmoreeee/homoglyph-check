import pytest

from homoglyph_check import check_text, decode_domain, extract_domains, is_lookalike_domain, skeleton
from homoglyph_check.domains import match_protected

REAL = "demarkstudio.ca"
SUB = "marvin.demarkstudio.ca"
PROTECT = [REAL, SUB]
CYR_A, CYR_O, GRK_O = "\u0430", "\u043e", "\u03bf"

VARIANTS = {
    "cyrillic-a": "dem" + CYR_A + "rkstudio.ca",
    "cyrillic-o": "demarkstudi" + CYR_O + ".ca",
    "greek-omicron": "demarkstudi" + GRK_O + ".ca",
    "cyrillic-sub": "marvin.dem" + CYR_A + "rkstudio.ca",
}


def puny(domain):
    return domain.encode("idna").decode("ascii")


@pytest.mark.parametrize("name", sorted(VARIANTS))
def test_unicode_lookalike_caught(name):
    d = VARIANTS[name]
    assert is_lookalike_domain(d, PROTECT)
    r = check_text("visit https://%s/login" % d, protect=PROTECT)
    assert [f.severity for f in r.findings if f.kind == "lookalike-domain"] == ["high"]


@pytest.mark.parametrize("name", sorted(VARIANTS))
def test_punycode_round_trip(name):
    d = VARIANTS[name]
    x = puny(d)
    assert "xn--" in x and x.isascii()
    assert decode_domain(x)[0] == d
    assert is_lookalike_domain(x, PROTECT)
    r = check_text("see http://%s/" % x, protect=PROTECT)
    hit = [f for f in r.findings if f.kind == "lookalike-domain"]
    assert len(hit) == 1 and hit[0].severity == "high"
    assert "decoded from punycode" in hit[0].message
    assert any(f.kind == "mixed-script-domain" for f in r.findings)


def test_real_domains_not_flagged():
    text = "http://demarkstudio.ca/ and https://marvin.demarkstudio.ca/x, www.demarkstudio.ca. Also DeMarkStudio.CA"
    r = check_text(text, protect=PROTECT)
    assert r.ok
    assert not is_lookalike_domain(REAL, PROTECT, distance=True)
    assert not is_lookalike_domain(SUB, PROTECT, distance=True)


def test_zero_width_inserted_is_flagged():
    d = "demark\u200bstudio.ca"
    assert is_lookalike_domain(d, PROTECT)
    r = check_text("go to " + d, protect=PROTECT)
    assert {"lookalike-domain", "zero-width"} <= {f.kind for f in r.findings}


def test_fullwidth_domain_flagged():
    d = "".join(chr(ord(c) + 0xFEE0) if c.isalpha() else c for c in REAL)
    assert d != REAL
    assert is_lookalike_domain(d, PROTECT)


def test_dot_variants_and_subdomain_of_lookalike():
    assert is_lookalike_domain("www.dem" + CYR_A + "rkstudio.ca", PROTECT)
    assert is_lookalike_domain("dem" + CYR_A + "rkstudio\u3002ca", PROTECT)


def test_digit_lookalike_and_edit_distance():
    assert is_lookalike_domain("demarkstud1o.ca", PROTECT, distance=True)  # 1 maps to l, not i: 1 edit
    m = match_protected("demarkstudi.ca", PROTECT)
    assert m and m.severity == "medium"
    assert not is_lookalike_domain("demarkstudi.ca", PROTECT)  # default: exact skeleton only
    assert match_protected("unrelated-site.org", PROTECT) is None


def test_unrelated_domains_not_flagged():
    r = check_text("mail me@example.com or visit https://example.org/a?b=1", protect=PROTECT)
    assert r.ok


def test_extract_domains_skips_numbers_and_abbreviations():
    found = [raw for _, raw in extract_domains("v1.2.3, e.g. 10.0.0.1 and demarkstudio.ca.")]
    assert found == ["demarkstudio.ca"]


def test_mixed_script_domain_without_protect_list():
    r = check_text("http://p" + CYR_A + "ypal.com/")
    assert [f.kind for f in r.findings] == ["mixed-script-domain"]
    assert r.findings[0].severity == "high"


def test_skeleton_of_variants_equal():
    for d in VARIANTS.values():
        if d.endswith(REAL[-3:]) and d.count(".") == 1:
            assert skeleton(d) == skeleton(REAL)
