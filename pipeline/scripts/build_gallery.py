#!/usr/bin/env python3
"""Build web/public/projects/gallery.json — the manifest behind the /projects/ wall.

Source of truth:  web/public/projects/gallery.yml
Output:           web/public/projects/gallery.json

THE WALL
--------
/projects/ is one chronological grid of every picture worth looking at. Two
kinds of tile live in it, and both come from the same YAML list:

  photo tile    a picture. `src:` points at a file.
  project card  a link to a project page. `folder:` names the project folder;
                `hero:` picks which of its images fronts the card. The title
                is read from that project's index.md, never retyped here.

WHERE THE PIXELS LIVE
---------------------
`src:` / `hero:` are paths relative to web/public/projects/ — i.e. exactly
what follows /projects/ in the URL. Two homes, and the distinction is the
whole filing system:

  <YYYYMMDD Project Name>/...   a picture that belongs to a project. Reference
                                it in place; never copy it into gallery/, or
                                the same bytes land in git twice.
  gallery/<YYYY-MM>/...         a picture that belongs to no project — a good
                                shot from an afternoon of messing about. One
                                folder per month, created on demand.

ADDING PICTURES
---------------
Drop files into gallery/<YYYY-MM>/ (make the folder if it's a new month), give
them short kebab-case names, add a row each to gallery.yml, and run this. The
script fails loudly on a missing file or an unknown science, so a typo is a
build error rather than a hole in the wall.

TAGS
----
`science:` is required and is one of the six. `toy:` is optional and must match
a toy `short` (or full `name`) that the science actually owns in
technology.json — the wall's second filter row is built from that same list, so
a tag here and a chip on the home page are guaranteed to be the same word.
Leave `toy:` off when no instrument we currently own is what the picture is
about: the retired SIL instruments (the Nicolet FT-IR, the OptiMelt) are the
reason that case exists.
"""

from __future__ import annotations

import json
import re
import struct
import sys
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT = ROOT / "web" / "public" / "projects"
SRC = CONTENT / "gallery.yml"
OUT = CONTENT / "gallery.json"
TECH_JSON = CONTENT / "technology.json"

SCIENCE_SLUGS = {
    "Mathematics": "math", "Computing": "comp", "Physics": "phys",
    "Chemistry": "chem", "Biology": "bio", "Astronomy": "astro",
}
# Wall order, top of the filter row to the bottom — mirrors the Olympiads page.
SCIENCE_ORDER = ["Mathematics", "Computing", "Physics", "Chemistry", "Biology", "Astronomy"]

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def slug(s: str) -> str:
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def url_for(rel: str) -> str:
    """web/public/projects-relative path → absolute site URL."""
    return "/projects/" + "/".join(urllib.parse.quote(p) for p in rel.split("/"))


# ── image dimensions ─────────────────────────────────────────────────
# The wall is a CSS-grid masonry: each tile spans a number of grid rows
# computed from its aspect ratio, so every dimension has to be known at build
# time or the layout reflows as images stream in. Parsed from file headers
# rather than via Pillow — this repo has no image dependency and does not
# need one for two integers.

def _png_size(fh) -> tuple[int, int] | None:
    fh.seek(0)
    if fh.read(8) != b"\x89PNG\r\n\x1a\n":
        return None
    fh.seek(16)
    w, h = struct.unpack(">II", fh.read(8))
    return w, h


def _jpeg_size(fh) -> tuple[int, int] | None:
    fh.seek(0)
    if fh.read(2) != b"\xff\xd8":
        return None
    while True:
        b = fh.read(1)
        if not b:
            return None
        if b != b"\xff":
            continue
        # Skip fill bytes, then read the marker.
        marker = fh.read(1)
        while marker == b"\xff":
            marker = fh.read(1)
        if not marker:
            return None
        m = marker[0]
        # Standalone markers carry no length payload.
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            continue
        length = struct.unpack(">H", fh.read(2))[0]
        # SOF0-SOF15, excluding the four that aren't frame headers.
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
            fh.read(1)  # sample precision
            h, w = struct.unpack(">HH", fh.read(4))
            return w, h
        fh.seek(length - 2, 1)


def image_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        size = _png_size(fh) or _jpeg_size(fh)
    if not size:
        raise ValueError(f"could not read image dimensions from {path}")
    return size


# ── capture date ─────────────────────────────────────────────────────
# The wall is chronological, so every tile needs a month. Rather than hand-type
# one per row, read the camera's own EXIF DateTimeOriginal — a photo dropped
# into gallery/ dates itself. `date:` in the YAML overrides it, and is required
# for images that have no EXIF at all (generated plots, screenshots).

_EXIF_FMTSIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 9: 4, 10: 8}


