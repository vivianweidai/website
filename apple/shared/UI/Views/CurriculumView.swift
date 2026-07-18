import SwiftUI
import ScienceCore

/// Curriculum landing page. Mirrors the webapp at /curriculum/ with a
/// vertical list of the six subjects in canonical order (Mathematics first,
/// Astronomy last). Tapping a subject cascades into sections → topics →
/// tables, each level preserving the order that `build_curriculum.py`
/// writes into `web/public/curriculum/curriculum.json`.
///
/// Navigation is value-driven (`NavigationStack(path:)`) so the
/// breadcrumb in `CurriculumTopicView` can pop multiple levels at once
/// when the user taps an upstream segment ("Physics" from inside a
/// Harmonics topic).
struct CurriculumView: View {
    @State private var store = ContentStore.shared
    @State private var path: [CurriculumDestination] = []

    var body: some View {
        NavigationStack(path: $path) {
            Group {
                if let manifest = store.manifest {
                    subjectList(manifest)
                } else if let errorMessage = store.manifestError {
                    ErrorState(message: errorMessage)
                } else {
                    LoadingState(
                        title: "Loading curriculum",
                        subtitle: "Fetching the syllabus manifest from GitHub."
                    )
                }
            }
            .navigationTitle("Curriculum")
            .refreshable { await store.refreshAll() }
            .navigationDestination(for: CurriculumDestination.self) { dest in
                switch dest {
                case .subject(let subject):
                    CurriculumSubjectView(subject: subject, path: $path)
                case .section(let subject, let section):
                    CurriculumSectionView(subject: subject, section: section, path: $path)
                case .topic(let subject, let section, let topic):
                    CurriculumTopicView(subject: subject, section: section, topic: topic, path: $path)
                }
            }
        }
    }

    private func subjectList(_ manifest: CurriculumManifest) -> some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                ForEach(manifest.subjects) { subject in
                    NavigationLink(value: CurriculumDestination.subject(subject)) {
                        SubjectRow(subject: subject)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding()
        }
    }

}

/// Push targets in the curriculum cascade. Each case carries every
/// upstream model needed to render that level, so a tap on the
/// breadcrumb can build a fresh path slice (e.g. `[.subject(s)]`)
/// without round-tripping through `ContentStore`.
enum CurriculumDestination: Hashable {
    case subject(CurriculumSubject)
    case section(CurriculumSubject, CurriculumSection)
    case topic(CurriculumSubject, CurriculumSection, CurriculumTopic)
}

/// Single colored row on the curriculum landing page.
private struct SubjectRow: View {
    let subject: CurriculumSubject

    var body: some View {
        HStack {
            Text(subject.name)
                .font(.system(size: 20, weight: .bold))
                .foregroundStyle(Color.black.opacity(0.82))
            Spacer()
            Image(systemName: "chevron.right")
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(Color.black.opacity(0.4))
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 22)
        .frame(maxWidth: .infinity)
        .background(
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .fill(SubjectPalette.color(for: subject.name))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 10, style: .continuous)
                .stroke(Color.black.opacity(0.08), lineWidth: 1)
        )
    }
}

// MARK: - Subject → Sections

/// Level 2: one subject expanded into its sections. The webapp uses a
/// 3-col section grid; iOS collapses this into a simple list in the same
/// canonical order (`build_curriculum.py:SECTION_ORDER`).
///
/// The subject color appears as a breadcrumb strip directly below the
/// navigation bar — matching `CurriculumTopicView` at level 4 — rather
/// than tinting the navigation bar itself. Tinting the nav bar with
/// `.toolbarBackground` caused the bar color to bleed onto the first
/// `List` row during the push transition and flash away once the
/// animation settled; the manual strip sidesteps that bug and keeps
/// all three curriculum levels visually consistent.
struct CurriculumSubjectView: View {
    let subject: CurriculumSubject
    @Binding var path: [CurriculumDestination]

    var body: some View {
        VStack(spacing: 0) {
            SubjectBreadcrumb(subject: subject, trail: [], onTapSubject: nil, onTapTrail: [])
            List {
                ForEach(subject.sections) { section in
                    NavigationLink(value: CurriculumDestination.section(subject, section)) {
                        Text(section.name)
                            .font(.system(size: 16, weight: .semibold))
                            .padding(.vertical, 4)
                    }
                }
            }
        }
        .navigationTitle(subject.name)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
    }
}

// MARK: - Section → Topics

/// Level 3: a single section expanded into its topics. One row per topic,
/// showing just the topic heading — this is an intermediate navigation
/// page, so the concrete table names are deferred to the topic view.
///
/// Like `CurriculumSubjectView`, this carries the subject color through
/// a manual breadcrumb strip below the navigation bar rather than
/// `.toolbarBackground`.
struct CurriculumSectionView: View {
    let subject: CurriculumSubject
    let section: CurriculumSection
    @Binding var path: [CurriculumDestination]

