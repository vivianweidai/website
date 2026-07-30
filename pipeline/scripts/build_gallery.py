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
  gallery/photos/...            everything else, in one flat folder, named
                                "YYYYMMDD Some Name.jpg". The date prefix is
                                the filing system — same convention the project
                                folders use — so the folder sorts itself and a
                                file states its own date without a sidecar.

ADDING PICTURES
---------------
Drop files into gallery/photos/ named "YYYYMMDD Some Name.ext", add a row each
to gallery.yml for the caption and tags, and run this. The script fails loudly
on a missing file, an unknown science, an unowned toy, or the same bytes used
twice, so a mistake is a build error rather than a hole in the wall.

Video works the same way. An .mp4 tile autoplays muted and loops; its
dimensions come from the MP4 header and it is served without re-encoding.

TAGS
----
`science:` is required and is one of the six.

`toy:` names the specific instrument. It must match a toy `short` (or full
`name`) the science owns in technology.json, it shows in the tile's caption,
and it determines the tile's category. Leave it off when no instrument we
currently own is what the picture is about — the retired shared-lab
instruments (Nicolet FT-IR, OptiMelt) are why that case exists.

`tech:` is the CATEGORY the wall filters on (Mechanics, Genomics, Measurements).
Normally derived from `toy:`; give it explicitly only for a picture that belongs
to a category but to no instrument we own. The wall's second filter row and the
home page's Projects tab are both this same category list, so a tag in one place
and a link in the other are guaranteed to be the same word.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
import subprocess
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


THUMBS = CONTENT / "gallery" / "thumbs"
THUMB_EDGE = 1000    # px on the long edge — a landscape tile spans two
                     # columns (~450 CSS px), so this keeps it retina-sharp
THUMB_BYTES = 200_000  # anything smaller than this is already web-sized
made: set[str] = set()  # thumbs this run touched; the rest get pruned


def slug(s: str) -> str:
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def thumbnail(rel: str, path: Path) -> tuple[str, int, int]:
    """Return (url, w, h) for the image the wall should actually load.

    The originals are camera-resolution — 57 MB across the whole wall, and a
    gallery is exactly the page where every one of them ends up requested.
    So each oversized source gets a long-edge-1000 copy under gallery/thumbs/,
    generated with macOS `sips` (already on the box, no image dependency to
    install) and committed alongside everything else. Files that are already
    web-sized are served as they are.

    Thumbs are regenerated only when missing or older than their source, so
    a normal run does no work.
    """
    w, h = image_size(path)
    # A clip is served as it is — `sips` cannot resize video, and re-encoding
    # would break the byte-for-byte rule the capture galleries run on.
    if path.suffix.lower() in VIDEO_EXTS:
        return url_for(rel), w, h
    if max(w, h) <= THUMB_EDGE and path.stat().st_size <= THUMB_BYTES:
        return url_for(rel), w, h

    stem = slug(rel.rsplit(".", 1)[0])[:48]
    name = f"{stem}-{hashlib.sha1(rel.encode()).hexdigest()[:6]}{path.suffix.lower()}"
    out = THUMBS / name
    THUMBS.mkdir(parents=True, exist_ok=True)

    if not out.is_file() or out.stat().st_mtime < path.stat().st_mtime:
        r = subprocess.run(
            ["sips", "-Z", str(THUMB_EDGE), str(path), "--out", str(out)],
            capture_output=True, text=True,
        )
        if r.returncode != 0 or not out.is_file():
            raise ValueError(f"sips failed on {rel}: {r.stderr.strip() or r.stdout.strip()}")

    made.add(name)
    tw, th = image_size(out)
    return url_for(f"gallery/thumbs/{name}"), tw, th


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