def _exif_month(path: Path) -> str | None:
    """Return 'YYYY-MM' from EXIF DateTimeOriginal (falling back to the IFD0
    DateTime), or None when the file carries no EXIF."""
    if path.suffix.lower() not in (".jpg", ".jpeg"):
        return None
    with path.open("rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            return None
        # Walk JPEG segments looking for APP1/Exif.
        blob = None
        while True:
            head = fh.read(2)
            if len(head) < 2 or head[0] != 0xFF:
                return None
            marker = head[1]
            if marker == 0xDA:  # start of scan — no EXIF before the image data
                return None
            length = struct.unpack(">H", fh.read(2))[0]
            payload = fh.read(length - 2)
            if marker == 0xE1 and payload[:6] == b"Exif\x00\x00":
                blob = payload[6:]
                break

    if not blob or len(blob) < 8:
        return None
    endian = "<" if blob[:2] == b"II" else ">" if blob[:2] == b"MM" else None
    if endian is None:
        return None

    def u16(off): return struct.unpack(endian + "H", blob[off:off + 2])[0]
    def u32(off): return struct.unpack(endian + "I", blob[off:off + 4])[0]

    def read_ifd(offset: int) -> dict[int, int]:
        """tag → value-or-offset, for the tags we care about."""
        tags: dict[int, int] = {}
        if offset + 2 > len(blob):
            return tags
        for i in range(u16(offset)):
            e = offset + 2 + i * 12
            if e + 12 > len(blob):
                break
            tag, fmt, count = u16(e), u16(e + 2), u32(e + 4)
            size = _EXIF_FMTSIZE.get(fmt, 0) * count
            tags[tag] = u32(e + 8) if size > 4 else e + 8
        return tags

    def ascii_at(off: int) -> str:
        end = blob.find(b"\x00", off)
        return blob[off:end if end >= 0 else off + 19].decode("ascii", "replace")

    try:
        ifd0 = read_ifd(u32(4))
        stamp = None
        if 0x8769 in ifd0:  # Exif sub-IFD → DateTimeOriginal
            sub = read_ifd(ifd0[0x8769])
            if 0x9003 in sub:
                stamp = ascii_at(sub[0x9003])
        if not stamp and 0x0132 in ifd0:  # plain DateTime
            stamp = ascii_at(ifd0[0x0132])
    except (struct.error, IndexError):
        return None

    m = re.match(r"(\d{4}):(\d{2}):", stamp or "")
    return f"{m.group(1)}-{m.group(2)}" if m else None


# ── toy vocabulary ───────────────────────────────────────────────────

def toys_by_science() -> dict[str, list[dict]]:
    """science name → the toys it owns, deduped by display label, in
    technology.json order. This is the same list the home page's Projects tab
    renders, and it becomes the wall's second filter row."""
    data = json.loads(TECH_JSON.read_text())
    out: dict[str, list[dict]] = {}
    for sci in data["sciences"]:
        seen: set[str] = set()
        toys = []
        for tech in sci["techs"]:
            for toy in tech.get("toys", []):
                label = toy.get("short") or toy["name"]
                if label in seen:
                    continue
                seen.add(label)
                toys.append({"label": label, "name": toy["name"], "slug": slug(label), "count": 0})
        out[sci["science"]] = toys
    return out


def read_title(folder: Path) -> str:
    """A project card's caption is the project's own title — read from its
    index.md so the wall can never drift from the page it links to."""
    text = (folder / "index.md").read_text()
    m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
    return m.group(1) if m else folder.name


def build() -> dict:
    entries = yaml.safe_load(SRC.read_text())
    if not isinstance(entries, list):
        raise ValueError("gallery.yml must be a YAML list")

    catalog = toys_by_science()
    tiles = []

    for i, e in enumerate(entries):
        where = f"gallery.yml[{i}]"
        science = e.get("science")
        if science not in SCIENCE_SLUGS:
            raise ValueError(f"{where}: science must be one of {sorted(SCIENCE_SLUGS)}, got {science!r}")

        tile: dict = {
            "science": science,
            "science_slug": SCIENCE_SLUGS[science],
        }

        if "folder" in e:
            folder = CONTENT / e["folder"]
            if not folder.is_dir():
                raise ValueError(f"{where}: no such project folder {e['folder']!r}")
            rel = f"{e['folder']}/{e['hero']}"
            tile["caption"] = e.get("caption") or read_title(folder)
            tile["href"] = url_for(e["folder"] + "/")
            tile["kind"] = "project"
        else:
            rel = e["src"]
            tile["caption"] = e.get("caption", "")
            tile["kind"] = "photo"

        path = CONTENT / rel
        if not path.is_file():
            raise ValueError(f"{where}: no such file {rel!r}")
        w, h = image_size(path)
        tile["src"] = url_for(rel)
        tile["w"], tile["h"] = w, h

        # Explicit `date:` wins; otherwise take the month off the camera.
        date = str(e["date"]) if e.get("date") else _exif_month(path)
        if not date:
            raise ValueError(
                f"{where}: {rel!r} has no EXIF date — add an explicit `date: YYYY-MM`")
        if not re.fullmatch(r"\d{4}-\d{2}", date):
            raise ValueError(f"{where}: date must be YYYY-MM, got {date!r}")
        tile["date"] = date
        tile["date_label"] = f"{MONTHS[int(date[5:7]) - 1]} {date[:4]}"

        if e.get("note"):
            tile["note"] = e["note"]

        toy = e.get("toy")
        if toy:
            match = next((t for t in catalog.get(science, [])
                          if toy in (t["label"], t["name"])), None)
            if not match:
                owned = ", ".join(t["label"] for t in catalog.get(science, []))
                raise ValueError(f"{where}: {science} owns no toy {toy!r}. Owned: {owned}")
            tile["toy"] = match["label"]
            tile["toy_slug"] = match["slug"]
            match["count"] += 1

        tiles.append(tile)

    # Newest first. Ties keep gallery.yml order, so a month's tiles can be
    # hand-arranged for how they sit next to each other on the grid.
    tiles.sort(key=lambda t: t["date"], reverse=True)

    sciences = []
    for name in SCIENCE_ORDER:
        sciences.append({
            "science": name,
            "slug": SCIENCE_SLUGS[name],
            "count": sum(1 for t in tiles if t["science"] == name),
            "toys": catalog.get(name, []),
        })
    return {"tiles": tiles, "sciences": sciences}


def main() -> int:
    try:
        payload = build()
    except (ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  {len(payload['tiles'])} tiles "
          f"({sum(1 for t in payload['tiles'] if t['kind'] == 'project')} project cards)")
    for s in payload["sciences"]:
        tagged = sum(t["count"] for t in s["toys"])
        print(f"    {s['science']:<12} {s['count']:>3} tiles, "
              f"{len(s['toys'])} toys ({tagged} tagged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
