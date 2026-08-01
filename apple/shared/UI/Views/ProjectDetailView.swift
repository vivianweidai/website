import SwiftUI
import ScienceCore

// MARK: - Project detail

/// A tapped image plus the rest of the page's images, handed to the
/// full-screen viewer. Identifiable so `.fullScreenCover(item:)` presents
/// (and re-presents on a different tile) without a separate flag.
private struct ViewerImages: Identifiable {
    let sources: [URL]
    let index: Int
    var id: String { "\(index)|\(sources.first?.absoluteString ?? "")" }
}

/// Loads a research project's index.md from GitHub raw and renders it
/// inside the app with the shared KaTeX markdown webview. Avoids the
/// Safari bounce the user was seeing when tapping a project tech.
struct ProjectDetailView: View {
    let title: String
    let indexURL: URL
    /// The wall's card for this project, which carries its photo pool.
    var tile: TheWallTile? = nil
    @State private var store = ContentStore.shared
    @State private var markdown: String = ""
    @State private var loading = true
    @State private var viewerImages: ViewerImages?

    var body: some View {
        Group {
            if loading {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                ScrollView {
                    MarkdownWebView(markdown: markdown) { urls, index in
                        viewerImages = ViewerImages(sources: urls, index: index)
                    }
                }
            }
        }
        .navigationTitle(title)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .fullScreenCover(item: $viewerImages) { images in
            ImageViewerView(sources: images.sources, index: images.index)
        }
        #endif
        .task {
            do {
                let (data, _) = try await URLSession.shared.data(from: indexURL)
                var md = String(data: data, encoding: .utf8) ?? ""

                // Front-matter photos: legacy projects list them explicitly.
                var photos = MarkdownHelper.extractPhotos(from: md, key: "photos")
                let dataPhotos = MarkdownHelper.extractPhotos(from: md, key: "data_photos")

                // Modern projects don't list photos in front matter — the
                // Astro layout scans photos/ at build time and
                // build_thewall.py bakes the same list into the project's
                // card, which the wall handed us.
                if photos.isEmpty, let tile {
                    photos = tile.photos ?? []
                    photos.shuffle()
                }

                // Title-row pills: one science-coloured pill per science the
                // project declares. These used to resolve each `tech:` name
                // against technology.json; with the toy catalog gone the
                // science is the whole of it.
                let pills = MarkdownHelper.extractPhotos(from: md, key: "sciences")
                    .map { (label: $0, slug: SubjectPaletteRGB.slug(for: $0)) }

                let titleBlock = MarkdownHelper.synthesizeProjectTitle(from: md, techPills: pills)
                md = MarkdownHelper.stripFrontMatter(md)
                md = titleBlock + md
                md = MarkdownHelper.stripTechnologySection(md)
                md = MarkdownHelper.injectPhotos(md, photos: photos)
                md = MarkdownHelper.injectDataPhotos(md, photos: dataPhotos)
                let folderURL = indexURL.deletingLastPathComponent()
                md = MarkdownHelper.resolveRelativeURLs(in: md, baseURL: folderURL)
                markdown = md
            } catch {
                markdown = "# Error\n\n\(error.localizedDescription)"
            }
            loading = false
        }
    }

}
