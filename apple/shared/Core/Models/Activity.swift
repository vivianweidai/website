import Foundation

public struct Activity: Identifiable, Hashable, Codable, Sendable {
    public let id: Int
    public let type: String           // "olympiad" or "textbook"
    public let subject: String
    public let date: String
    public let sortKey: String
    public let name: String
    public let highlighted: Int
    public let subjects: [String]?
    public let invited: Int?
    public let attended: Int?
    public let competitive: Int?
    public let alternate: Int?

    enum CodingKeys: String, CodingKey {
        case id, type, subject, date, name, highlighted, subjects
        case invited, attended, competitive, alternate
        case sortKey = "sort_key"
    }

    public var isOlympiad: Bool { type == "olympiad" }
    public var isTextbook: Bool { type == "textbook" }
}

public struct ActivityList: Codable, Sendable {
    public let items: [Activity]

    public init(items: [Activity]) {
        self.items = items
    }
}
