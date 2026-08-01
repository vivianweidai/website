---
project: Cat Food Color Preference
title: "Red or Green, What Colored Cat Food does Mi Prefer?"
sciences:
  - Computing
---

<div class="photo-grid" id="photo-grid">
  <img id="photo-0" alt="Experiment photo">
  <img id="photo-1" alt="Experiment photo">
  <img id="photo-2" alt="Experiment photo">
  <img id="photo-3" alt="Experiment photo">
</div>
<button class="shuffle-btn" onclick="shufflePhotos()">Shuffle Photos</button>

<div class="section-heading"><h2>Overview</h2><span class="section-date">February 25th 2025</span></div>

Does a cat prefer red or green colored food? This experiment tested whether a British Shorthair cat (Mi) shows a statistically significant preference for red- or green-dyed cat food. Regular dry cat food was dyed with food coloring and presented in two side-by-side bowls over 30 days. The bowl Mi approached first was recorded as his preference for that day. A chi-squared test was used to determine whether the observed preference differed significantly from chance.

## Setup

| Toolkit | Details |
|----------|---------|
| Subject | British Shorthair cat (Mi) |
| Food | Regular dry cat food |
| Dye | Red and green food coloring |
| Serving | 10 pieces per bowl per trial |
| Duration | 30 days (August-September 2024) |

Colored cat food was prepared by mixing regular dry food with red and green food coloring in separate jars. Each day, two bowls were placed side by side — one with 10 red pieces and one with 10 green pieces. Bowl positions were alternated daily to control for side bias. The color Mi approached and began eating first was recorded as his preference. Remaining pieces, serving time, and food dye concentration were also tracked. Days where Mi did not eat from either bowl were excluded. After 30 days, a chi-squared goodness-of-fit test was applied to the observed preferences.

## Data

<div class="photo-grid three-col" id="data-grid">
  <img src="photos/data/data1.jpeg" alt="Data sheet">
  <img src="photos/data/data2.jpeg" alt="Data sheet">
  <img src="photos/data/data3.jpeg" alt="Data sheet">
</div>

Raw data was recorded on handwritten data sheets and photographed. Variables tracked per trial include: date, serving number, pieces served and remaining, bowl position (left/right), serving time, and food dye drops used. The original handwritten data sheets are photographed and available in <a href="https://github.com/vivianweidai/website/tree/main/web/public/projects/20250225%20Catfood/photos/data" rel="noopener">photos</a>. The preference tallies were transcribed from these handwritten records into <a href="https://github.com/vivianweidai/website/blob/main/web/public/projects/20250225%20Catfood/output/catfood_summary.csv" rel="noopener">catfood_summary.csv</a>.

## Results

Over 30 days, Mi chose red on 13 days and green on 17 days. A chi-squared goodness-of-fit test with one degree of freedom yielded a test statistic of 0.533, well below the critical value of 3.841 at 95% confidence. The null hypothesis (no color preference) was not rejected. **Mi shows no statistically significant preference for red or green cat food.** The chi-squared test and supporting plots are in the analysis <a href="https://github.com/vivianweidai/website/blob/main/web/public/projects/20250225%20Catfood/output/catfood_analysis.ipynb" rel="noopener">notebook</a> and are reproducible on <a href="https://colab.research.google.com/github/vivianweidai/website/blob/main/web/public/projects/20250225%20Catfood/output/catfood_analysis.ipynb" rel="noopener">colab</a>. See also the full <a href="https://github.com/vivianweidai/website/blob/main/web/public/projects/20250225%20Catfood/output/20250225%20Catfood.pdf" rel="noopener">written report</a>.
