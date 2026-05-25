---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/wuttig-yamada-2007-pcm-review.md"
  - "Raw/Sources/Phase-change memory and switching materials.md"
source_count: 2
aliases:
  - "PCM crystal structure"
  - "p-bonding PCM"
  - "rocksalt GST"
---

# PCM Crystal Structure and Bonding

The common thread linking all phase-change materials used in data storage is their **octahedral-like crystal structure**, driven by p-orbital bonding rather than sp³ hybridization. This structural motif enables the fast, reversible amorphous ↔ crystalline transitions that make PCMs useful.

## Crystal Structures of Key PCMs

| Material | Crystal Structure | Notes |
|----------|-----------------|-------|
| Ge₂Sb₂Te₅ (GST-225) | Metastable rocksalt (cubic) | Te on one sublattice; Ge, Sb, vacancies on other |
| Ge₁Sb₂Te₄ | Rocksalt | ~25% vacancy concentration on cation sublattice |
| Te₆₀Ge₄Sn₁₁Au₂₅ | Simple cubic | No distortions; statistical atom distribution |
| AIST (Ag₅In₅Sb₆₀Te₃₀) | Distorted simple cubic | Becomes nearly cubic at high temperature |
| Stable GST | Hexagonal | Ground state; forms after annealing; not accessed during fast switching |

## Bonding Character

- PCM bonding is **p-orbital dominated**, not sp³. Electrons form 3-center, 4-electron bonds along p-orbital directions → octahedral geometry.
- Average valence electrons > 4 → octahedral arrangement preferred over tetrahedral (sp³).
- **Peierls distortions**: local symmetry reduction driven by p-bonding; reduces optical contrast if strong; low-vacancy, high-Ge compositions have fewer distortions.
- **Antibonding state occupation**: in Ge₂Sb₂Te₄, some antibonding states are occupied. Vacancies on the cation sublattice reduce average valence electron count → lower energy by reducing antibonding occupation. This explains why GST tolerates ~25% vacancy concentration.

## Nearest-Neighbor Geometry

- Rocksalt motifs: 4-fold rings, cubes, 90° bond angles, octahedral 6-fold coordination.
- Nearest-neighbor Ge–Te spacing: ~3 Å.
- **Hyper-bonding (seesaw units)**: defective octahedral sites with long, weak, strongly polarizable bonds along one axis (3-center 4-electron character). These appear in both crystalline and glassy phases.

## Amorphous State Structure

- **Ge atoms**: tetrahedral coordination in amorphous phase (4-fold, no lone pair).
- **Umbrella flip** (Kolobov et al.): on crystallization, Ge switches from tetrahedral to octahedral coordination. This is the primary structural change in the SET process.
- Amorphous GST retains **many crystalline-like (octahedral/seesaw) units** → minimal atomic movement needed to nucleate crystalline phase → fast crystallization.
- Even-folded ring structures in amorphous GST (no homopolar Ge–Ge bonds); GeTe has both even- and odd-numbered rings (Ge–Ge bonds present).
- Melt-quenched amorphous contains subcritical crystalline nuclei → faster recrystallization than as-deposited amorphous.

## Seesaw/Hyper-Bonded Units in the Glass

The glassy state of GST contains what Elliott's group call "seesaw" units — defective octahedral sites where:
- Two bonds are long, weak, strongly polarizable → 3-center 4-electron bonding
- These violate the octet rule (10 electrons in bonding shell)
- Chains of these seesaw units form localized conduction-band-edge states
- Deep gap states center on 5- or 6-coordinate Ge atoms with complex, multi-atom wavefunctions

## Crystallization Mechanism (Atomic Level)

From million-atom machine-learned potential simulations:
- At ~550 K (nucleation-dominated): many small polycrystalline grains form simultaneously
- At ~650 K (growth-dominated): single nucleus appears and grows into a large crystal — completely different morphology
- Device-scale (20×20×40 nm GST): full amorphous-to-polycrystalline transition in ~20 ns (matching experiment)
- Grain boundaries in polycrystalline GST have their own resistivity behavior — additional control parameter for neuromorphic computing

## Comparison: Successful vs. Unsuccessful PCMs

| Material | Structure | Valence e⁻ | PCM? |
|----------|-----------|-----------|------|
| GeTe | Rocksalt/rhombohedral | >4 | ✓ |
| Ge₁Sb₂Te₄, Ge₂Sb₂Te₅ | Rocksalt | >4 | ✓ |
| In₃SbTe₂ (IST) | Rocksalt | >4 | ✓ (plasmonic) |
| AIST | Distorted cubic | >4 | ✓ |
| AgInTe₂ | Chalcopyrite | 4 | ✗ |
| AuInTe₂ | Chalcopyrite | 4 | ✗ |

## Related Concepts

- [[pcm-material-design-rules]] — how to search for new PCMs
- [[pcm-crystallization-ostwald-rule]] — role of metastable rocksalt phase in fast crystallization
- [[plasmonic-pcm]] — IST: metallic crystalline phase from p-bonding with excess valence electrons
