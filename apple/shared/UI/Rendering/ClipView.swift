import SwiftUI
import AVKit

/// A clip on the wall, and the player it opens into.
///
/// The website's wall autoplays an `.mp4` tile muted and looping — "video is a
/// tile like any other" — and its lightbox opens the same clip with controls.
/// The app used to hand a clip to Safari, which left the app to show one tile.
/// `LoopingClipView` is the tile; `ClipPlayerView` is the lightbox.
///
/// ⚠️ **Both play from a downloaded copy, never from the https URL.**
/// vivianweidai.com answers a `Range:` request with a plain 200 and the whole
/// file — Cloudflare Static Assets does not do byte ranges through the
/// passthrough Worker — and AVFoundation will not start a remote asset it
/// cannot seek. The clips silently showed their poster forever. `URLSession`
/// has no such objection, so we fetch the bytes, drop them in Caches, and hand
/// AVPlayer a file URL. Fix the server and this stays correct; it just stops
/// being load-bearing.
#if canImport(UIKit)

import UIKit
import CryptoKit

/// Muted, looping, no controls — the tile itself. Shows nothing until its
/// local copy exists, which is fine: the poster sits underneath it.
struct LoopingClipView: View {
    let url: URL
    @State private var localURL: URL?

    var body: some View {
        Group {
            if let localURL {
                LoopingClipSurface(url: localURL)
            } else {
                Color.clear
            }
        }
        .task(id: url) {
            localURL = await ClipCache.shared.localCopy(of: url)
        }
    }
}

private struct LoopingClipSurface: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> LoopingClipUIView {
        let view = LoopingClipUIView()
        view.configure(url: url)
        return view
    }

    func updateUIView(_ uiView: LoopingClipUIView, context: Context) {}

    static func dismantleUIView(_ uiView: LoopingClipUIView, coordinator: ()) {
        uiView.stop()
    }
}

final class LoopingClipUIView: UIView {
    override class var layerClass: AnyClass { AVPlayerLayer.self }
    private var looper: AVPlayerLooper?
    private var queuePlayer: AVQueuePlayer?

    private var playerLayer: AVPlayerLayer { layer as! AVPlayerLayer }

    func configure(url: URL) {
        let item = AVPlayerItem(url: url)
        let player = AVQueuePlayer()
        player.isMuted = true
        looper = AVPlayerLooper(player: player, templateItem: item)
        queuePlayer = player
        playerLayer.player = player
        playerLayer.videoGravity = .resizeAspectFill
        player.play()
    }

    func stop() {
        queuePlayer?.pause()
        playerLayer.player = nil
        looper = nil
        queuePlayer = nil
    }

    /// Playback follows the tile on and off screen, so a wall of clips only
    /// ever costs the one or two actually visible.
    override func willMove(toWindow newWindow: UIWindow?) {
        super.willMove(toWindow: newWindow)
        if newWindow == nil { queuePlayer?.pause() } else { queuePlayer?.play() }
    }
}

/// Full-screen playback with controls, standing in for the web lightbox's
/// `<video controls>`. Loops like the tile does; sound on, since a tap is a
/// deliberate act.
struct ClipPlayerView: View {
    let url: URL
    @Environment(\.dismiss) private var dismiss
    @State private var player: AVPlayer?
    @State private var loopObserver: NSObjectProtocol?

    var body: some View {
        ZStack(alignment: .topTrailing) {
            Color.black.ignoresSafeArea()

            if let player {
                VideoPlayer(player: player)
                    .ignoresSafeArea()
            } else {
                ProgressView()
                    .controlSize(.large)
                    .tint(.white)
            }

            Button {
                dismiss()
            } label: {
                Image(systemName: "xmark")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundStyle(.white)
                    .padding(10)
                    .background(Circle().fill(Color.white.opacity(0.18)))
            }
            .padding(.top, 8)
            .padding(.trailing, 14)
            .accessibilityLabel("Close")
        }
        .statusBarHidden()
        .task(id: url) {
            guard let local = await ClipCache.shared.localCopy(of: url) else { return }
            let created = AVPlayer(url: local)
            loopObserver = NotificationCenter.default.addObserver(
                forName: .AVPlayerItemDidPlayToEndTime,
                object: created.currentItem,
                queue: .main
            ) { _ in
                created.seek(to: .zero)
                created.play()
            }
            player = created
            created.play()
        }
        .onDisappear {
            player?.pause()
            player = nil
            if let loopObserver { NotificationCenter.default.removeObserver(loopObserver) }
        }
    }
}

/// On-disk copies of wall clips, one per URL, kept in Caches. There are two
/// clips on the whole wall, so this is a dictionary and a download — not a
/// cache that needs a policy.
actor ClipCache {
    static let shared = ClipCache()

    private var inFlight: [String: Task<URL?, Never>] = [:]

    func localCopy(of remote: URL) async -> URL? {
        let destination = Self.destination(for: remote)
        if FileManager.default.fileExists(atPath: destination.path) { return destination }
        if let running = inFlight[remote.absoluteString] { return await running.value }

        let task = Task<URL?, Never> {
            do {
                let (temporary, response) = try await URLSession.shared.download(from: remote)
                guard let http = response as? HTTPURLResponse,
                      (200..<300).contains(http.statusCode) else { return nil }
                try? FileManager.default.createDirectory(
                    at: destination.deletingLastPathComponent(),
                    withIntermediateDirectories: true
                )
                try? FileManager.default.removeItem(at: destination)
                try FileManager.default.moveItem(at: temporary, to: destination)
                return destination
            } catch {
                return nil
            }
        }
        inFlight[remote.absoluteString] = task
        let result = await task.value
        inFlight[remote.absoluteString] = nil
        return result
    }

    /// A stable name — the URL's digest, keeping the extension so AVFoundation
    /// can pick the right demuxer for a `.mov` as readily as an `.mp4`.
    private static func destination(for remote: URL) -> URL {
        let digest = SHA256.hash(data: Data(remote.absoluteString.utf8))
            .map { String(format: "%02x", $0) }
            .joined()
            .prefix(32)
        let ext = remote.pathExtension.isEmpty ? "mp4" : remote.pathExtension
        let caches = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
        return caches.appendingPathComponent("clips/\(digest).\(ext)")
    }
}

#endif
