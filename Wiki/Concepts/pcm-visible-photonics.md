---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/Prof Robert Simpson From data storage to programmable photonics.md"
source_count: 1
aliases:
  - "visible PCM"
  - "wide-bandgap PCM"
  - "programmable metamaterials"
---

# PCMs for Visible Photonics

Conventional data-storage PCMs (GST, AIST) have bandgaps < 0.7 eV, making them opaque across the entire visible spectrum. Visible-wavelength metamaterials and holography require PCMs with bandgaps > ~1.5 eV — a completely different material class from optical storage PCMs.

## Why Conventional PCMs Fail at Visible Wavelengths

- Data-storage PCMs (GST, AIST): designed to **absorb** visible laser pulses to heat up and switch → inherently absorbing at visible wavelengths.
- In transmissive metamaterials for beam steering, holography, or color displays: **absorption is unwanted** — want to control the **phase** (real part of refractive index) of transmitted light, not its amplitude.
- Visible light requires material bandgap > photon energy > ~1.5 eV (i.e., > 800 nm wavelength).
- Telluride-based PCMs (Te, GeTe, GST): small bandgaps (~0.5 eV) → opaque throughout visible.

## Application Requirements vs. Data Storage Requirements

| Property | Data Storage | Visible Photonics / Holography |
|----------|-------------|-------------------------------|
| Amorphous stability | Decades | Minutes to days (displays) |
| Switching cycles | > 10⁶ | > 10³–10⁶ |
| Key contrast | Reflectance (Δk) | Phase (Δn, real part) |
| Absorption at target λ | High (to absorb laser) | **Near zero** |
| Multi-state | Binary preferred | Analog / multi-level preferred |
| Bandgap | Any | > 1.5 eV |

## Wide-Bandgap PCM Candidates

Moving up the chalcogenide periodic table (Te → Se → S) opens up the bandgap:
- Tellurides: ~0.5 eV (opaque)
- Selenides: ~1.0 eV (partially absorbing at visible)
- **Sulfides: ~1.5 eV** (transparent above ~600 nm)

**[[Sb2S3]]** (antimony trisulfide) is currently the leading candidate:
- Widest bandgap of any PCM (~1.5 eV); transparent above ~600 nm
- Refractive index ~3 (amorphous) → ~4 (crystalline) in near-IR
- Challenges: growth-dominated crystallization, birefringence, smaller Δn than GST

## Historical Context

- **Ovshinsky (1968)**: electrical switching in Telluride PCMs.
- **1990s**: Optical rewritable discs (Matsushita/Panasonic).
- **2000s**: PCRAM (Intel Optane); research oscillates between electrical and optical.
- **2011**: Simpson group (SUTD Singapore) — PCM-tuned silicon ring resonators and plasmonic waveguides.
- **2012**: First PCM metamaterial papers (simulation; SUTD and Wuttig/Aachen groups).
- **2006**: Ovshinsky's company (ECD) described beam-steering device concept using GST-like material at 1550 nm.
- **2016**: Zheludev group — laser-written Fresnel zones in GST for focusing.
- **2023**: Simpson group — Sb₂S₃ hyperbolic metamaterials, nanohole beam steering at ~700 nm.

## Metal Compatibility for PCM Metamaterials

When building metal/PCM heterostructures (resonators, plasmonic arrays), metal choice is critical:

| Metal | Reaction with GST | Tm (°C) | Assessment |
|-------|-----------------|---------|-----------|
| Al | Immediate reaction | 660 | ✗ — forms alloy |
| Ag | Reacts | 962 | ✗ — diffuses into GST |
| W | Mostly stable | 3422 | ✓ Better |
| Au | Minor interface reaction | 1064 | ✓ Good but not ideal with thin GST |
| **TiN** | No reaction | 3000 | **✓ Best** — standard PCRAM electrode, plasmonic in visible |

TiN is the preferred material because it: (1) does not react with GST even at switching temperatures, (2) has plasmonic response in the visible similar to gold, (3) melting point 3000 °C (far above GST switching temperatures), (4) is the standard electrode in PCRAM.

## Beam Steering and Programmable Meta-surfaces

Goal: phase-array of PCM-loaded resonators that can steer a laser beam to arbitrary angles.
- Requires control of **resonant frequency** (phase shift per meta-atom) rather than just absorption.
- Needs adequate Δn with near-zero absorption → wide-bandgap PCMs.
- Precedent: ECD (2006) described 8-element beam steering array using GST-like material; ~2° deflection, ~10° theoretical maximum.
- Current work: nanohole arrays in Sb₂S₃-loaded structures at ~700 nm.

## Related Concepts

- [[Sb2S3]] — leading wide-bandgap PCM candidate
- [[pcm-crystal-structure-bonding]] — why telluride PCMs have small bandgaps (p-bonding metallic character)
- [[pcm-material-design-rules]] — how to find new PCMs for specific wavelength ranges
- [[plasmonic-pcm]] — IST: the opposite extreme (metallic crystalline phase with ε′ < 0)
- [[optical-programming-pcm-nanostructures]] — IST-based direct laser writing in metallic nanostructures
