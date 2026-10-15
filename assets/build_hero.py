#!/usr/bin/env python3
"""Build the profile header SVGs (desktop and mobile).

The background is assets/horizon.jpg, generated locally with FLUX.2 Klein 9B (OverSeer Image, seed 1015). The name
and tagline are set in GitHub's open-source families (SIL OFL), Hubot Sans and Mona Sans, fetched from npm, pinned
to static instances, subset to the glyphs used and embedded with the image, so the SVGs render identically
everywhere and in both GitHub themes.

    pip install fonttools brotli pillow
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
from PIL import Image

OUT = Path(__file__).resolve().parent

NAME = "Michael Berardi"
TAGLINE = "New York · Buenos Aires"
TAGLINE_LINES = ("New York · Buenos Aires",)
TITLE = f"{NAME}. New York and Buenos Aires."
INK, BODY = "#f2f4f7", "#9aa3ad"
DISPLAY = "Hubot, -apple-system, 'Segoe UI', Helvetica, sans-serif"
SANS = "Mona, -apple-system, 'Segoe UI', Helvetica, sans-serif"


def fetch(pkg: str, member: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        name = subprocess.run(["npm", "pack", "-q", pkg], cwd=tmp, check=True,
                              capture_output=True, text=True).stdout.strip().splitlines()[-1]
        with tarfile.open(Path(tmp) / name) as tar:
            return tar.extractfile(f"package/files/{member}").read()


def embed(data: bytes, text: str, axes: dict) -> str:
    font = instancer.instantiateVariableFont(TTFont(io.BytesIO(data)), axes)
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
    hubot = fetch("@fontsource-variable/hubot-sans", "hubot-sans-latin-standard-normal.woff2")
    mona = fetch("@fontsource-variable/mona-sans", "mona-sans-latin-standard-normal.woff2")
    faces = [("Hubot", embed(hubot, NAME, {"wght": 700, "wdth": 108})),
             ("Mona", embed(mona, TAGLINE, {"wght": 380, "wdth": 100}))]
    return "\n".join(f"@font-face{{font-family:{n};src:url(data:font/woff2;base64,{b}) format('woff2')}}" for n, b in faces)


def jpeg(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.convert("RGB").save(buf, "JPEG", quality=86, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def svg(w: int, h: int, css: str, picture: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-labelledby="title">\n<title id="title">{TITLE}</title>\n<style>{css}</style>\n'
            f'<defs><clipPath id="r"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>\n'
            f'<g clip-path="url(#r)"><rect width="{w}" height="{h}" fill="#050607"/>\n'
            f'<image width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{picture}"/>\n'
            f'{body}</g>\n</svg>\n')


def desktop(source: Image.Image, css: str) -> str:
    w, h = 1536, 512
    body = (f'<text x="96" y="236" fill="{INK}" font-family="{DISPLAY}" font-size="84" letter-spacing="-1" word-spacing="14">{NAME}</text>\n'
            f'<text x="99" y="304" fill="{BODY}" font-family="{SANS}" font-size="30" letter-spacing="2">{TAGLINE}</text>\n')
    return svg(w, h, css, jpeg(source.resize((w, h), Image.LANCZOS)), body)


def mobile(source: Image.Image, css: str) -> str:
    w, h = 900, 640
    # the light on the horizon sits in the right of the frame: keep it, and the dark sea below it for the text
    span = round(source.height * w / h)
    canvas = source.crop((source.width - span, 0, source.width, source.height)).resize((w, h), Image.LANCZOS)
    body = (f'<text x="56" y="452" fill="{INK}" font-family="{DISPLAY}" font-size="90" letter-spacing="-1" word-spacing="14">{NAME}</text>\n'
            f'<text x="60" y="530" fill="{BODY}" font-family="{SANS}" font-size="42" letter-spacing="2">{TAGLINE_LINES[0]}</text>\n')
    return svg(w, h, css, jpeg(canvas), body)


def main():
    css = font_css()
    source = Image.open(OUT / "horizon.jpg")
    (OUT / "header.svg").write_text(desktop(source, css))
    (OUT / "header-mobile.svg").write_text(mobile(source, css))


if __name__ == "__main__":
    main()
