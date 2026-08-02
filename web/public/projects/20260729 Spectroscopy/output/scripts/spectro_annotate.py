#!/usr/bin/env python3
"""Annotate a Star Analyser streak with the Balmer absorption lines.

Rectifies the slanted streak into a horizontal strip (wavelength left to right),
marks the four Balmer lines on it, and stacks the 1-D profile underneath on a
shared wavelength axis -- so a dark band in the strip lines up with a dip in the
trace directly below it.

Usage:  spectro_annotate.py <frame.fit> [outdir]

Geometry comes from the closed-form dispersion recorded in SPECTROSCOPY.md:
    r(lambda) = A * tan(asin(lambda / 10000 nm))
with A RE-FITTED per mounting (55181 on 2026-07-28, 56181 on 2026-07-30 -- the
barrel threads on to a slightly different depth each time).
with r measured from the zero-order dot. The streak ANGLE is measured per frame
-- a threaded grating mount does not repeat (16 deg on 2026-07-28, -4.2 deg on
2026-07-30), so it must never be assumed.
"""
import sys, os
import numpy as np
from astropy.io import fits
from scipy.ndimage import (map_coordinates, gaussian_filter1d, median_filter,
                           center_of_mass)
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

A_PX = 55181.0
LINES = [('H$\\delta$', 410.17), ('H$\\gamma$', 434.05),
         ('H$\\beta$', 486.13), ('H$\\alpha$', 656.28)]

r_of_lam = lambda L: A_PX * np.tan(np.arcsin(np.asarray(L) / 10000.0))
lam_of_r = lambda r: 10000.0 * np.sin(np.arctan(np.asarray(r) / A_PX))


def load_rgb(path):
    """Half-resolution RGB from the GRBG mosaic. Row0: G R / Row1: B G."""
    d = fits.getdata(path).astype(float)
    d -= np.median(d)
    R = d[0::2, 1::2]
    B = d[1::2, 0::2]
    G = 0.5 * (d[0::2, 0::2] + d[1::2, 1::2])
    n = min(R.shape[0], B.shape[0], G.shape[0]), min(R.shape[1], B.shape[1], G.shape[1])
    return np.dstack([R[:n[0], :n[1]], G[:n[0], :n[1]], B[:n[0], :n[1]]]), d


def find_zero_order(d):
    y, x = np.unravel_index(np.argmax(gaussian_filter1d(
        gaussian_filter1d(d, 2, axis=0), 2, axis=1)), d.shape)
    return float(y), float(x)


def centroid_zero_order(d, y, x, box=60):
    """Flux centroid on the UNSATURATED wings -- argmax sits on a flat clipped
    core. Only ~3.6 px on Vega, but free to fix and it is the solution origin."""
    yi, xi = int(y), int(x)
    sub = d[yi - box:yi + box + 1, xi - box:xi + box + 1].astype(float)
    w = np.where(sub > 40000, 0.0, sub)
    w = np.clip(w - np.percentile(w, 50), 0, None)
    if w.sum() <= 0:
        return float(y), float(x)
    gy, gx = center_of_mass(w)
    return yi - box + gy, xi - box + gx


def measure_angle(d, y0, x0, r0=1600, r1=3600):
    """Brightest streak direction, then refined on its transverse drift."""
    H, W = d.shape

    def trace(ang):
        a = np.deg2rad(ang); ux, uy = np.sin(a), np.cos(a)
        px, py = uy, -ux
        out = []
        for r in range(r0, r1, 25):
            cx, cy = x0 + ux * r, y0 + uy * r
            if not (30 < cx < W - 30 and 30 < cy < H - 30):
                continue
            o = np.arange(-25, 26)
            v = np.clip(d[(cy + py * o).astype(int), (cx + px * o).astype(int)], 0, None)
            if v.sum() > 0:
                out.append((r, (v * o).sum() / v.sum(), v.sum()))
        return np.array(out)

    best = None
    for ang in np.arange(-30, 30, 0.25):
        p = trace(ang)
        if len(p) >= 20 and (best is None or p[:, 2].sum() > best[1]):
            best = (ang, p[:, 2].sum(), p)
    ang, _, p = best
    return ang + np.rad2deg(np.arctan(np.polyfit(p[:, 0], p[:, 1], 1)[0]))


def rectify(rgb, y0h, x0h, ux, uy, rs_h, half_width=22):
    """Resample the slanted streak into a straight horizontal strip."""
    px, py = uy, -ux
    t = np.arange(-half_width, half_width + 1)
    RR, TT = np.meshgrid(rs_h, t)
    xs = x0h + ux * RR + px * TT
    ys = y0h + uy * RR + py * TT
    return np.dstack([map_coordinates(rgb[:, :, c], [ys, xs], order=1, mode='constant')
                      for c in range(3)])


def stretch(strip, lo=40, hi=99.8, gamma=0.55):
    out = np.zeros_like(strip)
    for c in range(3):
        ch = strip[:, :, c]
        a, b = np.percentile(ch, lo), np.percentile(ch, hi)
        out[:, :, c] = np.clip((ch - a) / max(b - a, 1e-9), 0, 1) ** gamma
    return out


