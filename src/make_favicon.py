#!/usr/bin/env python
"""Generate the site icons, which the old site did not have at all.

Writes favicon.svg (vector, used by modern browsers), favicon.ico (32/16 px
fallback) and apple-touch-icon.png (180 px) to the repository root.

    python src/make_favicon.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

ACCENT = (26, 84, 144)   # matches --accent in site.css
FG = (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#1a5490"/>
  <text x="32" y="43" font-family="Helvetica, Arial, sans-serif" font-size="30"
        font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="-1">ZY</text>
</svg>
"""


def find_font(size: int) -> ImageFont.FreeTypeFont:
    for name in ("arialbd.ttf", "Arial Bold.ttf", "seguisb.ttf", "DejaVuSans-Bold.ttf"):
        for folder in (Path("C:/Windows/Fonts"), Path("/usr/share/fonts/truetype/dejavu"),
                       Path("/System/Library/Fonts")):
            candidate = folder / name
            if candidate.exists():
                return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def draw_icon(size: int) -> Image.Image:
    # Render at 4x then downsample: gives clean edges on the rounded corners.
    scale = 4
    big = size * scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.19), fill=ACCENT)

    font = find_font(int(big * 0.46))
    text = "ZY"
    box = d.textbbox((0, 0), text, font=font)
    d.text(
        ((big - (box[2] - box[0])) / 2 - box[0], (big - (box[3] - box[1])) / 2 - box[1]),
        text,
        font=font,
        fill=FG,
    )
    return img.resize((size, size), Image.LANCZOS)


def main() -> int:
    (ROOT / "favicon.svg").write_text(SVG, encoding="utf-8")
    print("  favicon.svg")

    ico = draw_icon(64)
    ico.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico")

    # Apple wants an opaque icon.
    touch = Image.new("RGB", (180, 180), ACCENT)
    touch.paste(draw_icon(180), (0, 0), draw_icon(180))
    touch.save(ROOT / "apple-touch-icon.png", optimize=True)
    print("  apple-touch-icon.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
