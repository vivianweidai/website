# SCIENCE — Claude Code Instructions

Personal science portfolio + lab notebook — live on [vivianweidai.com](https://vivianweidai.com) and the [App Store](https://apps.apple.com/app/id6762091743) (iPhone + iPad, with an embedded Apple Watch companion). Curriculum reference tables, an Olympiad timeline, and hands-on research projects (raw data, photos, notebooks, reproducible pipelines). Your role: process experimental data and build reproducible analysis pipelines — parse raw instrument outputs, clean and validate, analyze, visualize.

This CLAUDE.md is the repo's only doc — the README was folded in and deleted 2026-07-17 (Claude-maintained; even though the repo is public, James opted out of README upkeep).

## STACK

- **Astro 5** — static site generator. Builds to `pipeline/worker/dist/` (co-located with the Worker that serves it) via `outDir: '../pipeline/worker/dist'`.
- **Cloudflare Workers + Static Assets** — serves the build output at `vivianweidai.com`. The Worker is a true passthrough to the `ASSETS` binding (no edge logic).
- **GitHub** — source control only. Push triggers nothing.
- **Apple** — native app in `apple/` consumes `vivianweidai.com/{olympiads,research,curriculum}/*.json` (and per-discipline markdown under `curriculum/source/`). See § APPLE APP.

## REPO STRUCTURE

Top-level reads like every other repo: `apple/ web/ pipeline/ work/` + this doc. **The entire Astro app lives in `web/`** — its `astro.config.mjs`, `package.json`, `tsconfig.json`, `src/`, and `public/` (relocated from the repo root 2026-07-17 to keep the root clean; `src/`/`public/` stay at Astro's defaults *inside* `web/`). **All `pnpm` commands run from `web/`.**

- **`web/src/`** — `content.config.ts` (Content Collections: **`projects`** + **`tech`**); `layouts/` holds the `.astro` components *and* their imported CSS/JS; `pages/` is file-based routing (`research/` carries the dynamic `[slug]` project route + `[science]/[tech]` tech route).
- **`web/public/`** — source-of-truth served **verbatim at the site root**. Areas: `curriculum/` (`source/*.md` + `curriculum.json`), `olympiads/` (`olympiads.yml`), `research/` (`projects/<YYYYMMDD Name>/`, `technology/<science>/<Tech>/index.md` with a sibling `hero:` image + flat photos, `technology.yml`). `<science>` is the full word (mathematics, computing…) to mirror `curriculum/source/`.
- **`pipeline/`** — `worker/` (CF Worker: ASSETS passthrough → `dist/`) + `scripts/` (`build_olympiads.py` / `build_technology.py`, YAML→JSON; `build_curriculum.py`, .docx→markdown). Scripts resolve paths from their own location, so run them **from the repo root**; they write into `web/public/`.
- **`work/`** — research works-in-progress, git-tracked but **NOT web-served**. One dir per science (`physics/` `chemistry/` `biology/` `astronomy/`) + `IDEAS.md`. Named `work/` (not `projects/`) to stay distinct from the public `web/public/research/projects/`. **`work/scratch/`** is the rough scratchpad (tracked + pushed — backed up and distributed across machines; the relocated home of the old `~/GITHUB/scratch/`, 2026-07-16). Three-stage flow, all tracked — the difference is polish and web-visibility, not whether it's in git: `work/scratch/<topic>` (rough) → `work/<science>/` (organized WIP) → `web/public/research/projects/` (published).
- **`work/IDEAS.md`** (moved from the repo root 2026-07-17) — the research program's living doc: **ideation** (idea backlog) + **progress tracking** (the "Active work & progress" dashboard and in-flight detail like the home molecular-biology lab). Promote an idea to a dated project folder when a pilot starts; keep the dashboard and idea statuses current.

**Convention deviation: no top-level `content/`; source-of-truth lives under `web/public/`.** The cross-repo convention puts source-of-truth in a top-level `content/`. We deviate because Astro's `public/` is served verbatim at the site root — so `web/public/` **is** the content dir: a file at `web/public/X/Y` serves at `/X/Y`, 1:1, no rewrites, no sync step. Page URLs and asset URLs coexist under the same prefix (`/research/projects/<folder>/` is the rendered HTML; `/research/projects/<folder>/index.md` is the raw markdown the apps fetch; `/research/projects/<folder>/photos/…` are the photos). The Content Collection loader points at `./public/research/projects/` (relative to the `web/` Astro root); the dynamic route's photo discovery walks the same path.

## DATA MODEL — TECHNOLOGIES & TOYS

The Research pages (`vivianweidai.com/research/`) are organized around two concepts:

- **Technology (Tech)** — a research capability, a row on the Research page (e.g. *Spectroscopy*, *Photometry*, *Radio*). A way of asking nature a question.
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
| Science (card) | `science` | — | `/research/#<slug>` | — |
| Tech (row) | `techs[].tech` | `tech:` | `/research/technology/<sci>/<Tech>/` | `tech` |
| Toy (instrument) | `toys[].name` (under a tech) | `toys:` array | — | — |

`technology.yml` is **one flat entry per science** (`science:` + `techs:`; the old topic/category grouping tiers were dropped). It is the **source of truth for instruments and which Techs they enable**; a tech's spec (`techs[].specs`) lives here and nowhere else.

**🔒 The public site stays high-level and concise — LOCKED.** Tech pages and toy `description`/`short` fields are a **one-or-two-word summary of what the instrument is for**, not a capability inventory. New capabilities, accessories, verified specs, safety notes and operating nuance go in **`work/IDEAS.md`**, never onto the public pages. This has now been decided twice (the Star Analyser 100, 2026-07-19: *"a grating is an accessory rather than a headline instrument, so ownership is recorded here only"*; the Dino-Lite's UV fluorescence, same day, reverted). **Don't propose enriching a toy description because a capability turns out to be more interesting than its label suggests** — that's exactly the impulse the lock exists to stop. The registry answers *what do we own*; IDEAS.md answers *what can it do*.

**Instrument names must exactly match `technology.yml`** everywhere in code and prose — don't abbreviate, prefix, or rearrange words. (Per-instrument data-format notes belong in the project's `index.md` Setup table, not here.) The former top-level `archives/` folder — instrument catalogs, walk-up guides, the UNR/UBC landscape survey — was removed July 2026 when SIL access ended; recoverable from git history if ever needed.

## PREPPING A RUN (`work/IDEAS.md` projects)

When James asks to go deeper on a project from `work/IDEAS.md`, two things are wanted and a third is not:

- **The steps of the run, concretely.** What happens in what order, what's being measured, where the technique is fiddly, and what failure looks like — including failures that produce a plausible-but-wrong number rather than an obvious error.
- **Acquisition bottlenecks.** Which reagents, samples or consumables are *not* already in the house, and which are slow or awkward to get. Flag them early: with many projects live across the sciences, anything waiting on an order yields to something that isn't, so knowing the bottleneck reorders the queue rather than blocking it.
- **Do not compare units of work across sciences.** No "this is a fraction of an IYPT problem," no effort-equivalence between chemistry and biology and astronomy. **James handles parallelization and scheduling himself** and does not need Claude's estimate of relative size.

Findings from a deep dive get folded back into that project's entry in `work/IDEAS.md` — the doc carries decisions, numbers, hazards and gotchas, not the walkthrough prose, which is cheap to regenerate.

**Update `IDEAS.md` continuously while brainstorming — don't wait to be asked, and don't batch it to the end of a session.** A brainstorm that revises what a project needs (or corrects a wrong read of one) is exactly the durable content the doc exists to hold; leaving it in chat loses it. **Record corrections as corrections** — say what the earlier read was and that it was wrong, so a future session doesn't re-derive the same mistake from the stale sketch that's still sitting in a table nearby.

## AUTHORING A RESEARCH PROJECT

Each project is a date-prefixed folder under `web/public/research/projects/`. The public-facing overview is **`index.md`** (not `README.md`) — Astro's loader globs `*/index.md`, so the filename matters. Model new pages on `20260420 UV-Vis Spectroscopy/index.md` or `20260419 IR Spectroscopy/index.md`.

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

**Gallery projects** (`20260725 Stargazing`, `20260725 Cellgazing`) are the one deviation: their curated JPEG/MP4 tiles live in **`data/`**, *not* `photos/`, precisely so the `[slug]` route's shuffle scan skips them (renamed from `media/` 2026-07-25 — the tiles are byte-for-byte instrument captures, so `data/` names them honestly) — a gallery page hand-lays out its own grid and would fight the auto hero. The originals stay in `work/<science>/data/` (gitignored when they're instrument-sized), and an `output/collect_media.py` regenerates `data/` from them, so the crops and stretches are reproducible rather than hand-edited. Raw Seestar FITS **may be published as-is** — its `SITELAT`/`SITELONG` headers no longer need scrubbing (decided 2026-07-29; see § VISIBILITY & SECURITY).

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

**Registering a project = one frontmatter edit.** The project's `tech:` array is the only registration step; `build_technology.py` reverse-scans it and bakes the project list into each tech's `technology.json` entry (consumed by the research page, tech-detail pages, and the Apple app). Add any new instrument as a Toy under the appropriate tech in `technology.yml`. Cross-links are fully automatic:
- **Project → tech:** `Project.astro` renders one science-colored **pill** per `tech:` entry, linking to `/research/technology/<science>/<Tech>/`. (This replaced the old hand-coded `<div id="technology">` table in `ce2a710` — don't re-add such a table.)
- **Tech → project:** the `build_technology.py` reverse-scan above.

**Writing style — toolkit notes, not publications.** A fast future-you glance at what the tech does and what makes it different from its neighbors; the scaffold for research, not the research. Model density: the two Spectroscopy pages above.
- **Note-and-bullet first** — short bullets over paragraphs; 1–2 sentences when a paragraph is needed.
- **Differentiate, don't summarize** — lead with what distinguishes each tech/toy from the others; if two toys measure the same thing, say which this page uses and why.
- **Cut publication scaffolding** — no abstract intros, no "in this work we…", no non-load-bearing motivation.
- **Font styling judicious** — one or two bolds per section (the instrument's proper noun or the differentiator). Sub/superscripts only when the notation carries information (`λ<sub>max</sub>` yes; italicizing every verb no).
- **Push specs to Setup tables** — ranges, software names, filename patterns, cuvette sizes live in the Setup/Data table, not prose. Let tabs and section-heads carry the structure.

## CONTENT BUILDS & DEPLOY

**Every `*.json` under `web/public/` is generated — never edit it by hand; edit the `.yml`/source and rebuild.** The website (client-side JS) and the Apple app fetch the same JSON, so a stale manifest silently ships bad data to the app (the `.githooks/pre-commit` guard exists for exactly this).

- **Olympiads + textbooks** — edit `olympiads/olympiads.yml`, then `python pipeline/scripts/build_olympiads.py` (from repo root) → `olympiads.json`.
- **Research** — edit `technology.yml` (+ project `tech:` frontmatter), then `python pipeline/scripts/build_technology.py` → `technology.json`. The script also bakes each project's **shuffle photo list** (`projects[].photos`, every image under `photos/` except `photos/data/`, mirroring the `[slug]` route's build-time walk) — so **adding or renaming a project photo means rebuilding this JSON**, or the native apps show an empty photo grid. That list is how the apps get the pool; they used to walk the GitHub contents API, which is unauthenticated and rate-limited.
- **Curriculum** — a **one-time build**: the `.docx` sources were dropped (`f8e7ad3`), so `curriculum.json` and `source/*.md` are now committed artifacts. Re-add a subject's `.docx` to `web/public/curriculum/notes/` only to regenerate it. No database, no API, no admin endpoint.
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
- **Research** — tech browser from `research/technology.json` (one card per science → flat techs); project links open an in-app markdown render of the project's `index.md`, external links hand off to Safari.

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
