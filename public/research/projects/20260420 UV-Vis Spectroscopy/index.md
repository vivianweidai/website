---
project: UV-Vis Spectroscopy
tech:
  - Spectroscopy
title: "UV-Vis Spectroscopy - Test Run"
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

<div class="section-heading"><h2>Setup</h2><span class="section-date">April 20th 2026</span></div>

One set of samples through two instruments: the UV-2550 measures which colors of light a compound absorbs and how greedily; the FluoroMax-3 measures which colors come back out. The samples are all **fluorophores** — molecules that catch a photon and release a longer-wavelength one. The gap between the two peaks is the **Stokes shift**.

| Toolkit | Details |
|----------|---------|
| Instruments | Shimadzu UV-2550 UV-Vis Spectrophotometer, Horiba Jobin Yvon FluoroMax-3 Spectrofluorometer, and PerkinElmer Lambda 750 UV-Vis-NIR Spectrophotometer |
| Cuvettes | 10 mm fluorescence-grade quartz, four clear sides |
| Software | UVProbe (Shimadzu), FluorEssence (Horiba) |
| Blanks | Distilled water (aqueous), 95% ethanol (ethanol samples) |

## Method

<div class="hero-single"><img src="photos/samples/samples3.jpeg" alt="Eight labeled amber stock bottles — six fluorophore samples plus two blank solvents"></div>

Six fluorophores plus two blanks. Four water-baseline samples first — quinine (antimalarial, from tonic water), yellow highlighter (fluorescein-family dye), pink highlighter (rhodamine-family dye), salicylate (pharmaceutical, from aspirin + NaHCO₃) — then re-baseline and run two ethanol extracts: curcumin (turmeric) and green tea extract.

The UV-2550 yields λ<sub>max</sub> and A across 200–800 nm; both feed the FluoroMax — λ<sub>max</sub> sets λ<sub>ex</sub>, A sets the dilution factor D = A / 0.05 (the FluoroMax needs A ≈ 0.05 to avoid inner-filter effects). Stocks start at 1 drop in 3 mL solvent and dilute iteratively to land in the 0.3–0.8 A sweet spot; each baseline is followed by its solvent blank rescanned as a sample to confirm it returns flat near zero. The FluoroMax then runs two scans per sample — emission (fix λ<sub>ex</sub>, sweep λ<sub>em</sub>) and excitation (fix λ<sub>em</sub>, sweep λ<sub>ex</sub>). An EEM scan is planned for green tea extract. Raw files live under <a href="https://github.com/vivianweidai/science/tree/main/public/research/projects/20260420%20UV-Vis%20Spectroscopy/data" rel="noopener">data</a>; all UV-Vis, fluorescence and Lambda 750 plots were generated in the analysis <a href="https://github.com/vivianweidai/science/blob/main/public/research/projects/20260420%20UV-Vis%20Spectroscopy/output/uv_spectroscopy.ipynb" rel="noopener">notebook</a>, reproducible on <a href="https://colab.research.google.com/github/vivianweidai/science/blob/main/public/research/projects/20260420%20UV-Vis%20Spectroscopy/output/uv_spectroscopy.ipynb" rel="noopener">colab</a>.

## Results

### UV-Vis Absorption

