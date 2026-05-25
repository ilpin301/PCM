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
  - "plasmonic phase-change material"
---

# Plasmonic PCM

A **plasmonic PCM** is a phase-change material whose crystalline phase has a negative real permittivity (ε′ < 0), giving it metallic (plasmonic) character. This contrasts with conventional "dielectric PCMs" (e.g., GST alloys), where both phases have positive permittivity.

## Distinction from Dielectric PCMs

| Property | Dielectric PCMs (GST) | Plasmonic PCM (IST) |
|----------|-----------------------|---------------------|
| Amorphous ε′ | Positive (~12) | Positive (~14) |
| Crystalline ε′ | Positive (~36) | **Negative** (Drude-like) |
| Antenna tuning mechanism | Δn_eff around fixed antenna | Change antenna *size and shape* |
| Max TFOM (antenna tuning) | ~1 | ≥2 |
| Bonding (crystalline) | Metavalent | Bad metal |

## Physical Origin

In conventional dielectric PCMs, crystallization increases atomic density → higher background permittivity (Clausius-Mossotti). The additional large increase in GST is due to metavalent bonding: delocalized electrons increase polarizability.

IST is classified as a "bad metal" in the QTAIM bonding map — even stronger electron delocalization than metavalent PCMs. The resulting high free carrier density drives Drude-like behavior: ε′(ω) < 0 for ω < ω_plasma (infrared, below 11111 cm⁻¹ / 900 nm).

## Consequences for Nanophotonics

Because crystalline IST is metallic, directly crystallized IST spots *become* the antenna — not a refractive index modifier around a pre-existing antenna. This enables:

1. **Direct programming**: crystallize an arbitrary shape in amorphous IST film → instant plasmonic nanostructure
2. **Erasure**: reamorphize with a high-power short pulse → structure disappears
3. **Unlimited tuning range**: antenna length can be extended/shortened arbitrarily (not limited by fixed Δn_eff)

## Key Material

The only plasmonic PCM experimentally demonstrated for nanophotonics to date: **[[In3SbTe2]]** (IST).

## Non-volatility

The plasmonic state persists after the material is cooled down — unlike VO₂, which is a volatile insulator-to-metal transition material (reverts to insulating below 68°C) and cannot serve as a permanent template for nanostructures.

## Related Notes

- [[In3SbTe2]] — the specific plasmonic PCM
- [[optical-programming-pcm-nanostructures]] — application of the plasmonic property
- [[phase-change-materials]] — parent topic
