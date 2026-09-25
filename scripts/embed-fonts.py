#!/usr/bin/env python3
"""Embed fonts/*.woff2 into theme.css as base64, between the FONTS:GENERATED markers.

The community installer only fetches theme.css and manifest.json, and Obsidian's
theme policy bans network requests, so the font has to live inside the stylesheet.
Usage: python3 scripts/embed-fonts.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACES = [  # file, unicode-range
    ("inter-latin.woff2", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("inter-cyrillic.woff2", "U+0301,U+0400-052F,U+1C80-1C88,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F"),
]

blocks = []
for name, urange in FACES:
    data = base64.b64encode((ROOT / "fonts" / name).read_bytes()).decode()
    blocks.append(
        "@font-face {\n  font-family: Inter;\n"
        f"  src: url(\"data:font/woff2;base64,{data}\") format(\"woff2\");\n"
        "  font-weight: 400 600;\n  font-style: normal;\n  font-display: swap;\n"
        f"  unicode-range: {urange};\n}}\n")

css = (ROOT / "theme.css").read_text()
start = "/* FONTS:GENERATED:START — produced by scripts/embed-fonts.py, do not hand-edit */"
end = "/* FONTS:GENERATED:END */"
css = re.sub(re.escape(start) + r".*?" + re.escape(end),
             lambda _: start + "\n" + "\n".join(blocks) + end, css, flags=re.S)
(ROOT / "theme.css").write_text(css)
print(f"embedded {len(FACES)} faces")
