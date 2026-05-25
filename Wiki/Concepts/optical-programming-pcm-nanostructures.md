---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/conrads-2025-ist-review.md"
source_count: 1
aliases:
  - "direct laser writing IST"
  - "optical programming IST"
---

# Optical Programming of PCM Nanostructures

**Optical programming** refers to using focused laser pulses to locally switch a PCM film between its amorphous and crystalline states — directly writing or erasing nanoscale structures without conventional lithography.

## Concept

For the [[plasmonic-pcm]] [[In3SbTe2]] (IST):
- A focused 660 nm laser crystallizes IST spots → metallic patches appear in the amorphous film
- These metallic patches function as infrared plasmonic antennas, rods, SRRs, slit structures, etc.
- Reamorphization (high-power short pulse) erases the metallic structure → film returns to dielectric

The approach replaces time-consuming electron-beam lithography and etching with a single-day design-fabricate-characterize cycle.

## Switching Parameters (660 nm laser, ~1 µm² spot)

| Step | Power | Duration | Pulses |
|------|-------|----------|--------|
| Crystallization | 5–60 mW | 200–2000 ns | 2–100 |
| Reamorphization | 160–250 mW | 15–30 ns | 1 |

Multiple crystallization pulses needed because IST crystallization is growth-dominated — requires nuclei/defects to start.

## Layer Stack (typical)

CaF₂ substrate → 50 nm amorphous IST → 70 nm capping layer (oxidation protection)

## Applications Demonstrated

- **Rod antennas**: electric dipole resonances at ~5 µm; TFOM up to 2.0 for slit antennas
- **Split-ring resonators (SRRs)**: combined crystallization + reamorphization to carve openings; magnetic dipole resonance added/removed
- **Dual-layer metasurfaces**: two IST layers separated by Ge; individual control from top and bottom through substrate
- **Geometric phase metasurfaces**: rotated IST rod antennas programmed across cm²-scale area; beam steering, lensing (f = 11.5 cm at 9 µm), vortex beams, holography
- **Emissivity control**: IST grating bars above gold mirror; large-area thermal image encoding
- **Polariton resonators**: IST on SiC programs SPhP resonators; IST below hBN tunes hyperbolic polaritons

## Comparison to Conventional PCM Photonics

| Aspect | Dielectric PCM (GST) | Plasmonic PCM (IST) |
|--------|----------------------|---------------------|
| What changes | Refractive index around pre-patterned antenna | The antenna itself |
| Patterning needed | Yes (antenna must be lithographed first) | No (write directly into blank film) |
| Tuning range | ~1 resonance width (TFOM ≈ 1) | Unlimited (TFOM ≥ 2) |
| Post-fabrication tuning | Shape cannot change | Shape can be extended, shortened, erased |

## Related Notes

- [[plasmonic-pcm]] — why crystalline IST is metallic
- [[In3SbTe2]] — material properties
- [[phase-change-materials]] — parent topic
