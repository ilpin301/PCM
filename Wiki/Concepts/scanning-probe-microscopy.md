---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-16
updated: 2026-06-16
sources:
  - "Raw/Sources/scanning-probe-microscopy-textbook.md"
source_count: 1
aliases:
  - "SPM"
  - "scanning probe microscopy"
  - "scanning probe techniques"
---

# Scanning Probe Microscopy (SPM)

**Scanning probe microscopy (SPM)** is a family of surface-science techniques that achieve **atomic resolution** by scanning a sharp probe at a small distance over a surface and measuring the **tip–surface interaction** (electrical, magnetic, or mechanical). Unlike scattering experiments, SPM produces **real-space** images. The field began in **1981** with the invention of the scanning tunneling microscope (STM).

In this vault SPM is relevant as the **characterization-technique family** behind the surface probes used in PCM research — most directly **AFM**, which appears alongside EBSD/APT in the superlattice work (see [[laser-switching-setup-lss]]).

## STM — tunneling current

The **scanning tunneling microscope (STM)** uses the quantum-mechanical **tunneling effect** to image **conducting** surfaces (metals, semiconductors, superconductors).

- A bias applied between a metal tip and the sample across a ~1 nm gap drives a **tunneling current** `I`.
- `I` depends **exponentially** on the gap `z`: `I ∼ exp(−2 k_eff z)`. A 0.1 nm change in distance produces a large current change — the origin of atomic resolution.
- STM images the **local density of electronic states (LDOS) near the Fermi energy**, not the atoms directly.
- Two operating modes:
  - **Constant-current** — feedback adjusts tip height to hold the current constant.
  - **Constant-height** — current variations are recorded at a fixed height.
- Clean surfaces require **ultra-high vacuum** (< 1×10⁻⁸ Pa).

## AFM / SFM — force detection

The **atomic / scanning force microscope (AFM/SFM)** measures **forces** rather than current, so it can image **insulators, organic, and biological** samples that STM cannot.

- Relevant forces: van der Waals, electrostatic, magnetic, capillary, and repulsive (contact). The **Hamaker constant `A`** is the material-specific parameter setting the van der Waals force.
- **Detection — optical-lever method:** a laser reflects off the back of the cantilever onto a photodiode to track deflection. (This is the same role the AFM laser plays in the PCM characterization rig — see "Not to be confused: the AFM laser" in [[laser-switching-setup-lss]].)
- **Variants:** MFM (magnetic — e.g. storage media), EFM (electrostatic — surface charge), PFM (piezoresponse — ferroelectrics).
- Soft biomolecules are preserved using **tapping (intermittent-contact) mode** or **Q-control** in the low-force regime.

## Atomic manipulation — bottom-up nanotechnology

The probe is not only an imaging tool but a manipulator:

- **Lateral manipulation** — dragging or pushing an atom along the surface without lifting it.
- **Vertical manipulation** — transferring particles between the surface and the tip apex.
- **Quantum corral** — an artificial nanostructure (e.g. 48 Fe atoms on Cu) assembled atom-by-atom to confine a 2D electron gas and visualize the electrons' wave nature.
- **Controlled chemistry** — the tip can induce and stepwise-control reactions, e.g. the **Ullmann reaction** (aryl coupling, biphenyl synthesis) at low temperature.

Precise 3D tip motion (x, y, z) is provided by **piezo tubes**.

## Related Concepts

- [[laser-switching-setup-lss]] — PCM optical-switching rig whose AFM module uses the optical-lever detection described here
- [[pcm-superlattices]] — superlattice samples characterized by AFM/EBSD/APT
- [[phase-change-materials]] — parent topic

## Sources

- [[scanning-probe-microscopy-textbook]] — scanning probe techniques textbook excerpt (STM, AFM/SFM, atomic manipulation). PDF: `Raw/Files/Scanning_Probe_Techniques_Buchseiten.pdf`.
