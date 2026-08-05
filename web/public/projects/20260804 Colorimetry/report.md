---
project: Colorimetry
title: "Colorimetry"
sciences:
  - Astronomy
---

<p class="lede">A colour camera is three cameras interleaved, and photometry had been throwing two of them away. Recovered, they give two colour indices per star — enough, in principle, to separate how hot a star is from how much dust sits in front of it. Before any of that could be believed, the telescope itself had to be measured: our own optics make a star at the edge of the frame read <strong>0.20 magnitudes redder</strong> than the same star at the centre, which is larger than the entire real colour spread of the field.</p>

## What a colour is

<div class="step">

### A star's colour is its temperature

<!-- TO WRITE. The blackbody again, but read sideways. Spectroscopy read the
     absorption lines cut INTO the continuum; colorimetry reads the shape of the
     continuum itself. Wien: hotter peaks bluer. A colour index is the crudest
     possible spectrum — two numbers instead of two thousand — and the trade is
     that it costs one exposure of an ordinary image instead of a grating, a
     framing fight and a wavelength solution. Every star in the frame at once,
     rather than one star at a time. Cross-reference the Spectroscopy report's
     "The star makes a continuum". -->

</div>

<div class="step">

### Dust reddens, and reddening imitates cooling

<!-- TO WRITE. Interstellar dust grains scatter blue light more efficiently than
     red, so a star seen through dust arrives both dimmer and redder. The trap is
     that this is the SAME direction on a single colour index as being cool. One
     number cannot tell a hot star behind dust from a cool star in clear sky —
     they land on the same value. This degeneracy is the whole reason the project
     needs two indices rather than one, and it is why `physics.color` returns a
     pair. -->

<div class="term">

**A colour index** is the difference of two magnitudes — here TG − TR, the green
band minus the red. Because magnitudes are logarithmic, a difference of magnitudes
is a RATIO of brightnesses, so a colour index is independent of how far away the
star is and of how big the telescope is. It is a property of the light itself.

**Reddening** is what dust does. **Extinction** is the dimming that comes with it.
They are the same physical process measured on two different axes.

</div>

</div>

<div class="step">

### Two colours break the tie

<!-- TO WRITE. Temperature moves a star along one locus in the plane of (TB-TG)
     against (TG-TR); dust moves it along a different direction, the reddening
     vector, which is set by the physics of the grains and not by the star. Two
     axes, two effects, and they point different ways — so the position in the
     plane determines both. This is the diagram the whole project exists to draw. -->

</div>

## Three cameras in one

<div class="step">

### The Bayer mosaic

<!-- TO WRITE. Every pixel on this sensor sits under a coloured dye. The pattern
     is GRBG: in each 2x2 tile, two green, one red, one blue. So a single exposure
     is not one image but three interleaved ones, at different sampling rates,
     through three different filters. Include the tile diagram. -->

</div>

<div class="step">

### What photometry threw away

<!-- TO WRITE. Photometry's `green()` averages the two green pixels of each tile
     and discards the red and blue quarters — and that is CORRECT for photometry,
     because a raw mosaic mixes three filter throughputs and anything summed
     across it has no defined passband. But "do not sum them" and "do not use
     them" are different statements. This project is the second statement being
     retracted: 50% of the sensor was being used and 50% was being deleted, and
     the deleted half carries colour.

     The founding measurement: 20 stars, 12 plate-solved frames, from photometry's
     own SW Lac run. One common colour across all of them is rejected at
     chi-squared 897.2 / 19 dof. The colours are real and separable from noise. -->

<div class="result">
<strong>χ² = 897.2 / 19 dof</strong> against the hypothesis that every star has the same colour · p = 4.5 × 10⁻¹⁷⁸
</div>

</div>

<div class="step">

### These are not Johnson B, V and R

<!-- TO WRITE. AAVSO calls consumer-camera bands TB, TG, TR precisely because
     they are not the standard ones. TG is a decent match to Johnson V. TB and TR
     are broad, overlapping consumer dyes and are poor matches to B and R. How
     poor is unmeasured, and that unmeasured quantity sets the error bar on every
     temperature and every reddening this project will ever quote. State it here
     rather than in a footnote. -->

</div>

## Measuring the instrument before measuring the sky

<div class="step">

### The frame is not uniform

The blocking discovery, and the one that could have ended the project: a star near the edge of the frame reads redder than the same star near the centre. Not because it is redder — because of where it is.

<div class="result">
<strong>TG − TR runs +0.204 ± 0.024 mag</strong> from centre to edge, an 8.5σ measurement on 351 stars
</div>

The size is what makes it fatal rather than merely annoying. The real colour spread between different stars in that field is about 0.12 mag. The instrument's own gradient is larger than the entire signal it is supposed to measure.

<!-- TO WRITE. Spell out the consequence with the cluster case: a cluster's stars
     are spread across the frame by construction, so every colour-magnitude
     diagram would be smeared along the colour axis by our own optics — and it
     would still look like a perfectly plausible diagram. That is the danger. Not
     a wrong answer that announces itself, but a believable one. -->

</div>

<div class="step">

### Is it the star, or is it where the star is?

