"""Findings and reports, with text, JSON and Markdown output."""

import json
from dataclasses import asdict, dataclass, field

SEVERITIES = ("low", "medium", "high")
UTS39 = "https://www.unicode.org/reports/tr39/"


def severity_rank(sev):
    return SEVERITIES.index(sev)


def show(s):
    """ASCII-safe rendering: non-ASCII and control characters as \\uXXXX escapes."""
    out = []
    for c in s:
        cp = ord(c)
        if 32 <= cp < 127:
            out.append(c)
        elif cp <= 0xFFFF:
            out.append("\\u%04x" % cp)
        else:
            out.append("\\U%08x" % cp)
    return "".join(out)


@dataclass
class Finding:
    kind: str
    severity: str
    message: str
    index: int  # 0-based character offset in the input
    line: int
    column: int
    snippet: str = ""
    codepoint: str = ""
    name: str = ""
    advice: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Report:
    text_length: int
    findings: list = field(default_factory=list)

    def max_severity(self):
        if not self.findings:
            return None
        return max((f.severity for f in self.findings), key=severity_rank)

    def counts(self):
        return {s: sum(1 for f in self.findings if f.severity == s) for s in reversed(SEVERITIES)}

    def at_or_above(self, threshold):
        return [f for f in self.findings if severity_rank(f.severity) >= severity_rank(threshold)]

    @property
    def ok(self):
        return not self.findings

    def to_dict(self):
        return {
            "text_length": self.text_length,
            "max_severity": self.max_severity(),
            "counts": self.counts(),
            "findings": [f.to_dict() for f in self.findings],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    def to_text(self):
        if not self.findings:
            return "homoglyph-check: nothing suspicious found (%d characters checked)" % self.text_length
        c = self.counts()
        lines = ["homoglyph-check: %d finding(s) (high %d, medium %d, low %d)"
                 % (len(self.findings), c["high"], c["medium"], c["low"])]
        for f in self.findings:
            lines.append("[%s] %s  line %d, col %d" % (f.severity.upper(), f.kind, f.line, f.column))
            lines.append("    %s" % f.message)
            if f.advice:
                lines.append("    fix: %s" % f.advice)
        lines.append("Escapes like \\u0430 show the real code points. Guidance: NFKC + skeleton, %s" % UTS39)
        return "\n".join(lines)

    def to_markdown(self):
        if not self.findings:
            return "# homoglyph-check\n\nNothing suspicious found (%d characters checked).\n" % self.text_length
        c = self.counts()
        out = ["# homoglyph-check report", "",
               "%d finding(s): high %d, medium %d, low %d." % (len(self.findings), c["high"], c["medium"], c["low"]),
               "", "| Severity | Kind | Line:Col | Detail |", "|---|---|---|---|"]
        for f in self.findings:
            detail = f.message.replace("|", "\\|")
            out.append("| %s | %s | %d:%d | %s |" % (f.severity, f.kind, f.line, f.column, detail))
        out += ["", "Code points are shown as `\\uXXXX` escapes. Suggested handling: normalize with NFKC and compare "
                "skeletons, see [UTS #39](%s)." % UTS39, ""]
        return "\n".join(out)
