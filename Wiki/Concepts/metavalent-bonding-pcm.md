---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-10
updated: 2026-06-10
sources:
  - "Raw/Sources/widmann-2026-gst-in2te3-superlattices.md"
  - "Raw/Sources/piperidou-2025-gst-sb2te3-superlattices.md"
source_count: 2
aliases:
  - "metavalent bonding"
  - "MVB"
  - "bond confinement"
  - "PME"
---

# Metavalent Bonding in PCMs

**Metavalent bonding (MVB)** is the unconventional bonding mechanism of the *crystalline* phase of many phase-change materials. It is characterized by the **coexistence of electron localization and delocalization**, giving properties distinct from ionic, covalent, and metallic bonding. The amorphous phase, by contrast, is predominantly **covalent** — and this change in bonding is the origin of the large optical and electrical contrast that makes PCMs useful.

## Fingerprint properties

MVB sits between covalent and metallic bonding on several metrics (the amorphous→crystalline switch moves the material across this boundary):

| Property | Ionic | Covalent | Metavalent | Metallic |
|----------|-------|----------|------------|----------|
| Electronic conductivity σ | very low | low–moderate | moderate | high |
| Optical dielectric constant ε∞ | low | moderate | high | — |
| Born effective charge Z* | low | moderate | high | vanishes |
| Grüneisen parameter γ_TO | moderate | low | high | low |

The **8-N rule** is satisfied for covalent compounds but **not** for metavalent bonding. On a quantum-chemical map of *electrons shared (ES)* vs. *electrons transferred (ET)*, PCMs form a distinct cluster that is neither metallic, ionic, nor covalent — the signature of MVB.

## PME: an experimental indicator

In atom probe tomography (APT), the **Probability of Multiple Events (PME)** — the likelihood that a single field-evaporation pulse releases multiple ions — serves as a proxy for bonding character:

- **High PME** → strong metavalent character (delocalized p-electrons).
- **Low PME** → more covalent / localized bonding.

Typical values (Piperidou): GST-124 ~90%, Sb₂Te₃ ~86%, while covalently bonded PCMs are generally ~20%.

## The bond-confinement hypothesis

In GST-124/Sb₂Te₃ superlattices (Piperidou), PME falls to ~60–70%, and **thinner supercells show systematically lower PME** — i.e. more covalent character. Because lower PME correlates with lower required switching power and smaller amorphized areas, the proposed mechanism is **bond confinement**: confining the Sb₂Te₃ to ultrathin layers enhances electron localization/covalency, enabling more energy-efficient switching.

This revises the earlier **interface (vdW-gap) hypothesis** toward a bonding-based explanation. The causal chain from increased covalency to improved switching is not yet established; proposed probes include TEM, phonon (fs pump–probe), thermal-conductivity (FDTR), and DFT.

PME also tracks the phase transition itself: in an amorphized N:8 superlattice PME drops from 71% (crystalline) to 47% (amorphous), then recovers (~62–67%) on recrystallization — consistent with MVB being a crystalline-phase phenomenon. (The amorphous value staying above ~20% may indicate residual short-range order or an APT artifact.)

## Covalent layers as a design lever

If covalency aids switching, deliberately introducing a **covalent** layer is a natural next step. Widmann pairs metavalent GST-124 with covalent, non-PCM [[In2Te3]] — a metavalent–covalent interface distinct from the metavalent–metavalent SLs studied previously.

## Related Concepts

- [[pcm-superlattices]] — where the bond-confinement hypothesis applies
- [[In2Te3]] — a covalently bonded confinement layer
- [[pcm-crystal-structure-bonding]] — p-orbital bonding and rocksalt structure in bulk PCMs
- [[phase-change-materials]] — parent topic

## Sources

- [[widmann-2026-gst-in2te3-superlattices]] — MVB vs. covalent bonding; ES/ET map; metavalent–covalent SL interfaces
- [[piperidou-2025-gst-sb2te3-superlattices]] — PME as bonding indicator; bond-confinement hypothesis
