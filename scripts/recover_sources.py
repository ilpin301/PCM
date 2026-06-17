#!/usr/bin/env python3
"""Recover blocked NotebookLM exports into 'Temp sources/' with llmwiki frontmatter.

Routes:
  - PMC open-access  -> Europe PMC fullTextXML (JATS) -> clean markdown
  - Paywalled/Optica -> arXiv API search by title (preprint), else Unpaywall by DOI
  - Aggregator pages -> arXiv search by title; if nothing, report NOT RECOVERED

Uses urllib with an empty ProxyHandler so it ignores the machine SOCKS proxy
(direct internet works; see CLAUDE.md). Run:  python scripts/recover_sources.py
"""
import os, re, sys, json, glob, argparse, datetime, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

OUT = r"F:\____IL_AI\PCM\Temp sources"
TODAY = datetime.date.today().isoformat()
os.makedirs(OUT, exist_ok=True)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
opener.addheaders = [("User-Agent", "llmwiki-recover/1.0 (mailto:ilpin301@gmail.com)")]
urllib.request.install_opener(opener)

def fetch(url, timeout=90):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:80].strip("-")

def frontmatter(title, author, ref, ctype):
    return (
        "---\n"
        f'Title: "{title.replace(chr(34), chr(39))}"\n'
        f'Author: "{author.replace(chr(34), chr(39))}"\n'
        f'Reference: "{ref}"\n'
        "ContentType:\n"
        f'  - "{ctype}"\n'
        f"Created: {TODAY}\n"
        "Processed: false\n"
        "tags:\n"
        '  - "source"\n'
        "---\n\n"
    )

def write_note(title, author, ref, ctype, body, tag_slug):
    name = (tag_slug or slug(title) or "recovered") + ".md"
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter(title, author, ref, ctype))
        f.write(body.strip() + "\n")
    return path

# ---------- JATS (Europe PMC) ----------
def strip_ns(xml):
    # Drop xmlns declarations, then remove namespace prefixes from tags and
    # attributes so ElementTree doesn't choke on "unbound prefix" (xlink:, mml:, arxiv:).
    xml = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", xml)
    xml = re.sub(r'(</?)[A-Za-z_][\w.-]*:', r"\1", xml)        # <ns:tag> -> <tag>
    xml = re.sub(r'\s[A-Za-z_][\w.-]*:([A-Za-z_][\w.-]*=)', r" \1", xml)  # ns:attr= -> attr=
    return xml

def render(el, depth, out):
    for child in el:
        tag = child.tag
        if tag == "sec":
            out.append("")
            render(child, depth + 1, out)
        elif tag == "title":
            t = " ".join("".join(child.itertext()).split())
            if t:
                out.append("#" * min(depth + 1, 6) + " " + t)
        elif tag == "p":
            t = " ".join("".join(child.itertext()).split())
            if t:
                out.append(t)
        elif tag in ("fig", "table-wrap"):
            cap = child.find(".//caption")
            t = " ".join("".join(cap.itertext()).split()) if cap is not None else ""
            if t:
                out.append("*" + t + "*")
        else:
            render(child, depth, out)
    return out

def from_pmc(pmcid):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    raw = strip_ns(fetch(url))
    root = ET.fromstring(raw)
    at = root.find(".//article-title")
    title = " ".join("".join(at.itertext()).split()) if at is not None else pmcid
    authors = []
    for c in root.findall('.//contrib[@contrib-type="author"]'):
        sn = c.find(".//surname"); gn = c.find(".//given-names")
        nm = " ".join(x.text for x in (gn, sn) if x is not None and x.text)
        nm = " ".join(nm.split())  # collapse stray newlines/whitespace
        if nm:
            authors.append(nm)
    author = "; ".join(authors[:8]) + (" et al." if len(authors) > 8 else "") or "Unknown"
    body_lines = []
    ab = root.find(".//abstract")
    if ab is not None:
        ab_lines = render(ab, 1, [])
        # Only add the "## Abstract" header if the content doesn't already lead with a heading.
        if ab_lines and not ab_lines[0].lstrip().startswith("#"):
            body_lines.append("## Abstract")
        body_lines += ab_lines
    bd = root.find(".//body")
    if bd is not None:
        render(bd, 0, body_lines)
    body = "\n\n".join(x for x in body_lines if x.strip())
    if len(body) < 400:
        raise ValueError(f"{pmcid}: full text too short ({len(body)} chars) — may not be OA full text")
    ref = f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
    return write_note(title, author, ref, "markdown", body, slug(title))

