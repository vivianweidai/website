# SCIENCE

**`website`** — the publication repository of Vivian's journey into science, live on vivianweidai.com and the App Store. *(Renamed from `science` on 2026-08-01 to match its purpose; GitHub redirects the old URLs.)* The repo has three verticals of Curriculum, Olympiads and Projects served on the two surfaces of the webapp and the iOS app. A couple of relevant links in this repo are:

- for publishing the iOS app, refer to `apple/APPSTORE.md`
- for publishing to the Projects vertical, refer to `web/public/projects/PROJECTS.md`
- naming convention for `.md` files: lowercase for content (`report.md`), uppercase for instructions (`CLAUDE.md`, `PROJECTS.md`)
- this repo is **public** — flag anything personal before it goes in, then it is James's call

## THE THREE VERTICALS

The site, the app, and this repo are organized around exactly three content verticals. Everything in `web/public/` belongs to one of them.

| Vertical | Source of truth | Generated | What it is |
|---|---|---|---|
| **Curriculum** | `web/public/curriculum/content/*.md` | `curriculum.json` | Reference tables across the six Olympiad disciplines. **Largely done** — a stable body of reference material, not an active front. |
| **Olympiads** | `web/public/olympiads/olympiads.yml` | `olympiads.json` | Contests + unified textbooks on a timeline. **A journal** — it gets a row when something happens. |
| **Projects** | `web/public/projects/` (folders + `thewall/thewall.yml`) | `thewall.json` | Hands-on research: raw data, photos, notebooks, reproducible pipelines. **The frontier** — where the work happens. |

## THE TWO SURFACES

All three verticals are served by **both** surfaces, from **the same generated JSON**. Neither surface has a backend, an admin endpoint, or a database; both read static manifests.

- **Web app** — Astro 5 → Cloudflare Workers + Static Assets at `vivianweidai.com`.
- **iOS app** — universal SwiftUI ("My Science"), three tabs mirroring the three verticals, plus an embedded watchOS companion focused on the Olympiads timeline.

## STACK

- **Astro 5** — static site generator. Builds to `pipeline/worker/dist/` (co-located with the Worker that serves it) via `outDir: '../pipeline/worker/dist'`.
- **Cloudflare Workers + Static Assets** — serves the build output at `vivianweidai.com`. The Worker is a true passthrough to the `ASSETS` binding (no edge logic).
- **GitHub** — source control only. Push triggers nothing.
- **The whole Astro app lives in `web/`** (`astro.config.mjs`, `package.json`, `src/`, `public/`) — **all `pnpm` commands run from there.** `web/public/` is served verbatim at the site root, which is why there is no top-level `content/`.
- **Apple** — native app in `apple/` consumes `vivianweidai.com/{olympiads,projects,curriculum}/*.json` (and per-discipline markdown under `curriculum/content/`).

## CONTENT BUILDS & DEPLOY

**Every `*.json` under `web/public/` is generated — never edit it by hand; edit the `.yml`/source and rebuild.** The website (client-side JS) and the Apple app fetch the same JSON, so a stale manifest silently ships bad data to the app (the `.githooks/pre-commit` guard exists for exactly this).

- **Curriculum** — a **one-time build**: the `.docx` sources were dropped (`f8e7ad3`), so `curriculum.json` and `content/*.md` are committed artifacts. `curriculum/notes/` and its rendered PDFs went 2026-07-30 — **the site is web-only; don't re-add a downloadable handout.** To regenerate a subject, recreate `notes/` and drop its `.docx` back in.
- **Olympiads + textbooks** — edit `olympiads/olympiads.yml`, then `python pipeline/scripts/build_olympiads.py` (from repo root) → `olympiads.json`.
- **The wall** — see `web/public/projects/PROJECTS.md`; rebuild with `python pipeline/scripts/build_thewall.py`.
- 🔴 **Renaming any published path means adding a rule to `web/public/_redirects`.** Shipped App Store builds hardcode URLs and follow 301s, so a rename without a rule breaks installed copies silently, with no error anywhere, until the next release. Five renames are covered there; the reasoning for each lives in that file, including why every source pattern must stay **disjoint**.
- **Build & deploy** — `cd web && pnpm build` (writes to `../pipeline/worker/dist/`), then `cd pipeline/worker && pnpm run deploy` (wrangler ships `dist/` via Static Assets). GitHub push is backup only.
- **Local preview** — `cd web && pnpm dev` (port 4321, hot reload). After a change, `open -a Safari 'http://127.0.0.1:4321/<path>'` so the user sees the real native rendering (`qlmanage -t -s 1200 -o /tmp <file>.html` is only an inline-in-chat fallback).
- **Pre-commit hook** — `.githooks/pre-commit` is committed but **activated per-clone**: `git config core.hooksPath .githooks` once on a fresh machine. Warn-only (never blocks): flags staged PDFs over the 5 MB soft cap, and flags a staged source (`.yml`) whose generated JSON isn't also staged.

## APPLE APP

