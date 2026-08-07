#!/usr/bin/env python3
"""Convert a source image into a square, transparent-padded 128x128 PNG.

Used to normalize catalog icons (see icons/ in this repo). Pads the source to a
centered square on a transparent background, then downsizes to 128x128 with
high-quality resampling.

Usage:
    uv run --with pillow python scripts/make_icon.py <source> <dest.png> [size]

Example:
    uv run --with pillow python scripts/make_icon.py \
        icons/Eia-logomark.svg.webp icons/eia.png
"""

from __future__ import annotations

import sys

from PIL import Image


def make_square_png(src: str, dest: str, size: int = 128) -> None:
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    side = max(w, h)

    # Center the source on a transparent square canvas.
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(img, ((side - w) // 2, (side - h) // 2), img)

    square = square.resize((size, size), Image.LANCZOS)
    square.save(dest, format="PNG")
    print(f"wrote {dest} ({size}x{size}) from {src} ({w}x{h})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    dest = sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 128
    make_square_png(src, dest, size)
