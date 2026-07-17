# Research — ideation & progress

The living doc for the whole research program. Two jobs in one file:

1. **Ideation** — the idea backlog (below), organized by science, each with a status.
   Public on purpose: we target underserved areas and don't care about being scooped.
2. **Progress tracking** — the **Active work & progress** dashboard (next section) is
   the at-a-glance "where are we"; in-flight fronts keep their own detail sections
   (e.g. the home molecular-biology lab). Ideas graduate to
   `public/research/projects/YYYYMMDD Name/index.md` when a pilot starts and get
   published from there.

Keep this doc current as work moves — bump an idea's `Status`, update a front's line
in the dashboard, and log structural changes in the change log at the bottom.

_Last updated 2026-07-16 — reframed home-lab-first (SIL access retired): **Math + Computing** are the tool layer; **Physics · Chemistry · Biology · Astronomy** are the four research sciences._

---

## Active work & progress

At-a-glance status of live fronts. Thin index — details live in each front's own
section or project folder. Update these lines as work moves.

**Piloting / active**
- **Home molecular-biology lab** — ✅ **endpoint kit-set audit complete (S0–S5)**: every
  instrument verified, consumables accounted for, workflows understood; bench is
  Vivian-ready. First real-PCR kits (PTC Taster + 16S Barcoding) ordered. → *Home
  molecular-biology lab* section below.

**On deck (next up)**
- **Vivian's hands-on runs** — work the 5 endpoint labs in order (Microliter Madness →
  Cat Genetics → Glow Lab → Forensics → BioBits before ~Nov 2026).
- **PTC first-PCR run** — once the kits land (freezer; P200 gravimetric check first).
- **DNA barcoding of local biota** — flagship molecular-bio project + the **Biology activation
  vehicle** (→ BOLD/iBOL submission, science fair); promote to a project folder after the PTC
  training-wheels run succeeds.
- **IYPT 2027 physics** — prototype 2–3 of the 17 problems best matched to our sensors
  (Disc spectrometer · Cold drink · Magnetic carousel · Snail ball); theory + experiment.
- **Astronomy first light** — ZWO Seestar S30 Pro shakedown
  (imaging → photometry → astrometry; a grating for spectroscopy is a later acquire) →
  then join an **AAVSO photometry campaign** (the Astronomy activation vehicle).

**Completed & published** (in `public/research/projects/`)
- IR Spectroscopy · UV-Vis Spectroscopy · Four Point Probe. *(SIL-era; kept as
  historical past-work — those university instruments are no longer accessible.)*

**Backlog** — home-lab-runnable ideas across the four research sciences (Physics ·
Chemistry · Biology · Astronomy), with **Math + Computing as the cross-cutting tool
layer**; see **Idea backlog** below.

## Goals

- **Four research sciences, two tool sciences.** **Physics, Chemistry, Biology, Astronomy** are the standalone research targets — each should carry at least one live home-lab project. **Mathematics + Computing** are the *foundational tool layer* (modeling, statistics, ML, simulation, signal processing) applied *across* the four, not pursued as standalone research.
- **Home-lab-first.** As of the July 2026 Vancouver move, UNR SIL walk-up instrument access is retired. Every new idea must run on **toys we own and operate at home** — the miniPCR molecular-bio bench, the ZWO Seestar telescope, cameras + sensors, a soldering/scope/3D-print bench, and kitchen-scale wet chemistry. (The three completed SIL-instrument projects stay on the site as historical past-work.)
- **Publish.** At least one JEI-level paper per year, a *Journal of Chemical Education*-level paper, and one submission into a real peer-reviewed adult venue (mentor co-author). Physics also competes at **IYPT** (see Physics backlog).
- **Push the owned-toy advantage.** Where we own an instrument other high-schoolers don't (the PCR bench, the Seestar), the project should use it as its *primary* readout — not incidental confirmation.
- **Target underserved areas.** Local-biota barcoding, household-materials science with home readouts, quantitative pedagogy, cross-science combinations. Avoid re-running saturated studies.
- **Fold in machine learning where it fits** — sequence bioinformatics, spectral/image classification, video pose-tracking, kinetics fitting. Don't force ML where a linear fit answers the question.
- **Use curriculum knowledge.** Draw on what we've studied (AP-level math through calculus; stats + inference; ML methods/algorithms; full AP chem + organic; AP-level physics incl. modern; AP-level bio incl. genetics, ecology, neuroscience; Olympiad-level astronomy).
- **Activation vehicles + external gates.** Each research science should have a recurring *project generator* that exercises an owned instrument and feeds real external gates — see the next section. IYPT is that vehicle for Physics; the others are named below.

## Activation vehicles & external gates

The program runs on one move: **build a home-lab research project, then submit it to every external gate it fits.** The project is the asset; the contests/venues are just distribution. Physics proved the template — one **IYPT** investigation can feed CaYPT, a science fair, and a mentored-research submission from a single build. Each science gets its own *activation vehicle*: a recurring source of open-ended projects tied to an owned toy. **Deprioritize team-debate formats** (IYPT/IYNT-style Science Fights) — favour individual research-project vehicles and pro-am campaigns. (Exam Olympiads are a separate track — see the olympiads registry.)

### Per-science vehicle (verified 2026-07-16)

| Science | Activation vehicle | Activates | Recurring project stream |
|---|---|---|---|
| Physics | **IYPT 2027** — the 17-problem set | Vernier sensors · Digilent · 3D printer · camera | pick a problem → paired theory + experiment (table below) |
| Biology | **DNA barcoding → BOLD / iBOL** | the miniPCR bench, end-to-end | barcode local Vancouver biota → submit records with student attribution |
| Astronomy | **AAVSO photometry campaigns** (+ NASA Exoplanet Watch for compute) | Seestar S30 — **photometry only** (no spectrograph) | join a live campaign → submit light curves to the AAVSO database |
| Chemistry | **no dedicated vehicle exists** — PalmSens 6-experiment on-ramp → self-directed projects | PalmSens potentiostat · UV-Vis · polarimeter | CV / stripping voltammetry / UV-Vis kinetics from science-fair · RSC · ACS banks |

**Honest gaps (from the 2026-07-16 deep search):**
- **Chemistry has no BOLD/AAVSO analogue** — no curated open-ended citizen-science chemistry campaign activates the home instruments. Closest is PalmSens's six structured experiments (Cu/Ni deposition · Cottrell diffusion · cyclic voltammetry · heavy-metal stripping voltammetry · glucose-oxidase biosensor · Prussian-Blue H₂O₂) — a guided *curriculum* for the potentiostat, not a problem generator. So chemistry's real vehicle is **the science fair + a journal**, and projects are self-sourced.
- **Astronomy — the 30 mm Seestar is small.** It joins **photometry** campaigns only. NASA Exoplanet Watch personal transit observing wants ≥4″/100 mm, so use it as a compute/archival path (robotic-telescope data + free EXOTIC software), not scope activation. IASC analyses *provided* survey images — a compute vehicle, not scope activation.
- **Biology — barcoding is the cleanest 1:1 fit** to the bench (high-schoolers hit expert-level ID accuracy in the literature). CSHL's DNA Learning Center (dnabarcoding101.org) is a good protocol bank, but its named campaigns (Urban Barcode, Barcode Long Island) are NYC-geo-restricted — the open, enterable layer for a BC student is **BOLD/iBOL itself** (local-biota barcoding). Novel-species results are *possible, not guaranteed*.