    var body: some View {
        VStack(spacing: 0) {
            SubjectBreadcrumb(
                subject: subject,
                trail: [section.name],
                onTapSubject: { path = [.subject(subject)] },
                onTapTrail: []
            )
            List {
                ForEach(section.topics) { topic in
                    NavigationLink(value: CurriculumDestination.topic(subject, section, topic)) {
                        Text(topic.name)
                            .font(.system(size: 16, weight: .semibold))
                            .padding(.vertical, 4)
                    }
                }
            }
        }
        .navigationTitle(section.name)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
    }
}

/// Colored banner placed immediately below the navigation bar showing
/// the active subject (and optional trail). Mirrors the `breadcrumb`
/// inside `CurriculumTopicView` so levels 2, 3, and 4 all look alike.
///
/// Each segment can be made tappable by passing a non-nil callback —
/// the segment is wrapped in a `Button` whose action pops the
/// `NavigationStack` to the corresponding level. Pass `nil` to leave
/// a segment as plain text (e.g. the leaf segment, which is already
/// the active page).
private struct SubjectBreadcrumb: View {
    let subject: CurriculumSubject
    /// Extra path segments after the subject name. Empty on the
    /// subject landing view, `[section.name]` on the section view,
    /// `[section.name, topic.name]` on the topic view.
    let trail: [String]
    /// Tapping the subject segment runs this — typically pops the
    /// stack back to that subject. Nil = render as plain text.
    let onTapSubject: (() -> Void)?
    /// One callback per `trail` segment, in order. Each entry is
    /// either a closure (segment is tappable) or nil (plain text).
    /// The leaf is conventionally nil since it's the current page.
    let onTapTrail: [(() -> Void)?]

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 6) {
            segment(text: subject.name, bold: true, action: onTapSubject)
            ForEach(Array(trail.enumerated()), id: \.offset) { idx, piece in
                Text("/")
                    .foregroundStyle(.secondary)
                let action = idx < onTapTrail.count ? onTapTrail[idx] : nil
                // Last trail segment is the active page — bold it
                // even when it isn't tappable, matching the topic
                // breadcrumb convention.
                let isLeaf = idx == trail.count - 1
                segment(text: piece, bold: isLeaf, action: action)
            }
            Spacer(minLength: 0)
        }
        .font(.system(size: 12))
        .foregroundStyle(Color.black.opacity(0.82))
        .padding(.horizontal, 14)
        .padding(.vertical, 10)
        .background(SubjectPalette.color(for: subject.name))
    }

    @ViewBuilder
    private func segment(text: String, bold: Bool, action: (() -> Void)?) -> some View {
        let label = Text(text)
            .fontWeight(bold ? .semibold : .regular)
            .lineLimit(1)
            .truncationMode(.tail)
        if let action {
            Button(action: action) { label }
                .buttonStyle(.plain)
        } else {
            label
        }
    }
}

// MARK: - Topic → Tables

/// Level 4: render every table belonging to this topic, stacked in the
/// order that `build_curriculum.py` emits them. The colored breadcrumb
/// at the top mirrors `.curr-breadcrumb[data-subj=...]` on the webapp.
struct CurriculumTopicView: View {
    let subject: CurriculumSubject
    let section: CurriculumSection
    let topic: CurriculumTopic
    @Binding var path: [CurriculumDestination]

    var body: some View {
        VStack(spacing: 0) {
            SubjectBreadcrumb(
                subject: subject,
                trail: [section.name, topic.name],
                onTapSubject: { path = [.subject(subject)] },
                onTapTrail: [
                    { path = [.subject(subject), .section(subject, section)] },
                    nil, // leaf — the page we're on
                ]
            )
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 24) {
                    ForEach(topic.tables) { table in
                        CurriculumTableCard(table: table)
                    }
                }
                .padding(.vertical, 16)
            }
        }
        .navigationTitle(topic.name)
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbarBackground(SubjectPalette.color(for: subject.name), for: .navigationBar)
        .toolbarBackground(.visible, for: .navigationBar)
        #endif
    }
}

/// One rendered table — fetches its markdown body lazily and hands it to
/// MarkdownWebView along with the table name (for the prepended header row)
/// and highlighted row indices from the manifest.
struct CurriculumTableCard: View {
    let table: CurriculumTable

    @State private var markdownBody: String = ""
    @State private var loading = true
    @State private var failed = false

    var body: some View {
        Group {
            if loading {
                ProgressView()
                    .frame(maxWidth: .infinity, minHeight: 80)
            } else if failed {
                VStack(spacing: 6) {
                    Image(systemName: "exclamationmark.triangle")
                    Text("Failed to load \(table.name)")
                        .font(.caption)
                }
                .foregroundStyle(.secondary)
                .frame(maxWidth: .infinity, minHeight: 80)
            } else {
                // No explicit frame — MarkdownWebView sizes itself to its
                // content via a contentHeight binding, and the outer
                // LazyVStack + ScrollView owns the actual scroll gesture.
                MarkdownWebView(
                    markdown: markdownBody,
                    tableName: table.name,
                    highlightedRows: table.highlightedRows
                )
            }
        }
        .task { await load() }
    }

    private func load() async {
        guard markdownBody.isEmpty else { return }
        do {
            markdownBody = try await CurriculumLoader.shared.body(for: table)
            loading = false
        } catch {
            failed = true
            loading = false
        }
    }
}
