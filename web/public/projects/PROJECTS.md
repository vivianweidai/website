# Projects

How the published Projects vertical is structured: the picture wall at `/projects/`, and the project report pages under it. These rules live beside the files they govern — `thewall.yml`, `thewall/<science>/` and the `<YYYYMMDD Name>/` folders are all in this directory.


## The Wall

One folder per science; a picture belongs to exactly one.

    astronomy/20260730 M 31.jpg
    ^ science ^ sorts ^ for you, on disk

Nothing in the filename reaches a screen, so it is plumbing, not copy — it does two jobs: the folder is the science, and the `YYYYMMDD` prefix orders the wall (the date the picture joined, not necessarily when it was shot). The rest is just how you find the file. It is not used as `alt`/`aria-label`: the site is for personal consumption and the build should not compute what nothing renders.

Adding one: drop the file in, run `python3 pipeline/scripts/build_thewall.py`. No YAML for a photo tile. Resize on the way in — long edge 2000, `sips -Z 2000 in.jpg --out in.jpg`. There is no thumbnail folder; the wall and lightbox load these files directly, and there is deliberately no `thumbs/` folder, because a second generated copy is one more thing to explain and keep pruned. Full-resolution originals live outside the published site.

Video is a tile like any other: an `.mp4` autoplays muted and loops, dimensions come from the MP4 header (`tkhd`, rotation honoured), served without re-encoding. Give it a still named `<name>.poster.jpg` — the tile shows it before playing, and the iOS app shows it instead of the video.

