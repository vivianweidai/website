# PROJECTS

How the **published** Projects vertical is structured: the picture wall at `/projects/`, and the
individual project pages under it. These rules live here, beside the files they govern —
`thewall.yml`, `thewall/<science>/`, and the `<YYYYMMDD Name>/` project folders are all in this
directory, so anyone editing them is already standing next to this doc.


## THE WALL

One folder per science and a picture belongs to exactly one:

    astronomy/20260730 M 31.jpg
    ^ science  ^ sorts    ^ name

**Nothing in the filename is displayed.** A photo tile is the picture and nothing else. So the
filename is not copy, it is plumbing, and it does three jobs:

- the **`YYYYMMDD` prefix orders the wall** — it is the date the picture joined the wall, not
  necessarily when it was shot, and renaming it moves the tile
- the **rest of the name** becomes the `alt` text and the tile's `aria-label`, so a screen reader
  still reads it even though no one sees it
- the **folder** is the science

Drop a file in, run `python3 pipeline/scripts/build_thewall.py`, done. **No YAML for a photo tile.**

**Keep them web-sized: a long edge of 2000.** There is no thumbnail folder — the wall and the
lightbox both load these files directly, so camera-resolution originals would be three times the
page weight for no visible gain at any display size. `sips -Z 2000 in.jpg --out in.jpg` is the whole
recipe. Full-resolution originals live outside the published site.

An `.mp4` works as a tile — it autoplays muted and loops. Give it a still frame beside it named
`<name>.poster.jpg`; that is what the tile shows before the clip plays, and what the iOS app shows
instead of the video.

A picture that lives inside a project folder **stays there** and is referenced from `thewall.yml` beside it.
Copying it here would put the same bytes in git twice, and the build rejects that by content hash.

**Landscape tiles span two columns.** A portrait frame gets its presence from its own aspect
ratio; a 4:3 photo at one column is a stamp. `grid-auto-flow: row dense` back-fills the hole a
wide tile leaves at the end of a row — local order shifts, which on a wall reads as packing.

**Clicking a tile opens a lightbox** — full resolution, ‹ › buttons, ← → keys, Esc to close, click
the backdrop to dismiss. It pages through *currently visible* tiles, so a filtered wall stays
inside its filter, and it skips project cards because those are links to a write-up. The tile's
thumbnail shows instantly and the original swaps in when it arrives; neighbours preload.

**Video is a tile like any other.** An `.mp4` autoplays muted and loops, its dimensions come from
the MP4 header (`tkhd`, rotation matrix honoured), and it is served without re-encoding.

**Dating a tile** has three sources, in order: an explicit `date: YYYY-MM`; a `YYYYMMDD` prefix on
the filename *or on any folder above it* (which dates both `thewall/photos/` and every generated
plot by its project folder); then EXIF. Between them a row almost never needs a date by hand.
Tiles sort **newest month first, then by filename within the month** — so the filename is the one
lever for placement, and renaming a file moves its tile. A round-robin across the sciences used to
sit in here, to stop a busy week in one science landing as a slab; it was removed once the wall
became hand-curated, because it pushed apart two pictures deliberately named to sit together.

** A photo tile shows nothing but the photo — no caption, no pill, no date, no hover text.**
**The picture is the whole content**, on the tile
and in the lightbox alike, and the same holds in the iOS app. This supersedes the earlier "one line
and one pill" rule, and it is the *third* time a second axis of information has been added to this
page and then taken back off — twice a second filter row, and now the captions.
**Don't re-add text to a photo tile**, and don't reach for a caption to explain a picture that
isn't carrying itself: **replace the picture.**

- **Only a project card is captioned**, permanently, because it is a link and a link needs a name.
  Caption plus science pill plus a `Project →` badge, framed in its science colour — the whole
  point being that a card must *not* read as one more photo.
- **The caption string still exists; it is just never displayed.** `build_thewall.py` derives it
  from the filename and bakes it into `thewall.json`, and the wall spends it on the `alt` attribute
  and the tile's `aria-label`. So **the filename is still doing real work** — it orders the wall, it
  names the file, and it is what a screen reader announces. Write it as if someone will read it,
  because someone will; just don't expect to see it.
- **`note:` in `thewall.yml` renders nowhere either.** Between the two, a photo tile has no surface
  for prose at all. Anything that genuinely needs explaining belongs on a project page.

**Filtering is one tier.** Just the six sciences. A category row was built, then a third row of
a third row under it, and both were removed within the day — the wall is one grid of pictures, and every
extra axis of selection made the header busier without making the pictures easier to find.

