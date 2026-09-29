"""A small SUBSET of the Unicode confusables table, mapping look-alikes to Latin.

This is NOT the full confusables.txt. It holds the Cyrillic and Greek letters
that are most commonly swapped for Latin ones, plus a few Latin-internal
look-alikes (0, 1, dotless i). Entries were chosen by hand after the data
in confusables.txt (https://www.unicode.org/Public/security/latest/confusables.txt),
part of Unicode Security Mechanisms, UTS #39.

Unicode License v3 notice for the data this table is derived from:

  Copyright (c) 1991-2025 Unicode, Inc. All rights reserved.
  Distributed under the Terms of Use in https://www.unicode.org/copyright.html.

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of the Unicode data files and any associated documentation (the "Data Files")
  or Unicode software and any associated documentation (the "Software") to deal
  in the Data Files or Software without restriction, including without
  limitation the rights to use, copy, modify, merge, publish, distribute, and/or
  sell copies of the Data Files or Software, and to permit persons to whom the
  Data Files or Software are furnished to do so, provided that either (a) this
  copyright and permission notice appear with all copies of the Data Files or
  Software, or (b) this copyright and permission notice appear in associated
  Documentation.

  THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF
  THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED
  IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR
  CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
  TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
  OF THE DATA FILES OR SOFTWARE.

  Except as contained in this notice, the name of a copyright holder shall not
  be used in advertising or otherwise to promote the sale, use or other
  dealings in these Data Files or Software without prior written authorization
  of the copyright holder.

All code points are written as escapes so this file stays ASCII.
"""

CONFUSABLES = {
    # Cyrillic lowercase
    "\u0430": "a",  # CYRILLIC SMALL LETTER A
    "\u0435": "e",  # CYRILLIC SMALL LETTER IE
    "\u043e": "o",  # CYRILLIC SMALL LETTER O
    "\u0440": "p",  # CYRILLIC SMALL LETTER ER
    "\u0441": "c",  # CYRILLIC SMALL LETTER ES
    "\u0445": "x",  # CYRILLIC SMALL LETTER HA
    "\u0443": "y",  # CYRILLIC SMALL LETTER U
    "\u0456": "i",  # CYRILLIC SMALL BYELORUSSIAN-UKRAINIAN I
    "\u0458": "j",  # CYRILLIC SMALL LETTER JE
    "\u0455": "s",  # CYRILLIC SMALL LETTER DZE
    "\u04bb": "h",  # CYRILLIC SMALL LETTER SHHA
    "\u0501": "d",  # CYRILLIC SMALL LETTER KOMI DE
    "\u051b": "q",  # CYRILLIC SMALL LETTER QA
    "\u051d": "w",  # CYRILLIC SMALL LETTER WE
    "\u04cf": "l",  # CYRILLIC SMALL LETTER PALOCHKA
    # Cyrillic capitals
    "\u0410": "A",  # CYRILLIC CAPITAL LETTER A
    "\u0412": "B",  # CYRILLIC CAPITAL LETTER VE
    "\u0415": "E",  # CYRILLIC CAPITAL LETTER IE
    "\u041a": "K",  # CYRILLIC CAPITAL LETTER KA
    "\u041c": "M",  # CYRILLIC CAPITAL LETTER EM
    "\u041d": "H",  # CYRILLIC CAPITAL LETTER EN
    "\u041e": "O",  # CYRILLIC CAPITAL LETTER O
    "\u0420": "P",  # CYRILLIC CAPITAL LETTER ER
    "\u0421": "C",  # CYRILLIC CAPITAL LETTER ES
    "\u0422": "T",  # CYRILLIC CAPITAL LETTER TE
    "\u0423": "Y",  # CYRILLIC CAPITAL LETTER U
    "\u0425": "X",  # CYRILLIC CAPITAL LETTER HA
    "\u0406": "I",  # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I
    "\u0408": "J",  # CYRILLIC CAPITAL LETTER JE
    "\u0405": "S",  # CYRILLIC CAPITAL LETTER DZE
    "\u04c0": "l",  # CYRILLIC LETTER PALOCHKA
    # Greek lowercase
    "\u03bf": "o",  # GREEK SMALL LETTER OMICRON
    "\u03b1": "a",  # GREEK SMALL LETTER ALPHA
    "\u03bd": "v",  # GREEK SMALL LETTER NU
    "\u03c1": "p",  # GREEK SMALL LETTER RHO
    "\u03ba": "k",  # GREEK SMALL LETTER KAPPA
    "\u03b9": "i",  # GREEK SMALL LETTER IOTA
    "\u03c5": "u",  # GREEK SMALL LETTER UPSILON
    "\u03c7": "x",  # GREEK SMALL LETTER CHI
    # Greek capitals
    "\u0391": "A",  # GREEK CAPITAL LETTER ALPHA
    "\u0392": "B",  # GREEK CAPITAL LETTER BETA
    "\u0395": "E",  # GREEK CAPITAL LETTER EPSILON
    "\u0396": "Z",  # GREEK CAPITAL LETTER ZETA
    "\u0397": "H",  # GREEK CAPITAL LETTER ETA
    "\u0399": "I",  # GREEK CAPITAL LETTER IOTA
    "\u039a": "K",  # GREEK CAPITAL LETTER KAPPA
    "\u039c": "M",  # GREEK CAPITAL LETTER MU
    "\u039d": "N",  # GREEK CAPITAL LETTER NU
    "\u039f": "O",  # GREEK CAPITAL LETTER OMICRON
    "\u03a1": "P",  # GREEK CAPITAL LETTER RHO
    "\u03a4": "T",  # GREEK CAPITAL LETTER TAU
    "\u03a5": "Y",  # GREEK CAPITAL LETTER UPSILON
    "\u03a7": "X",  # GREEK CAPITAL LETTER CHI
    # Latin-internal look-alikes
    "\u0131": "i",  # LATIN SMALL LETTER DOTLESS I
    "0": "o",
    "1": "l",
}
