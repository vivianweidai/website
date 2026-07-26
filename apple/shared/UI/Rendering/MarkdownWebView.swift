import SwiftUI

/// Renders a markdown string with KaTeX math via a WKWebView hosting the
/// katex-shell.html bundled with the package.
///
/// Optional `tableName` + `highlightedRows` enable curriculum-specific
/// table rendering: the JS shell will prepend a full-width header row
/// with the table name, remove the original column-header row, merge
/// identical first-column cells into rowspans, and apply `.highlight` to
/// data rows by index.
///
/// The view sizes itself to the rendered content via a WKScriptMessage
/// channel (`contentHeight`) — katex-shell.html posts
/// `document.body.scrollHeight` after each render and SwiftUI frames the
/// outer view to that height. Internal WebKit scrolling is disabled so
/// multiple tables on one screen flow naturally inside an outer
/// ScrollView without competing scroll gestures.
///
/// On hosts missing UIKit or WebKit (macOS host-only `swift build`
/// type-checking; watchOS, which has UIKit but not WebKit) this falls
/// back to a plain SwiftUI stub so call sites can embed it from
/// shared code. The real rendering path is iOS/iPadOS only.
///
/// Both conditions have to hold: watchOS has UIKit but no WebKit, so
/// `canImport(UIKit)` alone leaks to watchOS and breaks the
/// `import WebKit` line. macOS has WebKit but no UIKit, so
/// `canImport(WebKit)` alone breaks the `import UIKit` line. The
/// intersection is iOS/iPadOS/tvOS, which is exactly what we want.
#if canImport(UIKit) && canImport(WebKit)

import UIKit
import WebKit

public struct MarkdownWebView: View {
    let markdown: String
    let tableName: String?
    let highlightedRows: [Int]
    let onImageTap: (([URL], Int) -> Void)?

    @State private var contentHeight: CGFloat = 80

    /// `onImageTap` receives every image on the page in document order plus
    /// the index of the tapped one, so the host can present a pageable
    /// zoomable viewer. When nil, image taps fall back to the plain link
    /// behaviour (Safari).
    public init(
        markdown: String,
        tableName: String? = nil,
        highlightedRows: [Int] = [],
        onImageTap: (([URL], Int) -> Void)? = nil
    ) {
        self.markdown = markdown
        self.tableName = tableName
        self.highlightedRows = highlightedRows
        self.onImageTap = onImageTap
    }

    public var body: some View {
        MarkdownWebViewRep(
            markdown: markdown,
            tableName: tableName,
            highlightedRows: highlightedRows,
            onImageTap: onImageTap,
            contentHeight: $contentHeight
        )
        .frame(height: contentHeight)
    }
}

private struct MarkdownWebViewRep: UIViewRepresentable {
    let markdown: String
    let tableName: String?
    let highlightedRows: [Int]
    let onImageTap: (([URL], Int) -> Void)?
    @Binding var contentHeight: CGFloat

    struct RenderOptions {
        let markdown: String
        let tableName: String?
        let highlightedRows: [Int]
    }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        // JS → Swift bridge: katex-shell.html posts scrollHeight here
        // after each render so we can size the outer SwiftUI frame.
        config.userContentController.add(context.coordinator, name: "contentHeight")
        // …and the tapped image (plus the page's full image list) here,
        // so taps open the native viewer instead of Safari.
        config.userContentController.add(context.coordinator, name: "imageTap")
        // Gallery pages lead with an autoplaying muted clip. Without both
        // of these iOS refuses to start it and takes the hero band over
        // full screen on play — the Stargazing hero rendered as a blank
        // band because of it.
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        let view = WKWebView(frame: .zero, configuration: config)
        view.isOpaque = false
        view.backgroundColor = .clear
        view.scrollView.backgroundColor = .clear
        // Disable internal scrolling — the SwiftUI parent ScrollView owns
        // the scroll gesture, and the webview sizes itself to the
        // contentHeight binding so nothing is clipped.
        view.scrollView.isScrollEnabled = false
        view.scrollView.bounces = false

        if let url = Bundle.module.url(forResource: "katex-shell", withExtension: "html") {
            view.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
        context.coordinator.webView = view
        context.coordinator.pendingOptions = RenderOptions(
            markdown: markdown,
            tableName: tableName,
            highlightedRows: highlightedRows
        )
        view.navigationDelegate = context.coordinator
        return view
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        context.coordinator.onImageTap = onImageTap
        context.coordinator.render(
            RenderOptions(
                markdown: markdown,
                tableName: tableName,
                highlightedRows: highlightedRows
            )
        )
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(contentHeight: $contentHeight, onImageTap: onImageTap)
    }

