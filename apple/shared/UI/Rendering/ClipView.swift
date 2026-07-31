import SwiftUI
import AVKit

/// A clip on the wall, and the player it opens into.
///
/// The website's wall autoplays an `.mp4` tile muted and looping in place —
/// "video is a tile like any other" — and its lightbox opens the same clip
/// with controls. The app used to hand a clip to Safari, which left the app to
/// show one tile. These two views close that gap: `LoopingClipView` is the
/// tile, `ClipPlayerView` is the lightbox.
#if canImport(UIKit)

import UIKit

/// Muted, looping, no controls — the tile itself. Playback stops when the
/// tile scrolls out of the lazy stack so a wall of clips is never more than
/// the one or two on screen.
struct LoopingClipView: UIViewRepresentable {
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
        // No stalls on a slow network: a tile that hitches reads as broken,
        // where a tile that waits a beat reads as loading.
        player.automaticallyWaitsToMinimizeStalling = true
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

    var body: some View {
        ZStack(alignment: .topTrailing) {
            Color.black.ignoresSafeArea()

            if let player {
                VideoPlayer(player: player)
                    .ignoresSafeArea()
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
        .onAppear {
            let created = AVPlayer(url: url)
            created.play()
            player = created
            // Loop, matching the tile and the web lightbox.
            NotificationCenter.default.addObserver(
                forName: .AVPlayerItemDidPlayToEndTime,
                object: created.currentItem,
                queue: .main
            ) { _ in
                created.seek(to: .zero)
                created.play()
            }
        }
        .onDisappear {
            player?.pause()
            player = nil
        }
    }
}

#endif
