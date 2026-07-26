---
project: Stargazing
tech:
  - Telescopes
title: "Stargazing"
sciences:
  - Astronomy
---

<div class="sky-hero">
  <video src="media/sun-loop.mp4" poster="media/sun-loop-poster.jpg" autoplay loop muted playsinline preload="auto" aria-label="The Sun in white light, sunspot groups crossing the disk"></video>
  <p class="sky-hero-cap">The Sun in white light — a 6-second look through the solar filter, July 24</p>
</div>

<div class="project-meta">July 2026<br>ZWO Seestar S30 Pro with Tilting Wedge</div>

## Overview

A running gallery of what the back-yard scope has caught. Nothing here is a measurement — these are the frames that came out looking like something, kept because they are worth looking at.

The Seestar shoots and exports **portrait**, 2160 × 3840, so the whole gallery is built that way: tall tiles, videos looping in place. Everything below is a stack of 10-second sub-frames (5 s for the fastest one) taken through the IR-cut filter, then cropped, flattened and stretched — no other retouching.

## Setup

| Toolkit | Details |
|----------|---------|
| Instrument | ZWO Seestar S30 Pro with Tilting Wedge |
| Optics | 160 mm focal length, IR-cut filter, gain 200 |
| Sub-frames | 10 s each (5 s on RR Lyrae); 5 to 425 of them per stack |
| Export | 2160 × 3840 JPEG + FITS, plus H.264 clips for the live views |
| Processing | Centre crop, sky-gradient subtraction, asinh stretch, chroma denoise — <a href="https://github.com/vivianweidai/science/blob/main/web/public/research/projects/20260725%20Stargazing/output/build_gallery.py" rel="noopener">build_gallery.py</a> |

## Sun

<div class="sky-grid">
  <figure class="sky-tile">
    <a href="media/sun-clouds.mp4">
      <video src="media/sun-clouds.mp4" poster="media/sun-clouds-poster.jpg" autoplay loop muted playsinline preload="auto" aria-label="Cloud drifting across the solar disk"></video>
    </a>
    <figcaption><b>Cloud transit</b><span>17 s live view · July 1</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/sun-sunspots.jpg">
      <img src="media/sun-sunspots.jpg" alt="The whole solar disk with several sunspot groups" loading="lazy">
    </a>
    <figcaption><b>Sunspot groups</b><span>Whole disk · July 24</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/sun-haze.jpg">
      <img src="media/sun-haze.jpg" alt="The Sun seen through high cloud, mottled and dimmed" loading="lazy">
    </a>
    <figcaption><b>Through high cloud</b><span>Whole disk · July 1</span></figcaption>
  </figure>
</div>

## Galaxies and Clusters

<div class="sky-grid">
  <figure class="sky-tile">
    <a href="media/m31.jpg">
      <img src="media/m31.jpg" alt="The Andromeda Galaxy with its two bright satellite galaxies" loading="lazy">
    </a>
    <figcaption><b>M 31 — Andromeda</b><span>17 × 10 s · with M 32 and M 110</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/m13.jpg">
      <img src="media/m13.jpg" alt="The globular cluster M 13, resolving into individual stars" loading="lazy">
    </a>
    <figcaption><b>M 13 — Hercules Cluster</b><span>30 × 10 s · edges resolving</span></figcaption>
  </figure>
</div>

## Stars

<div class="sky-grid">
  <figure class="sky-tile">
    <a href="media/vega.jpg">
      <img src="media/vega.jpg" alt="Vega blazing in a dense field of fainter stars" loading="lazy">
    </a>
    <figcaption><b>Vega</b><span>24 × 10 s · α Lyrae</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/deneb.jpg">
      <img src="media/deneb.jpg" alt="Deneb inside the crowded star fields of Cygnus" loading="lazy">
    </a>
    <figcaption><b>Deneb</b><span>32 × 10 s · α Cygni</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/rr-lyrae.jpg">
      <img src="media/rr-lyrae.jpg" alt="The crowded Milky Way field around the variable star RR Lyrae" loading="lazy">
    </a>
    <figcaption><b>RR Lyrae</b><span>425 × 5 s · 35 minutes deep</span></figcaption>
  </figure>
</div>

<style>
/* Gallery of Seestar captures. Everything is 9:16 because the scope exports
   9:16 — tiles, hero and videos all keep that shape rather than cropping to
   landscape. Dark plate behind the tiles so the sky reads as sky. */
.sky-hero {
  margin: 1.2em 0 0.4em;
  padding: 1.2em 1em 1em;
  background: radial-gradient(120% 90% at 50% 0%, #1b1f2a 0%, #0b0d12 70%);
  border-radius: 10px;
  text-align: center;
}
.sky-hero video {
  width: 100%;
  max-width: 300px;
  aspect-ratio: 9 / 16;
  object-fit: cover;
  border-radius: 8px;
  background: #000;
  box-shadow: 0 10px 34px rgba(0, 0, 0, 0.55);
}
.sky-hero-cap {
  margin: 0.9em 0 0;
  color: #b6bdc9;
  font-size: 0.82em;
}

.sky-grid {
  display: grid;
  /* Capped at 240px rather than 1fr: a two-tile row would otherwise stretch
     each portrait tile to ~440 x 780 and swallow the page. */
  grid-template-columns: repeat(auto-fit, minmax(160px, 240px));
  justify-content: center;
  gap: 0.75em;
  margin: 1.2em 0;
  padding: 0.9em;
  background: #0b0d12;
  border-radius: 10px;
}
.sky-tile { margin: 0; }
.sky-tile a { display: block; }
.sky-tile img,
.sky-tile video {
  display: block;
  width: 100%;
  aspect-ratio: 9 / 16;
  object-fit: cover;
  border-radius: 7px;
  background: #000;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.sky-tile a:hover img,
.sky-tile a:hover video {
  transform: scale(1.02);
  box-shadow: 0 8px 22px rgba(120, 150, 220, 0.28);
}
.sky-tile figcaption {
  padding: 0.55em 0.1em 0.2em;
  line-height: 1.35;
}
.sky-tile figcaption b {
  display: block;
  color: #e8ecf3;
  font-size: 0.82em;
}
.sky-tile figcaption span {
  display: block;
  color: #8d95a3;
  font-size: 0.74em;
}
@media (prefers-reduced-motion: reduce) {
  .sky-tile a:hover img,
  .sky-tile a:hover video { transform: none; }
}
</style>
