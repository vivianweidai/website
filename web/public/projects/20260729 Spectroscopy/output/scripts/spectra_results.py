#!/usr/bin/env python3
"""Evidence package for the 2026-07-29 spectroscopy first light.

Produces, beside this script in output/spectroscopy/:
  01_vega_spectrum.png       the combined Vega spectrum with the Balmer series
  02_wavelength_solution.png the residual plot -- the actual proof
  03_vega_vs_albireo.png     Vega against the unresolved Albireo pair
  results.txt                the numbers

Run:  work/astronomy/.venv/bin/python output/spectroscopy/spectra_results.py
"""
import glob
import os
import sys

import numpy as np
from scipy.ndimage import median_filter
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reduce_spectrum import BALMER, GRID, DATA, combine, planes, zero_orders, \
    trace_and_extract, lam_of, A_FIT   # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt        # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
STAMP = "20260729"   # the night this evidence package describes
os.makedirs(OUT, exist_ok=True)
log = open(f"{OUT}/{STAMP} spectroscopy results.txt", "w")


def say(s=""):
    print(s, flush=True)
    log.write(s + "\n")


vega_files = sorted(glob.glob(f"{DATA}/Vega/Light_Vega_5.0s_*20260729-22[2-5]*.fit"))
alb_files = sorted(glob.glob(f"{DATA}/Albireo/Light_Albireo_20.0s_*.fit"))

say("SPECTROSCOPY RESULTS — Seestar S30 Pro + Star Analyser 100, 2026-07-29")
say("=" * 72)
say(f"Vega    : {len(vega_files)} x 5 s subs")
say(f"Albireo : {len(alb_files)} x 20 s subs")
say()

vega = combine(vega_files, nmax=1, label_="Vega")[0]
alb = combine(alb_files, nmax=1, label_="Vega")[0]

# ---------- 1. Vega, with line depths and significance ------------------------
noise = np.nanstd(vega[(GRID > 600) & (GRID < 640)])
say(f"\nVEGA (A0V) — continuum noise in the 600-640 nm window: {noise:.4f}")
say(f"{'line':10}{'lambda':>9}{'depth':>9}{'significance':>14}")
rows = []
for n, l0 in BALMER:
    m = (GRID > l0 - 3) & (GRID < l0 + 3)
    d = 1 - np.nanmin(vega[m])
    rows.append((n, l0, d, d / noise))
    say(f"  {n:8}{l0:9.3f}{d*100:8.1f}%{d/noise:12.1f} sigma")

fig, ax = plt.subplots(figsize=(11, 4.6))
ax.plot(GRID, vega, lw=1.0, color="#1d3557")
for n, l0, d, s in rows:
    ax.axvline(l0, color="#d95f5f", lw=0.9, ls="--", alpha=0.85)
    # text lives in the report prose: ax.text(l0, 1.46, f"{n.split('-')[1]}\n{d*100:.0f}%", ha="center",
            # fontsize=8, color="#d95f5f")
ax.set_xlabel("wavelength (nm)"); ax.set_ylabel("normalised flux")
ax.set_ylim(0, 1.6); ax.grid(alpha=0.15)
# text lives in the report prose: ax.set_title(f"Vega (A0V) — {len(vega_files)} x 5 s combined · continuum noise {noise:.3f}\n"
             # "the four Balmer lines, all detected above 15 sigma", fontsize=10)
fig.tight_layout(); fig.savefig(f"{OUT}/{STAMP} Vega spectrum.png", dpi=150)

# ---------- 2. the wavelength solution: the actual proof ----------------------
obs = []
for n, l0 in BALMER:
    m = (GRID > l0 - 4) & (GRID < l0 + 4)
    idx = np.where(m)[0]
    j = idx[np.nanargmin(vega[idx])]
    k = slice(j - 2, j + 3)
    c = np.polyfit(GRID[k], vega[k], 2)
    obs.append(-c[1] / (2 * c[0]))
obs = np.array(obs); cat = np.array([l for _, l in BALMER])
resid = obs - cat
say(f"\nWAVELENGTH SOLUTION  px(lam) = A tan(asin(lam/10000)),  A = {A_FIT:.0f} px")
say(f"{'line':10}{'catalog':>10}{'measured':>11}{'residual':>11}")
for (n, l0), o, r in zip(BALMER, obs, resid):
    say(f"  {n:8}{l0:10.3f}{o:11.3f}{r:+11.3f}")