### External gates — the distribution list

Individual, non-debate; one project can feed several. Personal-eligibility specifics are tracked privately, not in this public doc.

| Gate | What it is | Canada / homeschool | Status |
|---|---|---|---|
| **Greater Vancouver Regional Science Fair (GVRSF)** → CWSF → Team Canada-ISEF | project fair, grades 7–12 | ✅ homeschool-eligible (BC 1701 status or birth-year; parent/educator signature substitutes; contact the committee chair to register) | **confirmed** |
| **AAVSO / BOLD submissions** | the pro-am campaigns above *are* gates — records & light curves land with attribution | ✅ open worldwide | via the vehicles |
| **JEI + high-school journals** | mentor-submitted publication (see venue cheatsheet) | open to international — verify | endpoint for any project |
| **Sanofi Biogenius Canada** | mentored biotech research competition, regional → national → international | grades 9–12, Canada — homeschool TBD | unverified |
| **MIT THINK Scholars** | proposal-stage project funding + mentorship | ⚠️ may require US enrollment/residence | **unresolved — key unknown** |
| **Davidson Fellows** | scholarship, US citizen/PR under 18 | ⚠️ Canadian residence may disqualify | **unresolved — key unknown** |

**Open verification items:** MIT THINK + Davidson eligibility for a Canada-resident dual-citizen (both unresolved by the search); Sanofi Biogenius Canada / JEI / Regeneron-ISEF-international specifics; whether any chemistry citizen-science data endpoint exists to mimic the BOLD/AAVSO submission loop (likely none).

## Selection criteria (applied to every idea)

An idea earns a project slot when it checks most of these:

1. **Owned-toy advantage** — runs on an instrument we own and operate at home (see the Home-lab inventory), not one we'd have to travel for.
2. **Underserved** — literature search shows a clear gap (local samples, home readouts, cross-science), not yet saturated.
3. **Curriculum fit** — connects to something we've already studied, so the analysis isn't a black box.
4. **Cross-discipline leverage** — ideally spans a research science + the Math/Computing tool layer, or two owned toys.
5. **Publishable / competition shape** — a clear hypothesis, a well-defined sample set, a figure set we can picture before starting (or an IYPT theory+experiment pairing).
6. **ML-ready (when applicable)** — the data shape supports classification, regression, clustering, or a fit we can learn from.

## Resources — the home-lab inventory

The real owned toys, from each tech page's `toys:` frontmatter (the source of truth), mapped to the site's science → tech structure. **Truly lost with SIL:** mid-IR structural ID (FT-IR), circular dichroism, NIR/integrating-sphere, mass spec (MALDI, LC-MS, GC-MS), chromatography, TGA/DSC, four-point probe. **Retained at home:** UV-Vis + fluorescence, polarimetry, full electrochemistry, thermal, mechanics, spectra, microscopy, physiology, genomics, telescope + archives.

### Chemistry
- **Spectroscopy** — **Vernier Go Direct Fluorescence UV-VIS Spectrophotometer** (absorbance + fluorescence) · **Vernier Go Direct Polarimeter** (optical rotation)
- **Electrochemistry** — **PalmSens EmStat Pico** (a real potentiostat — CV / LSV / amperometry) · **Vernier pH** · **Vernier Conductivity**
- **Thermal** — **Vernier Temperature Probe** · plus kitchen wet-lab (buffering, extraction, cooking-as-chemistry)

### Physics
- **Mechanics** — **Vernier Force & Acceleration · Motion Detector · Photogate** + phone video / pose tracking
- **Thermodynamics / fluids** — **Vernier Gas Pressure · Turbidity** (+ Temperature)
- **Electromagnetism** — **Vernier UV-VIS + optical fiber** (emission spectra) · **Vernier 3-Axis Magnetic Field Sensor**
- **Engineering** — **Digilent Analog Discovery 3** (scope + AWG + logic analyzer) · **TOAUTO DS90 soldering** · **Prusa CORE One+** 3D printer · microphone + FFT

### Biology
- **Genomics** — **miniPCR mini16** thermal cycler · **GELATO** electrophoresis + blue-LED viewer · **2× P51** · pipettes + balance (full bench log below)
- **Microscopes** — **Dino-Lite AF4515T-FUW** digital · **AmScope SM-4TZ-144** stereo · **Swift SW380T** compound
- **Physiology** — **Vernier Go Direct EKG · Spirometer · O₂+CO₂ gas sensor**

### Astronomy
- **Telescopes** — **ZWO Seestar S30 Pro (tilting wedge)** · UBC Thunderbird South (remote partner)
- **Data archives** — Gaia · AAVSO · MAST · Transient Name Server · WISeREP · Galaxy Zoo · Pickles Stellar Atlas

### Math + Computing — the tool layer
- NumPy · SciPy · Wolfram · Matplotlib · LaTeX · Jupyter · GitHub · Docker · Zenodo

