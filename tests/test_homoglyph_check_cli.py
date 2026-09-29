import io
import json
import sys

import pytest

from homoglyph_check import check_text
from homoglyph_check.cli import main, unescape

BAD = "dem\u0430rkstudio.ca"
BIDI = "a\u202eb"


def run(capsys, *argv, stdin=None, monkeypatch=None):
    if stdin is not None:
        monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(stdin.encode("utf-8"))))
    code = main(list(argv))
    return code, capsys.readouterr().out


def test_clean_exit_0(capsys):
    code, out = run(capsys, "hello there")
    assert code == 0 and "nothing suspicious" in out


def test_lookalike_exit_1(capsys):
    code, out = run(capsys, BAD, "--protect", "demarkstudio.ca")
    assert code == 1 and "HIGH" in out and "\\u0430" in out
    assert out.isascii()


def test_fail_on_thresholds(capsys):
    word = "p\u0430y"  # medium mixed-script only
    assert run(capsys, word)[0] == 0
    assert run(capsys, word, "--fail-on", "medium")[0] == 1
    assert run(capsys, word, "--fail-on", "low")[0] == 1
    assert run(capsys, BIDI, "--fail-on", "never")[0] == 0
    assert run(capsys, BIDI)[0] == 1


def test_usage_error_exit_2(capsys):
    with pytest.raises(SystemExit) as e:
        main(["--fail-on", "bogus"])
    assert e.value.code == 2


def test_missing_file_exit_2(capsys, tmp_path):
    assert main(["--file", str(tmp_path / "nope.txt")]) == 2


def test_file_and_stdin(capsys, tmp_path, monkeypatch):
    f = tmp_path / "in.txt"
    f.write_bytes(BIDI.encode("utf-8"))
    assert run(capsys, "--file", str(f))[0] == 1
    code, _ = run(capsys, "-f", "-", stdin=BIDI, monkeypatch=monkeypatch)
    assert code == 1
    code, _ = run(capsys, stdin="plain text", monkeypatch=monkeypatch)
    assert code == 0


def test_json_output(capsys):
    code, out = run(capsys, BAD, "--protect", "demarkstudio.ca,marvin.demarkstudio.ca", "--json")
    data = json.loads(out)
    assert code == 1
    assert data["max_severity"] == "high"
    assert data["counts"]["high"] >= 1
    kinds = {f["kind"] for f in data["findings"]}
    assert "lookalike-domain" in kinds
    assert {"kind", "severity", "line", "column", "index", "advice"} <= set(data["findings"][0])


def test_markdown_output(capsys):
    code, out = run(capsys, BIDI, "--markdown")
    assert out.startswith("# homoglyph-check report")
    assert "| high | bidi-control | 1:2 |" in out
    assert "https://www.unicode.org/reports/tr39/" in out
    code, out = run(capsys, "clean", "--markdown")
    assert "Nothing suspicious" in out and code == 0


def test_unescape_flag(capsys):
    assert unescape("p\\u0430y \\U0001F600") == "p\u0430y \U0001F600"
    code, out = run(capsys, "p\\u0430y", "--unescape", "--fail-on", "medium")
    assert code == 1 and "mixed-script" in out


def test_report_api_shapes():
    r = check_text(BIDI)
    assert r.to_dict()["findings"][0]["codepoint"] == "U+202E"
    assert json.loads(r.to_json())["text_length"] == 3
