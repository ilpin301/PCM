---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/phase-change-memory-from-molecular-tellurides.md"
  - "Raw/Sources/solution-derived-gesbsete-phase-change-chalcogenide-films.md"
source_count: 2
aliases:
  - "chalcogenide ink PCM"
  - "solution-processed PCM"
  - "telluride ink"
  - "amine-thiol PCM"
---

# Chalcogenide Ink / Solution-Processed PCM

Phase-change telluride and selenotelluride films can be fabricated entirely from **liquid molecular inks** at ambient pressure and temperature — bypassing the vacuum sputtering or MBE equipment traditionally required. Two complementary studies establish the state of the art for electrical (Schenk et al.) and optical (Kang et al.) PCM inks.

## Synthesis Route (Schenk et al. — telluride inks)

1. **Dissolution**: bulk telluride powders (Sb₂Te₃, GeTe, Sc₂Te₃, TiTe₂) dissolved in an **ethylenediamine / 1,2-ethanedithiol (en/Edtsh)** cosolvent at 50 °C. Rapid color change signals molecular complex formation; thiolate anions break M–Te bonds via nucleophilic attack.
2. **Polytelluride removal**: lithium triethylborohydride reduces polytelluride chains (Ten²⁻, up to ~50 nm), which otherwise degrade film quality.
3. **Purification**: precipitation in acetonitrile, centrifugation, redissolving in ethylenediamine; excess Te removed by tri-n-octylphosphine (TOP).
4. **Spin-coating + anneal**: spin-coated at 1250–4000 rpm; dried at 70 °C, then annealed at 350 °C / 20 min (ramp 5 °C min⁻¹). As-deposited films are amorphous; crystallization completes by ~250 °C.

Inks are stable for months under N₂. Sc₂Te₃ and TiTe₂ require 15 h dissolution (vs. 2 h for Sb₂Te₃/GeTe) due to stronger Sc–Te and Ti–Te bonds.

## Composition Tuning by Ink Mixing

Mixing GeTe + Sb₂Te₃ binary inks yields **homogeneous ternary GST** films across the full GeTe–Sb₂Te₃ pseudo-binary line, including stoichiometric GST225, GST124, and GST147. Ge content scales predictably with the volume ratio (concave/convex with concentration ratio). Similarly, admixing Sc₂Te₃ ink gives tunable **Sc–Sb–Te (SST)** at compositions matching co-sputtered reference materials (e.g., Sc₀.₂Sb₂Te₃ for sub-1 ns switching, Sc₀.₃Sb₂Te₃ for improved nucleation).

Minor S incorporation (~10–15 at.% max in binary GeTe) from thiolate binding does not preclude memory function; sulfur-containing PCMs are known. Longer stirring increases S content proportionally.

## Film Quality

- **Texture**: films spontaneously align with the c-axis perpendicular to substrate — (00l) preferred orientation. Driving force: low surface energy of Te-terminated vdW-like gaps aligning parallel to substrate. Texture quantified by pole figures: m.r.d. ≈ 30 for Sb₂Te₃, 12 for GST147, 3.5 for GST225.
- HR-TEM shows lattice fringes at 0.31 nm matching GST225 (103) planes; vdW-like gaps visible as dark lines parallel to substrate.
- RMS roughness: ~6–8 nm; no pinholes (AFM verified).
- Thickness tunable 15–85 nm by varying spin speed and ink concentration.
- Cross-plane thermal conductivity 60% lower than in-plane (layered texture) → reduces thermal dissipation and improves energy efficiency in crossbar devices.

## Deposition Engineering Advantages

- **Nanoscale via infilling**: molecular inks fill sub-100 nm trenches conformally (capillary forces drive inks into gaps); laminar fill comparable to ALD.
- **Flexible substrates**: deposited on polyimide (Kapton) with identical film quality; no delamination on bending — relevant for flexible/wearable electronics.
- **Substrate independence**: same annealing protocol applies to glass, Si, or polyimide.

## Functional Memory Devices (Schenk et al.)

Planar (lateral) prototype devices with two Pt electrodes 300 nm apart, SiO₂-encapsulated, GST225 ink drop-cast and annealed:
- **Threshold voltage**: Vth = 0.8–2.0 V (typical ~1.18 V); snapback I–V behavior on crystallization.
- **RESET**: 75 ns pulse, 3.5 V → resistance increase >100× (up to ~1 MΩ). SET: 10 μs pulse, 2.5 V → resistance drops back to ~4 kΩ.
- **Resistance contrast**: >2 orders of magnitude; comparable to state-of-the-art sputtered GST225.
- **Endurance**: 25 full RESET/SET cycles demonstrated; record cell reaches ~200 switches.
- **Reset energy**: 229 pJ at 7,200 nm² electrode area — nearly 1× below sputtered GST devices of comparable dimensions; consistent with the linear scaling law (energy ∝ electrode area).

## Solution-Derived Ge–Sb–Se–Te (Kang et al.) — Optical PCM

**Target material**: Ge₂Sb₂Se₄Te₁ (GSST), a Se-substituted GST, aimed at **reducing optical loss (k)** in the near-IR while preserving large Δn for photonic applications. DFT (Zhang et al.) shows partial Te→Se replacement reduces k via bandgap increase and lower free-carrier concentration, while maintaining resonant bonding Δn.

### Process challenges
- **Solvent**: EtSH/en mixture (50 vol% EtSH for maximum solubility) → Te fully dissolved, but EtSH evaporates preferentially over time, limiting process window.
- Improved solvent: **en:Edtsh (10:1 v/v)** — Edtsh evaporates slower; complete dissolution at 2.5 wt% loading level; forms dark brown, transparent solutions.
- Residual C (~few at.%) detected by EDS after 210 °C bake, attributed to solvent by-products; S and N absent.
- Crystallization to single-phase Ge₂Sb₂Se₄Te₁ not fully achieved from solution; partial Sb₂Se₃ phase observed, likely due to residual Te nanoparticles and solvent residues disrupting crystallization energetics.
- Reducing Te content from x=1.0 to x=0.5–0.7 suppresses Te crystal formation in as-coated films.

### Key optical results
- Solution-derived films show broadband IR transmission (mid- to long-wave); heat treatment reduces short-wave IR transparency (increased n, reduced bandgap, free-carrier absorption from crystallization).
- Femtosecond laser writing (801 nm, sub-ablation) locally crystallizes patterned regions; Raman confirms partial structural transformation consistent with Ge₂Sb₂Se₄Te₁ signature peaks (115, 155, 188 cm⁻¹), though mismatch with TE-deposited reference indicates incomplete crystallization.

## Outlook / Pathways to Extension

- Inkjet printing, optical lithography, or direct-light printing could enable patterned PCM layers at low cost.
- Sub-10 nm via infilling may approach ultimate PCM scaling limits.
- Telluride inks applicable to thermoelectrics, solar cells, photodetectors.
- Ge-rich GST inks (e.g., Ge₄Sb₂Te₅ with Tc ~350 °C) accessible by the same mixing approach — enabling embedded automotive memory from solution.

## Related Concepts

- [[pcm-material-design-rules]] — composition selection principles (GST, SST)
- [[pcm-superlattices]] — high-quality films traditionally require MBE/PVD; ink route offers simpler textured alternative
- [[pcm-crystal-structure-bonding]] — rhombohedral/trigonal phases and (00l) texture explained by vdW-like gap energetics
- [[pcm-memory-switching-speed]] — SST sub-ns switching; GST225 80 ns baseline
- [[pcm-visible-photonics]] — GSST is also used in visible/near-IR photonics
- [[phase-change-materials]] — parent topic
