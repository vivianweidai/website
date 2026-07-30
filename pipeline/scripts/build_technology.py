#!/usr/bin/env python3
"""Build web/public/projects/technology.json from the YAML source of truth.

Source of truth:  web/public/projects/technology.yml
Output:           web/public/projects/technology.json

Flat schema — one entry per science, each a plain list of techs (categories):
  input:   [{science, techs: [{tech, specs, toys: [{name, description, short?}]}]}]
  output:  {"sciences": [{id, science, science_slug,
              techs: [{id, tech, specs, toys?, projects?}]}]}

There are no tech pages any more, so nothing here emits a `tech_url` or a
`hero`. Both were optional in the Swift model, so a shipped app build decodes
this file unchanged — it just stops drawing hero images and tech links.

The old topic/category grouping tiers were dropped — every science now
renders as a flat tech list, so the data carries no grouping metadata.

The `projects[]` list is the one source for tech↔project links. It's
assembled by reverse-scanning every project's `index.md`
frontmatter `tech:` array (each project declares which techs it used).
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT = ROOT / "web" / "public" / "projects"
PROJECTS = CONTENT

SCIENCES = {"Biology", "Chemistry", "Physics", "Computing", "Mathematics", "Astronomy"}
# Short slug — used for chip styling and the /projects/#<slug> column anchor.
SCIENCE_SLUGS = {
    "Biology": "bio", "Chemistry": "chem", "Physics": "phys",
    "Computing": "comp", "Mathematics": "math", "Astronomy": "astro",
}
# Folder name on disk and in URLs — full word, matching web/public/curriculum/source.
SCIENCE_FOLDERS = {
    "Biology": "biology", "Chemistry": "chemistry", "Physics": "physics",
    "Computing": "computing", "Mathematics": "mathematics", "Astronomy": "astronomy",
}


def _read_frontmatter(md_path: Path) -> dict | None:
    """Parse the YAML frontmatter at the top of a markdown file.
    Returns None when the file is missing or has no `---\\n…\\n---` block."""
    if not md_path.is_file():
        return None
    text = md_path.read_text()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    return yaml.safe_load(text[4:end]) or {}



PHOTO_EXTS = (".jpg", ".jpeg", ".png")


def photos_for_project(proj: Path) -> list[str]:
    """Return the project's shuffle-pool photos as folder-relative paths
    (e.g. `photos/setup/setup1.jpeg`).

    Mirrors the build-time walk in `pages/projects/[slug]/index.astro`:
    every image under `photos/`, recursively, except `photos/data/` — those
    are handwritten data sheets, surfaced by a hand-coded grid rather than
    the hero shuffle. Keep the two in step if either changes.

    Baked into technology.json so the native apps get the same pool from a
    manifest they already load, instead of walking the GitHub contents API
    at runtime (unauthenticated, rate-limited, and silently empty when it
    fails — which is how the in-app photo grid went blank)."""
    root = proj / "photos"
    if not root.is_dir():
        return []
    out: list[str] = []

    def walk(d: Path) -> None:
        for f in sorted(d.iterdir()):
            if f.is_dir():
                if f.parent == root and f.name == "data":
                    continue
                walk(f)
            elif f.suffix.lower() in PHOTO_EXTS:
                out.append(f"photos/{f.relative_to(root).as_posix()}")

    walk(root)
    return out


def projects_per_tech() -> dict[str, list[dict]]:
    """Scan every project's index.md and return a reverse map
    from tech name to the list of projects that reference it via the
    project's `tech:` frontmatter array. Each entry is {date, title,
    url, sciences[]}, with `date` as YYYY-MM-DD parsed from the folder's
    date prefix. Used to bake the per-tech projects list into
    technology.json so iOS/Android can render the tech page natively
    without re-scanning all projects at runtime."""
    by_tech: dict[str, list[dict]] = {}
    if not PROJECTS.is_dir():
        return by_tech
    for proj in sorted(PROJECTS.iterdir()):
        if not proj.is_dir():
            continue
        m = re.match(r"^(\d{4})(\d{2})(\d{2})", proj.name)
        if not m:
            continue
        date_iso = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        fm = _read_frontmatter(proj / "index.md")
        if not fm:
            continue
        title = fm.get("title", fm.get("project", ""))
        sciences = list(fm.get("sciences") or [])
        url = f"/projects/{urllib.parse.quote(proj.name)}/"
        photos = photos_for_project(proj)
        for t in fm.get("tech") or []:
            entry = {
                "date": date_iso,
                "title": title,
                "url": url,
                "sciences": sciences,
            }
            if photos:
                entry["photos"] = photos
            by_tech.setdefault(str(t), []).append(entry)
    return by_tech


def build() -> list[dict]:
    data = yaml.safe_load((CONTENT / "technology.yml").read_text())
    if not isinstance(data, list):
        raise ValueError("technology.yml must be a YAML list")
    proj_index = projects_per_tech()
    sciences = []
    tech_id = 0
    for i, e in enumerate(data):
        if "science" not in e:
            raise ValueError(f"science[{i}] missing 'science'")
        if e["science"] not in SCIENCES:
            raise ValueError(f"science[{i}] invalid science {e['science']!r}")
        if "techs" not in e:
            raise ValueError(f"science[{i}] ({e['science']}) missing 'techs'")

        techs_out = []
        for k, tech in enumerate(e["techs"]):
            for f in ("tech", "specs"):
                if f not in tech:
                    raise ValueError(f"science[{i}].tech[{k}] missing {f!r}")
            tech_id += 1
            t: dict = {
                "id": tech_id,
                "tech": tech["tech"],
                "specs": tech["specs"],
            }
            # Toys are inline in the YAML now — there are no tech pages left to
            # read frontmatter from, and no tech_url or hero to point at them.
            toys = []
            for toy in tech.get("toys") or []:
                if not isinstance(toy, dict) or "name" not in toy:
                    continue
                entry = {"name": toy["name"], "description": toy.get("description", "")}
                if toy.get("short"):
                    entry["short"] = toy["short"]
                toys.append(entry)
            if toys:
                t["toys"] = toys
            # Reverse-scanned projects (whose frontmatter `tech:`
            # array references this tech), newest first. Filter by science
            # too — two sciences can share a tech name (e.g. Chemistry and
            # Astronomy both have "Spectroscopy"), so a project only attaches
            # where its own sciences include this tech's science.
            projects = [p for p in proj_index.get(tech["tech"], [])
                        if e["science"] in (p.get("sciences") or [])]
            if projects:
                projects.sort(key=lambda p: p["date"], reverse=True)
                t["projects"] = projects
            techs_out.append(t)
        sciences.append({
            "id": i + 1,
            "science": e["science"],
            "science_slug": SCIENCE_SLUGS[e["science"]],
            "techs": techs_out,
        })
    return sciences


def main() -> int:
    try:
        sciences = build()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    payload = {"sciences": sciences}
    out = CONTENT / "technology.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    n_techs = sum(len(s["techs"]) for s in sciences)
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"  {len(sciences)} sciences, {n_techs} techs")
    for s in sciences:
        print(f"    {s['science']}: {len(s['techs'])} techs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
