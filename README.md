# Science

Personal science portfolio and lab notebook — available on [web](https://vivianweidai.com) and the [App Store](https://apps.apple.com/app/id6762091743) for iPhone and iPad (with an embedded Apple Watch companion).

## What's Inside

- **Curriculum** — Interactive reference tables across six subjects (Mathematics, Computing, Physics, Chemistry, Biology, Astronomy) with LaTeX-rendered formulas via KaTeX.
- **Olympiads** — Filterable timeline of academic competitions and study materials.
- **Research** — Hands-on projects using lab instruments (FT-IR spectrometer, four-point probe, melting point system, centrifuge, miniPCR). Each project includes raw data, photos, Jupyter notebooks, and reproducible analysis pipelines.


## Structure

```
src/
  layouts/                 Astro components + their CSS/JS/images (bundled)
  pages/                   File-based routing
  content.config.ts        Content collection config
pipeline/worker/           Cloudflare Worker (Static Assets passthrough)
pipeline/scripts/          Python build scripts (.docx → markdown, YAML → JSON)
public/                    Source-of-truth — served at site root, organized by page
  curriculum/              notes/ + source/ + curriculum.json
  olympiads/               olympiads.{yml,json}
  research/                projects/ + technology/ + technology.{yml,json}
apple/                     iOS + watchOS app (SwiftUI, read-only)
```

## Tech Stack

- **Site** — Astro 5, HTML/CSS/JS, KaTeX
- **Analysis** — Python (pandas, numpy, scipy, matplotlib), Jupyter Notebooks
- **Data** — YAML/JSON source of truth, Word docs for curriculum
- **Hosting** — Cloudflare Workers + Static Assets (custom domain `vivianweidai.com`)
