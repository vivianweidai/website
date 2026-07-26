#!/usr/bin/env python3
"""Copy the chosen Seestar captures into the project's media/ folder, byte for byte.

Deliberately a copy and nothing else — no crop, no stretch, no re-encode, not
even a metadata strip. The gallery shows what the Seestar wrote; anything that
touched the pixels would make the page a processing demo instead of a capture
log.

Sources live in ``work/astronomy/data/`` (gitignored: ~500 MB of FITS + JPEG +
clips). KEEP is the hand-picked shortlist — one frame per target, chosen by eye
from the full set. Widen it by adding rows, not by globbing: the rest of the
folder is duplicates, clouded-out Moon shots and the FITS stacks (huge, and
their headers carry the observing site).

Run:  python3 output/collect_media.py     (prints the hero + tiles for index.md)
"""

import os
import re
import shutil

SRC = os.path.expanduser("~/GITHUB/science/work/astronomy/data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "media")

# Clip that plays large at the top of the page, above the grid.
HERO = ("Solar_video", "2026-07-24-164602-Solar.mp4")

# (folder, filename) — gallery order is this order.
KEEP = [
    ("M 31",     "Stacked_17_M 31_10.0s_IRCUT_20260725-014442.jpg"),
    ("M 13",     "Stacked_30_M 13_10.0s_IRCUT_20260721-215926.jpg"),
    ("M 51",     "Stacked_30_M 51_10.0s_IRCUT_20260704-222846.jpg"),
    ("NGC 5907", "Stacked_9_NGC 5907_10.0s_IRCUT_20260704-223446.jpg"),
    ("Vega",     "Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg"),
    ("Deneb",    "Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg"),
    ("RR Lyrae", "Stacked_21_RR Lyrae_5.0s_IRCUT_20260725-020642.jpg"),
]


def label(folder, fname):
    """Target name, and the stack that produced the frame: ``21 × 5s``."""
    stack = re.match(r"Stacked_(\d+)_.*?_([\d.]+)s_", fname)
    if not stack:
        return folder, ""
    n, exp = stack.groups()
    exp = exp.rstrip("0").rstrip(".")     # 10.0 -> 10
    return folder, f"{n} × {exp}s"


def dest_name(folder, fname):
    """Flatten to a URL-friendly name that still identifies the original."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", f"{folder}__{fname}")


def copy(folder, fname):
    dst = dest_name(folder, fname)
    shutil.copyfile(os.path.join(SRC, folder, fname), os.path.join(OUT, dst))
    return dst


def tile_html(folder, fname, dst):
    name, meta = label(folder, fname)
    return (f'  <figure class="sky-tile">\n'
            f'    <a href="media/{dst}"><img src="media/{dst}" alt="{name}" '
            f'loading="lazy"></a>\n'
            f'    <figcaption><b>{name}</b><span>{meta}</span></figcaption>\n'
            f'  </figure>')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero = copy(*HERO)
    print(f'<div class="sky-hero">\n'
          f'  <video src="media/{hero}" autoplay loop muted playsinline '
          f'preload="auto"></video>\n</div>\n')
    print('<div class="sky-grid">')
    for folder, fname in KEEP:
        print(tile_html(folder, fname, copy(folder, fname)))
    print("</div>")
