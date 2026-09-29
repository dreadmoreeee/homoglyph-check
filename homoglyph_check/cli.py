"""Command line interface."""

import argparse
import re
import sys

from .core import check_text
from .report import SEVERITIES

_ESC_RE = re.compile(r"\\u([0-9a-fA-F]{4})|\\U([0-9a-fA-F]{8})")


def unescape(text):
    """Turn \\uXXXX and \\UXXXXXXXX sequences into characters (keeps input files ASCII)."""
    return _ESC_RE.sub(lambda m: chr(int(m.group(1) or m.group(2), 16)), text)


def build_parser():
    p = argparse.ArgumentParser(
        prog="homoglyph-check",
        description="Offline check for look-alike letters, invisible/bidi characters and look-alike domains.",
        epilog="Exit codes: 0 clean, 1 finding at or above --fail-on, 2 usage or input error.",
    )
    p.add_argument("text", nargs="*", help="text to check (or use --file / stdin)")
    p.add_argument("-f", "--file", help="read text from a file ('-' for stdin)")
    p.add_argument("--protect", default="", help="comma-separated domains to guard, e.g. example.com,www.example.com")
    fmt = p.add_mutually_exclusive_group()
    fmt.add_argument("--json", action="store_true", help="JSON output")
    fmt.add_argument("--markdown", action="store_true", help="Markdown output")
    p.add_argument("--fail-on", choices=SEVERITIES + ("never",), default="high",
                   help="exit 1 if a finding is at or above this severity (default: high)")
    p.add_argument("--unescape", action="store_true", help="decode \\uXXXX / \\UXXXXXXXX sequences in the input first")
    return p


def _read(args):
    if args.file == "-" or (not args.file and not args.text):
        return sys.stdin.buffer.read().decode("utf-8", "replace")
    if args.file:
        with open(args.file, "rb") as fh:
            return fh.read().decode("utf-8", "replace")
    return "\n".join(args.text)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        text = _read(args)
    except OSError as exc:
        print("homoglyph-check: cannot read input: %s" % exc, file=sys.stderr)
        return 2
    if args.unescape:
        text = unescape(text)
    protect = [d.strip() for d in args.protect.split(",") if d.strip()]
    report = check_text(text, protect=protect)
    if args.json:
        out = report.to_json()
    elif args.markdown:
        out = report.to_markdown()
    else:
        out = report.to_text()
    sys.stdout.write(out + "\n")
    if args.fail_on != "never" and report.at_or_above(args.fail_on):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
