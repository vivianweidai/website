import Foundation

/// Read-only client for activity listings (olympiads + textbooks) and the
/// projects wall.
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
    public static let wallURL = URL(
        string: "https://vivianweidai.com/projects/thewall/thewall.json"
    )!

    private let session: URLSession
    private let decoder: JSONDecoder
    private var cachedActivities: [Activity]?
    private var cachedWall: TheWallResponse?

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

    public func loadWall() async throws -> TheWallResponse {
        if let cachedWall { return cachedWall }
        let wall = try await get(url: Self.wallURL, as: TheWallResponse.self)
        cachedWall = wall
        return wall
    }

    /// Invalidate caches — wired to pull-to-refresh so users can force
    /// a round trip when they've just pushed new YAML.
    public func invalidate() {
        cachedActivities = nil
        cachedWall = nil
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
