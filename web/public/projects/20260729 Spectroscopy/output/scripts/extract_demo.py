#!/usr/bin/env python3
"""Show what "extract the 1-D profile" actually does, and what the width costs.

    ../../../technology/seestar/.venv/bin/python extract_demo.py \
        ../data/Vega/Light_Vega_5.0s_IRCUT_failed_20260729-225258.fit ../output

Extraction is three lines of numpy once the streak is straight:

    strip = rectify(rgb, y0, x0, ux, uy, rs, half_width=w)   # slanted -> horizontal
    strip = strip.sum(axis=2)                                # R+G+B  (debayered first!)
    prof  = strip.sum(axis=0)                                # sum DOWN each column

The last line is the whole idea. Each column of the rectified strip is one
wavelength, so adding a column up collapses the 2-D streak into one number per
wavelength. That is the spectrum.

The only judgement call is `half_width` -- how far either side of the streak's
spine to keep. This script measures the trade instead of asserting it. Too
narrow and you throw away starlight that was really there; too wide and every
extra row adds sky noise but no signal, so the noise grows as sqrt(rows) while
the signal has stopped growing. There is a maximum in between, and it is not
where intuition puts it: the curve is flat-topped, so anything in a broad range
does nearly as well, and being slightly too wide is far cheaper than being
slightly too narrow.

Reuses spectro_annotate.py's geometry rather than re-deriving it -- one
definition of the streak, not two.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectro_annotate import (load_rgb, find_zero_order, centroid_zero_order,
                              measure_angle, rectify, lam_of_r, stretch)


def main():
    path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    rgb, d = load_rgb(path)

    y0, x0 = centroid_zero_order(d, *find_zero_order(d))
    ang = measure_angle(d, y0, x0)
    a = np.deg2rad(ang)
    ux, uy = np.sin(a), np.cos(a)
    H = d.shape[0]
    r_max = min(3760, int((H - y0 - 10) / max(abs(uy), 1e-6)))
    rs = np.arange(2050, r_max)
    lam = lam_of_r(rs)
    print(f"zero order (x,y) = ({x0:.0f},{y0:.0f})  angle {ang:+.2f} deg  "
          f"{lam[0]:.0f}-{lam[-1]:.0f} nm")

    WIDE = 40
    strip = rectify(rgb, y0 / 2, x0 / 2, ux, uy, rs / 2.0, half_width=WIDE)
    mono = strip.sum(axis=2)                       # R+G+B, already debayered
    offs = np.arange(-WIDE, WIDE + 1)

    # The trade-off, measured. Signal = summed flux in the aperture. Noise is
    # taken from rows far off the streak, scaled by sqrt(rows) -- adding a row
    # of pure sky adds variance and no signal.
    spine = mono[WIDE - 2:WIDE + 3].sum(0)
    sky_rows = np.r_[mono[:8], mono[-8:]]
    sky_sigma = float(np.std(sky_rows))
    hw = np.arange(1, WIDE + 1)
    snr, frac = [], []
    total = mono.sum()   # the whole strip, so the fraction cannot exceed 1
    for w in hw:
        sig = mono[WIDE - w:WIDE + w + 1].sum()
        noise = sky_sigma * np.sqrt(2 * w + 1) * np.sqrt(len(rs))
        snr.append(sig / noise)
        frac.append(sig / total)
    snr, frac = np.array(snr), np.array(frac)
    best = int(hw[np.argmax(snr)])
    print(f"  best half-width {best} px   (captures {100*frac[best-1]:.1f}% of the light)")
    for w in (2, 5, 10, 22, 40):
        if w <= WIDE:
            print(f"    hw {w:2d}: {100*frac[w-1]:5.1f}% of flux, SNR {snr[w-1]/snr.max():.2f} of peak")

    fig = plt.figure(figsize=(13.6, 9.4), facecolor="#0d0d0f")
    gs = fig.add_gridspec(3, 2, left=.075, right=.975, top=.845, bottom=.075,
                          hspace=.42, wspace=.2, height_ratios=[1, 1.15, 1.15])

    ax0 = fig.add_subplot(gs[0, :])
    ax0.imshow(stretch(strip), aspect="auto", origin="lower",
               extent=[lam[0], lam[-1], -WIDE, WIDE])
    for s in (-best, best):
        ax0.axhline(s, color="#ffd9a0", lw=1.3, ls="--")
    ax0.set_ylabel("offset from\nspine (px)", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax0.set_title("① the rectified streak — each column is one wavelength",
                  # color="#e8e4dd", fontsize=11.5, pad=7)

    ax1 = fig.add_subplot(gs[1, 0])
    for lo, hi, c, lb in [(430, 440, "#7fb0d0", "434 nm (Hγ)"),
                          (520, 530, "#9ccf8f", "525 nm (continuum)")]:
        sel = (lam > lo) & (lam < hi)
        if sel.sum():
            ax1.plot(offs, mono[:, sel].mean(1), color=c, lw=1.8, label=lb)
    ax1.axvspan(-best, best, color="#ffd9a0", alpha=.13)
    ax1.set_xlabel("offset across the streak (px)", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax1.set_title("② one column, seen side-on — this is what gets summed",
                  # color="#e8e4dd", fontsize=11.5, pad=7)

    ax2 = fig.add_subplot(gs[1, 1])
    ax2.plot(hw, 100 * frac, color="#e8b48c", lw=2, label="% of the light captured")
    ax2.plot(hw, 100 * snr / snr.max(), color="#7fb0d0", lw=2, label="signal-to-noise, % of best")
    ax2.axvline(best, color="#ffd9a0", lw=1.3, ls="--")
    ax2.set_xlabel("half-width kept (px)", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax2.set_title(f"③ the trade — widest is not best (peak at {best} px)",
                  # color="#e8e4dd", fontsize=11.5, pad=7)

    ax3 = fig.add_subplot(gs[2, :])
    for w, c, lb in [(2, "#8a6a55", "half-width 2 px — starved"),
                     (best, "#e8b48c", f"half-width {best} px — the choice"),
                     (WIDE, "#6f7f8c", f"half-width {WIDE} px — noise added, no signal")]:
        p = mono[WIDE - w:WIDE + w + 1].sum(0)
        ax3.plot(lam, p / np.median(p), color=c, lw=1.5, label=lb)
    ax3.set_xlabel("wavelength (nm)", color="#a09a90", fontsize=9.5)
    ax3.set_ylabel("flux / median", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax3.set_title("④ the extracted 1-D profile, at three widths",
                  # color="#e8e4dd", fontsize=11.5, pad=7)

    for ax in (ax0, ax1, ax2, ax3):
        ax.set_facecolor("#131316")
        ax.tick_params(colors="#7a746a", labelsize=8.5)
        for s in ax.spines.values():
            s.set_color("#3a3730")
    for ax in (ax1, ax2, ax3):
        lg = ax.legend(facecolor="#131316", edgecolor="#3a3730", fontsize=8.5)
        for t in lg.get_texts():
            t.set_color("#c8c2b8")

    # header moved to report prose: fig.text(.02, .955, "Extracting the 1-D profile — and what the aperture width costs",
             # color="#f2efe9", fontsize=17, weight="bold")
    # header moved to report prose: fig.text(.02, .916,
             # "prof = strip.sum(axis=2).sum(axis=0)  —  add R+G+B, then sum DOWN each column. "
             # "One 5 s Vega frame.", color="#a09a90", fontsize=10.5,
             # family="monospace")
    # header moved to report prose: fig.text(.02, .886,
             # f"Widest is not best: at {WIDE} px the aperture holds {100*frac[-1]:.0f}% of the light "
             # f"but only {100*snr[-1]/snr.max():.0f}% of the achievable signal-to-noise, because "
             # f"every extra row past the star adds sky and no star.",
             # color="#c9a389", fontsize=10.5, style="italic")

    out = os.path.join(outdir, "20260801 extraction demo.png")
    fig.savefig(out, dpi=110, facecolor=fig.get_facecolor())
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
