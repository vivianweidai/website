#!/usr/bin/env python3
"""Build the Stargazing gallery assets from the local Seestar captures.

Source frames live in ``work/astronomy/data/`` (Seestar S30 Pro exports —
gigabytes of FITS + full-res JPEG, gitignored and local-only). This script
turns a hand-picked subset into the small, portrait-cropped, EXIF-free JPEGs
served under the project's ``media/`` folder.

Per image it does three things:
  1. centre-crop by a per-target zoom factor (the Seestar plate-solves the
     target to frame centre, so a centred crop is the right crop),
  2. optionally stretch — a background-subtracted asinh curve that lifts faint
     galaxy/cluster light without blowing out the stars,
  3. resize to 9:16 and re-encode as a stripped JPEG.

Videos are transcoded separately with macOS ``avconvert`` (see VIDEOS below) —
it downsizes 2160x3840 to 1080x1920 and drops privacy-sensitive metadata.

Run:  python3 output/build_gallery.py        (needs pillow + numpy)
"""

import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

# Seestar exports are gitignored and local-only; adjust if the tree moves.
SRC = os.path.expanduser("~/GITHUB/science/work/astronomy/data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media")

# One entry per gallery tile.
#   zoom     fraction of the frame kept (the Seestar centres its target, so the
#            crop is centred unless dx/dy nudge it)
#   dx, dy   crop-centre offset, in fractions of the full frame
#   k        black point, in MADs above the sky median — raise it to bury the
#            noise of a short stack
#   s        asinh strength; 0 disables the stretch entirely (the Sun)
#   flat     subtract a sky-gradient model first (small targets only)
#   neutral  per-channel black point — cancels the orange of city light, at the
#            cost of some real star colour
IMAGES = [
    dict(name="sun-sunspots", src="Solar_photo/2026-07-24-164552-Solar.jpg", zoom=1.00),
    dict(name="sun-haze",     src="Solar_photo/2026-07-01-154746-Solar.jpg", zoom=1.00),
    dict(name="m31",     src="M 31/Stacked_17_M 31_10.0s_IRCUT_20260725-014442.jpg",
         zoom=0.58, k=1.5, s=8),
    dict(name="m13",     src="M 13/Stacked_30_M 13_10.0s_IRCUT_20260721-215926.jpg",
         zoom=0.24, k=3.0, s=6, flat=True, neutral=True),
    # M 51 and NGC 5907 were shot the same nights but stay out of the gallery:
    # 300 s and 90 s from a lit back yard leave both as smudges a few pixels
    # across, and no amount of stretching makes them read at tile size.
    dict(name="vega",    src="Vega/Stacked_24_Vega_10.0s_IRCUT_20260725-012737.jpg",
         zoom=0.80, k=1.5, s=6, flat=True),
    dict(name="deneb",   src="Deneb/Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg",
         zoom=0.80, k=1.5, s=6, flat=True),
    # 0.72 rather than 0.80: the wider crop catches the diagonal seam where a
    # 425-frame stack runs out of overlap.
    dict(name="rr-lyrae", src="RR Lyrae/Stacked_425_RR Lyrae_5.0s_IRCUT_20260725-074035.jpg",
         zoom=0.72, k=1.5, s=6, flat=True),
]

# name, source file — transcoded down to 1080p-class H.264 for autoplay loops.
# The Seestar writes a sibling *_thn.jpg per clip; it becomes the <video poster>.
VIDEOS = [
    ("sun-loop",   "Solar_video/2026-07-24-164602-Solar.mp4"),
    ("sun-clouds", "Solar_video/2026-07-01-154827-Solar.mp4"),
]

MAX_W = 1080          # gallery tiles never render wider than this
JPEG_QUALITY = 86


def flatten(arr, block=64, pct=25):
    """Subtract a smooth sky-background model — the city glow gradient that
    slopes across a back-yard frame.

    The model is a percentile-downsample (each block's 25th percentile rejects
    stars, so only sky is fitted) blown back up with bicubic interpolation.
    Only safe when the target is small compared with the block size; a galaxy
    that fills the frame would be eaten by its own background model.
    """
    h, w, _ = arr.shape
    bh, bw = h // block, w // block
    tiles = arr[: bh * block, : bw * block].reshape(bh, block, bw, block, 3)
    model = np.percentile(tiles, pct, axis=(1, 3))

    full = np.asarray(
        Image.fromarray(np.clip(model, 0, 255).astype(np.uint8)).resize(
            (w, h), Image.BICUBIC
        ),
        dtype=np.float64,
    )
    return arr - full + np.median(full, axis=(0, 1))


