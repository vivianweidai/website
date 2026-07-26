#!/usr/bin/env python3
"""Build web/public/research/technology.json from the YAML source of truth.

Source of truth:  web/public/research/technology.yml
Output:           web/public/research/technology.json

Flat schema — one entry per science, each a plain list of techs:
  input:   [{science, techs: [{tech, specs}]}]
  output:  {"sciences": [{id, science, science_slug,
              techs: [{id, tech, specs, tech_url, hero?,
                      toys?: [{name, description, short?, chip?, url?}],
                      projects?: [{date, title, url, sciences[], photos?[]}]}]
          }]}

The old topic/category grouping tiers were dropped — every science now
renders as a flat tech list, so the data carries no grouping metadata.

The `projects[]` list is the one source for tech↔project links. It's
assembled by reverse-scanning every research project's `index.md`
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
CONTENT = ROOT / "web" / "public" / "research"
PROJECTS = CONTENT / "projects"
TECH_DIR = CONTENT / "technology"

SCIENCES = {"Biology", "Chemistry", "Physics", "Computing", "Mathematics", "Astronomy"}
# Short slug — used for chip styling and the /research/#<slug> column anchor.
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


def hero_for_tech(science_folder: str, tech_name: str) -> str | None:
    """Return absolute hero-image URL for a tech by reading its index.md
    frontmatter (`hero:` field). Returns None when no tech folder exists yet
    or when the frontmatter has no hero. Relative paths in frontmatter are
    resolved against the tech folder's URL."""
    fm = _read_frontmatter(TECH_DIR / science_folder / tech_name / "index.md")
    if not fm:
        return None
    hero = fm.get("hero")
    if not hero:
        return None
    if hero.startswith(("/", "http://", "https://")):
        return hero
    base = f"/research/technology/{science_folder}/{urllib.parse.quote(tech_name)}/"
    return base + urllib.parse.quote(hero)


def toys_for_tech(science_folder: str, tech_name: str) -> list[dict]:
    """Return the Toys list for a tech by reading its index.md frontmatter
    (`toys:` array of {name, description}). Returns [] when no tech folder
    exists yet or the frontmatter has no toys. Baked into technology.json
    so iOS/Android render the same Toys list the website shows from the
    tech-page frontmatter."""
    fm = _read_frontmatter(TECH_DIR / science_folder / tech_name / "index.md")
    if not fm:
        return []
    toys = fm.get("toys")
    if not isinstance(toys, list):
        return []
    out = []
    for toy in toys:
        if not isinstance(toy, dict) or "name" not in toy:
            continue
        entry = {
            "name": toy["name"],
            "description": toy.get("description", ""),
        }
        if toy.get("url"):
            entry["url"] = toy["url"]
        if toy.get("short"):
            entry["short"] = toy["short"]
        # Only emit when explicitly hidden; default (shown) stays implicit.
        if toy.get("chip") is False:
            entry["chip"] = False
        out.append(entry)
    return out


PHOTO_EXTS = (".jpg", ".jpeg", ".png")


def photos_for_project(proj: Path) -> list[str]:
    """Return the project's shuffle-pool photos as folder-relative paths
    (e.g. `photos/setup/setup1.jpeg`).

    Mirrors the build-time walk in `pages/research/projects/[slug]/index.astro`:
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
    """Scan every research project's index.md and return a reverse map
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
        url = f"/research/projects/{urllib.parse.quote(proj.name)}/"
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

        folder = SCIENCE_FOLDERS[e["science"]]
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
                "tech_url": (
                    f"/research/technology/{folder}/"
                    f"{urllib.parse.quote(tech['tech'])}/"
                ),
            }
            hero = hero_for_tech(folder, tech["tech"])
            if hero:
                t["hero"] = hero
            toys = toys_for_tech(folder, tech["tech"])
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
