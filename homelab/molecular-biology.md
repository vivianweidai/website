# Home molecular-biology lab — reference

Operational reference for the Vancouver home molecular-biology bench: the miniPCR
kit set, the gear that runs it, and the hard-won procedure notes. Not a web-served
page — a toolkit doc we iterate on as the tech toys grow. Companion to the
forward-looking **molecular-bio expansion path** in [`IDEAS.md`](../IDEAS.md).

Started as a multi-session shakedown (July 2026): run every kit once, hands-on, to
learn what each instrument does. James audits gear + workflow; **Vivian does the
actual hands-on labs**.

---

## The kit set and lab order

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

**Why this order:** molecular biology fails invisibly — a mispipetted reaction gives
a blank gel with no clue why. The dye labs (1, 2) announce every mistake, so you
build pipetting and electrophoresis in isolation before combining them with real DNA
(3, 4). BioBits (5) floats — no instrument, no purchase — but has only **two
reactions' worth of reagent** and expires ~early Nov 2026, so don't leave it past October.

---

## Per-lab notes

**S1 Microliter Madness** — reusable practice card + blue/yellow/red dyes (5 ml ea) +
200 µl tips + guide. No pipette included; use the P20. Three exercises ending in
pipetting a picture in colored dots. The card drills **2 µl and 5 µl** — harder than
20 µl and exactly the range the real labs need (BioBits/Glow Lab dispense 4 µl).
*Habit to establish:* always use the smallest pipette whose range contains the volume.

**S2 Cat Genetics** — colored dyes, no DNA. Melt a SeeGreen tab → pour gel → seat
comb → load wells → run → view under the amber lid. Reagents for 8 groups (botch-
tolerant). **SeeGreen All-in-One tabs** = agarose + nucleic-acid stain + TBE in one
tab; store dark (photobleach). Distilled water for gels + diluting TBE (tap-water
ions → higher current → hot gel → smeared bands).

**S3 DNA Glow Lab** — the best lab, and the only one using the thermal cycler.
Samples: AT-rich, GC-rich, 50:50, unknown. A dye fluoresces only bound to *double-
stranded* DNA; heat the samples and the glow dies as the duplex denatures. GC-rich
holds its glow to higher T (G:C = 3 H-bonds vs A:T = 2). The miniPCR steps through
known temperatures so you read a **Tm number**, not just "hot"; the P51 reads the
fluorescence. Follow-ons: break strands with 100 mM NaOH (pH, no heat); estimate the
unknown's concentration from brightness.
- Volumes: 4 µl DNA (P20); 40–65 µl samples + NaOH (P200); Buffer 1/2 at 275/255 µl
  exceed the P200 ceiling → guide has you aliquot 135 µl twice.
- **TIMING TRAP:** once the dye is diluted into Buffer 1, fluorescence holds only
  ~2 h at room temp. Dilute immediately before use, never the night before. (Diluted
  dye keeps ~72 h cold + dark.)
- Concentrated dye is DMSO-based, **freezes at 4 °C** — may arrive solid; warm in a
  clenched fist. Keep foil-wrapped (photobleaches).
- **Bundle miniPCR + P51 + 0.2 ml strip tubes as one Glow Lab kit.**

