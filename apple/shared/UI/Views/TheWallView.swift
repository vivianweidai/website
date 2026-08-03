import SwiftUI
import ScienceCore

/// The projects wall, matching the website's /projects/ page: one
/// chronological grid of every picture worth looking at, newest first, with
/// photos, clips and project cards interleaved. Source of truth is
/// `web/public/projects/thewall/thewall.json`, the same manifest the website builds
/// from — so a row added to `thewall.yml` appears here without an app release.
///
/// Deliberately the same shape as the web page and no more: a filter row, the
/// grid, and nothing below the fold. Replaced the old tech browser 2026-07-30
/// when the website dropped its per-tech pages; that view had been reading
/// `hero` and `tech_url` out of technology.json — a file since deleted along
/// with the whole toy catalog.
///
/// Three things the web wall does that this now does too (2026-07-30):
///   • **Landscape tiles span two columns.** A 4:3 photo at one column is a
///     stamp; a portrait frame gets its presence from its own aspect ratio.
///   • **A photo tile carries no text.** Caption and science pill belong to
///     project cards; the picture is the whole content of a photo.
///   • **A clip plays in place**, muted and looping, and opens with controls.
///
/// One thing it deliberately does *not* copy: the web's filter pill row. The
/// filter is the toolbar menu the Olympiads tab already uses — the phone has
/// its own idiom for this and the wall would rather have the screen.
struct TheWallView: View {
    @State private var store = ContentStore.shared
    /// Science slug, or nil for "All" — the same one-tier filter the web wall
    /// settled on after a category row and a toy row were both removed.
    @State private var scienceSlug: String?
    @State private var viewer: TheWallViewerImages?
    @State private var clip: TheWallClip?
    /// Width of the scroll container, read from a background GeometryReader so
    /// the ScrollView can stay a direct child of the NavigationStack — see the
    /// note in `content(wall:)`.
    @State private var containerWidth: CGFloat = 0

