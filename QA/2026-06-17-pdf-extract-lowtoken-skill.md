# Low-Token PDF Extract Skill: Brainstorm / Discovery Notes
Date: 2026-06-17 · Goal: Design a skill that converts PDFs in `Raw/Files/` into ingest-ready `.pdf.md` companions using **minimal tokens**, as an alternative to `llm-wiki-pdf-extract` (which uses NotebookLM).

## Context gathered (pre-interview)
- Existing skill `llm-wiki-pdf-extract`: NotebookLM-based, produces an interpretive **study guide** companion (`Raw/Files/<name>.pdf.md`). Network round-trip per PDF; ~0 Claude tokens but slow and curated/lossy vs. raw text.
- Local tools present: `pdftotext` (poppler), Python `fitz` (PyMuPDF), `pypdf`. Missing: marker, markitdown, pdfplumber, mutool.
- `Raw/Files/`: 9 PDFs, 7 have `.pdf.md` companions. Missing companions: `oe-18-17-18383.pdf`, `ome-12-6-2145.pdf`.
- Companion format today = curated study guide (key concepts, Q&A, glossary) with a header (source/authors/links).

## Summary / key decisions
- **Name/location**: `llm-wiki-pdf-extract-local` in global `~/.claude/skills/`, sibling to `llm-wiki-pdf-extract`.
- **Output type**: Deterministic local text extraction + a **Haiku subagent** that writes only a short header from the first ~1-2 pages. Faithful body, NOT a study guide.
- **Engine**: PyMuPDF (`fitz`) — gives font-size info for heading detection; `pdftotext` as fallback.
- **Token control**: body never goes through any model; only first ~2 pages → Haiku for the header. Near-fixed tiny cost/PDF.
- **File contract**: writes `Raw/Files/<name>.pdf.md` (no YAML frontmatter; `# Title` + source line + body). Default skips PDFs that already have a companion; `--force` to refresh.
- **Scanned PDFs**: detect near-empty text (<~100 chars/page avg) → write nothing, flag for NotebookLM/OCR fallback.
- **Trigger**: "extract locally / offline / low-token / quick" PDF phrasing; the NotebookLM skill stays the default/curated path.

### Q7 — Completeness backstop
- Captured: defaults accepted (PyMuPDF engine, <100 chars/page scanned threshold, local/offline/low-token triggers). Nothing to add. Proceed to design + spec.

## Q&A log

### Q1 — Output type / quality-vs-token tradeoff
- Asked: What should the `.pdf.md` companion contain (raw text / local+cheap cleanup / study-guide summary)?
- Captured: **Local text + cheap-model cleanup.** Deterministic local extraction first, then a cheap model lightly structures/cleans it. Faithful, not a study guide.
- Flags: none

### Q2 — File contract / coexistence with existing companions
- Asked: How to coexist with the 7 existing NotebookLM `.pdf.md` study guides?
- Captured: **Same `<name>.pdf.md` target, only fill missing.** Default run skips any PDF that already has a companion (so only the 2 missing PDFs process now). One companion per PDF, no clobbering. Optional `--force` to refresh.
- Flags: none

### Q3 — Token-control / division of labor
- Asked: How to split work between deterministic script and the model to keep cost minimal?
- Captured: **Script does all mechanical cleanup** (PyMuPDF: dehyphenate, strip repeated headers/footers, collapse whitespace, detect headings via font size). **Cheap model sees ONLY the first ~1-2 pages** to write a short metadata/frontmatter header (title, authors, abstract). Body never goes through the model → near-fixed, tiny token cost per PDF regardless of length.
- Flags: none

### Finding (explored, not asked) — companion format contract
- `.pdf.md` companions have **NO YAML frontmatter**. They start with `# <Title>` + a short source/authors/links block, then markdown body. (Existing ones say `# Study Guide: ...`.)
- Frontmatter is added downstream by `scripts/add_frontmatter.py` during ingest; `_templates/source-note.md` is the eventual Wiki note shape.
- => The model-written header should mirror this light style (title + source line), NOT emit YAML frontmatter. Our title need not say "Study Guide" since it's raw extraction.

### Q4 — Scanned / no-text-layer PDFs
- Asked: How to handle PDFs with no extractable text layer (OCR likely unavailable)?
- Captured: **Detect, skip, flag for NotebookLM.** If extracted text is near-empty, write NO companion, report the PDF as needing NotebookLM/OCR, suggest the `llm-wiki-pdf-extract` fallback. Skill stays zero-dependency and offline; user routes hard cases to the network path.
- Flags: none

### Q5 — Cheap-model invocation mechanism
- Asked: How to invoke the cheap-model header step?
- Captured: **Haiku subagent via Claude Code.** Main agent runs extraction script per PDF, dispatches a Haiku subagent with only the first ~2 pages to produce the header block, assembles companion. No API key / extra deps; uses Claude Code subagent + cheaper model. Fits autonomy preference ([[prefer-cheaper-model-subagents]]).
- Flags: none

### Q6 — Name & location
- Asked: Skill name and where it lives?
- Captured: Name **`llm-wiki-pdf-extract-local`** (mirrors sibling, signals local/low-token variant). Location **global `~/.claude/skills/`** (alongside existing `llm-wiki-pdf-extract`, reusable across vaults).
- Flags: none

## Open flags (pending input)
