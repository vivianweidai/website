import SwiftUI
import ScienceCore

/// Full-screen detail for a single activity. Reached by tapping any
/// row in `OlympiadsListView`.
///
/// The row view is deliberately terse (month abbreviation, truncated
/// name, single subject chip) because the watch canvas is narrow. The
/// detail view is where the full information lives: untruncated name,
/// full date string from the source JSON, every subject when an
/// activity spans multiple disciplines, and the historical-record
/// metadata (highlighted, invited, type).
///
/// No countdown, no "days until" — the olympiads listing is a
/// historical record, not a forward-looking tracker.
struct ActivityDetailView: View {
    let activity: Activity

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                header

                Text(activity.name)
                    .font(.system(size: 16, weight: .semibold))
                    .fixedSize(horizontal: false, vertical: true)

                subjectChips

                Text(activity.date)
                    .font(.system(size: 12, weight: .regular))
                    .foregroundStyle(.secondary)

                if !badges.isEmpty {
                    VStack(alignment: .leading, spacing: 4) {
                        ForEach(badges, id: \.self) { badge in
                            BadgeView(text: badge)
                        }
                    }
                }
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .navigationTitle(activity.isOlympiad ? "Olympiad" : "Textbook")
        .navigationBarTitleDisplayMode(.inline)
    }

    /// Type glyph + type label, mirroring the small icon used in the
    /// list row but at a size that actually reads well on the detail
    /// canvas.
    private var header: some View {
        HStack(spacing: 6) {
            Image(systemName: activity.isOlympiad ? "trophy.fill" : "book.fill")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(activity.isOlympiad
                    ? Color(red: 0.99, green: 0.69, blue: 0.19)
                    : Color.secondary)
            Text(activity.isOlympiad ? "Olympiad" : "Textbook")
                .font(.system(size: 12, weight: .semibold))
                .foregroundStyle(.secondary)
                .textCase(.uppercase)
            Spacer(minLength: 0)
        }
    }

    /// Every subject the activity participates in — not just the
    /// primary like the list row shows. One chip per line so the
    /// narrow watch canvas never has to squeeze a chip's text.
    private var subjectChips: some View {
        let all: [String]
        if let subjects = activity.subjects, !subjects.isEmpty {
            all = subjects
        } else {
            all = [activity.subject]
        }
        return VStack(alignment: .leading, spacing: 4) {
            ForEach(all, id: \.self) { label in
                SubjectPillDetail(subject: label)
            }
        }
    }

    /// One chip per badge state, in the website timeline's own vocabulary —
    /// the labels its hover badge shows, in its own precedence order
    /// (FOUNDATION first, then how far the contest got). Stacked rather than
    /// packed in a row: "TEAM CANADA" alone fills a watch line.
    private var badges: [String] {
        var out: [String] = []
        if activity.highlighted == 1 { out.append("FOUNDATION") }
        if activity.attended == 1 { out.append("ATTENDED") }
        if activity.invited == 1 { out.append("INVITED") }
        if activity.competitive == 1 { out.append("COMPETITIVE") }
        if activity.team == 1 { out.append("TEAM CANADA") }
        if activity.alternate == 1 { out.append("ALTERNATE") }
        return out
    }
}

private struct BadgeView: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.system(size: 9, weight: .bold))
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(
                RoundedRectangle(cornerRadius: 4)
                    .fill(Color(red: 1.0, green: 0.84, blue: 0.0))
            )
            .foregroundStyle(Color(red: 0.35, green: 0.27, blue: 0.0))
    }
}

private struct SubjectPillDetail: View {
    let subject: String

    var body: some View {
        Text(subject)
            .font(.system(size: 11, weight: .semibold))
            .lineLimit(1)
            .fixedSize(horizontal: true, vertical: false)
            .padding(.horizontal, 7)
            .padding(.vertical, 2)
            .background(Capsule().fill(SubjectColor.color(for: subject)))
            .foregroundStyle(Color.black.opacity(0.82))
    }
}
