#!/usr/bin/env python3
"""Slitless spectrum reduction for the Seestar S30 Pro + Star Analyser 100.

The grating is an OBJECTIVE grating: each star gives a zero-order dot plus a
first-order streak thrown ~2200 px away at 400 nm. So a frame carries one
spectrum per star, and the reduction is per-object, not per-frame.

Method, in the order the mistakes were made and fixed on 2026-07-29:
  1. locate the zero-order dot  -- it is the lambda = 0 anchor
  2. fit the trace ROW BY ROW following the tilt. A fixed-x window walks off the
     streak over 1800 rows and locks onto a neighbour (first attempt: 5.1 px rms;
     tilt-following: 0.10 px rms).
  3. extract per Bayer plane, background from off-trace on the same row. A 2x2
     block sum stamps the R/G/B response onto the continuum and a row-median
     background eats the streak itself.
  4. wavelength from  px(lambda) = A * tan(asin(lambda / 10000 nm)),
     A = 56016 px fitted to Vega's Balmer series. Applied out-of-sample to the
     30-frame combined spectrum it reproduces the four lines to rms 0.185 nm
     over 410-656 nm. (The 0.053 nm quoted at first was the in-sample fit
     residual -- same lines used to fit and to score. Not a real accuracy.)

Run with the repo venv:
    work/astronomy/.venv/bin/python output/spectroscopy/reduce_spectrum.py
"""
import glob
import os
import warnings

import numpy as np
from astropy.io import fits
from scipy.ndimage import median_filter, label

warnings.filterwarnings("ignore")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))   # repo root
DATA = os.path.join(os.path.dirname(HERE), "data")   # spectroscopy owns its frames
OUT = os.path.join(os.path.dirname(HERE), "output")
os.makedirs(OUT, exist_ok=True)

A_FIT = 56016.0            # px, fitted to Vega's Balmer lines 2026-07-29
GROOVE = 10000.0           # nm, Star Analyser 100 = 100 lines/mm
BALMER = [("H-delta", 410.174), ("H-gamma", 434.047),
          ("H-beta", 486.135), ("H-alpha", 656.281)]


def planes(path):
    """GRBG -> (G, R, B) at half resolution, no interpolation."""
    d = fits.getdata(path).astype(float)
    return (0.5 * (d[0::2, 0::2] + d[1::2, 1::2]), d[0::2, 1::2], d[1::2, 0::2])


def lam_of(px):
    return GROOVE * np.sin(np.arctan(px / A_FIT))


def px_of(lam):
    return A_FIT * np.tan(np.arcsin(lam / GROOVE))


def zero_orders(G, nmax=2):
    """Compact bright blobs = zero-order dots. Streaks are long, so filter on extent."""
    S = G - median_filter(G, size=31)
    thr = np.percentile(S, 99.985)
    lab, n = label(S > thr)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 4:
            continue
        ext = max(ys.max() - ys.min(), xs.max() - xs.min())
        if ext > 30:                     # that is a streak, not a dot
            continue
        out.append((S[ys, xs].sum(), xs.mean(), ys.mean()))
    out.sort(reverse=True)
    return [(x, y) for _, x, y in out[:nmax]]


def trace_and_extract(P3, zx, zy, tilt_scan=(2.0, 6.0)):
    """Return (lam, flux) for the spectrum belonging to the dot at (zx, zy)."""
    G = P3[0]
    ny, nx = G.shape
    y0 = zy + px_of(400.0) / 2.0            # green plane is half-scale
    y1 = min(ny - 1, zy + px_of(700.0) / 2.0)
    if y1 - y0 < 200:
        return None
    ys_scan = np.arange(int(y0), int(y1))

    best = None                              # find the tilt that maximises flux
    for sgn in (+1, -1):
        for ang in np.arange(tilt_scan[0], tilt_scan[1], 0.25):
            t = np.tan(np.radians(ang)) * sgn
            tot = 0.0
            for y in ys_scan[::4]:
                xc = zx + (y - zy) * t
                lo, hi = int(xc - 10), int(xc + 10)
                if lo < 0 or hi >= nx:
                    break
                tot += G[y, lo:hi].sum()
            if best is None or tot > best[0]:
                best = (tot, t)
    t = best[1]

    ys, xs = [], []                          # centroid per row, then a smooth fit
    for y in ys_scan:
        xc = zx + (y - zy) * t
        lo, hi = int(xc - 14), int(xc + 14)
        if lo < 0 or hi >= nx:
            continue
        seg = G[y, lo:hi] - np.median(G[y])
        w = np.clip(seg, 0, None) ** 2
        if w.sum() <= 0:
            continue
        ys.append(y)
        xs.append((np.arange(lo, hi) * w).sum() / w.sum())
    if len(ys) < 100:
        return None
    ys, xs = np.array(ys), np.array(xs)
    p = np.polyfit(ys, xs, 2)
    r = xs - np.polyval(p, ys)
    k = np.abs(r) < 3 * np.std(r)
    p = np.polyfit(ys[k], xs[k], 2)
    rms = np.std(xs[k] - np.polyval(p, ys[k]))

    xc = np.polyval(p, ys)
    flux = np.zeros(len(ys))
    for P in P3:
        for i, (y, x) in enumerate(zip(ys, xc)):
            lo, hi = int(x - 9), int(x + 10)
            bl = np.median(np.r_[P[y, lo - 30:lo - 10], P[y, hi + 10:hi + 30]])
            flux[i] += P[y, lo:hi].sum() - bl * (hi - lo)
    return lam_of((ys - zy) * 2.0), flux, rms


