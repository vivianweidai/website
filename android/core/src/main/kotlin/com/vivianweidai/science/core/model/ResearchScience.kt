package com.vivianweidai.science.core.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import java.net.URLEncoder

/** Strongly-typed mirror of `public/research/technology.json`. One entry per
 *  science, each a flat list of techs (the old topic/category grouping tiers
 *  were dropped). */
@Serializable
data class ResearchScience(
    val id: Int,
    val science: String,
    @SerialName("science_slug") val scienceSlug: String,
    val techs: List<ResearchTech>,
)

@Serializable
data class ResearchTech(
    val id: Int,
    val tech: String,
    val specs: String? = null,
    val available: Int? = null,
    val url: String? = null,
    val hero: String? = null,
    @SerialName("tech_url") val techUrl: String? = null,
    val projects: List<ResearchTechProject>? = null,
) {
    val isAvailable: Boolean get() = (available ?: 0) == 1

    /** Absolute URL for the tech's hero image. Resolves repo-relative
     *  paths (the common case) against the site origin. */
    val heroUrl: String?
        get() {
            val h = hero ?: return null
            if (h.startsWith("http://") || h.startsWith("https://")) return h
            val trimmed = if (h.startsWith("/")) h.drop(1) else h
            return "https://vivianweidai.com/$trimmed"
        }

    /** External URL to open (Wolfram, GitHub, Colab) — or resolved to a raw
     *  GitHub URL when `url` is a repo-relative path like a photo link. */
    val externalUrl: String?
        get() {
            val raw = url ?: return null
            if (raw.startsWith("http://") || raw.startsWith("https://")) return raw
            val trimmed = if (raw.startsWith("/")) raw.drop(1) else raw
            val encoded = trimmed.split("/").joinToString("/") {
                URLEncoder.encode(it, "UTF-8").replace("+", "%20")
            }
            return "https://vivianweidai.com/$encoded"
        }
}

@Serializable
data class ResearchTechResponse(val sciences: List<ResearchScience>)

/** Per-tech project entry baked into technology.json by build_technology.py —
 *  reverse-scanned from research projects whose frontmatter `tech:` array
 *  references this tech. Lets iOS/Android render the tech detail view
 *  without re-scanning every project at runtime. */
@Serializable
data class ResearchTechProject(
    val date: String,                 // YYYY-MM-DD
    val title: String,
    val url: String,
    val sciences: List<String> = emptyList(),
) {
    /** URL of the project's `index.md` for in-app rendering. */
    val indexUrl: String
        get() {
            val trimmed = if (url.startsWith("/")) url.drop(1) else url
            val withIndex = if (trimmed.endsWith("/")) trimmed + "index.md" else "$trimmed/index.md"
            return "https://vivianweidai.com/$withIndex"
        }
}
