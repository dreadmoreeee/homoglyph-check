"""homoglyph-check: look-alike letters, invisible characters and look-alike domains."""

from .confusables_data import CONFUSABLES
from .core import check_text
from .domains import decode_domain, extract_domains, is_lookalike_domain, match_protected
from .invisible import INVISIBLE, find_invisible
from .report import Finding, Report
from .scripts import script_of, scripts_in
from .skeleton import normalize, skeleton

__version__ = "0.1.0"

__all__ = [
    "CONFUSABLES", "INVISIBLE", "Finding", "Report", "check_text", "decode_domain",
    "extract_domains", "find_invisible", "is_lookalike_domain", "match_protected",
    "normalize", "script_of", "scripts_in", "skeleton",
]
