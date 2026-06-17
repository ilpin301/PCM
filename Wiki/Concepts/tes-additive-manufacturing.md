---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/additive-manufacturing-for-phase-change-thermal-energy-storage-and-management.md"
source_count: 1
aliases:
  - "3D printing PCM"
  - "AM for TES"
  - "FFF PCM composites"
---

# Additive Manufacturing for TES with Phase Change Materials

Additive manufacturing (AM) — commonly 3D printing — enables co-optimisation of PCM material properties and device geometry simultaneously, unlike conventional manufacturing which optimises each independently. This unlocks complex internal topologies (microchannels, fins, lattice scaffolds) that dramatically improve TES energy and power density.

Source: Freeman (2023) PhD dissertation, Embry-Riddle Aeronautical University.

## Why AM for TES?

Conventional TES enhancement focuses on:
1. Maximising latent heat (material selection).
2. Increasing thermal conductivity (conductive additives/composites).

These goals conflict (see [[pcm-thermal-conductivity-enhancement]]): adding a non-phase-changing conductive material dilutes PCM mass. AM offers a third path:
- **Geometric enhancement**: complex channel networks, extended surfaces, and optimised fin geometries that increase heat transfer surface area without displacing PCM volume.
- **Ragone analysis**: AM-enhanced TES devices can simultaneously increase power density (rate of heat exchange) and maintain high energy density.

## AM Methods for PCM Composites

| Method | Description | PCM Compatibility |
|--------|-------------|-------------------|
| FFF (fused filament fabrication) / FDM | Extrusion of molten thermoplastic filament | Organic PCMs blended into thermoplastic matrix |
| SLS / SLM (selective laser sintering / melting) | Powder bed fusion | Challenging with PCM-containing powders |
| SLA (stereolithography) | UV photopolymerisation of resin | Digital Light Processing; emulsion-based |
| DIW (direct ink writing) | Extrusion of viscoelastic ink | PCM suspensions if rheology tuned |

## HDPE/PCM Composite Filament (FFF)

The primary experimental system: PCM42 (a commercial paraffin PCM, melting point ~42°C) compounded with high-density polyethylene (HDPE) and extruded into 3D-printing filament.

- **Filament fabrication**: single-screw extruder; optimal settings 190°C, 4 RPM; consistent diameter critical.
- **PCM loading**: up to 50 wt% PCM42 in HDPE.
- **Phase change retained**: DSC confirms the PCM42 peak is preserved in the composite; HDPE has a separate, higher-temperature peak (~130°C).
- **Microstructure**: optical microscopy shows HDPE as platelet-like structures; PCM as lattice-like structures.
- **Printed samples**: 25 mm diameter, 4 mm thick discs; HDPE requires elevated build environment to prevent delamination/curling.

## Microencapsulated PCM / TPU Composites (MEPCM-TPU)

A second system uses commercially microencapsulated PCM (MEPCM spheres) compounded with thermoplastic polyurethane (TPU, Shore 80A):

- MEPCM loaded at 50–80 wt% into TPU via single-screw or twin-screw extrusion.
- **Twin screw** produces better particle distribution at 50–60 wt%; SEM confirms intact capsule morphology.
- MEPCM retains its core PCM properties through the extrusion process (verified by DSC/TGA).
- Printed MEPCM-TPU samples demonstrate shape-stable PCM storage (no leakage during melting).
- Key challenge: filament consistency degrades at high MEPCM loadings; 60 wt% is practical upper limit for reliable FFF.

## Numerical Modelling of PCM Melting in TES Devices

Freeman also developed finite-volume (FVM, Fluent) and finite-difference (Matlab) models for PCM melting in a microchannel device:

- 3D microchannel geometry with PCM surroundings.
- Fluid: 20% propylene glycol in water (temperature-dependent material properties).
- PCM: tetradecane in graphite matrix (specific heat vs. temperature profile for phase change).
- FVM and FD agree well with experiments in constant-power condition.
- **Inactive zone** phenomenon: as melt front spans the full fluid channel length, a zone of low local Nusselt number develops; thermal boundary layer development changes character simultaneously with melt front movement.

## Key Design Insights

- The performance benefit of AM lies in enabling geometric designs inaccessible by machining — gyroid lattices, micro-pin fins, triply-periodic minimal surfaces.
- Future vision: heat exchangers spanning multiple length scales; surface-area-to-volume ratios vastly exceeding conventional shell-and-tube designs.
- DOE Building Technology Office target energy density: referenced as benchmark for AM-TES competitive performance.

## Salt Hydrate vs. Organic PCMs in AM Context

Organic PCMs are preferred for AM because:
- Available in microencapsulated form (MEPCM).
- Thermally stable at AM processing temperatures (unlike salt hydrates which can dehydrate).
- Not corrosive to metal AM components.
- No phase separation risk during processing.

Salt hydrates: limited to transition temperatures <100 °C; not yet practical in AM workflows.

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — PCM fundamentals and material properties
- [[pcm-thermal-conductivity-enhancement]] — composite PCM approaches
- [[pcm-microencapsulation]] — MEPCM form factor enabling AM processing
- [[n-alkanes-as-pcm]] — paraffin PCM material properties used in FFF composites
