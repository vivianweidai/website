---
project: Genes in Space
tech:
  - Genomics
title: "Meow to Mars — Will Space Help or Hurt Mi's Heart?"
sciences:
  - Biology
mi: true
---

<div class="hero-single"><img src="photos/photo.jpeg" alt="Mi the astronaut cat" style="object-position: center 70%;"></div>

<div class="section-heading"><h2>Overview</h2><span class="section-date">March 31st 2026</span></div>

**Sarcomere genes in microgravity.** Can a journey to Mars actually be good for Mi's heart? Mi is a British Shorthair, a breed particularly predisposed to hypertrophic cardiomyopathy (HCM) — the most common heart disease in cats and one that also affects 1 in 500 humans. The MYBPC3 gene mediates HCM by disrupting the cardiac myosin-binding protein C (cMyBP-C), which regulates muscle contraction in the sarcomere. On Earth, the heart must work against gravity's hemodynamic load. In microgravity, that mechanical load disappears — but does this compensate for or compound the effects of MYBPC3 mutations?

## Hypothesis

Microgravity differentially reduces MYBPC3 gene expression in mutant versus wild-type cardiomyocytes, revealing whether mechanical unloading compensates for or compounds hypertrophic cardiomyopathy in space. The molecular target is the **MYBPC3 gene** — two mutations associated with HCM in cats (**A31P** and **R820W**), with myriad other MYBPC3 mutations linked to HCM in humans.

## Method

| Category | Details |
|----------|---------|
| Instruments | miniPCR Thermal Cycler, BioBits Cell-Free System, P51 Fluorescence Viewer |
| Samples | Cardiomyocyte cell cultures (human and British Shorthair cat) |
| Variants | Wild-type and mutant MYBPC3 (A31P, R820W) |
| Controls | Identical samples processed on Earth under normal gravity |
| Measurement | mRNA transcript levels of MYBPC3, normalized against GAPDH |
| Readout | Fluorescence band intensity comparison (ISS vs. Earth) |

Cardiomyocyte cultures carrying both wild-type and known mutant MYBPC3 variants are prepared on Earth. Identical sample sets are sent to the ISS and processed in parallel on the ground as controls. On the ISS, mRNA transcripts of MYBPC3 are amplified using the **miniPCR Thermal Cycler** and detected with the **P51 Fluorescence Viewer**, comparing band intensity between ISS and Earth samples. The **BioBits Cell Free System** is used to express cMyBP-C protein from the amplified cDNA, testing whether microgravity affects protein translation as well as transcription. See the <a href="https://github.com/vivianweidai/science/blob/main/web/public/research/projects/20260401%20Genes%20in%20Space/output/20260331%20Genes%20in%20Space.pdf" rel="noopener">proposal document</a> and <a href="https://github.com/vivianweidai/science/tree/main/web/public/research/projects/20260401%20Genes%20in%20Space/papers" rel="noopener">reference literature</a>.
