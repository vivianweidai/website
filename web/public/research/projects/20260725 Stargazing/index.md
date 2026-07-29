---
project: Stargazing
tech:
  - Telescopes
title: "Stargazing"
sciences:
  - Astronomy
---

<div class="sky-hero">
  <video src="data/Solar_video__2026-07-24-164602-Solar.mp4" autoplay loop muted playsinline preload="auto"></video>
</div>

<div class="sky-grid">
  <figure class="sky-tile">
    <a href="data/M_31__Stacked_17_M_31_10.0s_IRCUT_20260725-014442.jpg"><img src="data/M_31__Stacked_17_M_31_10.0s_IRCUT_20260725-014442.jpg" alt="M 31" loading="lazy"></a>
    <figcaption><b>M 31</b><span>17 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/M_13__Stacked_5_M_13_60.0s_IRCUT_20260728-225801.jpg"><img src="data/M_13__Stacked_5_M_13_60.0s_IRCUT_20260728-225801.jpg" alt="M 13" loading="lazy"></a>
    <figcaption><b>M 13</b><span>5 × 60s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/M_51__Stacked_30_M_51_10.0s_IRCUT_20260704-222846.jpg"><img src="data/M_51__Stacked_30_M_51_10.0s_IRCUT_20260704-222846.jpg" alt="M 51" loading="lazy"></a>
    <figcaption><b>M 51</b><span>30 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/NGC_5907__Stacked_9_NGC_5907_10.0s_IRCUT_20260704-223446.jpg"><img src="data/NGC_5907__Stacked_9_NGC_5907_10.0s_IRCUT_20260704-223446.jpg" alt="NGC 5907" loading="lazy"></a>
    <figcaption><b>NGC 5907</b><span>9 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Vega__Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg"><img src="data/Vega__Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg" alt="Vega" loading="lazy"></a>
    <figcaption><b>Vega</b><span>8 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Deneb__Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg"><img src="data/Deneb__Stacked_32_Deneb_10.0s_IRCUT_20260725-015351.jpg" alt="Deneb" loading="lazy"></a>
    <figcaption><b>Deneb</b><span>32 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/RR_Lyrae__Stacked_21_RR_Lyrae_5.0s_IRCUT_20260725-020642.jpg"><img src="data/RR_Lyrae__Stacked_21_RR_Lyrae_5.0s_IRCUT_20260725-020642.jpg" alt="RR Lyrae" loading="lazy"></a>
    <figcaption><b>RR Lyrae</b><span>21 × 5s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Delta_Cygni__Stacked_54_Delta_Cygni_5.0s_IRCUT_20260728-223243.jpg"><img src="data/Delta_Cygni__Stacked_54_Delta_Cygni_5.0s_IRCUT_20260728-223243.jpg" alt="Delta Cygni" loading="lazy"></a>
    <figcaption><b>Delta Cygni</b><span>54 × 5s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/V530_Lyrae_sub__Light_V530_Lyrae_2.0s_IRCUT_20260728-232423.jpg"><img src="data/V530_Lyrae_sub__Light_V530_Lyrae_2.0s_IRCUT_20260728-232423.jpg" alt="Vega spectrum" loading="lazy"></a>
    <figcaption><b>Vega spectrum</b><span>1 × 2s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Vega_sub__Light_Vega_10.0s_LP_20260728-233740.jpg"><img src="data/Vega_sub__Light_Vega_10.0s_LP_20260728-233740.jpg" alt="Vega spectrum" loading="lazy"></a>
    <figcaption><b>Vega spectrum</b><span>1 × 10s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Juno_sub__Light_Juno_20.0s_IRCUT_20260729-000521.jpg"><img src="data/Juno_sub__Light_Juno_20.0s_IRCUT_20260729-000521.jpg" alt="Juno — before" loading="lazy"></a>
    <figcaption><b>Juno — before</b><span>1 × 20s</span></figcaption>
  </figure>
  <figure class="sky-tile">
    <a href="data/Juno_sub__Light_Juno_20.0s_IRCUT_20260729-003012.jpg"><img src="data/Juno_sub__Light_Juno_20.0s_IRCUT_20260729-003012.jpg" alt="Juno — after" loading="lazy"></a>
    <figcaption><b>Juno — after</b><span>1 × 20s</span></figcaption>
  </figure>
</div>

<style>
/* Every frame is a Seestar export, untouched — the scope shoots 9:16, so the
   tiles are 9:16 and object-fit never actually crops anything. Dark plate
   behind them so the sky reads as sky. */
