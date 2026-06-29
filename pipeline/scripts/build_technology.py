#!/usr/bin/env python3
"""Build public/research/technology.json from the YAML source of truth.

Source of truth:  public/research/technology.yml
Output:           public/research/technology.json

Three-level schema:
  topics[] → categories[] → techs[]

Output shape:
  {"topics": [{id, science, science_slug, topic,
    categories: [{id, category,
      techs: [{id, tech, specs, available, tech_url, hero?, url?,
              toys?: [{name, description}],
              projects?: [{date, title, url, sciences[]}]}]
    }]
  }]}

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
CONTENT = ROOT / "public" / "research"
PROJECTS = CONTENT / "projects"
TECH_DIR = CONTENT / "technology"

SCIENCES = {"Biology", "Chemistry", "Physics", "Computing", "Mathematics", "Astronomy"}
# Short slug — used for chip styling and the /research/#<slug> column anchor.
SCIENCE_SLUGS = {
    "Biology": "bio", "Chemistry": "chem", "Physics": "phys",
    "Computing": "comp", "Mathematics": "math", "Astronomy": "astro",
}
# Folder name on disk and in URLs — full word, matching public/curriculum/source.
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
        for t in fm.get("tech") or []:
            by_tech.setdefault(str(t), []).append({
                "date": date_iso,
                "title": title,
                "url": url,
                "sciences": sciences,
            })
    return by_tech


def build() -> list[dict]:
    data = yaml.safe_load((CONTENT / "technology.yml").read_text())
    if not isinstance(data, list):
        raise ValueError("technology.yml must be a YAML list")
    proj_index = projects_per_tech()
    topics = []
    cat_id = tech_id = 0
    for i, e in enumerate(data):
        for f in ("science", "topic", "categories"):
            if f not in e:
                raise ValueError(f"topic[{i}] missing {f!r}")
        if e["science"] not in SCIENCES:
            raise ValueError(f"topic[{i}] invalid science {e['science']!r}")

        cats_out = []
        for j, cat in enumerate(e["categories"]):
            if "category" not in cat:
                raise ValueError(f"topic[{i}].cat[{j}] missing 'category'")
            cat_id += 1
            techs_out = []
            for k, tech in enumerate(cat.get("techs") or []):
                for f in ("tech", "specs"):
                    if f not in tech:
                        raise ValueError(f"topic[{i}].cat[{j}].tech[{k}] missing {f!r}")
                tech_id += 1
                folder = SCIENCE_FOLDERS[e["science"]]
                t: dict = {
                    "id": tech_id,
                    "tech": tech["tech"],
                    "specs": tech["specs"],
                    "available": 1 if tech.get("available") else 0,
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
                if tech.get("url"):
                    t["url"] = tech["url"]
                if "tested" in tech:
                    t["tested"] = bool(tech["tested"])
                # Reverse-scanned projects (whose frontmatter `tech:`
                # array references this tech), newest first.
                projects = list(proj_index.get(tech["tech"], []))
                if projects:
                    projects.sort(key=lambda p: p["date"], reverse=True)
                    t["projects"] = projects
                techs_out.append(t)
            cats_out.append({
                "id": cat_id,
                "category": cat["category"],
                "techs": techs_out,
            })
        topics.append({
            "id": i + 1,
            "science": e["science"],
            "science_slug": SCIENCE_SLUGS[e["science"]],
            "topic": e["topic"],
            "categories": cats_out,
        })
    return topics


def main() -> int:
    try:
        topics = build()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    payload = {"topics": topics}
    out = CONTENT / "technology.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    n_cats = sum(len(t["categories"]) for t in topics)
    n_techs = sum(len(cat["techs"]) for t in topics for cat in t["categories"])
    avail = sum(1 for t in topics for cat in t["categories"]
                for tech in cat["techs"] if tech["available"])
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"  {len(topics)} topics, {n_cats} categories, {n_techs} techs")
    by = {}
    for t in topics:
        by.setdefault(t["science"], [0, 0, 0])
        by[t["science"]][0] += 1
        by[t["science"]][1] += len(t["categories"])
        by[t["science"]][2] += sum(len(cat["techs"]) for cat in t["categories"])
    for s in sorted(by):
        print(f"    {s}: {by[s][0]} topics, {by[s][1]} cats, {by[s][2]} techs")
    print(f"  available: {avail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
