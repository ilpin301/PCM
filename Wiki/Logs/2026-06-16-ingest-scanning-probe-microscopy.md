---
tags:
  - "log"
topics:
  - "phase-change-materials"
status: stable
created: 2026-06-16
updated: 2026-06-16
sources:
  - "Raw/Sources/scanning-probe-microscopy-textbook.md"
source_count: 1
aliases: []
---

# 2026-06-16 — Ingest: Scanning Probe Microscopy Textbook

## What Happened

Ingested a new PDF (`Raw/Files/Scanning_Probe_Techniques_Buchseiten.pdf`, scanned textbook pages on scanning probe techniques) into the Wiki. NotebookLM was available, so the PDF was extracted via the `llm-wiki-pdf-extract` pipeline into a study-guide companion (`.pdf.md`) before compiling.

## What Was Created

- Companion: `Raw/Files/Scanning_Probe_Techniques_Buchseiten.pdf.md` (NotebookLM study guide)
- Source note: [[scanning-probe-microscopy-textbook]]
- New Wiki note: [[scanning-probe-microscopy]] (concept)

## Why It Matters

Adds the **characterization-technique** layer behind the surface probes used in PCM research. STM (tunneling, LDOS imaging) and AFM/SFM (force detection via the optical-lever method, variants MFM/EFM/PFM) — the AFM optical-lever principle connects directly to the AFM module in [[laser-switching-setup-lss]] and the AFM/EBSD/APT characterization of [[pcm-superlattices]].

## Related Notes

- [[scanning-probe-microscopy]] — the new concept
- [[laser-switching-setup-lss]] — AFM in the PCM optical-switching rig
