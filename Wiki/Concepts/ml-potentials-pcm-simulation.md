---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/Phase-change memory and switching materials.md"
source_count: 1
aliases:
  - "machine-learned potentials"
  - "GAP potential"
  - "ACE potential"
  - "ML-IP"
---

# Machine-Learned Potentials for PCM Simulation

Machine-learned interatomic potentials (ML-IPs) bridge the gap between expensive ab initio DFT (accurate but slow, limited to ~500 atoms) and fast but inaccurate empirical force fields. Applied to GST and elemental Te, they enable device-scale, DFT-accurate simulations of phase-change dynamics.

## Motivation

Understanding glassy/amorphous PCMs requires atomistic simulation because:
- Crystal structure is uniquely defined; glass structure must be described statistically.
- Rare events (nucleation, chiral switching) require large atom counts to observe in statistically meaningful numbers.
- Device dimensions (20–100 nm) require hundreds of thousands to millions of atoms.

Before ML-IPs (~2018): DFT limited to ~500 atoms, taking months on supercomputers. This is a fundamental barrier to understanding amorphous GST and device-scale crystallization.

## How ML-IPs Work

1. **Training set**: thousands to tens of thousands of small DFT calculations across diverse configurations (liquid, amorphous, crystal, many compositions).
2. **Structural descriptor**: local atomic environment described by a feature vector (e.g., SOAP for GAP, ACE basis). Spatial cutoff (~10 Å) → **linear scaling** (double atoms = double time).
3. **Fitting**: Gaussian process regression (GAP) or linear regression on ACE basis maps local structure to DFT energy.
4. **Output**: atomic energies (not directly observable but computable); total energy, forces, stresses — all DFT-accurate.
5. **Limitation**: no direct electronic information (no wavefunctions); electronic properties must be machine-learned separately.

## Key ML-IP Milestones for GST (Elliott Group, Oxford)

| Year | Model | Size | Notes |
|------|-------|------|-------|
| pre-2018 | DFT | ~500 atoms | Months on supercomputer; baseline |
| 2018 | First GAP (SOAP) | ~4,000 atoms | ×10 scale-up; DFT-accurate |
| ~2020 | Improved GAP | 25,000 atoms | Published; 58,000 training configs |
| ~2021 | Next-gen GAP | 100,000 atoms | Trained from 25k model |
| 2023+ | ACE potential | 1,000,000+ atoms | ×1000× faster than original GAP; tested to 1 billion atoms (storage-limited) |

## Applications to GST

### Ensemble of Small Models (Statistical Structure)
- 30 models of 315-atom GST-225 made in parallel.
- ~60% have no gap states in the band gap; ~37% do.
- Deep gap states: localized on 5- or 6-coordinate Ge; complex multi-atom wavefunctions.
- Band-edge localized states: chains of hyper-bonded (3-center, 4-electron) seesaw units.
- **Advantage**: captures structural variability invisible in single DFT models.

### Device-Scale Crystallization (20×20×40 nm)
- 500,000-atom simulation of realistic PCRAM cell.
- Amorphous → polycrystalline in ~20 ns (matches experimental crystallization time).
- Reveals nucleation (550 K, many small grains) vs. growth (650 K, single large crystal) regimes.
- Grain boundary resistivity is an additional control parameter for neuromorphic storage.

### Neuromorphic Storage (100×100×5 nm slice, ~800,000 atoms)
- Models continuous amorphous/crystalline fractions for analog multilevel storage.
- Shows grain boundary effects on effective resistance (not just crystal/glass ratio).

## Applications to Elemental Te

### Single-Crystal to Polycrystalline Switching
- 100,000-atom ACE simulation.
- Single-crystal Te melts at ~723 K (matches experimental Tm).
- Polycrystalline Te (after first switching cycle) melts at ~500 K (~200 K lower) due to grain boundaries.
- Explains experimentally observed voltage drop from ~3 V (first event) to ~1 V (subsequent events) for Te selector switches.

### Chiral Te Crystallization
- Amorphous Te → cubic intermediate (only ~90 meV/atom above chain crystal) → right or left helical chains.
- Right and left chiralities nucleate in equal proportions.
- Chiral grain boundaries move via soliton-like mechanism (low energy barrier).
- First molecular dynamics observation of chiral crystallization pathway.

## Advantages Over Pure DFT

| Aspect | DFT | ML-IP |
|--------|-----|-------|
| Scale | ~500 atoms | ~10⁶ atoms |
| Speed scaling | Cubic (N³) | Linear (N) |
| Accuracy | Reference | DFT-accurate |
| Electronic properties | Direct | Machine-learned separately |
| Rare events | Inaccessible | Statistically observable |
| Device simulation | Impossible | Device-scale |

## Related Concepts

- [[pcm-crystal-structure-bonding]] — structural motifs in amorphous GST revealed by ML-IP simulations
- [[pcm-crystallization-ostwald-rule]] — nucleation vs. growth regime at different temperatures; chiral Te crystallization
- [[threshold-switching-pcm]] — electron/hole trapping in deep/shallow gap states of amorphous GST
