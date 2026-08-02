# Apple

Universal SwiftUI app ("My Science" on the App Store) mirroring vivianweidai.com on iPhone + iPad, with an embedded watchOS companion focused on the olympiads timeline. All data comes from public GitHub raw and `vivianweidai.com` URLs — no auth, no backend, no writes.

Run everything from `apple/`, on the main dev box. Repo-wide conventions and the three verticals are `../CLAUDE.md`.


## The two-package split

The SwiftPM package (`Package.swift`, iOS 17 + watchOS 10) is split in two so the watch target shares data and grouping logic without dragging in WebKit:

- `ScienceCore` — platform-neutral `Models/`, `API/` clients, and the `ActivityGrouping` / `SubjectPaletteRGB` helpers (`shared/Core/`). Builds on iOS, watchOS, macOS.
- `ScienceCoreUI` — iOS-only SwiftUI views plus the KaTeX `MarkdownWebView` (`shared/UI/`). Depends on `ScienceCore`.

The iPhone/iPad target (`ios/`) imports `ScienceCoreUI`; the watch target (`watch/`) imports only `ScienceCore` and owns its own views.

The watch app is embedded in the iOS bundle, so installing on iPhone auto-installs the companion on a paired watch. Bundle IDs `com.vivianweidai.science` and `.science.watchkitapp`. There is no separate watch submission: the embedded app rides inside the one iOS IPA, shares its `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION`, and goes through review with it, so watch changes never wait on a release of their own.

`project.yml` is the XcodeGen spec; regenerate the gitignored `Science.xcodeproj` with `xcodegen generate`.


## The three tabs

`shared/UI/Views/RootTabView.swift`. Each reads a generated JSON manifest — the same ones the webapp uses. `APIClient` fetches exactly two, `olympiads.json` and `thewall.json`, plus `curriculum.json` via `CurriculumLoader`. Nothing else.

- Curriculum — cascading subject → section → topic → table browser from `curriculum/curriculum.json`; tables fetched from GitHub raw URLs, rendered with KaTeX in a `WKWebView`.
- Olympiads — contests and unified textbooks from `olympiads/olympiads.json`. The watch companion renders this tab only, offline-first from `Caches/olympiads_cache.json`. Both surfaces carry the timeline's four standing markers in the website's own vocabulary — invited/attended, competitive, Team Canada/alternate — and the watch's detail badges use its label set (FOUNDATION / ATTENDED / INVITED / COMPETITIVE / TEAM CANADA / ALTERNATE).
- Projects — the same wall the website shows, from `projects/thewall/thewall.json`, laid out by the same rules (`WallMetrics` ports the CSS grid): landscape and square tiles span two columns, portraits take one, tiles stay in manifest order, and a half-filled row keeps its gap rather than back-filling. A photo tile carries no text — caption and science pill belong to project cards, which are framed in their science colour and badged `PROJECT →`. Tapping a photo opens the full-resolution pager; a project card opens that project's `report.md` in the markdown reader; a clip autoplays muted in place and opens with controls in-app (`ClipView.swift`).

Because the wall reads the same manifest the site builds, a row added to `thewall/thewall.yml` appears in the app with no release. Only layout changes need one.


## The two runtime traps

Both were silent failures with no error anywhere, and both are load-bearing.

Tiles load through `RemoteImage`, never `AsyncImage`. The wall does not ship thumbnails, so `src` is the 2000 px original and `AsyncImage` would decode about 12 MB per tile to fill a 190 pt box. `RemoteImage` downsamples at decode time and caches the result.

Clips must play from a downloaded copy, never from their https URL. `vivianweidai.com` answers a `Range:` request with a plain `200` and the whole body — no `Accept-Ranges`, no `206` — and AVFoundation will not start a remote asset it cannot seek, so both wall clips sat on their poster frame forever. `ClipCache` in `ClipView.swift` fetches the bytes with `URLSession`, which does not care, parks them in `Caches/clips/`, and hands AVPlayer a file URL.

Browsers tolerate the same response, which is why the website's `<video>` tags never showed the problem. If the range behaviour is ever fixed at the edge this stays correct, it just stops being load-bearing. Verify a clip by screenshotting the wall twice a few seconds apart and diffing: a poster is byte-identical, playback is not.


## Markdown shell contract

`shared/UI/Rendering/katex-shell.html`. Three things a project page can rely on in-app:

- Page `<style>` blocks are honored. CommonMark treats `<style>` as a type-1 HTML block, so marked passes it through, blank lines and all. A page `<script>` still never runs — `innerHTML` does not execute scripts, so anything interactive has to be native.
- Images open a native zoomable viewer rather than Safari. The shell posts the tapped image plus the page's full image list over an `imageTap` bridge and `ImageViewerView` pages through them with pinch, double-tap and swipe. Non-image links still hand off to Safari.
- `<video>` and `<source>` relative `src` is resolved like `<img>`, and the WebView allows inline autoplay. That combination is what makes the Stargazing solar hero play.


## Shipping — before you start

