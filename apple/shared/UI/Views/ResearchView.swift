import SwiftUI
import ScienceCore

/// Toy browser matching the webapp /research/ page. One card per science,
/// each a flat list of technologies and their toys. Source of truth:
/// public/research/technology.json.
struct ResearchView: View {
    @State private var store = ContentStore.shared
    @State private var subject: SubjectFilter = SubjectFilter.randomResearchSubject()

    var body: some View {
        NavigationStack {
            Group {
                if let sciences = store.sciences {
                    content(sciences: sciences)
                } else if let errorMessage = store.sciencesError {
                    ErrorState(message: errorMessage)
                } else {
                    LoadingState(
                        title: "Loading toys",
                        subtitle: "Fetching research topics from GitHub."
                    )
                }
            }
            .navigationTitle("Research")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    SubjectFilterMenu(selected: $subject)
                }
            }
            .refreshable { await store.refreshAll() }
        }
    }

    private func filteredSciences(_ sciences: [ResearchScience]) -> [ResearchScience] {
        guard case .named(let name) = subject else { return sciences }
        return sciences.filter { $0.science == name }
    }

    private func content(sciences: [ResearchScience]) -> some View {
        let visible = filteredSciences(sciences)
        return ScrollView {
            LazyVStack(alignment: .leading, spacing: 14) {
                ForEach(visible) { science in
                    ScienceCard(science: science)
                }
                if visible.isEmpty {
                    Text("No toys yet.")
                        .font(.system(size: 14))
                        .foregroundStyle(.secondary)
                        .italic()
                        .padding(.horizontal, 16)
                }
            }
            .padding(.vertical, 12)
        }
    }
}

// MARK: - Science card

private struct ScienceCard: View {
    let science: ResearchScience

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text(science.science)
                .font(.system(size: 16, weight: .bold))
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.vertical, 13)
                .padding(.leading, 14)
                .padding(.trailing, 12)
            Divider()
            VStack(alignment: .leading, spacing: 0) {
                ForEach(science.techs) { tech in
                    TechRow(science: science.science, tech: tech)
                    if tech.id != science.techs.last?.id {
                        Divider().padding(.leading, 28)
                    }
                }
            }
        }
        .background(
            RoundedRectangle(cornerRadius: 10)
                .fill(ResearchColors.cardBackground)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 10)
                .stroke(SubjectPalette.color(for: science.science).opacity(0.7), lineWidth: 1)
        )
        .overlay(alignment: .leading) {
            // Left accent bar, mirrors webapp .tech-accent-* border.
            RoundedRectangle(cornerRadius: 2)
                .fill(SubjectPalette.color(for: science.science))
                .frame(width: 4)
        }
        .padding(.horizontal, 12)
    }
}

private struct TechRow: View {
    let science: String
    let tech: ResearchTech
    @Environment(\.openURL) private var openURL

    private var hasLink: Bool { tech.techUrl != nil || tech.externalURL != nil }
    private var projectCount: Int { tech.projects?.count ?? 0 }

    var body: some View {
        Group {
            if tech.techUrl != nil {
                NavigationLink {
                    TechDetailView(science: science, tech: tech)
                } label: {
                    rowBody
                }
                .buttonStyle(.plain)
            } else if let external = tech.externalURL {
                Button { openURL(external) } label: {
                    rowBody
                }
                .buttonStyle(.plain)
            } else {
                rowBody
            }
        }
    }

    @ViewBuilder
    private var rowBody: some View {
        HStack(alignment: .center, spacing: 8) {
            Text(tech.tech)
                .font(.system(size: 16, weight: .regular))
                .foregroundStyle(hasLink ? Color.accentColor : Color.primary)
            Spacer(minLength: 0)
            if projectCount > 0 {
                Text("\(projectCount) project\(projectCount == 1 ? "" : "s")")
                    .font(.system(size: 12))
                    .foregroundStyle(.secondary)
            }
            if hasLink {
                Image(systemName: "chevron.right")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundStyle(.tertiary)
            }
        }
        .frame(minHeight: 44)
        .padding(.leading, 28)
        .padding(.trailing, 12)
        .contentShape(Rectangle())
    }
}

// MARK: - Tech detail

/// Native tech page — renders title, science chip, topic·category
/// context, hero image, spec description, and the projects list, all
/// from `technology.json` data. Replaces the previous markdown-passthrough
/// approach because most tech `index.md` bodies are empty by design (the
/// data-bearing fields live in `technology.json`).
struct TechDetailView: View {
    let science: String
    let tech: ResearchTech

    private static let scienceRank: [String: Int] = [
        "Mathematics": 0, "Computing": 1, "Physics": 2,
        "Chemistry": 3, "Biology": 4, "Astronomy": 5,
    ]