def _mp4_size(path: Path) -> tuple[int, int] | None:
    """(w, h) from the first video track's tkhd box, honouring a rotation matrix.

    Videos are tiles too — the Seestar's solar clip is the one moving thing on
    the wall — and the masonry needs their aspect ratio at build time exactly
    like a photo's. Walking the box tree costs thirty lines and saves adding
    ffmpeg as a build dependency."""
    data = path.read_bytes()

    def walk(start: int, end: int) -> tuple[int, int] | None:
        i = start
        while i + 8 <= end:
            size = struct.unpack(">I", data[i:i + 4])[0]
            typ = data[i + 4:i + 8]
            body = i + 8
            if size == 1:  # 64-bit extended size
                size = struct.unpack(">Q", data[i + 8:i + 16])[0]
                body = i + 16
            elif size == 0:
                size = end - i
            if size < 8:
                return None
            if typ in (b"moov", b"trak"):
                got = walk(body, i + size)
                if got:
                    return got
            elif typ == b"tkhd":
                ver = data[body]
                p = body + 4 + (32 if ver == 1 else 20)  # times, track id, duration
                p += 8 + 2 + 2 + 2 + 2                   # reserved, layer, group, volume, reserved
                mat = struct.unpack(">9i", data[p:p + 36])
                p += 36
                w, h = (v / 65536.0 for v in struct.unpack(">II", data[p:p + 8]))
                if w and h:
                    # a and d zero with b or c set is a 90/270 degree rotation.
                    if mat[0] == 0 and mat[4] == 0 and (mat[1] or mat[3]):
                        w, h = h, w
                    return int(round(w)), int(round(h))
            i += size
        return None

    return walk(0, len(data))


VIDEO_EXTS = (".mp4", ".m4v", ".mov")


def image_size(path: Path) -> tuple[int, int]:
    if path.suffix.lower() in VIDEO_EXTS:
        size = _mp4_size(path)
    else:
        with path.open("rb") as fh:
            size = _png_size(fh) or _jpeg_size(fh)
    if not size:
        raise ValueError(f"could not read dimensions from {path}")
    return size


# ── capture date ─────────────────────────────────────────────────────
# The wall is chronological, so every tile needs a month, and there are three
# ways to get one — in this order:
#
#   1. an explicit `date: YYYY-MM` in the row, which always wins
#   2. a YYYYMMDD prefix on the filename, or failing that on any folder above
#      it — which covers gallery/photos/ by its naming convention and every
#      generated plot by the project folder it sits in
#   3. the camera's own EXIF DateTimeOriginal, for project photos still under
#      their original camera names
#
# Between them, a row almost never needs to state a date by hand.

def _filename_month(path: Path) -> str | None:
    """'YYYY-MM' from a 'YYYYMMDD Some Name.ext' name.

    Checks the file itself, then walks up its directories — which is what dates
    a generated plot sitting in `20260420 UV-Vis Spectroscopy/output/images/`.
    Same YYYYMMDD prefix, whether it is on a file or on a project folder."""
    for part in [path.name] + [p.name for p in path.parents]:
        m = re.match(r"(\d{4})(\d{2})\d{2}(?:[ _-]|$)", part)
        if m:
            return f"{m.group(1)}-{m.group(2)}"
    return None


_EXIF_FMTSIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 9: 4, 10: 8}


def _exif_month(path: Path) -> str | None:
    """Return 'YYYY-MM' from EXIF DateTimeOriginal (falling back to the IFD0
    DateTime), or None when the file carries no EXIF."""
    if path.suffix.lower() not in (".jpg", ".jpeg"):
        return None  # PNGs and video carry no EXIF; those rows need an explicit date
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

