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
    public var manifest: CurriculumManifest?
    public var gallery: GalleryResponse?

    public var activitiesError: String?
    public var manifestError: String?
    public var galleryError: String?

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
            async let m: Void = self.loadManifest()
            async let g: Void = self.loadGallery()
            _ = await (a, m, g)
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
        manifest = nil
        gallery = nil
        activitiesError = nil
        manifestError = nil
        galleryError = nil
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

    private func loadGallery() async {
        do {
            gallery = try await APIClient.shared.loadGallery()
            galleryError = nil
        } catch {
            galleryError = error.localizedDescription
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