say(f"  rms residual: {np.sqrt((resid**2).mean()):.3f} nm over {cat.min():.0f}-{cat.max():.0f} nm")
say(f"  implied focal length: {A_FIT*2.9e-3:.1f} mm  (nameplate 160, plate scale ~163)")

fig, ax = plt.subplots(figsize=(8, 4))
ax.axhline(0, color="#999", lw=1)
ax.plot(cat, resid, "o", ms=9, color="#c1121f")
for (n, l0), r in zip(BALMER, resid):
    ax.annotate(n, (l0, r), textcoords="offset points", xytext=(0, 11),
                ha="center", fontsize=8)
ax.set_xlabel("catalogue wavelength (nm)"); ax.set_ylabel("measured − catalogue (nm)")
ax.set_ylim(-0.3, 0.3); ax.grid(alpha=0.2)
# text lives in the report prose: ax.set_title("Wavelength solution residuals — rms "
             # f"{np.sqrt((resid**2).mean()):.3f} nm across 410–656 nm", fontsize=10)
fig.tight_layout(); fig.savefig(f"{OUT}/{STAMP} wavelength solution.png", dpi=150)

# ---------- 3. Vega vs Albireo: A0V against a cooler composite ----------------
# Corrected 2026-07-30. This used to be labelled "A0V against K3II", which
# claimed we had isolated Albireo A. We have not: Albireo A-B are 35" apart =
# 4.8 px in the green plane, blended well beyond separation at this scale, so
# the brightest streak is the UNRESOLVED pair (K3II + B8V), not the K3II alone.
# The other streaks in the frame are field stars -- with an objective grating
# every star in the field disperses. A genuine A-vs-K contrast still needs a
# separate cool target (Arcturus or Antares).
anoise = np.nanstd(alb[(GRID > 600) & (GRID < 640)]) if alb is not None else np.nan
say(f"\nALBIREO (unresolved A+B: K3II + B8V) — continuum noise: {anoise:.4f}  "
    f"({anoise/noise:.1f}x Vega's, from {len(alb_files)} subs vs {len(vega_files)})")
say("  Balmer depth in the Albireo blend (an A0V would show 30%+):")
for n, l0 in BALMER:
    m = (GRID > l0 - 3) & (GRID < l0 + 3)
    d = 1 - np.nanmin(alb[m])
    say(f"    {n:8}{d*100:6.1f}%   {d/anoise:5.1f} sigma")

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(GRID, vega, lw=1.0, color="#1d3557", label="Vega — A0V")
ax.plot(GRID, alb - 0.55, lw=1.0, color="#c1121f",
        label="Albireo — A+B unresolved, K3II+B8V (offset −0.55)")
for n, l0 in BALMER:
    ax.axvline(l0, color="#888", lw=0.8, ls="--", alpha=0.6)
    # text lives in the report prose: ax.text(l0, 1.5, n.split('-')[1], ha="center", fontsize=8, color="#666")
ax.set_xlabel("wavelength (nm)"); ax.set_ylabel("normalised flux (offset)")
ax.set_ylim(0, 1.65); ax.grid(alpha=0.15); ax.legend(fontsize=9, loc="lower right")
# text lives in the report prose: ax.set_title("Two spectra, one grating: hydrogen-dominated A0V (Vega) vs the "
             # "unresolved Albireo pair", fontsize=10)
fig.tight_layout(); fig.savefig(f"{OUT}/{STAMP} Vega vs Albireo.png", dpi=150)

# NOT spectra.npz -- reduce_spectrum.py owns that name and writes a DIFFERENT
# schema into it (albireo_a / albireo_b, two streaks; this one carries a single
# combined `albireo`). Same folder, same filename, incompatible keys: whichever
# ran last silently won, and a reader written against one broke on the other.
np.savez(f"{OUT}/{STAMP} spectroscopy results.npz", grid=GRID, vega=vega, albireo=alb)
say(f"\nwrote {STAMP} Vega spectrum.png, {STAMP} wavelength solution.png, "
    f"{STAMP} Vega vs Albireo.png, {STAMP} spectroscopy results.npz")
log.close()
