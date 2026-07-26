import Foundation

/// Strongly-typed mirror of `web/public/research/technology.json`, the source of
/// truth for the Research page's tech browser. One entry per science, each a
/// flat list of techs (the old topic/category grouping tiers were dropped).
public struct ResearchScience: Codable, Identifiable, Hashable, Sendable {
    public let id: Int
    public let science: String
    public let scienceSlug: String
    public let techs: [ResearchTech]

    enum CodingKeys: String, CodingKey {
        case id, science, techs
        case scienceSlug = "science_slug"
    }
}

public struct ResearchTech: Codable, Identifiable, Hashable, Sendable {
    public let id: Int
    public let tech: String
    public let specs: String?
    public let hero: String?
    public let techUrl: String?
    public let toys: [ResearchToy]?
    public let projects: [ResearchTechProject]?

    enum CodingKeys: String, CodingKey {
        case id, tech, specs, hero, toys, projects
        case techUrl = "tech_url"
    }

    /// Absolute URL for the tech's hero image. Resolves relative paths
    /// (the common case — frontmatter `hero: numpy.jpeg` is rewritten by
    /// `build_technology.py` to `/research/tech/<sci>/<tech>/numpy.jpeg`)
    /// against the site origin.
    public var heroURL: URL? {
        guard let hero else { return nil }
        if hero.hasPrefix("http://") || hero.hasPrefix("https://") {
            return URL(string: hero)
        }
        let trimmed = hero.hasPrefix("/") ? String(hero.dropFirst()) : hero
        return URL(string: "https://vivianweidai.com/" + trimmed)
    }
}

/// A physical instrument that enables a Tech. Mirrors the `toys:` array
/// in each tech page's `index.md` frontmatter, baked into technology.json
/// by `build_technology.py`. Rendered as the Toys list on the tech detail
/// view, matching the website's tech page.
public struct ResearchToy: Codable, Hashable, Sendable, Identifiable {
    public let name: String
    public let description: String
    /// Optional link target for the toy name — usually the project page
    /// that used the instrument. Mirrors the toy `url` field added to the
    /// tech-page frontmatter and baked into technology.json.
    public let url: String?

    public var id: String { name }

    /// In-app project `index.md` URL when the toy links to a research project.
    public var projectIndexURL: URL? {
        guard let url, url.hasPrefix("/research/projects/") else { return nil }
        let trimmed = String(url.dropFirst())
        let withIndex = trimmed.hasSuffix("/") ? trimmed + "index.md" : trimmed + "/index.md"
        return URL(string: "https://vivianweidai.com/" + withIndex)
    }

    /// External URL for non-project toy links (vendor pages, etc.).
    public var externalURL: URL? {
        guard let url, projectIndexURL == nil else { return nil }
        if url.hasPrefix("http://") || url.hasPrefix("https://") { return URL(string: url) }
        let trimmed = url.hasPrefix("/") ? String(url.dropFirst()) : url
        return URL(string: "https://vivianweidai.com/" + trimmed)
    }
}

public struct ResearchTechResponse: Codable, Sendable {
    public let sciences: [ResearchScience]
}

/// Per-tech project entry — reverse-scanned from research projects
/// whose frontmatter `tech:` array references this tech. Baked into
/// `technology.json` by `build_technology.py` so iOS/Android can render
/// the tech detail view without re-scanning every project at runtime.
public struct ResearchTechProject: Codable, Hashable, Sendable, Identifiable {
    public let date: String           // YYYY-MM-DD
    public let title: String
    public let url: String
    public let sciences: [String]
    /// Shuffle-pool photos, project-folder-relative (`photos/setup/setup1.jpeg`).
    /// Baked in by `build_technology.py`, mirroring the build-time scan the
    /// website's `[slug]` route does. Absent for gallery projects, which lay
    /// out their own tiles.
    public let photos: [String]?

    public var id: String { url }

    /// URL of the project's `index.md` for in-app rendering.
    public var indexURL: URL? {
        let trimmed = url.hasPrefix("/") ? String(url.dropFirst()) : url
        let withIndex = trimmed.hasSuffix("/") ? trimmed + "index.md" : trimmed + "/index.md"
        return URL(string: "https://vivianweidai.com/" + withIndex)
    }

    /// Project folder name (`20260405 Melting Point`), percent-decoded — the
    /// stable key for matching a project across the manifest and a URL.
    public var folderName: String? {
        ResearchTechProject.folderName(inPath: url)
    }

    /// Last non-empty path component, ignoring a trailing `index.md`, decoded.
    static func folderName(inPath path: String) -> String? {
        var parts = path.split(separator: "/").map(String.init)
        if parts.last == "index.md" { parts.removeLast() }
        guard let last = parts.last else { return nil }
        return last.removingPercentEncoding ?? last
    }
}

public extension Array where Element == ResearchScience {
    /// Shuffle-pool photos for the project whose `index.md` is at `indexURL`.
    /// The manifest is the single source — the app used to walk the GitHub
    /// contents API here, which is unauthenticated (60 req/hr, shared per
    /// egress IP) and fails silently, leaving an empty photo grid.
    func projectPhotos(forIndexURL indexURL: URL) -> [String] {
        guard let folder = ResearchTechProject.folderName(inPath: indexURL.path) else {
            return []
        }
        for science in self {
            for tech in science.techs {
                for project in tech.projects ?? [] where project.folderName == folder {
                    if let photos = project.photos, !photos.isEmpty { return photos }
                }
            }
        }
        return []
    }
}
