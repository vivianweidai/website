"""
Clean raw FT-IR CSV exports into standardised per-sample files.

Input:  data/*.csv                     (headerless: wavenumber, transmittance)
Output: output/scrubbed/<sample>.csv   (headers: wavenumber,transmittance,absorbance)

The Nicolet 380 already applies background correction, so transmittance
values are already relative to the background (~100 % in non-absorbing
regions).  This script parses the scientific-notation format, adds an
absorbance column [A = -log10(T/100)], and writes clean CSVs.
"""

import os, numpy as np, pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(BASE)  # 20260419 IR Spectroscopy/
SCRUBBED = os.path.join(BASE, "scrubbed")
os.makedirs(SCRUBBED, exist_ok=True)

# Map raw filenames → clean output names
SAMPLES = {
    "acetone.csv":         "acetone",
    "cleaner.csv":         "cleaner",
    "coffee.csv":          "coffee",
    "conditioner.csv":     "conditioner",
    "finger.csv":          "finger",
    "isopropanol.csv":     "isopropanol",
    "leaf.csv":            "leaf",
    "lotion.csv":          "lotion",
    "orangepeel.csv":      "orange_peel",
    "paper.csv":           "paper",
    "paperplasticcup.csv": "paper_plastic_cup",
    "plastic bag.csv":     "plastic_bag",
    "plastic cap.csv":     "plastic_cap",
    "plastic glove.csv":   "plastic_glove",
    "plasticwrapper.csv":  "plastic_wrapper",
    "salt.csv":            "salt",
    "shampoo.csv":         "shampoo",
    "soap.csv":            "soap",
    "sugar.csv":           "sugar",
    "sunscreen.csv":       "sunscreen",
    "water.csv":           "water",
}

count = 0
for raw_name, clean_name in SAMPLES.items():
    path = os.path.join(PROJECT, "data", raw_name)
    df = pd.read_csv(path, header=None, names=["wavenumber", "transmittance"])
    # Transmittance is already in percent; convert to absorbance
    # Clip to avoid log(0) — any T <= 0 gets a floor of 0.001 %
    t_clipped = df["transmittance"].clip(lower=0.001)
    df["absorbance"] = -np.log10(t_clipped / 100.0)
    out = os.path.join(SCRUBBED, f"{clean_name}.csv")
    df.to_csv(out, index=False, float_format="%.6f")
    count += 1

print(f"Wrote {count} cleaned CSVs to {SCRUBBED}")
