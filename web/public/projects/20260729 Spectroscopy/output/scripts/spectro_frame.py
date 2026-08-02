#!/usr/bin/env python3
"""Where to point so a star's spectrum lands ON the sensor.

The Star Analyser is an objective grating, so the spectrum is thrown a long way
from the star: 400 nm lands 2209 px out and 700 nm at 3872 px, on a sensor whose
long axis is 3840 px. A CENTRED star therefore throws its entire spectrum off
the chip -- which is exactly why the first Vega attempts recorded other stars'
streaks and nothing from the target. The star has to sit in the corner the
spectrum runs away from.

    # 1. what the geometry allows, no data needed
    .venv/bin/python output/spectroscopy/spectro_frame.py --angle 16

    # 2. the actual goto, from one solved calibration frame
    .venv/bin/python output/spectroscopy/spectro_frame.py --angle 16 --frame calib.fits

Mode 2 is exact and needs no angle bookkeeping: to put the star at pixel P,
point at whatever sky coordinate currently sits at pixel (2*centre - P). Slewing
that point to the centre carries the star to P. The WCS does all the rotation.

Measure --angle from ONE frame with a bright star centred, by reading the
direction of the OTHER stars' streaks. A threaded grating mount does not repeat
its angle between sessions, so this is a per-session measurement, not a constant.
"""
import argparse
import math
import sys

# --- instrument ------------------------------------------------------------
# The Seestar writes its subs PORTRAIT: NAXIS1 = 2160 (short), NAXIS2 = 3840
# (long). SEESTAR.md §9's "3840 x 2160" is the sensor spec, not the array order, and
# assuming x was the long axis put a non-uniform scale factor (0.28 vs 0.89) into
# the WCS conversion here before this was checked against a real header.
NX, NY = 2160, 3840          # NAXIS1 (short) x NAXIS2 (long)
PIX = 3.669                  # arcsec/px, measured from solved frames
GROOVE_NM = 10000.0          # Star Analyser 100: 100 lines/mm -> 10 um period

# Dispersion: px = A * tan(asin(lambda / groove)).  A is fitted to our own
# 2026-07-28 measurement of 400 nm at 2209 px, and then reproduces 486, 656 and
# 700 nm to under a pixel -- so the four numbers in SPECTROSCOPY.md are not four
# measurements, they are one grating equation. A * 2.9 um/px = 160.0 mm, i.e.
# the nominal focal length exactly.
# (Note the 1.9% tension with the 3.669"/px plate scale, which implies ~163 mm.
#  Unresolved -- the grating may not be exactly 100 lines/mm. Harmless here:
#  everything below is anchored on our own pixel measurements, not on 160 mm.)
A_PX = 2209.0 / math.tan(math.asin(400.0 / GROOVE_NM))


def px_of(lam_nm):
    """Distance in px from the zero-order dot to wavelength lam_nm."""
    return A_PX * math.tan(math.asin(lam_nm / GROOVE_NM))


def lam_of(px):
    """Inverse: which wavelength lands px from the zero-order dot."""
    s = math.sin(math.atan(px / A_PX))
    return s * GROOVE_NM


def run_to_edge(x, y, ux, uy):
    """Distance from (x,y) to the frame boundary along unit vector (ux,uy)."""
    ts = []
    if ux > 0:
        ts.append((NX - 1 - x) / ux)
    elif ux < 0:
        ts.append((0 - x) / ux)
    if uy > 0:
        ts.append((NY - 1 - y) / uy)
    elif uy < 0:
        ts.append((0 - y) / uy)
    return min(ts) if ts else 0.0


