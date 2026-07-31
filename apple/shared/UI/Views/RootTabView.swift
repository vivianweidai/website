import SwiftUI
import ScienceCore

/// Root view for iPhone and iPad.
///
/// On iPhone (compact width) this is a standard bottom TabView. On iPad
/// (regular width) SwiftUI will automatically present the same TabView —
/// the individual screens already use `NavigationStack` which adapts to
/// the wider canvas.
///
/// Default tab is Curriculum, matching the website's home page, which
/// always opens on its Curriculum tab (the auto-rotating tabs were
/// dropped 2026-07-30). At launch, kicks off a parallel preload via the
/// shared ContentStore so Olympiads and Projects populate in the
/// background — when the user taps them the data is already there, no
/// per-tab spinner. See `ContentStore` for why we use a store rather
/// than each view's own `.task`.
public struct RootTabView: View {
    @State private var selection: Tab = .curriculum
    @State private var store = ContentStore.shared

    public init() {}

    public var body: some View {
        TabView(selection: $selection) {
            CurriculumView()
                .tabItem { Image(systemName: "book") }
                .tag(Tab.curriculum)
            OlympiadsView()
                .tabItem { Image(systemName: "trophy") }
                .tag(Tab.olympiads)
            GalleryView()
                .tabItem { Image(systemName: "photo.on.rectangle") }
                .tag(Tab.projects)
        }
        .task { await store.preloadAll() }
    }

    enum Tab: Hashable { case curriculum, olympiads, projects }
}
