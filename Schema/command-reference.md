# Command Reference

All commands run from the vault root. Requires Python 3.8+.

---

## wiki_tool.py

### `doctor`

Non-mutating health check. Verifies folder structure, Python version, catalog, source manifest, and note counts.

```bash
python3 scripts/wiki_tool.py doctor
```

### `build`

Regenerates `Wiki/catalog.jsonl`, `Wiki/index.md`, and per-folder index files.

```bash
python3 scripts/wiki_tool.py build
```

### `lint`

Validates compiled Wiki note frontmatter: allowed tags, `source_count` accuracy, source file existence, required date fields.

```bash
python3 scripts/wiki_tool.py lint
```

### `source-scan`

Lists all Raw sources. Optionally updates `Schema/source-manifest.jsonl`.

```bash
# List only
python3 scripts/wiki_tool.py source-scan

# Update manifest
python3 scripts/wiki_tool.py source-scan --update

# Update manifest, marking covered sources as processed
python3 scripts/wiki_tool.py source-scan --update --accept-covered
```

### `source-lint`

Validates Raw source frontmatter and coverage. Fails if a source is marked `Processed: true` but has no Wiki coverage.

```bash
python3 scripts/wiki_tool.py source-lint
```

### `source-delta`

Shows Raw sources that are not yet in the manifest.

```bash
python3 scripts/wiki_tool.py source-delta
```

### `source-coverage`

Shows which Raw sources are covered by compiled Wiki notes.

```bash
python3 scripts/wiki_tool.py source-coverage
```

### `search-catalog`

Searches compiled Wiki notes through the catalog.

```bash
python3 scripts/wiki_tool.py search-catalog --query "llm wiki"
```

### `log`

Appends a short entry to `Wiki/log.md`.

```bash
python3 scripts/wiki_tool.py log --title "Ingested LLM Wiki intro" --details "Added 3 Wiki notes from the LLM Wiki intro source."
```

---

## audit_public.py

Checks all tracked files for secrets, private keys, machine-local paths, and plugin/cache state.

```bash
python3 scripts/audit_public.py
```

---

## Maintenance Gate (run before every commit)

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

## Post-Ingest Gate

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```
