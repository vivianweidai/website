import SwiftUI

/// Async image that decodes at the size it is actually drawn.
///
/// The wall stopped shipping thumbnails on 2026-07-30 — `src` and `full` are
/// now the same file, a long edge of 2000 — so a tile fed to `AsyncImage`
/// decodes a ~2000×1500 bitmap (≈12 MB resident) in order to fill a 190 pt
/// box. Fifty of those is more memory than a phone will hand over, and the
/// wall is fifty tiles. `CGImageSourceCreateThumbnailAtIndex` decodes straight
/// to the target pixel size instead, so a tile costs what a tile is worth.
///
/// Bytes still come through `URLSession.shared`, so the shared `URLCache` is
/// doing the network-level caching; what is cached here is the *decoded*
/// image, keyed by URL and target size.
#if canImport(UIKit)

import UIKit
import ImageIO

struct RemoteImage: View {
    let url: URL?
    /// Longest edge the image will be drawn at, in points. Converted to
    /// pixels with the screen scale before decoding.
    let maxPointSize: CGFloat

    @State private var image: UIImage?
    @State private var failed = false

    var body: some View {
        ZStack {
            if let image {
                Image(uiImage: image)
                    .resizable()
                    .scaledToFill()
            } else {
                Color.black.opacity(0.06)
                if failed {
                    Image(systemName: "photo")
                        .foregroundStyle(.secondary)
                }
            }
        }
        .task(id: taskID) {
            guard let url else { return }
            if let loaded = await ThumbnailLoader.shared.image(
                for: url, maxPixelSize: maxPointSize * UIScreen.main.scale
            ) {
                image = loaded
            } else {
                failed = true
            }
        }
    }

    /// Re-decode when the tile is reused at a materially different size —
    /// rotation and the iPhone/iPad split — but not on every layout nudge.
    private var taskID: String {
        "\(url?.absoluteString ?? "")|\(Int(maxPointSize / 40))"
    }
}

/// Decoded-image cache with in-flight de-duplication, so a tile scrolling in
/// and out of the lazy stack does not restart a decode it already finished.
actor ThumbnailLoader {
    static let shared = ThumbnailLoader()

    private let cache: NSCache<NSString, UIImage> = {
        let c = NSCache<NSString, UIImage>()
        // Roughly 60 tiles' worth of decoded pixels at wall size — the whole
        // wall stays warm, and nothing bigger than the wall is ever kept.
        c.totalCostLimit = 64 * 1024 * 1024
        return c
    }()
    private var inFlight: [String: Task<UIImage?, Never>] = [:]

    func image(for url: URL, maxPixelSize: CGFloat) async -> UIImage? {
        let key = "\(url.absoluteString)|\(Int(maxPixelSize))"
        if let hit = cache.object(forKey: key as NSString) { return hit }
        if let running = inFlight[key] { return await running.value }

        let task = Task<UIImage?, Never> {
            var request = URLRequest(url: url)
            request.cachePolicy = .returnCacheDataElseLoad
            guard let (data, _) = try? await URLSession.shared.data(for: request)
            else { return nil }
            return Self.downsample(data, maxPixelSize: maxPixelSize)
        }
        inFlight[key] = task
        let decoded = await task.value
        inFlight[key] = nil

        if let decoded {
            let cost = Int(decoded.size.width * decoded.size.height * 4)
            cache.setObject(decoded, forKey: key as NSString, cost: cost)
        }
        return decoded
    }

    private static func downsample(_ data: Data, maxPixelSize: CGFloat) -> UIImage? {
        guard let source = CGImageSourceCreateWithData(
            data as CFData, [kCGImageSourceShouldCache: false] as CFDictionary
        ) else { return nil }
        let options: [CFString: Any] = [
            kCGImageSourceCreateThumbnailFromImageAlways: true,
            kCGImageSourceCreateThumbnailWithTransform: true,   // honour EXIF orientation
            kCGImageSourceShouldCacheImmediately: true,          // decode off the main thread
            kCGImageSourceThumbnailMaxPixelSize: max(1, maxPixelSize),
        ]
        guard let cgImage = CGImageSourceCreateThumbnailAtIndex(
            source, 0, options as CFDictionary
        ) else { return nil }
        return UIImage(cgImage: cgImage)
    }
}

#else

/// Host-only fallback so `swift build` on macOS still type-checks the views.
struct RemoteImage: View {
    let url: URL?
    let maxPointSize: CGFloat

    var body: some View {
        AsyncImage(url: url) { image in
            image.resizable().scaledToFill()
        } placeholder: {
            Color.black.opacity(0.06)
        }
    }
}

#endif