    /// Projects sorted by canonical science order (primary science chip),
    /// then newest-first within a science — matches the webapp tech page.
    private var sortedProjects: [ResearchTechProject] {
        (tech.projects ?? []).sorted { a, b in
            let ra = Self.scienceRank[a.sciences.first ?? ""] ?? Int.max
            let rb = Self.scienceRank[b.sciences.first ?? ""] ?? Int.max
            if ra != rb { return ra < rb }
            return a.date > b.date
        }
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 14) {
                if let url = tech.heroURL {
                    AsyncImage(url: url) { phase in
                        switch phase {
                        case .success(let image):
                            image.resizable().scaledToFill()
                        case .failure:
                            Color.clear
                        case .empty:
                            ResearchColors.cardBackground
                        @unknown default:
                            Color.clear
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: 200)
                    .clipped()
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.black.opacity(0.08), lineWidth: 1)
                    )
                }

                if let toys = tech.toys, !toys.isEmpty {
                    Text("Toys")
                        .font(.system(size: 17, weight: .bold))

                    VStack(spacing: 0) {
                        ForEach(toys) { toy in
                            TechToyRow(toy: toy)
                            if toy.id != toys.last?.id {
                                Divider()
                            }
                        }
                    }
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(ResearchColors.cardBackground)
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.black.opacity(0.08), lineWidth: 1)
                    )
                }

                Divider().padding(.vertical, 4)

                Text("Projects")
                    .font(.system(size: 17, weight: .bold))

                if !sortedProjects.isEmpty {
                    VStack(spacing: 0) {
                        ForEach(sortedProjects) { p in
                            TechProjectRow(project: p)
                            if p.id != sortedProjects.last?.id {
                                Divider()
                            }
                        }
                    }
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(ResearchColors.cardBackground)
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(Color.black.opacity(0.08), lineWidth: 1)
                    )
                } else {
                    Text("No projects yet.")
                        .italic()
                        .foregroundStyle(.secondary)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 14)
            .padding(.vertical, 14)
        }
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
        .toolbar {
            ToolbarItem(placement: .principal) {
                HStack(spacing: 8) {
                    Text(tech.tech)
                        .font(.system(size: 17, weight: .bold))
                    SubjectChip(subject: science)
                }
            }
        }
    }
}

private struct TechToyRow: View {
    let toy: ResearchToy
    @Environment(\.openURL) private var openURL

    private var hasLink: Bool { toy.projectIndexURL != nil || toy.externalURL != nil }

    var body: some View {
        Group {
            if let indexURL = toy.projectIndexURL {
                NavigationLink {
                    ProjectDetailView(title: toy.name, indexURL: indexURL)
                } label: {
                    rowBody
                }
                .buttonStyle(.plain)
            } else if let external = toy.externalURL {
                Button { openURL(external) } label: {
                    rowBody
                }
                .buttonStyle(.plain)
            } else {
                rowBody
            }
        }
    }

