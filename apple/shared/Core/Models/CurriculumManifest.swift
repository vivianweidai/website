import Foundation

/// Strongly-typed mirror of `web/public/curriculum/curriculum.json`, which is
/// the single source of truth for curriculum structure and ordering.
///
/// The build script (`pipeline/scripts/build_curriculum.py`) emits subjects,
/// sections, topics, and tables in a canonical order — never alphabetical
/// — and attaches `highlighted_rows` for each table so the render layer
/// knows which data rows to highlight. We decode the JSON verbatim and
/// then re-order subjects into the canonical webapp sequence.
public struct CurriculumManifest: Sendable {
    public let subjects: [CurriculumSubject]

    /// Webapp canonical subject order (see curriculum/index.md). Any
    /// subjects present in the JSON but missing from this list are
    /// appended at the end in decoding order.
    public static let canonicalSubjectOrder = [
        "mathematics", "computing", "physics",
        "chemistry", "biology", "astronomy",
    ]

    public init(from data: Data) throws {
        let raw = try JSONDecoder().decode([String: CurriculumSubject].self, from: data)
        var ordered: [CurriculumSubject] = []
        var remaining = raw
        for slug in Self.canonicalSubjectOrder {
            if let subject = remaining.removeValue(forKey: slug) {
                ordered.append(subject)
            }
        }
        // Stragglers (if build script ever adds a new subject before the
        // client learns about it): append in whatever order Dictionary gives.
        ordered.append(contentsOf: remaining.values)
        self.subjects = ordered
    }

    public func subject(withSlug slug: String) -> CurriculumSubject? {
        subjects.first { $0.slug == slug }
    }
}

public struct CurriculumSubject: Codable, Identifiable, Hashable, Sendable {
    public var id: String { slug }
    public let slug: String
    public let name: String
    public let sections: [CurriculumSection]
}

public struct CurriculumSection: Codable, Identifiable, Hashable, Sendable {
    public var id: String { slug }
    public let slug: String
    public let name: String
    public let topics: [CurriculumTopic]
}

public struct CurriculumTopic: Codable, Identifiable, Hashable, Sendable {
    public var id: String { slug }
    public let slug: String
    public let name: String
    public let tables: [CurriculumTable]
}

public struct CurriculumTable: Codable, Identifiable, Hashable, Sendable {
    public var id: String { path }
    public let name: String
    public let path: String
    public let highlightedRows: [Int]

    enum CodingKeys: String, CodingKey {
        case name, path
        case highlightedRows = "highlighted_rows"
    }
}
