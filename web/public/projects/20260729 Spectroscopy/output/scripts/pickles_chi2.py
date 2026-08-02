#!/usr/bin/env python3
"""Fetch the Pickles equivalent-width table and chi-square our two clean lines against it.

    ../../../technology/seestar/.venv/bin/python pickles_chi2.py ../output

Rung 2's reference. Pickles (1998) published a library of 131 stellar spectral
templates; VizieR J/PASP/110/863 table `lew` gives, for each one, the equivalent
widths of Hdelta, Hgamma, Hbeta and Halpha. That is the SAME quantity we can
measure, which is the whole reason this comparison is cheap: no resolution
matching, no flux calibration, no continuum model -- all three of which we would
fail at.

We use only Hgamma and Halpha. Hdelta and Hbeta sit on broken continuum (the
477 nm step and the blue cutoff), so including them would be fitting our own
artifacts and reporting the answer as a temperature.

    chi2(template) = sum over the two lines of (EW_ours - EW_template)^2 / sigma^2

sigma is NOT assumed. Sweep it, and the value that makes reduced chi2 = 1 is our
own EW uncertainty, derived from the requirement that the fit be self-consistent.

The table is 131 rows and a few kB. It IS cached to disk next to this script --
without it the classification cannot be re-run offline or checked later, and a
result whose reference has to be re-downloaded to verify is not reproducible.
The 16 GB of FITS is what git cannot carry; this is not that.
"""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pickles_lew.csv")
OURS = {"Hgamma": 13.11, "Halpha": 11.71}       # our two clean lines, in Angstrom
SEQ = "OBAFGKM"

INK, MUT, ACC, BLU, PANEL, BG = "#e8e4dd", "#a09a90", "#e8b48c", "#7fb0d0", "#131316", "#0d0d0f"


def load():
    """Cached copy if present, otherwise fetch once from VizieR and keep it."""
    if os.path.exists(CACHE):
        import csv
        with open(CACHE) as fh:
            rows = list(csv.DictReader(fh))
        print(f"  using cached {CACHE} ({len(rows)} templates)")
        return rows
    from astroquery.vizier import Vizier
    t = Vizier(columns=["**"], row_limit=-1).get_catalogs("J/PASP/110/863")["J/PASP/110/863/lew"]
    rows = [{"SpType": str(r["SpType"]).strip(),
             "Hdelta": r["Hdelta"], "Hgamma": r["Hgamma"],
             "Hbeta": r["Hbeta"], "Halpha": r["Halpha"]} for r in t]
    import csv
    with open(CACHE, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["SpType", "Hdelta", "Hgamma", "Hbeta", "Halpha"])
        w.writeheader(); w.writerows(rows)
    print(f"  fetched from VizieR and cached to {CACHE} ({len(rows)} templates)")
    return rows


