#!/usr/bin/env python3
"""Show where A comes from: measure r for each Balmer line, then fit.

    ../../../technology/seestar/.venv/bin/python fit_A_demo.py \
        ../data/Vega/Light_Vega_5.0s_IRCUT_failed_20260729-225258.fit ../output

A is not derived from the spec sheet and not computed from anything -- it is
FITTED to four measurements we make on our own frame. The measurement is exactly
what it sounds like: the distance in pixels from the zero-order dot to each dark
Balmer line, along the streak.

    r_measured   <- read off the image, per line
    r_predicted  =  A * tan(asin(lambda / 10000 nm))
    A            <- least squares, minimising sum (r_measured - r_predicted)^2

Four measurements, one unknown. Three degrees of freedom left over, and those
leftovers ARE the check -- if the model were wrong, no single A could put all
four lines in the right place at once, and the residuals would fan out with
wavelength instead of scattering around zero.

Note which numbers are which. lambda is a constant of nature (410.17, 434.05,
486.13, 656.28 nm -- hydrogen's n=6,5,4,3 -> 2 transitions). r is ours, and it
moves every time the barrel is re-threaded. The fit is what ties one to the
other, and it has to be redone every mounting.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d, median_filter
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectro_annotate import (LINES, load_rgb, find_zero_order, centroid_zero_order,
                              measure_angle, rectify, lam_of_r)

NICE = {"H$\\delta$": "Hδ", "H$\\gamma$": "Hγ", "H$\\beta$": "Hβ", "H$\\alpha$": "Hα"}


def main():
    path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "."
    rgb, d = load_rgb(path)

    y0, x0 = centroid_zero_order(d, *find_zero_order(d))
    ang = measure_angle(d, y0, x0)
    a = np.deg2rad(ang)
    ux, uy = np.sin(a), np.cos(a)
    H, W = d.shape
    r_max = min(3760, int((H - y0 - 10) / max(abs(uy), 1e-6)))
    rs = np.arange(2050, r_max)

    strip = rectify(rgb, y0 / 2, x0 / 2, ux, uy, rs / 2.0)
    sm = gaussian_filter1d(strip.sum(2).sum(0), 4)
    lam_nom = lam_of_r(rs)
    dl = float(lam_nom[1] - lam_nom[0])
    win = int(36.0 / ((lam_nom[-1] - lam_nom[0]) / len(lam_nom))) | 1
    norm = sm / np.clip(median_filter(sm, win), 1, None)

    def rows(A):
        out = []
        for nm, L in LINES:
            rp = A * np.tan(np.arcsin(L / 10000.0))
            w = np.abs(rs - rp) < 90
            if w.sum() >= 5:
                out.append((NICE.get(nm, nm), L, int(rs[np.argmin(np.where(w, norm, 9))]), rp))
        return out

    A = float(least_squares(lambda p: [m - q for _, _, m, q in rows(p[0])] or [0.0],
                            [55181.0]).x[0])
    tab = rows(A)
    res_nm = np.array([(m - q) * dl for _, _, m, q in tab])
    print(f"zero order (x,y) = ({x0:.1f},{y0:.1f})   streak {ang:+.2f} deg")
    print(f"FITTED A = {A:.0f} px  ->  grating-to-sensor {A*2.9e-3:.1f} mm")
    for (nm, L, m, q), rn in zip(tab, res_nm):
        print(f"  {nm:4s} {L:7.2f} nm   r measured {m:5d} px   predicted {q:7.1f}   {rn:+.3f} nm")
    print(f"  rms {np.sqrt((res_nm**2).mean()):.3f} nm")

    # ---- figure -------------------------------------------------------------
    B = 4
    img = d[:H // B * B, :W // B * B].reshape(H // B, B, W // B, B).mean((1, 3))
    lo, hi = np.percentile(img, 40), np.percentile(img, 99.93)
    shown = np.clip((img - lo) / (hi - lo), 0, None)
    shown = np.arcsinh(shown * 30) / np.arcsinh(30)

    fig = plt.figure(figsize=(13.4, 8.6), facecolor="#0d0d0f")
    gs = fig.add_gridspec(2, 2, left=.045, right=.975, top=.855, bottom=.075,
                          wspace=.16, hspace=.34, width_ratios=[1, 1.55])

    ax = fig.add_subplot(gs[:, 0])
    ax.imshow(np.clip(shown, 0, 1), cmap="gray", origin="upper", vmin=0, vmax=1)
    ax.plot([x0 / B, (x0 + ux * rs[-1]) / B], [y0 / B, (y0 + uy * rs[-1]) / B],
            color="#7fb0d0", lw=.9, alpha=.65)
    ax.plot(x0 / B, y0 / B, "o", mfc="none", mec="#ffd9a0", ms=13, mew=1.8)
    for nm, L, m, q in tab:
        px, py = (x0 + ux * m) / B, (y0 + uy * m) / B
        ax.plot([px - 26, px - 9], [py, py], color="#e8b48c", lw=1.6)
        ax.text(px - 32, py, nm, color="#e8b48c", fontsize=9.5,
                ha="right", va="center")
    ax.set_xlim(0, W / B); ax.set_ylim(H / B, 0)
    ax.set_xticks([]); ax.set_yticks([])
    # no in-figure title: ax.set_title("① measure r from the dot to each line", color="#e8e4dd", fontsize=11.5, pad=8)

    ax2 = fig.add_subplot(gs[0, 1])
    lamgrid = np.linspace(380, 700, 400)
    ax2.plot(lamgrid, A * np.tan(np.arcsin(lamgrid / 10000.0)), color="#7fb0d0", lw=1.8)
    ax2.plot([t[1] for t in tab], [t[2] for t in tab], "o", color="#e8b48c", ms=8)
    for nm, L, m, q in tab:
        ax2.annotate(nm, (L, m), (L + 8, m - 105), color="#c8c2b8", fontsize=9)
    ax2.set_ylabel("r from zero order (px)", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax2.set_title("② one curve, one free parameter, four points", color="#e8e4dd",
                  # fontsize=11.5, pad=8)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axhline(0, color="#3a3730", lw=1)
    ax3.plot([t[1] for t in tab], res_nm, "o", color="#e8b48c", ms=8)
    ax3.set_ylim(-.45, .45)
    ax3.set_xlabel("wavelength (nm)", color="#a09a90", fontsize=9.5)
    ax3.set_ylabel("measured − predicted (nm)", color="#a09a90", fontsize=9.5)
    # no in-figure title: ax3.set_title(f"③ what is left over — rms {np.sqrt((res_nm**2).mean()):.3f} nm, "
                  # f"scattered not sloped", color="#e8e4dd", fontsize=11.5, pad=8)

    for a_ in (ax2, ax3):
        a_.set_facecolor("#131316")
        a_.tick_params(colors="#7a746a", labelsize=8.5)
        for s in a_.spines.values():
            s.set_color("#3a3730")
        if a_.get_legend_handles_labels()[0]:
            lg = a_.legend(facecolor="#131316", edgecolor="#3a3730", fontsize=8.5)
            for t in lg.get_texts():
                t.set_color("#c8c2b8")
    for s in ax.spines.values():
        s.set_color("#3a3730")

    # header moved to report prose: fig.text(.02, .958, "Where A comes from — it is fitted to our own pixels, not looked up",
             # color="#f2efe9", fontsize=17, weight="bold")
    # header moved to report prose: fig.text(.02, .922,
             # "λ is a constant of nature; r is a property of this mounting. The fit ties one to the "
             # "other, and must be redone every time the barrel is re-threaded.",
             # color="#a09a90", fontsize=10.5)
    # header moved to report prose: fig.text(.02, .893,
             # f"Four measurements, one unknown — so three are spare, and they are the test: "
             # f"a wrong model could not place all four within {np.abs(res_nm).max():.2f} nm at once.",
             # color="#c9a389", fontsize=10.5, style="italic")

    out = os.path.join(outdir, "20260801 fitting A.png")
    fig.savefig(out, dpi=110, facecolor=fig.get_facecolor())
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