### Pre-order priorities (cross-discipline bench bottlenecks, ~$1,000–1,500)
- Analytical balance (0.1 mg) · microcentrifuge · vortex mixer · hot plate / magnetic stirrer. *(Dad's lab covers cold storage / incubation / laminar flow.)*

### Curriculum strengths (what we can *analyze*, not just measure)

- **Mathematics** — through calculus incl. vectors, differentials, fields, approximation.
- **Computing** — stats (distributions, inference, significance testing), algorithms, **Learning (Methods + Algorithms)** → ML foundation for classification / regression / clustering.
- **Physics** — mechanics, harmonics, E&M, thermodynamics, optics, modern.
- **Chemistry** — full AP + organic (incl. Spectroscopy module) + inorganic.
- **Biology** — cells, genetics (Mendel, non-Mendel, expression, regulation, mutation), ecology, plants, animals, neuroscience.
- **Astronomy** — Olympiad-level incl. observations, coordinates, mechanics, solar system, stars, cosmology.

### Highest-leverage combinations (research science × tool layer)

- **PCR bench + bioinformatics (Computing)** → local-biota barcoding: wet lab produces sequences, ML/alignment turns them into IDs. The pipeline is the result.
- **Seestar + image analysis (Computing)** → photometry light curves + astrometry, cross-matched against Gaia / AAVSO.
- **Camera / sensors + Math/Computing** → pose-tracking kinematics + ODE/Bayesian fits for the IYPT mechanics problems (Snail ball, Y-pendulum, Falling book cover).
- **Vernier UV-VIS/potentiostat + Math** → kinetics / voltammetry / thermochem time-series with proper uncertainty + model comparison.

## Home molecular-biology lab — bench reference & progress

Operational reference for the Vancouver home molecular-biology bench: the miniPCR
kit set, the gear that runs it, and the hard-won procedure notes. Forward-looking
ideas (PCR expansion path, DNA barcoding) are in **Future topic structure → Biology**
and the **Biology idea backlog** below.

Started as a multi-session shakedown (July 2026): run every kit once, hands-on, to
learn what each instrument does. James audits gear + workflow; **Vivian does the
actual hands-on labs.**

### The kit set and lab order

The @home kits we own are **endpoint labs** (dye, melting, electrophoresis) — none
uses PCR amplification except the Glow Lab, which uses the thermal cycler only as a
96 °C heat source. Ordered so **visible-failure labs come before silent-failure
labs**, and so the earliest-expiring reagent (BioBits) isn't stranded.

| # | Lab | Cat # | Teaches | Instruments | Pipette |
|---|-----|-------|---------|-------------|---------|
| 0 | Calibration & shakedown | — | metrology — prove the instruments are honest | scale, all pipettes, miniPCR (dry) | all |
| 1 | Microliter Madness | KT-1101-01 | the micropipetting skill that gates every lab | none | P20 |
| 2 | Cat Genetics (dye electrophoresis) | KT-1402-01 | gel mechanics, zero silent-failure risk | GELATO | P20 |
| 3 | DNA Glow Lab | KT-1900-01 | DNA melting temperature (the physics behind PCR's 95 °C step) | miniPCR + P51 | P20, P200 |
| 4 | Forensics: Wrongfully Convicted? | KT-1504-01 | first run combining real DNA + gel + staining | GELATO | P20 |
| 5 | BioBits: Central Dogma | KT-1102-01 / reagents KT-1910-02 | cell-free transcription & translation, live | none (37 °C body heat) | its own 4 µl minipette |

**Why this order:** molecular biology fails invisibly — a mispipetted reaction gives a
blank gel with no clue why. The dye labs (1, 2) announce every mistake, so you build
pipetting and electrophoresis in isolation before combining them with real DNA (3, 4).
BioBits (5) floats — no instrument, no purchase — but has only **two reactions' worth
of reagent** and expires ~early Nov 2026, so don't leave it past October.

### Per-lab notes

**S1 Microliter Madness** — reusable practice card + blue/yellow/red dyes (5 ml ea) +
200 µl tips + guide. No pipette included; use the P20. Drills **2 µl and 5 µl** —
harder than 20 µl and exactly the range the real labs need (BioBits/Glow Lab dispense
4 µl). *Habit:* always use the smallest pipette whose range contains the volume.

**S2 Cat Genetics** — colored dyes, no DNA. Melt a SeeGreen tab → pour gel → seat comb
→ load → run → view under the amber lid. Reagents for 8 groups (botch-tolerant).
**SeeGreen All-in-One tabs** = agarose + stain + TBE in one; store dark (photobleach).
Distilled water for gels + diluting TBE (tap-water ions → hot gel → smeared bands).

**S3 DNA Glow Lab** — the best lab, and the only one using the thermal cycler. Samples:
AT-rich, GC-rich, 50:50, unknown. A dye fluoresces only bound to *double-stranded* DNA;
heat the samples and the glow dies as the duplex denatures. GC-rich holds its glow to
higher T (G:C = 3 H-bonds vs A:T = 2). The miniPCR steps through known temperatures so
you read a **Tm number**; the P51 reads fluorescence. Follow-ons: 100 mM NaOH denatures
by pH without heat; estimate the unknown's concentration from brightness.
- Volumes: 4 µl DNA (P20); 40–65 µl samples + NaOH (P200); Buffer 1/2 at 275/255 µl
  exceed the P200 ceiling → aliquot 135 µl twice.
- **TIMING TRAP:** once diluted into Buffer 1, dye fluorescence holds only ~2 h at RT.
  Dilute immediately before use, never the night before. (Diluted dye keeps ~72 h cold+dark.)
- Concentrated dye is DMSO-based, **freezes at 4 °C** — may arrive solid; warm in a
  fist. Keep foil-wrapped (photobleaches). **Bundle miniPCR + P51 + 0.2 ml strips.**

**S4 Forensics** — first run with real DNA + gel + staining. Ships pre-made DNA
(Victim, J.M., Evidence 1/2 + Fast DNA Ladder 1); no PCR. 12 µl loads → **use the P20,
never the P200** (12 µl is 6% of P200 full scale, invisible double-digit error). Gloves
+ eyewear. Guide names GelGreen tabs; our SeeGreen tabs should substitute — **confirm.**

**S5 BioBits** — four tubes: negative control (water), DNA A, DNA A + kanamycin, DNA B.
Green = transcription, red = translation; kanamycin blocks the ribosome. **Read the
prediction table with Vivian before opening anything** — the prediction IS the pedagogy.
Only two reactions' worth; do it after Microliter Madness so the 4 µl-pellet mistakes
are burned on a practice card first. Ships its own P51 + 4 µl minipette. Incubate 37 °C
(fist/pocket) 15 min → RT overnight; read 8–72 h.

### Session 0 — calibration procedure (metrology)

Prove every instrument is honest before trusting it; the measurement chain has to
bottom out on a traceable standard.

- **0a Scale** (THINKSCALE 50 g × 0.001 g): battery in, solid surface away from airflow,
  warm up, **run the CAL routine against the 50 g weight** (placing the weight in weigh
  mode does NOT recalibrate). Re-weigh → 50.000. *After a good cal the same weight reads
  nominal by construction — the real test is whether a third mass reads true (0c).*
- **0b Gilsons:** cycle each plunger 20–30× full travel; grit/sticky return = dry O-ring
  (cheap Gilson seal kit).
- **0c Gravimetric check (the real test):** **weigh-by-difference, NOT a standing tare** —
  record empty tube `m0`, dispense **10×**, record `m1`, water = `m1 − m0`. Ten dispenses
  because one 20 µl shot = 20 mg and 1 mg readability is 5% quantization. *Why not a tare:
  a cheap milligram scale drifts over the ~2 min of dispensing (a first attempt read an
  impossible 52 µl/shot from pure tare drift).* Targets: P20→200 mg, P200→1000 mg,
  P1000→10 000 mg (±1%). Reads accuracy, not scatter; a known bias is usable.
- **Pipetting technique:** **first stop to fill, both stops to empty.** Press only to the
  first (soft) stop before drawing up — going to the hard stop first over-draws.
- **0d miniPCR dry-run:** run the built-in Quality control protocol empty. It heats the
  **lid first** (~105 °C, anti-condensation) before the block ramps ~18→95 °C in <1 min.
  Confirms heaters healthy + teaches the app. Full QC run ~3.7 h (burn-in); stop early.

### Gear

**Pipettes** — store hanging **tip-down** (liquid drains off the piston seal):

| Pipette | Range | Source | Status |
|---|---|---|---|
| P20 | 2–20 µl | ONiLAB | new, ISO 8655 cert. Ships with stand, hex adjustment/ejector wrench (**keep — recalibration tool**), color ID clips, 200 µl tips |
| P200 | 20–200 µl | Gilson Pipetman Classic (yellow) | cal due 2012-05; feels good; **gravimetric-verify before first real use (Glow Lab)** |
| P1000 | 100–1000 µl | Gilson Pipetman Classic (blue) | cal due 2012-05; feels good; verify when first needed |

**Consumables** — new fresh sterile: 2–200 µl tips (P20/P200), 1.5 mL microtubes, 8-strip
0.2 ml PCR tubes (thermal-cycler samples). Legacy (fine for endpoint/water only): Zap +
blue 1000 µl tips (P1000), one bag Sarstedt 2 ml screw tubes (leak-proof storage).
⚠️ **Real PCR needs fresh plastic** (fresh filter tips + 0.2 ml tubes) — one stray
molecule becomes a billion.

**Instruments** — **miniPCR mini16X** (full programmable thermal cycler, BLE+USB, miniPCR
v3.0 app; Glow Lab uses it as a heat source but it's PCR-capable for the expansion path).
**GELATO** electrophoresis + integrated blue-LED transilluminator (**standalone, no app**:
PSU 50–135 V, on-unit voltage+timer, amber viewing lid, phone doc-hood). **Two P51**
fluorescence viewers (one for Glow Lab, one ships in BioBits). *Physics:* GELATO
transilluminator and P51 use the same principle — blue-LED excitation + amber filter
exploiting the **Stokes shift** (blue in → green out); dsDNA-binding dye fluoresces only
when intercalated. Safe blue light, not UV.

### Cold chain

Label bins so nobody tosses reagents (a shared family freezer is the biggest risk).

| Where | What | Lot | Deadline |
|---|---|---|---|
| Freezer −20 °C | BioBits Central Dogma (KT-1910-02) | BBT-251120 | ~early Nov 2026 |
| Freezer −20 °C | Forensics (KT-1504-01) | EF-251110 | ~May 2027 |
| Freezer −20 °C | PTC Taster Lab (KT-1004-03) | — | 12 mo from receipt |
| Freezer −20 °C | 16S Barcoding (KT-1015-01) | — | 12 mo from receipt |
| Fridge 4 °C | Glow Lab dye + DNA samples + buffers | GLO-2512 | — |

Room-temp-but-dark: SeeGreen tabs, any diluted dye.

### Standing gotchas

- **Label the two power bricks:** big = GELATO, small = miniPCR (different voltages).
- **Antifog spray lives with the GELATO** (transilluminator lid fogs over a warm gel).
- Distilled water for gels + buffer; tap water fine for pipette calibration (soft Vancouver water).
- **Buy PTC taste paper separately** for the PTC lab (Bartovation Super Taster kit,
  amazon.ca) — it's the phenotype half, not in the kit. Only PTC + Control pair with the
  TAS2R38 genotyping; Na Benzoate + Thiourea are bonus taste-genetics.

### Current status (as of 2026-07-11)

- **S0 Calibration** ✅ complete — scale traceable (50.000), both Gilsons feel good
  (gravimetric deferred to point-of-use), P20 technique learned, miniPCR ramp healthy.
- **S1 Microliter Madness** ✅ audited — gear present, workflow understood, put away for Vivian.
- **S2 Cat Genetics** ✅ GELATO gear audit complete (2026-07-11). Full kit confirmed
  against the User's Guide: console + light-filtering buffer chamber + blue-filter
  cover, casting platform + gel trays (2 small 60×60 + 2 large 120×60), double-sided
  combs (25/13 + 13/9 teeth), gel-cutting/band-excision tray, Fold-a-View photo hood
  (the folded blue slab), ClearView anti-fog spray, microfiber cloth. **Verify: unfold
  the Fold-a-View to confirm; locate DNA visualization goggles (may be missing — minor,
  amber cover filters the light) + the other 2 combs (store under the platform).**
- **S3 DNA Glow Lab** ✅ audited — all gear present & located (buffers were in the fridge bag).
  Queued for the real run: P200 gravimetric check first; dilute dye <2 h before use; warm DMSO dye if frozen.
- **S4 Forensics** ✅ hardware audited (2026-07-11) — same GELATO gel gear as S2, all
  present. **SeeGreen-vs-GelGreen open item CLOSED:** the GELATO guide lists both as
  compatible dyes, so our SeeGreen All-in-One tabs substitute for the guide's GelGreen.
  Remaining for the real run: thaw the frozen pre-made DNA (Victim/J.M./Evidence 1-2 +
  ladder); 12 µl loads → P20 not P200; gloves + eyewear.
- **S5 BioBits** ✅ audited (2026-07-11) — fully self-contained: freeze-dried reagents
  (freezer, KT-1910-02, exp ~early Nov 2026), DNA templates, its **own P51** (why we own
  two), its **own 4 µl minipette**, guide. No shared instrument. Cell-free central dogma
  in a tube: green = transcription (RNA), red = translation (protein), kanamycin blocks
  the ribosome. **Read the prediction table with Vivian before opening — the prediction
  IS the pedagogy.** Only 2 reactions' worth of reagent; run after Microliter Madness.
- **★ ENDPOINT KIT-SET AUDIT COMPLETE (2026-07-11)** — all of S0–S5 swept: every
  instrument verified, all consumables accounted for, every workflow understood. The
  bench is Vivian-ready. Next phase is the actual hands-on runs (Vivian) + the real-PCR
  expansion once the ordered kits land.
- **First real-PCR kits ordered** (PTC Taster KT-1004-03 + 16S Barcoding KT-1015-01) →
  −20 °C freezer on arrival, 12-mo shelf life. Gear confirmed compatible. See the
  **molecular-bio expansion path** (Future topic structure → Biology).

**Open items:** ~~SeeGreen↔GelGreen (Forensics)~~ CLOSED · ~~eyeball GELATO casting gear~~
DONE · get a distilled-water jug (gels + ~350 mL running buffer) · confirm Fold-a-View
unfolds + locate DNA visualization goggles + the other 2 combs · second/third pipette
stand (need three hangers) · identify the ~15 dropper bottles (probably microscopy stains
→ microscope, not DNA work) · ZWO Seestar S30 accessory kit turned up in lab boxes →
belongs with the telescope · **S5 BioBits audit** (last one, needs no instrument).

## Idea backlog

Reorganized around the home lab (July 2026). **Mathematics + Computing are the foundational tool layer** — methods applied *across* the four research sciences, not standalone projects. **Physics · Chemistry · Biology · Astronomy** are the standalone research targets, each anchored to owned toys. All SIL-instrument ideas were removed (see change log). Status key at the bottom.

### 🔧 Foundational tool layer

Not standalone projects — the modeling/analysis muscle every project below leans on. Each science project names which of these it exercises.

**Mathematics — the modeling & analysis toolkit**
- **Curve fitting + uncertainty propagation** — least-squares, error bars, CIs; the backbone of every dataset.
- **Fourier / signal processing** — audio FFT (standing waves), image transforms.
- **Differential-equation models** — damped/driven oscillators, rolling/rocking dynamics (Snail ball, Falling book cover), reaction kinetics, diffusion.
- **Bayesian inference + model comparison** — posteriors on rate constants / damping; BIC/AIC between competing models. Pairs with any time-series.
- **Numerical simulation** — ODE / finite-element solvers to compare theory against measurement (IYPT wants both).

**Computing — the computational & ML toolkit**
- **Video pose / motion tracking** — extract kinematics from phone video (pendulum, rocking statue, rolling wheel).
- **Audio analysis** — FFT/spectrogram pipelines for standing-wave frequencies.
- **Sequence bioinformatics** — the barcoding pipeline (QC → align → BLAST/BOLD → phylogeny); the pipeline *is* the result.
- **Image analysis** — Seestar photometry/astrometry reduction; RGB colorimetry from photos.
- **Public-data ML** — CNN stellar classification on SDSS/LAMOST 1-D spectra.

### 🔬 Physics — anchored on IYPT 2027

The **International Young Physicists' Tournament** — 17 open-ended research problems (40th IYPT, approved by the IOC July 2026). Each needs a paired **theory model + controlled experiment**. Nearly all are home-scale with our Vernier sensors + phone camera + Digilent scope + 3D printer + kitchen. Pick 2–3 to prototype; **★ = strongest fit to a specific owned instrument.**

| # | IYPT 2027 problem | Home setup (owned toys) |
|---|---|---|
| 1 | Pinhole sunglasses | pinhole-array film + camera + light meter — optics / myopia correction |
| 2 ★ | **Disc spectrometer** | CD/Blu-ray reflection grating + camera → build a spectrometer; cross-check vs. the Vernier UV-VIS |
| 3 ★ | **Snail ball** | 3D-printed hollow sphere + viscous fluid + ball; Motion Detector / Photogate / video on an incline |
| 4 ★ | **Singing capacitor** | ceramic caps driven by the Digilent AWG; microphone + FFT |
| 5 ★ | **Y-shaped (Bowditch) pendulum** | build the Y-string rig; video pose-tracking → Lissajous patterns |
| 6 | Seeing sound | rubber membrane + loudspeaker (Digilent AWG) + laser/camera (Chladni-like patterns) |
| 7 | Sinking funnel | funnel in a water column; Force sensor + video (damped oscillations) |
| 8 | Upward-driven disc | disc sandwiched between two wheels; video tracking |
| 9 | Photographic bokeh | slit in front of the camera lens; image analysis of anisotropic blur |
| 10 ★ | **Air vortex** | magnetic stirrer + liquid; camera (air-channel formation vs. speed) |
| 11 | Sound isolation | small door-gap openings; mic + Digilent + speaker (transmission vs. geometry) |
| 12 | Dotted-line trick | chalk on a board; Force sensor + high-speed video (periodic stick-slip dots) |
| 13 | Vortex pendulum | cylindrical bob in a flow channel; video (vortex-induced oscillation) |
| 14 ★ | **Non-Newtonian worms** | cornflour suspension on a speaker cone; camera (kitchen + vibration) |
| 15 ★ | **Cold drink** | ice + salt + alcohol; **Vernier Temperature** (cooling rate / lowest temp) |
| 16 ★ | **Magnetic carousel** | neodymium magnets on a 3D-printed disc + steel ball; **Vernier 3-Axis Magnetic Field Sensor** + video |
| 17 | Falling book cover | book-cover release; video pose-tracking (rigid-body dynamics) |

Top starters by owned-toy advantage: **2 Disc spectrometer** (spectroscopy), **4 Singing capacitor** + **16 Magnetic carousel** (electronics + magnetics), **15 Cold drink** (Vernier temp), **3 Snail ball** + **5 Y-pendulum** (clean mechanics via motion sensors).

**Non-tournament home ideas:** damped pendulum as a Bayesian inverse problem (pose-tracking + Bayesian fit); sky-light Rayleigh polarization map (polarizer + camera).

### 🧪 Chemistry — spectroscopy + electrochemistry + thermal (all home)

Not gutted — UV-Vis/fluorescence, polarimetry, a real potentiostat, pH/conductivity, and temperature all run at home. (Only FT-IR structural ID, CD, NIR, mass-spec, and chromatography left with SIL.) Maps to the site's **Spectroscopy · Electrochemistry · Thermal** techs. **No dedicated activation vehicle exists** (no BOLD/AAVSO analogue for chemistry) — use the PalmSens six-experiment set as a potentiostat on-ramp, then self-source projects below; the gate is the **science fair + a journal** (see Activation vehicles above).

**Spectroscopy — Vernier UV-VIS/fluorescence + Polarimeter:**
- **Anthocyanin pH ladder across household products** — quantitative λmax/absorbance shifts vs. pH; underserved at realistic product diversity. `raw` · JEI / J. Chem. Educ. · ML: cluster in λmax×pH space.
- **Fruit-ripening pigment kinetics** (banana/tomato/blueberry) — chlorophyll + carotenoid + anthocyanin absorbance/fluorescence time-series; NMF spectral unmixing. `raw`
- **Catalase / enzyme kinetics** — potato/liver H₂O₂ by absorbance (or Vernier O₂); Michaelis–Menten. `raw`
- **Tea oxidation & Maillard browning kinetics** — real-time absorbance; first-order fits across substrates/methods. `raw`
- **Fluorescence quenching (quinine / riboflavin / chlorophyll)** — Stern–Volmer on the fluorescence channel; a capability most HS labs lack. `raw`
- **Optical rotation of sugars / chiral extracts** (Polarimeter) — specific rotation, glucose mutarotation kinetics. `raw` — polarimeter toy-advantage.

**Electrochemistry — PalmSens EmStat Pico potentiostat + pH/conductivity:**
- **Cyclic voltammetry of household redox couples** (vitamin C, ferro/ferricyanide, dopamine-in-banana) — real CV at HS level is rare and impressive. `raw` · anchors the **Electrochemistry** tech · ML: peak-feature classification.
- **Electrosynthesis / electroplating** — water splitting, Cu plating from CuSO₄; charge vs. mass yield (Faraday's laws). `raw` · anchors the planned **Transform** topic.
- **Conductometric / potentiometric titrations** — Vernier conductivity + pH; equivalence-point + kinetics. `raw`

**Thermal — Vernier Temperature:**
- **Melting point / freezing-point depression / calorimetry** — thermal transitions, colligative properties, reaction ΔH. `raw`

### 🧬 Biology — the home-lab flagship (genomics · microscopy · physiology)

Three owned tech stacks; biology carries the program near-term. **Activation vehicle: DNA barcoding → BOLD/iBOL** — the recurring project stream that maps 1:1 onto the miniPCR bench (see Activation vehicles above).

**Genomics — miniPCR + GELATO + P51:**
- **DNA barcoding of local Vancouver biota (COI / rbcL / matK / ITS)** — extract → amplify → gel → mail-in Sanger → BLAST/BOLD. Each specimen is new data; genuinely novel JEI shape + BOLD submissions; wet-lab × bioinformatics. **Flagship — promote to a project folder after the PTC training run.** `raw`
- **Human genotype→phenotype family panel (PTC TAS2R38, PV92 Alu, lactase MCM6)** — Hardy-Weinberg + allele-frequency stats. `raw` · Biochem. Mol. Biol. Educ.
- **Endpoint kit runs** (Microliter Madness → … → BioBits) — pedagogical, in progress; see the bench log. `piloting`

**Microscopy — Dino-Lite digital + AmScope stereo + Swift compound:**
- **Quantitative cell/tissue morphometry** — onion/cheek cells, pond microfauna, pollen, stress-treated plant stomata; image-analysis pipeline (Computing crossover). `raw`
- **Micro-materials & surfaces** (Dino-Lite digital) — textile fibers, microplastics, print/coating surfaces; recovers the "what material is this" angle *morphologically* (lost the FT-IR chemical version). `raw`

**Physiology — Vernier EKG + spirometer + O₂/CO₂:**
- **EKG / heart-rate variability under interventions** (exercise, breathing, caffeine) — ECG signal processing. `raw`
- **Spirometry + respiratory-gas exchange** — lung volumes + O₂/CO₂ across activity; quantitative human physiology. `raw`

**Grow (parked until toys/project commit):** Drosophila genetics (~$100 Carolina), yeast fermentation / microbiology.

### 🔭 Astronomy — Seestar imaging/photometry + public archives

Owned = the **Seestar S30 Pro** (imaging, photometry, astrometry) + public archives (Gaia, AAVSO, MAST, TNS, WISeREP, Galaxy Zoo, Pickles). No spectrograph yet. **Activation vehicle: AAVSO photometry campaigns** (photometry-tagged only — the 30 mm scope has no spectrograph), with NASA Exoplanet Watch as a compute/archival path (see Activation vehicles above).
- **Photometry / light curves (Seestar)** — variable stars, exoplanet transits, asteroid rotation; AAVSO-submittable. `raw` · JEI / AAVSO.
- **Astrometry (Seestar)** — asteroid/comet positions, proper-motion checks against Gaia. `raw`
- **Stellar / transient classification via public archives + CNN** — SDSS/LAMOST spectra, TNS transients, Galaxy Zoo morphology; Computing crossover, underserved at HS level. `raw` · Astron. Educ. Rev.
- **Light-pollution mapping — residential street survey** — lux meter + GPS; spatial interpolation / ML. `raw` · JEI.
- **Cheap add-on to unlock spectroscopy:** a ~$100 Star Analyser 100 grating would make the Seestar a slitless spectrograph (stellar classification). *Not owned yet — acquire trigger.*

## Publication venue cheatsheet

Four tiers, from lowest bar to highest. Aim up — a rigorous household-materials paper can reach Tier 3 with a mentor co-author.

### Tier 1 — High-school peer-reviewed

| Journal | Acceptance / cost | Notes |
|---|---|---|
| **Journal of Emerging Investigators (JEI)** | 70–75%, $45, must be submitted by mentor | Gold standard. Hypothesis-driven life/physical sciences only (as of Mar 2026). |
| **Journal of High School Science (JHSS)** | ~20%, free, rolling | STEAM, novelty-focused. |
| **International Journal of High School Research (IJHSR)** | Fee-based, verify cost | Broader scope. |
| **National High School Journal of Science (NHSJS)** | Free, student-run | Accepts reviews + essays. |
| **Young Scientists Journal (YSJ)** | Free, UK-based | International. |
| **Curieux Academic Journal** | Light review, fee-based | Training-ground tier. |
| **eiRxiv** | Preprint, no review, free | Timestamped pre-publication. |

### Tier 2 — Undergraduate peer-reviewed (accept advanced HS with mentor)

- **Journal of Undergraduate Chemistry Research (JUCR)** — chemistry-specific, perfect for spectroscopy.
- **American Journal of Undergraduate Research (AJUR)** — multidisciplinary, national.
- **Journal of Young Investigators (JYI)** — established since 1997.
- **Journal of Undergraduate Research (JUR)** — any subject.
- **Butler / PURE Insight / Pittsburgh Undergrad Review** — university-hosted, lower bar.

### Tier 3 — Teaching / bridge (real Scopus-indexed journals that reward pedagogy)

- **Journal of Chemical Education (ACS)** — realistic target for a well-documented household experiment. Publishes ATR-FTIR and UV-Vis undergrad experiments regularly.
- **Chemistry Education Research and Practice (RSC)** — ed-research.
- **Biochemistry and Molecular Biology Education (Wiley)** — biochem pedagogy.
- **Journal of Laboratory Chemical Education** — lab experiments, lower bar.
- **Physics Education** (IOP) · **American Journal of Physics** (AAPT) — physics equivalents.

### Tier 4 — "Real" academic peer-reviewed (by research area)

- **Food authenticity** — Food Chemistry · J. Agric. Food Chem. · LWT · Food Control · Food Analytical Methods.
- **Microplastics / polymer weathering** — Marine Pollution Bulletin · Environmental Science & Technology · Chemosphere · Science of the Total Environment · Polymer Degradation and Stability · Polymers (MDPI).
- **Natural pigments / DSSC** — Dyes and Pigments · Food Hydrocolloids · Solar Energy Materials and Solar Cells · J. Photochem. Photobiol. A.
- **Analytical methods / spectroscopy** — Spectrochimica Acta Part A · Talanta · Analytical Methods (RSC) · Anal. Bioanal. Chem. · Vibrational Spectroscopy · Applied Spectroscopy.
- **Open-access multidisciplinary** — ACS Omega · Royal Society Open Science · Scientific Reports · PLOS ONE · Heliyon · RSC Advances.
- **Preprints** — ChemRxiv · bioRxiv · arXiv · Research Square.

### Non-journal recognition (in parallel)

**Greater Vancouver Regional Science Fair → CWSF → Team Canada-ISEF** (the Canada-first, homeschool-eligible gate for any science) · Regeneron ISEF · Regeneron STS · JSHS · Sanofi Biogenius Canada (biology) · USABO / USNCO / USAPhO Olympiads · **IYPT** (International Young Physicists' Tournament — the Physics track's competition anchor; its problems drive the Physics backlog). See **Activation vehicles & external gates** for the full gate map.

## Future topic structure

Live structure as of 2026-05-01 — Math/Compute/Astronomy at 2 topics each (tools + special-purpose), Physics/Chemistry/Biology at 3 each (the bench-research bulk).

Hold these for later — *don't add to `technology.yml` until at least one concrete project anchors each one*, otherwise they sit thin like Polarimetry did.

### Chemistry — 3rd topic: **Transform**

The whole point after foundational analysis. Identify / React get you to "we know what's in the sample" and "we drove a reaction to learn"; Transform is "we made something new." Without this, the chemistry section reads as a pure-analysis discipline, which understates it.

```
Topic 3: Transform  (drive chemistry to make new things)
  Synthesis:    Electrosynthesis, Photochemistry, Mechanochemistry
  Catalysis:    Heterogeneous, Homogeneous
  Kinetics:     Real-time reaction monitoring
```

Triggers to promote: a planned electrosynthesis project (water splitting, Cu plating from CuSO₄), a photochemistry demo (E/Z isomerization of stilbene under UV), or a kinetics project (decomposition rate of H₂O₂ with various catalysts watched via O₂ probe). One of these falling out of a React-electrochemistry project is likely — they're adjacent.

### Physics — future categories worth planning

Current shape: **Measure + Build** (2 topics). Restructured 2026-05-01 to a verb-pair matching every other science. Measure has Motion / Fluids / Electromagnetism (fields + optics merged). Build has Circuits / Prototypes (3D printing). Heat moved to Chem React → Thermal where Vernier Temperature Probe enables Melting Point.

**Interferometer — PASCO OS-9255A on hold (decision-not-purchase, 2026-05-01).** The PASCO Precision Interferometer is the canonical educational Michelson but at ~$2,500 CAD via AYVA (quote-only, not click-and-buy) it doesn't pencil out for a single-experiment use case. The Interferometer tech remains as a placeholder slot on the page. Trigger to revisit: a sustained optics-bench project that justifies the spend, or a sale on a used PASCO unit.

Categories worth adding (within Measure or Build, when toys commit):

- **Measure → Materials** — hardness, elastic modulus, fracture, viscosity (home hammer-test rig, 3D-printed jigs).
- **Measure → Acoustics** — sound waves, vibration, frequency analysis. Toys: Vernier Go Direct Sound, oscilloscope-on-mic.
- **Build → Optics** — custom optical setups (lasers, prisms, polarization). When sustained optics work emerges.
- **Build → Machining** — CNC, lathe, mill. Real maker capability.

Topics worth adding (3rd Physics topic, when toys + projects commit):

- **Modern / Quantum** — radioactivity (Geiger, cloud chamber), photoelectric effect, atomic spectra.
- **Heat / Thermodynamics** — returns to Physics if a real physics-side thermo toy lands (IR camera, Stirling demo). Currently parked in Chem React → Thermal.

Triggers to promote: cloud-chamber kit + first muon-counting project (Modern); shop hammer-test rig (Materials); CNC purchase (Machining); FLIR ONE Pro purchase (Heat returns).

### Biology — 3rd topic: **Grow** (project-anchored)

Bacterial Culture, Antibiotic Susceptibility, Yeast Fermentation, Plant Tissue Culture, Drosophila Genetics — these are *project areas*, not techs. Same axis distinction as the chem reaction-types (acid/base, redox, precipitation): they describe biology happening, not instruments or methods. They surface through project pages, not the Tech matrix.

When a Grow project commits with real toys (Drosophila vials + food, microbiology incubator + plates), promote the relevant techs back into a Grow topic on the page. Lowest-friction first launch: **Drosophila genetics** (~$100 from Carolina Biological — vials, food, white-eye + wild-type stocks, ice-knockout). Stereoscope under Image → Microscopy already covers sorting.

### Biology — molecular-bio expansion path (miniPCR → real PCR → sequencing)

The **mini16X is a full thermal cycler** — the endpoint @home kits on hand don't use its PCR capability at all (only the Glow Lab uses it, as a 96 °C heat source). Amplification is a reagents-away upgrade, and it's the highest-leverage biology capability we own. Staged so the first real PCR isn't also the first debugging session:

1. **Training-wheels kit (next buy).** One pre-packaged miniPCR PCR lab — reagents guaranteed to work, self-contained, runs on mini16X + GELATO. Recommended: **PTC Taster (Genotype to Phenotype)** — swab own cheek → amplify TAS2R38 → restriction digest → gel; engaging + genotype-yourself payoff, no sequencing needed. Validates the full extract→amplify→visualize loop. ~$100–150 reagent pack; confirm current price.
2. **Roll-your-own reagents.** Generic Taq **master mix** (miniPCR EZ, NEB, Promega — Amazon carries 2× mixes, ~$0.20–0.50/rxn) + **custom primers from IDT** (idtdna.com, a few $/pair, ships home — *this* is what makes any target reachable) + **self-extracted template** (Chelex / boil prep / spin column). ⚠️ real PCR needs **fresh 0.2 ml tubes + fresh filter tips** — the 2007 legacy plastic is fine for endpoint dye labs but not amplification (one stray molecule → a billion; contamination control is the whole game).
3. **Read the amplicon.** The one real gap is sequencing. Near-term: **mail-in Sanger** (Azenta/Eurofins, ~$5–10/rxn). Down-the-road big-gear trigger: **Oxford Nanopore MinION** (~$1k) if barcoding sustains — turns the bench into a full sequencing lab.

Flagship project target: **DNA barcoding of local biota** (backlog row above) — real research, cross-disciplinary (wet lab + bioinformatics), Olympiad-bio aligned, publishable. Promote to a project folder when the training-wheels kit run succeeds. In the Tech/Toy schema the miniPCR is a **Toy under Biology → Replicate** (amplification); BioBits/cell-free stays under **Cell-Free**.

### Vancouver lab buildout — pre-order priorities

What is and isn't needed for the summer 2026 home lab.

**Not needed** (skip these):
- **Fume hood** — basement has two cross-ventilation windows; sufficient for the chemistry we'd run at home.
- **-80 °C / -20 °C freezer, dedicated lab incubator, laminar flow hood** — dad's lab covers these. Cold storage of bio samples and microbiology incubation runs there, not at home.

**Worth pre-ordering** (cross-discipline bench bottlenecks; ~$1,000-1,500 total):
- **Analytical balance** (0.1 mg, ~$300-500) — universal across chem and bio. The single biggest "didn't realize how often we'd reach for it" tool.
- **Microcentrifuge** (12k rpm, 24-tube, ~$150-300) — DNA prep, sample concentration, generic spin work.
- **Vortex mixer** (~$80-150) — sample prep universal.
- **Hot plate / magnetic stirrer combo** (~$150-300) — make agar plates, dissolve reagents, control temperature for kinetics. Heavy crossover with React-Thermal work.

**Held until project commits:**
- Drosophila kit (~$100) — when Grow gets greenlit
- Microbiology starter kit (~$300) — same
- Used laminar flow hood — only if plant tissue culture becomes specifically planned
- Real autoclave (~$500-2,000) — pressure cooker substitutes for ~95% of the time

## Status key

- **raw** — idea captured, not yet scoped
- **scoped** — hypothesis, samples, protocol, expected figures all defined
- **piloting** — first data collected
- **in-progress** — full dataset being collected / written up
- **completed** — published on the site, linked from `research/index.md`
- **shelved** — parked with a reason (don't delete)

## Change log

- **2026-07-16** — **Activation vehicles & external gates** section added (high-level scaffold: one project → many gates; "project is the asset, contests are distribution"). Named a per-science activation vehicle mirroring Physics/IYPT — **Biology → DNA barcoding to BOLD/iBOL** (cleanest 1:1 bench fit), **Astronomy → AAVSO photometry campaigns** (+ Exoplanet Watch for compute; 30 mm Seestar is photometry-only), **Chemistry → no dedicated vehicle exists** (PalmSens 6-experiment on-ramp → self-sourced projects; gate is the science fair + a journal). Verified gate: **GVRSF → CWSF → Team Canada-ISEF** is grade-9- and homeschool-accessible. Flagged unresolved: MIT THINK + Davidson Fellows eligibility for a Canada-resident dual-citizen. Per-science section anchors + dashboard + recognition list updated to match. Source: two deep-research runs (2026-07-16); personal-eligibility layer kept out of this public doc (private memory).
- **2026-07-16** — **Home-lab-first reframe** (corrected against the real toy registry — each tech page's `toys:` frontmatter, not `technology.yml`). Dropped only the truly-lost SIL capabilities: FT-IR mid-IR, circular dichroism, NIR, mass spec (MALDI/LC-MS/GC-MS), chromatography, TGA/DSC, four-point probe. **Kept everything the home lab owns:** Vernier Go Direct UV-VIS/fluorescence spectrophotometer + optical fiber, Vernier Polarimeter, PalmSens EmStat Pico potentiostat, Vernier pH/conductivity/temperature/gas/turbidity/magnetic-field/force/motion/photogate/EKG/spirometer/O₂-CO₂ sensors, three microscopes (Dino-Lite / AmScope / Swift), Digilent Analog Discovery 3, Prusa CORE One+, the miniPCR bench, and the ZWO Seestar S30 Pro. Reorganized into a **tool layer (Math + Computing)** across four research sciences (**Physics, Chemistry, Biology, Astronomy**). **Physics re-anchored on IYPT 2027** (17 problems). Resources rebuilt from the registry; the all-SIL instrument-category reference deleted; the three completed SIL projects stay as historical past-work.
- **2026-07-11** — Reframed the doc from "idea backlog" to the research program's **ideation + progress-tracking** doc: retitled, dual-purpose intro, and added an **Active work & progress** dashboard at the top (piloting / on deck / completed / backlog). Updated science `CLAUDE.md` to match.
- **2026-07-11** — Consolidated the home molecular-biology lab reference into IDEAS.md as the **"Home molecular-biology lab — bench reference & progress"** section (kit set + lab order, per-lab notes, Session 0 calibration procedure, gear, cold chain, current audit status). Absorbed from the short-lived `homelab/molecular-biology.md`, which was removed — IDEAS.md now tracks both bench progress and ideation in one file.
- **2026-07-11** — Added **molecular-bio expansion path** (miniPCR mini16X is a real thermal cycler; endpoint kits don't use PCR). Staged roadmap: training-wheels PTC Taster kit → roll-your-own (IDT primers + Taq master mix + self-extracted template + fresh plastic) → sequencing (mail-in Sanger now, MinION later). Added 2 Biology backlog rows (DNA barcoding of local biota; human genotype→phenotype family panel). Updated home-capability list to reflect the real molecular-bio bench (mini16X, GELATO, 2× P51, pipettes, balance). Source: home-lab miniPCR shakedown, working doc `~/GITHUB/scratch/minipcr-home-lab/plan.md`.
- **2026-05-01** — Physics restructure (final): Move/Heat/Wave → **Measure + Build** (2 topics, verb pair matching every other science). Measure: Motion (Force, Distance, Time), Fluids (Pressure, Turbidity), Electromagnetism (Magnetic Field, Spectrometer, Interferometer — fields + optics merged). Build: Circuits (Rigol scope, TOAUTO soldering, SainSmart helping hands; Multimeter dropped as too basic), Prototypes (Bambu Lab A1 Mini placeholder for 3D Printing). Heat dropped — Vernier Temperature Probe became a toy under Chem React → Thermal → new **Melting Point** tech (with broken OptiMelt as historical toy). Vernier Conductivity Probe moved from Physics → Chem React → Conductometry (now available). Tech-name rename: Photogate→Time, Motion Detector→Distance, Gas Pressure→Pressure (toys describe the instrument, techs describe the measurement). Dropped unsupported physics tech files. Four Point Probe project relinked to new Circuits tech. All 6 sciences now at 2 topics each with verb-pair labels.
- **2026-05-01** — Removed Bio Grow from `technology.yml`. The "techs" inside (Bacterial Culture, Drosophila Genetics, etc.) are project areas, not techs — same axis-mismatch as chem reaction types (acid/base, redox, precipitation). Bio sits at 2 topics (Image, Replicate); Grow returns when toys + project commit.
- **2026-05-01** — Added Vancouver lab buildout pre-order list (cross-discipline bench bottlenecks: balance, microcentrifuge, vortex, hot plate). Dad's lab covers cold storage / incubation / laminar flow.
- **2026-05-01** — Chemistry restructure: collapsed Resolve into Identify (Separation moved up), renamed Probe → React (Thermal joined Electrochemistry), Polarimetry stayed under Identify alongside CD. Chemistry now sits at 2 topics (Identify / React); Transform stays as the planned 3rd.
- **2026-05-01** — Added "Future topic structure" section: Chemistry's planned 4th topic (Transform), Physics future categories (Acoustics, Modern, Materials, Fluids), Biology hold rationale.
- **2026-04-25** — Moved from `content/research/README.md` to repo-root `IDEAS.md` per the cross-repo `IDEAS.md` convention. Stripped Jekyll layout frontmatter (Jekyll era ended; Astro doesn't consume this doc).
- **2026-04-24** — Initial backlog seeded: chemistry (13), biology (6), physics (5), computing (5), mathematics (4), astronomy (5). Instrument + venue reference tables included.
