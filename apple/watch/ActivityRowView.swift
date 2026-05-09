import SwiftUI
import ScienceCore

/// One row in the watchOS olympiads list. Tuned for the ~180 pt wide
/// Apple Watch canvas — two-line layout, tight spacing, single
/// subject chip (the iPhone row may show multiple). Highlight
/// behavior matches the iOS `ActivityRow` (yellow wash for
/// `highlighted == 1`, INVITED badge for `invited == 1`).
struct ActivityRowView: View {
    let activity: Activity

    private var month: String {
        let full = activity.date.split(separator: " ").first.map(String.init) ?? ""
        return String(full.prefix(3)).uppercased()
    }

    /// Show just the primary subject — the watch row is too narrow
    /// to wrap multiple chips without looking cluttered. The iPhone
    /// keeps the multi-chip layout for activities with subject arrays.
    private var primarySubject: String {
        if let subjects = activity.subjects, let first = subjects.first {
            return first
        }
        return activity.subject
    }

    var body: some View {
        HStack(alignment: .top, spacing: 6) {
            TypeGlyph(isOlympiad: activity.isOlympiad)
                .frame(width: 14, height: 14)
                .padding(.top, 2)

            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 4) {
                    Text(month)
                        .font(.system(size: 10, weight: .medium, design: .monospaced))
                        .foregroundStyle(.secondary)
                    SubjectPill(subject: primarySubject)
                    if activity.invited == 1 {
                        InvitedDot()
                    }
                    Spacer(minLength: 0)
                }
                Text(activity.name)
                    .font(.system(size: 13, weight: .semibold))
                    .lineLimit(3)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
        .padding(.vertical, 2)
        // Canonical curriculum highlight yellow — #fff056. Watch rows
        // keep a light alpha wash so the dense row text stays legible.
        .listRowBackground(
            activity.highlighted == 1
                ? Color(red: 1.0, green: 0.941, blue: 0.337).opacity(0.22)
                : Color.clear
        )
    }
}

/// Colored capsule for the row's subject. Same hex palette as the
/// iPhone row via `SubjectColor`.
private struct SubjectPill: View {
    let subject: String

    var body: some View {
        Text(subject)
            .font(.system(size: 9, weight: .semibold))
            .padding(.horizontal, 5)
            .padding(.vertical, 1)
            .background(Capsule().fill(SubjectColor.color(for: subject)))
            .foregroundStyle(Color.black.opacity(0.82))
    }
}

private struct InvitedDot: View {
    var body: some View {
        Text("★")
            .font(.system(size: 9, weight: .bold))
            .foregroundStyle(Color(red: 1.0, green: 0.75, blue: 0.0))
            .accessibilityLabel("Invited")
    }
}

/// Tiny glyph that distinguishes olympiads from textbooks. Watch
/// screen is too small for the full 5-ring Olympic logo the iPhone
/// uses, so we fall back to SF Symbols.
private struct TypeGlyph: View {
    let isOlympiad: Bool

    var body: some View {
        Image(systemName: isOlympiad ? "trophy.fill" : "book.fill")
            .font(.system(size: 11, weight: .semibold))
            .foregroundStyle(isOlympiad
                ? Color(red: 0.99, green: 0.69, blue: 0.19)   // matches olympic yellow ring
                : Color.secondary)
    }
}
