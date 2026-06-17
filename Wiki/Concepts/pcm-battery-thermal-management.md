---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/advances-in-phase-change-materials-for-thermal-energy-storage-and-management-cha.md"
  - "Raw/Sources/analysis-of-the-thermal-stability-of-pcms-and-its-effect-on-energy-storage-effic.md"
source_count: 2
aliases:
  - "battery TMS"
  - "lithium-ion battery PCM cooling"
  - "BTMS"
---

# PCM-Based Battery Thermal Management

Lithium-ion battery packs require precise temperature control for performance, longevity, and safety. [[latent-heat-pcm-thermal-storage|Thermal PCMs]] are a key passive strategy for battery thermal management systems (BTMS), absorbing transient heat spikes at constant temperature.

## Why PCMs for Batteries?

Battery performance and lifespan degrade significantly outside the 20–45°C optimal operating range. Three primary thermal challenges:

1. **Peak heat generation**: high-rate discharge/charge events generate concentrated heat spikes.
2. **Thermal runaway**: uncontrolled exothermic reactions; PCMs can absorb initial heat and delay propagation.
3. **Temperature uniformity**: non-uniform temperatures across cell surfaces reduce pack capacity and cycle life.

PCMs passively absorb heat spikes while maintaining a constant temperature equal to their melting point — ideal for "pulse heat dissipation" (lasers, power electronics, EV batteries).

## PCM Selection Criteria for Batteries

The PCM melting point must be matched to the target operating temperature window (ideally 25–45°C). Key selection criteria:

- Melting point in the desired range.
- High latent heat for maximum energy absorption per unit volume.
- High thermal conductivity (enhanced, since raw organics are too low).
- Chemical compatibility with cell materials (no corrosiveness).
- Low supercooling (for reliable heat release during cooling).
- Form stability / non-leakage during melting (critical for safe battery integration).

## Carbon-Based Additive Strategies

Carbon additives dominate battery BTMS due to high thermal conductivity, corrosion resistance, and low density:

| Additive | Notes |
|----------|-------|
| Expanded graphite (EG) | Most common; 3D foam provides highest conductivity boost; shape-stable |
| Graphene (GNP, rGO) | Highest conductivity; 1 wt% → +61.5% thermal conductivity; best at 30:70 MWCNT:graphene |
| Carbon fibre (CF) | 0.46 wt% optimal; shorter fibres (2 mm) for temperature reduction; longer (5 mm) for uniformity |
| MWCNTs | 1 wt% → +41% thermal conductivity |
| MWCNTs + graphene (30:70) | 1 wt% → +123.1% thermal conductivity (synergistic) |

## Shape-Stable CPCM for Batteries

Form stability (non-leakage) is especially critical for battery BTMS where leaking PCM would cause electrical shorts. Strategies:

- **EG matrix**: capillary forces retain molten organic PCM in graphite foam; shape-stable at temperatures well above melting point.
- **NiCo@C microcage / paraffin wax**: enthalpy = 130.39 J g⁻¹; efficient solar-thermal and magnetic-thermal conversion (−38.1 dB microwave absorption at 11.8 GHz); dual energy conversion.
- **Co-decorated carbonised hollow fibers**: photothermal efficiency 94.38%; stable 309.8 mV / 70.0 mA output.
- **PEG4K-Bx-PEG6K** supramolecular solid-solid PCM: 3.639 W m⁻¹ K⁻¹ with 5 wt% GNs; no leakage; self-healing; 22.90 MPa strength.
- **LA/KF@Ag** (lauric acid in kapok fiber microtubules with Ag NPs): ΔH = 146.8 J g⁻¹ (−3.8% vs. pure LA); +92.3% thermal conductivity; +15.8% storage rate; +23.5% release rate.

## Thermal Runaway Mitigation

PCMs show promise in delaying thermal runaway propagation:
- Absorb large heat flux at a fixed temperature, buying time for safety systems to activate.
- Questions remain about reliability under extreme conditions and long-term cycling stability (hundreds to thousands of high-rate cycles).

## Battery BTMS Integration Approaches

1. **PCM in direct contact with cell surfaces** (wrap or immersion): requires non-electrical-leakage PCM; form-stable composites preferred.
2. **PCM in structural module** (cavity filled with PCM composite): separates electrical and thermal management functions.
3. **Microencapsulated PCM in adhesive/polymer matrix**: allows complex geometries; see [[pcm-microencapsulation]].
4. **3D-printed PCM structures**: custom geometries; see [[tes-additive-manufacturing]].

## Temperature Management Trade-Offs

- Each carbon additive improves thermal conductivity but reduces specific latent heat proportionally (dilution).
- High nanoparticle loadings increase viscosity → suppress natural convection → can slow melting.
- Thermal hysteresis (difference between melting and crystallisation temperatures) increases with thicker shells and higher heat-ramping rates — must not exceed operating temperature range.

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — fundamental TES principles
- [[pcm-thermal-conductivity-enhancement]] — carbon additive strategies
- [[pcm-microencapsulation]] — form-stable encapsulated PCMs
- [[supramolecular-pcm]] — solid-solid and self-healing PCMs for battery BTMS
- [[tes-additive-manufacturing]] — 3D-printed battery thermal management structures