    var body: some View {
        NavigationStack {
            Group {
                if let wall = store.wall {
                    content(wall: wall)
                } else if let errorMessage = store.wallError {
                    ErrorState(message: errorMessage)
                } else {
                    LoadingState(
                        title: "Loading projects",
                        subtitle: "Fetching the wall from vivianweidai.com."
                    )
                }
            }
            .navigationTitle("Projects")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    ScienceFilterMenu(
                        selected: $scienceSlug,
                        sciences: store.wall?.sciences ?? []
                    )
                }
            }
            .refreshable { await store.refreshAll() }
        }
        #if os(iOS)
        .fullScreenCover(item: $viewer) { images in
            ImageViewerView(sources: images.sources, index: images.index)
        }
        .fullScreenCover(item: $clip) { clip in
            ClipPlayerView(url: clip.url)
        }
        #endif
    }

    private func visibleTiles(_ wall: TheWallResponse) -> [TheWallTile] {
        guard let scienceSlug else { return wall.tiles }
        return wall.tiles.filter { $0.scienceSlug == scienceSlug }
    }

    @ViewBuilder
    private func content(wall: TheWallResponse) -> some View {
        let tiles = visibleTiles(wall)
        // Photo tiles only, in display order — the viewer pages through what
        // is currently on screen, so a filtered wall stays inside its filter,
        // and project cards (links to a write-up) and clips are skipped the
        // way they are on the web.
        let photos = tiles.filter { !$0.isProject && !$0.isVideo }

        // ⚠️ The ScrollView must be a DIRECT child here, exactly as OlympiadsView
        // has it. Wrapping it in a GeometryReader (which is how this measured its
        // width until 2026-08-01) stops the navigation bar from tracking the
        // scroll properly: the large title collapsed to the small CENTRED inline
        // style the moment you scrolled, while Olympiads kept its left-aligned
        // large title. Width is measured from a zero-cost background instead,
        // which does not participate in layout.
        let metrics = WallMetrics(availableWidth: containerWidth)

        ScrollView {
            LazyVStack(spacing: WallMetrics.gutter) {
                if tiles.isEmpty {
                    Text("Nothing here yet.")
                        .font(.system(size: 14))
                        .foregroundStyle(.secondary)
                        .italic()
                        .padding(.top, 40)
                        .frame(maxWidth: .infinity)
                } else if containerWidth > 0 {
                    ForEach(WallMetrics.rows(tiles, columns: metrics.columns)) { row in
                        HStack(alignment: .top, spacing: WallMetrics.gutter) {
                            ForEach(row.tiles) { tile in
                                let width = metrics.width(
                                    spanning: WallMetrics.span(tile, columns: metrics.columns)
                                )
                                tileLink(tile, photos: photos, width: width)
                            }
                            // Holds a half-filled row left-aligned, which
                            // is exactly the gap the web grid leaves when
                            // a two-column tile will not fit beside a
                            // portrait.
                            Spacer(minLength: 0)
                        }
                        .frame(width: metrics.contentWidth)
                    }
                }
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, WallMetrics.gutter)
        }
        .background {
            GeometryReader { geo in
                Color.clear
                    .onAppear { containerWidth = geo.size.width }
                    .onChange(of: geo.size.width) { _, w in containerWidth = w }
            }
        }
    }

    @ViewBuilder
    private func tileLink(
        _ tile: TheWallTile, photos: [TheWallTile], width: CGFloat
    ) -> some View {
        let height = width / max(tile.aspectRatio, 0.05)

        if tile.isProject, let indexURL = tile.projectIndexURL {
            NavigationLink {
                ProjectDetailView(title: tile.caption, indexURL: indexURL, tile: tile)
            } label: {
                TheWallTileView(tile: tile, width: width, height: height)
            }
            .buttonStyle(.plain)
        } else if tile.isVideo, let url = tile.fullURL {
            Button {
                clip = TheWallClip(url: url)
            } label: {
                TheWallTileView(tile: tile, width: width, height: height)
            }
            .buttonStyle(.plain)
        } else {
            Button {
                guard let i = photos.firstIndex(where: { $0.id == tile.id }) else { return }
                viewer = TheWallViewerImages(
                    sources: photos.compactMap(\.fullURL), index: i
                )
            } label: {
                TheWallTileView(tile: tile, width: width, height: height)
            }
            .buttonStyle(.plain)
        }
    }
}

// MARK: - Presented media

/// A tapped image plus the rest of the visible wall, handed to the full-screen
/// viewer. Identifiable so `.fullScreenCover(item:)` re-presents on a new tap.
private struct TheWallViewerImages: Identifiable {
    let sources: [URL]
    let index: Int
    var id: String { "\(index)|\(sources.first?.absoluteString ?? "")" }
}

private struct TheWallClip: Identifiable {
    let url: URL
    var id: String { url.absoluteString }
}

// MARK: - Layout

/// The web wall is a CSS grid of 8 px rows with `auto-fill` columns and
/// explicit spans. Ported here as: how many columns fit, and which tiles take
/// two of them.
///
/// With `grid-auto-flow: row` (deliberately *not* `dense` — back-filling
/// hoists a later tile into an earlier gap, and the wall's tiles are ordered
/// by the names they were given), a two-column grid reduces exactly to rows:
/// a wide tile owns its row, portraits pair up, and a lone portrait next to a
/// wide tile leaves the gap the web page also leaves.
struct WallMetrics {
    static let gutter: CGFloat = 10
    /// Matches `body { padding: 30px 1rem }` on the site, so the column count
    /// works out the same at the same device width.
    static let horizontalPadding: CGFloat = 16
    /// `max-width: 900px` on the site's body — without this an iPad lays out
    /// five and six columns where the desktop page shows four.
    static let maxContentWidth: CGFloat = 900

    let contentWidth: CGFloat
    let columns: Int

