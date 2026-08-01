# TRANSFER — doc restructure, session handoff

**Temporary file.** A record of a design discussion (2026-07-31) that ran in a parallel Claude session while this one was doing astronomy night ops. Nothing here has been applied — the one build was reverted. **Delete this file once the restructure lands.**

**Why it was paused:** the two sessions were editing overlapping context and confusing each other. All the work below was reverted so night ops could proceed. Pick it up when the astronomy work is at a stable point.

---

## The question

How should operating procedure, findings, and ideation be stored across `science/` so that a session can resume work **without re-reading and re-analyzing everything from scratch** — i.e. an efficient way to summarize findings iteratively rather than starting at square one each time.

## What the survey found

Memory layers as they exist today, and how each reaches a session:

| Layer | Size | Loaded when |
|---|---|---|
| `~/.claude/CLAUDE.md` (global, outside this repo) | — | every session, every directory |
| `science/CLAUDE.md` | 397 ln / 50 KB | automatically, in science-repo sessions |
| `work/IDEAS.md` | **2,564 ln / 280 KB** | only if a session explicitly reads or greps it |
| `work/astronomy/output/setup/seestar_COMMANDS.md` | 330 ln | on demand |
| `work/astronomy/output/setup/seestar_VERIFY.md` | 120 ln | on demand |
| `work/physics/spike/spike_VERIFY.md` | 122 ln | on demand |
| `work/physics/problems/<n>/PLAN.md` × 17 | 37–186 ln each | on demand |
| `work/astronomy/output/setup/night_run.py` (`PLAN` block) | — | only if you know to look |

At survey time there was **no nested `CLAUDE.md` anywhere** — nothing under `work/` ever entered context automatically. `work/chemistry/` and `work/biology/` were empty (`.gitkeep` only).

> ⚠️ **All counts are a snapshot taken before commit `b5497bc`.** Re-measure before acting.

## The diagnosis

`work/IDEAS.md` grew **743 → 2,564 lines in two weeks** (2026-07-17 → 2026-07-31). Its own header states *"This doc does not track progress."* It does.

Breaking down **§6 Astronomy** (1,200 ln / 103 KB — most of that growth):

| Kind of content | Lines | Examples |
|---|---:|---|
| **Operating procedure** | ~294 | polar alignment, programmatic control, reduction rules, weather, dew |
| **Results** | ~629 | Photometry 185 · Astrometry 152 · Spectroscopy 274 |
| **Ideation** | ~238 | grounding, the reference ladder, the observing queue, publishing bar |

So the ideation doc is roughly **20% ideation**.

**Root cause: three different clocks sharing one file.** Procedure changes when a gotcha is found. Results append after every run. Ideation changes when direction changes. Mixed together, a session either eats ~70k tokens whole or greps a fragment with no way to tell what supersedes it. That is the "back to square one" feeling.

A parallel imbalance in `science/CLAUDE.md`: ~300 of its 397 lines are publishing/shipping mechanics (the wall, project pages, builds, the iOS app); ~30 lines (§ ANALYSIS & NOTEBOOKS) cover actually doing science in `work/`.

## Proposal A — split by clock (first pass, superseded in part)

Three files per science, each with a rule about *how it is written*:

1. **`work/<science>/CLAUDE.md`** — how we operate. ~150 ln, hard cap ~200. Auto-loads when a session touches that subtree. Sections: toolchain (venv, entry-point scripts) · where things go · invariants that were bugs first · read-first pointers · open loops. **Rewritten in place, never appended** — that is what keeps it bounded.
2. **`work/<science>/FINDINGS.md`** — what we found. A **rolling state-of-play header** (~30 ln, overwritten each time: current best numbers, what has been retracted) over an **append-only dated log**. The header is the anti-re-derivation device: 30 lines gives the current answer; the log is for "why did we do it that way."
3. **`work/IDEAS.md`** shrinks to what it claims to be — goals, grounding, backlogs, change log, the `overview.pdf` appendix. Est. 2,564 → ~900 ln.

Left alone: `physics/problems/<n>/PLAN.md` and the two `*_VERIFY.md` checklists — already correctly shaped and located.

## Proposal B — James's reframe (the one to build)

Organize the root doc around the repo's actual shape, not around the sciences.

**The repo has three content verticals. Make this unmissable at the top of `CLAUDE.md`:**

| Vertical | Source of truth | Generated | What it is |
|---|---|---|---|
| **Curriculum** | `web/public/curriculum/source/*.md` | `curriculum.json` | **Largely done** — stable reference tables, not an active front |
| **Olympiads** | `web/public/olympiads/olympiads.yml` | `olympiads.json` | **A journal** — tracks Vivian's contest progress |
| **Projects** | `web/public/projects/` + `gallery.yml` + `technology.yml`; WIP under `work/` | `gallery.json`, `technology.json` | **The frontier** — where the work happens |

**All three verticals are served by two surfaces, from the same generated JSON:** the Astro/Cloudflare web app and the SwiftUI iOS app (three tabs = three verticals). The Apple app belongs in the orientation *as a surface*, not as an appendix.

**Everything else currently in the root doc is Projects-specific and should move to `work/PROJECTS.md`.** Projects is where we live, but it is still one vertical of three and should not occupy ~75% of a doc meant to orient a session to the whole repo. `work/` is where the vertical is actually worked on, so that is where its manual belongs.

