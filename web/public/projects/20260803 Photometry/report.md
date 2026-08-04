---
project: Photometry
title: "Photometry"
sciences:
  - Astronomy
---

<p class="lede">SW Lacertae is a pair of stars orbiting so close that each eclipses the other every few hours. Measuring its brightness across 510 exposures caught one of those eclipses whole — 83 minutes of lead-in, the floor, and 119 minutes of egress — and timed the moment of minimum to <strong>±2.6 minutes</strong>. The eclipse is 0.713 magnitudes deep and symmetric to within a hundredth of a magnitude.</p>


## What photometry measures

<div class="step">

### Brightness is also only ever relative

<!-- TO WRITE. The same idea as the Astrometry report's opening, in the other
     dimension: you do not measure how bright a star is, you measure how bright
     it is compared with its neighbours in the same frame. Anything that dims
     the target — cloud, altitude, dew — dims the comparisons too and divides
     out. That is what "differential" means. Five comparison stars here, which
     is the reducer's maximum. -->

</div>

<div class="step">

### Why an eclipsing binary is the right first target

<!-- TO WRITE. Two stars, one orbit, and the light curve repeats on a known
     period (7.70 hr). You know what shape to expect, so the measurement can be
     checked against itself, and against TESS, which has observed the same star
     from space in three sectors. -->

</div>


## The nights

<div class="step">

### Two runs, and only the second counts

<!-- TO WRITE. 2026-07-31 caught a minimum at the very start of coverage — the
     floor and the egress but no ingress, which is not a quotable timing however
     clean the night is. 2026-08-02/03 bracketed one properly. Say why an
     un-bracketed minimum cannot be timed. -->

<div class="result">
<strong>510 subs over 200 min</strong>, all 510 through the noise cut · 44 % phase coverage, 0.201 → 0.633
</div>

</div>

<div class="step">

### The photometric floor

<div class="result">
Comparison-star scatter <strong>0.072 mag</strong> — the number that sets which variables are reachable at all
</div>

<!-- TO WRITE. Per-point scatter on the target is 0.257 mag; the comparison
     floor is what says whether an amplitude is measurable. -->

</div>


## Reading the result

<div class="step">

### Timing the minimum

<div class="result">
<p class="big">HJD 2461255.78416 ± 0.00182 d</p>
<p>±2.6 min, on the <strong>primary</strong> minimum at phase 0.3600.</p>
</div>

<!-- TO WRITE. Kwee–van Woerden. And the error bar is the part worth arguing
     about: the formula's own answer is 1.80 min, which describes one parabola
     fit rather than the measurement. Re-running across nine sensible choices of
     reflection reach and trial window moves the epoch 5.6 min peak to peak, so
     the spread is 1.91 min and the quoted number adds the two in quadrature.
     Quoting the formal error alone would have overstated the result about
     twofold. -->

</div>

<div class="step">

### Amplitude, and a trap in it

<div class="result">
<strong>0.713 mag</strong> on binned medians
</div>

<!-- TO WRITE. Raw maximum minus minimum of single points reads 1.518 mag, which
     is 0.805 mag of per-point noise sitting on top of a real 0.713. The
     inflation is larger than the signal, and it GROWS with frame count rather
     than converging, because the extremes of a noisy sample keep finding
     further extremes. Only binned medians can be compared against a catalogue.
     This is the same shape of error as the raw-width scatter in the
     Spectroscopy report — a statistic that looks like a measurement and is
     actually a property of the sampling. -->

</div>

<div class="step">

### Testing for the O'Connell effect

<div class="result">
Symmetry about minimum <strong>−0.001 ± 0.011 mag</strong>, −0.1σ. No effect detected.
</div>

<!-- TO WRITE. And the first attempt was wrong, which is the lesson: it found
     +0.179 mag by comparing phase < 0.28 against phase > 0.58 around a minimum
     at 0.36 — that is 0.08–0.16 before against 0.22–0.27 after, so it measured
     the light curve's own shape at unequal offsets rather than an asymmetry.
     Pairing equal distances gives −0.001 ± 0.011, the six bins alternate in
     sign, and chi²/dof is 3.8. Scatter, not a starspot. -->

</div>

<div class="step">

### Which minimum is which

<!-- TO WRITE. This matters and is invisible without whole-cycle coverage,
     because one minimum has no second depth to compare against. Folding all
     three TESS sectors on the VSX ephemeris settles it — the primary sits at
     phase ~0.38, so the 07-31 run's faintest point at 0.908 was the SECONDARY.

     | Sector | min A phase | depth | min B phase | depth | primary |
     |---|---|---|---|---|---|
     | s0016 (2019.7) | 0.4020 | 0.612 | 0.8985 | 0.535 | A |
     | s0056 (2022.7) | 0.3953 | 0.594 | 0.8954 | 0.499 | A |
     | s0083 (2024.7) | 0.3841 | 0.738 | 0.8861 | 0.515 | A |

     Read the right way that night is the project's best correspondence result:
     a 30 mm scope agreeing with a space telescope to 10 minutes across a
     1.9-year gap, 0.9080 against TESS s83's 0.8861. -->

</div>
