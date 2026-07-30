import Foundation

/// Strongly-typed mirror of `web/public/projects/gallery.json`, the manifest
/// behind the website's /projects/ wall.
///
/// Built by `pipeline/scripts/build_gallery.py` from `gallery.yml`. The app
/// renders the same wall from the same file, so a row added on the Mac shows
/// up here the next time the app fetches — no app release needed.
///
/// A picture belongs to exactly one science, and that science is the folder it
/// sits in under gallery/ — there is no tagging layer above it.
///
/// Two kinds of tile share the list:
///   photo    a picture (or a clip). Tapping opens the full-resolution viewer.
///   project  a link to a write-up. `href` is the project page's path; tapping
///            opens that project's index.md in the in-app markdown reader.
public struct GalleryResponse: Codable, Sendable {
    public let tiles: [GalleryTile]
    public let sciences: [GalleryScience]
}

public struct GalleryScience: Codable, Sendable, Identifiable {
    public let science: String
    public let slug: String
    public let count: Int

    public var id: String { slug }
}

public struct GalleryTile: Codable, Sendable, Identifiable {
    /// What the wall loads — a long-edge-1000 thumbnail for anything oversized.
    public let src: String
    /// The original, full resolution. What the viewer opens.
    public let full: String
    public let caption: String
    public let science: String
    public let scienceSlug: String
    public let kind: String
    /// Sorting only — the wall never shows a date, on either surface.
    public let date: String
    public let w: Int
    public let h: Int
    /// Project cards only: the project page's path, e.g. `/projects/20260411%20Centrifuge/`.
    public let href: String?
    public let video: Bool?
    /// A still frame for a clip. `AsyncImage` cannot decode an mp4, so this is
    /// what a video tile actually shows.
    public let poster: String?
    /// A project card's shuffle-pool photos, folder-relative. Baked by
    /// build_gallery.py; used to live in technology.json, which is gone.
    public let photos: [String]?

    enum CodingKeys: String, CodingKey {
        case src, full, caption, science, kind, date, w, h, href, video, poster, photos
        case scienceSlug = "science_slug"
    }

    /// Stable across a refresh — `full` is unique per tile because the build
    /// rejects the same bytes appearing twice.
    public var id: String { full }

    public var isProject: Bool { kind == "project" }
    public var isVideo: Bool { video == true }
    public var aspectRatio: Double { h > 0 ? Double(w) / Double(h) : 1 }

    /// What the tile shows: the poster for a clip, otherwise the thumbnail.
    public var thumbURL: URL? { Self.absolute(poster ?? src) }
    public var fullURL: URL? { Self.absolute(full) }

    /// A project card's `index.md`, for the in-app markdown reader — the same
    /// resolution the website's project cards use.
    public var projectIndexURL: URL? {
        guard isProject, let href else { return nil }
        let path = href.hasSuffix("/") ? href + "index.md" : href + "/index.md"
        return Self.absolute(path)
    }

    /// Absolute URLs for a project card's photos, resolved against its folder.
    public var photoURLs: [URL] {
        guard let photos, let href else { return [] }
        let base = href.hasSuffix("/") ? href : href + "/"
        return photos.compactMap { Self.absolute(base + Self.encode($0)) }
    }

    private static func encode(_ path: String) -> String {
        path.split(separator: "/")
            .map { $0.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? String($0) }
            .joined(separator: "/")
    }

    /// Paths in the manifest are site-absolute and already percent-encoded by
    /// the build, so hand them to URL unchanged rather than re-encoding.
    private static func absolute(_ path: String) -> URL? {
        if path.hasPrefix("http://") || path.hasPrefix("https://") {
            return URL(string: path)
        }
        return URL(string: "https://vivianweidai.com" + path)
    }
}
