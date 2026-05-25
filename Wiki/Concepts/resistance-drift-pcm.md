---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/bruns-2012-electronic-switching-pcm.md"
source_count: 1
aliases:
  - "resistance drift"
  - "drift effect"
---

# Resistance Drift in PCMs

**Resistance drift** is the spontaneous, time-dependent increase of electrical resistivity in amorphous phase-change materials, occurring even without an applied field.

## Phenomenology

Resistivity follows a power law over time:

> R(t) ∝ t^ν

where ν is the **drift exponent** (material- and condition-dependent).

Drift is an intrinsic property: Bruns 2012 demonstrated that the drift behavior is identical in unstructured as-deposited amorphous films and in actual PCRAM memory cells.

## Physical Origin

The exact origin is not fully understood. Structural relaxation of the amorphous network is the leading hypothesis. Key findings from Bruns 2012:

- Drift exponent ν correlates with the **activation energy for conduction E_A**
- A new functional dependence of drift energy on E_A was identified
- This allows improvement of existing phenomenological drift models

## Impact on Multilevel Storage

- **Multilevel PCRAM** stores >1 bit/cell using intermediate resistance states between SET and RESET
- Drift shifts these intermediate resistances upward with time
- A state initially written at resistance R₁ may drift into the R₂ window → misread
- Current compensation approaches (Papandreou et al.) extend correct readout to weeks only; long-term multilevel storage remains unsolved

## Why It Matters

- Single-level PCRAM (1 bit/cell): drift is less critical — large resistance contrast between SET and RESET makes occasional drift tolerable
- Multilevel PCRAM (≥2 bits/cell): drift is a primary reliability concern
- Also relevant for PCM-based analog/neuromorphic computing where precise resistance levels are needed

## Related Notes

- [[threshold-switching-pcm]] — another amorphous-phase electrical phenomenon
- [[pcm-memory-switching-speed]] — the switching operations that create the amorphous states that then drift
- [[phase-change-materials]] — parent topic