No App Store Connect identifiers live in this repo, because it is public. Team ID, app ID, API Key ID, issuer and account-holder name go in `.release.env` (gitignored) or the operator's own records. The `.p8` upload key stays at `~/.appstoreconnect/private_keys/` at mode 600, referenced by path, never committed.


## Release flow

1. `xcodegen generate`
2. Bump `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` in `project.yml`
3. Archive:
   ```
   xcodebuild -project Science.xcodeproj -scheme Science -configuration Release \
     -destination 'generic/platform=iOS' -archivePath build/Science.xcarchive \
     -allowProvisioningUpdates archive
   ```
4. Export — with NO `-authenticationKey*` args, see the signing gotcha below:
   ```
   xcodebuild -exportArchive -archivePath build/Science.xcarchive \
     -exportOptionsPlist <plist: method=app-store-connect, destination=export,
                          signingStyle=automatic, teamID=…> \
     -exportPath build/export -allowProvisioningUpdates
   ```
5. `xcrun altool --upload-app -f build/export/Science.ipa -t ios --apiKey <KEY_ID> --apiIssuer <ISSUER>`
6. Wait a few minutes for processing, then in ASC web: iOS App + → new version → What's New → Add Build → release option → Add for Review → Submit for Review

Check the Included Assets row under the chosen build before submitting: it should list App Icon + Apple Watch. That is the one place the embedded watch app is visibly riding along.

The ASC steps can be driven through Claude-in-Chrome on an already-signed-in session.


### The signing gotcha — the thing that wastes a cycle

The dev box typically has only an Apple Development cert, no distribution cert, and an App Manager API key cannot do cloud signing, so you get `No signing certificate "iOS Distribution" found`.

Fix without an Admin key: run `-exportArchive` without the `-authenticationKey*` args, so it re-signs via the signed-in Xcode account session instead. With `-allowProvisioningUpdates` the account holder can create the dist cert and profiles silently. Then upload separately with `altool`.


### Resubmitting a version already Waiting for Review

ASC will not accept a new build while the version sits in review. Removing it costs your place in the review queue — that is the whole price, so decide before clicking.

1. Click remove this version from review → confirm → it flips to Developer Rejected
2. Swap the build. The attached build has no visible controls: hover its row to reveal a red remove button at the far right. Remove it, and the Add Build button reappears. Pick the new build → Done. Only builds that have finished processing are listed; a fresh upload usually takes a few minutes.
3. Save. The version flips to Prepare for Submission.
4. Reload the page. `Add for Review` stays greyed out until you do. It reads exactly like a validation failure, but it is stale UI.
5. Add for Review → the draft panel opens; confirm it lists the version and build you expect → Submit for Review
6. Confirmation reads "1 Item Submitted", up to 48 hours, email on completion.

Keep `MARKETING_VERSION` unchanged and bump only `CURRENT_PROJECT_VERSION`. The ASC version record is pinned to the marketing string, so a build carrying a different one is not selectable.


### Dev install, for review rather than release

`xcodebuild … build`, then `xcrun devicectl device install app --device <coredevice-id> <Science.app>`. The phone must be unlocked to launch.

`ITSAppUsesNonExemptEncryption: NO` is set in `project.yml`, so export compliance never prompts.


## Screenshots

One set per device family — that is the whole policy. Every smaller iPhone size (6.5", 6.3") reads "Using 6.9" Display" and inherits, so there is no 6.5" or 13"-landscape set. A second set is a second thing to remember to refresh, which is exactly how the last one went stale.

| Set | Pixels | Simulator | Shots |
|---|---|---|---|
| iPhone 6.9" | 1320 × 2868 | iPhone 17 Pro Max | 6 — curriculum list · curriculum table · olympiads timeline · wall (photo tiles) · wall (project cards) · project page |
| iPad 13" | 2064 × 2752 | iPad Pro 13-inch M5 | 4 — curriculum list · curriculum table · olympiads timeline · wall filtered to Chemistry |

Both portrait.


### Media Manager's file inputs go stale on every re-render

Uploading N files in one call lands them in nondeterministic order, and a `ref` captured before a Delete All silently rebinds to the next section's input — which is how six 6.9" screenshots were uploaded against the 6.5" size limits and rejected.

- Upload one file per call. Order of upload is order on the listing.
- Re-`find` the input after any action that redraws the section.


### Driving the simulator

`cliclick` (Homebrew) posts raw CGEvents at screen coordinates, so the device-pixel to screen-point mapping has to be right.

1. Set the window to Window ▸ Point Accurate first — the iPad otherwise renders at about 70 % and every tap misses.
2. `global = window_origin + inset + device_px / scale`, where inset is (12, 18) for the bezel-less phone window and (56, 120) for the bezelled iPad one.
3. Scrolling must use `cliclick dd: … dm: … du:` — a plain `m:` between press and release posts mouseMoved rather than leftMouseDragged, and the scroll view ignores it entirely.
4. Capture with `xcrun simctl io <udid> screenshot`, which comes out at exactly the pixel sizes ASC wants.

The Olympiads tab preselects a random subject on every launch, matching the website. Relaunch until a good one comes up rather than trying to drive the filter menu.