    private var rowBody: some View {
        HStack(alignment: .firstTextBaseline, spacing: 8) {
            VStack(alignment: .leading, spacing: 4) {
                Text(toy.name)
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(hasLink ? Color.accentColor : Color.primary)
                    .fixedSize(horizontal: false, vertical: true)
                if !toy.description.isEmpty {
                    Text(toy.description)
                        .font(.system(size: 12))
                        .foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            Spacer(minLength: 0)
            if hasLink {
                Image(systemName: "chevron.right")
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundStyle(.tertiary)
            }
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .contentShape(Rectangle())
    }
}

private struct TechProjectRow: View {
    let project: ResearchTechProject

    var body: some View {
        Group {
            if let indexURL = project.indexURL {
                NavigationLink {
                    ProjectDetailView(title: project.title, indexURL: indexURL)
                } label: {
                    rowBody
                }
                .buttonStyle(.plain)
            } else {
                rowBody
            }
        }
    }

    private var rowBody: some View {
        HStack(alignment: .firstTextBaseline, spacing: 10) {
            VStack(alignment: .leading, spacing: 4) {
                Text(project.title)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundStyle(project.indexURL != nil ? Color.accentColor : Color.primary)
                if !project.sciences.isEmpty {
                    HStack(spacing: 4) {
                        ForEach(project.sciences, id: \.self) { s in
                            SubjectChip(subject: s)
                        }
                    }
                }
            }
            Spacer(minLength: 0)
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .contentShape(Rectangle())
    }
}

// MARK: - Project detail

/// Loads a research project's index.md from GitHub raw and renders it
/// inside the app with the shared KaTeX markdown webview. Avoids the
/// Safari bounce the user was seeing when tapping a project tech.
struct ProjectDetailView: View {
    let title: String
    let indexURL: URL
    @State private var markdown: String = ""
    @State private var loading = true
    @State private var techNames: [String] = []

    var body: some View {
        Group {
            if loading {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                ScrollView {
                    VStack(alignment: .leading, spacing: 0) {
                        MarkdownWebView(markdown: markdown)
                        if !techNames.isEmpty {
                            ProjectTechnologySection(techNames: techNames)
                                .padding(.horizontal, 14)
                                .padding(.bottom, 14)
                        }
                    }
                }
            }
        }
        .navigationTitle(title)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
        .task {
            do {
                let (data, _) = try await URLSession.shared.data(from: indexURL)
                var md = String(data: data, encoding: .utf8) ?? ""

                // Front-matter photos: legacy projects list them explicitly.
                var photos = MarkdownHelper.extractPhotos(from: md, key: "photos")
                let dataPhotos = MarkdownHelper.extractPhotos(from: md, key: "data_photos")

                // Modern projects don't list photos in front matter — the
                // Astro layout scans photos/setup + photos/samples at build
                // time. Replicate that by querying the GitHub contents
                // API so the in-app grid has sources to show.
                if photos.isEmpty {
                    photos = await Self.scanProjectPhotos(indexURL: indexURL).shuffled()
                }

                // Capture the project's `tech:` front-matter array before
                // we strip; that's the source for the native Technology
                // table that replaces the inline `<ul class="updates-list">`.
                techNames = MarkdownHelper.extractPhotos(from: md, key: "tech")

                let titleBlock = MarkdownHelper.synthesizeProjectTitle(from: md)
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

    /// Fetch the union of image filenames under a project's
    /// `photos/setup/` and `photos/samples/` via the GitHub contents
    /// API. Returns relative paths (e.g. `photos/setup/setup1.jpeg`) so
    /// they resolve through `MarkdownHelper.resolveRelativeURLs` with
    /// the project folder as base. Silent on failure — photos are
    /// decorative; a broken network should not crash the page.
    ///
    /// `indexURL` here is the deployed-site URL (`https://vivianweidai.com/research/projects/{folder}/index.md`),
    /// not a GitHub raw URL — we fetch markdown over the website. The
    /// repo + branch are hardcoded since this app only ever reads its
    /// own repo.
    private static func scanProjectPhotos(indexURL: URL) async -> [String] {
        let parts = indexURL.path.split(separator: "/").map(String.init)
        guard let idxPos = parts.firstIndex(of: "index.md"),
              idxPos > 0 else { return [] }
        let folder = parts[idxPos - 1]
        // public/ is the on-disk root mapped to the site root; that's
        // what the GitHub Contents API needs to see.
        let folderPath = "public/research/projects/\(folder)"

        var all: [String] = []
        for sub in ["photos/setup", "photos/samples"] {
            let apiPath = "\(folderPath)/\(sub)"
            let encoded = apiPath.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? apiPath
            guard let url = URL(string: "https://api.github.com/repos/vivianweidai/science/contents/\(encoded)?ref=main") else {
                continue
            }
            var req = URLRequest(url: url)
            req.setValue("application/vnd.github+json", forHTTPHeaderField: "accept")
            do {
                let (data, response) = try await URLSession.shared.data(for: req)
                guard let http = response as? HTTPURLResponse,
                      (200..<300).contains(http.statusCode) else { continue }
                let entries = try JSONDecoder().decode([GitHubContentEntry].self, from: data)
                for e in entries where e.type == "file" {
                    let lower = e.name.lowercased()
                    if lower.hasSuffix(".jpg") || lower.hasSuffix(".jpeg")
                        || lower.hasSuffix(".png") {
                        all.append("\(sub)/\(e.name)")
                    }
                }
            } catch {
                continue
            }
        }
        return all
    }
}

private struct GitHubContentEntry: Decodable {
    let name: String
    let type: String
}

// MARK: - Project Technology section

/// Native rendering of the Technology section for a project page —
/// replaces the inline `<ul class="updates-list">` HTML that was
/// shipped in markdown bodies. The list of toys comes from the
/// project's `tech:` front-matter array; each tech is resolved via
/// ContentStore (technology.json) for its parent science, and tapping a
/// row navigates internally to TechDetailView (no Safari bounce). Techs
/// missing from ContentStore (e.g. typo or not yet in technology.yml)
/// are silently skipped.
private struct ResolvedTech: Identifiable {
    let science: ResearchScience
    let tech: ResearchTech
    var id: String { tech.tech }
}

private struct ProjectTechnologySection: View {
    let techNames: [String]
    @State private var store = ContentStore.shared

    private static let scienceRank: [String: Int] = [
        "Mathematics": 0, "Computing": 1, "Physics": 2,
        "Chemistry": 3, "Biology": 4, "Astronomy": 5,
    ]

    /// Resolve each tech name against ContentStore and sort:
    /// 1. by science in math → comp → phys → chem → bio → astro order;
    /// 2. within a science, by `tech.id` (which monotonically increases
    ///    in technology.yml authoring order, so this preserves the
    ///    intra-subject sequence the user laid out in the source file).
    private var resolved: [ResolvedTech] {
        techNames
            .compactMap { name -> ResolvedTech? in
                guard let r = store.findTech(named: name) else { return nil }
                return ResolvedTech(science: r.science, tech: r.tech)
            }
            .sorted { a, b in
                let ra = Self.scienceRank[a.science.science] ?? Int.max
                let rb = Self.scienceRank[b.science.science] ?? Int.max
                if ra != rb { return ra < rb }
                return a.tech.id < b.tech.id
            }
    }

    var body: some View {
        if !resolved.isEmpty {
            VStack(alignment: .leading, spacing: 8) {
                Text("Technology")
                    .font(.system(size: 17, weight: .bold))
                    .padding(.top, 8)

                VStack(spacing: 0) {
                    ForEach(Array(resolved.enumerated()), id: \.element.id) { idx, r in
                        NavigationLink {
                            TechDetailView(science: r.science.science, tech: r.tech)
                        } label: {
                            ProjectTechnologyRow(resolved: r)
                        }
                        .buttonStyle(.plain)
                        if idx != resolved.count - 1 {
                            Divider()
                        }
                    }
                }
                .background(
                    RoundedRectangle(cornerRadius: 8)
                        .fill(ResearchColors.cardBackground)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Color.black.opacity(0.08), lineWidth: 1)
                )
            }
        }
    }
}

private struct ProjectTechnologyRow: View {
    let resolved: ResolvedTech

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 10) {
            Text(resolved.tech.tech)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(Color.accentColor)
            Spacer(minLength: 6)
            SubjectChip(subject: resolved.science.science)
        }
        .padding(.vertical, 8)
        .padding(.horizontal, 12)
        .contentShape(Rectangle())
    }
}

// MARK: - Subject filter (shared pattern with OlympiadsView)

private enum SubjectFilter: Hashable {
    case all
    case named(String)

    static let allCases: [SubjectFilter] = [
        .all,
        .named("Mathematics"),
        .named("Computing"),
        .named("Physics"),
        .named("Chemistry"),
        .named("Biology"),
        .named("Astronomy"),
    ]

    /// Matches the webapp pick pool: chem / bio / phys / comp.
    static func randomResearchSubject() -> SubjectFilter {
        let pool: [SubjectFilter] = [
            .named("Chemistry"), .named("Biology"),
            .named("Physics"), .named("Computing"),
        ]
        return pool.randomElement() ?? .all
    }

    var label: String {
        switch self {
        case .all: return "All"
        case .named(let n): return n
        }
    }

    var color: Color? {
        switch self {
        case .all: return nil
        case .named(let n): return SubjectPalette.color(for: n)
        }
    }
}

private struct SubjectFilterMenu: View {
    @Binding var selected: SubjectFilter

    var body: some View {
        Menu {
            // Plain Buttons instead of a Picker so each row's dot can
            // carry its own palette color — see OlympiadsView for the
            // same pattern.
            ForEach(SubjectFilter.allCases, id: \.self) { filter in
                Button { selected = filter } label: {
                    filterMenuRow(filter: filter, isSelected: filter == selected)
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
}

@ViewBuilder
private func filterMenuRow(filter: SubjectFilter, isSelected: Bool) -> some View {
    HStack {
        Text(filter.label)
        Spacer()
        if isSelected {
            Image(systemName: "checkmark")
        }
        if let color = filter.color {
            Circle().fill(color).frame(width: 12, height: 12)
        } else {
            Image(systemName: "square.grid.2x2")
        }
    }
}

// MARK: - Cross-platform colors

/// Semantic colors that adapt to light/dark mode on iOS, with macOS
/// fallbacks for the watchOS/macOS ScienceCoreUI build. Uses UIKit/AppKit
/// bridges guarded by platform availability.
private enum ResearchColors {
    static var cardBackground: Color {
        #if canImport(UIKit)
        return Color(uiColor: .secondarySystemBackground)
        #else
        return Color.gray.opacity(0.08)
        #endif
    }

    static var technologyHeader: Color {
        #if canImport(UIKit)
        return Color(uiColor: .tertiarySystemBackground)
        #else
        return Color.gray.opacity(0.05)
        #endif
    }
}

// MARK: - Subject chip

private struct SubjectChip: View {
    let subject: String

    var body: some View {
        Text(subject)
            .font(.system(size: 10, weight: .semibold))
            .padding(.horizontal, 7)
            .padding(.vertical, 2)
            .background(Capsule().fill(SubjectPalette.color(for: subject)))
            .foregroundStyle(Color.black.opacity(0.82))
    }
}
