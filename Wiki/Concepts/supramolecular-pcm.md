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
source_count: 1
aliases:
  - "SPCM"
  - "supramolecular phase change material"
  - "self-healing PCM"
---

# Supramolecular Phase Change Materials (SPCMs)

An advanced class of [[latent-heat-pcm-thermal-storage|thermal PCM]] where the phase change and energy storage are governed by dynamic, reversible non-covalent interactions within a polymer network, rather than simple melting of individual molecules. SPCMs represent a paradigm shift that simultaneously addresses the classical limitations of conventional PCMs: leakage, low thermal conductivity, and mechanical weakness.

## Core Concept

Conventional PCMs (paraffins, fatty acids, salt hydrates) store and release energy via a macroscopic solid–liquid phase transition. The critical challenge is that the liquid state flows, causing leakage.

SPCMs use **non-covalent interactions** (hydrogen bonds, π–π stacking, metal–ligand coordination, van der Waals forces) to:
1. Create a supramolecular polymer network that retains shape even when constituent molecules are mobile.
2. Enable **isostructural phase transitions**: significant thermal energy storage/release without macroscopic change of physical state (no flowing liquid).
3. Confer **self-healing capability** from reversible bond reformation.
4. Allow **reprocessability** (not thermally set).

## Nucleobase-Derived SPCMs

A leading platform uses adenine-functionalised poly(propylene glycol) (BA-PPG) — adenine is a nucleobase capable of self-complementary hydrogen bonding:

- BA-PPG self-assembles into spherical micelles in aqueous solution via adenine–adenine H-bonding.
- Micelle size: 124 nm (pure BA-PPG), expanding to 385 nm with pyrene loading (PDI = 0.13).
- Solid-state SAXS: long-period peak at q = 2.1 nm⁻¹ (d = 2.99 nm) from PPG segment spacing + adenine H-bonded dimers.
- With hydrophobic guest loading (e.g., pyrene): peak shifts to q = 1.9 nm⁻¹; scattering at 1:√7 ratio confirms hexagonally packed cylindrical phase.

**BA-PPG/Ag composite (CPCSM)**:
- ΔHm = 254.07 J g⁻¹, ΔHcr = 235 J g⁻¹ — high latent heat for a supramolecular system.
- Tm_onset = 87.80°C, Tm_peak = 110.47°C.
- Ag NPs (10–18 nm) encapsulated with 82.65% efficiency via electrostatic interactions / electron transfer.
- Heat capacity CPCSM = 2.31 J g⁻¹ °C (vs. 1.02 for PCSM alone).
- Ag NPs enhance mechanical strength and thermal stability without disrupting reversible H-bonding.

## Boron Nitride / APPG Hybrids

- APPG (adenine-functionalised PPG) exfoliates h-BN nanosheets by sonication + noncovalent functionalisation.
- Few-layer BNNSs: 2.0–3.5 nm thick; lateral size 0.1–0.5 µm; hexagonal structure confirmed by SAED (lattice spacing 0.32 nm).
- BN/APPG/Ag hybrid: Ag NPs (uniform size, distinguishable from h-BN by contrast) deposited on BN/APPG via N–Ag bonds (nitrogen from adenine).
- BN incorporation: shifts phase transition temperature; increases thermal stability, shape retention, and leakage prevention proportionally; does not disrupt A-PPG self-assembly.
- Composites show consistent melting points across weight ratios; enthalpy increases with A-PPG content.

## Solid-Solid SPCMs

Solid–solid PCMs avoid liquid-phase leakage entirely by using crystalline–amorphous transitions instead of solid–liquid:

- **PEG with silanol end groups**: self-cross-linking through Si–OH hydrogen bonds → solid–solid phase change (crystalline ↔ amorphous PEG) without liquefaction.
- **PEG4K-Bx-PEG6K** (boroxine + H-bond network): tensile strength ~22.90 MPa, strain ~733.62%; directional thermal conductivity 3.639 W m⁻¹ K⁻¹ with only 5 wt% graphene nanosheets (GNs); self-healing and reprocessable.
- Cross-linked PEG copolymer network: ΔH = 156.8 J g⁻¹; stable after 500 cycles; unchanged after 12 h at 120°C; tensile strength 6.6–11.0 MPa.

## Healable Supramolecular PCPs

Poly(4-vinylpyridine) backbone + stearic acid side chains + polypyrrole (PPy):
- Dynamic hydrogen-bonding network.
- Anti-leakage capability.
- Long-term stability: 111.5 J g⁻¹ maintained after 1000 solar irradiation cycles.

## Advantages Over Conventional PCMs

| Property | Conventional PCM | Supramolecular PCM |
|----------|-----------------|-------------------|
| Leakage | Major issue | Eliminated or greatly reduced |
| Thermal conductivity | Low | Tunable with nanofillers |
| Self-healing | None | Possible (dynamic bonds) |
| Reprocessability | Generally no | Yes (reversible crosslinks) |
| Latent heat | High (150–250 J g⁻¹) | Competitive (111–254 J g⁻¹) |
| Mechanical strength | Weak (liquifies) | Strong (6–23 MPa tensile) |
| Cycling stability | 100–500 cycles typical | 500–1000 cycles demonstrated |

## Key Challenge: TES Capacity vs. Mechanical Strength Trade-Off

A persistent challenge: achieving simultaneously high latent heat capacity and robust mechanical strength. Chemical cross-linking or ionic interactions that provide mechanical strength often reduce crystallinity and latent heat. SPCMs partially overcome this by using dynamic bonds that are strong enough mechanically but reversible enough to preserve phase change.

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — conventional PCM fundamentals
- [[pcm-thermal-conductivity-enhancement]] — nanofillers for enhanced conductivity in composites
- [[pcm-microencapsulation]] — alternative leakage-prevention strategy
