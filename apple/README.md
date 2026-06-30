# Science — Apple App

Universal SwiftUI app that mirrors vivianweidai.com on iPhone and iPad,
with an embedded watchOS companion focused on the olympiads timeline.

The SwiftPM package is split in two so the watch target can share data
and grouping logic without dragging in WebKit:

- **`ScienceCore`** — platform-neutral Models, API clients, and the
  `ActivityGrouping` / `SubjectPaletteRGB` helpers. Builds on iOS,
  watchOS, and macOS.
- **`ScienceCoreUI`** — iOS-only SwiftUI views (`RootTabView`,
  `CurriculumView`, `OlympiadsView`, `ResearchView`) and the KaTeX
  `MarkdownWebView`. Depends on `ScienceCore`.

The iPhone/iPad target imports `ScienceCoreUI`; the watch target
imports only `ScienceCore` and owns its own views under `watch/`.

Three tabs:

- **Curriculum** — cascading subject → section → topic → table browser
  driven by `curriculum/curriculum.json` (the same manifest the
  webapp uses). Individual tables are fetched from GitHub raw URLs and
  rendered with KaTeX in a `WKWebView`, including highlighted rows from
  the manifest.
- **Olympiads** — contests tracker plus unified textbooks list, read
  from `olympiads/olympiads.json` (built from
  `olympiads.yml` via `pipeline/scripts/build_olympiads.py`).
- **Research** — tech browser driven by `research/technology.json`
  (one card per science → flat techs). Project links open an in-app markdown
  render of the project's `index.md`; external links (photos, GitHub,
  Colab, Wolfram, etc.) hand off to Safari.

## Layout

```
apple/
├── Package.swift             SwiftPM manifest — iOS 17 + watchOS 10
├── project.yml               XcodeGen spec — regenerate with `xcodegen generate`
├── shared/
│   ├── Core/                 ScienceCore library (platform-neutral)
│   │   ├── ContentStore.swift @Observable store shared by all 3 tabs
│   │   ├── Models/           Activity, ResearchScience, CurriculumManifest
│   │   ├── API/              APIClient, CurriculumLoader, MarkdownHelper
│   │   └── Grouping/         ActivityGrouping, SubjectPaletteRGB
│   └── UI/                   ScienceCoreUI library (iOS-only)
│       ├── Rendering/        MarkdownWebView + katex-shell.html
│       └── Views/
│           ├── RootTabView.swift          Root (3-tab TabView)
│           ├── CurriculumView.swift       Flashcard browser
│           ├── OlympiadsView.swift        Contests + textbooks
│           └── ResearchView.swift         Research projects
├── ios/                      iPhone + iPad target
│   ├── ScienceApp.swift      @main → RootTabView
│   └── Assets.xcassets/
└── watch/                    watchOS companion target (olympiads-only)
    ├── ScienceWatchApp.swift      @main → OlympiadsRootView
    ├── OlympiadsRootView.swift    Load/refresh + @AppStorage sticky filter
    ├── OlympiadsListView.swift    Year-grouped List with NavigationLink rows
    ├── ActivityRowView.swift      Compact watch-sized row
    ├── ActivityDetailView.swift   Full-record push view (tapped from list)
    ├── ActivityCache.swift        Offline-first Caches/olympiads_cache.json
    ├── SubjectFilterSheet.swift   Subject picker
    ├── SubjectColor.swift         SwiftUI Color bridge
    └── Assets.xcassets/
```

## Building

Run `xcodegen generate` from this directory to create `Science.xcodeproj`,
then open in Xcode.

- **Deployment targets:** iOS 17, watchOS 10
- **Supported destinations:** iPhone, iPad, Apple Watch
- **Bundle IDs:** `com.vivianweidai.science`, `com.vivianweidai.science.watchkitapp`
- **Watch app is embedded in the iOS app bundle** — installing Science
  on the iPhone auto-installs the olympiads companion on a paired watch.
- **Dependencies:** iOS target → `ScienceCoreUI`, watch target → `ScienceCore`.

All data comes from public GitHub raw URLs — no auth, no backend, no writes.
