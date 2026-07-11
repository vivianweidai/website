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

_Last updated 2026-07-11._

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
- **TGA Q50** — thermogravimetric analysis, walk-up guide in hand.
- **DNA barcoding of local biota** — flagship molecular-bio project; promote to a
  project folder after the PTC training-wheels run succeeds.

**Completed & published** (in `public/research/projects/`)
- IR Spectroscopy · UV-Vis Spectroscopy (+ FluoroMax/Lambda 750/J-1500 side scans) ·
  Four Point Probe.

**Backlog** — ~30 raw ideas across all six sciences; see **Idea backlog** below.

## Goals

- **Cover all six sciences** — Mathematics, Computing, Physics, Chemistry, Biology, Astronomy. Each should have at least one live project by end of 2026.
- **Publish.** At least one JEI-level paper per year, one Journal of Chemical Education paper, and one submission into a real peer-reviewed adult venue (mentor co-author).
- **Push our toy advantage.** Where we have hands-on walk-up access to instruments that other high-school researchers don't, the project should use those instruments as its primary readout, not as incidental confirmation.
- **Target underserved areas.** Household-materials science, quantitative pedagogy, and cross-instrument combinations. Avoid re-running studies that already have hundreds of papers.
- **Fold in machine learning** where it fits — spectral classification, chemometrics, kinetics fitting. Don't force ML into projects where a linear fit answers the question.
- **Use curriculum knowledge.** Projects should draw on what we've studied (AP-level math through calculus; stats + inference; ML methods/algorithms; full AP chem + organic; AP-level physics incl. modern; AP-level bio incl. genetics, ecology, neuroscience; Olympiad-level astronomy).

## Selection criteria (applied to every idea)

An idea earns a project slot when it checks most of these:

1. **Toy advantage** — uses a walk-up instrument we've already been trained on, OR one we can reach within the next visit (see Resources below).
2. **Underserved** — literature search shows a clear gap at the household-sample or cross-instrument level, not yet saturated.
3. **Curriculum fit** — connects to something we've already studied, so the analysis isn't a black box.
4. **Cross-discipline leverage** — ideally spans two sciences or two instruments. Single-instrument projects are fine but lower priority unless the underserved angle is strong.
5. **Publishable shape** — a clear hypothesis, a well-defined sample set, a figure set we can picture before starting.
6. **ML-ready (when applicable)** — the data shape supports classification, regression, or clustering we can learn from.

## Resources

### Toys with hands-on walk-up experience (our advantage)

| Instrument | Discipline | Typical readout | Completed project |
|---|---|---|---|
| Thermo Scientific Nicolet 380 FT-IR Spectrometer | Chemistry | 4000–400 cm⁻¹ transmittance/absorbance | `20260419 IR Spectroscopy` |
| Shimadzu UV-2550 UV/Vis Spectrophotometer | Chemistry | 200–1100 nm absorbance | `20260420 UV-Vis Spectroscopy` |
| Horiba Jobin Yvon FluoroMax-3 Spectrofluorometer | Chemistry | 200–800 nm emission + excitation | `20260420 UV-Vis Spectroscopy` |
| Jandel RM3 Four-Point Probe | Chemistry / Physics | Sheet resistance, resistivity | `20260404 Four Point Probe` |
| PerkinElmer Lambda 750 UV/Vis/NIR | Chemistry | 190–3300 nm, integrating sphere | Side scan in `20260420` |
| Jasco J-1500 CD Spectrometer | Chemistry / Biology | 163–950 nm circular dichroism | Side scan in `20260420` |
| OptiMelt Automated Melting Point System | Chemistry | Melting point | Attempted in `20260405` — non-functional |

### Toys on deck (walk-up guide in hand, not yet run)

- **TA Instruments TGA Q50** — thermogravimetric analysis (mass loss vs. temp). Next up.
- Agilent 7890A GC / 5975C Inert MSD, Waters Micromass ZQ LC-MS, Shimadzu MALDI-8020 — guides available; unscheduled.
- CEM Discover Microwave Reactor, Orec Ozonator — guides available.

### Non-toy experimental capability (home / kit-based)