def best_corner(angle_deg, margin):
    """Put the star in the corner the spectrum runs AWAY from.

    Returns (px, py, run) for whichever corner gives the longest on-sensor run
    along the dispersion direction.
    """
    # angle is measured from the LONG axis, which is +y in this array order.
    ux, uy = math.sin(math.radians(angle_deg)), math.cos(math.radians(angle_deg))
    best = None
    for cx in (margin, NX - 1 - margin):
        for cy in (margin, NY - 1 - margin):
            r = run_to_edge(cx, cy, ux, uy)
            if best is None or r > best[2]:
                best = (cx, cy, r)
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--angle", type=float, required=True,
                    help="dispersion direction in SENSOR coords, deg from the LONG axis (+y in array order). "
                         "Measure it each session from a centred-star frame.")
    ap.add_argument("--margin", type=int, default=120,
                    help="px to inset the star from the corner so it is not clipped (default 120)")
    ap.add_argument("--frame", help="a solved calibration FITS -> print the goto RA/Dec")
    args = ap.parse_args()

    sx, sy, run = best_corner(args.angle, args.margin)
    lam_max = lam_of(min(run, px_of(700.0)))

    print(f"\nSPECTROSCOPY FRAMING   dispersion {args.angle:.1f} deg from long axis, "
          f"margin {args.margin} px\n")
    print(f"  put the star at pixel      ({sx:.0f}, {sy:.0f})   "
          f"[frame is {NX} x {NY}, centre ({NX//2}, {NY//2})]")
    print(f"  on-sensor run from there   {run:.0f} px")
    print(f"  wavelength coverage        {lam_of(px_of(400.0)):.0f}"
          f" - {lam_max:.0f} nm")

    print("\n  line                 lands at   on sensor?")
    for name, lam in (("H-beta", 486.1), ("Mg b", 517.0), ("Na D", 589.3),
                      ("H-alpha", 656.3), ("red cutoff", 700.0)):
        p = px_of(lam)
        print(f"  {name:18s} {lam:6.1f} nm  {p:6.0f} px   "
              f"{'yes' if p <= run else 'OFF THE END'}")

    if run < px_of(656.3):
        print("\n  ⚠️  H-alpha does not fit. Reduce --margin, or re-thread the grating so the")
        print("      dispersion runs closer to the frame diagonal.")

    if not args.frame:
        print("\n  Pass --frame <solved.fits> to turn this into a goto coordinate.\n")
        return

    from astropy.io import fits
    from astropy.wcs import WCS
    hdr = fits.getheader(args.frame)
    w = WCS(hdr)
    if not w.has_celestial:
        sys.exit(f"{args.frame} has no WCS -- plate-solve it first (solve-field).")

    # The calibration frame is usually the GREEN-EXTRACTED half-res grid (1920x1080
    # at 7.338"/px), because that is what solves. Its WCS is in those pixels, so
    # feeding it full-res coordinates extrapolates and doubles the offset -- which
    # is exactly what happened the first time this ran (4.06 deg instead of 2.03).
    # Scale into whatever grid the frame is actually on.
    fx, fy = hdr.get("NAXIS1", NX), hdr.get("NAXIS2", NY)
    kx, ky = fx / NX, fy / NY
    if abs(kx - 1.0) > 0.01:
        print(f"\n  (calibration frame is {fx}x{fy} — scaling pixel coords by {kx:.2f})")

    # To land the star at (sx,sy), point at the sky currently at (2*centre - star).
    qx, qy = (NX / 2 - (sx - NX / 2)) * kx, (NY / 2 - (sy - NY / 2)) * ky
    q = w.pixel_to_world(qx, qy)
    ra_h = q.ra.deg / 15.0
    print(f"\n  goto this coordinate:")
    print(f"    RA  {q.ra.deg:10.5f} deg = {ra_h:.6f} h")
    print(f"    Dec {q.dec.deg:+10.5f} deg")
    print(f"    seestar.py goto {ra_h:.6f} {q.dec.deg:.5f}")
    print(f"\n  (offset {q.separation(w.pixel_to_world(NX/2*kx, NY/2*ky)).deg:.3f} deg "
          f"from the calibration frame's centre)\n")


if __name__ == "__main__":
    main()
