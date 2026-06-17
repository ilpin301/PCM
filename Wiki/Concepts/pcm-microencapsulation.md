---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-17
updated: 2026-06-17
sources:
  - "Raw/Sources/nanoencapsulation-of-phase-change-materials-for-advanced-thermal-energy-storage.md"
  - "Raw/Sources/ini-alkanes-phase-change-materials-and-their-microencapsulation-for-thermal-ener.md"
  - "Raw/Sources/analysis-of-the-thermal-stability-of-pcms-and-its-effect-on-energy-storage-effic.md"
  - "Raw/Sources/additive-manufacturing-for-phase-change-thermal-energy-storage-and-management.md"
  - "Raw/Sources/advances-in-phase-change-materials-for-thermal-energy-storage-and-management-cha.md"
source_count: 5
aliases:
  - "MEPCM"
  - "NEPCM"
  - "microencapsulated PCM"
  - "nanoencapsulated PCM"
---

# PCM Microencapsulation and Nanoencapsulation

Encapsulation of [[latent-heat-pcm-thermal-storage|thermal PCMs]] inside polymer or inorganic shells at the micro- (1–1000 µm) or nano- (1–1000 nm) scale. Encapsulation is the central enabling technology for practical deployment of solid–liquid PCMs, resolving the twin problems of leakage and low thermal conductivity.

## Why Encapsulate?

Raw solid–liquid PCMs melt and flow, causing leakage, contamination of adjacent materials, and loss of PCM volume. Encapsulation:

1. Physically contains the liquid PCM during melting.
2. Increases surface-area-to-volume ratio, improving heat transfer (a 1 mm capsule gives ~300 m² m⁻³ surface area increase vs. bulk PCM).
3. Protects the PCM from chemical reactions with the external environment (critical for salt hydrates which can dehydrate).
4. Reduces supercooling in organic PCMs (heterogeneous nucleation off the shell wall).
5. Enables powder/paste form for blending into concrete, paint, foams, and textiles.

## Size Classes

| Class | Diameter | Key Properties |
|-------|----------|---------------|
| Macro | > 1000 µm | Simplest; prone to rupture during pumping |
| Micro (MPCM) | 1–1000 µm | Industrial standard; processable; good durability |
| Nano (NEPCM) | 1–1000 nm | Highest SA/V; more stable than microcapsules under flow; lower viscosity in slurries |

Nanocapsules are structurally more stable under deformation forces than microcapsules and show lower flow drag in slurry applications.

## Emulsion Templates

Encapsulation starts from an emulsion of PCM droplets in a continuous phase. Droplet size controls final capsule size:

- **Regular emulsion / homogenisation**: yields microcapsules > 1 µm.
- **Miniemulsion (nanoemulsion)**: formed by high-energy sonication or microfluidics; droplets 100–500 nm; kinetically stable; requires 3–10 wt% surfactant.
- **Microemulsion**: thermodynamically stable; requires > 20 wt% surfactant; spontaneous formation.

**Sonication** (acoustic cavitation) is the standard lab method for miniemulsion formation; industrial scale-up is possible but not yet routine.

## Shell Materials

### Polymer Shells
- Most common: polystyrene (PS), poly(methyl methacrylate) (PMMA), polyurethane (PU), urea–formaldehyde (UF), melamine–formaldehyde (MF), polyurea.
- Formed by in situ polymerisation, interfacial polymerisation, miniemulsion polymerisation, or coacervation.
- Thermal conductivity ~0.20 W m⁻¹ K⁻¹ — low, limits heat exchange rate.
- Advantage: flexible (resist rupture from PCM volume change during melting ~10–15% volume expansion).

### Inorganic Shells (Silica, Alumina, Clay)
- SiO₂ thermal conductivity ~1.3 W m⁻¹ K⁻¹ vs ~0.15 W m⁻¹ K⁻¹ for bulk octadecane — ~5–10× improvement.
- Silica nanocapsules (via sol–gel TEOS hydrolysis): encapsulation efficiency up to 87.5 wt%; 500-cycle stability demonstrated.
- More brittle; may fracture under PCM volume change stress.
- Adding just 1 wt% SiO₂ to a PS shell increased thermal conductivity by 8.4%.

### Carbon-Based Shells (GO–CNT)
- Graphene oxide/carbon nanotube (GO–CNT) hybrid shells: mechanically reinforce against volume-change rupture; enhance thermal conductivity through the shell.
- Docosane/GO–CNT capsules: encapsulation ratio 96.7 wt%; average latent heat 240.8 J g⁻¹; stable over 100 thermal cycles; negligible supercooling.

