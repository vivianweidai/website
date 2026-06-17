import SwiftUI
import ScienceCore

/// Unified chronological timeline of olympiads + textbooks, visually matching
/// the webapp at /olympiads/. Groups entries by year (newest first), renders
/// each row with a month label, type icon, subject chips, and name with
/// optional INVITED badge.
///
/// The webapp's implementation lives in olympiads/index.md — keep this view
/// in sync with the timeline JS there when the design changes.
struct OlympiadsView: View {
    @State private var store = ContentStore.shared
    @State private var subject: SubjectFilter = SubjectFilter.randomSubject()

    var body: some View {
        NavigationStack {
            Group {
                if let activities = store.activities {
                    timelineContent(activities: activities)
                } else if let errorMessage = store.activitiesError {
                    ErrorState(message: errorMessage)
                } else {
                    LoadingState(
                        title: "Loading olympiads",
                        subtitle: "Fetching the latest timeline from GitHub."
                    )
                }
            }
            .navigationTitle("Olympiads")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    SubjectFilterMenu(selected: $subject)
                }
            }
            .refreshable { await store.refreshAll() }
        }
    }

    // MARK: - Timeline

    private func timelineContent(activities: [Activity]) -> some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 0) {
                ForEach(yearGroups(for: activities), id: \.year) { group in
                    YearSection(year: group.year, entries: group.entries)
                }
            }
            .padding(.bottom, 24)
        }
    }

    // Grouping semantics shared with watchOS via `ScienceCore`.
    private func yearGroups(for activities: [Activity]) -> [ActivityGrouping.YearGroup] {
        let subjectName: String? = {
            if case .named(let name) = subject { return name }
            return nil
        }()
        let filtered = ActivityGrouping.filtered(activities, subject: subjectName)
        return ActivityGrouping.groupedByYear(filtered)
    }
}

// MARK: - Subject filter

private enum SubjectFilter: Hashable {
    case all
    case named(String)

    static let allCases: [SubjectFilter] = [
        .all,
        .named("Mathematics"),
        .named("Computing"),
        .named("Physics"),
        .named("Chemistry"),
        .named("Biology"),
        .named("Astronomy"),
    ]

    /// Pick a random non-"All" subject for the initial filter on launch,
    /// matching the webapp which randomly preselects one of the six subject
    /// tabs each page load (see olympiads/index.md line 16-18).
    static func randomSubject() -> SubjectFilter {
        let subjects: [SubjectFilter] = allCases.filter {
            if case .all = $0 { return false }
            return true
        }
        return subjects.randomElement() ?? .all
    }

    var label: String {
        switch self {
        case .all: return "All"
        case .named(let n): return n
        }
    }

    var color: Color? {
        switch self {
        case .all: return nil
        case .named(let n): return SubjectPalette.color(for: n)
        }
    }
}

/// Native toolbar filter: a "Filter" button with a colored dot for the
/// active subject opens a system menu of all subjects with a checkmark on
/// the current selection. Adapts to light/dark mode automatically.
private struct SubjectFilterMenu: View {
    @Binding var selected: SubjectFilter

    var body: some View {
        Menu {
            // Plain Button rows (not a Picker) so each subject dot can
            // carry its own palette color. SwiftUI's Picker inside a
            // Menu renders system-tinted symbols only.
            ForEach(SubjectFilter.allCases, id: \.self) { filter in
                Button { selected = filter } label: {
                    filterMenuRow(filter: filter, isSelected: filter == selected)
                }
            }
        } label: {
            HStack(spacing: 4) {
                if let color = selected.color {
                    Circle().fill(color).frame(width: 10, height: 10)
                }
                Text(selected.label)
                    .font(.system(size: 15, weight: .medium))
            }
        }
    }
}

/// Menu row for Olympiads subject filter. ResearchView carries its own
/// near-identical copy because `SubjectFilter` is file-private to each
/// view.
@ViewBuilder
private func filterMenuRow(filter: SubjectFilter, isSelected: Bool) -> some View {
    HStack {
        Text(filter.label)
        Spacer()
        if isSelected {
            Image(systemName: "checkmark")
        }
        if let color = filter.color {
            Circle().fill(color).frame(width: 12, height: 12)
        } else {
            Image(systemName: "square.grid.2x2")
        }
    }
}

/// Initial-load placeholder shown while the first network fetch is in
/// flight. A bare `ProgressView()` reads as a blank screen on iPhone;
/// this wraps it with a title + subtle subtitle so the wait feels
/// intentional. Used by all three top-level tabs.
struct LoadingState: View {
    let title: String
    let subtitle: String

    var body: some View {
        VStack(spacing: 14) {
            ProgressView()
                .controlSize(.large)
            Text(title)
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(.primary)
            Text(subtitle)
                .font(.system(size: 12))
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

/// Simple error display used when the initial fetch fails. Avoids
/// `ContentUnavailableView` which requires macOS 14 and complicates
/// host type-checking via `swift build`.
struct ErrorState: View {
    let message: String

    var body: some View {
        VStack(spacing: 10) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 28))
                .foregroundStyle(.secondary)
            Text("Could not load")
                .font(.headline)
            Text(message)
                .font(.caption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
    }
}

// MARK: - Year section

private struct YearSection: View {
    let year: String
    let entries: [Activity]

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text(year)
                .font(.system(size: 17, weight: .bold))
                .padding(.horizontal)
                .padding(.top, 16)
                .padding(.bottom, 4)

            ForEach(entries) { entry in
                ActivityRow(activity: entry)
                Divider()
                    .padding(.leading, 16)
            }
        }
    }
}