    init(availableWidth: CGFloat) {
        let content = min(availableWidth, Self.maxContentWidth) - Self.horizontalPadding * 2
        contentWidth = max(content, 1)
        // `repeat(auto-fill, minmax(178px, 1fr))`, and 132px under the
        // 600px breakpoint — which is what puts two columns on every iPhone.
        let minTile: CGFloat = availableWidth < 600 ? 132 : 178
        columns = max(1, Int((contentWidth + Self.gutter) / (minTile + Self.gutter)))
    }

    /// Pixel width of a tile spanning `span` columns.
    func width(spanning span: Int) -> CGFloat {
        let columnWidth = (contentWidth - Self.gutter * CGFloat(columns - 1)) / CGFloat(columns)
        return columnWidth * CGFloat(span) + Self.gutter * CGFloat(span - 1)
    }

    /// Landscape and square tiles span two columns; portrait tiles one.
    static func span(_ tile: TheWallTile, columns: Int) -> Int {
        min(tile.w >= tile.h ? 2 : 1, columns)
    }

    /// Pack tiles into rows in manifest order, never reordering to close a
    /// gap — the same trade the web grid makes.
    static func rows(_ tiles: [TheWallTile], columns: Int) -> [WallRow] {
        var rows: [WallRow] = []
        var current: [TheWallTile] = []
        var used = 0

        for tile in tiles {
            let span = span(tile, columns: columns)
            if used + span > columns, !current.isEmpty {
                rows.append(WallRow(tiles: current))
                current = []
                used = 0
            }
            current.append(tile)
            used += span
            if used >= columns {
                rows.append(WallRow(tiles: current))
                current = []
                used = 0
            }
        }
        if !current.isEmpty { rows.append(WallRow(tiles: current)) }
        return rows
    }
}

struct WallRow: Identifiable {
    let tiles: [TheWallTile]
    /// The first tile's id — unique per row because `full` is unique per tile
    /// (the build rejects the same bytes reaching the wall twice).
    var id: String { tiles.first?.id ?? "empty" }
}

// MARK: - Tile

/// One tile. A photo is only the picture — no caption, no science, nothing on
/// top of it, matching the web wall where "the picture is the whole content".
/// A project card is framed in its science colour, badged, and permanently
/// captioned, so it never reads as one more photo.
private struct TheWallTileView: View {
    let tile: TheWallTile
    let width: CGFloat
    let height: CGFloat

    var body: some View {
        ZStack(alignment: .topLeading) {
            ZStack(alignment: .bottom) {
                media
                if tile.isProject { caption }
            }
            .frame(width: width, height: height)

            if tile.isProject { badge }
            if tile.isVideo { playGlyph }
        }
        .frame(width: width, height: height, alignment: .topLeading)
        .background(Color.black.opacity(0.9))
        .clipShape(RoundedRectangle(cornerRadius: 9, style: .continuous))
        .overlay {
            if tile.isProject {
                RoundedRectangle(cornerRadius: 9, style: .continuous)
                    .strokeBorder(SubjectPalette.color(for: tile.science), lineWidth: 3)
            }
        }
        .shadow(color: .black.opacity(0.1), radius: 1.5, y: 1)
    }

    @ViewBuilder
    private var media: some View {
        #if canImport(UIKit)
        if tile.isVideo, let url = tile.fullURL {
            ZStack {
                // The poster holds the frame until the first video frame
                // paints — otherwise a clip tile opens as a black hole.
                RemoteImage(url: Self.posterURL(tile), maxPointSize: max(width, height))
                LoopingClipView(url: url)
            }
        } else {
            RemoteImage(url: tile.thumbURL, maxPointSize: max(width, height))
        }
        #else
        RemoteImage(url: tile.thumbURL, maxPointSize: max(width, height))
        #endif
    }

    /// `thumbURL` already prefers the poster for a clip; this is the same
    /// resolution, named for what it is at the call site.
    private static func posterURL(_ tile: TheWallTile) -> URL? { tile.thumbURL }