Universal SwiftUI app ("My Science" on the App Store) mirroring vivianweidai.com on iPhone + iPad, with an embedded watchOS companion focused on the olympiads timeline. All data comes from public GitHub raw / `vivianweidai.com` URLs — no auth, no backend, no writes.

### Architecture

The SwiftPM package (`Package.swift`, iOS 17 + watchOS 10) is split in two so the watch target shares data + grouping logic without dragging in WebKit:

- **`ScienceCore`** — platform-neutral `Models/`, `API/` clients, and the `ActivityGrouping` / `SubjectPaletteRGB` helpers (`shared/Core/`). Builds on iOS, watchOS, macOS.
- **`ScienceCoreUI`** — iOS-only SwiftUI views + the KaTeX `MarkdownWebView` (`shared/UI/`). Depends on `ScienceCore`.

The iPhone/iPad target (`ios/`) imports `ScienceCoreUI`; the watch target (`watch/`) imports only `ScienceCore` and owns its own views. The watch app is **embedded in the iOS bundle** — installing on iPhone auto-installs the companion on a paired watch. Bundle IDs `com.vivianweidai.science` / `.science.watchkitapp`. **There is no separate watch submission**: the embedded app rides inside the one iOS IPA, shares its `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION`, and goes through review with it — so watch changes never wait on a release of their own.

Three tabs (`shared/UI/Views/RootTabView.swift`), each reading a generated JSON manifest — the same ones the webapp uses:

- **Curriculum** — cascading subject → section → topic → table browser from `curriculum/curriculum.json`; tables fetched from GitHub raw URLs, rendered with KaTeX in a `WKWebView`.
- **Olympiads** — contests + unified textbooks from `olympiads/olympiads.json`. The watch companion renders this tab only (offline-first cache at `Caches/olympiads_cache.json`). Both surfaces carry the timeline's four standing markers in the website's own vocabulary — ⭐ invited/attended, 🎯 competitive, 🇨🇦 Team Canada/alternate — and the watch's detail badges use its label set (FOUNDATION / ATTENDED / INVITED / COMPETITIVE / TEAM CANADA / ALTERNATE).
- **Projects** — the same wall the website shows, from `projects/thewall/thewall.json`, and laid out by the same rules (`WallMetrics` ports the CSS grid): **landscape and square tiles span two columns**, portraits take one, tiles stay in manifest order and a half-filled row keeps its gap rather than back-filling. **A photo tile carries no text** — caption and science pill belong to project cards, which are also framed in their science colour and badged `PROJECT →`. Tapping a photo opens the full-resolution pager; a project card opens that project's `report.md` in the markdown reader; **a clip autoplays muted in place and opens with controls in-app** (`ClipView.swift`). Because it reads the same manifest the site builds, **a row added to `thewall/thewall.yml` appears in the app with no release** — only layout changes need one.
  - ⚠️ **Tiles load through `RemoteImage`, never `AsyncImage`.** The wall stopped shipping thumbnails 2026-07-30, so `src` *is* the 2000px original; `AsyncImage` would decode ~12 MB per tile to fill a 190 pt box. `RemoteImage` downsamples at decode time and caches the result.
  - 🎬 **Clips must play from a downloaded copy, never from their https URL.** `vivianweidai.com` answers a `Range:` request with a plain `200` and the whole body — no `Accept-Ranges`, no `206` — and **AVFoundation will not start a remote asset it cannot seek**, so both wall clips sat on their poster frame forever, silently, with no error anywhere. `ClipCache` (in `ClipView.swift`) fetches the bytes with `URLSession`, which does not care, parks them in `Caches/clips/`, and hands AVPlayer a file URL. Browsers tolerate the same response, which is why the website's `<video>` tags never showed the problem. **If the range behaviour is ever fixed at the edge, this stays correct — it just stops being load-bearing.** Verify a clip by screenshotting the wall twice a few seconds apart and diffing: a poster is byte-identical, playback is not.

**`APIClient` fetches exactly two manifests** — `olympiads.json` and `thewall.json` — plus `curriculum.json` via `CurriculumLoader`. Nothing else.

**Markdown shell contract** (`shared/UI/Rendering/katex-shell.html`). Three things a project page can rely on in-app:
- **Page `<style>` blocks are honored** (they used to be stripped). CommonMark treats `<style>` as a type-1 HTML block, so marked passes it through blank lines and all. A page `<script>` still never runs (innerHTML doesn't execute scripts) — anything interactive has to be native.
- **Images open a native zoomable viewer**, not Safari: the shell posts the tapped image plus the page's full image list over an `imageTap` bridge and `ImageViewerView` pages through them (pinch, double-tap, swipe). Non-image links still hand off to Safari.
- **`<video>`/`<source>` relative `src` is resolved** like `<img>`, and the WebView allows inline autoplay — that combination is what makes the Stargazing solar hero play.
- `apple/project.yml` is the XcodeGen spec (regenerate the gitignored `Science.xcodeproj` with `xcodegen generate`).
