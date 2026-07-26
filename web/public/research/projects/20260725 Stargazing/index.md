---
project: Stargazing
tech:
  - Telescopes
title: "Stargazing"
sciences:
  - Astronomy
---

<div class="sky-hero">
  <video src="media/Solar_video__2026-07-24-164602-Solar.mp4" autoplay loop muted playsinline preload="auto"></video>
</div>

<div class="sky-grid">
  <figure class="sky-tile">
    <a href="media/M_31__Stacked_17_M_31_10.0s_IRCUT_20260725-014442.jpg"><img src="media/M_31__Stacked_17_M_31_10.0s_IRCUT_20260725-014442.jpg" alt="M 31" loading="lazy"></a>
    <figcaption><b>M 31</b><span>17 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/M_13__Stacked_30_M_13_10.0s_IRCUT_20260721-215926.jpg"><img src="media/M_13__Stacked_30_M_13_10.0s_IRCUT_20260721-215926.jpg" alt="M 13" loading="lazy"></a>
    <figcaption><b>M 13</b><span>30 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/M_51__Stacked_30_M_51_10.0s_IRCUT_20260704-222846.jpg"><img src="media/M_51__Stacked_30_M_51_10.0s_IRCUT_20260704-222846.jpg" alt="M 51" loading="lazy"></a>
    <figcaption><b>M 51</b><span>30 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/NGC_5907__Stacked_9_NGC_5907_10.0s_IRCUT_20260704-223446.jpg"><img src="media/NGC_5907__Stacked_9_NGC_5907_10.0s_IRCUT_20260704-223446.jpg" alt="NGC 5907" loading="lazy"></a>
    <figcaption><b>NGC 5907</b><span>9 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/Vega__Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg"><img src="media/Vega__Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg" alt="Vega" loading="lazy"></a>
    <figcaption><b>Vega</b><span>8 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/Deneb__Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg"><img src="media/Deneb__Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg" alt="Deneb" loading="lazy"></a>
    <figcaption><b>Deneb</b><span>32 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="media/RR_Lyrae__Stacked_21_RR_Lyrae_5.0s_IRCUT_20260725-020642.jpg"><img src="media/RR_Lyrae__Stacked_21_RR_Lyrae_5.0s_IRCUT_20260725-020642.jpg" alt="RR Lyrae" loading="lazy"></a>
    <figcaption><b>RR Lyrae</b><span>21 × 5s</span></figcaption>
  </figure>
</div>

<style>
/* Every frame is a Seestar export, untouched — the scope shoots 9:16, so the
   tiles are 9:16 and object-fit never actually crops anything. Dark plate
   behind them so the sky reads as sky. */
.sky-hero {
  margin: 1.2em 0 0.6em;
  padding: 1.1em;
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
.sky-grid {
  display: grid;
  /* Capped at 240px rather than 1fr: a short row would otherwise stretch each
     portrait tile to ~440 x 780 and swallow the page. */
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
.sky-tile img {
  display: block;
  width: 100%;
  aspect-ratio: 9 / 16;
  object-fit: cover;
  border-radius: 7px;
  background: #000;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.sky-tile a:hover img {
  transform: scale(1.02);
  box-shadow: 0 8px 22px rgba(120, 150, 220, 0.28);
}
/* Target left, stack right, on one line. */
.sky-tile figcaption {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.6em;
  padding: 0.55em 0.15em 0.2em;
  line-height: 1.35;
}
.sky-tile figcaption b {
  color: #e8ecf3;
  font-size: 0.82em;
}
.sky-tile figcaption span {
  color: #8d95a3;
  font-size: 0.74em;
  white-space: nowrap;
}
@media (prefers-reduced-motion: reduce) {
  .sky-tile a:hover img { transform: none; }
}
</style>
