# RELEASE — shipping the iOS app

The operational runbook for building and submitting **My Science** to the App Store. Split out of
the root `CLAUDE.md` on 2026-08-01: that doc is the repo's *orientation*, and this is a procedure
run about three times a year. Architecture, the three tabs, and the two ⚠️ runtime traps stay in
`CLAUDE.md` § APPLE APP — they describe what the app *is*, and are load-bearing far more often
than this is.

Everything below is run from `apple/`.

### App Store release

The native app is built + submitted from the main dev box. Run from `apple/`. **This repo is public — the concrete App Store Connect account identifiers (team ID, app ID, API Key ID, issuer, account-holder name) are NOT stored here.** Keep them in an untracked local file (`apple/.release.env`, gitignored) or the operator's own records; the `.p8` upload key stays at `~/.appstoreconnect/private_keys/` (600 perms) and is referenced by path, never committed.

**Signing gotcha (the thing that wastes a cycle):** the dev box typically has only an *Apple Development* cert — **no distribution cert** — and an *App Manager* API key **cannot do cloud signing** (`No signing certificate "iOS Distribution" found`). Fix without an Admin key: run `xcodebuild -exportArchive` **without** the `-authenticationKey*` args so it re-signs for distribution via the **signed-in Xcode account session** (the team's account holder can create the dist cert/profiles silently with `-allowProvisioningUpdates`), export a local IPA, then upload separately with `altool`.

**Flow (from `apple/`):**
1. `xcodegen generate`
2. Bump the version in `project.yml` (`MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`).
3. `xcodebuild -project Science.xcodeproj -scheme Science -configuration Release -destination 'generic/platform=iOS' -archivePath build/Science.xcarchive -allowProvisioningUpdates archive`
4. `xcodebuild -exportArchive -archivePath build/Science.xcarchive -exportOptionsPlist <plist: method=app-store-connect, destination=export, signingStyle=automatic, teamID=…> -exportPath build/export -allowProvisioningUpdates` (**no** auth key → the Xcode session signs)
5. `xcrun altool --upload-app -f build/export/Science.ipa -t ios --apiKey <KEY_ID> --apiIssuer <ISSUER>`
6. Build processes a few min. Then in ASC web: iOS App **+** → new version → **What's New** → **Add Build** → release option → **Add for Review** → **Submit for Review**.

`ITSAppUsesNonExemptEncryption: NO` is set in `project.yml`, so export-compliance never prompts. Direct-to-device dev install (for review) is separate: `xcodebuild … build`, then `xcrun devicectl device install app --device <coredevice-id> <Science.app>` (phone must be unlocked to launch).

**The flow above is verified end-to-end, 1.5.6 (build 4), 2026-07-30** — archive → export without auth args → `altool` → the six ASC web steps, the last of them driven through Claude-in-Chrome on an already-signed-in session. Build 4 had finished processing by the time the version metadata was filled in, so **Add Build** never had to be waited on. The **Included Assets** row under the chosen build lists *App Icon* + *Apple Watch*, which is the one place the embedded watch app visibly rides along — check it before submitting.

**Resubmitting a version that is already Waiting for Review** (1.5.6 build 5, 2026-07-30): ASC will not take a new build while the version sits in review, so click **remove this version from review** on the version page. The version flips to *Developer Rejected* and becomes fully editable; attaching a build then flips it to *Prepare for Submission*, and **Add for Review** → **Submit for Review** puts it back in the queue. Keep `MARKETING_VERSION` unchanged and bump only `CURRENT_PROJECT_VERSION` — the ASC version record is pinned to the marketing string, so a build carrying a different one would not be selectable.

### App Store screenshots

**Refreshed 2026-07-30 for 1.5.6 (build 5)** — they had been stale since the Research→Projects rename. Current sets, both captured in portrait from simulators:

- **iPhone 6.9"** (1320 × 2868, iPhone 17 Pro Max sim) — 6 shots: curriculum list · curriculum table · olympiads timeline · the wall (photo tiles) · the wall (project cards) · a project page.
- **iPad 13"** (2064 × 2752, iPad Pro 13-inch M5 sim) — 4 shots: curriculum list · curriculum table · olympiads timeline · the wall filtered to Chemistry.

**The 6.5" and 13"-landscape sets were deleted, not replaced.** Every smaller iPhone size (6.5", 6.3") now reads *"Using 6.9" Display"* and inherits, which is the whole reason to keep exactly one set per device family — a second set is a second thing to remember to refresh, and that is precisely how the last one went stale.

⚠️ **Media Manager's file inputs go stale on every re-render.** Uploading N files in one call lands them in **nondeterministic order**, and a `ref` captured before a *Delete All* silently rebinds to the *next* section's input — which is how six 6.9" screenshots ended up rejected against the 6.5" size limits. Upload **one file per call**, and **re-`find` the input** after any action that redraws the section. Order of upload is order on the listing.

**Driving the simulator for captures** (`cliclick`, installed via Homebrew): taps and swipes are posted as raw CGEvents at screen coordinates, so the device-pixel → screen-point mapping has to be right. Set the window to **Window ▸ Point Accurate** first (the iPad otherwise renders at ~70% and every tap misses), then `global = window_origin + inset + device_px / scale`, where the inset is `(12, 18)` for the bezel-less phone window and `(56, 120)` for the bezelled iPad one. Scrolling **must** use `cliclick dd: … dm: … du:` — plain `m:` between press and release posts *mouseMoved* rather than *leftMouseDragged*, and the scroll view ignores it entirely. Screenshots come out of `xcrun simctl io <udid> screenshot` at exactly the pixel sizes ASC wants.

The Olympiads tab **preselects a random subject on every launch** (matching the website), so relaunch until a good one comes up rather than trying to drive the filter menu.