<div class="tabs">
  <input type="radio" name="uv-tab" id="uv-overlay" checked>
  <input type="radio" name="uv-tab" id="uv-baseline">
  <input type="radio" name="uv-tab" id="uv-quinine">
  <input type="radio" name="uv-tab" id="uv-yellow">
  <input type="radio" name="uv-tab" id="uv-pink">
  <input type="radio" name="uv-tab" id="uv-salicylate">

  <div class="tab-labels">
    <label for="uv-overlay">Overlay</label>
    <label for="uv-baseline">Baseline</label>
    <label for="uv-quinine">Quinine</label>
    <label for="uv-yellow">Yellow HL</label>
    <label for="uv-pink">Pink HL</label>
    <label for="uv-salicylate">Salicylate</label>
  </div>

  <div class="tab-content" id="content-uv-overlay">
    <img src="output/images/uvvis_overlay.png" alt="UV-Vis overlay — four water samples" class="result-img">
    <p>Four fluorophores; only yellow HL (A = 0.40 at 454 nm) hit the 0.3–0.8 sweet spot.</p>
  </div>
  <div class="tab-content" id="content-uv-baseline">
    <img src="output/images/uvvis_baseline.png" alt="Distilled water baseline" class="result-img">
    <p>Distilled water vs water baseline — flat across 200–800 nm.</p>
  </div>
  <div class="tab-content" id="content-uv-quinine">
    <img src="output/images/uvvis_quinine.png" alt="Quinine UV-Vis spectrum" class="result-img">
    <p>Quinoline π→π* at 347 nm; A = 0.10, over-diluted past target.</p>
  </div>
  <div class="tab-content" id="content-uv-yellow">
    <img src="output/images/uvvis_yellow.png" alt="Yellow highlighter UV-Vis spectrum" class="result-img">
    <p>Fluorescein-family xanthene π→π* at 454 nm; A = 0.40 in sweet spot.</p>
  </div>
  <div class="tab-content" id="content-uv-pink">
    <img src="output/images/uvvis_pink.png" alt="Pink highlighter UV-Vis spectrum" class="result-img">
    <p>Rhodamine-family π→π* at 532 nm; A = 0.05, over-diluted at ⅙ drop.</p>
  </div>
  <div class="tab-content" id="content-uv-salicylate">
    <img src="output/images/uvvis_salicylate.png" alt="Salicylate UV-Vis spectrum" class="result-img">
    <p>Hydroxybenzoate π→π* at 307 nm — UV-only; A = 0.06.</p>
  </div>
</div>

### Fluorescence

<div class="tabs">
  <input type="radio" name="flu-tab" id="flu-quinine" checked>
  <input type="radio" name="flu-tab" id="flu-yellow">
  <input type="radio" name="flu-tab" id="flu-pink">
  <input type="radio" name="flu-tab" id="flu-salicylate">

  <div class="tab-labels">
    <label for="flu-quinine">Quinine</label>
    <label for="flu-yellow">Yellow HL</label>
    <label for="flu-pink">Pink HL</label>
    <label for="flu-salicylate">Salicylate</label>
  </div>

  <div class="tab-content" id="content-flu-quinine">
    <img src="output/images/fluoromax_quinine.png" alt="Quinine excitation and emission spectra" class="result-img">
    <p>λ<sub>ex</sub> 350, λ<sub>em</sub> 445, Stokes 95 nm — the blue tonic-water glow.</p>
  </div>
  <div class="tab-content" id="content-flu-yellow">
    <img src="output/images/fluoromax_yellow.png" alt="Yellow highlighter excitation and emission spectra" class="result-img">
    <p>λ<sub>ex</sub> 403, λ<sub>em</sub> 512, Stokes 109 nm — perturbed xanthene (pure fluorescein ~30 nm).</p>
  </div>
  <div class="tab-content" id="content-flu-pink">
    <img src="output/images/fluoromax_pink.png" alt="Pink highlighter emission only" class="result-img">
    <p>Emission only; λ<sub>em</sub> 582 (near 585 prediction); rhodamine red with dimer tail.</p>
  </div>
  <div class="tab-content" id="content-flu-salicylate">
    <img src="output/images/fluoromax_salicylate.png" alt="Salicylate excitation and emission spectra" class="result-img">
    <p>ESIPT: λ<sub>ex</sub> 301, λ<sub>em</sub> 409, Stokes 108 nm — excited-state proton transfer.</p>
  </div>
</div>

### Solvent NIR

<img src="output/images/lambda750_water.png" alt="Lambda 750 distilled water NIR spectrum" class="result-img">

Distilled water on the Lambda 750. O–H overtones at ~970, 1200 and 1450 nm; detector pinned past ~1500 nm.