# ---------- arXiv search ----------
def arxiv_search(title):
    q = urllib.parse.quote(f'ti:"{title}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=2"
    raw = strip_ns(fetch(url))
    root = ET.fromstring(raw)
    e = root.find("entry")
    if e is None:
        return None
    t = " ".join("".join(e.find("title").itertext()).split())
    summ = " ".join("".join(e.find("summary").itertext()).split())
    auths = [a.find("name").text for a in e.findall("author")]
    absurl = e.find("id").text
    return {"title": t, "abstract": summ, "authors": "; ".join(auths), "url": absurl}

def from_arxiv(orig_title, orig_url):
    hit = arxiv_search(orig_title)
    if not hit:
        return None
    body = f"## Abstract (arXiv preprint)\n\n{hit['abstract']}\n\n" \
           f"_Recovered as arXiv preprint of paywalled source. Original: {orig_url}_"
    return write_note(hit["title"], hit["authors"], hit["url"], "web", body, slug(hit["title"]))

# ---------- Open-access PDF (Crossref -> Unpaywall -> PDF text) ----------
EMAIL = "ilpin301@gmail.com"

def fetch_bytes(url, timeout=120):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()

def _authors(lst):
    names = [" ".join(filter(None, [a.get("given"), a.get("family")])) for a in (lst or [])]
    names = [" ".join(n.split()) for n in names if n.strip()]
    return "; ".join(names) or "Unknown"

def crossref_doi(title):
    url = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(title)
    items = json.loads(fetch(url)).get("message", {}).get("items", [])
    if not items:
        return None
    it = items[0]
    return {"doi": it.get("DOI"),
            "title": (it.get("title") or [title])[0],
            "author": _authors(it.get("author"))}

def unpaywall(doi):
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
    d = json.loads(fetch(url))
    loc = d.get("best_oa_location") or {}
    return {"title": d.get("title") or "",
            "author": _authors(d.get("z_authors")),
            "pdf": loc.get("url_for_pdf") or loc.get("url"),
            "is_oa": d.get("is_oa")}

def extract_pdf_text(data):
    import io
    try:
        import fitz  # PyMuPDF
        with fitz.open(stream=data, filetype="pdf") as doc:
            return "\n\n".join(p.get_text() for p in doc)
    except ImportError:
        pass
    try:
        from pdfminer.high_level import extract_text
        return extract_text(io.BytesIO(data))
    except ImportError:
        pass
    try:
        from pypdf import PdfReader
        return "\n\n".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(data)).pages)
    except ImportError:
        pass
    raise RuntimeError("No PDF library installed. Run:  $env:NO_PROXY='*'; python -m pip install pymupdf")

def clean_pdf_text(t):
    t = t.replace("\r", "")
    t = re.sub(r"-\n(\w)", r"\1", t)       # join hyphenated line breaks
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def from_oa_pdf(entry):
    title, orig, doi = entry["title"], entry["orig"], entry.get("doi")
    if not doi:
        cr = crossref_doi(title)
        if not cr or not cr["doi"]:
            raise RuntimeError("no DOI found via Crossref")
        doi = cr["doi"]
    up = unpaywall(doi)
    if not up["pdf"]:
        raise RuntimeError(f"DOI {doi} has no open-access PDF (is_oa={up['is_oa']})")
    data = fetch_bytes(up["pdf"])
    if data[:4] != b"%PDF":
        raise RuntimeError(f"{up['pdf']} did not return a PDF (got {data[:16]!r}) — likely blocked")
    text = clean_pdf_text(extract_pdf_text(data))
    if len(text) < 800:
        raise RuntimeError(f"extracted text too short ({len(text)} chars)")
    final_title = up["title"] or title
    author = up["author"] if up["author"] != "Unknown" else "Unknown"
    ref = f"https://doi.org/{doi}"
    body = (f"## Full text (open-access, recovered via Unpaywall)\n\n"
            f"_Original (blocked): {orig}_  \n_DOI: {doi}_\n\n{text}")
    return write_note(final_title, author, ref, "pdf", body, slug(final_title))