// MARK: - Activity row

private struct ActivityRow: View {
    let activity: Activity

    /// The month label shown in the timeline column. The source-of-truth
    /// dates are full month names ("December 2025"); we abbreviate to three
    /// letters here so longer names don't wrap in the narrow fixed-width
    /// column. Source data is untouched.
    private var month: String {
        let full = activity.date.split(separator: " ").first.map(String.init) ?? ""
        return String(full.prefix(3))
    }

    private var chips: [String] {
        if let subjects = activity.subjects, !subjects.isEmpty {
            return subjects
        }
        return [activity.subject]
    }

    var body: some View {
        let highlighted = activity.highlighted == 1
        // Force dark ink on highlighted rows — in dark mode the default
        // body color is near-white, which is unreadable on the yellow wash.
        // Matches Android OlympiadsView.kt.
        let nameColor: Color = highlighted ? Color.black.opacity(0.82) : Color.primary
        let monthColor: Color = highlighted ? Color.black.opacity(0.55) : Color.secondary

        return HStack(alignment: .firstTextBaseline, spacing: 8) {
            Text(month)
                .font(.system(size: 12, weight: .regular, design: .monospaced))
                .foregroundStyle(monthColor)
                .frame(width: 56, alignment: .leading)

            TypeIcon(isOlympiad: activity.isOlympiad)
                .frame(width: 24)

            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 4) {
                    ForEach(chips, id: \.self) { subject in
                        SubjectChip(subject: subject)
                    }
                }
                HStack(alignment: .firstTextBaseline, spacing: 4) {
                    Text(activity.name)
                        .font(.system(size: 14))
                        .foregroundStyle(nameColor)
                        .fixedSize(horizontal: false, vertical: true)
                    if activity.invited == 1 || activity.attended == 1 {
                        Text("⭐").font(.system(size: 12))
                    }
                    if activity.competitive == 1 {
                        Text("🎯").font(.system(size: 12))
                    }
                    if activity.alternate == 1 {
                        Text("🇨🇦").font(.system(size: 12))
                    }
                }
            }

            Spacer(minLength: 0)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        // Canonical curriculum highlight yellow — #fff056, matching
        // --highlight-bg in archives/apple/shared/UI/Rendering/katex-shell.html
        // and content/research/curriculum.css. Keep these in sync.
        .background(
            highlighted
                ? Color(red: 1.0, green: 0.941, blue: 0.337)
                : Color.clear
        )
    }
}

// MARK: - Subject chip

private struct SubjectChip: View {
    let subject: String

    var body: some View {
        Text(subject)
            .font(.system(size: 10, weight: .semibold))
            .padding(.horizontal, 7)
            .padding(.vertical, 2)
            .background(Capsule().fill(SubjectPalette.color(for: subject)))
            .foregroundStyle(Color.black.opacity(0.82))
    }
}

// MARK: - Type icons

private struct TypeIcon: View {
    let isOlympiad: Bool

    var body: some View {
        if isOlympiad {
            OlympicRings()
                .frame(width: 22, height: 12)
        } else {
            Text("📖")
                .font(.system(size: 13))
        }
    }
}

/// Simplified Olympic rings — 5 circles in two rows matching the webapp SVG.
private struct OlympicRings: View {
    var body: some View {
        ZStack {
            ring(color: Color(red: 0.0, green: 0.51, blue: 0.78), offset: CGPoint(x: -8, y: -2))    // blue
            ring(color: .black, offset: CGPoint(x: 0, y: -2))
            ring(color: Color(red: 0.93, green: 0.20, blue: 0.31), offset: CGPoint(x: 8, y: -2))   // red
            ring(color: Color(red: 0.99, green: 0.69, blue: 0.19), offset: CGPoint(x: -4, y: 3))   // yellow
            ring(color: Color(red: 0.0, green: 0.65, blue: 0.32), offset: CGPoint(x: 4, y: 3))     // green
        }
    }

    private func ring(color: Color, offset: CGPoint) -> some View {
        Circle()
            .strokeBorder(color, lineWidth: 1.2)
            .frame(width: 7, height: 7)
            .offset(x: offset.x, y: offset.y)
    }
}

// MARK: - Subject palette

/// Thin SwiftUI wrapper over `ScienceCore.SubjectPaletteRGB`. The raw
/// (r,g,b) tuples live in Core so the watchOS companion can share them
/// without dragging SwiftUI into the platform-neutral target.
enum SubjectPalette {
    static func color(for subject: String) -> Color {
        let rgb = SubjectPaletteRGB.rgb(for: subject)
        return Color(red: rgb.red, green: rgb.green, blue: rgb.blue)
    }
}
