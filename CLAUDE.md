# Website

`website` — the publication repository of Vivian's journey into science, live on vivianweidai.com and the App Store.

- for the iOS app — how it is built and how to ship it — refer to `apple/APPLE.md`
- for publishing to the Projects vertical, refer to `web/public/projects/PROJECTS.md`
- this repo is public — flag anything personal before it goes in, then it is James's call
- this file is locked. Material changes need James's agreement; tweaks and corrections do not. New detail belongs at the edge, in the folder it describes


## The three verticals

The site, the app, and this repo are organized around exactly three content verticals. Everything in `web/public/` belongs to one of them.

| Vertical | Source of truth | Generated | What it is |
|---|---|---|---|
| Curriculum | `web/public/curriculum/content/*.md` | `curriculum.json` | Reference tables across the six Olympiad disciplines. Largely done — a stable body of reference material, not an active front. |
| Olympiads | `web/public/olympiads/olympiads.yml` | `olympiads.json` | Contests + unified textbooks on a timeline. A journal — it gets a row when something happens. |
| Projects | `web/public/projects/` (folders + `thewall/thewall.yml`) | `thewall.json` | Hands-on research: raw data, photos, notebooks, reproducible pipelines. The frontier — where the work happens. |


## The two surfaces

All three verticals are served by both surfaces, from the same generated JSON. Neither surface has a backend, an admin endpoint, or a database; both read static manifests.

- Web app — Astro 5 → Cloudflare Workers + Static Assets at `vivianweidai.com`.
- iOS app — universal SwiftUI ("My Science"), three tabs mirroring the three verticals, plus an embedded watchOS companion focused on the Olympiads timeline.


## Stack

| Piece | Where | Notes |
|---|---|---|
| Astro 5 | `web/` | Static site generator. Builds to `pipeline/worker/dist/` via `outDir: '../pipeline/worker/dist'`, co-located with the Worker that serves it. All `pnpm` commands run from `web/` |
| Cloudflare Workers + Static Assets | `pipeline/worker/` | Serves the build output at `vivianweidai.com`. A true passthrough to the `ASSETS` binding, no edge logic |
| GitHub | — | Source control only. Push triggers nothing |
| Apple app | `apple/` | Consumes `vivianweidai.com/{olympiads,projects,curriculum}/*.json`, plus per-discipline markdown under `curriculum/content/` |

`web/public/` is served verbatim at the site root, which is why there is no top-level `content/`.


## Content builds and deployment

Every `*.json` under `web/public/` is generated — never edit it by hand; edit the `.yml`/source and rebuild. The website (client-side JS) and the Apple app fetch the same JSON, so a stale manifest silently ships bad data to the app (the `.githooks/pre-commit` guard exists for exactly this).

- Curriculum — a one-time build: the `.docx` sources were dropped (`f8e7ad3`), so `curriculum.json` and `content/*.md` are committed artifacts. To regenerate a subject, recreate `notes/` and drop its `.docx` back in.
- Olympiads + textbooks — edit `olympiads/olympiads.yml`, then `python pipeline/scripts/build_olympiads.py` (from repo root) → `olympiads.json`.
- The wall — see `web/public/projects/PROJECTS.md`; rebuild with `python pipeline/scripts/build_thewall.py`.
- Renaming any published path means adding a rule to `web/public/_redirects`. Shipped App Store builds hardcode URLs and follow 301s, so a rename without a rule breaks installed copies silently, with no error anywhere, until the next release. Five renames are covered there; the reasoning for each lives in that file, including why every source pattern must stay disjoint.
- Build & deploy — `cd web && pnpm build` (writes to `../pipeline/worker/dist/`), then `cd pipeline/worker && pnpm run deploy` (wrangler ships `dist/` via Static Assets). GitHub push is backup only.
- The Cloudflare Worker is named `science`, and must stay that way. It is not a mistake and not a leftover to tidy up — deploy output saying `Uploaded science` is correct. `vivianweidai.com` is bound to the Worker of that name; renaming it deploys a SECOND, empty Worker and leaves the domain on the old one, so the site keeps serving the previous deployment while every new deploy goes nowhere visible. A Cloudflare resource name is not a repo name and nothing requires them to match. (Confusing extra: `science` is now also the name of the private working repo, which is unrelated to this Worker.) Full reasoning in `pipeline/worker/wrangler.toml`.
- Local preview — `cd web && pnpm dev` (hot reload), then `open -a Safari 'http://localhost:<port>/<path>/'` so the user sees the real native rendering (`qlmanage -t -s 1200 -o /tmp <file>.html` is only an inline-in-chat fallback). Five things bite here:
  - `localhost`, never `127.0.0.1`. Vite binds IPv6 loopback only — `lsof -nP -iTCP -sTCP:LISTEN` shows `TCP [::1]:4321`, with nothing on IPv4 — so `127.0.0.1` is refused outright (curl exit 7, empty reply). `localhost` resolves to `::1` first and works.
  - Read the port from the startup banner; do not assume 4321. If 4321 is occupied Vite prints `Port 4321 is in use, trying another one...` and silently moves to 4322, 4323, … The `┃ Local` line is the truth. A dev server backgrounded with a bare `&` outlives its shell and squats the port invisibly — hence the drift. Kill strays with `lsof -ti :4321 | xargs kill -9` before assuming the page is broken; a 404/000 on 4321 is usually a stale server, not a bad page.
  - Trailing slash is mandatory. `astro.config.mjs` sets `trailingSlash: 'always'`, so `/projects/Foo` 404s and `/projects/Foo/` is 200. Percent-encode spaces when checking with curl (`%20`); Safari does it for you.
  - Never run `pnpm build` while `pnpm dev` is up. The build rewrites `web/.astro/content-assets.mjs` out from under the dev server, which then 500s on every route with `Failed to load url /.astro/content-assets.mjs`. It looks like a broken page; it is a broken server — restart it. Renaming a project folder also needs a restart: the content collection caches the folder list and hot reload does not see a rename.
  - Verifying a fresh deploy needs a cache-buster. The edge copy is served for a minute or two after `wrangler deploy`, so a just-published page can 404 and `thewall.json` can come back at its old tile count. `curl "…?cb=$(date +%s)"` gets the truth; without it you will go debugging a deploy that actually worked.
- Pre-commit hook — `.githooks/pre-commit` is committed but activated per-clone: `git config core.hooksPath .githooks` once on a fresh machine. Warn-only (never blocks): flags staged PDFs over the 5 MB soft cap, and flags a staged source (`.yml`) whose generated JSON isn't also staged.