- Kitchen-scale wet-lab chemistry (cooking, buffering, extraction, pH).
- **Molecular biology bench (miniPCR home lab)** — real capability, not a toy demo. **miniPCR mini16X** (full programmable thermal cycler — does real PCR, not just the endpoint labs we bought), **GELATO** electrophoresis + blue-LED transilluminator, **two P51** fluorescence viewers, ONiLAB P20 + Gilson P200/P1000 pipettes, milligram balance. The @home kits on hand (Microliter Madness, Cat Genetics, DNA Glow Lab, Forensics, BioBits) are *endpoint* labs; the hardware is fully PCR-capable the moment reagents are added. See **Molecular-bio expansion path** under Future topic structure.
- Kit biology — Genes in Space kit (PCR-adjacent), centrifuge, basic microscopy.
- Arduino / Raspberry Pi sensors if a project calls for it.

### Curriculum strengths (what we can analyze, not just measure)

- **Mathematics** — through calculus incl. vectors, differentials, fields, approximation.
- **Computing** — stats (distributions, inference, significance testing), algorithms, **Learning (Methods + Algorithms)** → ML foundation for classification / regression / clustering.
- **Physics** — mechanics, harmonics, E&M, thermodynamics, optics, modern.
- **Chemistry** — full AP + organic (incl. Spectroscopy module) + inorganic.
- **Biology** — cells, genetics (Mendel, non-Mendel, expression, regulation, mutation), ecology, plants, animals, neuroscience.
- **Astronomy** — Olympiad-level incl. observations, coordinates, mechanics, solar system, stars, cosmology.

### Cross-instrument combinations (highest leverage)

- **FT-IR + UV-Vis** on the same samples → polymer weathering (carbonyl index + yellowing), cooking-oil oxidation (C=O + conjugated dienes), natural-dye characterization (functional-group class + λmax).
- **UV-Vis + Four-Point Probe** → DSSC workflow (dye absorption + substrate conductivity).
- **UV-Vis + Fluorescence (FluoroMax-3)** → same sample, absorption + emission + Stokes shift + quantum yield estimation.
- **UV-Vis + CD (J-1500)** → chiral pigments (carotenoids) or protein samples.

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

Organized by science discipline. Each idea lists status, primary instruments, one-line hypothesis, why it's underserved, target publication venue, and ML hook (if any).

### Chemistry

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **Anthocyanin pH ladder across household products** | raw | UV-2550 | Red-cabbage indicator is ubiquitous in hobby/pedagogy material but rarely tied to quantitative λmax shifts across realistic household-product diversity. | JEI / J. Chem. Educ. | Cluster household products in λmax × pH space; flag metal-complexation outliers. |
| **Cooking-oil oxidation over reheat cycles** | raw | FT-IR + UV-2550 | Industrial oil-oxidation data doesn't map to home-kitchen reheat conditions; per-cycle home data is thin. | J. Chem. Educ. / Food Chemistry | Regression: cycle count → carbonyl index + 234 nm diene absorbance, across oil types. |
| **Thermal-receipt paper BPA/BPS/BHPF survey** | raw | FT-IR | Receipt-paper developer replacements (BPA→BPS→BHPF) have rolled through retail with almost no public fingerprint survey by retailer/year. | JEI → Environ. Sci. Technol. Lett. (mentor) | Classifier: ATR spectrum → developer class. |
| **Thrift-store textile authenticity (silk/cashmere/wool claims)** | raw | FT-IR | Single-fiber ATR classification hasn't been run at consumer-retail scale. | JEI / J. Chem. Educ. | Amide I/II band ratios + Random Forest to label protein vs. cellulose vs. synthetic. |
| **Home-dryer lint microfiber survey** | raw | FT-IR | Indoor textile-microfiber shedding at household scale is under-reported vs. ocean/beach microplastics. | JEI → Mar. Pollut. Bull. (mentor) | Classifier: spectrum → polymer class (PET / nylon / acrylic / cotton blend). |
| **Face-mask polymer aging (post-COVID archive)** | raw | FT-IR | Polypropylene non-woven aging under realistic storage (drawer, car, pocket) is not documented in the open literature. | JEI | Carbonyl-index regression vs. stated storage condition. |
| **Produce-surface coating survey (apples, citrus, cucumber)** | raw | FT-IR | Wax/shellac/resin coatings vary by supplier and season; systematic ATR survey isn't published. | JEI / J. Agric. Food Chem. | Spectral clustering → supplier ID. |
| **Reusable vs. single-use grocery-bag aging** | raw | FT-IR | Reusable-bag microplastic shedding is under-studied compared to single-use debate. | JEI → Chemosphere (mentor) | Weathering regression. |
| **Tire-wear particles vs. roadside microplastics** | raw | FT-IR | Tire-wear is the largest urban microplastic source but rarely sampled at benchtop ATR scale. | Mar. Pollut. Bull. / Sci. Total Environ. (mentor) | Classifier: TWP vs. other polymer class. |
| **Sunscreen UV-A/UV-B brand survey + photodegradation kinetics** | raw | UV-2550 (+ Lambda 750) | SPF claims are public; per-brand coverage curves and avobenzone decay rates aren't. | JEI → Photochem. Photobiol. A (mentor) | Kinetic fit + brand classifier from absorbance curve. |
| **Laundry-dye wash-off kinetics** | raw | UV-2550 | Colorfastness is industry-measured by eye; quantitative per-cycle dye-release curves are thin. | JEI / J. Chem. Educ. | Kinetic fit (first/second order). |
| **Anthocyanin stability under cooking (boil/steam/roast/microwave)** | raw | UV-2550 | Cross-source cooking-method comparison under identical protocol is under-documented. | J. Chem. Educ. / LWT | Degradation-rate regression. |
| **Natural-dye DSSC screening — λmax vs. open-circuit voltage** | raw | UV-2550 + Jandel RM3 | Most DSSC papers use a single dye; a systematic λmax→efficiency correlation across 10–20 edible extracts is a publishable shape. | J. Chem. Educ. → Sol. Energy Mater. Sol. Cells (mentor) | Regression: dye spectral features → efficiency. |