    /// A clip is the one moving thing on the wall — say so quietly, so the
    /// motion reads as deliberate rather than as a broken image.
    private var playGlyph: some View {
        Text("▶")
            .font(.system(size: 11))
            .foregroundStyle(.white.opacity(0.85))
            .shadow(color: .black.opacity(0.8), radius: 3, y: 1)
            .padding(.leading, 8)
            .padding(.bottom, 6)
            .frame(width: width, height: height, alignment: .bottomLeading)
            .allowsHitTesting(false)
    }

    /// The web's `.tile-badge`: uppercase, science-tinted, tucked into the
    /// top-left corner with only its inner corner rounded.
    private var badge: some View {
        Text("REPORT →")
            .font(.system(size: 9, weight: .bold))
            .tracking(0.6)
            .foregroundStyle(Color.black.opacity(0.82))
            .padding(.horizontal, 6)
            .padding(.vertical, 3)
            .background(
                UnevenRoundedRectangle(bottomTrailingRadius: 7, style: .continuous)
                    .fill(SubjectPalette.color(for: tile.science))
            )
    }

    private var caption: some View {
        HStack(alignment: .bottom, spacing: 6) {
            Text(tile.caption)
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(.white)
                .lineLimit(2)
                .multilineTextAlignment(.leading)
            Spacer(minLength: 0)
            Text(tile.science)
                .font(.system(size: 9, weight: .semibold))
                .lineLimit(1)
                .fixedSize()
                .padding(.horizontal, 6)
                .padding(.vertical, 1)
                .background(Capsule().fill(SubjectPalette.color(for: tile.science)))
                .foregroundStyle(Color.black.opacity(0.82))
        }
        .padding(.horizontal, 8)
        .padding(.top, 26)
        .padding(.bottom, 7)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            LinearGradient(
                colors: [Color.black.opacity(0.94), Color.black.opacity(0.55), Color.black.opacity(0)],
                startPoint: .bottom, endPoint: .top
            )
        )
    }
}

// MARK: - Science filter

/// The same toolbar bubble the Olympiads tab uses: a label showing the current
/// selection, tapping it drops a system menu of the six sciences with a
/// checkmark on the active one and its palette dot alongside. Native, and it
/// leaves the wall the whole screen.
///
/// This replaced a port of the website's pill row (2026-07-31). The pill row
/// was faithful to the web page and wrong for the app — the phone already has
/// a filter idiom, one tab over.
///
/// Slugs and counts come from the manifest, so a science with no pictures
/// never offers a dead-end filter.
private struct ScienceFilterMenu: View {
    @Binding var selected: String?
    let sciences: [TheWallScience]

    var body: some View {
        Menu {
            // Plain Buttons rather than a Picker, so each science can carry
            // its own palette dot — a Picker inside a Menu renders
            // system-tinted symbols only. Same shape as SubjectFilterMenu.
            Button { selected = nil } label: {
                row(label: "All", color: nil, isSelected: selected == nil)
            }
            ForEach(sciences.filter { $0.count > 0 }) { science in
                Button { selected = science.slug } label: {
                    row(
                        label: science.science,
                        color: SubjectPalette.color(for: science.science),
                        isSelected: selected == science.slug
                    )
                }
            }
        } label: {
            HStack(spacing: 4) {
                if let name = selectedName {
                    Circle()
                        .fill(SubjectPalette.color(for: name))
                        .frame(width: 10, height: 10)
                }
                Text(selectedName ?? "All")
                    .font(.system(size: 15, weight: .medium))
            }
        }
    }

    /// Display name for the active slug. The manifest's slug is the full
    /// lowercase word, so the science's own `science` field is the label.
    private var selectedName: String? {
        guard let selected else { return nil }
        return sciences.first { $0.slug == selected }?.science
    }

    @ViewBuilder
    private func row(label: String, color: Color?, isSelected: Bool) -> some View {
        HStack {
            Text(label)
            Spacer()
            if isSelected { Image(systemName: "checkmark") }
            if let color {
                Circle().fill(color).frame(width: 12, height: 12)
            } else {
                Image(systemName: "square.grid.2x2")
            }
        }
    }
}
