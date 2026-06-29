---
project: IR Spectroscopy
tech:
  - Spectroscopy
title: "IR Spectroscopy - Test Run"
sciences:
  - Chemistry
---

<div class="photo-grid" id="photo-grid">
  <img id="photo-0" alt="Experiment photo">
  <img id="photo-1" alt="Experiment photo">
  <img id="photo-2" alt="Experiment photo">
  <img id="photo-3" alt="Experiment photo">
</div>
<button class="shuffle-btn" onclick="shufflePhotos()">Shuffle Photos</button>

<div class="section-heading"><h2>Setup</h2><span class="section-date">April 19th 2026</span></div>

IR Spectroscopy identifies polar covalent bonds in a sample by measuring which infrared frequencies it absorbs. Different functional groups — O-H, C=O, C-H, N-H — vibrate at characteristic frequencies, producing a unique absorption fingerprint for each compound.

A background spectrum was collected first. The IR beam reflects inside the diamond crystal, an evanescent wave penetrating microns into the pressed sample — no prep, measure as-is. The Nicolet 380 applies background correction automatically and exports raw spectra to <a href="https://github.com/vivianweidai/science/tree/main/public/research/projects/20260419%20IR%20Spectroscopy/data" rel="noopener">CSV</a> (wavenumber in cm⁻¹, transmittance in %); the cleaning <a href="https://github.com/vivianweidai/science/blob/main/public/research/projects/20260419%20IR%20Spectroscopy/output/clean_data.py" rel="noopener">pipeline</a> parses the headerless files, converts to absorbance via A = −log₁₀(T/100) (Beer-Lambert) and saves 21 cleaned CSVs to a <a href="https://github.com/vivianweidai/science/tree/main/public/research/projects/20260419%20IR%20Spectroscopy/output/scrubbed" rel="noopener">scrubbed</a> folder. All overlays were generated in the analysis <a href="https://github.com/vivianweidai/science/blob/main/public/research/projects/20260419%20IR%20Spectroscopy/output/ir_analysis.ipynb" rel="noopener">notebook</a>, reproducible on <a href="https://colab.research.google.com/github/vivianweidai/science/blob/main/public/research/projects/20260419%20IR%20Spectroscopy/output/ir_analysis.ipynb" rel="noopener">colab</a>.

| Toolkit | Details |
|---------|---------|
| Instrument | Thermo Scientific Nicolet 380 FT-IR Spectrometer — bulk samples, ~550–4000 cm⁻¹ |
| Mode | Attenuated Total Reflectance (ATR) — sample pressed onto the diamond crystal |
| Samples | 21 — solvents, food/minerals, personal care, polymers, paper, biological, control |
| Software | Thermo Scientific OMNIC 8 |

## Results

<div class="tabs">
  <input type="radio" name="chem-tab" id="chem-oh">
  <input type="radio" name="chem-tab" id="chem-ch">
  <input type="radio" name="chem-tab" id="chem-co">
  <input type="radio" name="chem-tab" id="chem-mixed">
  <input type="radio" name="chem-tab" id="chem-cellulose">
  <input type="radio" name="chem-tab" id="chem-protein">
  <input type="radio" name="chem-tab" id="chem-ionic">

  <div class="chem-tab-labels tab-labels">
    <label for="chem-oh">O–H Dominant</label>
    <label for="chem-ch">C–H Dominant</label>
    <label for="chem-co">Carbonyl</label>
    <label for="chem-mixed">Organic</label>
    <label for="chem-cellulose">Cellulose</label>
    <label for="chem-protein">Protein</label>
    <label for="chem-ionic">Ionic</label>
  </div>

  <div class="tab-content" id="content-chem-oh">
    <img src="output/images/chem_oh_spectrum.png" alt="O–H dominant spectra" class="result-img">
    <p>Shared broad O–H 3,200–3,600 cm⁻¹ with different fingerprints.</p>
  </div>

  <div class="tab-content" id="content-chem-ch">
    <img src="output/images/chem_ch_spectrum.png" alt="C–H dominant spectra" class="result-img">
    <p>Shared C–H doublet 2,920/2,850 cm⁻¹ + 1,460 cm⁻¹ bend; no heteroatoms, so spectra overlap tightly.</p>
  </div>

  <div class="tab-content" id="content-chem-co">
    <img src="output/images/chem_co_spectrum.png" alt="Carbonyl spectra" class="result-img">
    <p>Shared C=O at ~1,715 cm⁻¹; ketone in acetone, ester/ketone UV filters in sunscreen.</p>
  </div>

  <div class="tab-content" id="content-chem-mixed">
    <img src="output/images/chem_mixed_spectrum.png" alt="Mixed organic spectra" class="result-img">
    <p>No single peak wins; busy across every region.</p>
  </div>

  <div class="tab-content" id="content-chem-cellulose">
    <img src="output/images/chem_cellulose_spectrum.png" alt="Cellulose spectra" class="result-img">
    <p>Shared cellulose O–H + glycosidic C–O at 1,000–1,150 cm⁻¹; cup adds polyethylene C–H, leaf adds cuticle wax.</p>
  </div>

  <div class="tab-content" id="content-chem-protein">
    <img src="output/images/chem_protein_spectrum.png" alt="Protein / amide spectra" class="result-img">
    <p>Shared amide I 1,640 cm⁻¹ + II 1,540 cm⁻¹; keratin in finger, mimicked by glove's nitrile.</p>
  </div>

  <div class="tab-content" id="content-chem-ionic">
    <img src="output/images/chem_ionic_spectrum.png" alt="Ionic spectra" class="result-img">
    <p>No covalent bonds, no IR-active vibrations; flat baseline — why NaCl makes classical IR-transparent windows.</p>
  </div>
</div>

<div id="technology" class="tech-table-wrap">
<div class="tech-table">
<div class="tech-table-header">Technology</div>
<ul class="updates-list">
  <li data-subj="chem"><span class="update-name"><a href="/research/technology/chemistry/Spectroscopy/">Spectroscopy</a></span> <span class="update-desc">Bonds, absorbance, chirality</span> <a class="chip chem" href="/research/#chem">Chemistry</a></li>
</ul>
</div>
</div>
