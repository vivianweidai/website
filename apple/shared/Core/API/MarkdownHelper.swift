import Foundation

/// Markdown processing utilities for transforming GitHub-hosted project
/// pages into content suitable for the iOS WKWebView renderer.
public enum MarkdownHelper {

    // MARK: - Cached regex patterns

    private static let mdImageRegex = try! NSRegularExpression(pattern: #"(\!\[[^\]]*\]\()(?!https?://)([^\)]+)(\))"#)
    private static let htmlImgRegex = try! NSRegularExpression(pattern: #"(<img\s[^>]*src=")(?!https?://)([^"]+)(")"#)
    /// Markdown hyperlinks `[text](path)` with a relative target — the
    /// `(?<!!)` negative lookbehind excludes image syntax `![...](...)`
    /// which is handled by `mdImageRegex`. Used so links to extension
    /// photos, local notebooks, etc. resolve against the project's
    /// GitHub raw base.
    private static let mdLinkRegex = try! NSRegularExpression(pattern: #"(?<!!)(\[[^\]]*\]\()(?!https?://|mailto:|#)([^\)]+)(\))"#)
    private static let htmlHrefRegex = try! NSRegularExpression(pattern: #"(<a\s[^>]*href=")(?!https?://|mailto:|#)([^"]+)(")"#)
    // MARK: - Front matter

    /// Strip YAML front matter (--- ... ---) from the top of markdown.
    public static func stripFrontMatter(_ md: String) -> String {
        let trimmed = md.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.hasPrefix("---") else { return md }
        let afterFirst = trimmed.dropFirst(3)
        guard let endRange = afterFirst.range(of: "\n---") else { return md }
        let afterFrontMatter = afterFirst[endRange.upperBound...]
        return String(afterFrontMatter).trimmingCharacters(in: .newlines)
    }

    /// Extract photo paths from a specific YAML front-matter key.
    /// Defaults to `"photos"` so existing call sites keep working; pass
    /// `"data_photos"` to get the data-sheet grid entries instead.
    ///
    /// Projects like `20250225 Catfood` declare BOTH keys — `photos`
    /// for the top experiment-photo grid and `data_photos` for a
    /// separate data-sheet grid with `<img id="data-0">` slots. They
    /// need to be extracted independently so each grid gets its own
    /// list of sources.
    public static func extractPhotos(from md: String, key: String = "photos") -> [String] {
        let trimmed = md.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.hasPrefix("---") else { return [] }
        let afterFirst = trimmed.dropFirst(3)
        guard let endRange = afterFirst.range(of: "\n---") else { return [] }
        let frontMatter = String(afterFirst[..<endRange.lowerBound])
        var photos: [String] = []
        var capturing = false
        for line in frontMatter.components(separatedBy: "\n") {
            let t = line.trimmingCharacters(in: .whitespaces)
            if t.hasPrefix("\(key):") {
                capturing = true
                continue
            }
            if capturing {
                if t.hasPrefix("- ") {
                    photos.append(String(t.dropFirst(2)))
                } else if !t.isEmpty {
                    // A new top-level key ended this list.
                    capturing = false
                }
            }
        }
        return photos
    }

    /// Extract a single-line scalar YAML value (e.g. `title: "X"` or
    /// `project: Y`). Returns the value with surrounding quotes stripped,
    /// or nil if the key is missing.
    public static func extractScalar(from md: String, key: String) -> String? {
        let trimmed = md.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmed.hasPrefix("---") else { return nil }
        let afterFirst = trimmed.dropFirst(3)
        guard let endRange = afterFirst.range(of: "\n---") else { return nil }
        let frontMatter = String(afterFirst[..<endRange.lowerBound])
        for line in frontMatter.components(separatedBy: "\n") {
            let t = line.trimmingCharacters(in: .whitespaces)
            if t.hasPrefix("\(key):") {
                var value = String(t.dropFirst(key.count + 1)).trimmingCharacters(in: .whitespaces)
                if value.hasPrefix("\"") && value.hasSuffix("\"") && value.count >= 2 {
                    value = String(value.dropFirst().dropLast())
                }
                return value.isEmpty ? nil : value
            }
        }
        return nil
    }

    /// Synthesise the title HTML block to prepend to a project or tech
    /// page so in-app rendering matches the website headings. Looks for:
    ///   - **Project pages** — `title:` (scalar) + `sciences:` (array).
    ///   - **Tech pages** — `tech:` (scalar) + `science:` (scalar).
    /// Returns an empty string when no usable title field is present.
    /// Call against raw front-matter-bearing markdown *before*
    /// `stripFrontMatter`, then prepend the result to the stripped body.
    ///
    /// `techPills` mirrors the webapp project page (Project.astro): one
    /// science-colored pill per tech the project used, resolved by the
    /// caller against technology.json (the parent science gives the chip
    /// color). When empty, falls back to plain science-name pills from the
    /// `sciences:`/`science:` front matter — the same fallback the webapp
    /// uses for a project that declares no techs.
    public static func synthesizeProjectTitle(
        from md: String,
        techPills: [(label: String, slug: String)] = []
    ) -> String {
        let title = extractScalar(from: md, key: "title")
            ?? extractScalar(from: md, key: "tech")
        guard let title else { return "" }
        let slugs: [String: String] = [
            "Mathematics": "math", "Computing": "comp", "Physics": "phys",
            "Chemistry": "chem", "Biology": "bio", "Astronomy": "astro",
        ]
        let pills: [(label: String, slug: String)]
        if !techPills.isEmpty {
            pills = techPills
        } else {
            var sciences = extractPhotos(from: md, key: "sciences")
            if sciences.isEmpty, let single = extractScalar(from: md, key: "science") {
                sciences = [single]
            }
            pills = sciences.compactMap { s in
                guard let slug = slugs[s] else { return nil }
                return (label: s, slug: slug)
            }
        }
        let chips = pills.map { "<span class=\"chip \($0.slug)\">\($0.label)</span>" }.joined()
        let chipBlock = chips.isEmpty ? "" : "<span class=\"project-chips\">\(chips)</span>"
        return "<div class=\"project-title\"><h1>\(title)</h1>\(chipBlock)</div>\n\n"
    }

    /// Remove the `## Technology` heading and its inline
    /// `<ul class="updates-list">…</ul>` block from a project's markdown
    /// body. Native UI renders the technology table from the project's
    /// `tech:` front-matter array + ContentStore lookup, so the inline
    /// list would otherwise show up twice (and with broken Safari links).
    /// Idempotent: returns the input unchanged when the section is
    /// missing.
    public static func stripTechnologySection(_ md: String) -> String {
        // Legacy markdown form: ## Technology ... </ul>
        if let h = md.range(of: "## Technology") {
            let tail = md[h.lowerBound...]
            if let end = tail.range(of: "</ul>") {
                return String(md[..<h.lowerBound]) + String(tail[end.upperBound...])
            }
        }
        // Current HTML div form: <div id="technology" class="tech-table-wrap"> ... </div></div>
        if let divStart = md.range(of: "<div id=\"technology\"") {
            let afterStart = md[divStart.lowerBound...]
            if let ulEnd = afterStart.range(of: "</ul>") {
                let afterUl = afterStart[ulEnd.upperBound...]
                if let firstClose = afterUl.range(of: "</div>") {
                    let afterFirst = afterUl[firstClose.upperBound...]
                    if let secondClose = afterFirst.range(of: "</div>") {
                        return String(md[..<divStart.lowerBound]) + String(afterFirst[secondClose.upperBound...])
                    }
                }
            }
        }
        return md
    }

    // MARK: - Photo injection

    /// Replace empty `<img id="photo-N">` tags in the experiment-photo
    /// grid with actual src from the `photos:` front-matter array.
    public static func injectPhotos(_ md: String, photos: [String]) -> String {
        injectImageSources(
            md, photos: photos,
            idPrefix: "photo-", altText: "Experiment photo"
        )
    }

    /// Replace empty `<img id="data-N">` tags in the data-sheet grid
    /// with actual src from a `data_photos:` front-matter array.
    /// Currently no project ships this pattern (catfood was the last
    /// holdout, migrated 2026-04-25), so this is a noop today; kept
    /// as the obvious symmetric helper to `injectPhotos` for any
    /// future project that wants a separate data-sheet grid.
    public static func injectDataPhotos(_ md: String, photos: [String]) -> String {
        injectImageSources(
            md, photos: photos,
            idPrefix: "data-", altText: "Data sheet"
        )
    }

    private static func injectImageSources(
        _ md: String,
        photos: [String],
        idPrefix: String,
        altText: String
    ) -> String {
        guard !photos.isEmpty else { return md }
        var result = md
        for (i, photo) in photos.enumerated() {
            let pattern = "<img id=\"\(idPrefix)\(i)\" alt=\"\(altText)\">"
            let replacement = "<img id=\"\(idPrefix)\(i)\" src=\"\(photo)\" alt=\"\(altText)\">"
            result = result.replacingOccurrences(of: pattern, with: replacement)
        }
        return result
    }

    // MARK: - URL resolution

    /// Rewrite relative image/link paths to absolute GitHub raw URLs.
    ///
    /// `baseURL` must be the raw.githubusercontent.com URL of the folder
    /// that contains the markdown file (i.e. `indexURL.deletingLastPathComponent()`).
    /// Callers pass this through rather than hardcoding the repo layout so
    /// that reorganizations like `research/` → `research/projects/` do not
    /// silently break photo resolution here.
    public static func resolveRelativeURLs(in markdown: String, baseURL: URL) -> String {
        // AbsoluteString on a URL produced by deletingLastPathComponent is
        // already percent-encoded, and we guarantee it ends with a slash so
        // simple concatenation with an encoded relative path yields a valid
        // absolute URL.
        var base = baseURL.absoluteString
        if !base.hasSuffix("/") { base += "/" }

        var result = markdown

        // Markdown images: ![alt](relative)
        result = replaceRelativePaths(in: result, regex: mdImageRegex, base: base, group: 2)

        // HTML images: <img src="relative">
        result = replaceRelativePaths(in: result, regex: htmlImgRegex, base: base, group: 2)

        // Markdown hyperlinks: [text](relative) — exclude images via
        // the negative lookbehind in the regex.
        result = replaceRelativePaths(in: result, regex: mdLinkRegex, base: base, group: 2)

        // HTML anchors: <a href="relative">
        result = replaceRelativePaths(in: result, regex: htmlHrefRegex, base: base, group: 2)

        return result
    }

    private static func replaceRelativePaths(in text: String, regex: NSRegularExpression, base: String, group: Int) -> String {
        var result = text
        let ns = result as NSString
        let matches = regex.matches(in: result, range: NSRange(location: 0, length: ns.length))
        for match in matches.reversed() {
            let path = ns.substring(with: match.range(at: group))
            let encodedPath = path.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? path
            var full = ""
            for i in 1...match.numberOfRanges - 1 {
                if i == group {
                    full += base + encodedPath
                } else {
                    full += ns.substring(with: match.range(at: i))
                }
            }
            result = (result as NSString).replacingCharacters(in: match.range, with: full)
        }
        return result
    }
}