**A wrong picture is now the only way to be wrong, so look at the frames.** Captions used to be the
hazard — several first-pass ones described the wrong instrument entirely (a bench of samples called
"the printed jig"). With captions gone that particular trap is closed, and a subtler one is open:
**nothing on the page will ever correct a misleading image**, and a filename that misidentifies its
subject still reaches screen readers and the JSON. Render the tiles and look before shipping.


## PROJECT REPORTS

Each project is a date-prefixed folder under `web/public/projects/`. The public-facing overview is **`report.md`** (not `README.md`) — Astro's loader globs `*/report.md`, so the filename matters. Model new pages on `20260420 UV-Vis Spectroscopy/report.md` or `20260419 IR Spectroscopy/report.md`.

```
YYYYMMDD Project Name/
├── data/      # Raw instrument data (CSVs, spectra). NEVER modify — read-only.
├── photos/    # Experiment photos, split by purpose (see below)
│   ├── setup/    # Setup + sample shots — feed the top-page shuffle
│   ├── samples/  # (optional) sample close-ups — also shuffled
│   └── data/     # Handwritten data sheets — excluded from shuffle; shown via #data-grid
├── papers/    # Background papers
├── output/    # ALL generated output: *.py/*.ipynb, *.png plots, *.csv/*.json processed data
└── report.md  # Overview, methods, results
```

Create these subdirs as needed and follow the existing names rather than inventing new ones. **Never modify raw data** — read from `data/`, write everything generated to `output/`.

**Photos.** The shuffle pool is **auto-populated** by `Project.astro`: its `getStaticPaths` scans every `.jpg`/`.jpeg`/`.png` under `photos/` (`setup/` + `samples/`, **never `data/`**) and injects them as `window._pagePhotos`. So:
- **Don't** list photos in frontmatter or add a per-page inline `_pagePhotos` script — the layout's shuffle script runs on every project page.
- Name files sequentially in capture order: `setup1.jpeg`, `setup2.jpeg`, … / `data1.jpeg`, …. `git mv` originals (e.g. `20240920 Catfood G.jpeg`) so references stay short and stable.
- `photos/data/` (handwritten sheets) is surfaced explicitly via a hand-coded in-page `#data-grid` of plain `<img>` — the `[slug]` route filters it out of the shuffle so it never hits the hero. Keep that contract if you add subfolders.

**Frontmatter** (`content.config.ts` validates it): `project:` short name · `title:` H1 prose title ·
`sciences:` array of **full science names**, which drives the title-row pills and the page's subject
colouring.

**Page structure.** Frontmatter → `# [Experiment Title]` → hero → body. Hero:
- **4+ photos** → shuffle grid (pool auto-populates; no `photos:` array, no inline script):
  ```html
  <div class="photo-grid" id="photo-grid"><img id="photo-0" alt="…"><img id="photo-1" alt="…"><img id="photo-2" alt="…"><img id="photo-3" alt="…"></div>
  <button class="shuffle-btn" onclick="shufflePhotos()">Shuffle Photos</button>
  ```
- **1 photo** → `<div class="hero-single"><img src="photos/[file]" alt="…"></div>`
- Then `<div class="project-meta">[Month Dayth Year]<br>[Instrument name]</div>` (right-aligned, Instrument on its own line).

Body sections **in order**: `## Overview` (1–2 para) · `## Setup` (Category/Details table + procedure prose) · `## Samples` (**top-level `##`**, not under Setup) · `## Data` (format; if `photos/data/` has sheets, add the hand-coded `#data-grid` — `three-col` for 3, shuffle button only if >4) · `## Results` (link **written report → static notebook → Colab**, in that order). `## Results` is the **last thing in the file** — no footer or nav div: `Project.astro` injects `<PageFooter />` and one science-coloured pill per `sciences:` entry, each linking to the wall filtered to it. **Never add a `#`/row-number column to any table** (repo-wide rule) — row order conveys sequence.

**Writing style — toolkit notes, not publications.** A fast future-you glance at what the method does and what makes it different from its neighbours; the scaffold for research, not the research. Model density: the two Spectroscopy pages above.
- **Note-and-bullet first** — short bullets over paragraphs; 1–2 sentences when a paragraph is needed.
- **Differentiate, don't summarize** — lead with what distinguishes this instrument or method from its neighbours; if two measure the same thing, say which this page used and why.
- **Cut publication scaffolding** — no abstract intros, no "in this work we…", no non-load-bearing motivation.
- **Font styling judicious** — one or two bolds per section (the instrument's proper noun or the differentiator). Sub/superscripts only when the notation carries information (`λ<sub>max</sub>` yes; italicizing every verb no).
- **Push specs to Setup tables** — ranges, software names, filename patterns, cuvette sizes live in the Setup/Data table, not prose. Let tabs and section-heads carry the structure.

