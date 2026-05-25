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
  - "threshold switching"
  - "Ovshinsky effect"
---

# Threshold Switching in PCMs

**Threshold switching** is a transient, reversible drop in electrical resistivity that occurs in amorphous PCMs when the applied electric field exceeds a threshold value. It is distinct from memory switching (which causes a permanent phase transition).

## Mechanism

Discovered by Ovshinsky (1968). Two competing model classes exist:

1. **Electronic models**: exponential increase in carrier generation/recombination rate above the threshold field → more conduction carriers → resistivity drop. No change in atomic order.
2. **Nucleation models**: reversible local atomic rearrangement toward a crystalline-like structure is induced by the field.

Experimental evidence in this thesis (Bruns 2012) is consistent with electronic models, but the debate continues.

## Phenomenology

- **OFF state** (sub-threshold): ohmic I–V curve; high amorphous resistivity
- **Threshold field E_th**: when E_applied ≥ E_th, dynamic resistance collapses (snap-back) → ON state
- **ON state**: high conductivity; similar resistance to crystalline (SET) state but material is still amorphous
- **Holding voltage U_h**: minimum voltage to maintain ON state; below U_h, material returns to OFF state

## Key Finding (Bruns 2012)

Prior literature described threshold switching by a single material-specific threshold field E_th. This work measured a **field-dependent delay time τ_d**:
- At fields just above E_th, delay time τ_d is long
- At higher fields, τ_d decreases
- τ_d predicts *when* the conductivity drop occurs, not just *whether* it occurs

The threshold switching itself occurs on sub-nanosecond timescales once triggered.

## Role in PCRAM

Threshold switching is essential for practical PCRAM operation:
- Amorphous RESET state resistance can be several MΩ; direct SET requires very high voltages
- Threshold switching temporarily drops resistance to near-SET levels at supply-compatible voltages (< 3.7 V)
- The transient ON state enables the SET current to flow and recrystallize the amorphous volume

## Related Notes

- [[resistance-drift-pcm]] — another amorphous-phase effect in PCMs
- [[pcm-memory-switching-speed]] — the memory switching that follows threshold switching
- [[phase-change-materials]] — parent topic
