import Foundation
import Observation

/// Single shared data store for the three top-level tabs. Views observe
/// this object via `@Observable` so they re-render automatically when
/// the background preload fills each slot in turn.
///
/// Why a store instead of per-view @State: SwiftUI only runs a tab's
/// `.task` when that tab becomes visible. If the user taps Curriculum
/// while the root-level preload is still fetching, the view's task
/// awaits again and the user sees a spinner. With a store, the root
/// preload writes into `manifest` (etc.) the moment each fetch
/// resolves, and any currently-visible view reading that property
/// refreshes immediately — no second spin.
@MainActor
@Observable
public final class ContentStore {
    public static let shared = ContentStore()

    public var activities: [Activity]?
    public var sciences: [ResearchScience]?
    public var manifest: CurriculumManifest?

    public var activitiesError: String?
    public var sciencesError: String?
    public var manifestError: String?

    private var preloadTask: Task<Void, Never>?

    public init() {}

    /// Kick off all three fetches in parallel. Idempotent — calling
    /// twice during launch is fine; the second call joins the existing
    /// task instead of starting new fetches (the underlying loaders
    /// also cache).
    public func preloadAll() async {
        if let existing = preloadTask {
            await existing.value
            return
        }
        let task = Task {
            async let a: Void = self.loadActivities()
            async let t: Void = self.loadSciences()
            async let m: Void = self.loadManifest()
            _ = await (a, t, m)
        }
        preloadTask = task
        await task.value
    }

    /// Force a fresh fetch (wired to pull-to-refresh). Clears caches
    /// and local state so every tab shows a spinner, then re-populates.
    public func refreshAll() async {
        preloadTask?.cancel()
        preloadTask = nil
        await APIClient.shared.invalidate()
        await CurriculumLoader.shared.invalidate()
        activities = nil
        sciences = nil
        manifest = nil
        activitiesError = nil
        sciencesError = nil
        manifestError = nil
        await preloadAll()
    }

    private func loadActivities() async {
        do {
            activities = try await APIClient.shared.listActivities()
            activitiesError = nil
        } catch {
            activitiesError = error.localizedDescription
        }
    }

    /// Look up a tech by name and return its parent science + the tech,
    /// or nil if the tech isn't present in `sciences` (or `sciences`
    /// hasn't loaded yet). Used by ProjectDetailView to render the
    /// native tech table from a project's `tech:` front-matter array —
    /// each tech resolves to its parent science for the chip.
    public func findTech(named: String) -> (
        science: ResearchScience, tech: ResearchTech
    )? {
        guard let sciences else { return nil }
        for science in sciences {
            if let tech = science.techs.first(where: { $0.tech == named }) {
                return (science, tech)
            }
        }
        return nil
    }

    private func loadSciences() async {
        do {
            sciences = try await APIClient.shared.listResearchSciences()
            sciencesError = nil
        } catch {
            sciencesError = error.localizedDescription
        }
    }

    private func loadManifest() async {
        do {
            manifest = try await CurriculumLoader.shared.manifest()
            manifestError = nil
        } catch {
            manifestError = error.localizedDescription
        }
    }
}