<!-- TO WRITE. The obvious test — compare stars near the edge with stars near the
     centre — cannot distinguish the two explanations on its own. If edge stars
     read redder, that could be the optics, or the field could simply happen to
     have redder stars around its rim. With enough stars coincidence becomes
     implausible, but the test still ASSUMES the field has no colour pattern of
     its own, and a star cluster breaks that assumption by construction. -->

</div>

<div class="step">

### Watching one star move

<!-- TO WRITE. The assumption-free version: instead of comparing different stars
     at different places, follow ONE star as it moves around the frame. If its
     colour changes, the star did not change — the instrument did. This is
     self-calibration, and it is standard practice rather than anything invented
     here; large surveys use it to solve their flat fields rather than trusting
     lab calibration. Credit that explicitly.

     It normally costs telescope time, because you have to dither on purpose. -->

</div>

<div class="step">

### A fault becomes the method

<!-- TO WRITE. We did not have to dither. The mount slipped all through both
     runs — the same fault that cost 9.4% of the XZ Cyg subs in the Photometry
     report — and it walked the field 20 to 30 arcminutes across each night.
     Every star sampled a range of distances from the frame centre for free.
     The defect that ruined subs is what makes the calibration possible.

     ⚠️ AND THEN SELF-CALIBRATION DID NOT WORK, which is the honest part of this
     section and must not be dropped. Its lever arm is the amount a single star's
     radius changes, and that is only 0.12 of the frame radius against ~0.1 mag of
     photometric noise. The fit is nearly degenerate: a per-band radial term is
     almost indistinguishable from each star simply being that brightness. Tested
     against progressively brighter subsamples the answer wandered between +0.39
     and +0.73 with no sign of converging, while the direct method held at +0.13
     to +0.21 across the same cuts. The stable estimator won on evidence, not on
     which one was more elegant.

     Two more corrections belong here because they were the real work: an error
     bar that was seven times too small because the bootstrap resampled
     measurements rather than stars, and a detection threshold that silently
     capped the sample at 91 stars when the frames hold about a thousand. -->

</div>

<div class="step">

### What a radial model cannot see

<!-- TO WRITE. State the assumption plainly. The correction fitted here is a
     function of distance from the frame centre and nothing else. That catches
     vignetting and a symmetric focus gradient, which are the likely causes. It is
     blind to anything that is not circularly symmetric: a tilted sensor, a
     decentred element, or a gradient in the Bayer dyes across the chip would all
     produce a colour pattern that this model cannot represent and would quietly
     average away.

     Testing for those needs the same star at many positions across a GRID rather
     than at many radii — a deliberate dither pattern, not a drifting mount. Say
     what it would take. Also note that r and r^2 fit equally well here (rms
     0.2816 against 0.2823), so the data supports a one-parameter radial term but
     does not determine its shape. -->

</div>

## From colour to physics

<div class="step">

### The colour-magnitude diagram

<!-- TO WRITE. Many stars, one epoch — the new axis this project adds, since every
     other astronomy result here is one object across many epochs. Main sequence,
     giant branch, and the turnoff where they meet. Needs no ephemeris and no
     return visit.

     State the reach limit honestly and up front: an open cluster's main sequence
     at V 7-13 is comfortably inside a 30 mm aperture; a globular's turnoff near
     V 19 is not, so those give an upper red giant branch and no cluster age. -->

</div>

<div class="step">

### The two-colour diagram and the reddening vector

<!-- TO WRITE. The plane where temperature and dust separate. Draw the reddening
     vector as an arrow with its length labelled — a CMD without one invites the
     reader to read temperature straight off the horizontal axis, which is exactly
     the mistake the second colour exists to prevent. -->

</div>

<div class="step">

### Putting it on a standard system

<!-- TO WRITE. Instrumental indices say star A is redder than star B and nothing
     else. APASS covers our fields at V 10-17; cross-match by position, regress
     instrumental TG-TR against catalogued B-V, and QUOTE THE SCATTER — that
     number is the error bar on every temperature and reddening downstream, and
     it decides whether the Cepheid distance in the Photometry report is worth
     attempting at all. If the scatter is large that is a result, not a failure. -->

</div>

## The reddening ladder

<div class="step">

### Three clusters, one prediction

<!-- TO WRITE. The actual experiment, and the reason the three clusters are one
     entry rather than three. A single CMD is a picture: you draw it, it looks
     like a main sequence, and nothing about it could come out wrong in a way you
     would notice. Three clusters at KNOWN, DIFFERENT reddenings is a test,
     because the two-colour diagram predicts in advance that each cluster's locus
     sits displaced along the reddening vector by a published amount.

     | Cluster | E(B−V) | Distance | Best months |
     |---|---|---|---|
     | NGC 752 | 0.023 | 483 pc | Sep–Dec |
     | NGC 1647 | 0.206 | 635 pc | Oct–Jan |
     | Double Cluster | 0.55 | 2,150 pc | Sep–Jan |

     All three from one homogeneous Gaia DR2 source (Cantat-Gaudin & Anders 2020),
     which matters more than the individual numbers: a ladder assembled from three
     papers would carry three systematics and test nothing.

     And say why the field term had to be fixed first — it is 72% of the closest
     rung's separation. Uncorrected, the experiment measures our optics. -->

</div>
