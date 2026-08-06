---
project: Temperature
title: "Temperature"
sciences:
  - Astronomy
---

<p class="lede">The same Seestar and grating that labeled two stars by their absorption lines can also weigh their light against Vega's published spectrum, which removes the camera and leaves the star. What is left is a continuum, and a continuum is a temperature: <strong>Xi Draconis at 4260 K</strong>, measured rather than matched against a list.</p>

## What a label cannot tell you

<div class="step">

### Reading a star by its lines

The first spectroscopy report classified Vega as A0V from the depth of its hydrogen lines, and Xi Draconis as K2–K3 III from magnesium and iron bands, because on a star that cool the hydrogen lines are gone entirely.

Both of those are labels. We measured how deep a few absorption bands were, compared the pattern against a library of catalogued stars, and took the name of the closest match. Nothing in that procedure produces a physical quantity. It produces a rank.

</div>

<div class="step">

### Why the label survived a defective camera

The Seestar's sensor is a color camera. Red, green and blue filters sit over the pixels in a repeating mosaic, so when a grating spreads a star into a rainbow, different parts of that rainbow are recorded through different filters. The throughput jumps where one filter hands over to the next.

<div class="term">

**Band index.** The depth of an absorption band, measured against a straight line drawn between two clear stretches of continuum on either side of it. The line is the local baseline, so anything that changes slowly across those few nanometers divides straight out.

</div>

That local baseline is why the classification was never in danger. A band index only cares about the ten or twenty nanometers around one feature, and across a stretch that narrow the camera's distortion is close enough to a straight line to cancel. The label was sound the whole time.

Temperature is the opposite. Temperature is written in the overall slope of the light across hundreds of nanometers — the thing a local baseline throws away by design. To read it we needed the camera gone.

</div>

## Removing the camera

<div class="step">

### Using Vega as the ruler

Vega is the primary spectrophotometric standard of astronomy. Its true spectrum has been measured from space and published, wavelength by wavelength, in the CALSPEC database.

So the camera's distortion is recoverable by division. Photograph Vega, divide what we recorded by what Vega truly emits, and everything left over belongs to the instrument — every filter edge, the grating, the atmosphere on that night. Divide any other star by that curve and the instrument disappears.

</div>

<div class="step">

### Finding the error that made it fail

This had been tried before and recorded as a failure. Applied to Xi Draconis it made the match to a K giant worse, not better, and the blame had landed on the grating shifting between nights.

The real fault was upstream. The Vega spectrum being fed into the division had already had its continuum divided out by an earlier step, so it was flat before the calculation began. Dividing a flat line by Vega's true spectrum does not measure a camera. It measures Vega, upside down.

The check that settled it was to feed the correction a flat line with no star in it at all. It produced the same failure, very slightly worse. The star was not participating in its own result.

<div class="result">

Roughly <strong>90%</strong> of what had been called the instrument's fingerprint was Vega's own spectrum, inverted.

</div>

</div>

<div class="step">

### Measuring the response properly

Rebuilt from spectra that still carried their continuum, the curve changes character completely. Both filter handovers appear as sharp steps, marked here, and between them the response is smooth.

![](photos/figures/instrument_response.png)

The blue-to-green handover at 477 nm is a factor of 2.7. The green-to-red handover at 588 nm is a factor of 1.2. Neither is subtle, and neither is the star.

</div>

<div class="step">

### Testing it on a star it had never seen

A correction that only works on the star it came from is arithmetic, not calibration. The test is a different star: build the curve from Vega on one night, apply it to Xi Draconis shot five nights later, and ask whether the corrected shape matches a K giant better or worse than before.

Uncorrected, the overall shape of Xi Draconis's light best matched a K4III template — two subclasses too cool, because the camera was still in it making the star look redder than it is. Corrected, it matches K2III, which is what the catalogs list.

<div class="result">

The shape ranking moved from <strong>K4III</strong> to <strong>K2III</strong>, on a star that never entered the calibration and against a template that never entered the response.

</div>

</div>

## Where the correction is trustworthy

<div class="step">

### Splitting the leftover at the handovers

The correction works, but not perfectly, and the shape of what was left over turned out to be the most useful thing in the project. Dividing the corrected star by its template and plotting the ratio across the whole range gives this.

![](photos/figures/three_zones.png)

It is not a gentle curve with the ends drooping, which is what a general calibration error would look like. It is three flat zones with a jump at each handover. Between 477 and 588 nm the ratio sits on 1.0, meaning the correction is right there. Outside those marks it jumps.

<div class="result">

Between the handovers the calibration is good to <strong>3%</strong>. Outside them it is wrong, and the error is entirely in the two steps.

</div>

</div>

<div class="step">

### Finding that the steps move between nights

A filter is a piece of glass. Its handover should be a fixed property of the camera, identical every night. It is not.

With each star's own continuum divided out, the 477 nm step measures 2.75 on the night Vega was shot and 1.36 on the night Xi Draconis was shot — a factor of two. Frames taken within a single night agree far better than that, scattering by 5% and 13%. The step belongs to the mounting, and the grating had been unscrewed and refitted in between.

That is the whole remaining error. It also fixes the working rule for every night from now on: the standard star and the target have to be shot on the same mounting, without the grating coming off in between.

</div>

## Reading the temperature

<div class="step">

### Fitting the continuum inside the good zone

Restricting to 477–588 nm, where the calibration is trustworthy, the corrected continuum can be compared against real stellar spectra of known temperature.

![](photos/figures/temperature.png)

The white trace is Xi Draconis with the camera removed. The three colored curves are catalogued giants either side of it. Our star sits on the K3 curve, below K1 and above K5.

<div class="result">

Xi Draconis, <strong class="big">4260 K</strong>. The literature value for a K2 giant is 4390 K.

</div>

That agreement is at the level the noise allows. A continuum good to 3% constrains temperature to about ±100 K at these temperatures, and the two numbers differ by 130 K.

</div>

<div class="step">

### Not using a blackbody, and seeing why

A star radiates roughly as a blackbody, so the obvious move is to fit the Planck curve and read the temperature off it. The dotted line on the figure above is that fit, and it returns 4000 K — low by 390 K.

<div class="term">

**Line blanketing.** In a cool star, thousands of metal absorption lines crowd together at the blue end and remove flux wholesale. The continuum there sits well below a blackbody, so the star looks redder, and therefore cooler, than it is.

</div>

The error has the sign the mechanism predicts, and it bites hardest on exactly the cool stars this method works best on. So the comparison has to be against real stellar continua, which already carry the blanketing, not against an idealized curve. Being able to see the bias in the direction of the error is what separates a measurement from a fit that happens to return a number.

</div>

<div class="step">

### What the number is worth

Two things make 4260 K different from K2–K3 III.

It is a physical property of the star in physical units, arrived at by comparing our light to published light, rather than a name borrowed from the closest entry in a catalog. And it can be wrong. A label matched against a list is either the nearest match or it is not; a temperature can be checked against an independent measurement and disagree.

It also arrives by a route that shares nothing with the line method. The classification used four absorption band depths. The temperature used the overall slope with those same bands contributing almost nothing. Two independent observables, one answer.

The last part matters most for what comes next. Hydrogen lines vanish on cool stars, which was the central finding of the first report — the method has to change with the star. The continuum does not vanish. It is sharpest, in fact, on the coolest stars, exactly where the hydrogen method fails completely.

</div>
