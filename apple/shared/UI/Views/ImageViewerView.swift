import SwiftUI

/// Full-screen photo viewer for images tapped inside a rendered project
/// page. Gallery pages (Stargazing, Cellgazing) wrap every tile in an
/// `<a href="…jpg">` for a page lightbox whose JS can't run in the app's
/// markdown shell, so those taps used to leave the app for Safari; the
/// shell now posts them here instead (see `MarkdownWebView`'s imageTap
/// bridge).
///
/// Pinch-to-zoom and pan come from a real `UIScrollView` rather than a
/// SwiftUI `MagnificationGesture`, which is what makes the zoom feel like
/// Photos: momentum, rubber-banding and double-tap all come for free.
/// Swipe left/right pages through the rest of the page's images.
#if canImport(UIKit)

import UIKit

struct ImageViewerView: View {
    let sources: [URL]
    @State var index: Int
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack(alignment: .topTrailing) {
            Color.black.ignoresSafeArea()

            TabView(selection: $index) {
                ForEach(Array(sources.enumerated()), id: \.offset) { offset, url in
                    ZoomableImage(url: url)
                        .tag(offset)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: sources.count > 1 ? .automatic : .never))
            .ignoresSafeArea()

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
    }
}

/// One page of the viewer: the image inside a zooming scroll view.
private struct ZoomableImage: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> UIScrollView {
        let scroll = UIScrollView()
        scroll.delegate = context.coordinator
        scroll.backgroundColor = .black
        scroll.maximumZoomScale = 6
        scroll.minimumZoomScale = 1
        scroll.bouncesZoom = true
        scroll.showsHorizontalScrollIndicator = false
        scroll.showsVerticalScrollIndicator = false
        // The page TabView owns horizontal swipes until the image is
        // zoomed in; at zoom 1 the content exactly fills the view so the
        // scroll view has nothing to pan and lets the gesture through.
        scroll.contentInsetAdjustmentBehavior = .never

        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFit
        imageView.isUserInteractionEnabled = true
        scroll.addSubview(imageView)
        context.coordinator.imageView = imageView
        context.coordinator.scrollView = scroll

        let doubleTap = UITapGestureRecognizer(
            target: context.coordinator,
            action: #selector(Coordinator.handleDoubleTap(_:))
        )
        doubleTap.numberOfTapsRequired = 2
        scroll.addGestureRecognizer(doubleTap)

        context.coordinator.load(url)
        return scroll
    }

    func updateUIView(_ uiView: UIScrollView, context: Context) {
        context.coordinator.layout()
    }

    func makeCoordinator() -> Coordinator { Coordinator() }

    final class Coordinator: NSObject, UIScrollViewDelegate {
        weak var scrollView: UIScrollView?
        var imageView: UIImageView?
        private var task: URLSessionDataTask?

        func load(_ url: URL) {
            task?.cancel()
            task = URLSession.shared.dataTask(with: url) { [weak self] data, _, _ in
                guard let data, let image = UIImage(data: data) else { return }
                DispatchQueue.main.async {
                    self?.imageView?.image = image
                    self?.layout()
                }
            }
            task?.resume()
        }

        /// Size the image view to the scroll view and re-centre it. Called
        /// on load and on every SwiftUI layout pass (rotation included).
        func layout() {
            guard let scroll = scrollView, let imageView else { return }
            let bounds = scroll.bounds
            guard bounds.width > 0, bounds.height > 0 else { return }
            if scroll.zoomScale == 1 {
                imageView.frame = CGRect(origin: .zero, size: bounds.size)
                scroll.contentSize = bounds.size
            }
        }

        func viewForZooming(in scrollView: UIScrollView) -> UIView? { imageView }

        /// Keep the image centred while it's smaller than the viewport —
        /// without this a zoomed-out image sticks to the top-left corner.
        func scrollViewDidZoom(_ scrollView: UIScrollView) {
            guard let imageView else { return }
            let bounds = scrollView.bounds.size
            var frame = imageView.frame
            frame.origin.x = frame.width < bounds.width
                ? (bounds.width - frame.width) / 2 : 0
            frame.origin.y = frame.height < bounds.height
                ? (bounds.height - frame.height) / 2 : 0
            imageView.frame = frame
        }

        @objc func handleDoubleTap(_ gesture: UITapGestureRecognizer) {
            guard let scroll = scrollView else { return }
            if scroll.zoomScale > scroll.minimumZoomScale {
                scroll.setZoomScale(scroll.minimumZoomScale, animated: true)
            } else {
                // Zoom to a rect centred on the tap, a third of the view
                // wide — the usual "one double-tap gets you close" feel.
                let point = gesture.location(in: scroll)
                let scale: CGFloat = 3
                let size = CGSize(
                    width: scroll.bounds.width / scale,
                    height: scroll.bounds.height / scale
                )
                let origin = CGPoint(
                    x: point.x - size.width / 2,
                    y: point.y - size.height / 2
                )
                scroll.zoom(to: CGRect(origin: origin, size: size), animated: true)
            }
        }
    }
}

#endif
