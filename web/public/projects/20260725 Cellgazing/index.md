---
project: Cellgazing
tech:
  - Microscopes
title: "Cellgazing"
sciences:
  - Biology
---

<div class="cell-hero">
  <img src="data/reticulate-specimen.jpg" alt="">
</div>

<div class="cell-grid">
  <figure class="cell-tile">
    <a href="data/leaf-epidermis.jpg"><img src="data/leaf-epidermis.jpg" alt="Leaf epidermis" loading="lazy"></a>
    <figcaption><b>Leaf epidermis</b><span>peel · stomata</span></figcaption>
  </figure>
  <figure class="cell-tile">
    <a href="data/tissue-section.jpg"><img src="data/tissue-section.jpg" alt="Tissue" loading="lazy"></a>
    <figcaption><b>Tissue</b><span>stained · lobules septa</span></figcaption>
  </figure>
</div>

<style>
/* Bright-field slides are mostly white, so the plate is light — a dark one
   turns every specimen into a glowing blob. Frames are 4:3 straight off the
   camera, so the tiles are 4:3 and object-fit never crops. */
.cell-hero {
  aspect-ratio: 5 / 2;
  margin: 1.2em 0 0.6em;
  overflow: hidden;
  border-radius: 10px;
  background: #eef2ef;
}
.cell-hero img {
  width: 100%;
  height: 100%;
  /* The frame is ~3:2 and the band is 5:2, so cover trims top and bottom.
     Centred: the texture is uniform, there is no subject to keep in view. */
  object-fit: cover;
  object-position: 50% 50%;
  display: block;
}
.cell-grid {
  display: grid;
  /* Capped at 320px: a short row would otherwise stretch three landscape tiles
     across the whole page and swamp it. */
  grid-template-columns: repeat(auto-fit, minmax(220px, 320px));
  justify-content: center;
  gap: 0.75em;
  margin: 1.2em 0;
  padding: 0.9em;
  background: #eef2ef;
  border-radius: 10px;
}
.cell-tile { margin: 0; }
.cell-tile a { display: block; }
.cell-tile img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 7px;
  background: #fff;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.cell-tile a:hover img {
  transform: scale(1.02);
  box-shadow: 0 8px 22px rgba(90, 160, 145, 0.32);
}
/* Specimen left, note right, on one line. */
.cell-tile figcaption {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.6em;
  padding: 0.55em 0.15em 0.2em;
  line-height: 1.35;
}
.cell-tile figcaption b { color: #24312d; font-size: 0.82em; }
.cell-tile figcaption span { color: #6d7f79; font-size: 0.74em; white-space: nowrap; }
@media (prefers-reduced-motion: reduce) {
  .cell-tile a:hover img { transform: none; }
}
/* Full-screen viewer for a clicked tile: slide, its caption, arrows through
   the set. Dark backdrop here even though the plate is light — a bright
   surround would wash out a bright-field slide. */
.cell-lightbox {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  padding: 2.5vh 1vw;
  background: rgba(8, 12, 11, 0.97);
}
.cell-lightbox[hidden] { display: none; }
.cell-stage {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin: 0;
  min-width: 0;
}
.cell-stage img {
  display: block;
  width: auto;
  max-width: 88vw;
  max-height: 86vh;
  border-radius: 6px;
  background: #fff;
}
.cell-stage figcaption {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.6em;
  padding: 0.7em 0.15em 0;
}
.cell-stage figcaption b { color: #eef2ef; font-size: 0.9em; }
.cell-stage figcaption span { color: #8fa39c; font-size: 0.8em; white-space: nowrap; }
.cell-nav,
.cell-close {
  flex: none;
  border: none;
  background: transparent;
  color: #8fa39c;
  font-family: inherit;
  cursor: pointer;
  line-height: 1;
  transition: color 0.15s ease;
}
.cell-nav { padding: 0.2em 0.5em; font-size: 3em; }
.cell-nav:hover,
.cell-close:hover { color: #eef2ef; }
.cell-close {
  position: absolute;
  top: 0.6em;
  right: 0.9em;
  padding: 0.1em 0.3em;
  font-size: 2em;
}
@media (max-width: 600px) {
  .cell-nav { font-size: 2.2em; padding: 0.2em 0.15em; }
  .cell-stage img { max-width: 80vw; }
}
</style>

<div class="cell-lightbox" id="cell-lightbox" hidden>
  <button class="cell-nav cell-prev" type="button" aria-label="Previous image">‹</button>
  <figure class="cell-stage">
    <img id="cell-shot" alt="">
    <figcaption><b id="cell-name"></b><span id="cell-meta"></span></figcaption>
  </figure>
  <button class="cell-nav cell-next" type="button" aria-label="Next image">›</button>
  <button class="cell-close" type="button" aria-label="Close">×</button>
</div>

<script>
// Same viewer as the Stargazing gallery: tiles open in place so the arrows
// (and ← →) can move through the set. The tile markup stays the source of
// truth — href, name and note are read back out of it.
(function () {
  var tiles = [].slice.call(document.querySelectorAll('.cell-tile'));
  if (!tiles.length) return;

  var shots = tiles.map(function (tile) {
    return {
      src: tile.querySelector('a').getAttribute('href'),
      name: tile.querySelector('figcaption b').textContent,
      meta: tile.querySelector('figcaption span').textContent
    };
  });

  var box = document.getElementById('cell-lightbox');
  var img = document.getElementById('cell-shot');
  var name = document.getElementById('cell-name');
  var meta = document.getElementById('cell-meta');
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

  box.querySelector('.cell-prev').addEventListener('click', function () { show(at - 1); });
  box.querySelector('.cell-next').addEventListener('click', function () { show(at + 1); });
  box.querySelector('.cell-close').addEventListener('click', close);
  // Clicking the backdrop closes; clicking the slide or a button does not.
  box.addEventListener('click', function (e) { if (e.target === box) close(); });

  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'ArrowLeft') show(at - 1);
    else if (e.key === 'ArrowRight') show(at + 1);
    else if (e.key === 'Escape') close();
  });
})();
</script>
