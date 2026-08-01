# APPSTORE — shipping the iOS app

Build + submit **My Science** to the App Store. Run everything from `apple/`, on the main dev box.
Architecture and the two runtime traps are in `../CLAUDE.md` § APPLE APP, not here.

## Before you start

🔒 **No App Store Connect identifiers live in this repo — it is public.** Team ID, app ID, API Key
ID, issuer and account-holder name go in `apple/.release.env` (gitignored) or the operator's own
records. The `.p8` upload key stays at `~/.appstoreconnect/private_keys/` (600), referenced by
path, never committed.

## Release flow

1. `xcodegen generate`
2. Bump `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` in `project.yml`
3. Archive:
   ```
   xcodebuild -project Science.xcodeproj -scheme Science -configuration Release \
     -destination 'generic/platform=iOS' -archivePath build/Science.xcarchive \
     -allowProvisioningUpdates archive
   ```
4. Export — ⚠️ **with NO `-authenticationKey*` args**, see the signing gotcha below:
   ```
   xcodebuild -exportArchive -archivePath build/Science.xcarchive \
     -exportOptionsPlist <plist: method=app-store-connect, destination=export,
                          signingStyle=automatic, teamID=…> \
     -exportPath build/export -allowProvisioningUpdates
   ```
5. `xcrun altool --upload-app -f build/export/Science.ipa -t ios --apiKey <KEY_ID> --apiIssuer <ISSUER>`
6. Wait a few min for processing, then in ASC web:
   **iOS App +** → new version → **What's New** → **Add Build** → release option → **Add for
   Review** → **Submit for Review**

✅ **Check the Included Assets row** under the chosen build before submitting: it should list
*App Icon* **+ *Apple Watch***. That is the one place the embedded watch app is visibly riding
along — there is no separate watch submission.

*Verified end-to-end on 1.5.6 build 4 (2026-07-30), the ASC steps driven through Claude-in-Chrome
on an already-signed-in session.*

### ⚠️ The signing gotcha — the thing that wastes a cycle

The dev box typically has only an *Apple Development* cert, **no distribution cert**, and an
*App Manager* API key **cannot do cloud signing** — you get
`No signing certificate "iOS Distribution" found`.

**Fix without an Admin key:** run `-exportArchive` **without** the `-authenticationKey*` args, so it
re-signs via the **signed-in Xcode account session** instead. With `-allowProvisioningUpdates` the
account holder can create the dist cert and profiles silently. Then upload separately with `altool`.

### Resubmitting a version already *Waiting for Review*

ASC will not accept a new build while the version sits in review.

1. Click **remove this version from review** → it flips to *Developer Rejected* and becomes editable
2. Attach the build → it flips to *Prepare for Submission*
3. **Add for Review** → **Submit for Review**

⚠️ **Keep `MARKETING_VERSION` unchanged; bump only `CURRENT_PROJECT_VERSION`.** The ASC version
record is pinned to the marketing string, so a build carrying a different one is not selectable.

### Dev install (for review, not release)

`xcodebuild … build`, then
`xcrun devicectl device install app --device <coredevice-id> <Science.app>`. The phone must be
unlocked to launch.

`ITSAppUsesNonExemptEncryption: NO` is set in `project.yml`, so export compliance never prompts.

## Screenshots

**One set per device family — that is the whole policy.** Every smaller iPhone size (6.5", 6.3")
reads *"Using 6.9" Display"* and inherits, so the 6.5" and 13"-landscape sets were **deleted, not
replaced**. A second set is a second thing to remember to refresh, which is exactly how the last
one went stale.

| Set | Pixels | Simulator | Shots |
|---|---|---|---|
| iPhone 6.9" | 1320 × 2868 | iPhone 17 Pro Max | 6 — curriculum list · curriculum table · olympiads timeline · wall (photo tiles) · wall (project cards) · project page |
| iPad 13" | 2064 × 2752 | iPad Pro 13-inch M5 | 4 — curriculum list · curriculum table · olympiads timeline · wall filtered to Chemistry |

Both portrait. Last refreshed 2026-07-30 for 1.5.6 build 5.

### 🔴 Media Manager's file inputs go stale on every re-render

Uploading N files in one call lands them in **nondeterministic order**, and a `ref` captured before
a *Delete All* **silently rebinds to the next section's input** — which is how six 6.9" screenshots
were uploaded against the 6.5" size limits and rejected.

- **Upload one file per call.** Order of upload is order on the listing.
- **Re-`find` the input** after any action that redraws the section.

### Driving the simulator

`cliclick` (Homebrew) posts raw CGEvents at *screen* coordinates, so the device-pixel → screen-point
mapping has to be right.

1. **Set the window to Window ▸ Point Accurate first** — the iPad otherwise renders at ~70% and
   every tap misses.
2. `global = window_origin + inset + device_px / scale`, where inset is **(12, 18)** for the
   bezel-less phone window and **(56, 120)** for the bezelled iPad one.
3. ⚠️ **Scrolling must use `cliclick dd: … dm: … du:`** — a plain `m:` between press and release
   posts *mouseMoved* rather than *leftMouseDragged*, and the scroll view ignores it entirely.
4. Capture with `xcrun simctl io <udid> screenshot` — comes out at exactly the pixel sizes ASC wants.

💡 The Olympiads tab **preselects a random subject on every launch** (matching the website).
Relaunch until a good one comes up rather than trying to drive the filter menu.
