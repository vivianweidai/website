import Foundation

/// Read-only client for activity listings (olympiads + textbooks) and
/// research tech.
///
/// Source of truth: YAML files under public/content/{olympiads,research}/.
/// A Python build script generates the corresponding .json files in the
/// same dirs, which we fetch from vivianweidai.com directly. No database,
/// no API layer, no writes.
public actor APIClient {
    public static let shared = APIClient()

    public static let olympiadsURL = URL(
        string: "https://vivianweidai.com/olympiads/olympiads.json"
    )!
    public static let techURL = URL(
        string: "https://vivianweidai.com/research/technology.json"
    )!

    private let session: URLSession
    private let decoder: JSONDecoder
    private var cachedActivities: [Activity]?
    private var cachedSciences: [ResearchScience]?

    public init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
    }

    /// Return cached activities if a previous fetch (e.g. the
    /// app-launch preload) already populated them; otherwise fetch.
    /// Caching here is what makes the background preload useful — when
    /// the user taps the Olympiads tab, its `.task` returns the
    /// already-loaded list instantly.
    public func listActivities() async throws -> [Activity] {
        if let cachedActivities { return cachedActivities }
        let items = try await get(url: Self.olympiadsURL, as: ActivityList.self).items
        cachedActivities = items
        return items
    }

    public func listResearchSciences() async throws -> [ResearchScience] {
        if let cachedSciences { return cachedSciences }
        let sciences = try await get(url: Self.techURL, as: ResearchTechResponse.self).sciences
        cachedSciences = sciences
        return sciences
    }

    /// Invalidate caches — wired to pull-to-refresh so users can force
    /// a round trip when they've just pushed new YAML.
    public func invalidate() {
        cachedActivities = nil
        cachedSciences = nil
    }

    // MARK: - Private

    private func get<T: Decodable>(url: URL, as: T.Type) async throws -> T {
        var request = URLRequest(url: url)
        request.cachePolicy = .reloadRevalidatingCacheData
        let (data, response) = try await session.data(for: request)
        try Self.check(response)
        return try decoder.decode(T.self, from: data)
    }

    private static func check(_ response: URLResponse) throws {
        guard let http = response as? HTTPURLResponse,
              (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
    }
}