# ---------- local PDF extraction ----------
def pdf_metadata(data):
    try:
        import fitz
        with fitz.open(stream=data, filetype="pdf") as doc:
            m = doc.metadata or {}
            return (m.get("title") or "").strip(), (m.get("author") or "").strip()
    except Exception:
        return "", ""

def run_local(folder):
    pdfs = sorted(glob.glob(os.path.join(folder, "*.pdf")))
    if not pdfs:
        print(f"No PDFs found in {folder}")
        return
    ok, fail = [], []
    for path in pdfs:
        name = os.path.basename(path)
        try:
            with open(path, "rb") as f:
                data = f.read()
            if data[:4] != b"%PDF":
                raise RuntimeError("not a valid PDF")
            text = clean_pdf_text(extract_pdf_text(data))
            if len(text) < 800:
                raise RuntimeError(f"little/no extractable text ({len(text)} chars) — may be scanned/image-only")
            mtitle, mauthor = pdf_metadata(data)
            base = os.path.splitext(name)[0]
            title = mtitle or re.sub(r"[_-]+", " ", base).strip()
            author = mauthor or "Unknown"
            body = (f"## Full text (extracted from local PDF)\n\n"
                    f"_Source file: {name}_\n\n{text}")
            # Reference defaults to the filename as a local identifier — edit to a DOI/URL if known.
            p = write_note(title, author, name, "pdf", body, slug(title) or slug(base))
            print(f"[OK ] {name} -> {p}")
            ok.append(p)
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            fail.append((name, str(e)))
    print(f"\nLocal extraction done. Extracted {len(ok)}, failed {len(fail)}.")
    for f in fail:
        print("  -", f[0], "::", f[1])

# ---------- targets ----------
PMC = [
    "PMC10786157", "PMC5987736", "PMC10512918", "PMC11300797",
    "PMC13150642", "PMC13089636", "PMC11068603",
]
# Open-access PDF recovery. doi=None => resolve via Crossref by title.
OA_PDF = [
    {"title": "Endurance of chalcogenide optical phase change materials: a review",
     "orig": "https://opg.optica.org/ome/fulltext.cfm?uri=ome-12-6-2145",
     "doi": None},
    {"title": "Laser-induced phase transitions of Ge2Sb2Te5 thin films used in optical and electronic data storage and in thermal lithography",
     "orig": "https://opg.optica.org/fulltext.cfm?uri=oe-18-17-18383",
     "doi": "10.1364/OE.18.018383"},  # Optics Express DOIs are deterministic: vol.zero-padded-page
    {"title": "Morphological characterization and applications of phase change materials in thermal energy storage: A review",
     "orig": "https://ideas.repec.org/a/eee/rensus/v72y2017icp128-145.html",
     "doi": None},
]

def main():
    ok, fail = [], []
    for pid in PMC:
        try:
            p = from_pmc(pid)
            print(f"[OK ] PMC {pid} -> {p}")
            ok.append(p)
        except Exception as e:
            print(f"[FAIL] PMC {pid}: {e}")
            fail.append((pid, str(e)))
    for entry in OA_PDF:
        try:
            p = from_oa_pdf(entry)
            print(f"[OK ] OA-PDF <- {entry['orig']} -> {p}")
            ok.append(p)
        except Exception as e:
            print(f"[MISS] OA-PDF {entry['orig']}: {e}")
            fail.append((entry["orig"], str(e)))
    print(f"\nDone. Recovered {len(ok)}, failed/missing {len(fail)}.")
    if fail:
        print("Needs manual attention:")
        for f in fail:
            print("  -", f[0], "::", f[1])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Recover blocked sources into 'Temp sources/'.")
    ap.add_argument("--local", nargs="?", const=r"F:\____IL_AI\PCM\Raw\Files",
                    metavar="DIR",
                    help="Extract text from local PDFs in DIR (default Raw/Files) "
                         "instead of online recovery.")
    args = ap.parse_args()
    if args.local:
        run_local(args.local)
    else:
        main()