**Naming:** `PROJECTS.md`, not `CLAUDE.md` — it is a vertical name, and it leaves `work/<science>/CLAUDE.md` free for the per-science operating layer from Proposal A.

**Then:** review `IDEAS.md`, move its skeleton into `PROJECTS.md`, and delete it. Rationale — the ideas have gone stale; the program is in **iterative-execute mode** now, with a settled basic skeleton for each of the four sciences, not in ideation mode.

### Known cost, and the mitigation

`PROJECTS.md` does **not** auto-load the way a `CLAUDE.md` in the same directory would. Mitigate with a hard pointer block at the top of the root `CLAUDE.md`: *read `work/PROJECTS.md` before touching anything in the Projects vertical* — explicitly including `web/public/projects/`, `gallery.yml`, and `technology.yml`, which sit **outside** `work/` and would otherwise never trigger it.

## The section-move map (built once, verified, then reverted)

Result of the build: `CLAUDE.md` **397 → 155 ln**; `work/PROJECTS.md` 186 ln. Bytes went 50 KB → 52 KB, so essentially nothing was lost — the delta is the new orientation material. Content moved close to verbatim; these are hard-won decisions carrying 🔒 locks and ⚠️ warnings, and should not be paraphrased down.

**Stays in `science/CLAUDE.md`:**
- *(new)* THE THREE VERTICALS · THE TWO SURFACES · pointer block to `work/PROJECTS.md`
- STACK · REPO STRUCTURE
- CONTENT BUILDS & DEPLOY — restructured as a four-row table, one build per vertical
- VISIBILITY & SECURITY
- APPLE APP — whole. It is a *surface*, so splitting it by vertical would be worse than keeping it intact.
- The `/research/` → `/projects/` rename, **condensed to the `_redirects` contract only** — installed App Store builds still fetch `/research/…` and follow the 301s. That is deploy/compat plumbing, not vertical-specific.

**Moves to `work/PROJECTS.md`:**
- DATA MODEL — TECHNOLOGIES & TOYS (tech/toy vocabulary, access tiers, the 🔒 public-site lock, exact-name-match rule)
- PREPPING A RUN (incl. the physics leads generator)
- STAGING GALLERY CANDIDATES
- THE WALL (~105 ln — the largest single section)
- AUTHORING A RESEARCH PROJECT (+ the "project folders lost a path segment" half of the rename)
- ANALYSIS & NOTEBOOKS (astronomy venv, `night_run.py` rule, physics venv, reproducibility, chart palette, Jupyter conventions)

**`work/PROJECTS.md` opens with:** the three-stage pipeline `work/scratch/<topic>` (rough) → `work/<science>/` (organized WIP) → `web/public/projects/` (published), all git-tracked — the difference being polish and web-visibility, not whether it is in git. Then a related-docs line pointing at `IDEAS.md`, `work/astronomy/NIGHT.md`, the per-problem `PLAN.md` files, and the `*_VERIFY.md` checklists.

## Open items

- **`IDEAS.md` is the real work, and it is unfinished.** The ~629-line astronomy results block has no obvious home yet. It is neither orientation nor operating procedure, and it is exactly what "summarize our findings iteratively" was about. Proposal A's `FINDINGS.md` (rolling header + append-only log) is the candidate; the decision was never made.
- **Four references to `IDEAS.md` inside `PROJECTS.md` need rewriting when `IDEAS.md` is deleted:** the "update it continuously while brainstorming" rule · the 🔒 lock that routes capability detail there · the SPIKE Prime rationale pointer · the Albireo retraction citation (`§6, Albireo`).
- **`work/overview.pdf`'s source is the print template embedded in `IDEAS.md`'s final appendix** (~14 KB of HTML). It was deliberately put there in 2026-07-25 after a standalone `work/scratch/overview.html` drifted from the doc. Moving it back out re-opens that drift risk — decide consciously, do not let it ride along with the deletion.
- **`work/chemistry/` and `work/biology/` are empty.** Seed them from the same skeleton at the same time, so the first session that touches them does not invent its own layout.
- **Re-measure all line counts** before acting.

## Prior art in this repo — read it first

The astronomy session independently created **`work/astronomy/NIGHT.md`** (75 ln, committed in `b5497bc` as a "front door") after tonight's SW Lac run was nearly lost three separate ways, each failing while logging success. That is the Proposal-A per-science operating layer arriving on its own, under real pressure, without being designed.

**Read `NIGHT.md` before designing the `work/<science>/CLAUDE.md` layer.** It is evidence of the shape the work actually wants, and it should inform the template rather than be retrofitted to one.

## State when this was written

- `CLAUDE.md` and `work/IDEAS.md` are **clean at HEAD** — the trial build was fully reverted (`git diff HEAD` empty), and `work/PROJECTS.md` was deleted.
- The only working-tree changes belong to the astronomy session: `work/astronomy/horizon.yml`, `work/astronomy/output/setup/seestar_COMMANDS.md`, three `output/photometry/2026073*/` folders, four `night_2026073*.log` files.
- Nothing in `work/astronomy/` was touched by the doc-restructure session at any point.
