#!/usr/bin/env python3
"""Copy the chosen Seestar captures into the project's data/ folder, byte for byte.

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

Only that block is generated — index.md's <style> and the lightbox markup
and script below it are hand-maintained, so paste the output above them.
"""

import os
import re
import shutil

SRC = os.path.expanduser("~/GITHUB/science/work/astronomy/data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Clip that plays large at the top of the page, above the grid.
HERO = ("Solar_video", "2026-07-24-164602-Solar.mp4")

# (folder, filename) or (folder, filename, display_name) — gallery order is
# this order. The third field is needed where the folder name is not the subject.
# Single ``Light_`` subs are as legitimate here as stacks: they are equally
# byte-for-byte what the Seestar wrote. The 2026-07-29 additions are all from
# the night the polar alignment was fixed (10.4 deg -> 0.5 deg), which is why
# 60 s subs became possible at all.
KEEP = [
    # M 31 upgraded 2026-07-30: 25 x 20s reaches the dust lane and M110,
    # where the 17 x 10s it replaces showed little beyond the core.
    ("M 31",     "Stacked_25_M 31_20.0s_IRCUT_20260730-015655.jpg"),
    # M 13 upgraded 2026-07-29: the 5 x 60s stack goes visibly deeper than the
    # 30 x 10s it replaces, because fixing the polar alignment made 60 s subs
    # possible. Same target, better night.
    ("M 13",     "Stacked_5_M 13_60.0s_IRCUT_20260728-225801.jpg"),
    ("M 51",     "Stacked_30_M 51_10.0s_IRCUT_20260704-222846.jpg"),
    ("NGC 5907", "Stacked_9_NGC 5907_10.0s_IRCUT_20260704-223446.jpg"),
    ("Vega",     "Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg"),
    ("Deneb",    "Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg"),
    ("RR Lyrae", "Stacked_21_RR Lyrae_5.0s_IRCUT_20260725-020642.jpg"),
    ("Delta Cygni", "Stacked_54_Delta Cygni_5.0s_IRCUT_20260728-223243.jpg"),
    # Spectroscopy, first light with the Star Analyser 100. Both spectra are VEGA's.
    # The 2 s frame is out of focus -- continuous-capture mode did not inherit the
    # focuser position, so it ran at FOCUSPOS 0 and smeared the spectrum ~60x wider
    # than it should be. Kept deliberately: it is the prettiest frame of the night
    # and an honest picture of what a first attempt looks like. This first one sits in the V530 Lyrae folder only
    # because V530 Lyrae was the custom target used to shift Vega toward the frame
    # edge -- the spectrum starts 2209 px from the zero-order dot, so a centred
    # star throws it off the sensor entirely. The folder records the pointing,
    # not the subject; V530 Lyrae itself is far too faint to show a spectrum.
    ("V530 Lyrae", "Light_V530 Lyrae_2.0s_IRCUT_20260728-232423.jpg", "Vega spectrum"),
    ("Vega",       "Light_Vega_10.0s_LP_20260728-233740.jpg", "Vega spectrum"),
    # 3 Juno: the first and last CLEAN subs of the run, 37.5 min apart, which is
# the widest baseline the night allows. Juno shifts 6.2 px against fixed stars;
# a narrower pair was tried first and showed only 4.1 px.
    ("Juno",       "Light_Juno_20.0s_IRCUT_20260729-000521.jpg", "Juno — before"),
    ("Juno",       "Light_Juno_20.0s_IRCUT_20260729-003012.jpg", "Juno — after"),
    # 2026-07-29/30, the first fully programmatic night -- no phone app in the
    # loop at any point. Both spectra are single subs the on-board stacker
    # REJECTED (``_failed_`` in the name): a deliberately off-centre streak is
    # not a star field, so it throws every frame away. They exist only because
    # ``save_discrete_frame`` keeps the rejects.
    ("Vega",     "Light_Vega_5.0s_IRCUT_failed_20260729-222828.jpg", "Vega spectrum"),
    # Albireo is a colour-contrast double: K3II + B8V. Both components disperse
    # in the same exposure, so the comparison is within-frame -- same optics,
    # same air, same calibration.
    ("Albireo",  "Light_Albireo_20.0s_IRCUT_failed_20260729-225851.jpg", "Albireo — two spectra"),
    # Honest caption: through IRCUT this is a Cygnus star field, not the nebula.
    # NGC 7000 is an H-alpha emission object and barely registers without a
    # narrowband filter.
    ("NGC 7000", "Stacked_20_NGC 7000_20.0s_IRCUT_20260730-014616.jpg", "NGC 7000 field"),
]


def label(folder, fname, name=None):
    """Display name, and how the frame was built: ``21 × 5s``, ``1 × 20s``.

    A single sub is written ``1 × 20s`` rather than "single 20s" so every tile
    reads on the same ``count × exposure`` pattern.
    """
    name = name or folder

    stack = re.match(r"Stacked_(\d+)_.*?_([\d.]+)s_", fname)
    if stack:
        n, exp = stack.groups()
        return name, f"{n} × {exp.rstrip('0').rstrip('.')}s"

    sub = re.match(r"Light_.*?_([\d.]+)s_", fname)
    if sub:
        exp = sub.group(1)
        return name, f"1 × {exp.rstrip('0').rstrip('.')}s"

    return name, ""


def dest_name(folder, fname):
    """Flatten to a URL-friendly name that still identifies the original."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", f"{folder}__{fname}")


def copy(folder, fname):
    dst = dest_name(folder, fname)
    shutil.copyfile(os.path.join(SRC, folder, fname), os.path.join(OUT, dst))
    return dst


def tile_html(folder, fname, dst, name=None):
    name, meta = label(folder, fname, name)
    return (f'  <figure class="sky-tile">\n'
            f'    <a href="data/{dst}"><img src="data/{dst}" alt="{name}" '
            f'loading="lazy"></a>\n'
            f'    <figcaption><b>{name}</b><span>{meta}</span></figcaption>\n'
            f'  </figure>')


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # data/ is generated, so drop anything no longer in HERO/KEEP -- otherwise a
    # swapped-out tile (e.g. M 13's 10 s stack, replaced by the 60 s one) lingers
    # as an orphan that nothing links to.
    wanted = {dest_name(*HERO)} | {dest_name(e[0], e[1]) for e in KEEP}
    for stale in sorted(set(os.listdir(OUT)) - wanted):
        os.remove(os.path.join(OUT, stale))
        print(f"<!-- removed orphan tile: {stale} -->")
    hero = copy(*HERO)
    print(f'<div class="sky-hero">\n'
          f'  <video src="data/{hero}" autoplay loop muted playsinline '
          f'preload="auto"></video>\n</div>\n')
    print('<div class="sky-grid">')
    for entry in KEEP:
        folder, fname = entry[0], entry[1]
        name = entry[2] if len(entry) > 2 else None
        print(tile_html(folder, fname, copy(folder, fname), name))
    print("</div>")
