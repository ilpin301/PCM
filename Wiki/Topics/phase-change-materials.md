---
tags:
  - "topic"
topics: []
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/conrads-2025-ist-review.md"
  - "Raw/Sources/bruns-2012-electronic-switching-pcm.md"
  - "Raw/Sources/wuttig-yamada-2007-pcm-review.md"
  - "Raw/Sources/adams-2025-firstprinciples-pcm-thermo.md"
  - "Raw/Sources/Phase-change memory and switching materials.md"
  - "Raw/Sources/Prof Robert Simpson From data storage to programmable photonics.md"
  - "Raw/Sources/Are Phase Change Materials the Future of Water Heaters.md"
  - "Raw/Sources/Cooling AI How Phase Change Materials Make a Difference.md"
source_count: 8
aliases:
  - "PCMs"
  - "phase change materials"
---

# Phase-Change Materials

Phase-change materials (PCMs) switch reversibly between an amorphous and a crystalline phase. The two phases differ dramatically in resistivity, reflectance, and optical permittivity — all of which can be exploited for data storage and active photonics.

## Overview

The amorphous phase lacks long-range order; conduction is by thermally activated hopping transport (R ∝ exp(E_A/k_BT)). The crystalline phase has periodic atomic order and typically metallic or semi-metallic conduction. The resistivity contrast between phases can reach several orders of magnitude.

Switching is a first-order phase transition driven by heat:
- **Crystallization (SET)**: heat above T_crys; atoms rearrange into the energetically favorable crystalline lattice.
- **Amorphization (RESET)**: heat above T_melt, then rapidly quench; liquid state is "frozen" into disorder.

Both phases are (meta-)stable at room temperature for years to decades. Switching can occur in nanoseconds.

## Key Concepts

- [[plasmonic-pcm]] — IST switches to a metallic crystalline phase (ε′ < 0), unlike conventional dielectric PCMs.
- [[threshold-switching-pcm]] — Electrical field-induced transient conductivity increase in amorphous PCMs.
- [[resistance-drift-pcm]] — Time-dependent resistance increase in amorphous phase; limits multilevel storage.
- [[pcm-memory-switching-speed]] — Nanosecond SET times make PCRAM competitive with DRAM.
- [[optical-programming-pcm-nanostructures]] — Direct laser writing of metallic nanostructures in IST films.

## Common PCM Materials

| Material | Type | Notes |
|----------|------|-------|
| GeTe | Growth-dominated | Fastest known SET (ns); studied by Bruns 2012 |
| Ge₂Sb₂Te₅ (GST) | Nucleation-limited | Standard PCM; smoother crystallization transition |
| AIST (AgIn-doped Sb₂Te) | Nucleation-dominated | Competing fast PCM |
| In₃SbTe₂ (IST) | Plasmonic ("bad metal") | Metallic crystalline phase; unique for nanophotonics |
| [[Sb2S3]] | Wide-bandgap | Transparent in visible (> 600 nm); for visible photonics |
| Elemental Te | Selector switch | Crystal = semiconductor, liquid = metal; volatile switching |

## Applications

- **Optical data storage**: CD, DVD, Blu-ray (reflectance contrast)
- **Electronic memory (PCRAM)**: resistivity contrast; non-volatile, fast
- **Active nanophotonics**: see [[In3SbTe2]] for IST-specific applications; [[pcm-visible-photonics]] for visible wavelengths
- **Thermal energy storage**: distinct domain — see [[latent-heat-pcm-thermal-storage]]

## Key Concepts (Extended)

- [[pcm-crystal-structure-bonding]] — p-orbital bonding, rocksalt structure, umbrella flip, hyper-bonded seesaw units
- [[pcm-material-design-rules]] — Wuttig–Yamada empirical rules + Adams et al. thermodynamic screening
- [[pcm-crystallization-ostwald-rule]] — Two-step RS→hex pathway, Trg ≈ 0.5, nucleation vs. growth regimes
- [[ml-potentials-pcm-simulation]] — GAP/ACE machine-learned potentials for device-scale GST and Te simulations
- [[pcm-visible-photonics]] — Wide-bandgap PCMs for visible metamaterials; metal compatibility; TiN preferred

## Sources

- [[conrads-2025-ist-review]] — IST optical properties and nanophotonic applications
- [[bruns-2012-electronic-switching-pcm]] — Electronic switching: speed, threshold switching, resistance drift
- [[wuttig-yamada-2007-pcm-review]] — Crystal structure, bonding, optical contrast origin, design rules
- [[adams-2025-firstprinciples-pcm-thermo]] — Ostwald-rule DFT screening of ternary chalcogenides
- [[Phase-change memory and switching materials]] — Elliott: ML-IPs, device-scale GST, Te chiral crystallization
- [[Prof Robert Simpson From data storage to programmable photonics]] — Metal compatibility, Sb₂S₃, visible photonics
- [[Are Phase Change Materials the Future of Water Heaters]] — Thermal latent-heat PCMs for residential use
- [[Cooling AI How Phase Change Materials Make a Difference]] — PCM-TES for data centre cooling (SINTEF La-Flex)
