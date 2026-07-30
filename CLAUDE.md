# SCIENCE — Claude Code Instructions

Personal science portfolio + lab notebook — live on [vivianweidai.com](https://vivianweidai.com) and the [App Store](https://apps.apple.com/app/id6762091743) (iPhone + iPad, with an embedded Apple Watch companion). Curriculum reference tables, an Olympiad timeline, and hands-on projects (raw data, photos, notebooks, reproducible pipelines). Your role: process experimental data and build reproducible analysis pipelines — parse raw instrument outputs, clean and validate, analyze, visualize.

This CLAUDE.md is the repo's only doc — the README was folded in and deleted 2026-07-17 (Claude-maintained; even though the repo is public, James opted out of README upkeep).

## STACK

- **Astro 5** — static site generator. Builds to `pipeline/worker/dist/` (co-located with the Worker that serves it) via `outDir: '../pipeline/worker/dist'`.
- **Cloudflare Workers + Static Assets** — serves the build output at `vivianweidai.com`. The Worker is a true passthrough to the `ASSETS` binding (no edge logic).
- **GitHub** — source control only. Push triggers nothing.
- **Apple** — native app in `apple/` consumes `vivianweidai.com/{olympiads,projects,curriculum}/*.json` (and per-discipline markdown under `curriculum/source/`). See § APPLE APP.

## REPO STRUCTURE

Top-level reads like every other repo: `apple/ web/ pipeline/ work/` + this doc. **The entire Astro app lives in `web/`** — its `astro.config.mjs`, `package.json`, `tsconfig.json`, `src/`, and `public/` (relocated from the repo root 2026-07-17 to keep the root clean; `src/`/`public/` stay at Astro's defaults *inside* `web/`). **All `pnpm` commands run from `web/`.**

- **`web/src/`** — `content.config.ts` (Content Collections: **`projects`** + **`tech`**); `layouts/` holds the `.astro` components *and* their imported CSS/JS; `pages/` is file-based routing (`projects/` carries the dynamic `[slug]` project route + `technology/[science]/[tech]` tech route).
- **`web/public/`** — source-of-truth served **verbatim at the site root**. Areas: `curriculum/` (`source/*.md` + `curriculum.json`), `olympiads/` (`olympiads.yml`), `projects/` (`<YYYYMMDD Name>/` project folders sitting **directly** under it, plus `gallery.yml` + `gallery/<science>/`). `<science>` is the full word (mathematics, computing…) to mirror `curriculum/source/`.
- **`pipeline/`** — `worker/` (CF Worker: ASSETS passthrough → `dist/`) + `scripts/` (`build_olympiads.py` / `build_gallery.py`, YAML→JSON; `build_curriculum.py`, .docx→markdown). Scripts resolve paths from their own location, so run them **from the repo root**; they write into `web/public/`.
- **`work/`** — works-in-progress, git-tracked but **NOT web-served**. One dir per science (`physics/` `chemistry/` `biology/` `astronomy/`) + `IDEAS.md`. Named `work/` (not `projects/`) to stay distinct from the published `web/public/projects/`. **`work/scratch/`** is the rough scratchpad (tracked + pushed — backed up and distributed across machines; the relocated home of the old `~/GITHUB/scratch/`, 2026-07-16). Three-stage flow, all tracked — the difference is polish and web-visibility, not whether it's in git: `work/scratch/<topic>` (rough) → `work/<science>/` (organized WIP) → `web/public/projects/` (published).
- **`work/IDEAS.md`** (moved from the repo root 2026-07-17) — the research program's living doc: **ideation** (idea backlog) + **progress tracking** (the "Active work & progress" dashboard and in-flight detail like the home molecular-biology lab). Promote an idea to a dated project folder when a pilot starts; keep the dashboard and idea statuses current.

**Convention deviation: no top-level `content/`; source-of-truth lives under `web/public/`.** The cross-repo convention puts source-of-truth in a top-level `content/`. We deviate because Astro's `public/` is served verbatim at the site root — so `web/public/` **is** the content dir: a file at `web/public/X/Y` serves at `/X/Y`, 1:1, no rewrites, no sync step. Page URLs and asset URLs coexist under the same prefix (`/projects/<folder>/` is the rendered HTML; `/projects/<folder>/index.md` is the raw markdown the apps fetch; `/projects/<folder>/photos/…` are the photos). The Content Collection loader points at `./public/projects/` (relative to the `web/` Astro root); the dynamic route's photo discovery walks the same path.

## DATA MODEL — TECHNOLOGIES & TOYS

The toy catalog behind the site is organized around two concepts:

- **Technology (Tech)** — a research capability, and the **category** the site filters on (e.g. *Spectroscopy*, *Mechanics*, *Genomics*). A way of asking nature a question.
- **Toy** — a specific physical instrument that *enables* a Technology (e.g. *Paton Hawksley Star Analyser 100 Grating* enables Spectroscopy; *ZWO Seestar S30 Pro* enables Amateur, Spectroscopy, Photometry, Astrometry). One Toy can enable multiple Techs. A Tech is "available" when we own ≥1 Toy that enables it.

**Access tiers** (the collection is grounded in Toys we can regularly touch; prefer lower tiers — don't propose a Tier-4 path when a Tier-1/2/3 Toy does the job):

1. **Home lab** (foundational) — instruments owned + operated at home. Daily hands-on access. New research centers here.
2. ~~**Shared Instruments Lab** (UNR SIL)~~ — **RETIRED July 2026** (access ended with the Vancouver move), and **fully purged from the registry 2026-07-18**. The Toy list is now strictly *instruments we have at home* — no SIL instruments, and no aspirational purchases. Removed: the Nicolet 380 FT-IR (Spectroscopy), DSC Q20 + TGA Q50 (Thermal), and the whole **Spectrometry** tech (MALDI-TOF, LC-MS, GC-MS — it had no projects). The PalmSens EmStat Pico went with them: **we never owned it.** *(Supersedes the earlier "SIL instruments stay as historical past-work" rule — don't re-add them.)*
   **Completed projects keep naming the instrument they actually used** — the IR Spectroscopy project still cites the Nicolet 380 in its Setup table, and Melting Point cites the OptiMelt. A project's instrument is a historical record and need not appear in `technology.yml`; the exact-name-match rule applies to *live* Toys.
3. **Remote terminals into partner observatories** — UBC Thunderbird South. Real instrument time, operated over a network.
4. **Pay-per-use / mail-in services** (future) — for Techs we can't reasonably own. Add only after Tiers 1–3 cover the foundational science.

**Schema** — the data layer matches this vocabulary end-to-end:

| Layer | YAML/JSON field | Frontmatter | URL path | Astro collection |
|---|---|---|---|---|
| Science (card) | `science` | — | `/projects/#<slug>` | — |
| Tech (category) | `techs[].tech` | `tech:` | `/projects/#<sci>/<tech>` | — |
| Toy (instrument) | `techs[].toys[].name` | — | — | — |

`technology.yml` is **one flat entry per science** (`science:` + `techs:`, with `toys:` inline under each tech). It is a **pure catalog — there are no tech pages.** `web/public/projects/technology/` was deleted 2026-07-30: a documentation layer nobody read, whose hero photos were better off as gallery tiles, and whose toys now live inline in the YAML where a reader would look for them. The catalog supplies the *vocabulary*: the home page's Projects tab lists each science's categories, the wall filters on them, and `gallery.yml` tags a photo with a `toy:` that rolls up to its category.

**Engineering was removed as a category** (2026-07-30) with its toys — LEGO, the Analog Discovery, the Prusa. They are tools that cross every science rather than a way of asking nature a question, so they never sat right under one. A write-up still names the printer it used; the catalog just stops pretending that makes a category.

**🔒 The public site stays high-level and concise — LOCKED.** Tech pages and toy `description`/`short` fields are a **one-or-two-word summary of what the instrument is for**, not a capability inventory. New capabilities, accessories, verified specs, safety notes and operating nuance go in **`work/IDEAS.md`**, never onto the public pages. This has now been decided twice (the Star Analyser 100, 2026-07-19: *"a grating is an accessory rather than a headline instrument, so ownership is recorded here only"*; the Dino-Lite's UV fluorescence, same day, reverted). **Don't propose enriching a toy description because a capability turns out to be more interesting than its label suggests** — that's exactly the impulse the lock exists to stop. The registry answers *what do we own*; IDEAS.md answers *what can it do*.

**Instrument names must exactly match `technology.yml`** everywhere in code and prose — don't abbreviate, prefix, or rearrange words. (Per-instrument data-format notes belong in the project's `index.md` Setup table, not here.) The former top-level `archives/` folder — instrument catalogs, walk-up guides, the UNR/UBC landscape survey — was removed July 2026 when SIL access ended; recoverable from git history if ever needed.

## PREPPING A RUN (`work/IDEAS.md` projects)

When James asks to go deeper on a project from `work/IDEAS.md`, two things are wanted and a third is not:

- **The steps of the run, concretely.** What happens in what order, what's being measured, where the technique is fiddly, and what failure looks like — including failures that produce a plausible-but-wrong number rather than an obvious error.
- **Acquisition bottlenecks.** Which reagents, samples or consumables are *not* already in the house, and which are slow or awkward to get. Flag them early: with many projects live across the sciences, anything waiting on an order yields to something that isn't, so knowing the bottleneck reorders the queue rather than blocking it.
- **Do not compare units of work across sciences.** No "this is a fraction of an IYPT problem," no effort-equivalence between chemistry and biology and astronomy. **James handles parallelization and scheduling himself** and does not need Claude's estimate of relative size.

Findings from a deep dive get folded back into that project's entry in `work/IDEAS.md` — the doc carries decisions, numbers, hazards and gotchas, not the walkthrough prose, which is cheap to regenerate.

**Physics problem leads are generated.** Each `work/physics/problems/<n> <name>/PAPER Leads.pdf` (paywalled papers worth retrieving by hand) is built from **`work/physics/archives/leads.yml`** by `python3 work/physics/archives/build_leads.py` (optionally with problem numbers: `… build_leads.py 8 13`). Both live in `archives/` to keep `work/physics/` to just `archives/ problems/` — but the script is **live tooling, not dead reference material**; it writes into `../problems/`. Edit the YAML and rebuild; never hand-edit the PDFs. Rendering is Chrome headless `--print-to-pdf`, same as `work/overview.pdf`.

**Update `IDEAS.md` continuously while brainstorming — don't wait to be asked, and don't batch it to the end of a session.** A brainstorm that revises what a project needs (or corrects a wrong read of one) is exactly the durable content the doc exists to hold; leaving it in chat loses it. **Record corrections as corrections** — say what the earlier read was and that it was wrong, so a future session doesn't re-derive the same mistake from the stale sketch that's still sitting in a table nearby.

## STAGING GALLERY CANDIDATES

Images destined for the site land first in **`work/scratch/gallery/`**. **Never stage bare
images** — always ship the context with them, because whoever builds the page needs hover text,
captions and filter tags, and cannot recover any of it from the pixels.

Each staging batch carries two sidecars:
- **`metadata.yml`** — the machine-readable one, and the one to parse. Per asset: `title`,
  `alt` (hover), `caption`, `tags`, `exposure`, `confidence`, and `caveat` where the result is
  weaker than it looks.
- **`README.md`** — the prose: what the batch is, how it was produced, and what would be wrong
  to claim from it.

⚠️ **Tag every asset `kind: capture` or `kind: figure`.** A *capture* is byte-for-byte instrument
output and may go in the Stargazing/Cellgazing capture galleries, which forbid any pixel edit. A
*figure* is derived from our own reduction and must **not** go there — it belongs on a project
page, where analysis is the point. Cropping a capture turns it into a figure.

Record confidence honestly at staging time. A caption written months later from a filename will
overstate a 3-sigma result as readily as a 20-sigma one.

Staging is the front half of one pipeline: `work/scratch/gallery/` → a row in
`web/public/projects/gallery.yml` → a tile on the wall. See § THE WALL.

## THE WALL (`/projects/`)

`/projects/` is **one chronological grid of pictures and nothing else** — no inventory, no links
below the fold, no second kind of content. That emptiness is the design, not an omission: the
page answers "what have they been doing" at a glance, and anything that invites reading instead
of looking belongs somewhere other than here. Two tile kinds, both from `gallery.yml`:

- **photo tile** — `src:` a picture. Caption + note + toy + month appear on hover.
- **project card** — `folder:` + `hero:`. Framed in its science colour, permanently captioned,
  links to the project page. Its caption is read from that project's `index.md` title, never
  retyped. A card's hero must not also be a photo tile; the build rejects the duplicate.

**Where pixels live.** `src:`/`hero:` are paths under `web/public/projects/` — exactly what
follows `/projects/` in the URL.
- A picture inside a project folder is referenced **in place**. Never copy it into `gallery/`,
  or the same bytes land in git twice. The build checks this by **content hash**, not just by
  path — two names for the same capture is a build error. That is not hypothetical: the
  Statistics hero turned out to be a byte-for-byte copy of a Catfood project photo, and two
  staged spectroscopy RAWs were copies of Stargazing frames.
- Everything else lives flat in **`gallery/photos/`**, named `YYYYMMDD Some Name.ext`. The date
  prefix is the filing system — the same convention project folders use — so the folder sorts
  itself and a file states its own date without a sidecar. No month subfolders.
- **`gallery/thumbs/`** is generated, never hand-edited, and **not optional**. `build_gallery.py`
  shrinks every oversized source to a long-edge-1000 copy with `sips` and prunes thumbs whose row
  is gone. CDN caching is not a substitute: the originals total ~58 MB and a gallery is precisely
  the page that requests all of them; thumbs take that to ~9 MB. An edge cache changes who serves
  the bytes, not how many a browser downloads to fill a 200 px tile.

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
the filename *or on any folder above it* (which dates both `gallery/photos/` and every generated
plot by its project folder); then EXIF. Between them a row almost never needs a date by hand.
Tiles sort newest-month-first, and within a month are dealt round-robin across the sciences so a
busy week in one science doesn't land as a slab of near-identical frames.

**Tags.** `science:` is required. `toy:` names the instrument, shows in the caption, and rolls up
to that instrument's category. `tech:` names the category directly — use it when a picture belongs
to a category but to no instrument we own. Either way the build fails on a name the catalog does
not have, which is what keeps the filter row and the home page the same vocabulary.

**A tile shows one line and one pill.** The caption on the bottom left, the *science* on the
bottom right — not the category, not the instrument, not the date. The lightbox shows exactly the
same two things over the picture. `note:` is still carried in `gallery.yml` and in the JSON but is
**no longer rendered anywhere**; fold anything load-bearing into the `caption:`.

**Filtering is one tier.** Just the six sciences. A category row was built, then a third row of
individual toys under it, and both were removed within the day — the wall is a gallery, and every
extra axis of selection made the header busier without making the pictures easier to find.
Categories still live in `technology.yml` and still show on the home page's Projects tab as an
organising principle; they simply do not filter here. Home-page links land on `/projects/#<sci>`.

**`tech:`/`toy:` are still validated** even though nothing on the wall filters on them, because
the validation is what keeps the vocabulary honest and the data is still the record of what a
picture is about.

**Captions are load-bearing — verify them against the actual frame.** Several first-pass captions
here described the wrong instrument entirely (a bench of samples called "the printed jig"). Render
the tiles and look before shipping copy.

## AUTHORING A RESEARCH PROJECT

Each project is a date-prefixed folder under `web/public/projects/`. The public-facing overview is **`index.md`** (not `README.md`) — Astro's loader globs `*/index.md`, so the filename matters. Model new pages on `20260420 UV-Vis Spectroscopy/index.md` or `20260419 IR Spectroscopy/index.md`.

```
YYYYMMDD Project Name/
├── data/      # Raw instrument data (CSVs, spectra). NEVER modify — read-only.
├── photos/    # Experiment photos, split by purpose (see below)
│   ├── setup/    # Setup + sample shots — feed the top-page shuffle
│   ├── samples/  # (optional) sample close-ups — also shuffled
│   └── data/     # Handwritten data sheets — excluded from shuffle; shown via #data-grid
├── papers/    # Background papers
├── output/    # ALL generated output: *.py/*.ipynb, *.png plots, *.csv/*.json processed data
└── index.md   # Overview, methods, results
```

Create these subdirs as needed and follow the existing names rather than inventing new ones. **Never modify raw data** — read from `data/`, write everything generated to `output/`.

**Gallery projects are gone.** `20260725 Stargazing` and `20260725 Cellgazing` were project folders holding only curated tiles and a hand-laid grid — galleries pretending to be write-ups. Both folded into the wall 2026-07-30, their frames moved to `gallery/photos/`. `work/astronomy/output/collect_media.py` still copies Seestar captures out byte-for-byte and now prints `gallery.yml` rows instead of page HTML. Raw Seestar FITS **may be published as-is** — the `SITELAT`/`SITELONG` headers no longer need scrubbing (decided 2026-07-29; see § VISIBILITY & SECURITY).

**Photos.** The shuffle pool is **auto-populated** by `Project.astro`: its `getStaticPaths` scans every `.jpg`/`.jpeg`/`.png` under `photos/` (`setup/` + `samples/`, **never `data/`**) and injects them as `window._pagePhotos`. So:
- **Don't** list photos in frontmatter or add a per-page inline `_pagePhotos` script — the layout's shuffle script runs on every project page.
- Name files sequentially in capture order: `setup1.jpeg`, `setup2.jpeg`, … / `data1.jpeg`, …. `git mv` originals (e.g. `20240920 Catfood G.jpeg`) so references stay short and stable.
- `photos/data/` (handwritten sheets) is surfaced explicitly via a hand-coded in-page `#data-grid` of plain `<img>` — the `[slug]` route filters it out of the shuffle so it never hits the hero. Keep that contract if you add subfolders.

**Page structure.** Frontmatter (`project: [Short Name]`) → `# [Experiment Title]` → hero → body. Hero:
- **4+ photos** → shuffle grid (pool auto-populates; no `photos:` array, no inline script):
  ```html
  <div class="photo-grid" id="photo-grid"><img id="photo-0" alt="…"><img id="photo-1" alt="…"><img id="photo-2" alt="…"><img id="photo-3" alt="…"></div>
  <button class="shuffle-btn" onclick="shufflePhotos()">Shuffle Photos</button>
  ```
- **1 photo** → `<div class="hero-single"><img src="photos/[file]" alt="…"></div>`
- Then `<div class="project-meta">[Month Dayth Year]<br>[Instrument name]</div>` (right-aligned, Instrument on its own line).

Body sections **in order**: `## Overview` (1–2 para) · `## Setup` (Category/Details table + procedure prose) · `## Samples` (**top-level `##`**, not under Setup) · `## Data` (format; if `photos/data/` has sheets, add the hand-coded `#data-grid` — `three-col` for 3, shuffle button only if >4) · `## Results` (link **written report → static notebook → Colab**, in that order). `## Results` is the **last thing in the file** — no footer or nav div: `Project.astro` injects `<PageFooter />` and the science-colored tech pills automatically. **Never add a `#`/row-number column to any table** (repo-wide rule) — row order conveys sequence.

**Registering a project = one frontmatter edit** (plus a `folder:` row in `gallery.yml` if it should have a card on the wall). The project's `tech:` array is the only registration step; `build_technology.py` reverse-scans it and bakes the project list into each tech's `technology.json` entry (consumed by the research page, tech-detail pages, and the Apple app). Add any new instrument as a Toy under the appropriate tech in `technology.yml`. Cross-links are fully automatic:
- **Project → tech:** `Project.astro` renders one science-colored **pill** per `tech:` entry, linking to `/projects/technology/<science>/<Tech>/`. (This replaced the old hand-coded `<div id="technology">` table in `ce2a710` — don't re-add such a table.)
- **Tech → project:** the `build_technology.py` reverse-scan above.

**Writing style — toolkit notes, not publications.** A fast future-you glance at what the tech does and what makes it different from its neighbors; the scaffold for research, not the research. Model density: the two Spectroscopy pages above.
- **Note-and-bullet first** — short bullets over paragraphs; 1–2 sentences when a paragraph is needed.
- **Differentiate, don't summarize** — lead with what distinguishes each tech/toy from the others; if two toys measure the same thing, say which this page uses and why.
- **Cut publication scaffolding** — no abstract intros, no "in this work we…", no non-load-bearing motivation.
- **Font styling judicious** — one or two bolds per section (the instrument's proper noun or the differentiator). Sub/superscripts only when the notation carries information (`λ<sub>max</sub>` yes; italicizing every verb no).
- **Push specs to Setup tables** — ranges, software names, filename patterns, cuvette sizes live in the Setup/Data table, not prose. Let tabs and section-heads carry the structure.

## THE `/research/` → `/projects/` RENAME (2026-07-30)

The whole vertical was renamed: nav label, URL, page directory, public directory, Astro
collection base, and the Swift API client. Two things about it are easy to trip over later:

- **Project folders lost a path segment.** They were `web/public/research/projects/<Name>/`,
  serving at `/research/projects/<Name>/`. They are now `web/public/projects/<Name>/`, serving at
  `/projects/<Name>/` — one level, not two, sitting as siblings of `technology/` and `gallery/`.
  `build_technology.py` selects them by their `YYYYMMDD` prefix rather than by directory.
- **`web/public/_redirects` keeps every old URL alive**, and is not optional. App Store builds in
  the wild fetch `/research/technology.json` and `/research/projects/<folder>/index.md`;
  `URLSession` follows the 301s, so those installs keep working until the next release. Cloudflare
  Workers Static Assets reads that file — the Worker itself is still a pure passthrough.

The Apple source now points at `/projects/technology.json` but **a release has not shipped**, and
`ResearchScience.projectIndexURL` still accepts the old prefix so a stale cached manifest resolves.

**The app's tech browser was replaced by the gallery (2026-07-30).** `ResearchView.swift` is gone —
it rendered per-tech pages from `hero` and `tech_url`, and once the website deleted its tech pages
the build stopped emitting both, so the tab had quietly degraded to a list of names. In its place
`GalleryView.swift` renders the wall from `gallery.json`; `ProjectDetailView` moved to its own file
and is unchanged. `technology.json` is still fetched — it is what `ProjectDetailView` uses to
resolve a project's tech pills and its photo pool. **Still not released**; installed copies keep
showing the old tech browser until a build ships.

## CONTENT BUILDS & DEPLOY

**Every `*.json` under `web/public/` is generated — never edit it by hand; edit the `.yml`/source and rebuild.** The website (client-side JS) and the Apple app fetch the same JSON, so a stale manifest silently ships bad data to the app (the `.githooks/pre-commit` guard exists for exactly this).

- **Olympiads + textbooks** — edit `olympiads/olympiads.yml`, then `python pipeline/scripts/build_olympiads.py` (from repo root) → `olympiads.json`.
- **Technology / toys** — edit `technology.yml` (+ project `tech:` frontmatter), then `python pipeline/scripts/build_technology.py` → `technology.json`.
- **The wall** — edit `projects/gallery.yml`, then `python pipeline/scripts/build_gallery.py` → `gallery.json` (+ thumbnails). See § THE WALL. The script also bakes each project's **shuffle photo list** (`projects[].photos`, every image under `photos/` except `photos/data/`, mirroring the `[slug]` route's build-time walk) — so **adding or renaming a project photo means rebuilding this JSON**, or the native apps show an empty photo grid. That list is how the apps get the pool; they used to walk the GitHub contents API, which is unauthenticated and rate-limited.
- **Curriculum** — a **one-time build**: the `.docx` sources were dropped (`f8e7ad3`), so `curriculum.json` and `source/*.md` are now committed artifacts. `web/public/curriculum/notes/` is **gone too** — its six rendered `.pdf` handouts went with the home page's per-subject "pdf" links on 2026-07-30 (**the site is web-only now: don't re-add a downloadable handout to any page**). To regenerate a subject, recreate `notes/` and drop its `.docx` back in; a missing directory just makes `build_curriculum.py` skip every subject. No database, no API, no admin endpoint.
- **`work/overview.pdf`** (the shareable three-pager; not web-served) — **its source is the print template embedded in `work/IDEAS.md`'s final appendix**, not a separate file (`work/scratch/overview.html` was retired 2026-07-25 after the two drifted). Never edit the PDF, and don't recreate a standalone `.html`: extract the template with the `awk` sentinel command in that appendix and render it with **Chrome headless `--print-to-pdf`** — both commands are written out there, verified to reproduce the committed PDF. **Page 2 restates §2's instrument runs and page 3 the per-science project lists**, so a section edit and the appendix edit are one pass, not two.

**Build & deploy** — `cd web && pnpm build` (writes to `../pipeline/worker/dist/`), then `cd pipeline/worker && pnpm run deploy` (wrangler ships `dist/` via Static Assets). GitHub push is backup only. Follow the global commit/push/deploy default for self-contained one-off changes; pause it while iterating on a multi-turn redesign.

- **Local preview** — `cd web && pnpm dev` (port 4321, hot reload). After a change, `open -a Safari 'http://127.0.0.1:4321/<path>'` so the user sees the real native rendering (`qlmanage -t -s 1200 -o /tmp <file>.html` is only an inline-in-chat fallback).
- **One-off mockups** — non-Astro HTML in `work/scratch/<topic>.html` (tracked; serve with `live-server`); layout-aware Astro in `web/src/pages/scratch-<topic>.astro`, view via `pnpm dev`, then `git restore`. Promote a chosen asset by moving it into the appropriate tracked path (a tech folder or a project's `output/`).
- **Pre-commit hook** — `.githooks/pre-commit` is committed but **activated per-clone**: `git config core.hooksPath .githooks` once on a fresh machine. Warn-only (never blocks): flags staged PDFs over the 5 MB soft cap, and flags a staged source (`.yml` / tech-page `index.md`) whose generated JSON isn't also staged.

## ANALYSIS & NOTEBOOKS

- **Tools** — flexible; default to the Python scientific stack (pandas, numpy, scipy, matplotlib, seaborn) absent a strong reason otherwise.
- ⚠️ **Astronomy reduction needs the repo venv at `work/astronomy/.venv`** — `astropy` / `astroquery` / `scipy` are **not installed system-wide on any interpreter**, so `python3 script.py` fails with `ModuleNotFoundError` no matter which python you reach for. Run these as `work/astronomy/.venv/bin/python output/<script>.py`. The venv is gitignored (`.venv/`), so **a fresh clone must rebuild it**:

  ```sh
  cd work/astronomy && /opt/homebrew/bin/python3.14 -m venv .venv
  .venv/bin/pip install astropy astroquery numpy scipy matplotlib
  ```

  Created 2026-07-29, after the working copy was found to be living in an **ephemeral session scratchpad** that would have vanished before the next observing night. Plate solving is separate and system-wide: `/opt/homebrew/bin/solve-field` (astrometry.net) with the Gaia index files 4212–4216.
- **Reproducibility** — every script runnable end-to-end from the project folder, with comments explaining each step. Pin versions in `requirements.txt` if the pipeline uses non-standard packages. Always inspect/summarize raw data (shape, missing values, outliers, units) before analysis and flag anything unexpected.
- **Visualizations** — matplotlib/seaborn with clear axis labels, units, titles, legends; save PNG at 300 dpi (into an `output/images/` subfolder if a project produces many, else directly into `output/`).
- **Jupyter conventions:**
  - **Colab compatibility** — data references use absolute GitHub raw URLs (`https://raw.githubusercontent.com/vivianweidai/science/main/...`); ship notebooks **with outputs** so GitHub renders statically.
  - **Sections** — numbered markdown headings (`## 1. Title`, …); typical flow Data Collection → Load/Inspect → Visualize → Statistical Test → Conclusion.
  - **Output** — plain `print()`; no HTML boxes, no `IPython.display`, no spacing hacks. Keep code tight.
  - **Chart styling** — matplotlib defaults (no custom fonts/facecolors). Soft muted pastels: Mathematics `#c5d9f7`, Computing `#d9ccee`, Physics `#f9c4a8`, Chemistry `#d4e8a0`, Biology `#a8ddd4`, Astronomy `#f4c2cb`; data line traces slightly deeper (e.g. `#d95f5f`). Light and airy — never saturated or bold.
  - **Colab badge** — final markdown cell: a `---` separator, then just the badge link (no text): `<a href="COLAB_URL"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="vertical-align:middle;"></a>`

## VISIBILITY & SECURITY

Synced to `vivianweidai/science` and served at `vivianweidai.com` — **everything is publicly viewable**.

- **No sensitive or personal information.** In particular, **never include researcher names** in public-facing files — project pages carry Date + Instrument, not Researchers.
- **Observing location is publishable** (decided 2026-07-29, superseding the earlier "never include lab location" rule). Seestar FITS keep their `SITELAT`/`SITELONG` headers, and a project page may name the observing site. Researcher names stay off the site regardless — the two were previously one rule and are now decoupled.
- **Results links** point to the GitHub blob URL (`https://github.com/vivianweidai/science/blob/main/...`) so files render inside GitHub.
- **PDFs — soft cap 5 MB.** Compress: `gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=out.pdf in.pdf` (`/screen` for image-heavy manuals). Verify: a mid-doc page renders (`pdftoppm -r 60 -f 50 -l 50 out.pdf /tmp/check`), page count matches, and `gs` reported zero "Page drawing error" warnings. Tools: `brew install ghostscript poppler`.
- **Before any commit, scan staged paths for oversized images** and shrink offenders — once a large blob is in git history it stays there forever.

## APPLE APP (`apple/`)

*(Architecture folded in from the retired `apple/README.md`, 2026-07-18 — `apple/` now holds only source + project files, like the other repos.)*

Universal SwiftUI app ("My Science" on the App Store) mirroring vivianweidai.com on iPhone + iPad, with an embedded watchOS companion focused on the olympiads timeline. All data comes from public GitHub raw / `vivianweidai.com` URLs — no auth, no backend, no writes.

### Architecture

The SwiftPM package (`Package.swift`, iOS 17 + watchOS 10) is split in two so the watch target shares data + grouping logic without dragging in WebKit:

- **`ScienceCore`** — platform-neutral `Models/`, `API/` clients, and the `ActivityGrouping` / `SubjectPaletteRGB` helpers (`shared/Core/`). Builds on iOS, watchOS, macOS.
- **`ScienceCoreUI`** — iOS-only SwiftUI views + the KaTeX `MarkdownWebView` (`shared/UI/`). Depends on `ScienceCore`.

The iPhone/iPad target (`ios/`) imports `ScienceCoreUI`; the watch target (`watch/`) imports only `ScienceCore` and owns its own views. The watch app is **embedded in the iOS bundle** — installing on iPhone auto-installs the companion on a paired watch. Bundle IDs `com.vivianweidai.science` / `.science.watchkitapp`.

Three tabs (`shared/UI/Views/RootTabView.swift`), each reading a generated JSON manifest — the same ones the webapp uses:

- **Curriculum** — cascading subject → section → topic → table browser from `curriculum/curriculum.json`; tables fetched from GitHub raw URLs, rendered with KaTeX in a `WKWebView`.
- **Olympiads** — contests + unified textbooks from `olympiads/olympiads.json`. The watch companion renders this tab only (offline-first cache at `Caches/olympiads_cache.json`).
- **Projects** — the same wall the website shows, from `projects/gallery.json`. A science filter, a two-column grid of tiles (caption bottom-left, science bottom-right), tapping a photo opens the full-resolution pager, tapping a project card opens that project's `index.md` in the markdown reader, and a clip hands off to the system player. Because it reads the same manifest the site builds, **a row added to `gallery.yml` appears in the app with no release** — only layout changes need one.

**Markdown shell contract** (`shared/UI/Rendering/katex-shell.html`, kept byte-identical with the Android copy). Three things a project page can rely on in-app:
- **Page `<style>` blocks are honored** (they used to be stripped). The gallery pages — Stargazing, Cellgazing — carry their whole layout inline, so stripping it broke the hero band and ran the tile captions together. CommonMark treats `<style>` as a type-1 HTML block, so marked passes it through blank lines and all. A page `<script>` still never runs (innerHTML doesn't execute scripts) — anything interactive has to be native.
- **Images open a native zoomable viewer**, not Safari: the shell posts the tapped image plus the page's full image list over an `imageTap` bridge and `ImageViewerView` pages through them (pinch, double-tap, swipe). Non-image links still hand off to Safari.
- **`<video>`/`<source>` relative `src` is resolved** like `<img>`, and the WebView allows inline autoplay — that combination is what makes the Stargazing solar hero play.

`apple/project.yml` is the XcodeGen spec (regenerate the gitignored `Science.xcodeproj` with `xcodegen generate`).

### App Store release

The native app is built + submitted from the main dev box. Run from `apple/`. **This repo is public — the concrete App Store Connect account identifiers (team ID, app ID, API Key ID, issuer, account-holder name) are NOT stored here.** Keep them in an untracked local file (`apple/.release.env`, gitignored) or the operator's own records; the `.p8` upload key stays at `~/.appstoreconnect/private_keys/` (600 perms) and is referenced by path, never committed.

**Signing gotcha (the thing that wastes a cycle):** the dev box typically has only an *Apple Development* cert — **no distribution cert** — and an *App Manager* API key **cannot do cloud signing** (`No signing certificate "iOS Distribution" found`). Fix without an Admin key: run `xcodebuild -exportArchive` **without** the `-authenticationKey*` args so it re-signs for distribution via the **signed-in Xcode account session** (the team's account holder can create the dist cert/profiles silently with `-allowProvisioningUpdates`), export a local IPA, then upload separately with `altool`.

**Flow (from `apple/`):**
1. `xcodegen generate`
2. Bump the version in `project.yml` (`MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`).
3. `xcodebuild -project Science.xcodeproj -scheme Science -configuration Release -destination 'generic/platform=iOS' -archivePath build/Science.xcarchive -allowProvisioningUpdates archive`
4. `xcodebuild -exportArchive -archivePath build/Science.xcarchive -exportOptionsPlist <plist: method=app-store-connect, destination=export, signingStyle=automatic, teamID=…> -exportPath build/export -allowProvisioningUpdates` (**no** auth key → the Xcode session signs)
5. `xcrun altool --upload-app -f build/export/Science.ipa -t ios --apiKey <KEY_ID> --apiIssuer <ISSUER>`
6. Build processes a few min. Then in ASC web: iOS App **+** → new version → **What's New** → **Add Build** → release option → **Add for Review** → **Submit for Review**.

`ITSAppUsesNonExemptEncryption: NO` is set in `project.yml`, so export-compliance never prompts. Direct-to-device dev install (for review) is separate: `xcodebuild … build`, then `xcrun devicectl device install app --device <coredevice-id> <Science.app>` (phone must be unlocked to launch).
