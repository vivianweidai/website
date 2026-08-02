#!/usr/bin/env python3
"""Figures for the individual steps of the explanation document.

    ../../../technology/seestar/.venv/bin/python step_figures.py ../output

Each one shows a MEASUREMENT on real data rather than asserting a number in
prose. One script rather than five, because they share the same frame, the same
geometry and the same stretch.

  seeing   step 3  -- the star's image profile, which IS the resolution element
  filter   step 5  -- what the dual-band LP filter does to a spectrum
  bayer    step 7  -- the mosaic, and the ripple it puts in an un-debayered trace
  contin   step 10 -- the continuum fit, and the 477 nm step that breaks it
  ew       step 11 -- equivalent width as an area, and its convergence
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import gaussian_filter1d, median_filter, maximum_filter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectro_annotate import (load_rgb, find_zero_order, centroid_zero_order,
                              measure_angle, rectify, lam_of_r)

FRAME = "../data/Vega/Light_Vega_5.0s_IRCUT_failed_20260729-225258.fit"
LPFRAME = "../data/Vega/Light_Vega_10.0s_LP_20260728-233718.fit"
# Step 5 uses the Seestar's own COLOUR renders rather than the FITS. The point of that
# figure is which wavelengths survive the filter, and colour IS wavelength here -- a
# grey stretch throws away the one variable being demonstrated.
LP_JPG = "../output/20260728 Vega through LP.jpg"
IR_JPG = "../output/20260729 Vega through IRCUT.jpg"
# The PSF CANNOT be measured on a grating frame: with an objective grating every
# star in the field is a streak, so "bright peaks" are spectrum segments, not
# point sources. Measuring them gave a nonsense 13 px / 47.7". Use a plain frame.
PLAIN = "/Users/jamesdai/GITHUB/science/technology/seestar/data/RR Lyrae/Light_RR Lyrae_5.0s_IRCUT_20260725-020557.fit"
NPZ = "../output/20260729 spectroscopy results.npz"
PX_NATIVE = 3.669          # arcsec/px, unbinned (SEESTAR.md)
LINES = [("Hδ", 410.174), ("Hγ", 434.047), ("Hβ", 486.135), ("Hα", 656.281)]

INK, MUT, ACC, BLU, PANEL, BG = "#e8e4dd", "#a09a90", "#e8b48c", "#7fb0d0", "#131316", "#0d0d0f"


def dress(ax, xlabel=None, ylabel=None, title=None):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors="#7a746a", labelsize=8.5)
    for s in ax.spines.values():
        s.set_color("#3a3730")
    if xlabel: ax.set_xlabel(xlabel, color=MUT, fontsize=9.5)
    if ylabel: ax.set_ylabel(ylabel, color=MUT, fontsize=9.5)
    # Panel titles are deliberately dropped: the report's prose names each panel.
    # Text baked into a figure competes with the paragraph beside it and drifts
    # out of step with it. Kept: axis labels and ticks, which are the graph.
    _ = title
    if ax.get_legend_handles_labels()[0]:
        lg = ax.legend(facecolor=PANEL, edgecolor="#3a3730", fontsize=8.5)
        for t in lg.get_texts():
            t.set_color("#c8c2b8")


def head(fig, title, *lines):
    """No-op. Figure titles and standfirsts now live in the report prose.

    Call sites keep their text so the intent of each figure stays readable in
    the source; nothing is drawn. Because no header space is needed, each
    gridspec runs to the top of the canvas."""
    return


# ---------------------------------------------------------------- step 3
def fig_seeing(outdir):
    """The star's own image profile. Measured on field stars, not asserted."""
    raw = fits.getdata(PLAIN).astype(np.float32)
    raw -= np.median(raw)
    # Bin 2x2 FIRST. Measuring a PSF on the raw mosaic samples alternating colour
    # filters and stamps the Bayer checkerboard straight into the profile -- the
    # very mistake step 7 is about. One binned px = 2 native px.
    h, w = raw.shape[0] // 2 * 2, raw.shape[1] // 2 * 2
    d = raw[:h, :w].reshape(h // 2, 2, w // 2, 2).sum((1, 3))
    mx = maximum_filter(d, 9)
    ys, xs = np.nonzero((d == mx) & (d > 1200) & (d < 200000))   # unsaturated only
    keep = (ys > 30) & (ys < d.shape[0] - 30) & (xs > 30) & (xs < d.shape[1] - 30)
    ys, xs = ys[keep][:400], xs[keep][:400]

    R = 12
    stack, fwhm = [], []
    for y, x in zip(ys, xs):
        cut = d[y - R:y + R + 1, x - R:x + R + 1]
        if cut.shape != (2 * R + 1, 2 * R + 1) or cut.max() <= 0:
            continue
        cut = cut / cut.max()
        stack.append(cut)
        row = cut[R]
        above = np.nonzero(row > 0.5)[0]
        if len(above):
            fwhm.append(above.max() - above.min() + 1)
    stack = np.array(stack)
    prof = stack.mean(0)[R]
    fwhm = np.array(fwhm)
    med = float(np.median(fwhm)) * 2.0          # binned px -> native px
    print(f"[seeing] {len(stack)} field stars, FWHM median {med:.1f} native px "
          f"= {med*PX_NATIVE:.1f}\" at {PX_NATIVE}\"/px")

    fig = plt.figure(figsize=(14.6, 5.4), facecolor=BG)
    gs = fig.add_gridspec(1, 3, left=.05, right=.982, top=.94, bottom=.135, wspace=.26)

    ax = fig.add_subplot(gs[0])
    ax.imshow(np.arcsinh(stack.mean(0) * 12), cmap="magma", origin="lower",
              extent=[-R, R, -R, R])
    ax.set_xticks([-10, 0, 10]); ax.set_yticks([-10, 0, 10])
    dress(ax, "binned px", "binned px", f"① {len(stack)} field stars, averaged")

    ax = fig.add_subplot(gs[1])
    off = np.arange(-R, R + 1)
    ax.plot(off, prof, color=ACC, lw=2)
    ax.axhline(.5, color=BLU, ls="--", lw=1.2)
    ax.annotate("", (-med / 4, .5), (med / 4, .5),
                arrowprops=dict(arrowstyle="<->", color=BLU, lw=1.4))
    dress(ax, "offset from centre (px)", "peak-normalised", "② full width at half maximum")

    ax = fig.add_subplot(gs[2])
    ax.hist(np.array(fwhm) * 2, bins=np.arange(0, 13), color=ACC, alpha=.85)
    ax.axvline(med, color=BLU, lw=1.5, ls="--")
    dress(ax, "FWHM (native px)", "stars", "③ every star alike — it is the optics, not them")

    head(fig, "The resolution element, measured",
         (f"Every unsaturated star has the same {med:.1f}-native-px profile "
          f"({med*PX_NATIVE:.0f}″ at {PX_NATIVE}″/px) — the width that smears one wavelength "
          f"into the next.", MUT),
         (f"Note how large: {med*PX_NATIVE:.0f}″ against 2-4″ of typical atmospheric seeing. "
          f"Our blur is not the sky — it is optics, focus and tracking.", "#c9a389"))
    p = os.path.join(outdir, "20260801 seeing profile.png")
    fig.savefig(p, dpi=110, facecolor=BG); print("  wrote", p)


# ---------------------------------------------------------------- step 5
def fig_filter(outdir):
    """LP versus IRCUT, shown in colour, because here colour IS the measurement."""
    def prep(path, binf=4, nb=32):
        """Downsample the JPEG and stretch it WITHOUT desaturating it."""
        from PIL import Image
        from scipy.ndimage import zoom
        d = np.asarray(Image.open(os.path.join(os.path.dirname(__file__), path)),
                       dtype=np.float32)[..., :3] / 255.0
        h, w = d.shape[0] // binf * binf, d.shape[1] // binf * binf
        d = d[:h, :w].reshape(h // binf, binf, w // binf, binf, 3).mean((1, 3))

        # Skyglow model: block medians on an nb-px grid, splined back up. A single
        # global median is not enough -- the LP frame has a strong red gradient toward
        # the horizon, and subtracting a constant leaves half the panel glowing red.
        H, W, _ = d.shape
        ch, cw = H // nb, W // nb
        coarse = np.median(d[:ch * nb, :cw * nb].reshape(ch, nb, cw, nb, 3), axis=(1, 3))
        d = d - np.dstack([zoom(coarse[..., c], (H / ch, W / cw), order=1) for c in range(3)])

        # Stretch the LUMINANCE and rescale the triplet by the same factor. Stretching
        # the three channels independently is what greys a spectrum out: it lifts the
        # weak channels fastest and drives every bright pixel toward white. Scaling the
        # triplet instead means even a clipped pixel keeps its hue at full saturation,
        # which is what lets the white point sit low enough to show the faint trails.
        lum = d.max(2)
        # Black point from the noise itself (median + 3 sigma via MAD), not a fixed
        # percentile -- the two frames differ in exposure and in skyglow, so any single
        # percentile leaves one of them either milky or amputated.
        med = np.median(lum)
        blk = med + 3 * 1.4826 * np.median(np.abs(lum - med))
        y = np.clip((lum - blk) / (np.percentile(lum, 99.5) - blk), 0, None)
        g = np.minimum(np.arcsinh(y * 6) / np.arcsinh(6), 1)
        return np.clip(d * (g / np.maximum(lum, 1e-6))[..., None], 0, 1)

    def show(ax, img, title):
        ax.imshow(img, origin="upper")
        ax.set_xticks([]); ax.set_yticks([])
        dress(ax, title=title)

    # NOTE: a "longest bright trail" statistic was tried here and abandoned -- on these
    # frames it latches onto satellite trails and reported the LP streak as LONGER than
    # the IRCUT one, which is backwards. The comparison below is visual plus the
    # passband schematic; the quantitative version is the 208 px / 483-520 nm frame
    # already recorded in SPECTROSCOPY.md.
    print("[filter] visual comparison only -- see docstring note on the abandoned metric")

    fig = plt.figure(figsize=(12.4, 7.4), facecolor=BG)
    gs = fig.add_gridspec(1, 3, left=.03, right=.975, top=.95, bottom=.06,
                          wspace=.16, width_ratios=[1, 1, 1.25])
    show(fig.add_subplot(gs[0]), prep(LP_JPG), "① LP — cyan stubs only, no red, no blue")
    show(fig.add_subplot(gs[1]), prep(IR_JPG), "② IRCUT — violet through red, unbroken")

    ax = fig.add_subplot(gs[2])
    span = np.arange(2050, 3900)
    lam = lam_of_r(span)
    ax.axvspan(483, 520, color=BLU, alpha=.35)
    ax.axvspan(650, 663, color=BLU, alpha=.35)
    ax.axvspan(400, 700, color=ACC, alpha=.10)
    ax.set_xlim(380, 720); ax.set_yticks([])
    dress(ax, "wavelength (nm)", None, "③ why: LP passes two slivers, IRCUT a band")

    head(fig, "What the LP filter does to a spectrum",
         ("Same scope, same star, same grating — only the filter differs. Every trail in ① is a "
          "stub because the filter deleted the wavelengths in between.", MUT),
         ("2026-07-28 through LP: a 208 px streak spanning exactly 483-520 nm — the Hβ/OIII "
          "window — while its Hα window fell 153 px off the sensor.", "#c9a389"))
    p = os.path.join(outdir, "20260801 filter comparison.png")
    fig.savefig(p, dpi=110, facecolor=BG); print("  wrote", p)


# ---------------------------------------------------------------- step 7
def fig_bayer(outdir):
    """The mosaic itself, and the ripple it leaves if you ignore it."""
    raw = fits.getdata(FRAME).astype(np.float32)
    raw -= np.median(raw)
    rgb, d = load_rgb(FRAME)
    y0, x0 = centroid_zero_order(d, *find_zero_order(d))
    ang = measure_angle(d, y0, x0)
    a = np.deg2rad(ang); ux, uy = np.sin(a), np.cos(a)
    r_max = min(3760, int((d.shape[0] - y0 - 10) / max(abs(uy), 1e-6)))
    rs = np.arange(2050, r_max)
    lam = lam_of_r(rs)

    strip = rectify(rgb, y0 / 2, x0 / 2, ux, uy, rs / 2.0, half_width=8)
    good = strip.sum(2).sum(0)

    # The wrong way: one box straight across the raw mosaic, no debayering.
    t = np.arange(-16, 17)
    xs = (x0 + ux * rs[:, None] + uy * t[None, :]).astype(int)
    ys = (y0 + uy * rs[:, None] - ux * t[None, :]).astype(int)
    np.clip(xs, 0, raw.shape[1] - 1, out=xs); np.clip(ys, 0, raw.shape[0] - 1, out=ys)
    bad = raw[ys, xs].sum(1)

    def ripple(p):
        w = (lam > 600) & (lam < 645)                      # line-free window
        q = p[w] / np.clip(median_filter(p[w], 61), 1, None)
        return float(np.std(q))

    r_bad, r_good = ripple(bad), ripple(good)
    print(f"[bayer] ripple raw-mosaic {r_bad:.4f} -> debayered {r_good:.4f}")

    fig = plt.figure(figsize=(13.2, 5.6), facecolor=BG)
    gs = fig.add_gridspec(1, 2, left=.05, right=.978, top=.94, bottom=.13,
                          wspace=.16, width_ratios=[.85, 1.6])

    ax = fig.add_subplot(gs[0])
    yy, xx = int(y0 + uy * 2600), int(x0 + ux * 2600)
    patch = raw[yy - 10:yy + 10, xx - 10:xx + 10]
    ax.imshow(patch, cmap="gray", interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    dress(ax, title="① the raw mosaic, 20×20 px — the checkerboard IS the filters")

    ax = fig.add_subplot(gs[1])
    w = (lam > 600) & (lam < 645)
    for p, c in [(bad, "#8a7f95"), (good, ACC)]:
        q = p[w] / np.clip(median_filter(p[w], 61), 1, None)
        ax.plot(lam[w], q, color=c, lw=1.3)
    dress(ax, "wavelength (nm)", "flux / local median",
          "② a line-free window — everything here should be flat")

    head(fig, "Why debayer first",
         ("Each pixel sits under one colour filter, so a box drawn on the raw mosaic averages "
          "three different throughputs — and the mix shifts as the streak drifts across the grid.", MUT),
         (f"Measured in a line-free window: ripple {r_bad:.3f} → {r_good:.3f}. "
          f"None of that wobble is the star.", "#c9a389"))
    p = os.path.join(outdir, "20260801 bayer ripple.png")
    fig.savefig(p, dpi=110, facecolor=BG); print("  wrote", p)


# ---------------------------------------------------------------- steps 10-11
def fig_continuum_ew(outdir):
    """Normalisation, the 477 nm step, and EW as an area that converges."""
    z = np.load(NPZ)
    lam, f = z["grid"], z["vega"]

    fig = plt.figure(figsize=(13.2, 8.8), facecolor=BG)
    gs = fig.add_gridspec(2, 2, left=.06, right=.978, top=.95, bottom=.07,
                          hspace=.36, wspace=.19)

    ax = fig.add_subplot(gs[0, :])
    ax.plot(lam, f, color="#cfc8bd", lw=1.1)
    ax.axhline(1, color=BLU, lw=1.2, ls="--")
    for nm, L in LINES:
        ax.axvline(L, color=ACC, lw=.9, ls=":")
        ax.text(L, 1.52, nm, color=ACC, fontsize=9, ha="center")
    ax.axvspan(470, 495, color="#b05a4a", alpha=.18)
    # The 477 nm response step used to be labelled in words here. Marked
    # graphically instead -- the prose beside the figure says what it is.
    ax.axvspan(475, 479, color="#e08a72", alpha=.30)
    ax.set_ylim(.55, 1.62)
    dress(ax, "wavelength (nm)", "flux / continuum", "① normalised — every line is now a dip below 1")

    ax = fig.add_subplot(gs[1, 0])
    sel = (lam > 434.047 - 14) & (lam < 434.047 + 14)
    ax.plot(lam[sel], f[sel], color="#cfc8bd", lw=1.6)
    ax.axhline(1, color=BLU, lw=1.2, ls="--")
    ax.fill_between(lam[sel], f[sel], 1, where=f[sel] < 1, color=ACC, alpha=.55)
    dress(ax, "wavelength (nm)", "flux / continuum",
          "② EW is that shaded AREA, not the depth")

    ax = fig.add_subplot(gs[1, 1])
    widths = np.arange(1, 9.5, .5)
    for nm, L in LINES:
        ews = []
        for w in widths:
            s = (lam > L - w) & (lam < L + w) & np.isfinite(f)
            ews.append(np.trapezoid(1 - f[s], lam[s]) * 10 if s.sum() > 3 else np.nan)
        ax.plot(widths, ews, lw=1.8, label=nm,
                color={"Hδ": "#6f7f8c", "Hγ": ACC, "Hβ": "#b05a4a", "Hα": BLU}[nm])
        print(f"[ew] {nm}: at +-6 nm  EW = {ews[10]:.2f} A")
    ax.axhline(0, color="#3a3730", lw=1)
    dress(ax, "integration half-width (nm)", "equivalent width (Å)",
          "③ widen the window — a real EW flattens out")

    head(fig, "Normalising, and measuring equivalent width",
         ("Dividing by the continuum removes both the star's blackbody slope and the instrument's "
          "response, leaving lines as dips below 1.", MUT),
         ("Hγ and Hα flatten off — those are real. Hβ runs negative and Hδ turns over: both sit on "
          "a broken piece of continuum, so both are unusable.", "#c9a389"))
    p = os.path.join(outdir, "20260801 continuum and EW.png")
    fig.savefig(p, dpi=110, facecolor=BG); print("  wrote", p)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "../output"
    fig_seeing(out)
    fig_filter(out)
    fig_bayer(out)
    fig_continuum_ew(out)
