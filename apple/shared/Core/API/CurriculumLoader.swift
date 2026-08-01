import Foundation

/// Loads the curriculum manifest from `web/public/curriculum/curriculum.json`
/// and fetches individual table markdown files on demand. Replaces the
/// older `NotesLoader` which walked the GitHub contents API and therefore
/// got section/topic ordering wrong (alphabetical instead of the canonical
/// order that `build_curriculum.py` produces).
///
/// The manifest is cached for the life of the actor so repeated navigation
/// into the curriculum tab doesn't re-download it. Call `invalidate()` to
/// force a refresh (wired to pull-to-refresh).
public actor CurriculumLoader {
    public static let shared = CurriculumLoader()

    private static let manifestURL = URL(
        string: "https://vivianweidai.com/curriculum/curriculum.json"
    )!
    private static let rawBaseURL = URL(
        string: "https://vivianweidai.com/curriculum/content/"
    )!

    private let session: URLSession
    private var cachedManifest: CurriculumManifest?

    public init(session: URLSession = .shared) {
        self.session = session
    }

    public func manifest() async throws -> CurriculumManifest {
        if let cachedManifest { return cachedManifest }
        var request = URLRequest(url: Self.manifestURL)
        request.cachePolicy = .reloadRevalidatingCacheData
        let (data, response) = try await session.data(for: request)
        try Self.checkHTTP(response)
        let manifest = try CurriculumManifest(from: data)
        cachedManifest = manifest
        return manifest
    }

    public func invalidate() {
        cachedManifest = nil
    }

    /// Fetch the raw markdown body for a given table. The manifest's
    /// `path` field is relative to `curriculum/`, so we resolve against
    /// `raw.githubusercontent.com/.../curriculum/` to build the full URL.
    public func body(for table: CurriculumTable) async throws -> String {
        guard let encodedPath = table.path.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed),
              let url = URL(string: encodedPath, relativeTo: Self.rawBaseURL) else {
            throw URLError(.badURL)
        }
        var request = URLRequest(url: url)
        request.cachePolicy = .reloadRevalidatingCacheData
        let (data, response) = try await session.data(for: request)
        try Self.checkHTTP(response)
        return String(data: data, encoding: .utf8) ?? ""
    }

    private static func checkHTTP(_ response: URLResponse) throws {
        guard let http = response as? HTTPURLResponse,
              (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
    }
}
