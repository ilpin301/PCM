---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/nanoencapsulation-of-phase-change-materials-for-advanced-thermal-energy-storage.md"
  - "Raw/Sources/advances-in-phase-change-materials-for-thermal-energy-storage-and-management-cha.md"
  - "Raw/Sources/morphological-characterization-and-applications-of-phase-change-materials-in-the.md"
  - "Raw/Sources/multifunctional-electrospun-phase-change-material-mats-for-solarthermal-energy-s.md"
source_count: 4
aliases:
  - "PCM conductivity enhancement"
  - "composite PCM"
  - "CPCM"
---

# Thermal Conductivity Enhancement in PCMs

The most significant practical limitation of most thermal PCMs is low thermal conductivity — typically 0.1–0.6 W m⁻¹ K⁻¹ for organic PCMs (paraffins, fatty acids) and 0.5–1.5 W m⁻¹ K⁻¹ for salt hydrates. This limits charge/discharge rates, especially in large-scale TES systems.

PCMs doped with thermally conductive additives are called **composite PCMs (CPCMs)**.

## Enhancement Strategies by Filler Morphology

The three main morphological classes of thermally conductive additives (per the Huang et al. 2017 review):

### 1. Fibrous Additives
- Carbon fibres, carbon nanotubes (CNTs), metal fibres.
- Create 1D conductive pathways; effective at low loading fractions.
- Carbon fibre at 0.46 wt% optimises temperature reduction and uniformity in battery applications; shorter fibres (2 mm) lower temperature more effectively, longer fibres (5 mm) improve distribution.
- MWCNTs at 1 wt% improve thermal conductivity of a paraffin/PCM by ~41%.

### 2. Porous/Foam Additives
- Expanded graphite (EG), metal foams (Al, Cu), aerogels.
- 3D interconnected networks; highest enhancement per unit volume.
- EG at 12 wt% in a stearic acid–behenic acid (SA–BA) eutectic: 12.3× conductivity increase; negligible phase change property change after 100 cycles.
- Adipic acid / EG composite: ΔH_m = 162.5 J g⁻¹ vs. 202.0 J g⁻¹ for pure AA (thermal conductivity improved; latent heat reduced by dilution).

### 3. Spherical/Particle Additives (Nanoparticles)
- Carbon black, graphene nanoplatelets (GNPs), metal nanoparticles (Ag, Cu), metal oxide (Al₂O₃, TiO₂, SiO₂), hexagonal boron nitride (h-BN).
- Graphene at 20 wt%: significant thermal conductivity improvement.
- MWCNTs + graphene (30:70 ratio) at 1 wt% combined: +123.1% thermal conductivity improvement.
- Ag NPs at 10 wt% in kapok fiber/lauric acid composite: +92.3% thermal conductivity; +15.8% energy storage rate; +23.5% release rate.
- TiO₂ nanoparticles in PEG/aerogel composite: thermal conductivity 0.53 W m⁻¹ K⁻¹ (+140% over matrix alone).
- Doping a salt with 10 wt% Zn@Al₂O₃ microparticles enhanced heat capacity by 6.7%.

## The Latent Heat Trade-Off

The central dilemma: adding non-phase-changing fillers dilutes the PCM mass fraction, directly reducing specific latent heat (J g⁻¹). This is often greater than predicted by simple mixing rules because:

1. Filler mass displaces PCM mass (dilution).
2. Nanofillers can physically confine PCM molecules, restricting mobility and inhibiting complete phase transition.
3. High nanoparticle loading increases viscosity dramatically (up to 100× at highest loading for graphene-in-PCM suspensions), which suppresses natural convection during melting and can slow the overall heat transfer despite improved conduction.

**Net effect**: the loss in natural convection often outweighs the gain in conduction, resulting in slower, not faster, melting at high filler loadings.

## Two-Dimensional Nanomaterial Additives

- **Graphene** (GNPs, GO, rGO): highest thermal conductivity; risk of restacking; strong π–π interactions; enhances electrical conductivity.
- **Hexagonal boron nitride (h-BN)**: thermally conductive but electrically insulating; excellent for electronics applications where electrical isolation is required; exfoliated by sonication; few-layer BNNSs ~2–3.5 nm thick; lattice spacing 0.32 nm.
- BN/APPG (adenine-functionalised PPG polymer): increasing BN content improves thermal stability, shape retention, and leakage prevention without disrupting the intrinsic self-assembly of APPG.

## Enhanced Shell Conductivity in Encapsulated PCMs

For encapsulated PCMs, the shell itself is a thermal resistance. Strategies:
- Silica shell: ~1.3 W m⁻¹ K⁻¹ vs. ~0.2 W m⁻¹ K⁻¹ for polymer.
- Adding 1 wt% SiO₂ to a PS/PMMA shell: +8.4% conductivity.
- LbL assembly with nanoparticle layers: can boost shell stiffness and conductivity simultaneously.
- GO–CNT hybrid shell (docosane capsules): thermal conductivity enhanced through conjugated carbon network.

## Photothermal-Enhanced Composites

Combining conductive/absorbing fillers with PCMs enables **solar-to-thermal energy conversion**:
- PPy-coated electrospun PA11/PPCM mats: 0.51 W m⁻¹ K⁻¹ thermal conductivity; 18.5 S m electrical conductivity; surfaces exceed 90°C under 1.5 sun irradiation.
- Graphene-filled electrospun mats: 0.27 W m⁻¹ K⁻¹; enables moderate photothermal response.
- Co-decorated carbonised hollow fibers in PCM: photothermal efficiency 94.38%; generates 309.8 mV electrical output.
- 3D carbon foam + CNT + Co nanoparticles hierarchical hybrid: photothermal efficiency 97.07%.

## Summary of Key Values

| Additive | Loading | Conductivity Enhancement | Latent Heat Reduction |
|----------|---------|-------------------------|-----------------------|
| EG | 12 wt% | 12.3× | Modest (~20%) |
| Graphene | 20 wt% | Significant | ~20% dilution |
| MWCNTs + graphene (30:70) | 1 wt% | +123.1% | <2% |
| Ag NPs | 10 wt% | +92.3% | ~4% |
| h-BN nanosheets | varies | Proportional to content | Proportional to dilution |
| Carbon fibre | 0.46 wt% | Modest | Negligible |

## Related Notes

- [[pcm-microencapsulation]] — encapsulation as shell-conductivity strategy
- [[latent-heat-pcm-thermal-storage]] — baseline PCM properties
- [[electrospun-pcm-mats-photothermal]] — fibre-matrix PCM composites with conductivity enhancement
- [[supramolecular-pcm]] — self-healing composite PCMs
