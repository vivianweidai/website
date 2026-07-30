import SwiftUI
import ScienceCore

/// The projects wall, matching the website's /projects/ page: one
/// chronological grid of every picture worth looking at, newest first, with
/// photos and project cards interleaved. Source of truth is
/// `web/public/projects/gallery.json`, the same manifest the website builds
/// from — so a row added to `gallery.yml` appears here without an app release.
///
/// Deliberately the same shape as the web page and no more: a science filter,
/// the grid, and nothing below the fold. Replaced the old tech browser
/// 2026-07-30 when the website dropped its per-tech pages; that view had been
/// reading `hero` and `tech_url` out of technology.json, and the build stopped
/// emitting both, so it had quietly become a list of names.
struct GalleryView: View {
    @State private var store = ContentStore.shared
    @State private var subject: GallerySubject = .all
    @State private var viewer: GalleryViewerImages?

    var body: some View {
        NavigationStack {
            Group {
                if let gallery = store.gallery {
                    content(gallery: gallery)
                } else if let errorMessage = store.galleryError {
                    ErrorState(message: errorMessage)
                } else {
                    LoadingState(
                        title: "Loading projects",
                        subtitle: "Fetching the gallery from vivianweidai.com."
                    )
                }
            }
            .navigationTitle("Projects")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    GallerySubjectMenu(selected: $subject, sciences: store.gallery?.sciences ?? [])
                }
            }
            .refreshable { await store.refreshAll() }
        }
        #if os(iOS)
        .fullScreenCover(item: $viewer) { images in
            ImageViewerView(sources: images.sources, index: images.index)
        }
        #endif
    }

    private func visibleTiles(_ gallery: GalleryResponse) -> [GalleryTile] {
        guard case .named(let slug) = subject else { return gallery.tiles }
        return gallery.tiles.filter { $0.scienceSlug == slug }
    }

    @ViewBuilder
    private func content(gallery: GalleryResponse) -> some View {
        let tiles = visibleTiles(gallery)
        // Photo tiles only, in display order — the viewer pages through what
        // is currently on screen, so a filtered wall stays inside its filter
        // and project cards are skipped the way they are on the web.
        let photos = tiles.filter { !$0.isProject && !$0.isVideo }

        ScrollView {
            if tiles.isEmpty {
                Text("Nothing here yet.")
                    .font(.system(size: 14))
                    .foregroundStyle(.secondary)
                    .italic()
                    .padding(.top, 40)
            } else {
                LazyVGrid(
                    columns: [GridItem(.flexible(), spacing: 10),
                              GridItem(.flexible(), spacing: 10)],
                    spacing: 10
                ) {
                    ForEach(tiles) { tile in
                        if tile.isVideo, let url = tile.fullURL {
                            // The viewer decodes images; a clip goes to the
                            // system player, which is also the only thing here
                            // that reliably decodes the Seestar's H.264.
                            Link(destination: url) { GalleryTileView(tile: tile) }
                                .buttonStyle(.plain)
                        } else if tile.isProject, let indexURL = tile.projectIndexURL {
                            NavigationLink {
                                ProjectDetailView(title: tile.caption, indexURL: indexURL)
                            } label: {
                                GalleryTileView(tile: tile)
                            }
                            .buttonStyle(.plain)
                        } else {
                            Button {
                                guard let i = photos.firstIndex(where: { $0.id == tile.id })
                                else { return }
                                viewer = GalleryViewerImages(
                                    sources: photos.compactMap(\.fullURL), index: i
                                )
                            } label: {
                                GalleryTileView(tile: tile)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 12)
            }
        }
    }
}

/// A tapped image plus the rest of the visible wall, handed to the full-screen
/// viewer. Identifiable so `.fullScreenCover(item:)` re-presents on a new tap.
private struct GalleryViewerImages: Identifiable {
    let sources: [URL]
    let index: Int
    var id: String { "\(index)|\(sources.first?.absoluteString ?? "")" }
}

// MARK: - Tile

/// One tile: the picture, with its caption bottom-left and its science
/// bottom-right, exactly the two things the web tile shows on hover. Held to
/// the picture's own aspect ratio so portrait captures stay portrait.
private struct GalleryTileView: View {
    let tile: GalleryTile

    var body: some View {
        ZStack(alignment: .bottom) {
            AsyncImage(url: tile.thumbURL) { phase in
                switch phase {
                case .success(let image):
                    image.resizable().scaledToFill()
                case .failure:
                    Color.black.opacity(0.06)
                        .overlay(Image(systemName: "photo").foregroundStyle(.secondary))
                default:
                    Color.black.opacity(0.06)
                }
            }
            .frame(maxWidth: .infinity)
            .aspectRatio(tile.aspectRatio, contentMode: .fit)
            .clipped()

            caption
        }
        .overlay {
            if tile.isVideo {
                Image(systemName: "play.circle.fill")
                    .font(.system(size: 34))
                    .foregroundStyle(.white.opacity(0.85))
                    .shadow(radius: 6)
            }
        }
        .background(Color.black.opacity(0.9))
        .clipShape(RoundedRectangle(cornerRadius: 9, style: .continuous))
        .overlay {
            // A project card is framed in its science colour and reads as a
            // link; a photo is just a photo.
            if tile.isProject {
                RoundedRectangle(cornerRadius: 9, style: .continuous)
                    .strokeBorder(SubjectPalette.color(for: tile.science), lineWidth: 3)
            }
        }
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
        .padding(.top, 24)
        .padding(.bottom, 7)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            LinearGradient(
                colors: [Color.black.opacity(0.85), Color.black.opacity(0)],
                startPoint: .bottom, endPoint: .top
            )
        )
    }
}

// MARK: - Subject filter

/// File-private, matching the pattern in OlympiadsView — the codebase keeps a
/// near-identical copy per view rather than sharing one, so the filter can
/// speak each screen's own vocabulary. Here that is the gallery's science
/// slugs, taken from the manifest rather than hard-coded.
private enum GallerySubject: Hashable {
    case all
    case named(String)   // science slug

    var label: String {
        switch self {
        case .all: return "All"
        case .named(let slug): return GallerySubject.name(for: slug)
        }
    }

    static func name(for slug: String) -> String {
        switch slug {
        case "math": return "Mathematics"
        case "comp": return "Computing"
        case "phys": return "Physics"
        case "chem": return "Chemistry"
        case "bio": return "Biology"
        case "astro": return "Astronomy"
        default: return slug
        }
    }

    var color: Color? {
        switch self {
        case .all: return nil
        case .named(let slug): return SubjectPalette.color(for: GallerySubject.name(for: slug))
        }
    }
}

private struct GallerySubjectMenu: View {
    @Binding var selected: GallerySubject
    let sciences: [GalleryScience]

    var body: some View {
        Menu {
            Button { selected = .all } label: {
                menuRow(label: "All", color: nil, isSelected: selected == .all)
            }
            // Only sciences that actually have pictures — an empty filter is a
            // dead end, and the manifest already carries the counts.
            ForEach(sciences.filter { $0.count > 0 }) { science in
                Button { selected = .named(science.slug) } label: {
                    menuRow(
                        label: science.science,
                        color: SubjectPalette.color(for: science.science),
                        isSelected: selected == .named(science.slug)
                    )
                }
            }
        } label: {
            HStack(spacing: 4) {
                if let color = selected.color {
                    Circle().fill(color).frame(width: 10, height: 10)
                }
                Text(selected.label)
                    .font(.system(size: 15, weight: .medium))
            }
        }
    }

    @ViewBuilder
    private func menuRow(label: String, color: Color?, isSelected: Bool) -> some View {
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