def catalog_by_science() -> tuple[dict[str, list[dict]], dict[str, dict[str, str]]]:
    """Read technology.json into the two lookups the wall needs.

    Returns (techs, toy_to_tech):
      techs        science → its categories, each {label, slug, count, toys[]},
                   with toys nested underneath. The wall filters in three
                   tiers — science, then category, then a single toy — so the
                   default view stays a short menu of four categories rather
                   than eleven instruments, and the fine-grained tags are still
                   one click away. Picking a category implies every toy in it.
      toy_to_tech  science → {toy label → category label}, for rolling a
                   gallery row's instrument up to its category. Within a
                   science each toy sits under exactly one category, so the
                   rollup is unambiguous.
    """
    data = json.loads(TECH_JSON.read_text())
    techs: dict[str, list[dict]] = {}
    toy_to_tech: dict[str, dict[str, str]] = {}
    for sci in data["sciences"]:
        rows = []
        mapping: dict[str, str] = {}
        for tech in sci["techs"]:
            seen: set[str] = set()
            toys = []
            for toy in tech.get("toys", []):
                label = toy.get("short") or toy["name"]
                mapping.setdefault(label, tech["tech"])
                mapping.setdefault(toy["name"], tech["tech"])
                if label in seen:
                    continue
                seen.add(label)
                toys.append({"label": label, "name": toy["name"],
                             "slug": slug(label), "count": 0})
            rows.append({"label": tech["tech"], "slug": slug(tech["tech"]),
                         "count": 0, "toys": toys})
        techs[sci["science"]] = rows
        toy_to_tech[sci["science"]] = mapping
    return techs, toy_to_tech


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

    techs, toy_to_tech = catalog_by_science()
    tiles = []
    seen_src: dict[str, int] = {}
    seen_bytes: dict[str, int] = {}

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
        # One picture, one place on the wall. This mostly catches a project
        # card whose hero is also listed as a standalone tile — which reads as
        # the grid stuttering rather than as two entries.
        if rel in seen_src:
            raise ValueError(
                f"{where}: {rel!r} is already used by gallery.yml[{seen_src[rel]}]. "
                "A project card's hero should not also be a photo tile.")
        seen_src[rel] = i
        # …and again by content, because the same capture reaching the wall
        # under two names is the failure that actually happened: a staged copy
        # was ingested next to the original it had been copied from.
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        if digest in seen_bytes:
            raise ValueError(
                f"{where}: {rel!r} is byte-identical to gallery.yml[{seen_bytes[digest]}]. "
                "Same picture, two names — keep one.")
        seen_bytes[digest] = i
        src, w, h = thumbnail(rel, path)
        tile["src"] = src            # what the wall loads
        tile["full"] = url_for(rel)  # the original, for anything that wants it
        tile["w"], tile["h"] = w, h

        date = str(e["date"]) if e.get("date") else (_filename_month(path) or _exif_month(path))
        if not date:
            raise ValueError(
                f"{where}: cannot date {rel!r} — name it 'YYYYMMDD …' or add `date: YYYY-MM`")
        if not re.fullmatch(r"\d{4}-\d{2}", date):
            raise ValueError(f"{where}: date must be YYYY-MM, got {date!r}")
        tile["date"] = date
        tile["date_label"] = f"{MONTHS[int(date[5:7]) - 1]} {date[:4]}"

        if path.suffix.lower() in VIDEO_EXTS:
            tile["video"] = True

        if e.get("note"):
            tile["note"] = e["note"]

        # `toy:` names the specific instrument and shows in the caption.
        # `tech:` is the category the wall filters on, and is normally derived
        # from the toy — give it explicitly only when a picture belongs to a
        # category but to no instrument we own (the retired FT-IR work).
        toy = e.get("toy")
        tech_name = e.get("tech")
        if toy:
            mapping = toy_to_tech.get(science, {})
            if toy not in mapping:
                owned = ", ".join(sorted({v for v in mapping}))
                raise ValueError(f"{where}: {science} owns no toy {toy!r}. Owned: {owned}")
            tile["toy"] = toy
            tech_name = tech_name or mapping[toy]
        if tech_name:
            match = next((t for t in techs.get(science, []) if t["label"] == tech_name), None)
            if not match:
                have = ", ".join(t["label"] for t in techs.get(science, []))
                raise ValueError(f"{where}: {science} has no category {tech_name!r}. Has: {have}")
            tile["tech"] = match["label"]
            tile["tech_slug"] = match["slug"]
            match["count"] += 1
            if toy:
                hit = next((x for x in match["toys"] if x["label"] == toy or x["name"] == toy), None)
                if hit:
                    tile["toy_slug"] = hit["slug"]
                    hit["count"] += 1

        tiles.append(tile)

    # Newest month first — but *within* a month, deal the tiles out round-robin
    # across the sciences instead of keeping gallery.yml order. Without this a
    # busy month in one science (a week of clear skies, say) lands as a slab of
    # fifteen near-identical frames at the top of the wall. Dealing them out
    # mixes the grid without touching the chronology, since the date only
    # resolves to a month anyway. Order within one science is preserved, so
    # a run of related shots still reads in sequence.
    def interleave(group: list[dict]) -> list[dict]:
        queues = [[t for t in group if t["science"] == name] for name in SCIENCE_ORDER]
        out = []
        while any(queues):
            for q in queues:
                if q:
                    out.append(q.pop(0))
        return out

    by_month: dict[str, list[dict]] = {}
    for t in tiles:
        by_month.setdefault(t["date"], []).append(t)
    tiles = [t for month in sorted(by_month, reverse=True) for t in interleave(by_month[month])]

    sciences = []
    for name in SCIENCE_ORDER:
        sciences.append({
            "science": name,
            "slug": SCIENCE_SLUGS[name],
            "count": sum(1 for t in tiles if t["science"] == name),
            "techs": techs.get(name, []),
        })
    if THUMBS.is_dir():
        for f in THUMBS.iterdir():
            if f.name not in made:
                f.unlink()

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
        tagged = sum(t["count"] for t in s["techs"])
        print(f"    {s['science']:<12} {s['count']:>3} tiles, "
              f"{len(s['techs'])} categories ({tagged} tagged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