### Biology

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **Fruit-ripening pigment kinetics (banana, tomato, blueberry)** | raw | UV-2550 + FluoroMax-3 | Static ripeness snapshots are common; true kinetic time-series at home conditions are rare. | JEI / J. Chem. Educ. | Fit chlorophyll disappearance + carotenoid rise simultaneously; spectral unmixing. |
| **Chlorophyll-a content as leaf-stress indicator (drought / salt / light)** | raw | UV-2550 + FluoroMax-3 | Plant-stress spectroscopy usually uses field reflectance; controlled benchtop extract-based comparisons at household-stressor level are thin. | JEI / Plant Physiology (mentor) | Regression: stress treatment → chlorophyll a/b ratio. |
| **Catalase activity across potato varieties / storage conditions** | raw | UV-2550 | Enzyme kinetics (H₂O₂ decomposition) is classical — but supermarket-variety comparison is undocumented. | JEI / J. Biol. Ed. / J. Chem. Educ. | Michaelis-Menten fit; cluster varieties. |
| **Protein secondary structure of commercial egg whites / casein / gelatin** | raw | J-1500 CD | CD on household proteins at controlled denaturation is rarely done outside of pure research labs. | JEI / Biochem. Mol. Biol. Educ. | α-helix / β-sheet deconvolution via convex mixture model. |
| **Tea oxidation live (green → black) kinetics** | raw | UV-2550 + FluoroMax-3 | Industrial tea-processing data is usually endpoint; real-time home-replicated oxidation curves aren't. | JEI / LWT | Kinetic fit + theaflavin/thearubigin ratio regression. |
| **Maillard browning in caramelization of honey / sugars / bread** | raw | UV-2550 | Classic Maillard kinetics under real home conditions (oven, toaster) vs. idealized industrial data is a gap. | JEI / J. Chem. Educ. | First-order kinetic fit at 420 nm across substrates. |
| **DNA barcoding of local Vancouver biota (COI / rbcL / matK / ITS)** | raw | miniPCR mini16X + GELATO + mail-in Sanger | Household/citizen barcoding of local plants, insects, fungi, and market seafood — with a full extract→amplify→sequence→BLAST→BOLD pipeline — is a strong, genuinely novel JEI shape (each specimen is new data). Doubles as a wet-lab + bioinformatics cross-project. | JEI + BOLD submissions | Sequence QC + alignment + BLAST/phylo placement; the pipeline IS the result. |
| **Human genotype→phenotype family panel (PTC TAS2R38, PV92 Alu, lactase MCM6)** | raw | miniPCR mini16X + GELATO | Classic markers, but running them as a *quantitative* family/population panel tied to Hardy–Weinberg and allele-frequency stats is an Olympiad-aligned pedagogical shape. | JEI / Biochem. Mol. Biol. Educ. | Allele-frequency estimation, HWE χ² test, small-sample inference. |

