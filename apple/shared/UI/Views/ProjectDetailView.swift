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
                // Sciences power the title-row tech pills; idempotent +
                // cached, so this returns immediately when already loaded.
                await store.preloadAll()

                let (data, _) = try await URLSession.shared.data(from: indexURL)
                var md = String(data: data, encoding: .utf8) ?? ""

                // Front-matter photos: legacy projects list them explicitly.
                var photos = MarkdownHelper.extractPhotos(from: md, key: "photos")
                let dataPhotos = MarkdownHelper.extractPhotos(from: md, key: "data_photos")

                // Modern projects don't list photos in front matter — the
                // Astro layout scans photos/ at build time and
                // build_technology.py bakes the same list into
                // technology.json, which the store already holds.
                if photos.isEmpty {
                    photos = (store.sciences ?? [])
                        .projectPhotos(forIndexURL: indexURL)
                        .shuffled()
                }

                // Title-row pills mirror the webapp project page: one
                // science-colored pill per tech the project used, resolved
                // against technology.json. Replaces both the old plain
                // science-name title pills and the bottom Technology table.
                let techNames = MarkdownHelper.extractPhotos(from: md, key: "tech")
                let projSciences = MarkdownHelper.extractPhotos(from: md, key: "sciences")
                let pills = titlePills(techNames: techNames, projectSciences: projSciences)

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

    /// Resolve a project's `tech:` front-matter names into title-row pills,
    /// matching the webapp (Project.astro): one science-colored pill per
    /// tech, ordered by the tech's global id (science order, then within a
    /// science) so the sequence matches the /research/ listing. A tech name
    /// can live in more than one science (Chemistry and Astronomy both have
    /// "Spectroscopy"), so disambiguate by the project's own `sciences:`.
    /// Returns [] when sciences haven't loaded — the caller then falls back
    /// to plain science-name pills, same as the webapp's no-tech fallback.
    private func titlePills(
        techNames: [String], projectSciences: [String]
    ) -> [(label: String, slug: String)] {
        guard let sciences = store.sciences else { return [] }
        var ranked: [(label: String, slug: String, id: Int)] = []
        for name in techNames {
            var candidates: [(science: ResearchScience, tech: ResearchTech)] = []
            for science in sciences {
                if let tech = science.techs.first(where: { $0.tech == name }) {
                    candidates.append((science, tech))
                }
            }
            guard !candidates.isEmpty else { continue }
            let pick = candidates.first { projectSciences.contains($0.science.science) }
                ?? candidates[0]
            ranked.append((label: name, slug: pick.science.scienceSlug, id: pick.tech.id))
        }
        return ranked
            .sorted { $0.id < $1.id }
            .map { (label: $0.label, slug: $0.slug) }
    }

}
