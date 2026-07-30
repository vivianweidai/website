# gallery/

`photos/` holds every picture and clip on the wall that does not belong to a
project — a good frame from an afternoon of messing about, an instrument that
just arrived, a failure worth keeping.

One flat folder. The filename carries the date:

    20260730 M 31.jpg
    20260724 The Sun.mp4

That `YYYYMMDD` prefix is the filing system — the same convention the project
folders use — so the folder sorts itself and a file states its own date without
a sidecar. `build_gallery.py` reads the month straight off the name.

A picture that lives inside a project folder stays there and is referenced in
place from `../gallery.yml`; copying it here would put the same bytes in git
twice, and the build rejects that by content hash.

`thumbs/` is generated — never edit it, never add to it. `build_gallery.py`
writes a long-edge-1000 copy of anything oversized and deletes thumbs whose row
has gone. The originals total ~58 MB and a gallery is exactly the page that
requests all of them; the thumbs are ~9 MB.

Captions and tags live in `../gallery.yml`, not here.
