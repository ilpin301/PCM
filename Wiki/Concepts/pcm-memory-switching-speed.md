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
  - "PCM SET speed"
  - "nanosecond switching PCM"
---

# PCM Memory Switching Speed

Memory switching in PCMs — the phase transition between amorphous (RESET) and crystalline (SET) states — can occur on nanosecond timescales, making PCRAM competitive with DRAM.

## Key Result (Bruns 2012)

- **GeTe** memory cells demonstrated crystallization (SET) within a **few nanoseconds**
- This matches or approaches DRAM access times (typically 10–100 ns)
- Measured using a custom pulsed electrical tester (PET) with sub-nanosecond resolution

## SET vs. RESET Timescales

| Operation | Mechanism | Speed |
|-----------|-----------|-------|
| SET (crystallization) | Moderate pulse → heat above T_crys; growth of crystalline phase | Nanoseconds (GeTe) |
| RESET (amorphization) | High pulse → melt above T_melt + quench | Nanoseconds (fast quench required) |

Quench rate requirement: ~100 K/ns → demands small PCM volumes and small heater contact area (< 100 nm diameter).

## Material Dependence

| Material | Crystallization | Notes |
|----------|-----------------|-------|
| GeTe | Growth-dominated | Fastest (~ns); needs crystalline rim present |
| Ge₂Sb₂Te₅ (GST) | Nucleation-limited | Slower; smoother transition |
| AIST | Nucleation-dominated | Different kinetics; also fast |

Growth-dominated PCMs (GeTe) recrystallize fastest once a crystalline boundary exists (e.g., at the heater-PCM interface in a mushroom cell).

## Design Implications for Fast Switching

- Bottom electrode (heater) < 100 nm diameter → high current density from small supply voltage (< 3.7 V)
- Small amorphous plug volume → faster quench, lower programming energy
- Threshold switching enables SET from high-resistance RESET state at practical voltages
- Multilevel storage trades SET speed for increased state resolution

## Related Notes

- [[threshold-switching-pcm]] — precursor effect that enables low-voltage SET operation
- [[resistance-drift-pcm]] — consequence of amorphous state; limits multilevel storage
- [[phase-change-materials]] — parent topic
