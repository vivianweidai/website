import Foundation

/// Strongly-typed mirror of `public/research/technology.json`, the source of
/// truth for the Research page's tech browser.
public struct ResearchTopic: Codable, Identifiable, Hashable, Sendable {
    public let id: Int
    public let science: String
    public let scienceSlug: String
    public let topic: String
    public let categories: [ResearchCategory]

    enum CodingKeys: String, CodingKey {
        case id, science, topic, categories
        case scienceSlug = "science_slug"
    }
}

public struct ResearchCategory: Codable, Identifiable, Hashable, Sendable {
    public let id: Int
    public let category: String
    public let techs: [ResearchTech]
}

public struct ResearchTech: Codable, Identifiable, Hashable, Sendable {
    public let id: Int
    public let tech: String
    public let specs: String?
    public let available: Int?
    public let url: String?
    public let hero: String?
    public let techUrl: String?
    public let toys: [ResearchToy]?
    public let projects: [ResearchTechProject]?

    enum CodingKeys: String, CodingKey {
        case id, tech, specs, available, url, hero, toys, projects
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

    public var isAvailable: Bool { (available ?? 0) == 1 }

    /// External URL for the tech-name link (Wolfram, GitHub, Colab,
    /// vendor pages, etc.). Repo-relative paths are resolved against
    /// `vivianweidai.com`; absolute URLs pass through.
    public var externalURL: URL? {
        guard let raw = url else { return nil }
        if raw.hasPrefix("http://") || raw.hasPrefix("https://") {
            return URL(string: raw)
        }
        let trimmed = raw.hasPrefix("/") ? String(raw.dropFirst()) : raw
        let encoded = trimmed.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? trimmed
        return URL(string: "https://vivianweidai.com/" + encoded)
    }
}

/// A physical instrument that enables a Tech. Mirrors the `toys:` array
/// in each tech page's `index.md` frontmatter, baked into technology.json
/// by `build_technology.py`. Rendered as the Toys list on the tech detail
/// view, matching the website's tech page.
public struct ResearchToy: Codable, Hashable, Sendable, Identifiable {
    public let name: String
    public let description: String

    public var id: String { name }
}

public struct ResearchTechResponse: Codable, Sendable {
    public let topics: [ResearchTopic]
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

    public var id: String { url }

    /// URL of the project's `index.md` for in-app rendering.
    public var indexURL: URL? {
        let trimmed = url.hasPrefix("/") ? String(url.dropFirst()) : url
        let withIndex = trimmed.hasSuffix("/") ? trimmed + "index.md" : trimmed + "/index.md"
        return URL(string: "https://vivianweidai.com/" + withIndex)
    }
}
