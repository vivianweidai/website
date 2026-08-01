# SCIENCE — Claude Code Instructions

Personal science portfolio + lab notebook — live on [vivianweidai.com](https://vivianweidai.com) and the [App Store](https://apps.apple.com/app/id6762091743) (iPhone + iPad, with an embedded Apple Watch companion). Curriculum reference tables, an Olympiad timeline, and hands-on projects (raw data, photos, notebooks, reproducible pipelines).

This CLAUDE.md is the repo's **orientation doc**: the three verticals, the two surfaces that serve them, and the plumbing they share. The README was folded in and deleted 2026-07-17 (Claude-maintained; even though the repo is public, James opted out of README upkeep).

> 📁 **Working on the Projects vertical? Read `../sandbox/PROJECTS.md` first.** The
> technology/toy vocabulary, the wall, authoring a project page, prepping and running an
> experiment, and the analysis conventions all live there, not here — in the **`sandbox` repo**,
> which is where that vertical is actually worked on. That includes edits to
> **`web/public/projects/` and `thewall.yml`**, which live in *this* repo and so
> would never route you there on their own. This doc will not tell you the rules for any of it.
>
> 🔭 **Running an observing night? Read `../sandbox/astronomy/NIGHT.md` first** — and note that
> the night's plan usually already exists in `../sandbox/astronomy/output/setup/night_run.py`.

## THE THREE VERTICALS

The site, the app, and this repo are organized around exactly three content verticals. Everything in `web/public/` belongs to one of them.

| Vertical | Source of truth | Generated | What it is |
|---|---|---|---|
| **Curriculum** | `web/public/curriculum/source/*.md` | `curriculum.json` | Reference tables across the six Olympiad disciplines. **Largely done** — a stable body of reference material, not an active front. |
| **Olympiads** | `web/public/olympiads/olympiads.yml` | `olympiads.json` | Contests + unified textbooks on a timeline. **A journal** — it gets a row when something happens. |
| **Projects** | `web/public/projects/` (folders + `thewall.yml`); WIP in the **`sandbox` repo** | `thewall.json` | Hands-on research: raw data, photos, notebooks, reproducible pipelines. **The frontier** — where the work happens. |

**Projects is where we live, but it is still one vertical of three.** Its rules are extensive enough to crowd out everything else, which is why they moved to `PROJECTS.md` (2026-07-31) — and then out of this repo entirely with `work/` (2026-08-01). The manual lives where the vertical is worked on.

### ⚠️ `work/` left this repo — the gate

**`work/` moved to the private [`sandbox`](https://github.com/vivianweidai/sandbox) repo on 2026-08-01**, with its history (subtree split, 225 commits). This repo is now purely a **publishing entity**; the work happens next door.

**The boundary is one-way: `sandbox` → `science`, never the reverse.** Two things cross:
- **Images** → `web/public/projects/thewall/`, written by `sandbox/astronomy/output/setup/collect_media.py`, which finds this repo via `$SCIENCE_REPO` or the sibling `~/GITHUB/science` path.
- **Finished write-ups** → `web/public/projects/`.

⚠️ **Crossing the gate is a private-to-public act.** `sandbox` is private and this repo is PUBLIC, so anything promoted becomes world-readable — read what's crossing, not just its filename. Nothing in this repo is ever a source for `sandbox`.

## THE TWO SURFACES

All three verticals are served by **both** surfaces, from **the same generated JSON**. Neither surface has a backend, an admin endpoint, or a database; both read static manifests.

- **Web app** — Astro 5 → Cloudflare Workers + Static Assets at `vivianweidai.com`.
- **iOS app** — universal SwiftUI ("My Science"), three tabs mirroring the three verticals, plus an embedded watchOS companion focused on the Olympiads timeline. See § APPLE APP.

⚠️ **This is why a stale manifest is a real bug, not a cosmetic one:** the app fetches the same file the website does, so a `.json` that wasn't rebuilt ships bad data to installed copies with no release and no warning. The `.githooks/pre-commit` guard exists for exactly this.

## STACK

- **Astro 5** — static site generator. Builds to `pipeline/worker/dist/` (co-located with the Worker that serves it) via `outDir: '../pipeline/worker/dist'`.
- **Cloudflare Workers + Static Assets** — serves the build output at `vivianweidai.com`. The Worker is a true passthrough to the `ASSETS` binding (no edge logic).
- **GitHub** — source control only. Push triggers nothing.
- **Apple** — native app in `apple/` consumes `vivianweidai.com/{olympiads,projects,curriculum}/*.json` (and per-discipline markdown under `curriculum/source/`). See § APPLE APP.

## REPO STRUCTURE

Top-level reads like every other repo: `apple/ web/ pipeline/` + this doc (`work/` left for `sandbox` 2026-08-01). **The entire Astro app lives in `web/`** — its `astro.config.mjs`, `package.json`, `tsconfig.json`, `src/`, and `public/` (relocated from the repo root 2026-07-17 to keep the root clean; `src/`/`public/` stay at Astro's defaults *inside* `web/`). **All `pnpm` commands run from `web/`.**

- **`web/src/`** — `content.config.ts` (**one** Content Collection: `projects`; the `tech` collection and the `technology/[science]/[tech]` route went with the toy catalog 2026-07-30); `layouts/` holds the `.astro` components *and* their imported CSS/JS; `pages/` is file-based routing, with `projects/` carrying the dynamic `[slug]` project route.
- **`web/public/`** — source-of-truth served **verbatim at the site root**. Areas: `curriculum/` (`source/*.md` + `curriculum.json`), `olympiads/` (`olympiads.yml`), `projects/` (`<YYYYMMDD Name>/` project folders sitting **directly** under it, plus `thewall.yml` + `thewall/<science>/`). `<science>` is the full word (mathematics, computing…) to mirror `curriculum/source/`.
- **`pipeline/`** — `worker/` (CF Worker: ASSETS passthrough → `dist/`) + `scripts/` (`build_olympiads.py` / `build_thewall.py`, YAML→JSON; `build_curriculum.py`, .docx→markdown). Scripts resolve paths from their own location, so run them **from the repo root**; they write into `web/public/`.
- **The work itself is in [`sandbox`](https://github.com/vivianweidai/sandbox)**, a sibling checkout at `~/GITHUB/sandbox` — one dir per science plus `scratch/`, `IDEAS.md` (the research program's living doc), `PROJECTS.md` (the Projects vertical's manual) and `astronomy/NIGHT.md` (the observing-night front door). The three-stage flow now spans two repos: `sandbox/scratch/<topic>` (rough) → `sandbox/<science>/` (organized WIP) → **the gate** → `web/public/projects/` (published). See `sandbox/CLAUDE.md`.

**Convention deviation: no top-level `content/`; source-of-truth lives under `web/public/`.** The cross-repo convention puts source-of-truth in a top-level `content/`. We deviate because Astro's `public/` is served verbatim at the site root — so `web/public/` **is** the content dir: a file at `web/public/X/Y` serves at `/X/Y`, 1:1, no rewrites, no sync step. Page URLs and asset URLs coexist under the same prefix (`/projects/<folder>/` is the rendered HTML; `/projects/<folder>/index.md` is the raw markdown the apps fetch; `/projects/<folder>/photos/…` are the photos). The Content Collection loader points at `./public/projects/` (relative to the `web/` Astro root); the dynamic route's photo discovery walks the same path.

## URL RENAMES — the compatibility contract

**`web/public/_redirects` keeps every old URL alive**, and is not optional. App Store builds in the
wild fetch `/research/technology.json` and `/research/projects/<folder>/index.md`; `URLSession`
follows the 301s, so those installs keep working until the next release. Cloudflare Workers Static
Assets reads that file — the Worker itself is still a pure passthrough.

Two renames are covered: **`/research/` → `/projects/`** (2026-07-30) and **`gallery` → `thewall`**
(2026-08-01, the wall's manifest and picture folder). The second needs *two* rules, not one —
`/projects/gallery.json` for the URL shipped builds hardcode, and `/projects/gallery/*` for anything
still holding an older copy of the manifest, whose tiles point at the old picture folder.

*(The path-shape half of the `/research/` rename — project folders losing a directory level — is in
`sandbox/PROJECTS.md`.)*

**The app's tech browser was replaced by the wall (2026-07-30).** `ResearchView.swift` is gone —
it rendered per-tech pages from `hero` and `tech_url`, and once the website deleted its tech pages
the build stopped emitting both, so the tab had quietly degraded to a list of names. In its place
`TheWallView.swift` renders the wall from `thewall.json`; `ProjectDetailView` moved to its own file.
**`technology.json` is no longer fetched at all** — a project's pills come from its own `sciences:`
front matter and its shuffle pool from the `photos` array `build_thewall.py` bakes into that
project's card on the wall. `APIClient` fetches exactly two manifests now (`olympiads.json`,
`thewall.json`), plus `curriculum.json` via `CurriculumLoader`. Shipping in **1.5.6**.

## CONTENT BUILDS & DEPLOY

**Every `*.json` under `web/public/` is generated — never edit it by hand; edit the `.yml`/source and rebuild.** The website (client-side JS) and the Apple app fetch the same JSON, so a stale manifest silently ships bad data to the app (the `.githooks/pre-commit` guard exists for exactly this).

- **Olympiads + textbooks** — edit `olympiads/olympiads.yml`, then `python pipeline/scripts/build_olympiads.py` (from repo root) → `olympiads.json`.
- **Technology / toys — gone, don't rebuild it.** `technology.yml`, `technology.json`, `web/public/projects/technology/` and `build_technology.py` were all deleted 2026-07-30 with the toy catalog. Projects still carry a `tech:` frontmatter array and `content.config.ts` still accepts it, but **nothing reads it** — it is vestigial, not a live input. The *vocabulary* survives in `sandbox/PROJECTS.md`; the generated layer does not.
- **The wall** — edit `projects/thewall.yml`, then `python pipeline/scripts/build_thewall.py` → `thewall.json` (+ thumbnails). See § THE WALL. The script also bakes each project's **shuffle photo list** (`projects[].photos`, every image under `photos/` except `photos/data/`, mirroring the `[slug]` route's build-time walk) — so **adding or renaming a project photo means rebuilding this JSON**, or the native apps show an empty photo grid. That list is how the apps get the pool; they used to walk the GitHub contents API, which is unauthenticated and rate-limited.
- **Curriculum** — a **one-time build**: the `.docx` sources were dropped (`f8e7ad3`), so `curriculum.json` and `source/*.md` are now committed artifacts. `web/public/curriculum/notes/` is **gone too** — its six rendered `.pdf` handouts went with the home page's per-subject "pdf" links on 2026-07-30 (**the site is web-only now: don't re-add a downloadable handout to any page**). To regenerate a subject, recreate `notes/` and drop its `.docx` back in; a missing directory just makes `build_curriculum.py` skip every subject. No database, no API, no admin endpoint.
- **`sandbox/overview.pdf`** (the shareable three-pager; not web-served, and now in the other repo) — **its source is the print template embedded in `sandbox/IDEAS.md`'s final appendix**, not a separate file (`scratch/overview.html` was retired 2026-07-25 after the two drifted). Never edit the PDF, and don't recreate a standalone `.html`: extract the template with the `awk` sentinel command in that appendix and render it with **Chrome headless `--print-to-pdf`** — both commands are written out there, verified to reproduce the committed PDF. **Page 2 restates §2's instrument runs and page 3 the per-science project lists**, so a section edit and the appendix edit are one pass, not two.

**Build & deploy** — `cd web && pnpm build` (writes to `../pipeline/worker/dist/`), then `cd pipeline/worker && pnpm run deploy` (wrangler ships `dist/` via Static Assets). GitHub push is backup only. Follow the global commit/push/deploy default for self-contained one-off changes; pause it while iterating on a multi-turn redesign.

- **Local preview** — `cd web && pnpm dev` (port 4321, hot reload). After a change, `open -a Safari 'http://127.0.0.1:4321/<path>'` so the user sees the real native rendering (`qlmanage -t -s 1200 -o /tmp <file>.html` is only an inline-in-chat fallback).
- **One-off mockups** — non-Astro HTML in `sandbox/scratch/<topic>.html` (tracked; serve with `live-server`); layout-aware Astro in `web/src/pages/scratch-<topic>.astro`, view via `pnpm dev`, then `git restore`. Promote a chosen asset by moving it into the appropriate tracked path (a tech folder or a project's `output/`).
- **Pre-commit hook** — `.githooks/pre-commit` is committed but **activated per-clone**: `git config core.hooksPath .githooks` once on a fresh machine. Warn-only (never blocks): flags staged PDFs over the 5 MB soft cap, and flags a staged source (`.yml` / tech-page `index.md`) whose generated JSON isn't also staged.

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

The iPhone/iPad target (`ios/`) imports `ScienceCoreUI`; the watch target (`watch/`) imports only `ScienceCore` and owns its own views. The watch app is **embedded in the iOS bundle** — installing on iPhone auto-installs the companion on a paired watch. Bundle IDs `com.vivianweidai.science` / `.science.watchkitapp`. **There is no separate watch submission**: the embedded app rides inside the one iOS IPA, shares its `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION`, and goes through review with it — so watch changes never wait on a release of their own.

Three tabs (`shared/UI/Views/RootTabView.swift`), each reading a generated JSON manifest — the same ones the webapp uses:

- **Curriculum** — cascading subject → section → topic → table browser from `curriculum/curriculum.json`; tables fetched from GitHub raw URLs, rendered with KaTeX in a `WKWebView`.
- **Olympiads** — contests + unified textbooks from `olympiads/olympiads.json`. The watch companion renders this tab only (offline-first cache at `Caches/olympiads_cache.json`). Both surfaces carry the timeline's four standing markers in the website's own vocabulary — ⭐ invited/attended, 🎯 competitive, 🇨🇦 Team Canada/alternate — and the watch's detail badges use its label set (FOUNDATION / ATTENDED / INVITED / COMPETITIVE / TEAM CANADA / ALTERNATE). The watch showed only `invited` until 1.5.6, silently dropping three of the four.
- **Projects** — the same wall the website shows, from `projects/thewall.json`, and laid out by the same rules (`WallMetrics` ports the CSS grid): **landscape and square tiles span two columns**, portraits take one, tiles stay in manifest order and a half-filled row keeps its gap rather than back-filling. **A photo tile carries no text** — caption and science pill belong to project cards, which are also framed in their science colour and badged `PROJECT →`. **The science filter is the toolbar bubble menu, the same one Olympiads uses** — a port of the web's pill row was built and removed the same day (2026-07-31): the web page needs a filter row because it has no toolbar, the app has one, and matching the website is not a reason to pass up the native idiom. Tapping a photo opens the full-resolution pager; a project card opens that project's `index.md` in the markdown reader; **a clip autoplays muted in place and opens with controls in-app** (`ClipView.swift`). Because it reads the same manifest the site builds, **a row added to `thewall.yml` appears in the app with no release** — only layout changes need one.
  - ⚠️ **Tiles load through `RemoteImage`, never `AsyncImage`.** The wall stopped shipping thumbnails 2026-07-30, so `src` *is* the 2000px original; `AsyncImage` would decode ~12 MB per tile to fill a 190 pt box. `RemoteImage` downsamples at decode time and caches the result.
  - 🎬 **Clips must play from a downloaded copy, never from their https URL.** `vivianweidai.com` answers a `Range:` request with a plain `200` and the whole body — no `Accept-Ranges`, no `206` — and **AVFoundation will not start a remote asset it cannot seek**, so both wall clips sat on their poster frame forever, silently, with no error anywhere. `ClipCache` (in `ClipView.swift`) fetches the bytes with `URLSession`, which does not care, parks them in `Caches/clips/`, and hands AVPlayer a file URL. Browsers tolerate the same response, which is why the website's `<video>` tags never showed the problem. **If the range behaviour is ever fixed at the edge, this stays correct — it just stops being load-bearing.** Verify a clip by screenshotting the wall twice a few seconds apart and diffing: a poster is byte-identical, playback is not.

**Markdown shell contract** (`shared/UI/Rendering/katex-shell.html`, kept byte-identical with the Android copy). Three things a project page can rely on in-app:
- **Page `<style>` blocks are honored** (they used to be stripped). CommonMark treats `<style>` as a type-1 HTML block, so marked passes it through blank lines and all. *(The bug that forced this was the Stargazing and Cellgazing pages, which carried their whole layout inline — stripping it broke their hero band and ran the tile captions together. **Both pages were retired 2026-07-30** when they folded into the wall, so the original reproduction is gone; the behaviour stays because any project page may style itself inline.)* A page `<script>` still never runs (innerHTML doesn't execute scripts) — anything interactive has to be native.
- **Images open a native zoomable viewer**, not Safari: the shell posts the tapped image plus the page's full image list over an `imageTap` bridge and `ImageViewerView` pages through them (pinch, double-tap, swipe). Non-image links still hand off to Safari.
- **`<video>`/`<source>` relative `src` is resolved** like `<img>`, and the WebView allows inline autoplay — that combination is what makes the Stargazing solar hero play.

`apple/project.yml` is the XcodeGen spec (regenerate the gitignored `Science.xcodeproj` with `xcodegen generate`).

### App Store release, screenshots, simulator driving → `apple/RELEASE.md`

The six-step `xcodegen` → `xcodebuild` → `altool` → ASC-web flow, the **signing gotcha** that
wastes a cycle (no distribution cert + an App Manager key cannot cloud-sign), how to resubmit a
version already *Waiting for Review*, the current screenshot sets, and the `cliclick` simulator
coordinate math all live in **`apple/RELEASE.md`**. It is a procedure run ~3×/year; this doc is
orientation. Nothing was dropped in the move.
