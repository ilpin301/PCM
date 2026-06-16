---
tags:
  - "concept"
  - "method"
topics:
  - "phase-change-materials"
status: seed
created: 2026-06-13
updated: 2026-06-13
sources:
  - "Raw/Sources/widmann-2026-gst-in2te3-superlattices.md"
source_count: 1
aliases:
  - "Laser Switching Setup"
  - "LSS"
  - "laser switching setup"
---

# Laser Switching Setup (LSS)

The **Laser Switching Setup (LSS)** is the optical bench used to **locally switch PCM superlattice samples** between their amorphous and crystalline phases with well-controlled laser pulses, while simultaneously imaging the sample surface. It combines two physically distinct light paths: a **pulsed laser** that does the actual switching and a **white LED** that only provides illumination for visualization and spot positioning. (Bachelor thesis, §3.1.1.)

## Two light paths, two jobs

The key to understanding the setup is that the laser and the LED do completely different things and are merged onto a common axis by a dichroic combiner.

| Path | Role | Schematic color |
|------|------|-----------------|
| **Pulsed laser** | Actively switches the PCM (writes amorphous/crystalline spots) | red |
| **White LED** | Pure illumination for real-time imaging + laser-spot positioning | blue |

## The laser — the "writing tool"

The laser induces the local temperature rise that drives the phase transition.

- Source: semiconductor **pulsed laser diode**, λ = **660 nm**, driven by a **PICOLAS PLCS-21** module.
- The PLCS-21 acts as a **digital pulse generator**; an applied voltage U sets the average pulse power:

```
P = 37.89 mW/V · U − 154.93 mW        (Eq. 3.1)
```

  with a maximum output power of **400 mW**.
- Four pulse parameters are adjustable via a **LabVIEW** program:
  - pulse duration τ (1–10000 ns)
  - pulse power (0–150 mW for τ < 30 ns; 0–400 mW for τ > 30 ns)
  - repetition rate f (1–2000 Hz)
  - number of pulses

The parameter regime selects the outcome (see [[pcm-crystallization-ostwald-rule]]):
- **short, high-energy pulses** → melt + rapid quench → **amorphous**
- **longer, lower-energy pulses** → heat into the crystallization window → **crystalline** (nucleation + growth)

## The white LED — illumination only

The LED switches nothing; it lights the sample so the camera can see it.

- A **white LED** beam is coupled into the path via reflection at a beam splitter.
- Reflected light from the sample returns through the same objective and beam splitter to a **CCD camera**, giving a **real-time image of the surface** and enabling **precise positioning of the laser spot** (IDS software).

## Optical path and stage

- Laser beam collimated by an aspheric lens (NA = 0.5), steered by two mirrors to a **dichroic beam combiner**.
- The **dichroic combiner reflects the laser wavelength and transmits the LED light**, aligning both onto a common axis — so the camera image shows exactly where the laser will hit.
- Both beams pass a microscope objective (10×, NA = 0.25) and focus onto the sample.
- Sample sits on a **NanoMax-TS piezoelectric stage** (Thorlabs): 3D motion, 20 µm range, 5 nm step accuracy, LabVIEW-controlled.

## Not to be confused: the AFM laser

A separate laser appears in the **AFM** (§3.2.3). It plays no role in switching — it only reflects off the back of the cantilever onto a position-sensitive photodetector to track tip deflection.

## Related Concepts

- [[pcm-superlattices]] — the samples switched on this setup
- [[pcm-crystallization-ostwald-rule]] — nucleation- vs. growth-dominated recrystallization, set by pulse parameters
- [[pcm-memory-switching-speed]] — amorphization vs. crystallization energetics and timing
- [[phase-change-materials]] — parent topic

## Sources

- [[widmann-2026-gst-in2te3-superlattices]] — Bachelor's thesis (Ricco Widmann, RWTH Aachen, May 2026), §3.1.1 "Laser Switching Setup (LSS)" and §3.2 characterization techniques. PDF: `Raw/Files/Bachelorarbeit_FINAL_RW_final_260513_130841.pdf`.
