#!/usr/bin/env python3
"""Copy the chosen microscope captures into the project's data/ folder.

Same principle as the Stargazing gallery: a copy, byte for byte, so the page
shows what the camera wrote rather than what a processing step made of it.

ONE exception, and it is documented per-file below. The 2026-07-01 frame is a
macOS *window screenshot*, not a camera capture -- the specimen sits inside a
viewer window with desktop wallpaper all around it. That wallpaper is not data,
so the window is cropped out. Nothing inside the window is touched: no resize,
no stretch, no colour change. If the original capture ever turns up, replace it
and drop the crop.

Sources live in ``work/biology/data/``. KEEP is a hand-picked list -- widen it
by adding rows rather than globbing, so the gallery stays curated.

Run:  python3 output/collect_media.py     (prints the tile block for index.md)

Only that block is generated; index.md's <style>, lightbox markup and script
are hand-maintained, so paste the output above them.
"""

import os
import shutil

SRC = os.path.expanduser("~/GITHUB/science/work/biology/data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# HERO is the wide band at the top of the page. It carries no caption, so it
# needs no name/meta -- just the slug and whether it must be cropped.
HERO = ("Screenshot 2026-07-01 microscope.jpeg", "reticulate-specimen.jpg", True)

# (source filename, output slug, caption, sub-caption, crop_window) -- gallery
# order is this order.
#
# Captions describe what is visible, not a confident identification -- these are
# teaching slides whose labels were not recorded with the captures. Correct them
# here when the slide names are known; the page reads them from this table.
KEEP = [
    ("TS-20250307151924476.jpeg", "leaf-epidermis.jpg",
     "Leaf epidermis", "peel · stomata", False),
    ("TS-20250305001552414.jpeg", "tissue-section.jpg",
     "Tissue", "lobules · septa", False),
]


def crop_window(src, dst):
    """Crop a macOS window screenshot down to the window's content.

    The desktop wallpaper behind the window is strongly blue; the specimen is
    not. Threshold on `blue - max(red, green)`, take the rows and columns that
    are mostly window, and inset past the rounded corners and border.
    """
    from PIL import Image
    import numpy as np

    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(int)
    blue = a[..., 2] - np.maximum(a[..., 0], a[..., 1])
    win = blue < 25
    rows = np.where(win.mean(axis=1) > 0.6)[0]
    cols = np.where(win.mean(axis=0) > 0.6)[0]
    pad = 14
    box = (cols.min() + pad, rows.min() + pad, cols.max() - pad, rows.max() - pad)
    im.crop(box).save(dst, quality=95, subsampling=0)
    return box


def main():
    os.makedirs(OUT, exist_ok=True)

    hsrc, hslug, hcrop = HERO
    hpath = os.path.join(SRC, hsrc)
    if os.path.exists(hpath):
        if hcrop:
            print(f"  cropped {hsrc} -> {hslug}  box={crop_window(hpath, os.path.join(OUT, hslug))}  [hero]")
        else:
            shutil.copy2(hpath, os.path.join(OUT, hslug))
            print(f"  copied  {hsrc} -> {hslug}  [hero]")

    tiles = []
    for fname, slug, name, meta, do_crop in KEEP:
        src = os.path.join(SRC, fname)
        dst = os.path.join(OUT, slug)
        if not os.path.exists(src):
            print(f"  MISSING {fname}")
            continue
        if do_crop:
            box = crop_window(src, dst)
            print(f"  cropped {fname} -> {slug}  box={box}")
        else:
            shutil.copy2(src, dst)
            print(f"  copied  {fname} -> {slug}")
        tiles.append((slug, name, meta))

    print("\n--- paste into index.md above the <style> block ---\n")
    print('<div class="cell-hero">')
    print(f'  <img src="data/{hslug}" alt="">')
    print('</div>\n')
    print('<div class="cell-grid">')
    for slug, name, meta in tiles:
        print('  <figure class="cell-tile">')
        print(f'    <a href="data/{slug}"><img src="data/{slug}" alt="{name}" loading="lazy"></a>')
        print(f'    <figcaption><b>{name}</b><span>{meta}</span></figcaption>')
        print('  </figure>')
    print('</div>')


if __name__ == "__main__":
    main()
