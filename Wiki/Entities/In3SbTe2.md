---
tags:
  - "entity"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/conrads-2025-ist-review.md"
source_count: 1
aliases:
  - "IST"
  - "In3SbTe2"
  - "In₃SbTe₂"
---

# In3SbTe2 (IST)

In3SbTe2 (IST) is a plasmonic phase-change material (PCM) from the In–Sb–Te ternary system. Its crystalline phase is metallic with negative permittivity across the entire infrared — a sharp contrast to conventional dielectric PCMs.

## Description

IST was originally introduced for data-storage technology (Maeda et al., 1988) and for PCRAM applications. It was introduced into nanophotonics in 2021 (Heßler et al., Nat. Commun.) when its metallic crystalline permittivity was exploited to directly program plasmonic nanostructures.

## Key Attributes

| Property | Amorphous | Crystalline |
|----------|-----------|-------------|
| Permittivity ε′ (infrared) | ≈ +14 (constant) | < 0 (Drude-like) |
| Plasma frequency | — | 11111 cm⁻¹ (900 nm) |
| Thermal conductivity (W/(K·m)) | 0.4–0.5 | 23 |
| Density (g/cm³) | 6.1 | 6.75 |
| Electrical conductivity | — | ~10⁴ S/cm |

- **Crystal structure**: cubic rocksalt, lattice parameter a = 6.126 Å
- **Bonding type**: "bad metal" (QTAIM classification) — stronger electron delocalization than metavalent PCMs, weaker than true metals
- **Crystallization**: growth-dominated; may proceed via InSb + InTe intermediates (~300°C / ~420°C) or directly to ternary phase (~250°C, film-thickness dependent)
- **Non-volatile**: phase persists after cooling, unlike VO₂

## Optical Switching (660 nm laser, ~1 µm² spot)

| Parameter | Crystallization | Reamorphization |
|-----------|-----------------|-----------------|
| Power (mW) | 5–60 | 160–250 |
| Pulse duration | 200–2000 ns | 15–30 ns |
| Pulses required | 2–100 | 1 |

## Nanophotonic Applications

- **Antenna programming**: direct laser writing of rod antennas, SRRs, slit antennas with arbitrary shapes
- **Emissivity shaping**: grating-based perfect absorbers and Fabry-Perot multilayer emitters
- **Beam shaping**: geometric phase metasurfaces for beam steering, lensing, vortex beams, holography at 9 µm
- **Polariton control**: SPhP resonators on SiC (confinement λ/35), hyperbolic polaritons in hBN, ghost polaritons in calcite

## Related Notes

- [[plasmonic-pcm]] — concept explaining IST's unique dielectric-to-metallic switch
- [[optical-programming-pcm-nanostructures]] — how laser pulses create IST antennas
- [[phase-change-materials]] — parent topic