/* Wide banner cropped to the disk. The clip is portrait 9:16 with the Sun
   filling 0.54 of the frame height, so scaling it to 172% of the band height
   and clipping the overflow leaves the disk spanning ~92% of the band — the
   empty sky above and below is cut, not letterboxed. translateX corrects for
   the Sun sitting 1.5% right of frame centre. */
.sky-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 5 / 2;
  margin: 1.2em 0 0.6em;
  overflow: hidden;
  border-radius: 10px;
  /* Matched to the clip's own corner tone (rgb 9,4,1) so the band reads as
     one surface instead of a video pasted on a plate. */
  background: radial-gradient(circle at 50% 50%, #120802 0%, #090401 60%, #070300 100%);
}
.sky-hero video {
  height: 172%;
  width: auto;
  max-width: none;
  transform: translateX(-1.5%);
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
/* Full-screen viewer for a clicked tile: photo, the same caption the tile
   carries, and arrows through the set. */
.sky-lightbox {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  padding: 2.5vh 1vw;
  background: rgba(6, 7, 10, 0.97);
}
.sky-lightbox[hidden] { display: none; }
.sky-stage {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin: 0;
  min-width: 0;
}
.sky-stage img {
  display: block;
  width: auto;
  max-width: 84vw;
  max-height: 86vh;
  border-radius: 6px;
}
.sky-stage figcaption {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.6em;
  padding: 0.7em 0.15em 0;
}
.sky-stage figcaption b { color: #e8ecf3; font-size: 0.9em; }
.sky-stage figcaption span { color: #8d95a3; font-size: 0.8em; white-space: nowrap; }
.sky-nav,
.sky-close {
  flex: none;
  border: none;
  background: transparent;
  color: #8d95a3;
  font-family: inherit;
  cursor: pointer;
  line-height: 1;
  transition: color 0.15s ease;
}
.sky-nav { padding: 0.2em 0.5em; font-size: 3em; }
.sky-nav:hover,
.sky-close:hover { color: #e8ecf3; }
.sky-close {
  position: absolute;
  top: 0.6em;
  right: 0.9em;
  padding: 0.1em 0.3em;
  font-size: 2em;
}
@media (max-width: 600px) {
  .sky-nav { font-size: 2.2em; padding: 0.2em 0.15em; }
  .sky-stage img { max-width: 78vw; }
}
</style>

<div class="sky-lightbox" id="sky-lightbox" hidden>
  <button class="sky-nav sky-prev" type="button" aria-label="Previous image">‹</button>
  <figure class="sky-stage">
    <img id="sky-shot" alt="">
    <figcaption><b id="sky-name"></b><span id="sky-meta"></span></figcaption>
  </figure>
  <button class="sky-nav sky-next" type="button" aria-label="Next image">›</button>
  <button class="sky-close" type="button" aria-label="Close">×</button>
</div>

<script>
// Tiles open in place instead of navigating to the bare .jpg, so the arrows
// (and ← →, and swipe-free clicks) can move through the set. The tile markup
// stays the source of truth: href, name and stack are read back out of it.
(function () {
  var tiles = [].slice.call(document.querySelectorAll('.sky-tile'));
  if (!tiles.length) return;

  var shots = tiles.map(function (tile) {
    return {
      src: tile.querySelector('a').getAttribute('href'),
      name: tile.querySelector('figcaption b').textContent,
      meta: tile.querySelector('figcaption span').textContent
    };
  });

  var box = document.getElementById('sky-lightbox');
  var img = document.getElementById('sky-shot');
  var name = document.getElementById('sky-name');
  var meta = document.getElementById('sky-meta');
  var at = 0;

  function show(i) {
    at = (i + shots.length) % shots.length;   // wrap at both ends
    var shot = shots[at];
    img.src = shot.src;
    img.alt = shot.name;
    name.textContent = shot.name;
    meta.textContent = shot.meta;
  }

  function open(i) {
    show(i);
    box.hidden = false;
    document.body.style.overflow = 'hidden';
  }

  function close() {
    box.hidden = true;
    img.src = '';
    document.body.style.overflow = '';
  }

  tiles.forEach(function (tile, i) {
    tile.querySelector('a').addEventListener('click', function (e) {
      e.preventDefault();
      open(i);
    });
  });

  box.querySelector('.sky-prev').addEventListener('click', function () { show(at - 1); });
  box.querySelector('.sky-next').addEventListener('click', function () { show(at + 1); });
  box.querySelector('.sky-close').addEventListener('click', close);
  // Clicking the backdrop closes; clicking the photo or a button does not.
  box.addEventListener('click', function (e) { if (e.target === box) close(); });

  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'ArrowLeft') show(at - 1);
    else if (e.key === 'ArrowRight') show(at + 1);
    else if (e.key === 'Escape') close();
  });
})();
</script>