GRID = np.arange(400, 672, 0.35)


def combine(files, nmax=1, label_=""):
    """Extract every frame onto a common lambda grid and median-combine."""
    stack = [[] for _ in range(nmax)]
    used = 0
    for f in files:
        P3 = planes(f)
        dots = zero_orders(P3[0], nmax=nmax)
        if len(dots) < nmax:
            continue
        dots.sort(key=lambda d: d[1])              # deterministic order by y
        ok = False
        for j, (zx, zy) in enumerate(dots):
            r = trace_and_extract(P3, zx, zy)
            if r is None:
                continue
            lam, fl, rms = r
            if rms > 1.5:
                continue
            cont = median_filter(fl, size=121)
            norm = fl / np.maximum(cont, 1e-9)
            stack[j].append(np.interp(GRID, lam, norm, left=np.nan, right=np.nan))
            ok = True
        used += ok
    print(f"  {label_}: {used}/{len(files)} frames contributed", flush=True)
    # Stashed on the function so a caller can put the honest count in a title
    # without changing the return shape (spectra_results.py imports this too).
    combine.last_used = used
    return [np.nanmedian(np.array(s), axis=0) if s else None for s in stack]


if __name__ == "__main__":
    print("VEGA (A0V) — spectrum subs at the corner framing", flush=True)
    vega = sorted(glob.glob(f"{DATA}/Vega/Light_Vega_5.0s_*20260729-22[2-5]*.fit"))
    vspec = combine(vega, nmax=1, label_="Vega")[0]
    vused = combine.last_used

    # Corrected 2026-07-30: nmax=2 does NOT give Albireo A and B. The pair is
    # 35" = 4.8 px apart in the green plane, blended beyond separation, so the
    # brightest streak is the unresolved A+B and the second is a FIELD STAR --
    # with an objective grating every star in the field disperses.
    print("ALBIREO FIELD — brightest two streaks (A+B blended, then a field star)",
          flush=True)
    alb = sorted(glob.glob(f"{DATA}/Albireo/Light_Albireo_20.0s_*.fit"))
    aspec = combine(alb, nmax=2, label_="Vega")

    fig, ax = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    if vspec is not None:
        ax[0].plot(GRID, vspec, lw=0.9, color="#2a6ebb")
        noise = np.nanstd(vspec[(GRID > 600) & (GRID < 640)])
        for n, l0 in BALMER:
            ax[0].axvline(l0, color="#d95f5f", lw=0.9, ls="--", alpha=0.9)
            m = (GRID > l0 - 3) & (GRID < l0 + 3)
            d = 1 - np.nanmin(vspec[m])
            ax[0].text(l0, 1.42, f"{n.split('-')[1]}\n{d*100:.0f}%",
                       ha="center", fontsize=8, color="#d95f5f")
        # Count what CONTRIBUTED, not what was globbed -- frames fail the trace-rms
        # cut and the difference is real (25 of 30 on the 07-29 Vega set).
        ax[0].set_title(f"Vega A0V — {vused} of {len(vega)} x 5 s subs combined · "
                        f"continuum noise {noise:.3f}", fontsize=10)
    ax[0].set_ylabel("normalised flux"); ax[0].set_ylim(0, 1.6); ax[0].grid(alpha=0.15)

    for s, c, nm in zip(aspec, ("#c1121f", "#4361ee"),
                        ("brightest streak — Albireo A+B, unresolved",
                         "second streak — a field star")):
        if s is not None:
            ax[1].plot(GRID, s, lw=0.9, color=c, label=nm)
    for n, l0 in BALMER:
        ax[1].axvline(l0, color="#999", lw=0.8, ls="--", alpha=0.7)
    ax[1].set_title("Albireo field — the brightest streak is A+B unresolved; "
                    "the others are field stars, not the pair", fontsize=10)
    ax[1].set_xlabel("wavelength (nm)"); ax[1].set_ylabel("normalised flux")
    ax[1].set_ylim(0, 1.6); ax[1].grid(alpha=0.15); ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{OUT}/spectra_vega_albireo.png", dpi=150)
    np.savez(f"{OUT}/spectra.npz", grid=GRID, vega=vspec,
             albireo_a=aspec[0], albireo_b=aspec[1])
    print(f"saved {OUT}/spectra_vega_albireo.png", flush=True)
