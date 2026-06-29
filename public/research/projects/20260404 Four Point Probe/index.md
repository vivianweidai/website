---
project: Four-Point Probe
tech:
  - Engineering
  - Publishing
title: "Four-Point Probe of Sheet Resistance"
sciences:
  - Physics
---

<div class="photo-grid" id="photo-grid">
  <img id="photo-0" alt="Experiment photo">
  <img id="photo-1" alt="Experiment photo">
  <img id="photo-2" alt="Experiment photo">
  <img id="photo-3" alt="Experiment photo">
</div>
<button class="shuffle-btn" onclick="shufflePhotos()">Shuffle Photos</button>

<div class="section-heading"><h2>Overview</h2><span class="section-date">April 4th 2026</span></div>

**Sheet resistance** (Ω/□) — how easily current flows across a surface, independent of thickness. The four-point probe drives current through the outer pair and senses voltage across the inner pair, cancelling contact resistance and leaving only the sample's own resistance.

| Toolkit | Details |
|---------|---------|
| Instrument | Jandel RM3 Four-Point Probe |
| Technique | Four-point probe — separate current and voltage pairs eliminate contact resistance |
| Measurement | Sheet resistance (Ω/□) |

## Setup

<div class="hero-single"><img src="photos/setup/setup39.jpeg" alt="Tri-band penny under four-point probe"></div>

| Category | Items |
|----------|-------|
| Coins | quarter, penny (unpolished / semi-polished / fully polished) |
| Household metals | stainless steel spoon, aluminum foil, metal washer, house key |
| Biological | leaf |
| Other | DVD, paper cardboard |

Conductive samples gave readings; non-conductive ones returned Contact Limit or Out of Range. The penny was sanded into three bands — untouched copper, lightly polished, fully sanded to zinc — to test surface effects. Raw data were photographs of the instrument display, manually transcribed into a CSV; the raw photos are in the <a href="https://github.com/vivianweidai/science/tree/main/public/research/projects/20260404%20Four%20Point%20Probe/photos" rel="noopener">photos</a> directory and the scrubbed <a href="https://github.com/vivianweidai/science/blob/main/public/research/projects/20260404%20Four%20Point%20Probe/output/four_point_probe_readings.csv" rel="noopener">CSV</a> is in the <a href="https://github.com/vivianweidai/science/tree/main/public/research/projects/20260404%20Four%20Point%20Probe/output" rel="noopener">output</a> directory.

## Results

Fifty-six valid readings at 9 µA. Three non-conductive samples (leaf, DVD, paper cardboard) returned Contact Limit; one <a class="no-preview" href="https://vivianweidai.com/research/projects/20260404%20Four%20Point%20Probe/photos/setup/setup89.jpeg">washer reading was excluded</a> — current had been left at 20 nA after testing insulators. Quarter and spoon ranked most conductive; brass key least. Two surprises: sanding the penny from copper to zinc *increased* resistance (47.3 → 50.1 Ω/□), and flipping the aluminum foil also raised it (48.1 → 54.7 Ω/□) — matte and shiny sides differ measurably. The wide ranges reflect probe drift on irregular surfaces (four-point probes assume flat, uniform samples), not true variation — readings bounced around continuously and never really settled, even when held still on the same sample. Full per-sample plots in the analysis <a href="https://github.com/vivianweidai/science/blob/main/public/research/projects/20260404%20Four%20Point%20Probe/output/four_point_probe_analysis.ipynb" rel="noopener">notebook</a> or on <a href="https://colab.research.google.com/github/vivianweidai/science/blob/main/public/research/projects/20260404%20Four%20Point%20Probe/output/four_point_probe_analysis.ipynb" rel="noopener">colab</a>.

<img src="output/mean_sheet_resistance.png" alt="Mean sheet resistance by sample" class="result-img">

<div id="technology" class="tech-table-wrap">
<div class="tech-table">
<div class="tech-table-header">Technology</div>
<ul class="updates-list">
  <li data-subj="comp"><span class="update-name"><a href="/research/technology/computing/Publishing/">Publishing</a></span> <span class="update-desc">Data code notebooks</span> <a class="chip comp" href="/research/#comp">Computing</a></li>
  <li data-subj="phys"><span class="update-name"><a href="/research/technology/physics/Engineering/">Engineering</a></span> <span class="update-desc">Circuits and fabrication</span> <a class="chip phys" href="/research/#phys">Physics</a></li>
</ul>
</div>
</div>