### Layer-by-Layer (LbL) Assembly
- Alternating deposition of oppositely charged polyelectrolytes (e.g., PSS / PDADMAC) on emulsion droplets.
- Allows nm-precise shell thickness control; can incorporate conductive nanoparticles in intermediate layers.
- Shell thicknesses ~10 nm achievable; demonstrated for octadecane (500 nm capsules, 91.3 wt% core content).

## Synthesis Methods Summary

| Method | Type | Notes |
|--------|------|-------|
| In situ polymerisation | Chemical | Monomer only in continuous phase |
| Interfacial polymerisation | Chemical | Monomers in both phases |
| Miniemulsion polymerisation | Chemical | Best for nanocapsules; scalable |
| Sol–gel (TEOS) | Chemical | Inorganic SiO₂ shell; high efficiency |
| Coacervation | Physico-chemical | Simpler; lower shell quality |
| Pickering emulsion | Physico-chemical | Nanoparticle-stabilised; no surfactant purification needed |
| Spray drying | Physical | Simple; industrial; lower encapsulation efficiency |
| LbL assembly | Chemical | Ultrathin, multifunctional shells |

## Encapsulation Efficiency

Encapsulation efficiency (EE) is defined as the ratio of the composite latent heat to that of pure PCM:

EE = (ΔH_composite / ΔH_PCM) × 100%

State-of-the-art values: 80–97 wt% for organic PCMs in polymer shells; typically lower for inorganic (salt hydrate) PCMs.

## Supercooling Effects

Encapsulation generally reduces supercooling in organic PCMs by promoting heterogeneous nucleation at the shell wall. However, in inorganic PCMs (salt hydrates), supercooling remains problematic even after encapsulation, because heat transfer is still insufficient to trigger nucleation at small undercooling.

## Inorganic (Salt Hydrate) PCM Encapsulation

Salt hydrates are much harder to encapsulate than paraffins due to hydrophilicity, tendency to alter water content, and chemical instability. Key strategies:

- **W/O emulsion** (inverted): water-phase PCM dispersed in oil continuous phase.
- **Inverse Pickering emulsion**: nanoparticles stabilise the W/O interface.
- Shell materials: polyurea/polyurethane, PMMA, poly(ethoxysiloxane), ORMOCER (Fraunhofer ISC biodegradable hybrids).
- Nanoencapsulation of Mg(NO₃)₂·6H₂O in ethyl-2-cyanoacrylate (in situ miniemulsion): stable over 100 cycles, no water loss, reduced supercooling.
- Eutectic nanoencapsulation: 1:2 Mg(NO₃)₂·6H₂O : Na₂SO₄·10H₂O eutectic — single peak at T_M = 15.4 °C; ΔH = 126.8 J g⁻¹; 67 wt% encapsulation efficiency; > 100 cycle stability.

## Applications Enabled by Encapsulation

- **PCM slurries** (heat-transfer fluids): NEPCM dispersed in poly-α-olefin (PAO) or water; heat transfer coefficient up to 47 000 W m⁻² K at 3.5 ml s⁻¹ in microchannel heat exchangers (2× improvement over single-phase PAO).
- **Building materials**: addition to concrete, mortar, plaster, paint; indoor temperature regulation; requires >7300 melt/freeze cycles (20-year life at 1 cycle/day).
- **Textiles and smart fabrics**: see [[electrospun-pcm-mats-photothermal]] for electrospun PCM fibre mats.
- **3D-printed composites**: see [[tes-additive-manufacturing]].
- **Battery thermal management**: see [[pcm-battery-thermal-management]].

## Key Challenges

- Low thermal conductivity of polymer shells limits heat exchange rate.
- < 100% encapsulation efficiency (shell displaces PCM mass).
- Nanoparticle additives enhance thermal conductivity but reduce latent heat capacity (dilution effect).
- Salt hydrate encapsulation remains immature vs. paraffin encapsulation.

## Related Notes

- [[latent-heat-pcm-thermal-storage]] — latent heat storage principles and materials
- [[pcm-thermal-conductivity-enhancement]] — filler-based enhancement strategies
- [[tes-additive-manufacturing]] — 3D printing with PCM composites
- [[pcm-battery-thermal-management]] — battery pack cooling applications
