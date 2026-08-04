---
project: Astrometry
title: "Astrometry"
sciences:
  - Astronomy
---

<p class="lede">Fifty twenty-second exposures of the asteroid 3 Juno, measured against the fixed stars around it, put its position within <strong>1.35″</strong> of where JPL Horizons says it was. That residual is not the asteroid — Horizons knows Juno's orbit far better than a 30 mm telescope can measure it — so it is the error bar on every position this instrument will ever produce. A comet found by accident in an earlier night's frames gave the same answer by a different route.</p>


## What astrometry measures

<div class="step">

### A position is only ever relative

<!-- TO WRITE. The idea: you cannot measure where something is in the sky
     directly. You measure where it sits among stars whose positions are
     already known, and inherit their calibration. Introduce the catalogue
     (Gaia DR3) as the ruler. -->

</div>

<div class="step">

### Plate solving turns a picture into coordinates

<!-- TO WRITE. Already defined in the Spectroscopy report at the focal-length
     step; here it is the main event rather than an aside, so it needs the
     fuller version — pattern-matching the star field against a catalogue,
     what a WCS is, and what "residual" means for one. -->

</div>


## The night

<div class="step">

### Fifty subs of a moving target

<div class="result">
50 × 20 s subs over 37.5 min · median SNR 32 · <strong>6.2 px</strong> of motion against the fixed stars
</div>

<!-- TO WRITE. -->

</div>

<div class="step">

### Refitting the frames against Gaia

<div class="result">
Refit covered <strong>34 of 50</strong> frames · WCS residual <strong>2.02″ → 1.68″</strong> on a median of 36 Gaia stars
</div>

<!-- TO WRITE. The 22 % median gain is not the interesting part. The along-track
     systematic collapsing from −0.93″ to −0.04″ is, because that is what a real
     WCS correction looks like and noise does not do it. -->

</div>


## Reading the result

<div class="step">

### Observed minus computed

<div class="result">
<p class="big">O−C = 1.35″ median, 1.43″ rms</p>
<p>Along-track −0.04″ ± 0.75 · cross-track −1.15″ ± 0.60. Unrefit, the same frames give 1.74″ median.</p>
</div>

<!-- TO WRITE. -->

</div>

<div class="step">

### Where the error actually comes from

<!-- TO WRITE. This is the finding worth the most space. On a frame from the run
     the WCS sits 1.46″ from Gaia DR3 in Dec while Juno's residual in Dec is
     1.50″ — they agree to 0.04″, and they must, because Juno and the reference
     stars share a frame and inherit the same bias. So the centroid is already
     better than the frame's absolute calibration, which inverts the improvement
     plan: a better centroid buys nothing until the WCS is better. It was a
     prediction before the refit and the refit confirmed it.

     What it is not: not the catalogue epoch (propagating back to 2MASS 1999.5
     only moves 1.49″ → 1.22″); not field distortion (SIP shows no radial trend,
     2.39 / 1.40 / 1.41 / 2.70″ centre to corner); not refraction (the plate
     solve absorbs it, and the offset points 21° from the zenith anyway). What
     is left is astrometry.net's own accuracy. -->

</div>


## The comet that turned up

<div class="step">

### C/2024 J3, found serendipitously

<div class="result">
<strong>3.0″</strong> from a 399-frame shift-and-stack — one measurement, 4.3σ
</div>

<!-- TO WRITE. Note the statistics differ: the comet's 3.0″ is one measurement
     from a stack, Juno's 1.35″ is the median of 50 independent single-sub
     measurements. -->

</div>

<div class="step">

### Telling a comet from an asteroid

<!-- TO WRITE. Classification here is morphological — asteroids are inert rock
     and nothing sublimates, so they are never extended.

     | | FWHM | What it is |
     |---|---|---|
     | C/2024 J3, comet-aligned | 18.3″ | the object |
     | field stars, star-aligned | 14.5″ | the instrument, 55 stars |
     | field stars, comet-aligned | 19.8″ | control — must be wider, and is |

     The 1.27x ratio is the weaker half. The profile SHAPE is the strong half:
     peak-normalised, the comet holds 0.324 at 12.8″ where a star holds 0.094,
     and 0.235 at 16.5″ against 0.025. Between 9″ and 24″ it carries light the
     PSF does not have, and a halo cannot be faked by seeing.

     Widths combine in quadrature under convolution, so the intrinsic size is
     sqrt(18.3² − 14.5²) = 11.3″; at 3.445 AU that is a coma near 28,000 km —
     an upper bound, because the comet-aligned stack smears with ephemeris
     error. Deblended of a G = 14.94 neighbour the comet is about mag 14.2
     against Horizons' Tmag 14.90. -->

</div>
