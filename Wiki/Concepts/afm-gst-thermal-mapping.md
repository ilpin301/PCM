---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/protocol-for-nanoscale-thermal-mapping-of-electronic-devices-using-atomic-force.md"
source_count: 1
aliases:
  - "GST thermal mapping"
  - "nanoscale thermometry AFM"
  - "phase-change thermometry"
---

# AFM-GST Nanoscale Thermal Mapping

**AFM-GST thermal mapping** is a nanoscale thermometry technique that exploits the **density change of Ge₂Sb₂Te₅ (GST)** during its amorphous-to-crystalline phase transition to image temperature fields in operating microelectronic devices, with spatial resolution down to ~20 nm.

The key insight: amorphous GST sputtered as a thin (~20 nm) coating on a device will crystallize (and shrink in thickness by ~1 nm) only where the local temperature exceeds the glass-transition temperature T_g. AFM then reads the resulting topographic step as a T_g isotherm. Multiple isotherms are built up by varying either heater power or heating time.

## Operating Principle

1. **GST coating** — ~20 nm amorphous GST is sputter-deposited on the device at ~5 nm/min in high vacuum (~10⁻⁶ torr). Film must have sharp edges for accurate thickness reference. The film is thin enough to negligibly perturb device heat transfer.
2. **Tg calibration** — GST-coated silicon wafer heated at known temperatures (300 s dwell); AFM measures thickness reduction. Tg is identified from the onset of thickness reduction. For the protocol's sputtered GST: Tg = 149 °C at 300 s dwell. Heating history shifts Tg slightly (Arrhenius process with activation energy ~2.6 eV: longer dwell → lower effective Tg).
3. **Thermal mapping by varying heater power** — device heater stepped through increasing powers Pi. AFM images after each step capture the crystallized contour (thickness reduction) corresponding to the Tg isotherm. Temperature at each earlier contour is scaled linearly with applied power:
   `Ti = (Tg − RT) × (Pi / Po) + RT`
4. **Thermal mapping by varying heating time** — fixed power P0, varying dwell time ti. Shorter dwell times require higher temperatures to crystallize, following Arrhenius:
   `Ti = [−kB/EA × (ln(1/ti) − ln(1/tref)) + 1/Tg]⁻¹`
   where EA ≈ 2.6 eV.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Spatial resolution | ~20 nm (GST grain size limited) |
| Film thickness | ~20 nm GST |
| Tg (sputtered GST, 300 s) | 149 °C |
| Minimum detectable thickness change | ~1 nm |
| Temperature uncertainty from heating history | ~2 K at Tg |
| Working temperature range | > 149 °C (adjustable via composition) |

## Limitations

- Only resolves temperatures **above Tg** (~149 °C for standard GST). For lower working temperatures, alternate GeSbTe compositions or polymers must be used.
- Multiple crystallization steps alter the GST phase history → temperature steps must be kept >10 K to minimize cumulative error.
- Technique resolves only the thermal state at the moment of maximum applied temperature; it does not track transient events.

## PCM Relevance

GST's phase-transition thermometry is used here as a **measurement tool** rather than the memory medium itself. The protocol demonstrated temperature mapping of magnetic recording heads with embedded nano-heaters, but is directly applicable to PCM device characterization: the same GST film that stores data in memory can serve as an integrated thermometer in test structures, with AFM reading out the phase-change boundary.

See [[scanning-probe-microscopy]] for AFM fundamentals. See [[pcm-crystal-structure-bonding]] and [[threshold-switching-pcm]] for the GST material properties exploited here.

## Related Concepts

- [[scanning-probe-microscopy]] — AFM platform used for thickness readout
- [[phase-change-materials]] — parent topic
- [[pcm-crystal-structure-bonding]] — GST phase-transition physics
- [[threshold-switching-pcm]] — PCM switching and heating during programming

## Sources

- Cheng et al. (2024), *STAR Protocols* via PMC11068603 — step-by-step protocol for GST-based nanoscale thermal mapping of electronic devices using AFM.