**S4 Forensics** — first run with real DNA + real gel + real staining. Kit ships
pre-made DNA (Victim, J.M., Evidence 1/2 + Fast DNA Ladder 1); no PCR. 12 µl loads →
**use the P20, never the P200** (12 µl is 6% of P200 full scale, double-digit error
you'd never see). Gloves + eyewear. Guide names GelGreen tabs from the Companion Kit;
our SeeGreen All-in-One tabs should substitute (dye included) — **confirm before running.**

**S5 BioBits** — four tubes: negative control (water), DNA A, DNA A + kanamycin,
DNA B. Green = transcription, red = translation; kanamycin blocks the ribosome.
**Read the prediction table with Vivian before opening anything** — the prediction IS
the pedagogy. Only two reactions' worth of reagent; do it after Microliter Madness so
the 4 µl-pellet mistakes are burned on a practice card first. Ships its own P51 + 4 µl
minipette. Incubate at 37 °C (fist/pocket) 15 min, then RT overnight; read 8–72 h.

---

## Session 0 — calibration procedure (metrology)

Prove every instrument is honest before trusting it. The measurement chain has to
bottom out on a traceable standard.

**0a — Scale.** THINKSCALE 50 g × 0.001 g. Install battery, place on a solid surface
away from HVAC/airflow (milligram scales drift with air), warm up, then **run the CAL
routine against the 50 g weight** (just placing the weight in weigh mode does NOT
recalibrate — hold the CAL button until it prompts). Re-weigh: expect 50.000. *After a
successful cal, the same weight must read nominal by construction — so the real test
of a scale is whether a **third** mass reads true, which 0c does.*

**0b — Gilsons.** Cycle each plunger 20–30× through full travel; feel for grit or a
sticky return (dry O-ring → cheap Gilson seal kit, ~10 min). Both stops should be
palpable.

**0c — Gravimetric check (the real test).** Weigh water the pipette dispenses.
- **Method: weigh-by-difference, NOT a standing tare.** Record empty tube mass `m0`,
  dispense **10×** into it, record `m1`; water = `m1 − m0`. Ten dispenses because one
  20 µl shot = 20 mg and 1 mg readability is 5% quantization — too coarse to see ±1%.
- **Why weigh-by-difference:** a cheap milligram balance won't hold a tare for the
  ~2 min it takes to dispense 10× — the zero drifts and you get impossible readings
  (a first attempt read 52 µl/shot from pure tare drift). Two absolute weighings
  seconds apart beat one trusted-for-2-minutes tare.

  | Pipette | Set to | 10× target | Pass (±1%) |
  |---|---|---|---|
  | P20 | 20 µl | 200 mg | 198–202 |
  | P200 | 100 µl | 1000 mg | 990–1010 |
  | P1000 | 1000 µl | 10 000 mg | 9900–10 100 |

- Reads accuracy (systematic bias), not precision (scatter). A pipette biased low is
  **usable if you know the bias**; one that scatters is dead.

**Pipetting technique (learned the hard way):** **first stop to fill, both stops to
empty.** Press ONLY to the first (soft) stop before drawing up — going to the second
(hard/blow-out) stop before aspirating over-draws. Dispense = first stop, then through
to the second; withdraw the tip before releasing the plunger.

**0d — miniPCR dry-run.** Run the built-in **Quality control protocol** empty. It
heats the **lid first** (~105 °C, anti-condensation) before the block ramps; then the
block goes ~18→95 °C in <1 min (fast, clean). Confirms block + lid heaters healthy and
teaches the app. The full QC run is ~3.7 h (a burn-in soak) — stop early once you've
seen the ramp; a real PCR is 45–90 min.

---

## Gear

### Pipettes

| Pipette | Range | Source | Status |
|---|---|---|---|
| P20 | 2–20 µl | ONiLAB | new, ISO 8655 cert, 0.5 µl increment. Ships with stand, hex adjustment/ejector wrench (**keep — it's the recalibration tool**), color ID clips, 200 µl tips |
| P200 | 20–200 µl | Gilson Pipetman Classic (yellow cap) | cal due 2012-05; feels good; **gravimetric-verify before first real use (Glow Lab)** |
| P1000 | 100–1000 µl | Gilson Pipetman Classic (blue cap) | cal due 2012-05; feels good; verify when first needed |

Nothing in any lab needs <2 µl. Store all pipettes **hanging tip-down** (liquid drains
away from the piston seal).

### Consumables

- **New (fresh, sterile):** 2–200 µl tips → P20 & P200; 1.5 mL microtubes → reactions
  + gravimetric weighing; 8-strip 0.2 ml PCR tubes → thermal-cycler samples.
- **Legacy (fine for endpoint labs, water):** Zap 100–1000 µl filter tips (exp 2007) +
  loose blue 1000 µl tips → P1000; one bag of Sarstedt 2 ml screw tubes kept as
  leak-proof/freeze storage (pruned the surplus).
- ⚠️ **Real PCR needs fresh plastic** — fresh filter tips + fresh 0.2 ml tubes.
  Legacy tips are fine for endpoint assays but PCR turns one stray molecule into a
  billion; contamination control is the whole game.

### Instruments

- **miniPCR mini16X** — full programmable thermal cycler (BLE + USB). Controlled via
  the miniPCR **v3.0 app** (Mac: links.minipcr.com/mac_download; iOS: App Store). Used
  by the Glow Lab only in the endpoint set, but PCR-capable for the expansion path.
- **GELATO** — electrophoresis + integrated blue-LED transilluminator. **Standalone,
  no app**: built-in PSU 50–135 V, on-unit voltage + timer, amber viewing lid, phone
  doc-hood for imaging.
- **Two P51 fluorescence viewers** — one for the Glow Lab, one ships inside BioBits.

**Physics note:** the GELATO transilluminator and the P51 use the *same* principle —
blue-LED excitation + amber filter exploiting the **Stokes shift** (blue in → longer-
wavelength green out); the dsDNA-binding dye fluoresces only when intercalated in a
double helix. Two implementations of one idea, at two scales. Safe blue light, not UV.

---

## Cold chain

Label a bin so nobody in the house tosses reagents — a shared family freezer is the
single biggest risk to the reagents.

| Where | What | Lot | Deadline |
|---|---|---|---|
| Freezer −20 °C | BioBits Central Dogma (KT-1910-02) | BBT-251120 | ~early Nov 2026 |
| Freezer −20 °C | Forensics (KT-1504-01) | EF-251110 | ~May 2027 |
| Freezer −20 °C | PTC Taster Lab (KT-1004-03) | — | 12 mo from receipt |
| Freezer −20 °C | 16S Barcoding (KT-1015-01) | — | 12 mo from receipt |
| Fridge 4 °C | Glow Lab dye + DNA samples + buffers | GLO-2512 | — |

Room-temperature-but-dark: SeeGreen tabs, any diluted dye.

---

## Standing gotchas

- **Label the two power bricks.** Big = GELATO, small = miniPCR — similar-looking,
  different voltages.
- **Antifog spray lives with the GELATO** — the transilluminator lid fogs when a warm
  gel goes under it.
- Distilled water for gels + buffer; tap water is fine for pipette calibration
  (Vancouver water is very soft).
- Buy **PTC taste paper separately** for the PTC lab (Bartovation Super Taster kit,
  amazon.ca) — it's the phenotype half and not in the kit. Only the PTC + Control
  strips pair with the TAS2R38 genotyping; Na Benzoate + Thiourea are bonus.

---

## Current status (as of 2026-07-11)

- **S0 Calibration** ✅ complete — scale traceable (50.000), both Gilsons feel good
  (gravimetric deferred to point-of-use), P20 technique learned, miniPCR ramp healthy.
- **S1 Microliter Madness** ✅ audited — gear present, workflow understood, put away
  for Vivian.
- **S2 Cat Genetics** 🟡 GELATO powers on & understood; still to eyeball casting tray +
  comb + distilled water.
- **S3 DNA Glow Lab** ✅ audited — all gear present & located (buffers were in the
  fridge bag). Queued for the real run: P200 gravimetric check first; dilute dye <2 h
  before use; warm DMSO dye if frozen.
- **S4 Forensics · S5 BioBits** ⬜ pending audit.
- **First real-PCR kits ordered** (PTC Taster KT-1004-03 + 16S Barcoding KT-1015-01) →
  −20 °C freezer on arrival, 12-mo shelf life. Gear confirmed compatible. See the
  expansion path in `IDEAS.md`.

### Open items

- [ ] Confirm SeeGreen tabs substitute for GelGreen in the Forensics lab.
- [ ] Eyeball GELATO casting tray + comb; get a distilled-water jug.
- [ ] Second/third pipette stand (need three hangers).
- [ ] Identify the ~15 dropper bottles (probably microscopy stains → belong with the
      microscope, not the DNA work).
- [ ] ZWO Seestar S30 accessory kit (dew shield, dust cap, Bahtinov mask, filter
      adapter) turned up in the lab boxes — belongs with the telescope.
