---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/multifunctional-electrospun-phase-change-material-mats-for-solarthermal-energy-s.md"
source_count: 1
aliases:
  - "electrospun PCM fibers"
  - "PPCM mats"
  - "photothermal PCM textiles"
---

# Electrospun PCM Mats for Solar-Thermal Energy Storage

Electrospinning of polymer/PCM blends produces flexible, bead-free nanofibrous mats capable of simultaneously storing thermal energy (via latent heat) and converting solar irradiation to heat (photothermal conversion). This concept integrates [[latent-heat-pcm-thermal-storage|TES]] with fibre-form factors for smart textiles, flexible solar collectors, and thermal management.

## Polyester-Based PCMs (PPCMs)

The core PCMs in this work are linear aliphatic polyesters synthesised by polycondensation of diols and diacids. Chain-length nomenclature: PPCM_diol-chain_diacid-chain_.

| Material | Diol (carbons) | Diacid (carbons) | Tm (°C) | Tc (°C) | ΔHm (J g⁻¹) | Supercooling ΔT (°C) |
|----------|---------------|------------------|---------|---------|-------------|----------------------|
| PPCM1010 | 10 | 10 | 76.2 | 61.6 | 123 | 14.6 |
| PPCM1212 | 12 | 12 | ~85 | ~72 | ~140 | ~13 |
| PPCM1218 | 12 | 18 | 90.6 | 80.9 | 157 | 9.7 |

PPCM1218 was selected for electrospinning: highest latent heat (157 J g⁻¹) and lowest supercooling — comparable to decanoic acid (~160 J g⁻¹) and PEG4000 (150–170 J g⁻¹).

Higher chain length → stronger van der Waals interactions → higher Tm and ΔH; lower supercooling.

## Electrospun Mat Architecture

**Matrix polymer**: polyamide 11 (PA11) — fully biobased aliphatic PA; excellent electrospinnability; amide groups form hydrogen bonds with PPCM ester C=O and –OH end groups, enhancing dispersion.

**Designations**:
- `ePPCM50`: 50 wt% PPCM1218 / 50 wt% PA11 — continuous bead-free fibres.
- `ePPCM85`: 85 wt% PPCM1218 / 15 wt% PA11 — slightly rougher surface but still bead-free.

No phase separation between PA11 and PPCM visible in SEM, indicating good compatibility.

## Thermal Storage Performance

| Sample | ΔHm (J g⁻¹) | ΔHc (J g⁻¹) | Tm (°C) |
|--------|-------------|-------------|---------|
| PPCM1218 (bulk) | 157 | — | 90.6 |
| ePPCM50 | 77 | 74 | ~90 |
| ePPCM85 | 132 | 126 | 90.1 |

ePPCM85 retains 84% of PPCM1218 latent heat — high loading preserved. Transition temperatures essentially unchanged after blending, confirming no PCM–polymer disruption.

## Photothermal Functionalisation

Three additives were tested on ePPCM85:

| Filler | Code | Electrical conductivity | Thermal conductivity | Notes |
|--------|------|------------------------|---------------------|-------|
| 10 wt% Biochar | BC@ePPCM85 | ~1.8 µS m⁻¹ (unchanged) | 0.22 W m⁻¹ K⁻¹ | Modest improvement |
| 10 wt% Graphene | Gr@ePPCM85 | 4.5 µS m⁻¹ | 0.27 W m⁻¹ K⁻¹ | Some bead formation; limited percolation |
| PPy surface coating | PPy@ePPCM85 | **18.5 S m⁻¹** | **0.51 W m⁻¹ K⁻¹** | Best performance; in situ polymerisation on fibres |

PPy polymerisation occurred both on fiber surfaces and within fibre interiors (dual localisation confirmed by SEM cross-section + EDX nitrogen mapping), creating a continuous conductive network.

## Solar-to-Thermal Performance

Under 1.5 sun irradiation (300 s on, 300 s off):
- **PPy@ePPCM85** surfaces exceeded 90°C — fully melting the PCM; stable over 100 photothermal cycles.
- PA11 and BC/Gr mats showed lower temperatures; PPy provided the strongest solar absorption.

Applications leveraged: solar-driven water purification, wearable thermal regulation, flexible solar collectors.

## Thermal Durability

PPy@ePPCM85 over 100 DSC heating–cooling cycles: transition temperatures and enthalpy values unchanged — no degradation. Leakage test at 120°C for 2 h: no leakage or deformation of the mat vs. complete melting of bulk PPCM85. PA11 matrix effectively prevents melt flow.

## Mechanical Properties

Higher PPCM loading reduces tensile strength:
- ePPCM50: modulus 37 MPa, strength 2.27 MPa.
- ePPCM85: modulus 29 MPa, strength 1.64 MPa.
- BC/Gr addition stiffens matrix (modulus 97–105 MPa) with modest strength gain.
- PPy: moderate stiffening (+25% modulus vs. ePPCM85).

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — underlying TES principles
- [[pcm-thermal-conductivity-enhancement]] — conductivity strategies; PPy/graphene as additives
- [[pcm-microencapsulation]] — alternative form-stabilisation strategy
