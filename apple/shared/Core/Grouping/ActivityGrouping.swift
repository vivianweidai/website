import Foundation

/// Pure-data helpers for filtering and grouping the unified olympiad +
/// textbook list. Lifted out of the iOS `OlympiadsView` so the watchOS
/// companion can share the exact same semantics.
///
/// No SwiftUI or UIKit dependencies — call sites map these results to
/// their platform's view types.
public enum ActivityGrouping {
    /// Filter activities by a single subject name. Passing `nil` (or an
    /// empty string) returns everything. When an activity has a
    /// `subjects` array it matches if the array contains `subject`;
    /// otherwise the scalar `subject` field is used. Results are sorted
    /// newest-first by `sortKey`.
    public static func filtered(_ items: [Activity], subject: String?) -> [Activity] {
        let matched: [Activity]
        if let subject, !subject.isEmpty {
            matched = items.filter { activity in
                if let all = activity.subjects, !all.isEmpty {
                    return all.contains(subject)
                }
                return activity.subject == subject
            }
        } else {
            matched = items
        }
        return matched.sorted { $0.sortKey > $1.sortKey }
    }

    /// Groups a (pre-sorted) list of activities into year buckets in
    /// source order. The returned array preserves the order the
    /// buckets were first encountered, so callers that pass a
    /// newest-first list get newest-year-first groups.
    public static func groupedByYear(_ items: [Activity]) -> [YearGroup] {
        var order: [String] = []
        var buckets: [String: [Activity]] = [:]
        for entry in items {
            let year = String(entry.sortKey.prefix(4))
            if buckets[year] == nil {
                order.append(year)
                buckets[year] = []
            }
            buckets[year]?.append(entry)
        }
        return order.map { YearGroup(year: $0, entries: buckets[$0] ?? []) }
    }

    public struct YearGroup: Identifiable, Hashable, Sendable {
        public let year: String
        public let entries: [Activity]
        public var id: String { year }

        public init(year: String, entries: [Activity]) {
            self.year = year
            self.entries = entries
        }
    }
}

/// Canonical six-subject palette as RGB tuples in the [0, 1] range.
/// Matches the webapp/iOS hex colors but avoids a SwiftUI dependency so
/// `ScienceCore` stays platform-neutral. Watch and iOS views convert
/// these to `Color` at the edge.
public enum SubjectPaletteRGB {
    public static let canonicalSubjects: [String] = [
        "Mathematics", "Computing", "Physics", "Chemistry", "Biology", "Astronomy",
    ]

    /// Short slug for a science — "Mathematics" -> "math". Mirrors the slugs
    /// the website uses in its URLs and chip class names.
    public static func slug(for subject: String) -> String {
        switch subject {
        case "Mathematics": return "math"
        case "Computing":   return "comp"
        case "Physics":     return "phys"
        case "Chemistry":   return "chem"
        case "Biology":     return "bio"
        case "Astronomy":   return "astro"
        default:            return subject.lowercased()
        }
    }

    /// (red, green, blue) in [0, 1]. Returns a neutral gray for anything
    /// outside the canonical six subjects.
    public static func rgb(for subject: String) -> (red: Double, green: Double, blue: Double) {
        switch subject {
        case "Mathematics": return (0.773, 0.851, 0.969) // #c5d9f7
        case "Computing":   return (0.851, 0.800, 0.933) // #d9ccee
        case "Physics":     return (0.976, 0.769, 0.659) // #f9c4a8
        case "Chemistry":   return (0.831, 0.910, 0.627) // #d4e8a0
        case "Biology":     return (0.659, 0.867, 0.831) // #a8ddd4
        case "Astronomy":   return (0.957, 0.761, 0.796) // #f4c2cb
        default:            return (0.82, 0.82, 0.84)    // neutral gray fallback
        }
    }
}
