---
tags:
  - "entity"
topics:
  - "phase-change-materials"
status: draft
created: 2026-05-25
updated: 2026-05-25
sources:
  - "Raw/Sources/Prof Robert Simpson From data storage to programmable photonics.md"
source_count: 1
aliases:
  - "antimony trisulfide"
  - "Sb2S3"
  - "antimony sulfide"
---

# Sb₂S₃ (Antimony Trisulfide)

Sb₂S₃ is a wide-bandgap phase-change material and the most transparent PCM candidate for visible-wavelength photonics. It is transparent in the visible spectrum (above ~600 nm) while retaining a usable refractive index contrast between amorphous and crystalline states.

## Key Properties

| Property | Amorphous | Crystalline | Notes |
|----------|-----------|------------|-------|
| Bandgap | ~1.5 eV | ~1.5 eV | Widest of any PCM candidate |
| Transparency | > ~600 nm | > ~600 nm | Only PCM transparent in visible |
| Refractive index (near-IR) | ~3 | ~4 | Smaller Δn than GST (4→6) but adequate |
| Absorption at 800 nm | Low | Low | Transparent; contrast vs. GST/GSST which strongly absorb |
| Color (thin film) | Pink | Blue | Resonator-mediated color contrast |

## Advantages

- **Widest bandgap** among PCM candidates → only PCM transparent in visible above ~600 nm
- **Earth-abundant and cheap**: antimony and sulfur are among the most abundant elements; Sb₂S₃ costs ~$50/100g (~20× cheaper than Sb₂Se₃, ~60× cheaper than Sb₂Te₃)
- **Multi-state capability**: antimony coordination changes with temperature → multiple intermediate states with different refractive indices lockable by temperature; demonstrated > 7,000 cycles on partial switching
- **Non-toxic and bio-based production possible** (vs. Te-based PCMs)

## Challenges

- Transparent only above ~600 nm (not fully visible)
- Smaller refractive index contrast (Δn ~1) vs. GST (Δn ~2)
- **Growth-dominated crystallization** (vs. nucleation-dominated for GST) → harder to confine amorphous marks to small areas
- **Birefringence**: anisotropic optical properties complicate design of isotropic metamaterials
- Absorption contrast exploited in early demonstrations relies on onset of absorption near 600 nm, not pure refractive index change

## Demonstrated Applications

- **Color-change films**: pink (amorphous) → blue (crystalline) on laser crystallization; fully reversible
- **Microscale art writing**: Girl with Pearl Earring / Mona Lisa written and overwritten (proof of cyclability)
- **On-chip Mach-Zehnder interferometer**: ~π phase shift demonstrated (with TU Eindhoven); useful for weight-setting in optical neural networks
- **Hyperbolic metamaterials**: Sb₂S₃ as dielectric + Ag as conductor → Type 2 hyperbolic metamaterial (negative permittivity out-of-plane, positive in-plane); potential for sub-wavelength imaging and biosensing at visible wavelengths
- **Nanohole beam-steering arrays** at ~700 nm (unpublished as of 2023 talk)

## Comparison with Other Wide-Bandgap PCMs

| Material | Bandgap | Transparent (visible) | Δn | Notes |
|----------|---------|---------------------|-----|-------|
| **Sb₂S₃** | ~1.5 eV | > 600 nm | ~1 | Best transparency |
| Sb₂Se₃ | ~1.0 eV | No (absorbs at 800 nm) | ~1 | More studied; some visible work |
| GSST (Ge₂Sb₂Se₄Te) | ~0.5 eV | Partial IR | ~1.5 | Near-IR to mid-IR; not visible |
| GST-225 | ~0.5 eV | No | ~2 | Standard; opaque at all visible wavelengths |

## Related Concepts

- [[pcm-visible-photonics]] — why visible-wavelength PCMs need wide bandgaps
- [[plasmonic-pcm]] — IST: the opposite extreme (metallic crystalline phase)
- [[phase-change-materials]] — parent topic