### Physics

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **Sheet-resistance vs. sputter/anneal for PEDOT:PSS films (DMSO dopant)** | raw | Jandel RM3 + UV-2550 | Classic PEDOT:PSS conductivity boost is textbook; systematic kitchen-lab reproduction is a publishable pedagogical artifact. | J. Chem. Educ. / J. Mater. Educ. | Regression of conductivity vs. secondary-dopant concentration. |
| **Bandgap of semiconductor powders via Tauc plot** | raw | Lambda 750 + UV-2550 | Quick-start Tauc-plot pedagogy across household-accessible semiconductors (TiO₂, ZnO, Fe₂O₃, CuO) with quantitative uncertainty. | J. Chem. Educ. | Linear-regression bandgap extraction with proper CI propagation. |
| **Pendulum / damped oscillator — period & Q** | raw | Home (camera + ML pose tracking) | Every intro physics lab does this; nobody frames it as a Bayesian inverse problem. | JEI / Phys. Educ. | Pose-tracking ML + Bayesian fit of damping + drive. |
| **DSSC I–V curves with natural dyes — efficiency benchmarking** | raw | Jandel RM3 + Home multimeter | Junction of physics + chemistry; efficiency measurements at household-reagent scale. | Sol. Energy Mater. Sol. Cells (mentor) | Efficiency regression from dye UV-Vis features. |
| **Polarization of sky light (Rayleigh scattering) — angle map** | raw | Home polarizer + camera | Classroom demo; rarely published as a full angular map with ML. | Phys. Educ. / JEI | Fit Rayleigh model to pixel-level polarization intensity. |

### Computing