def main():
    path = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(path) or '.'
    rgb, d = load_rgb(path)

    y0, x0 = find_zero_order(d)
    y0, x0 = centroid_zero_order(d, y0, x0)
    ang = measure_angle(d, y0, x0)
    a = np.deg2rad(ang); ux, uy = np.sin(a), np.cos(a)
    print(f'zero order (x,y) = ({x0:.0f},{y0:.0f})   streak angle {ang:+.2f} deg')

    H, W = d.shape
    r_max = min(3760, int((H - y0 - 10) / max(abs(uy), 1e-6)))
    rs = np.arange(2050, r_max)
    print(f'usable streak r = {rs.min()}-{rs.max()} px  ->  '
          f'{lam_of_r(rs.min()):.0f}-{lam_of_r(rs.max()):.0f} nm')

    strip = rectify(rgb, y0 / 2, x0 / 2, ux, uy, rs / 2.0)
    disp = stretch(strip)

    # Extract from the DEBAYERED strip, never the raw mosaic: a box on the mosaic
    # mixes three filter throughputs and beats against the streak, doubling the
    # ripple (0.05 -> 0.026 rms in a line-free window).
    prof = strip.sum(axis=2).sum(axis=0)
    sm = gaussian_filter1d(prof, 4)
    lam_nom = lam_of_r(rs)
    win = int(36.0 / ((lam_nom[-1] - lam_nom[0]) / len(lam_nom))) | 1
    norm = sm / np.clip(median_filter(sm, win), 1, None)

    # Re-fit A to the Balmer series, trusting the zero-order dot as the origin.
    # A is NOT a constant: it is (grating-to-sensor distance)/(pixel size), and
    # re-threading the barrel moves the grating a few mm axially -- 55181 on
    # 2026-07-28, 56181 on 2026-07-30. Fitting A with the dot trusted gives
    # 0.14 nm rms; holding A fixed and fitting an origin offset instead gives
    # 1.75 nm, i.e. 12x worse for the same one free parameter.
    def resid(p):
        out = []
        for _, L in LINES:
            rp = p[0] * np.tan(np.arcsin(L / 10000.0))
            w = np.abs(rs - rp) < 90
            if w.sum() >= 5:
                out.append(rs[np.argmin(np.where(w, norm, 9))] - rp)
        return out or [0.0]

    A_fit = float(least_squares(resid, [A_PX]).x[0])
    lam = 10000.0 * np.sin(np.arctan(rs / A_fit))
    r_of_lam_fit = lambda L: A_fit * np.tan(np.arcsin(np.asarray(L) / 10000.0))
    rms = np.sqrt(np.mean(np.square(resid([A_fit])))) * (lam[1] - lam[0])
    print(f'A re-fitted to the Balmer series: {A_fit:.0f} px '
          f'(nominal {A_PX:.0f}) -> grating-to-sensor {A_fit * 2.9e-3:.1f} mm')

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(15, 6.4), sharex=True,
        gridspec_kw={'height_ratios': [1, 2.1], 'hspace': 0.06})

    ax1.imshow(disp, aspect='auto', origin='lower',
               extent=[lam[0], lam[-1], 0, disp.shape[0]])
    ax1.set_yticks([])
    # text lives in the report prose: ax1.set_title(f'Vega (A0V) - Star Analyser 100 streak, rectified   '
                  # f'[{os.path.basename(path)}, 5 s, IRCUT, streak {ang:+.1f}$\\degree$]',
                  # fontsize=11)

    # Positions come from the grating equation, not from searching this trace:
    # +/-30 px out of a 1600 px streak is invisible when the job is pointing at
    # a band on an image, and it cannot be dragged off by a noise spike.
    for label, L in LINES:
        if not (lam[0] < L < lam[-1]):
            continue
        r = r_of_lam_fit(L)
        for ax in (ax1, ax2):
            ax.axvline(L, color='#ff2d55', ls='--', lw=1.1, alpha=0.85)
        ax1.annotate('', xy=(L, disp.shape[0] * 0.34),
                     xytext=(L, disp.shape[0] * 0.02),
                     arrowprops=dict(arrowstyle='-|>', color='#ff2d55', lw=1.7))
        ax1.text(L, disp.shape[0] * 0.78, label, color='#ff2d55',
                 ha='center', fontsize=14, weight='bold')
        ax2.text(L, 1.15, f'{L:.0f} nm', color='#ff2d55', ha='center', fontsize=9)
        w = np.abs(lam - L) < 9
        j = np.argmin(np.where(w, norm, 9)) if w.sum() >= 5 else None
        dep = f'{1 - norm[j]:.0%} deep, resid {lam[j] - L:+.1f} nm' if j is not None else 'n/a'
        print(f'  {label:>12s} {L:6.1f} nm -> r = {r:6.0f} px from zero order, '
              f'native pixel (x,y) = ({x0 + ux * r:.0f}, {y0 + uy * r:.0f})   {dep}')

    ax1.text(0.005, 0.06, 'blue end\n(near the star)', transform=ax1.transAxes,
             color='w', fontsize=8, va='bottom', ha='left', alpha=0.75)
    ax1.text(0.995, 0.06, 'red end\n(far from star)', transform=ax1.transAxes,
             color='w', fontsize=8, va='bottom', ha='right', alpha=0.75)

    ax2.plot(lam, norm, 'k-', lw=0.9)
    ax2.axvspan(560, 590, color='#7a5cff', alpha=0.10, zorder=0)
    ax2.text(575, 0.52, 'CFA green/red\ncrossover -- instrumental,\nnot stellar',
             color='#5b3ecc', fontsize=8, ha='center', va='center')
    ax2.set_ylim(0.45, 1.22)
    ax2.set_xlim(lam[0], lam[-1])
    ax2.set_ylabel('normalised flux\n(quick re-extraction)')
    ax2.set_xlabel('wavelength (nm)')
    ax2.grid(alpha=0.25)
    ax2.axhline(1.0, color='0.6', lw=0.6)

    out = os.path.join(outdir, 'vega_streak_annotated.png')
    fig.savefig(out, dpi=140, bbox_inches='tight')
    print('wrote', out)


if __name__ == '__main__':
    main()
