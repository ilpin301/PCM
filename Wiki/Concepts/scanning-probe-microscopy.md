---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-16
updated: 2026-06-17
sources:
  - "Raw/Sources/scanning-probe-microscopy-textbook.md"
  - "Raw/Sources/atomic-force-microscopy-for-crossdisciplinary-materials-research---pmc---nih.md"
  - "Raw/Sources/thermally-induced-nanoscale-phase-change-in-chalcogenide-glass-cr2ge2te6-reveale.md"
source_count: 3
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

## Advanced AFM Modes for Property Mapping

Beyond topography, AFM probes local physical properties by modifying the tip or applying targeted stimuli. All measurements exploit the same cantilever/photodiode platform but report different signals.

### Electrical and electrochemical modes

- **C-AFM (conductive-AFM)** — applies a DC voltage through a conducting tip in contact mode; maps local current flow with nanoscale precision to reveal electrical heterogeneities (e.g., grain boundary conductance in chalcogenides).
- **KPFM / SKPM (Kelvin probe force microscopy)** — applies AC voltage, nullifies oscillations with DC bias to extract local surface potential and work-function distribution.
- **SCM (scanning capacitance microscopy)** — measures ∂C/∂V to map carrier density and dopant profiles in semiconductors.
- **ESM (electrochemical strain microscopy)** — detects Vegard strains from AC-voltage-driven ion redistribution; maps ionic conductivity and activation energies in battery materials.

### Mechanical and ferroelectric modes

- **PFM (piezoresponse force microscopy)** — AC voltage drives inverse piezoelectric expansion; maps ferroelectric domain walls and polarization switching. Can resolve both in-plane and out-of-plane polarization.
- **MFM (magnetic force microscopy)** — lift mode with a magnetized tip; images magnetic domains and stray fields in storage media and spintronic devices; resolution to tens of nanometers.

### Operating-mode physics (contact vs. non-contact)

- **Contact mode (CM)** — tip in continuous contact; loading force set by cantilever spring constant, InvOLS, and setpoint. Good for flat, rigid surfaces and electrical contact measurements; can damage soft samples.
- **Non-contact / tapping mode (NCM)** — oscillating tip near resonance; amplitude modulation (AM-AFM) or frequency modulation (FM-AFM). Phase channel images compositional heterogeneity by tracking resonance shifts from attractive/repulsive force gradients.
- **PeakForce tapping** — controlled oscillation with well-defined peak force; enables simultaneous nanomechanical mapping with minimal damage.

### Key practical notes (Joo et al. 2025)

Signal interpretation pitfalls: elastic-modulus differences between PS (2 GPa) and LDPE (0.1 GPa) cause apparent height offsets in NCM because the tip indents softer domains. Amplitude/phase artifacts appear at slope transitions when feedback cannot keep up. Tip contamination, humidity, and electromagnetic interference affect all modes — non-specialists frequently underappreciate these factors.

## STM and STS applied to PCM phase-change tracking

STM/STS (scanning tunneling spectroscopy) provides a direct nanoscale window into the **electronic-structure change** during PCM amorphous-to-crystalline transitions:

- A UHV-STM (base pressure ~5×10⁻⁸ Pa) with tungsten tips was used on **Cr₂Ge₂Te₆ (CrGT)** thin films deposited on HOPG substrates.
- Topographic images: amorphous CrGT shows grain diameter ~15–25 nm (RMS roughness 0.87 nm at 200 °C); after crystallization at 320 °C grains grow to 50–60 nm (RMS 7.8 nm).
- Power spectral density (PSD) analysis of 2D-FFT STM data quantifies lateral correlation length `x` and vertical roughness `σ`, both increasing with annealing temperature and changing abruptly near the crystallization point.
- STS (dI/dV mapping over 50×50 points in 500×500 nm²): dI/dV at −0.8 V decreases after crystallization; histogram Gaussian narrows with increasing crystallinity. This tracks the reduction in hole carrier density when localized Cr-cluster electrons redistribute into Cr–Te bonds.
- Cross-validation: nanoscale crystalline fraction from STS histograms agrees with macroscale Raman Eg²/Ag¹ peak intensities. Both follow Arrhenius kinetics with activation energy ~3.0 eV (higher thermal stability than GST).
- CrGT's **inverse resistance** characteristic (high-R crystalline, low-R amorphous) contrasts with GST and arises from carrier density suppression on crystallization.

See [[cr2ge2te6-pcm]] for full CrGT material details.

## Related Concepts

- [[laser-switching-setup-lss]] — PCM optical-switching rig whose AFM module uses the optical-lever detection described here
- [[pcm-superlattices]] — superlattice samples characterized by AFM/EBSD/APT
- [[cr2ge2te6-pcm]] — CrGT PCM material studied by STM/STS
- [[afm-gst-thermal-mapping]] — nanoscale thermal mapping protocol using GST as a phase-change thermometry layer
- [[phase-change-materials]] — parent topic

## Sources

- [[scanning-probe-microscopy-textbook]] — scanning probe techniques textbook excerpt (STM, AFM/SFM, atomic manipulation). PDF: `Raw/Files/Scanning_Probe_Techniques_Buchseiten.pdf`.
- Joo et al. (2025), *Small Methods* 9(11):2500514 — cross-disciplinary AFM review covering advanced modes, data-interpretation pitfalls, and practical protocols (KAIST). PMC12641378.
- Kim et al. (2024), *Jpn. J. Appl. Phys.* 63:015504 — STM/STS study of thermally induced nanoscale phase change in CrGT thin films on HOPG.