    final class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
        weak var webView: WKWebView?
        var pendingOptions: RenderOptions?
        var loaded = false
        var contentHeight: Binding<CGFloat>
        var onImageTap: (([URL], Int) -> Void)?

        init(contentHeight: Binding<CGFloat>, onImageTap: (([URL], Int) -> Void)?) {
            self.contentHeight = contentHeight
            self.onImageTap = onImageTap
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            loaded = true
            if let pending = pendingOptions {
                render(pending)
            }
        }

        /// Intercept link clicks inside rendered markdown. Without this,
        /// tapping any `<a href>` inside the shell causes WKWebView to
        /// navigate in place — replacing our katex-shell with the link
        /// target and breaking the page. Redirect link activations to
        /// Safari (images, notebooks, repo URLs alike) while letting
        /// the initial katex-shell.html load through as a same-document
        /// navigation.
        func webView(
            _ webView: WKWebView,
            decidePolicyFor navigationAction: WKNavigationAction,
            decisionHandler: @escaping (WKNavigationActionPolicy) -> Void
        ) {
            if navigationAction.navigationType == .linkActivated,
               let url = navigationAction.request.url {
                // Belt-and-braces for image links: the shell's tap bridge
                // already preventDefaults these, but if it ever misses one
                // the viewer is still the right destination, not Safari.
                let ext = url.pathExtension.lowercased()
                if let onImageTap,
                   ["jpg", "jpeg", "png", "gif", "webp", "avif"].contains(ext) {
                    onImageTap([url], 0)
                } else {
                    UIApplication.shared.open(url)
                }
                decisionHandler(.cancel)
                return
            }
            decisionHandler(.allow)
        }

        /// Called by katex-shell.html via
        /// `window.webkit.messageHandlers.contentHeight.postMessage(...)`
        /// at the end of every render. Pushes the new height into the
        /// SwiftUI @State binding so the view frame updates.
        func userContentController(
            _ userContentController: WKUserContentController,
            didReceive message: WKScriptMessage
        ) {
            switch message.name {
            case "contentHeight":
                if let number = message.body as? NSNumber {
                    let height = CGFloat(truncating: number)
                    if height > 0 {
                        DispatchQueue.main.async {
                            self.contentHeight.wrappedValue = height
                        }
                    }
                }
            case "imageTap":
                guard let onImageTap,
                      let body = message.body as? [String: Any],
                      let strings = body["sources"] as? [String] else { return }
                let urls = strings.compactMap(URL.init(string:))
                let index = min(max(body["index"] as? Int ?? 0, 0), max(urls.count - 1, 0))
                guard !urls.isEmpty else { return }
                DispatchQueue.main.async { onImageTap(urls, index) }
            default:
                return
            }
        }

        func render(_ options: RenderOptions) {
            guard let view = webView else { return }
            guard loaded else { pendingOptions = options; return }

            var payload: [String: Any] = [
                "markdown": options.markdown,
                "highlightedRows": options.highlightedRows
            ]
            if let tableName = options.tableName {
                payload["tableName"] = tableName
            }

            guard let data = try? JSONSerialization.data(withJSONObject: payload, options: [.fragmentsAllowed]),
                  let json = String(data: data, encoding: .utf8) else {
                return
            }
            view.evaluateJavaScript("window.renderMarkdown(\(json));", completionHandler: nil)
        }
    }
}

#else

/// Host-only stub so `swift build` on macOS type-checks. Never runs in
/// practice — the app is iOS-only.
public struct MarkdownWebView: View {
    let markdown: String
    let tableName: String?
    let highlightedRows: [Int]
    let onImageTap: (([URL], Int) -> Void)?

    public init(
        markdown: String,
        tableName: String? = nil,
        highlightedRows: [Int] = [],
        onImageTap: (([URL], Int) -> Void)? = nil
    ) {
        self.markdown = markdown
        self.tableName = tableName
        self.highlightedRows = highlightedRows
        self.onImageTap = onImageTap
    }

    public var body: some View {
        Text("Preview unavailable on this platform")
            .foregroundStyle(.secondary)
            .padding()
    }
}

#endif
