---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/ini-alkanes-phase-change-materials-and-their-microencapsulation-for-thermal-ener.md"
  - "Raw/Sources/additive-manufacturing-for-phase-change-thermal-energy-storage-and-management.md"
source_count: 2
aliases:
  - "paraffins as PCM"
  - "n-alkane PCM"
  - "Cn PCM"
---

# n-Alkanes as Phase Change Materials

n-Alkanes (linear hydrocarbons CₙH₂ₙ₊₂, abbreviated Cₙ) are among the most widely studied organic PCMs for [[latent-heat-pcm-thermal-storage|thermal energy storage]]. Paraffin waxes are commercial blends of n-alkanes (C20–C40, 80–95% Cₙ content).

## Phase Change Properties of Pure n-Alkanes

Key PCM-relevant properties are the melting point (MP) and melting enthalpy (ΔHm):

- Both MP and ΔHm increase monotonically with carbon number from C8 to C50.
- Temperature range: C8 (−57 °C) to C50 (~86 °C); covering most building and comfort applications.
- Enthalpy range: ~20 kJ mol⁻¹ (C8) to ~200 kJ mol⁻¹ (C50).

Selected paraffin PCMs (Freeman 2023, Peng et al. 2018):

| Name | Formula | MP (°C) | ΔHfus (kJ kg⁻¹) | Energy Density (kWh m⁻³) |
|------|---------|---------|-----------------|--------------------------|
| n-Tetradecane | C14H30 | 5.5 | 228 | 48.1 |
| n-Hexadecane | C16H34 | 16.7 | 237 | 50.9 |
| n-Octadecane | C18H38 | 28.0 | 244 | 52.7 |
| n-Eicosane | C20H42 | 36.7 | 246 | 53.9 |
| n-Docosane | C22H46 | 44.0 | 249 | 54.9 |

## Polymorphic Complexity

n-Alkanes have a complex polymorphic nature:
- **Odd-numbered** Cₙ: 'C23-Pbcm' orthorhombic structure (C13–C41).
- **Even-numbered** Cₙ: 'C18-P1' triclinic (C14–C26); 'C36-P21/a' monoclinic (C28–C36); various orthorhombic forms for larger chains.
- **Rotator (R) phase** (mesostate): a crystalline state between ordered solid and liquid, where molecules have rotational freedom along their long axes. Present in many Cₙ blends; causes complex multi-step phase transitions.
- Solid–solid transitions contribute additional latent heat alongside the main solid–liquid transition.

## Blends of n-Alkanes

Pure Cₙ have fixed melting points. Blends allow tuning of the melting temperature to a specific application:

**Kravchenko's miscibility rule** (solid-state miscibility in binary Cₙ blends):
- Δnc = 1 (odd-even neighbours): total miscibility only for nc > 16; no miscibility for nc < 8.
- Δnc = 2: total miscibility for nc > 33.
- Δnc = 4: total miscibility for nc > 67.

**Phase equilibrium types** in binary Cₙ systems:
- Eutectic (E): single sharp transition point; best for PCM.
- Peritectic (P): prone to supercooling and phase separation during non-equilibrium cooling; not ideal.
- Isomorphous Congruent Melting (ICM): solid and liquid have same composition; excellent PCM behaviour.
- Isomorphous Incongruent Melting (IIM): ascending type.
- Partially Isomorphous Peritectic (PIP).

**PCM-optimal** blends require:
1. Melting point at the required application temperature.
2. Narrow thermal window (phase change temperature range): ideally 1–2 °C, capturing ≥ 95% of total latent heat within this window.

Well-characterised binary PCM systems include: C14–C16, C15–C18, C15–C21, C18–C21, C20–C22, C26–C28, C44–C50.

Ternary eutectic examples:
- C11–C12–C13 (3:85:12 mol%): MP = 257.1 K, window = 1.2 K, ΔH = 141.3 kJ kg⁻¹.
- C12–C13–C14 (51:40:9 mol%): MP = 261.4 K, window = 1.6 K, ΔH = 144.1 kJ kg⁻¹.

## Advantages and Disadvantages

**Advantages**: chemically stable, noncorrosive, high enthalpy, no supercooling (for pure compounds), wide range of transition temperatures, available in microencapsulated form.

**Disadvantages**: low thermal conductivity (~0.2 W m⁻¹ K⁻¹), volume expansion on melting (~10–15%), leakage, flammability, derived from petroleum (not renewable), higher cost than commercial paraffins.

## Microencapsulated n-Alkane PCMs

See [[pcm-microencapsulation]] for full detail. n-Alkanes are the most well-studied core for MPCM:
- Common shells: PMMA, polystyrene (PS), polyurethane (PU), urea-formaldehyde (UF), melamine-formaldehyde (MF).
- Synthesis: in situ polymerisation, emulsion polymerisation, miniemulsion polymerisation.
- Key outputs: encapsulation efficiency (Een), energy storage efficiency (Ees), leakage rate (Lr).
- SEM, DSC, TGA, FT-IR, AFM, and XRD used for characterisation.

**Confinement effect**: smaller capsules (2 µm vs 10 µm of docosane in PU) show higher crystallinity (more triclinic phase peaks visible by XRD) and higher latent heat (ΔHm = 79 vs 47 J g⁻¹). Spatial confinement modifies the phase transition path.

## Applications

- **Slurry**: MPCM dispersed in water or oil as a heat-transfer fluid with enhanced effective heat capacity.
- **Buildings**: blended into wallboard, plaster, concrete; MPCM-plaster with PMMA/CuO shell (n-dodecanol core): ΔH = 148.88 J g⁻¹, 72.28% encapsulation efficiency, 195 nm average diameter.
- **Textiles**: thermal comfort regulation; see also [[electrospun-pcm-mats-photothermal]].
- **Foam**: PCM-integrated polyurethane or other structural foams for passive thermal regulation.

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — overview of PCM-TES principles
- [[pcm-microencapsulation]] — encapsulation methods and properties
- [[pcm-thermal-conductivity-enhancement]] — conductivity improvement strategies
- [[tes-additive-manufacturing]] — n-alkane PCMs in 3D-printed composites
