#!/usr/bin/env python3
"""The third panel of the filter row: what each filter actually passes.

    ../../../technology/seestar/.venv/bin/python passband_strip.py ../output

Drawn to match the two photographs it sits beside -- same 1125x2000 portrait
frame, wavelength running top to bottom so blue sits at the top exactly as it
does in the streaks. Two bars, LP on the left and IRCUT on the right, mirroring
the order of the photos. Everything a caption would have said is baked in as
three tick labels: 400, 700 and 1100 nm.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1125, 2000
LAM0, LAM1 = 380.0, 1150.0          # top and bottom of the axis
TOP, BOT = 250, 1900                # y of LAM0 and LAM1
BG = (10, 10, 12)
BLOCKED = (26, 26, 30)              # what a filter rejects
INK = (232, 228, 221)
MUT = (150, 144, 136)

LP_WINDOWS = [(483.0, 520.0), (650.0, 663.0)]
IRCUT_BAND = (400.0, 700.0)


def visible_rgb(lam):
    """Approximate sRGB for a wavelength in nm; black outside 380-780."""
    if lam < 380 or lam > 780:
        return (0.0, 0.0, 0.0)
    if lam < 440:   r, g, b = -(lam - 440) / 60, 0.0, 1.0
    elif lam < 490: r, g, b = 0.0, (lam - 440) / 50, 1.0
    elif lam < 510: r, g, b = 0.0, 1.0, -(lam - 510) / 20
    elif lam < 580: r, g, b = (lam - 510) / 70, 1.0, 0.0
    elif lam < 645: r, g, b = 1.0, -(lam - 645) / 65, 0.0
    else:           r, g, b = 1.0, 0.0, 0.0
    # roll off at the ends of human response so the strip fades rather than clips
    if lam < 420:   f = 0.3 + 0.7 * (lam - 380) / 40
    elif lam > 700: f = 0.3 + 0.7 * (780 - lam) / 80
    else:           f = 1.0
    return (r * f, g * f, b * f)


def y_of(lam):
    return TOP + (lam - LAM0) / (LAM1 - LAM0) * (BOT - TOP)


def font(size):
    for path in ("/System/Library/Fonts/Helvetica.ttc",
                 "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main(outdir="."):
    img = Image.new("RGB", (W, H), BG)
    px = img.load()

    bars = [(200, 470, "LP", lambda l: any(a <= l <= b for a, b in LP_WINDOWS)),
            (655, 925, "IRCUT", lambda l: IRCUT_BAND[0] <= l <= IRCUT_BAND[1])]

    for x0, x1, _, passes in bars:
        for y in range(TOP, BOT):
            lam = LAM0 + (y - TOP) / (BOT - TOP) * (LAM1 - LAM0)
            if passes(lam):
                r, g, b = visible_rgb(lam)
                # a passed band beyond human vision still gets through the
                # filter; show it as dim grey rather than nothing
                col = (int(r * 255), int(g * 255), int(b * 255)) if max(r, g, b) > 0 else (70, 70, 74)
            else:
                col = BLOCKED
            for x in range(x0, x1):
                px[x, y] = col

    d = ImageDraw.Draw(img)
    f_lab, f_tick = font(46), font(38)

    for x0, x1, name, _ in bars:
        w = d.textlength(name, font=f_lab)
        d.text(((x0 + x1) / 2 - w / 2, TOP - 78), name, font=f_lab, fill=INK)
        d.rectangle([x0, TOP, x1 - 1, BOT - 1], outline=(58, 55, 48), width=2)

    # Wavelength scale: the three numbers that carry the whole point --
    # where the visible starts, where IRCUT cuts, where silicon gives up.
    for lam in (400, 700, 1100):
        y = y_of(lam)
        d.line([(130, y), (170, y)], fill=MUT, width=3)
        # right-align against the tick so 1100 does not run into it
        tw = d.textlength(str(lam), font=f_tick)
        d.text((110 - tw, y - 22), str(lam), font=f_tick, fill=MUT)

    out = os.path.join(outdir, "20260801 filter passbands.png")
    img.save(out)
    print("  wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