def order(sp):
    """Rough temperature ordering so the chi2 curve reads left-to-right hot->cool."""
    sp = sp.lstrip("wr")
    if not sp or sp[0] not in SEQ:
        return 99.0
    sub = ""
    for ch in sp[1:]:
        if ch.isdigit() or ch == ".":
            sub += ch
        else:
            break
    return SEQ.index(sp[0]) + (float(sub) / 10 if sub else 0.0)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "../output"
    rows = load()

    keep = []
    for r in rows:
        try:
            g, a = float(r["Hgamma"]), float(r["Halpha"])
        except (TypeError, ValueError):
            continue
        if np.isfinite(g) and np.isfinite(a):
            keep.append((r["SpType"], g, a, order(r["SpType"])))
    print(f"  {len(keep)} templates with both Hgamma and Halpha")

    def chi2(sigma):
        return np.array([((OURS["Hgamma"] - g) ** 2 + (OURS["Halpha"] - a) ** 2) / sigma ** 2
                         for _, g, a, _ in keep])

    # sigma is derived, not assumed: pick the one making reduced chi2 = 1 at the best fit.
    # dof = 2, the number of lines. Each template is a fixed hypothesis with NO free
    # parameter fitted to our data, so nothing is subtracted. Using dof = 1 instead
    # gives sigma = 2.07 A and is wrong for that reason.
    sigmas = np.linspace(.3, 4.0, 400)
    red = np.array([chi2(s).min() / 2.0 for s in sigmas])
    sig = float(sigmas[np.argmin(np.abs(red - 1.0))])
    c = chi2(sig)
    idx = np.argsort(c)
    print(f"  sigma giving reduced chi2 = 1 : {sig:.2f} A")
    for i in idx[:5]:
        print(f"    {keep[i][0]:8s} chi2 {c[i]:6.2f}   Hg {keep[i][1]:5.2f}  Ha {keep[i][2]:5.2f}")
    one_sig = [keep[i][0] for i in idx if c[i] <= c[idx[0]] + 1.0]
    print(f"  1-sigma set: {one_sig}")

    fig = plt.figure(figsize=(13.4, 8.4), facecolor=BG)
    gs = fig.add_gridspec(2, 2, left=.065, right=.978, top=.845, bottom=.085,
                          hspace=.42, wspace=.2, height_ratios=[1.25, 1])

    ax = fig.add_subplot(gs[0, :])
    xs = np.array([k[3] for k in keep])
    ax.scatter(xs, c, s=26, color=BLU, alpha=.75, label="the other 130 templates")
    ax.scatter([keep[idx[0]][3]], [c[idx[0]]], s=120, color=ACC, zorder=5,
               label=f"best fit: {keep[idx[0]][0]}  (χ² = {c[idx[0]]:.2f})")
    ax.set_yscale("log")
    ax.set_xticks(range(7)); ax.set_xticklabels(list(SEQ))
    for i in idx[:4]:
        ax.annotate(keep[i][0], (keep[i][3], c[i]), (keep[i][3] + .12, c[i]),
                    color="#c8c2b8", fontsize=9)
    ax.set_xlabel("spectral type — hot to cool", color=MUT, fontsize=9.5)
    ax.set_ylabel("χ²  (log)", color=MUT, fontsize=9.5)
    # no in-figure title: ax.set_title(f"① our two lines against all {len(keep)} Pickles templates",
                 # color=INK, fontsize=11.5, pad=8)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(sigmas, red, color=ACC, lw=2)
    ax2.axhline(1, color=BLU, ls="--", lw=1.3)
    ax2.axvline(sig, color=BLU, ls="--", lw=1.3)
    ax2.set_yscale("log")
    ax2.annotate(f"σ ≈ {sig:.1f} Å", (sig, 1), (sig + .3, 4), color=BLU, fontsize=10,
                 arrowprops=dict(arrowstyle="->", color=BLU, lw=1))
    ax2.set_xlabel("assumed EW uncertainty σ (Å)", color=MUT, fontsize=9.5)
    ax2.set_ylabel("reduced χ² at best fit  (dof = 2)", color=MUT, fontsize=9.5)
    # no in-figure title: ax2.set_title("② σ is derived, not assumed", color=INK, fontsize=11.5, pad=8)

    ax3 = fig.add_subplot(gs[1, 1])
    top = idx[:6]
    ax3.barh(range(len(top)), [c[i] for i in top][::-1], color=ACC, alpha=.85)
    ax3.set_yticks(range(len(top)))
    ax3.set_yticklabels([keep[i][0] for i in top][::-1], fontsize=9)
    ax3.axvline(c[idx[0]] + 1.0, color=BLU, ls="--", lw=1.3, label="1σ boundary (Δχ² = 1)")
    ax3.set_xlabel("χ²", color=MUT, fontsize=9.5)
    # no in-figure title: ax3.set_title("③ the shortlist — and how few survive", color=INK, fontsize=11.5, pad=8)

    for a_ in (ax, ax2, ax3):
        a_.set_facecolor(PANEL)
        a_.tick_params(colors="#7a746a", labelsize=8.5)
        for s in a_.spines.values():
            s.set_color("#3a3730")
        if a_.get_legend_handles_labels()[0]:
            lg = a_.legend(facecolor=PANEL, edgecolor="#3a3730", fontsize=8.5)
            for t in lg.get_texts():
                t.set_color("#c8c2b8")

    # header moved to report prose: fig.text(.02, .958, "Rung 2 — our equivalent widths against Pickles' 131 templates",
             # color="#f2efe9", fontsize=17, weight="bold")
    # header moved to report prose: fig.text(.02, .922,
             # f"Two clean lines only: Hγ {OURS['Hgamma']} Å, Hα {OURS['Halpha']} Å. Hδ and Hβ sit on "
             # f"broken continuum and are excluded rather than fitted.", color=MUT, fontsize=10.5)
    # header moved to report prose: fig.text(.02, .893,
             # f"Result: {keep[idx[0]][0]}, with a 1σ set of {{{', '.join(one_sig)}}} at σ ≈ {sig:.1f} Å. "
             # f"SIMBAD's answer for Vega is A0V.", color="#c9a389", fontsize=10.5, style="italic")

    p = os.path.join(outdir, "20260801 Pickles chi2.png")
    fig.savefig(p, dpi=110, facecolor=BG)
    print(f"  wrote {p}")


if __name__ == "__main__":
    main()
