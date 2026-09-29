# homoglyph-check report

19 finding(s): high 18, medium 1, low 0.

| Severity | Kind | Line:Col | Detail |
|---|---|---|---|
| high | lookalike-domain | 5:11 | dem\u0430rkstudio.ca: skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 5:11 | domain dem\u0430rkstudio.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 6:11 | demarkstudi\u043e.ca: skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 6:11 | domain demarkstudi\u043e.ca has a label (demarkstudi\u043e) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 7:11 | demarkstudi\u03bf.ca: skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 7:11 | domain demarkstudi\u03bf.ca has a label (demarkstudi\u03bf) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 8:11 | marvin.dem\u0430rkstudio.ca: skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 8:11 | domain marvin.dem\u0430rkstudio.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 9:11 | demark\u200bstudio.ca: skeleton equals the protected domain demarkstudio.ca |
| medium | zero-width | 9:17 | U+200B ZERO WIDTH SPACE at offset 234 |
| high | lookalike-domain | 10:11 | \uff44\uff45\uff4d\uff41\uff52\uff4b\uff53\uff54\uff55\uff44\uff49\uff4f.\uff43\uff41: skeleton equals the protected domain demarkstudio.ca |
| high | lookalike-domain | 12:11 | xn--demrkstudio-0ij.ca (decoded from punycode: dem\u0430rkstudio.ca): skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 12:11 | domain xn--demrkstudio-0ij.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 13:11 | xn--demarkstudi-1nj.ca (decoded from punycode: demarkstudi\u043e.ca): skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 13:11 | domain xn--demarkstudi-1nj.ca has a label (demarkstudi\u043e) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 14:11 | xn--demarkstudi-ifi.ca (decoded from punycode: demarkstudi\u03bf.ca): skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 14:11 | domain xn--demarkstudi-ifi.ca has a label (demarkstudi\u03bf) mixing Latin with Cyrillic or Greek |
| high | lookalike-domain | 15:11 | marvin.xn--demrkstudio-0ij.ca (decoded from punycode: marvin.dem\u0430rkstudio.ca): skeleton equals the protected domain demarkstudio.ca |
| high | mixed-script-domain | 15:11 | domain marvin.xn--demrkstudio-0ij.ca has a label (dem\u0430rkstudio) mixing Latin with Cyrillic or Greek |

Code points are shown as `\uXXXX` escapes. Suggested handling: normalize with NFKC and compare skeletons, see [UTS #39](https://www.unicode.org/reports/tr39/).