(Projects where the primary contribution is algorithmic / ML, even if the data came from another discipline's instrument.)

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **ML classifier for microplastic polymer class from ATR-FTIR** | raw | FT-IR data | Open-source classifiers exist but aren't benchmarked on household-shedding samples (dryer lint, car upholstery, synthetic fabric). | JEI / Anal. Methods | CNN on raw spectrum OR Random Forest on band-integrated features. |
| **Autoencoder for FT-IR spectral library compression + anomaly detection** | raw | FT-IR data | Library search is dominant; anomaly detection (unknown substance) is underexplored. | JEI / Anal. Chem. (mentor) | Convolutional autoencoder; reconstruction-error threshold. |
| **Chemometric oil-authenticity PLS regression** | raw | FT-IR + UV-Vis | Olive-oil adulteration published often, but with small datasets; a home-scale benchmark is missing. | J. Chem. Educ. / Food Chemistry | Partial least squares regression. |
| **Spectral unmixing of fruit-pigment mixtures (chlorophyll + carotenoid + anthocyanin)** | raw | UV-Vis + FluoroMax-3 | Non-negative matrix factorization on kitchen-chemistry mixtures is rare. | JEI / J. Chem. Educ. | NMF; cross-validate against known single-component spectra. |
| **Bayesian kinetics fitting for enzyme / reaction time-series** | raw | UV-Vis time-series | Textbook regression ignores parameter uncertainty; Bayesian fits on home data are rare and pedagogically valuable. | J. Chem. Educ. | PyMC or numpyro; posterior on rate constant. |

### Mathematics

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **Beer-Lambert nonlinearity at high concentration** | raw | UV-2550 | Every textbook says "linear up to A ≈ 1"; quantitative deviation mapping as a function of molecular structure is rarely done. | J. Chem. Educ. | Residual regression vs. concentration. |
| **Four-point-probe geometric correction factors for irregular samples** | raw | Jandel RM3 | Valdes corrections assume thin infinite plane; real household samples (non-rectangular films) deviate. Finite-element + measurement comparison is publishable. | J. Chem. Educ. / Rev. Sci. Instrum. (mentor) | Finite-element simulation vs. measured ratio. |
| **Fourier transform of an FT-IR interferogram — pedagogical derivation** | raw | FT-IR raw interferogram | Every student uses FT-IR; almost none have seen the interferogram → spectrum transform done by hand. | J. Chem. Educ. / Am. J. Phys. | Walk through FFT from first principles with real data. |
| **Tea-steeping diffusion model — Fickian vs. anomalous** | raw | UV-2550 time-series | Great real-world Fick's-law application; home dataset is a clean vehicle. | J. Chem. Educ. | Curve-fit diffusion equation; BIC comparison between Fickian and anomalous. |

### Astronomy

| Idea | Status | Instruments | Why underserved | Target venue | ML hook |
|---|---|---|---|---|---|
| **Solar spectrum through the window — Fraunhofer line mapping** | raw | UV-2550 | Lab UV-Vis can capture a real solar spectrum; almost no student paper reports Fraunhofer-line identifications at benchtop resolution. | JEI / Am. J. Phys. | Line-matching algorithm vs. NIST solar line database. |
| **Atmospheric absorption via dual-time-of-day UV-Vis** | raw | UV-2550 | Beer-Lambert applied to the sun across a day — classic Langley plot, rarely replicated at home scale. | JEI / Am. J. Phys. | Langley-plot regression to infer exo-atmospheric flux. |
| **Stellar classification via public spectra** | raw | SDSS / LAMOST public data | Pedagogically underserved at the high-school level. | JEI / Astron. Educ. Rev. | CNN on 1-D spectra → spectral class. |
| **Light-pollution mapping — residential street survey** | raw | Lux meter + GPS | Citizen science exists; household-street-scale ML mapping is thin. | JEI / J. Quant. Spec. Rad. Transf. (mentor) | Spatial interpolation; ML regression on features (streetlights, canopy). |
| **Eclipse UV-Vis during partial solar coverage** | raw | UV-2550 + opportunity | Opportunity-driven; time-resolved spectrum through partial eclipse is publishable curiosity. | JEI / Am. J. Phys. | Fit disk-coverage model to absorbance drop. |

## Instrument research-category reference

Cheat sheet of what each hands-on toy is the *primary* tool for in the literature — for retrieval when brainstorming.

### Nicolet 380 FT-IR (mid-IR ATR/transmission workhorse)
Polymer/plastic identification · natural-product structural confirmation · food authenticity (oils, honey, milk) · microplastic ID · pharmaceutical polymorphs · forensics (paint, fiber, ink) · art conservation · polymer weathering (carbonyl index).

### Shimadzu UV-2550 (200–1100 nm double-beam)
Beer's-law quantitation · reaction kinetics · enzyme kinetics · natural-pigment quantitation (anthocyanins, chlorophyll, carotenoids) · nanoparticle plasmon sizing · bandgap (Tauc) · DNA/RNA/protein concentration · DSSC natural-dye screening.

### Horiba FluoroMax-3 (spectrofluorometer)
Fluorophore excitation/emission · quenching (Stern-Volmer) · quantum-dot / carbon-dot characterization · environmental fluorophores (PAHs, CDOM) · metal-ion sensors · protein tryptophan fluorescence · FRET · upconversion.

### PerkinElmer Lambda 750 UV/Vis/NIR (190–3300 nm, integrating sphere)
Solid-film optical properties · semiconductor bandgap on opaque samples · photovoltaic active-layer absorbance · textile/coating reflectance · tissue diffuse reflectance · NIR overtones (water content in food).

### Jasco J-1500 CD (163–950 nm)
Protein secondary structure · protein thermal stability · nucleic-acid conformation · drug-protein binding · chiral small-molecule assignment · amyloid / aggregation.

### Jandel RM3 Four-Point Probe
Transparent conductive oxides (ITO, FTO, AZO) · conductive polymers (PEDOT:PSS) · 2D materials (graphene, MXene) · solar-cell contact layers · printed/flexible electronics · doped-semiconductor QA.

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

Regeneron ISEF · Regeneron STS · JSHS · USABO / USNCO / USAPhO Olympiads.

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

- **Measure → Materials** — hardness, elastic modulus, fracture, viscosity. Bridges to Chem-Thermal (TGA-DSC of polymers).
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
