# gallery/

One folder per science. A picture belongs to exactly one, and the folder it
sits in is the whole of the tagging:

    astronomy/20260730 M 31.jpg
    ^ science  ^ sorts    ^ name

**Nothing here is displayed.** A photo tile is the picture and nothing else —
no caption, no science pill, no date, no hover text (locked; see the repo
`CLAUDE.md` § THE WALL). So the filename is not copy, it is plumbing, and it
does three jobs:

- the **`YYYYMMDD` prefix orders the wall** — it is the date the picture joined
  the gallery, not necessarily when it was shot, and renaming it moves the tile
- the **rest of the name** becomes the `alt` text and the tile's `aria-label`,
  so a screen reader still reads it even though no one sees it
- the **folder** is the science, and the only tag there is

Drop a file in, run `python3 pipeline/scripts/build_gallery.py`, done. No YAML.

**Keep them web-sized: a long edge of 2000.** There is no thumbnail folder —
the wall and the lightbox both load these files directly, so camera-resolution
originals would be three times the page weight for no visible gain at any
display size. `sips -Z 2000 in.jpg --out in.jpg` is the whole recipe, and
`sandbox/astronomy/output/setup/collect_media.py` already does it when it copies Seestar
captures in. Full-resolution originals live outside the published site.

An `.mp4` works as a tile — it autoplays muted and loops. Give it a still frame
beside it named `<name>.poster.jpg`; that is what the tile shows before the
clip plays, and what the iOS app shows instead of the video.

A picture that lives inside a project folder stays there and is referenced from
`../gallery.yml`. Copying it here would put the same bytes in git twice, and
the build rejects that by content hash.
