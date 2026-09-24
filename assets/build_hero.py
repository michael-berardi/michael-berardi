#!/usr/bin/env python3
"""Build the profile header SVGs (desktop + mobile, light + dark).

Fonts are GitHub's open-source families (SIL OFL): Hubot Sans, Mona Sans,
and Monaspace Neon. They are fetched from npm, pinned to static instances,
subset to the glyphs used, and embedded so the SVGs render identically
everywhere.

    pip install fonttools brotli
    python3 assets/build_hero.py
"""

import base64
import io
import subprocess
import tarfile
import tempfile
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parent

NAME = ("Michael", "Berardi")
TAGLINE = ("I build software that stays useful", "when the demo is over.")
KICKER = "AGENT INFRASTRUCTURE · LOCAL-FIRST SOFTWARE"
LANGS = "SWIFT · RUST · TYPESCRIPT · PYTHON"
PROMPT = "$ cat stack"
STACK = [
    ("memory", "retex", ""),
    ("hands", "overseer-browser", "computer-use"),
    ("plan", "ultraterm-plan", "usap"),
    ("bill", "ultracompress", "$0 per compaction"),
]

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", line="#30363d", ink="#f0f6fc",
                 body="#c9d1d9", muted="#8b949e", accent="#ffa657", dot="#21262d"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", line="#d0d7de", ink="#1f2328",
                  body="#31373d", muted="#656d76", accent="#bc4c00", dot="#eaeef2"),
}


def fetch(pkg: str, member: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        name = subprocess.run(["npm", "pack", "-q", pkg], cwd=tmp, check=True,
                              capture_output=True, text=True).stdout.strip().splitlines()[-1]
        with tarfile.open(Path(tmp) / name) as tar:
            return tar.extractfile(f"package/files/{member}").read()


def embed(data: bytes, text: str, axes: dict | None = None) -> str:
    font = TTFont(io.BytesIO(data))
    if axes:
        font = instancer.instantiateVariableFont(font, axes)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css() -> str:
    everything = " ".join([*NAME, *TAGLINE, KICKER, LANGS, PROMPT]
                          + [w for row in STACK for w in row]) + "●▍"
    hubot = fetch("@fontsource-variable/hubot-sans", "hubot-sans-latin-standard-normal.woff2")
    mona = fetch("@fontsource-variable/mona-sans", "mona-sans-latin-standard-normal.woff2")
    neon = fetch("@fontsource/monaspace-neon", "monaspace-neon-latin-400-normal.woff2")
    faces = [
        ("Hubot", embed(hubot, "".join(NAME), {"wght": 800, "wdth": 112})),
        ("Mona", embed(mona, " ".join(TAGLINE), {"wght": 420, "wdth": 100})),
        ("Neon", embed(neon, everything)),
    ]
    return "\n".join(
        f"@font-face{{font-family:{n};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
        for n, b in faces)


MONO = "Neon, ui-monospace, SFMono-Regular, Menlo, monospace"
SANS = "Mona, -apple-system, 'Segoe UI', Helvetica, sans-serif"
DISPLAY = "Hubot, -apple-system, 'Segoe UI', Helvetica, sans-serif"


def terminal(t, x, y, w, size=17, row=38):
    h = 96 + row * len(STACK) + 44
    out = [f'<g transform="translate({x} {y})">',
           f'<rect width="{w}" height="{h}" rx="12" fill="{t["panel"]}" stroke="{t["line"]}"/>',
           f'<path d="M0 44H{w}" stroke="{t["line"]}"/>']
    for i, _ in enumerate(range(3)):
        out.append(f'<circle cx="{24 + i * 18}" cy="22" r="5" fill="{t["line"]}"/>')
    out.append(f'<text x="{w / 2}" y="27" text-anchor="middle" fill="{t["muted"]}" '
               f'font-family="{MONO}" font-size="13">~/michael-berardi</text>')
    out.append(f'<g font-family="{MONO}" font-size="{size}">')
    out.append(f'<text x="28" y="86" fill="{t["muted"]}">{PROMPT}</text>')
    col2 = 28 + size * 5.2
    for i, (k, a, b) in enumerate(STACK):
        yy = 86 + row * (i + 1)
        out.append(f'<text x="28" y="{yy}" fill="{t["muted"]}">{k}</text>')
        tail = ""
        if b:
            fill = t["accent"] if b.startswith("$") else t["body"]
            tail = f'<tspan fill="{t["muted"]}">  ·  </tspan><tspan fill="{fill}">{b}</tspan>'
        out.append(f'<text x="{col2:.0f}" y="{yy}" fill="{t["ink"]}">{a}{tail}</text>')
    cy = 86 + row * (len(STACK) + 1)
    out.append(f'<text x="28" y="{cy}" fill="{t["accent"]}">▍</text>')
    out.append("</g></g>")
    return "\n".join(out)


def dots(t, w, h, step=22):
    return (f'<defs><pattern id="d" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern>'
            f'<linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="{t["bg"]}"/>'
            f'<stop offset=".45" stop-color="{t["bg"]}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#d)"/><rect width="{w}" height="{h}" fill="url(#f)"/>')


def svg(w, h, t, css, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title">\n'
            f'<title id="title">Michael Berardi. I build software that stays useful when the demo is over.</title>\n'
            f'<style>{css}</style>\n'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/>\n'
            f'{body}\n</svg>\n')


def desktop(t, css):
    w, h = 1280, 500
    body = [dots(t, w, h),
            f'<text x="72" y="84" fill="{t["accent"]}" font-family="{MONO}" font-size="15" letter-spacing="1.5">{KICKER}</text>',
            f'<g fill="{t["ink"]}" font-family="{DISPLAY}" font-size="112" letter-spacing="-3">',
            f'<text x="66" y="210">{NAME[0]}</text><text x="66" y="318">{NAME[1]}</text></g>',
            f'<g fill="{t["body"]}" font-family="{SANS}" font-size="26">',
            f'<text x="72" y="382">{TAGLINE[0]}</text><text x="72" y="416">{TAGLINE[1]}</text></g>',
            terminal(t, 700, 92, 508),
            f'<text x="1208" y="438" text-anchor="end" fill="{t["muted"]}" font-family="{MONO}" font-size="13" letter-spacing="1.5">{LANGS}</text>']
    return svg(w, h, t, css, "\n".join(body))


def mobile(t, css):
    w, h = 600, 790
    body = [dots(t, w, h),
            f'<text x="44" y="70" fill="{t["accent"]}" font-family="{MONO}" font-size="13" letter-spacing="1">{KICKER}</text>',
            f'<g fill="{t["ink"]}" font-family="{DISPLAY}" font-size="92" letter-spacing="-2.5">',
            f'<text x="38" y="170">{NAME[0]}</text><text x="38" y="258">{NAME[1]}</text></g>',
            f'<g fill="{t["body"]}" font-family="{SANS}" font-size="24">',
            f'<text x="44" y="318">{TAGLINE[0]}</text><text x="44" y="350">{TAGLINE[1]}</text></g>',
            terminal(t, 38, 400, 524, size=16, row=36),
            f'<text x="44" y="746" fill="{t["muted"]}" font-family="{MONO}" font-size="13" letter-spacing="1.5">{LANGS}</text>']
    return svg(w, h, t, css, "\n".join(body))


def main():
    css = font_css()
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(desktop(t, css))
        (OUT / f"header-{name}-mobile.svg").write_text(mobile(t, css))


if __name__ == "__main__":
    main()
