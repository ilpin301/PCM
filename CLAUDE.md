# CLAUDE.md — LLM Wiki Rules For AI Agents

# Machine environment: SOCKS system proxy
This Windows machine's system proxy is `socks=127.0.0.1:10808` (local V2RayN/Xray client; no HTTP port on 10809). Python reads it from the registry, so `pip install` (and requests/urllib in fresh environments) can fail with `OSError: Missing dependencies for SOCKS support`. Direct internet access works without the proxy.
- Fix per command (PowerShell): `$env:NO_PROXY='*'; python -m pip install <pkg>`
- Permanent fix per environment: install `pysocks` (using the bypass above once)
- Diagnose: `python -c "import urllib.request; print(urllib.request.getproxies())"`

# Working style
1. Let you think privately. If I need to see you thinking, I read the thinking output rather than making it narrate.
2. Lead with the outcome, keep it simple, and pause only when the work truly needs me.
3. Before you tell me something is done, point to the result that proves it. Only report work you can show evidence for. If something isn't verified, say so plainly instead of guessing.
4. When you have enough information to act, act. Don't re-derive what we've already settled or narrate options you won't pursue. If you're weighing a choice, give a recommendation, not an exhaustive survey.
5. Don`t show me every changed stroke in some files, except when I ask for it myself
6. When I'm describing a problem or asking a question, the deliverable is your assessment. Report what you find and stop. Don't fix, send, edit, or delete anything until I say go. Do the simplest thing that works, and skip cleanup I didn't ask for.

Read this file before doing any work in this vault.

## Core Principle

This vault separates two distinct layers:

- **Raw/Sources/** — original source material, captured as-is. Do not treat this as compiled knowledge.
- **Wiki/** — compiled, reusable knowledge notes. This is the authoritative layer.

## Rules

### Raw Sources

- Treat every file in `Raw/Sources/` as raw input material, not as a knowledge source to cite directly.
- Do not modify Raw source files when compiling Wiki notes.
- Raw sources preserve the original context and wording of the creator.

### Wiki Notes

- Write all reusable knowledge exclusively under `Wiki/`.
- Every compiled Wiki note **must** link back to at least one Raw source in the `sources` frontmatter field.
- Do not invent citations or create unsupported claims. Every claim must be traceable to a Raw source.
- Keep `source_count` equal to the number of entries in `sources`.
- Use only allowed tags: `topic`, `concept`, `entity`, `project`, `log`.

### Before Answering a Question

1. Search `Wiki/catalog.jsonl` before opening any Raw sources:
   ```bash
   python scripts/wiki_tool.py search-catalog --query "your topic"
   ```
2. Open relevant Wiki notes.
3. Open Raw sources only when the compiled note is insufficient or the user needs source-level verification.
4. Cite both the compiled note and the Raw source when the answer depends on source material.

### Before Every Commit

Run the full maintenance gate:

```powershell
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

After source ingestion, also run:

```powershell
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
```

### PDF Files in Raw/Files/

- Before ingesting any file from `Raw/Files/`, check if a `.pdf.md` companion exists.
- If a PDF has no companion `.pdf.md`, ask me which skill should use: `llm-wiki-pdf-extract`,  `llm-wiki-pdf-extract-local` or if pdf is pure scan use `llm-wiki-pdf-extract-ocr`.
- Never ingest a raw PDF directly — always ingest the `.pdf.md` companion.

### Cloudflare auto-clicker (cf-click) for ResearchGate harvests

When you run a ResearchGate harvest (`researchgate-harvester` / "rg harvest"),
wrap the delegation so the user does not have to click the Cloudflare checkbox:

1. `python ~/.claude/skills/cf-click/cf_click.py start`
2. delegate to `researchgate-harvester` (still ask for the query + page count first)
3. `python ~/.claude/skills/cf-click/cf_click.py stop`

Tell the user to keep the Chrome window visible and the screen unlocked.
`cf-click` is best-effort: if it gives up (3 failed attempts or 30 clicks), the
user clicks manually — the harvester's own ~3-min title poll is the safety net.

### Schema

- Follow frontmatter schemas defined in `Schema/frontmatter-schema.md`.
- Follow naming conventions in `Schema/naming-conventions.md`.
- Consult `Schema/workflow-examples.md` for ingest and query examples.

### Security

- Never commit secrets, private keys, machine-local paths, or plugin/cache state.
- Run `python scripts/audit_public.py` to catch these before committing.
- Never edit raw exports.
- Never invent frequencies.
- Never present a tiny sample as a dataset-wide truth.

## Folder Map

```
Raw/Sources/     — original source notes (Processed: false until compiled)
Raw/Files/       — binary source files (ignored by git except .gitkeep)
Wiki/Topics/     — broad topic notes
Wiki/Concepts/   — specific concept notes
Wiki/Entities/   — people, tools, organizations
Wiki/Projects/   — project-level notes
Wiki/Logs/       — log and change notes
Schema/          — rules, schemas, and the source manifest
Samples/         - not for wiki processing, just samples of style and structure for some out creation
Autors           - not for wiki processing, its names of autors for notebookLM creation
_templates/      — note templates
.agents/skills/  — agent skill definitions
scripts/         — deterministic tooling
tutorial/        — tutorial fixtures and examples
```
