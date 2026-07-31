#!/usr/bin/env python3
"""Build web/public/projects/gallery.json — the manifest behind the /projects/ wall.

Source of truth:  web/public/projects/gallery.yml
Output:           web/public/projects/gallery.json

THE WALL
--------
/projects/ is one chronological grid of every picture worth looking at. Two
kinds of tile live in it, and both come from the same YAML list:

  photo tile    a picture, or a clip. An .mp4
                autoplays muted and loops on the web; give it a still frame
                beside it named "<name>.poster.jpg" and that is what the tile
                shows before it plays, and what the iOS app shows instead.
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
  gallery/<science>/...         everything else, named
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

ONE SCIENCE PER PICTURE
-----------------------
A picture belongs to exactly one science and that science is the folder it sits
in. There is no tagging layer above it — no categories, no toys, nothing to
declare. Only two things still need a row in gallery.yml: a project card, and a
picture that lives inside a project folder and should also appear on the wall.
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
GALLERY = CONTENT / "gallery"
OUT = CONTENT / "gallery.json"

SCIENCE_SLUGS = {
    "Mathematics": "math", "Computing": "comp", "Physics": "phys",
    "Chemistry": "chem", "Biology": "bio", "Astronomy": "astro",
}
# Wall order, top of the filter row to the bottom — mirrors the Olympiads page.
SCIENCE_ORDER = ["Mathematics", "Computing", "Physics", "Chemistry", "Biology", "Astronomy"]
# Folder under gallery/ per science — the full word, matching the convention
# curriculum/source/ already uses. The folder IS the tag: a picture's science
# is where it sits, not something declared about it.
SCIENCE_FOLDERS = {name: name.lower() for name in SCIENCE_ORDER}

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]




PHOTO_EXTS = (".jpg", ".jpeg", ".png")


def project_photos(proj: Path) -> list[str]:
    """A project's shuffle-pool photos, folder-relative (`photos/setup/1.jpeg`).

    Every image under `photos/`, recursively, except `photos/data/` — those are
    handwritten data sheets, surfaced by a hand-coded grid rather than the hero
    shuffle. Mirrors the build-time walk in `pages/projects/[slug]/index.astro`;
    keep the two in step.

    Baked into gallery.json so the native app can render a project page's photo
    grid from a manifest it already loads. This used to live in technology.json,
    which was deleted 2026-07-30 along with the toy catalog.
    """
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


def caption_from(name: str) -> str:
    """'20260730 M 31.jpg' -> 'M 31'. The date prefix sorts the wall and is
    never displayed, so the caption is whatever is left of the filename."""
    stem = name.rsplit(".", 1)[0]
    return re.sub(r"^\d{8}[ _-]+", "", stem).strip()


def slug(s: str) -> str:
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def measured(rel: str, path: Path) -> tuple[str, int, int]:
    """(url, w, h) for a file. One copy, served as it is.

    There used to be a gallery/thumbs/ folder holding a long-edge-1000 copy of
    everything oversized. It was deleted 2026-07-30: the wall is around fifty
    pictures, not five hundred, and a second generated copy of each one was a
    folder to explain and keep pruned. Instead the pictures under
    gallery/<science>/ are themselves web-sized — a long edge of 2000, which is
    ample for the lightbox on any display and about a third of camera output.
    Resize on the way in, not on the way out.
    """
    w, h = image_size(path)
    return url_for(rel), w, h


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



def read_title(folder: Path) -> str:
    """A project card's caption is the project's own title — read from its
    index.md so the wall can never drift from the page it links to."""
    text = (folder / "index.md").read_text()
    m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
    return m.group(1) if m else folder.name


def build() -> dict:
    tiles: list[dict] = []
    seen_src: dict[str, str] = {}
    seen_bytes: dict[str, str] = {}

    def add(rel: str, science: str, caption: str, where: str,
            kind: str = "photo", href: str | None = None,
            photos: list[str] | None = None) -> None:
        path = CONTENT / rel
        if not path.is_file():
            raise ValueError(f"{where}: no such file {rel!r}")
        # One picture, one place on the wall — checked by path and again by
        # content, because the same capture reaching the wall under two names
        # is the failure that actually happened once already.
        if rel in seen_src:
            raise ValueError(f"{where}: {rel!r} already used by {seen_src[rel]}")
        seen_src[rel] = where
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        if digest in seen_bytes:
            raise ValueError(
                f"{where}: {rel!r} is byte-identical to {seen_bytes[digest]}. "
                "Same picture, two names — keep one.")
        seen_bytes[digest] = where

        src, w, h = measured(rel, path)
        tile = {
            "kind": kind,
            "science": science,
            "science_slug": SCIENCE_SLUGS[science],
            "caption": caption,
            "src": src,             # what the wall loads
            "full": url_for(rel),   # the original, for the viewer
            "w": w,
            "h": h,
        }
        if href:
            tile["href"] = href
        if photos:
            tile["photos"] = photos

        # Sorting only — the wall never shows a date.
        date = _filename_month(path) or _exif_month(path)
        if not date:
            raise ValueError(
                f"{where}: cannot date {rel!r} — name it 'YYYYMMDD Some Name.ext'")
        tile["date"] = date

        if path.suffix.lower() in VIDEO_EXTS:
            tile["video"] = True
            poster = path.parent / (path.stem + ".poster.jpg")
            if poster.is_file():
                purl, pw, ph = measured(str(poster.relative_to(CONTENT)), poster)
                tile["poster"] = purl
                # The still is the honest shape of the frame; a container's own
                # dimensions can disagree with its rotation matrix.
                tile["w"], tile["h"] = pw, ph

        tiles.append(tile)

    # ── 1. everything filed under gallery/<science>/ ─────────────────
    # No YAML at all for these: the folder is the science, the YYYYMMDD prefix
    # is the sort key, and the rest of the filename is the caption. Dropping a
    # file into gallery/astronomy/ puts it on the wall.
    for science, folder in SCIENCE_FOLDERS.items():
        d = GALLERY / folder
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.name.startswith(".") or not f.is_file():
                continue
            if f.suffix.lower() not in (".jpg", ".jpeg", ".png") + VIDEO_EXTS:
                continue
            if f.name.endswith(".poster.jpg"):
                continue          # a clip's still, not a tile of its own
            rel = str(f.relative_to(CONTENT))
            add(rel, science, caption_from(f.name), f"gallery/{folder}/{f.name}")

    # ── 2. gallery.yml ──────────────────────────────────────────────
    # Only two things still need it: project cards, and pictures that live
    # inside a project folder and should also appear on the wall (referenced
    # in place, never copied, so the bytes stay in git once).
    entries = yaml.safe_load(SRC.read_text()) or []
    if not isinstance(entries, list):
        raise ValueError("gallery.yml must be a YAML list")

    for i, e in enumerate(entries):
        where = f"gallery.yml[{i}]"
        science = e.get("science")
        if science not in SCIENCE_SLUGS:
            raise ValueError(
                f"{where}: science must be one of {sorted(SCIENCE_SLUGS)}, got {science!r}")
        if "folder" in e:
            proj = CONTENT / e["folder"]
            if not proj.is_dir():
                raise ValueError(f"{where}: no such project folder {e['folder']!r}")
            add(f"{e['folder']}/{e['hero']}", science,
                e.get("caption") or read_title(proj), where,
                kind="project", href=url_for(e["folder"] + "/"),
                photos=project_photos(proj))
        else:
            rel = e["src"]
            add(rel, science, e.get("caption") or caption_from(rel.split("/")[-1]), where)

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

    sciences = [
        {
            "science": name,
            "slug": SCIENCE_SLUGS[name],
            "count": sum(1 for t in tiles if t["science"] == name),
        }
        for name in SCIENCE_ORDER
    ]
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
        print(f"    {s['science']:<12} {s['count']:>3} tiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
