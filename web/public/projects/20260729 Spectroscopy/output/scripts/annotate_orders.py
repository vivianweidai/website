#!/usr/bin/env python3
"""Mark m = 0 and m = 1 on the raw Vega frame.

    ../../../technology/seestar/.venv/bin/python annotate_orders.py <frame.jpg> <out.jpg>

The report explains the two orders in prose; this puts the labels on the frame
itself so the reader can see which is which without counting down from the top.
Positions are measured from the frame, not hard-coded -- the zero order is the
compact bright blob, the first order the long one.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, label

INK = (255, 217, 160)      # the dot
ACC = (232, 180, 140)      # the streak
BAL = (188, 220, 240)      # the Balmer absorption bands

# Distance from the zero-order dot to each Balmer line, in NATIVE sensor pixels,
# as fitted on the 2026-07-29 frame. Scaled by image height / 3840 for a resized
# copy. Verified against this JPEG: all four land on a local minimum of the
# streak profile within one pixel, the deepest being Hgamma at 0.83 of continuum.
LINES_NATIVE = [("Hδ", 2305), ("Hγ", 2441), ("Hβ", 2735), ("Hα", 3693)]


def font(size):
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load(path, rotate=True):
    """Open the frame, optionally turned a quarter turn anticlockwise.

    Portrait costs 2000 px of scroll in the report for a streak that is mostly
    empty sky. Rotating puts the zero order on the left and runs the spectrum
    left to right, blue first — the way a spectrum is normally drawn — and the
    figure then fits the column at a third of the height. The rotation happens
    before detection so the labels are drawn upright rather than turned on
    their side with the image."""
    im = Image.open(path).convert("RGB")
    return im.rotate(90, expand=True) if rotate else im


def blobs(im):
    a = np.asarray(im.convert("L"), dtype=float)
    b = gaussian_filter(a - np.median(a), 2)
    lab, _ = label(b > np.percentile(b, 99.95))
    sizes = np.bincount(lab.ravel()); sizes[0] = 0
    H, W = a.shape
    out = []
    for i in np.argsort(sizes)[::-1][:14]:
        ys, xs = np.nonzero(lab == i)
        w, h = xs.max() - xs.min(), ys.max() - ys.min()
        # Sensor banding runs the full length of the frame and touches an edge.
        # A real feature sits clear of the border and is narrow across.
        if xs.min() < 5 or xs.max() > W - 6 or ys.min() < 5 or ys.max() > H - 6:
            continue
        if min(w, h) > 150:          # thin in its short direction, either way up
            continue
        out.append(dict(x0=xs.min(), x1=xs.max(), y0=ys.min(), y1=ys.max(),
                        span=max(w, h), n=sizes[i]))
    zero = min(out, key=lambda b: b["span"])     # compact blob
    first = max(out, key=lambda b: b["span"])    # long one

    # The bright cut finds only the saturated core of the streak. Re-scan the
    # band it sits in at a lower threshold to reach the full rainbow, which
    # fades out gradually at both the violet and the red end.
    if first["x1"] - first["x0"] >= first["y1"] - first["y0"]:
        band = b[max(0, first["y0"] - 25):first["y1"] + 25, :]
        lit = np.nonzero(band.max(axis=0) > np.percentile(b, 99.0))[0]
        if len(lit):
            first["x0"], first["x1"] = int(lit.min()), int(lit.max())
    else:
        band = b[:, max(0, first["x0"] - 25):first["x1"] + 25]
        lit = np.nonzero(band.max(axis=1) > np.percentile(b, 99.0))[0]
        if len(lit):
            first["y0"], first["y1"] = int(lit.min()), int(lit.max())
    return zero, first


def main(src, dst):
    im = load(src)
    d = ImageDraw.Draw(im)
    f = font(42)
    zero, first = blobs(im)

    cx, cy = (zero["x0"] + zero["x1"]) / 2, (zero["y0"] + zero["y1"]) / 2

    # Everything below is drawn relative to the streak axis rather than to the
    # frame, so the same code works whichever way up the frame is.
    ux = (first["x0"] + first["x1"]) / 2 - cx
    uy = (first["y0"] + first["y1"]) / 2 - cy
    L = (ux ** 2 + uy ** 2) ** 0.5
    ux, uy = ux / L, uy / L
    nx, ny = -uy, ux                       # perpendicular to the streak
    if ny > 0:                             # keep the labelled side "above"
        nx, ny = -nx, -ny

    # The spectrum runs along the LONG side of the sensor whichever way the
    # frame is turned, so the native-pixel scale follows the long edge.
    scale = max(im.width, im.height) / 3840.0

    r = 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.text((cx + nx * 96 - 40, cy + ny * 96 - 26), "m = 0", font=f, fill=INK)

    # Bracket along the far side of the streak, clear of the light itself.
    def at(rr, off):
        return (cx + ux * rr + nx * off, cy + uy * rr + ny * off)

    r0 = LINES_NATIVE[0][1] * scale - 130
    r1 = min(LINES_NATIVE[-1][1] * scale + 130, L + 260)
    b0, b1 = at(r0, -62), at(r1, -62)
    d.line([b0, b1], fill=ACC, width=3)
    d.line([b0, at(r0, -40)], fill=ACC, width=3)
    d.line([b1, at(r1, -40)], fill=ACC, width=3)
    mx, my = at((r0 + r1) / 2, -104)
    tw = d.textlength("m = 1", font=f)
    d.text((mx - tw / 2, my - 26), "m = 1", font=f, fill=ACC)

    # Mark the absorption bands. Positions come from the grating geometry, not
    # from hunting for dips -- which is what makes them checkable.
    f_small = font(34)
    for name, r_native in LINES_NATIVE:
        rr = r_native * scale
        tip = at(rr, 26)
        tail = at(rr, 82)
        if not (0 <= tip[0] < im.width and 0 <= tip[1] < im.height):
            continue
        d.line([tail, at(rr, 38)], fill=BAL, width=3)
        hx, hy = tip
        d.polygon([(hx, hy), (hx - nx * 16 - ux * 7, hy - ny * 16 - uy * 7),
                   (hx - nx * 16 + ux * 7, hy - ny * 16 + uy * 7)], fill=BAL)
        lx, ly = at(rr, 100)
        tw = d.textlength(name, font=f_small)
        # Halpha sits ~80 px from the frame edge, so its label would run off.
        tx = min(max(8, lx - tw / 2), im.width - tw - 8)
        d.text((tx, ly - 22), name, font=f_small, fill=BAL)

    im.save(dst, quality=94)
    print(f"  wrote {dst}  {im.width}x{im.height}  m=0 at ({cx:.0f},{cy:.0f})  streak len {L:.0f}px")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