def stretch(arr, k, strength, neutral=True):
    """Background-subtracted asinh stretch. Keeps colour, lifts faint signal.

    The sky background dominates the histogram, so the black point is set from
    the median (plus a MAD margin, which keeps the sky dark instead of lifting
    single-pixel noise into a grey haze) rather than from the minimum. A single
    shared white point preserves star colour.

    ``neutral`` picks a per-channel black point, which cancels the orange cast
    of city light. Skip it on frames already run through ``flatten`` — a second
    colour correction there drains real star colour (Vega goes from blue-white
    to butter).
    """
    lum = arr.mean(axis=2)
    bg = np.median(lum)
    mad = np.median(np.abs(lum - bg)) or 1.0
    black = (np.array([np.median(arr[:, :, c]) for c in range(3)])
             if neutral else bg) + k * mad
    white = np.percentile(lum, 99.9) - bg + 1.0

    x = np.clip((arr - black) / white, 0, None)
    out = np.arcsinh(strength * x) / np.arcsinh(strength)
    return np.clip(out, 0, 1) * 255.0


def denoise_chroma(im, radius):
    """Blur only the colour channels — kills the confetti of chroma noise a
    short stack leaves behind, while stars and galaxy detail (luminance) stay
    sharp."""
    y, cb, cr = im.convert("YCbCr").split()
    blur = ImageFilter.GaussianBlur(radius)
    return Image.merge("YCbCr", (y, cb.filter(blur), cr.filter(blur))).convert("RGB")


def build_image(name, src, zoom, dx=0.0, dy=0.0, k=1.5, s=0, flat=False, neutral=None):
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    w, h = im.size

    cw, ch = int(w * zoom), int(h * zoom)
    left = round((w - cw) / 2 + dx * w)
    top = round((h - ch) / 2 + dy * h)
    im = im.crop((left, top, left + cw, top + ch))

    if s:
        arr = np.asarray(im, dtype=np.float64)
        if flat:
            arr = flatten(arr)
        # Default: neutralise unless flatten() already did the colour work.
        n = (not flat) if neutral is None else neutral
        im = Image.fromarray(stretch(arr, k, s, neutral=n).astype(np.uint8))
        # Floor of 2 px: on a hard crop the frame is small but the red-channel
        # speckle is not, so a width-scaled radius alone leaves it visible.
        im = denoise_chroma(im, max(2.0, im.width / 400))

    # Stretched frames are downsampled below their native crop as well: at 0.7
    # scale the LANCZOS average visibly smooths the shot noise a 5-minute stack
    # still carries, and the tiles never render near full width anyway.
    target = min(MAX_W, round(im.width * (0.7 if s else 1.0)))
    if im.width != target:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)

    dst = os.path.join(OUT, name + ".jpg")
    im.save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    print(f"{name:12s} {im.width}x{im.height}  {os.path.getsize(dst)/1024:6.0f} KB")


def build_video(name, rel):
    src = os.path.join(SRC, rel)
    dst = os.path.join(OUT, name + ".mp4")
    subprocess.run(
        ["avconvert", "--source", src, "--output", dst,
         "--preset", "Preset1920x1080", "--replace"],
        check=True, stdout=subprocess.DEVNULL,
    )

    thumb = os.path.join(SRC, rel.replace(".mp4", "_thn.jpg"))
    poster = Image.open(thumb).convert("RGB")
    poster.save(os.path.join(OUT, name + "-poster.jpg"), "JPEG", quality=82, optimize=True)
    print(f"{name:12s} video          {os.path.getsize(dst)/1024:6.0f} KB")


if __name__ == "__main__":
    if not os.path.isdir(SRC):
        sys.exit(f"source captures not found: {SRC}")
    os.makedirs(OUT, exist_ok=True)
    for spec in IMAGES:
        build_image(**spec)
    for row in VIDEOS:
        build_video(*row)
