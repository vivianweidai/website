"""UV-Vis Spectroscopy analysis pipeline — pilot run on partial Session 01 data.

Canonical spectroscopy chart style (shared with IR Spectroscopy):
  figsize=(12, 5), linewidth=0.8, top/right spines hidden, y-grid only,
  colored wavelength-region shading with rotated labels, peak λmax
  annotations drawn on the chart. One PNG per sample; tabs on the page.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import find_peaks

ROOT = Path(__file__).resolve().parent.parent
DATA_SHIMADZU = ROOT / "data" / "shimadzu"
DATA_FLUOROMAX = ROOT / "data" / "fluoromax"
DATA_LAMBDA = ROOT / "data" / "lambda"
IMG = ROOT / "output" / "images"
IMG.mkdir(parents=True, exist_ok=True)

# Visible-light rainbow regions for UV-Vis (nm, label, fill color).
# Deep UV + NIR are left unshaded. Colors are light/pastel to match the
# repo chart palette.
REGIONS = [
    (200, 380, "UV",      "#e8eaf0"),
    (380, 450, "violet",  "#d9ccee"),
    (450, 495, "blue",    "#c5d9f7"),
    (495, 570, "green",   "#d4e8a0"),
    (570, 590, "yellow",  "#fff3a8"),
    (590, 620, "orange",  "#f9c4a8"),
    (620, 750, "red",     "#f4c2cb"),
]

TRACE = "#d95f5f"
PALETTE = ["#d95f5f", "#5b9bd5", "#70ad47", "#ed7d31", "#9b59b6", "#e6a532"]


def load_uvvis(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, skiprows=2, header=None, names=["wavelength_nm", "absorbance"])
    df = df.dropna().astype(float)
    df = df[(df["wavelength_nm"] >= 190) & (df["wavelength_nm"] <= 800)]
    return df.sort_values("wavelength_nm").reset_index(drop=True)


def load_fluoromax(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, skiprows=2, header=None, names=["wavelength_nm", "signal"])
    return df.dropna().astype(float).reset_index(drop=True)


UVVIS_SAMPLES = {
    # slug -> (display title, filename, (lo, hi) window for primary peak)
    "baseline":   ("Baseline — distilled water",                     "baseline.txt",                        (220, 750)),
    "quinine":    ("Quinine — 8 drops",                              "quinine-drop-8.txt",                  (300, 450)),
    "yellow":     ("Yellow highlighter — 1 drop",                    "yellow-drop-1.txt",                   (300, 600)),
    "pink":       ("Pink highlighter — ⅙ drop",                      "pink-drop-onesixth.txt",              (400, 700)),
    "salicylate": ("Salicylate — ⅙ drop further diluted ⅕",          "salicylate-drop-onesixth-onefifth.txt", (220, 500)),
}


def annotate_regions(ax):
    ylo, yhi = ax.get_ylim()
    for lo, hi, label, color in REGIONS:
        ax.axvspan(lo, hi, alpha=0.35, color=color, zorder=0)
        ax.text((lo + hi) / 2, yhi * 0.95, label,
                ha="center", va="top", fontsize=7, rotation=90, color="#555")


def fmt(ax):
    ax.set_xlim(200, 750)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Absorbance")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)


def find_primary_peak(df, lo, hi):
    mask = (df.wavelength_nm >= lo) & (df.wavelength_nm <= hi)
    sub = df[mask].reset_index(drop=True)
    sub = sub[sub.absorbance < 4.9]
    if sub.empty:
        return None, None
    peaks, props = find_peaks(sub.absorbance.values, prominence=0.02, distance=20)
    if not len(peaks):
        i = int(sub.absorbance.idxmax())
        return float(sub.wavelength_nm.iloc[i]), float(sub.absorbance.iloc[i])
    idx = peaks[np.argmax(props["prominences"])]
    return float(sub.wavelength_nm.iloc[idx]), float(sub.absorbance.iloc[idx])


def plot_single(slug, title, filename, window):
    df = load_uvvis(DATA_SHIMADZU / filename)
    # Clip saturated points (detector pin at A=5) to keep y-axis readable.
    df_plot = df.copy()
    df_plot.loc[df_plot.absorbance > 4.9, "absorbance"] = np.nan

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_plot.wavelength_nm, df_plot.absorbance, color=TRACE, linewidth=0.8)

    ax.set_ylim(0, 1)

    peak_nm, peak_a = find_primary_peak(df, *window)
    fmt(ax)
    annotate_regions(ax)

    if peak_nm is not None and peak_a < 4.9:
        ylo, yhi = ax.get_ylim()
        ax.text(
            peak_nm + 35, peak_a + (yhi - peak_a) * 0.15,
            f"λmax = {peak_nm:.0f} nm   A = {peak_a:.2f}",
            color=TRACE, fontsize=9, fontweight="bold",
            va="center", ha="left",
        )

    ax.set_title(title)
    plt.tight_layout()
    fig.savefig(IMG / f"uvvis_{slug}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return {"sample": title, "lambda_max_nm": peak_nm, "A_at_peak": peak_a}


OVERLAY_SLUGS = ["quinine", "yellow", "pink", "salicylate"]


def plot_overlay():
    fig, ax = plt.subplots(figsize=(12, 5))
    for slug, color in zip(OVERLAY_SLUGS, PALETTE):
        title, fname, _ = UVVIS_SAMPLES[slug]
        df = load_uvvis(DATA_SHIMADZU / fname)
        df_plot = df.copy()
        df_plot.loc[df_plot.absorbance > 4.9, "absorbance"] = np.nan
        ax.plot(df_plot.wavelength_nm, df_plot.absorbance,
                color=color, linewidth=0.8, label=title)
    ax.set_ylim(0, 1)
    fmt(ax)
    annotate_regions(ax)
    ax.set_title("UV-Vis absorption — day 3 water samples")
    ax.legend(fontsize=8, loc="upper right")
    plt.tight_layout()
    fig.savefig(IMG / "uvvis_overlay.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


FLUO_SAMPLES = [
    ("quinine",    "Quinine"),
    ("yellow",     "Yellow highlighter"),
    ("pink",       "Pink highlighter"),
    ("salicylate", "Salicylate"),
]


def plot_fluoromax_sample(slug, title):
    em_path = DATA_FLUOROMAX / f"{slug}-emission.csv"
    ex_path = DATA_FLUOROMAX / f"{slug}-excitation.csv"
    em = load_fluoromax(em_path) if em_path.exists() else None
    ex = load_fluoromax(ex_path) if ex_path.exists() else None

    fig, ax = plt.subplots(figsize=(12, 5))
    peaks = {}
    if ex is not None:
        ex_n = ex.signal / ex.signal.max()
        ax.plot(ex.wavelength_nm, ex_n, color="#5b9bd5", linewidth=0.8,
                label="Excitation")
        peaks["ex"] = float(ex.loc[ex.signal.idxmax(), "wavelength_nm"])
    if em is not None:
        em_n = em.signal / em.signal.max()
        ax.plot(em.wavelength_nm, em_n, color=TRACE, linewidth=0.8,
                label="Emission")
        peaks["em"] = float(em.loc[em.signal.idxmax(), "wavelength_nm"])

    ax.set_ylim(-0.05, 1.2)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.set_xlim(200, 750)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Normalized signal (0\u20131)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    annotate_regions(ax)

    y_cursor = 0.95
    if "ex" in peaks:
        ax.text(0.02, y_cursor, f"ex λmax = {peaks['ex']:.0f} nm",
                transform=ax.transAxes, fontsize=9, color="#5b9bd5",
                fontweight="bold", va="top", ha="left")
        y_cursor -= 0.07
    if "em" in peaks:
        ax.text(0.02, y_cursor, f"em λmax = {peaks['em']:.0f} nm",
                transform=ax.transAxes, fontsize=9, color=TRACE,
                fontweight="bold", va="top", ha="left")
        y_cursor -= 0.07
    if "em" in peaks and "ex" in peaks:
        stokes = peaks["em"] - peaks["ex"]
        ax.text(0.02, y_cursor, f"Stokes shift: {stokes:.0f} nm",
                transform=ax.transAxes, fontsize=9, color="#333",
                fontweight="bold", va="top", ha="left")
        peaks["stokes"] = stokes

    ax.set_title(f"{title} — FluoroMax-3" +
                 (" excitation + emission" if ex is not None and em is not None
                  else (" emission only" if em is not None else " excitation only")))
    ax.legend(loc="upper right", fontsize=8)
    plt.tight_layout()
    fig.savefig(IMG / f"fluoromax_{slug}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return peaks


def plot_fluoromax():
    results = {}
    for slug, title in FLUO_SAMPLES:
        results[slug] = plot_fluoromax_sample(slug, title)
    return results


def plot_lambda750():
    sample = pd.read_csv(DATA_LAMBDA / "sample.csv", names=["nm", "absorbance"], skiprows=1)
    sample = sample.astype(float).sort_values("nm").reset_index(drop=True)
    # Clip detector-pinned rows (A ≥ 9.9) to NaN for a readable scale.
    sample.loc[sample.absorbance >= 9.9, "absorbance"] = np.nan

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(sample.nm, sample.absorbance, color=TRACE, linewidth=0.8, label="Distilled water")
    ax.set_xlim(200, 2500)
    ax.set_ylim(0, 3)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Absorbance")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

    # Expected water NIR overtone bands.
    for x, label in [(970, "2nd O–H\novertone"),
                     (1200, "O–H\ncombination"),
                     (1450, "1st O–H\novertone"),
                     (1940, "combination\nband")]:
        ax.axvline(x, color="#666", linestyle=":", linewidth=0.6, alpha=0.6)
        ax.text(x, 2.85, label, fontsize=7, color="#555", ha="center", va="top")

    ax.set_title("Distilled water — Lambda 750 NIR scan")
    ax.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    fig.savefig(IMG / "lambda750_water.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    records = []
    for slug, (title, fname, window) in UVVIS_SAMPLES.items():
        r = plot_single(slug, title, fname, window)
        records.append(r)
        print(f"{slug:14s} λmax = {r['lambda_max_nm']} nm  A = {r['A_at_peak']}")

    plot_overlay()

    peaks_df = pd.DataFrame(records)
    peaks_df["D = A / 0.05"] = (peaks_df["A_at_peak"] / 0.05).round(1)
    peaks_df.to_csv(ROOT / "output" / "uvvis_peaks.csv", index=False)

    fluo = plot_fluoromax()
    print("\nFluoroMax-3:")
    for slug, peaks in fluo.items():
        print(f"  {slug}: {peaks}")

    plot_lambda750()
    print("\nLambda 750: water NIR scan plotted")


if __name__ == "__main__":
    main()
