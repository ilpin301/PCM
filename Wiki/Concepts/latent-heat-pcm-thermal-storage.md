---
tags:
  - "concept"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/Are Phase Change Materials the Future of Water Heaters.md"
  - "Raw/Sources/Cooling AI How Phase Change Materials Make a Difference.md"
source_count: 2
aliases:
  - "thermal PCM"
  - "latent heat storage"
  - "PCM-TES"
---

# Latent-Heat PCM Thermal Storage

> **Disambiguation**: This note covers PCMs in the **thermal energy storage** sense (paraffin, salt hydrates, etc.). These are completely distinct from [[phase-change-materials|electronic/photonic PCMs]] (GeSbTe, AIST, etc.) that switch between amorphous and crystalline states for memory and photonics.

Thermal PCMs exploit the latent heat of a solid–liquid phase transition to store or release large amounts of thermal energy at a nearly constant temperature equal to the material's melting point.

## Operating Principle

- **Charging** (melting): material absorbs heat from environment or heat source; transitions solid → liquid.
- **Discharging** (solidification): material releases stored latent heat; transitions liquid → solid.
- Unlike sensible heat storage (e.g., water tanks), energy density is ~4× higher for the same temperature range because most energy goes into the phase transition, not temperature change.
- Temperature stays near-constant during phase change → **precise thermal output**.

## Common Materials

| Material | Phase Transition | Notes |
|----------|----------------|-------|
| Paraffin wax | Solid ↔ liquid | Widely studied; non-toxic; low flammability |
| Sodium acetate (trihydrate) | Solid ↔ liquid | "Hot ice"; high energy density |
| Hydrated salts (salt hydrates) | Solid ↔ liquid | Cheap; prices dropping; some corrosive |
| Bio-based PCMs | Solid ↔ liquid | Lower cost alternative to paraffin |

## Applications

### Hot Water Storage (Heat Batteries)
- **Sunamp Thermino**: PCM hot water battery; 4× more compact than conventional water tank; 50% less heat loss (0.74 vs. 1.3 kWh/day); compatible with heat pumps, solar PV, boilers. Cost ~£3,245 installed; saves ~£602/yr in case study.
- **MaREI solar-PCM tank**: 300 L hot water storage with paraffin PCM bed; maintains 60 °C for 7 hours with single solar collector.

### Building Thermal Management
- **BioPCM ENRG Blanket** (Phase Change Solutions): placed above drop ceilings/roofs; absorbs excess heat during the day, releases at night; reduces HVAC power 25–35%, runtime 15–20%, cycling 20–25%; ROI < 4 years for commercial buildings.
- **QE Platinum** (Texas): multi-layer film for attic/ceiling insulation; ~20% energy savings; 20-year life.
- Cost: ~$3.50/sq ft vs. $0.25–$1.40 for conventional foam insulation.

### Data Centre Cooling
- PCM-TES units can provide peak shaving (reduce grid load during peak demand) and participate in **frequency regulation** ancillary services (rapidly absorb/release energy in response to grid frequency deviations).
- **La-Flex project** (SINTEF-led, EU): testing PCM cold storage unit (Cartesian AS) in data centre context; DTU evaluating applicability; AI-nergy studying ancillary services; THWS doing techno-economic assessment.
- Data centre cooling consumes up to 50% of total power; ~700,000 kWh/day globally for LLMs; generating 10–50 AI responses requires ~500 mL of cooling water.
- Norway: 18 data centres; new regulations require cost-benefit analysis for waste heat utilization (centres > 2 MW).

## Market
- PCM (thermal storage) market: $477M (2021) → ~$1B by 2026.

## Challenges
- **Temperature specificity**: only effective within a narrow temperature range; thermostat cannot be adjusted freely without wasting energy on re-charging the thermal mass.
- **Eutectic vs. non-eutectic**: eutectic compositions have sharp solid–liquid transitions; non-eutectics go through a pasty intermediate phase — affects thermal performance.
- **Weight**: heavier than conventional insulation; installation must prevent PCM cells from being punctured or sagging.
- **Cost**: 2.5–14× more expensive than conventional insulation upfront; improving as scale-up and bio-based alternatives emerge.
- **Awareness and regulation**: limited consumer awareness; subsidy frameworks still developing.