`thewall.yml` holds project cards only. A card is a link, so it gets a caption (read from the project's `report.md` title, never retyped), a science pill and a `Report →` badge, framed in its science colour — a card must not read as one more photo. `hero:` names which image inside the project folder fronts it; that hero is the only thing that still points into a project folder. A project gets exactly one tile.

Layout. Landscape and square tiles span two columns, portraits one — a portrait gets its presence from its aspect ratio, and a 4:3 photo at one column is a stamp. `grid-auto-flow: row dense` back-fills the hole a wide tile leaves at the end of a row; local order shifts, which on a wall reads as packing. Clicking opens a lightbox — ‹ › buttons, ← → keys, Esc, click-backdrop to dismiss. It pages through currently visible tiles, so a filtered wall stays inside its filter, and skips project cards because those are links. Neighbours preload.

Dating and sorting. One source: a `YYYYMMDD` prefix on the filename or any folder above it, which dates every generated plot by its project folder. A file the build cannot date is a build error — there is no EXIF fallback and no `date:` row key. Tiles sort newest month first, then by filename descending within the month, so the filename is the one lever for placement and renaming a file moves its tile. Ordering is otherwise untouched: the wall is hand-curated, and pictures named to sit together must stay together.

A wrong picture is the only way left to be wrong, so look at the frames before shipping. Nothing on the page will ever correct a misleading image, and a filename that misidentifies its subject still reaches screen readers and the JSON.


## Project Reports

Each project is a date-prefixed folder under `web/public/projects/`. The page is `report.md` — not `README.md`, because Astro's loader globs `*/report.md`.

```
YYYYMMDD Project Name/
├── photos/
│   ├── setup/     # the rig — instrument, mounting, bench checks
│   ├── data/      # what came off the instrument, as pictures
│   └── figures/   # finished plots, copied over from science
└── report.md
```

**The two repos are split by job, and the split is strict.**

`science` is where the work happens: raw data, scripts, notebooks, the Python environment, and all the iterating. A reduction gets rewritten, a defect gets fixed, the numbers move — that all belongs there, and it keeps rolling.

`website` is publication only. A project folder holds `report.md` and pictures. **No data, no scripts, no notebooks, no logic of any kind.** When a figure is finished in `science`, its PNG is copied into `photos/figures/` as a finished product. Nothing here is ever run, so nothing here can drift out of step with anything.

That is the whole point of the split: maintaining two copies of the same scripts and the same frames is upkeep that buys nothing, because the published page is a *snapshot* either way — this data, reduced this way, on this date. Reproducibility lives in `science`, where the data and the interpreter already are. If a later re-reduction moves the numbers, that is new science on the same data and earns a dated revision on the page, not a quiet overwrite.

A report may still name a script and quote a few lines of it. That is prose describing what was done, it is what makes the page teachable, and it creates no upkeep because nothing here runs. It just does not ship the file.

The reason that is enough: these are teaching pages, not publications. A real publication carries its data and its code so a stranger can check the result, and if one of these ever becomes that, shipping both becomes a deliberate decision made at the time. Until then a page and the `science` repo do not have to stay coherent with each other — the page is a snapshot of what was understood on a date, and `science` keeps moving. If you ever need to verify a number or re-run a figure, the script and the frames are still there.

Two hard constraints behind the rule. `web/public/` is served verbatim, so anything under a project folder is published, publicly downloadable, and re-uploaded to Cloudflare on every deploy. And this repo is public with effectively permanent history, so a 16 MB FITS committed once cannot be taken back. `.gitignore` carries `projects/*/data/` and `projects/*/output/` as a guard against both.

The historical project report pages had their own format with shuffled photos at the top and tables of instruments. Lets park those as legacy. Moving forward, while the folder structure remains similar, let's structure report.md more as instructional step-by-step guides that take us from data to analysis. We will start this experiment with the Stellar Spectroscopy project. Any generally applicable lessons learned for generalizing the presentation will be saved as notes below.


### The Walkthrough Format

First built for `20260729 Spectroscopy`. The classes live in `layouts/Project.astro`, not in the page, so a second report inherits the format instead of re-inventing it. Nothing here is per-project styling — if a page needs a `<style>` block, that is a signal the format is missing something and the layout should grow it.

| Class | For |
|---|---|
| `.lede` | the one paragraph before step 1 — what this is, in a breath |
| `.step` | one numbered step; the number is a CSS counter, so steps renumber themselves when you reorder or insert |
| `.term` | a pull-out defining a technical word, placed where the word first bites |
| `.result` | a number the step exists to produce; `.big` inside it for the headline one |
| `.eq` | a display equation, with `<small>` for the line explaining it |
| `.row` / `.row.two` | a strip of 3 (or 2) figures |
| `.small` / `.tall` | a single figure narrowed and centred — 26em for a photo, 17em for a portrait frame |

Writing rules that came out of the first one:

- One step = one thing that happened. Either something physical done to the sample or the signal, or one operation on the numbers. If a step needs "and" in its title, it is two steps.
- Steps run in the order you did them, setup through to the answer. The reader is following a path, not consulting a reference — this is what makes it teachable and what separates it from the legacy format.
- Cut the meta. No "this report describes", no standalone Data or Method section describing where files live and what format they are in. Where that matters it belongs in the step that touches it.
- Write it as a recipe, not an essay. The target is reproducing the work, so no scene-setting, no motivation, no adjectives doing emotional work. The lede is instrument, data, result — three clauses.
- Define the word where it bites, in a `.term`, not in a glossary and not on first mention in the lede. A reader meets "seeing" at the step where seeing is the problem.
- Say what the thing is *for* before saying how it works — and name the use case, not the abstract function. This one took three passes. "LP is dual-band: two narrow windows at Hα and Hβ/OIII" is mechanism with no purpose. "LP is there to reject light pollution" is a function, still abstract, and leaves the reader assembling the point. "LP is a filter for photographing nebulae from a city, and was never meant to be pointed at a star" is the use case, and every fact after it lands as a consequence. Name the job, then explain the machinery.
- One pull-out, one idea. If a `.term` is defining something and also explaining what it costs you, it is two things: leave the definition in the pull-out and move the consequences to running prose beneath it. Watch the ordering when you split — prose that refers back to a number the pull-out establishes has to sit after it, not before.
- Every step earns a picture if one exists — setup photos, the raw frame, the plot. Show the artifact, not a description of it. `## ` heads group steps into phases without restarting the numbering.
- No captions. The prose around a figure carries it; a caption is a second, competing explanation and it drifts out of step with the text. If a picture needs explaining, explain it in the sentence above it.
- Stay at the physics level. No script names, no code blocks, no function signatures. These are educational pages, not publications, and the reader has not written the code and is not going to read it line by line — so a code block asks for trust it cannot earn and spends length that a picture or an explanation would use better. Say what was done and let the machinery be assumed. Length is the real constraint: every one of these pages is competing for attention against its own physics, and code is the first thing to cut. Where a step needs its method pinned down, give the numbers instead — the four Balmer wavelengths against their four measured pixel distances, as a table, say everything the Python list said and are readable by someone who has never seen Python.
- Pitch at Vivian's level, not at the writer's. She has the standard curriculum cold, and the Curriculum vertical next door is the test: if the material is in `curriculum/content/<subject>/`, she has it and explaining it is padding. Hydrogen energy levels and the Balmer ladder came out of the first report for exactly this reason. What earns space is what no curriculum covers — the instrument, this data, and the specific way a measurement can go wrong. The Bayer mosaic, the point spread function, a saturated core wrecking a centroid, a streak beating against the pixel grid: none of that is taught anywhere, and all of it is where the depth should go. The temptation to resist is writing for whoever is enjoying the page most, which is usually the author.
- The bar is the logic flowing without a gap, not reproducibility. A publishable report would have to ship its data and code so a stranger could check it; that is a different document and a later decision. Here the test is whether a reader can follow every step and see why each one had to happen. Anything that serves that stays, anything that only serves an auditor goes.
- Say what was done in the first person plural, not by naming the tool that did it. "We swept the width" rather than "`figure_extraction.py` swept the width". The work is ours either way, and the sentence reads better without the filename in the middle of it.
- Stop writing when the figure has made the point. A paragraph restating what the picture already shows reads as a lack of confidence in the picture. Say what the panels are, since there are no captions, and stop.
- Don't explain the repository. No GitHub paths, no folder structure, no "the raw data lives in". The scripts are assumed available; the reader is us.
- Put the answer in a `.result`, including intermediate answers. A step that produces a number should end in the number.
- Past tense, and headings as gerunds — "Threading the grating onto the objective lens", "We held it up to a laptop screen". The page records what was done, not what a reader should go and do. An imperative ("hold the grating up to a screen") reads as an instruction manual and quietly promises a completeness the page is not offering.
- No italics. Reach for them and the sentence is usually the problem; rebuild it so the important word lands on its own. Bold stays, but structurally only — the defined term at the head of a `.term`, and the numbers inside a `.result`.
- Never compare to an alternative you do not explain. "We threaded it onto the objective lens rather than behind it" raises a second method, says nothing about it, and leaves the reader wondering what they missed. Either explain the alternative because the choice mattered, or just say what was done. Every surviving "rather than" in a good page answers itself in the same sentence.
- Cut sentences that praise the step. "The check takes two minutes and settles whether the grating is the right way round" is the page telling you a step was worthwhile instead of telling you what happened. State the action and the outcome; the reader can judge.
- Two figures showing the same thing is one figure too many. The first draft carried both a residual panel and a standalone residual plot; they disagreed in the third decimal and clashed in styling, which is how the redundancy got noticed.
- Generated figures should share one visual theme. Plots made by older scripts arrive on a white background and read as foreign next to the rest.
- Keep text out of the figure. No figure title, no standfirst, no panel headings, no value labels on the points — all of that is prose, and prose is where it can be edited. Keep only what is part of the graph: axis labels, tick labels, and bare series identifiers where two curves would otherwise be indistinguishable. The plotting scripts enforce this — in `step_figures.py` the `head()` helper is a deliberate no-op and `dress()` ignores its `title` argument, so a call site can keep its wording as documentation without drawing it.
- Point with graphics, not words. To call out a feature, mark it — an `axvspan` over the 477 nm response step, a ring around the zero-order dot, a double-headed arrow across a width — and let the sentence beside the figure say what it means. Reclaim the top margin the removed header used to occupy or the figure floats in dead space.
- Size the figure to its job, centred. A multi-panel analysis plot earns full width; a single photo making a single point does not. `.small` (26em) for a standalone photo, `.tall` (17em) for a portrait frame. Both centre horizontally — a narrow figure flush left reads as a mistake.
