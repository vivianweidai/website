#!/usr/bin/env python3
"""Regenerate curriculum markdown files and web/public/curriculum/curriculum.json
from the Word (.docx) source documents in web/public/curriculum/notes/.

That notes/ directory no longer exists in the repo: the .docx sources were
dropped in f8e7ad3 and the six rendered .pdf handouts on 2026-07-30, when the
home page's per-subject "pdf" links came off and the site went web-only. To
regenerate a subject, recreate notes/ and drop its .docx back in — a missing
directory just makes every subject skip, it is not an error.

Single source of truth: each subject's .docx file contains the complete
curriculum with tables, LaTeX formulas (as Office Math), and yellow
highlighted rows (cell shading #fff056). This script extracts everything
in one pass — no separate PDF highlight step needed.

Dependencies: python-docx, pandoc (for Office Math → LaTeX conversion)

Usage:
    python3 pipeline/scripts/build_curriculum.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx is required: pip3 install python-docx")

WML = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
OMATH = "http://schemas.openxmlformats.org/officeDocument/2006/math"

YELLOW = "fff056"

SECTION_ORDER = {
    "mathematics": ["number-theory", "combinatorics", "geometry",
                    "algebra", "precalculus", "calculus"],
    "computing":   ["statistics", "sampling", "inference",
                    "language", "computing", "learning"],
    "physics":     ["mechanics", "harmonics", "electromagnetism",
                    "thermodynamics", "optics", "modern"],
    "chemistry":   ["atoms", "bonds", "stoichiometry",
                    "physical", "organic", "inorganic"],
    "biology":     ["cells", "genetics", "ecology",
                    "plants", "animals", "neuroscience"],
    "astronomy":   ["observations", "coordinates", "mechanics",
                    "solar-system", "stars", "cosmology"],
}

SUBJECT_NAMES = {
    "mathematics": "Mathematics",
    "computing":   "Computing",
    "physics":     "Physics",
    "chemistry":   "Chemistry",
    "biology":     "Biology",
    "astronomy":   "Astronomy",
}


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# --------------------------------------------------------------------------
# Formula extraction via pandoc
# --------------------------------------------------------------------------

def extract_formulas_pandoc(docx_path: Path) -> list[str]:
    """Run pandoc on the docx and return all math expressions in document order.

    Uses pandoc's JSON AST output to cleanly extract math elements,
    avoiding issues with multiline formulas (matrices) in markdown tables.
    """
    result = subprocess.run(
        ["pandoc", str(docx_path), "-t", "json"],
        capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pandoc warning: {result.stderr[:200]}", file=sys.stderr)
    ast = json.loads(result.stdout)

    formulas: list[str] = []

    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("t") == "Math":
                # Collapse multiline formulas (e.g. matrices) to single line
                tex = re.sub(r"\s*\n\s*", " ", obj["c"][1]).strip()
                formulas.append(tex)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(ast)
    return formulas


# --------------------------------------------------------------------------
# DOCX table parsing
# --------------------------------------------------------------------------

def cell_text(cell_elem) -> str:
    """Extract plain text from a table cell, ignoring oMath."""
    parts = []
    for p in cell_elem.findall(f"{{{WML}}}p"):
        for r in p.findall(f"{{{WML}}}r"):
            for t in r.findall(f"{{{WML}}}t"):
                if t.text:
                    parts.append(t.text)
    return " ".join(parts).strip()


def cell_has_math(cell_elem) -> bool:
    return len(cell_elem.findall(f".//{{{OMATH}}}oMath")) > 0


def count_math(cell_elem) -> int:
    return len(cell_elem.findall(f".//{{{OMATH}}}oMath"))


def _extract_cell(cell_elem, formulas: list[str], idx: int) -> tuple[str, int]:
    """Extract cell content, substituting oMath with pandoc LaTeX formulas.
    Returns (text, new_formula_index)."""
    parts = []
    for p in cell_elem.findall(f"{{{WML}}}" + "p"):
        for child in p:
            tag = child.tag.split("}")[-1]
            ns_prefix = child.tag.split("}")[0] + "}" if "}" in child.tag else ""
            if tag == "r":
                # Regular text run
                for t in child.findall(f"{{{WML}}}t"):
                    if t.text:
                        parts.append(t.text)
            elif tag == "oMath":
                # Math element — use pandoc formula
                if idx < len(formulas):
                    parts.append(f"${formulas[idx]}$")
                idx += 1
            elif tag == "oMathPara":
                # Math paragraph wrapper — contains oMath children
                for om in child.findall(f".//{{{OMATH}}}oMath"):
                    if idx < len(formulas):
                        parts.append(f"${formulas[idx]}$")
                    idx += 1
    text = " ".join(parts).strip()
    # Collapse multiple spaces (from paragraph boundaries)
    text = re.sub(r"  +", " ", text)
    return text, idx


def cell_fill(cell_elem) -> str:
    """Return the fill color of a cell, or '' if none."""
    shd = cell_elem.find(f".//{{{WML}}}shd")
    if shd is not None:
        fill = shd.get(qn("w:fill"))
        if fill:
            return fill.lower()
    return ""


def row_is_yellow(row_elem) -> bool:
    """Check if non-label cells (col 1+) have yellow shading."""
    cells = row_elem.findall(f"{{{WML}}}tc")
    for cell in cells[1:]:
        if cell_fill(cell) == YELLOW:
            return True
    return False


def para_text(p_elem) -> str:
    return "".join(t.text or "" for t in p_elem.findall(f".//{{{WML}}}t")).strip()


def process_docx(docx_path: Path, formulas: list[str]) -> tuple[list[dict], int]:
    """Parse a single docx. Returns (tables_data, formula_count_consumed).

    Each entry in tables_data:
        {section, topic, table_name, rows: [{label, formula, description}],
         highlighted_rows: [int]}
    """
    doc = Document(str(docx_path))
    body = doc.element.body
    elements = list(body)

    # Walk body: track section/topic from uppercase paragraphs
    current_section = ""
    current_topic = ""
    tables_data = []
    formula_idx = 0
    toc_tables_seen = 0
    subject_heading_skipped = False
    expect_topic = False  # after a repeated section heading, next is a topic

    for elem in elements:
        tag = elem.tag.split("}")[-1]

        if tag == "p":
            text = para_text(elem)
            if text and text.strip().isupper() and len(text.strip()) >= 2:
                upper = text.strip()
                # The subject name appears first (e.g. "MATHEMATICS"),
                # then alternating section/topic pairs
                if upper == docx_path.stem.upper() and not subject_heading_skipped:
                    subject_heading_skipped = True
                    continue  # skip subject heading
                if upper.title() == current_section:
                    # Repeated section heading before a topic.
                    # Also handles topic with same name as section.
                    current_topic = upper.title()
                    expect_topic = True
                    continue
                if expect_topic:
                    # After a repeated section heading, the next
                    # heading is always a topic (even if its name
                    # matches a known section, e.g. "BONDS" topic
                    # inside the Inorganic section).
                    current_topic = upper.title()
                    expect_topic = False
                    continue
                if not current_section or upper.title() != current_topic:
                    slug = slugify(upper)
                    subj_slug = docx_path.stem.lower()
                    known_sections = SECTION_ORDER.get(subj_slug, [])
                    if slug in known_sections:
                        current_section = upper.title()
                    elif not current_section:
                        current_section = upper.title()
                    else:
                        current_topic = upper.title()

        elif tag == "tbl":
            # Skip first 2 tables (TOC tables)
            toc_tables_seen += 1
            if toc_tables_seen <= 2:
                # Still count any formulas in TOC tables
                for cell in elem.findall(f".//{{{WML}}}tc"):
                    formula_idx += count_math(cell)
                continue

            rows_elem = elem.findall(f"{{{WML}}}tr")
            if not rows_elem:
                continue

            # Header row (row 0) has the table name
            header_cells = rows_elem[0].findall(f"{{{WML}}}tc")
            table_name = cell_text(header_cells[0]) if header_cells else "unknown"
            # Remove bold markers
            table_name = table_name.strip("*").strip()
            # Count any formulas in header
            for cell in header_cells:
                formula_idx += count_math(cell)

            # Data rows
            table_rows = []
            highlighted = []
            last_label = ""
            for ri, row in enumerate(rows_elem[1:]):
                cells = row.findall(f"{{{WML}}}tc")

                # Handle rows where columns 2-3 are merged (gridSpan=2)
                if len(cells) == 2:
                    gs = cells[1].find(f".//{{{WML}}}gridSpan")
                    if gs is not None and gs.get(qn("w:val")) == "2":
                        raw_label, formula_idx = _extract_cell(
                            cells[0], formulas, formula_idx)
                        raw_span, formula_idx = _extract_cell(
                            cells[1], formulas, formula_idx)
                        label = raw_label if raw_label else last_label
                        last_label = label
                        is_yellow = cell_fill(cells[1]) == YELLOW
                        if is_yellow:
                            highlighted.append(len(table_rows))
                        table_rows.append({
                            "label": label,
                            "formula": raw_span,
                            "description": "",
                            "is_latex": count_math(cells[1]) > 0,
                            "colspan": True,
                        })
                        continue
                    else:
                        # Unknown 2-cell layout, count formulas and skip
                        for cell in cells:
                            formula_idx += count_math(cell)
                        continue

                if len(cells) < 2:
                    for cell in cells:
                        formula_idx += count_math(cell)
                    continue

                # Process all three columns, consuming pandoc formulas
                # in document order (col 0, col 1, col 2)
                raw_label, formula_idx = _extract_cell(
                    cells[0], formulas, formula_idx)
                raw_formula, formula_idx = _extract_cell(
                    cells[1], formulas, formula_idx)
                description, formula_idx = _extract_cell(
                    cells[2], formulas, formula_idx)

                label = raw_label if raw_label else last_label
                last_label = label
                formula = raw_formula
                is_latex = count_math(cells[1]) > 0

                if row_is_yellow(row):
                    highlighted.append(len(table_rows))

                table_rows.append({
                    "label": label,
                    "formula": formula,
                    "description": description,
                    "is_latex": is_latex,
                })

            tables_data.append({
                "section": current_section,
                "topic": current_topic,
                "table_name": table_name,
                "rows": table_rows,
                "highlighted_rows": highlighted,
            })

    return tables_data, formula_idx


# --------------------------------------------------------------------------
# Markdown generation
# --------------------------------------------------------------------------

def escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_table_md(path: Path, table_name: str, rows: list[dict]) -> None:
    lines = [
        f"# {table_name}",
        "",
        "<table>",
        "<tr><th>Label</th><th>Formula / Concept</th><th>Description</th></tr>",
    ]
    for row in rows:
        label = row["label"]
        formula = row["formula"]
        # Fields from _extract_cell already have $...$ around LaTeX parts
        # Only escape non-LaTeX text segments
        if "$" not in label:
            label = escape_html(label)
        cell = formula if "$" in formula else escape_html(formula)
        if row.get("colspan"):
            lines.append(f"<tr><td>{label}</td><td colspan=\"2\">{cell}</td></tr>")
        else:
            desc = row["description"]
            if "$" not in desc:
                desc = escape_html(desc)
            lines.append(f"<tr><td>{label}</td><td>{cell}</td><td>{desc}</td></tr>")
    lines.append("</table>")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
# Manifest assembly
# --------------------------------------------------------------------------

def build_all(root: Path) -> dict:
    notes_dir = root / "web" / "public" / "curriculum" / "notes"
    source_dir = root / "web" / "public" / "curriculum" / "source"
    manifest: dict = {}

    for subj_slug, subj_name in SUBJECT_NAMES.items():
        docx_path = notes_dir / f"{subj_slug}.docx"
        if not docx_path.exists():
            print(f"  skipping {subj_slug}: no docx found", file=sys.stderr)
            continue

        print(f"Processing {subj_slug}.docx...", file=sys.stderr)
        formulas = extract_formulas_pandoc(docx_path)
        print(f"  {len(formulas)} formulas extracted by pandoc", file=sys.stderr)

        tables_data, consumed = process_docx(docx_path, formulas)
        print(f"  {len(tables_data)} tables, {consumed} formula slots consumed",
              file=sys.stderr)

        # Group tables by section → topic
        sections: dict[str, dict] = {}
        order = 0
        for td in tables_data:
            section_name = td["section"]
            topic_name = td["topic"]
            section_slug = slugify(section_name)
            topic_slug = slugify(topic_name)
            table_slug = slugify(td["table_name"])
            topic_table_slug = f"{topic_slug}-{table_slug}" if topic_slug else table_slug
            order += 1

            # Write markdown file
            md_path = source_dir / subj_slug / section_slug / f"{topic_table_slug}.md"
            write_table_md(md_path, td["table_name"], td["rows"])

            # Build manifest entry. `order` stays as a local sort key so
            # topics within a section come out in document order, but it's
            # not emitted in the JSON — the array order preserves it.
            if section_slug not in sections:
                sections[section_slug] = {
                    "slug": section_slug,
                    "name": section_name,
                    "topics": {},
                }
            topics = sections[section_slug]["topics"]
            if topic_slug not in topics:
                topics[topic_slug] = {
                    "slug": topic_slug,
                    "name": topic_name,
                    "tables": [],
                    "_first_order": order,
                }
            topics[topic_slug]["tables"].append({
                "name": td["table_name"],
                "path": f"{subj_slug}/{section_slug}/{topic_table_slug}.md",
                "highlighted_rows": td["highlighted_rows"],
            })

        # Sort sections and topics
        canonical = SECTION_ORDER.get(subj_slug, [])
        ordered_sections = [sections[s] for s in canonical if s in sections]
        remaining = sorted(s for s in sections if s not in canonical)
        ordered_sections.extend(sections[s] for s in remaining)

        for sec in ordered_sections:
            topics_dict = sec.pop("topics")
            sec["topics"] = sorted(
                topics_dict.values(),
                key=lambda t: (t["_first_order"], t["name"]),
            )
            for t in sec["topics"]:
                t.pop("_first_order")

        manifest[subj_slug] = {
            "slug": subj_slug,
            "name": subj_name,
            "sections": ordered_sections,
        }

    return manifest


def main() -> None:
    root = Path(__file__).resolve().parent.parent.parent
    manifest = build_all(root)

    out_path = root / "web" / "public" / "curriculum" / "curriculum.json"
    out_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    total_tables = 0
    tables_with_hl = 0
    for subj in manifest.values():
        for sec in subj["sections"]:
            for topic in sec["topics"]:
                for table in topic["tables"]:
                    total_tables += 1
                    if table["highlighted_rows"]:
                        tables_with_hl += 1
    print(
        f"Wrote {out_path} "
        f"({out_path.stat().st_size} bytes, "
        f"{tables_with_hl}/{total_tables} tables with highlights)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
