package com.vivianweidai.science.ui

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.Saver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.vivianweidai.science.core.ContentStore
import com.vivianweidai.science.core.api.Http
import com.vivianweidai.science.core.api.MarkdownHelper
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import com.vivianweidai.science.core.model.ResearchCategory
import com.vivianweidai.science.core.model.ResearchTopic
import com.vivianweidai.science.core.model.ResearchTech
import com.vivianweidai.science.core.model.ResearchTechProject
import java.net.URLEncoder

/** Tech browser mirroring the webapp at /research/. Topics grouped into
 *  cards with subject chip; each card nests categories + their techs. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResearchView(store: ContentStore, modifier: Modifier = Modifier) {
    val topics by store.topics.collectAsStateWithLifecycle()
    val error by store.topicsError.collectAsStateWithLifecycle()
    val nav = rememberNavController()

    var filter by rememberSaveable(
        stateSaver = Saver<SubjectFilter, String>(
            save = { (it as? SubjectFilter.Named)?.name ?: "__all__" },
            restore = { if (it == "__all__") SubjectFilter.All else SubjectFilter.Named(it) },
        )
    ) { mutableStateOf<SubjectFilter>(SubjectFilter.randomResearchSubject()) }

    NavHost(navController = nav, startDestination = "list", modifier = modifier) {
        composable("list") {
            Scaffold(
                topBar = {
                    TopAppBar(
                        title = { Text("Research") },
                        actions = {
                            SubjectFilterMenu(
                                selected = filter,
                                onSelect = { filter = it },
                            )
                        },
                    )
                },
            ) { p ->
                Box(Modifier.padding(p)) {
                    when {
                        topics != null -> TopicList(
                            topics = topics!!.filterBy(filter),
                            onTech = { name ->
                                // URLEncoder uses '+' for spaces, but NavHost path
                                // args decode with %20 semantics — so swap '+'
                                // back to %20 to keep "Liquid Chromatography" intact
                                // through the route round-trip.
                                val encoded = URLEncoder.encode(name, "UTF-8")
                                    .replace("+", "%20")
                                nav.navigate("tech/$encoded")
                            },
                        )
                        error != null -> ErrorState(error!!)
                        else -> LoadingState(
                            "Loading tech",
                            "Fetching research topics from GitHub.",
                        )
                    }
                }
            }
        }
        // NavHost already URL-decodes path arguments once, so do NOT call
        // Uri.decode here. Double-decoding was turning `%20` (the real
        // percent-encoding of a space in the GitHub raw URL) back into a
        // literal space, which broke every downstream image fetch AND
        // kept marked.js from parsing `[text](url with space)` as a
        // link on research project pages (Extension tables rendered
        // their URLs as raw text instead of links).
        composable("tech/{name}") { back ->
            val name = back.arguments?.getString("name") ?: ""
            TechDetailScreen(
                store = store,
                techName = name,
                onBack = { nav.popBackStack() },
                onProject = { title, url ->
                    val encoded = URLEncoder.encode(url, "UTF-8")
                    nav.navigate("project/${URLEncoder.encode(title, "UTF-8")}/$encoded")
                },
            )
        }
        composable("project/{title}/{url}") { back ->
            val title = back.arguments?.getString("title") ?: ""
            val url = back.arguments?.getString("url") ?: ""
            ProjectDetailScreen(
                store = store,
                title = title,
                indexUrl = url,
                onBack = { nav.popBackStack() },
                onTech = { name ->
                    val encoded = URLEncoder.encode(name, "UTF-8").replace("+", "%20")
                    nav.navigate("tech/$encoded")
                },
            )
        }
    }
}

private fun List<ResearchTopic>.filterBy(filter: SubjectFilter): List<ResearchTopic> =
    when (filter) {
        SubjectFilter.All -> this
        is SubjectFilter.Named -> filter { it.science == filter.name }
    }

@Composable
private fun TopicList(
    topics: List<ResearchTopic>,
    onTech: (String) -> Unit,
) {
    LazyColumn(
        contentPadding = androidx.compose.foundation.layout.PaddingValues(vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        if (topics.isEmpty()) {
            item {
                Text(
                    text = "No tech yet.",
                    fontSize = 14.sp,
                    fontStyle = FontStyle.Italic,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(horizontal = 16.dp),
                )
            }
        }
        items(topics, key = { it.id }) { topic ->
            TopicCard(topic, onTech)
        }
    }
}

@Composable
private fun TopicCard(
    topic: ResearchTopic,
    onTech: (String) -> Unit,
) {
    Surface(
        shape = RoundedCornerShape(10.dp),
        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
        border = BorderStroke(1.dp, SubjectPalette.color(topic.science).copy(alpha = 0.7f)),
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp),
    ) {
        Row {
            // Left accent bar, mirrors webapp .tech-accent-* border.
            Box(
                modifier = Modifier
                    .width(4.dp)
                    .fillMaxSize()
                    .background(SubjectPalette.color(topic.science))
            )
            Column(Modifier.weight(1f)) {
                // Header — the science name (topic == science now). No chip:
                // the title already names the science, and the accent bar +
                // border carry its color. Matches iOS's ScienceCard header.
                Text(
                    topic.science,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = 14.dp, end = 12.dp, top = 10.dp, bottom = 10.dp),
                )
                HorizontalDivider()
                topic.categories.forEach { category ->
                    TechnologyBlock(category, onTech)
                }
            }
        }
    }
}

@Composable
private fun TechnologyBlock(
    category: ResearchCategory,
    onTech: (String) -> Unit,
) {
    Column {
        // Header shows only for named categories. Flat sciences ship one
        // empty-named category (see build_technology.py), so they render as a
        // plain tech list; Biology keeps its named groups.
        if (category.category.isNotEmpty()) {
            Text(
                text = category.category,
                fontSize = 13.sp,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.surfaceContainer)
                    .padding(start = 14.dp, end = 12.dp, top = 6.dp, bottom = 6.dp),
            )
        }
        category.techs.forEachIndexed { i, tech ->
            TechRow(tech, onTech)
            if (i != category.techs.lastIndex) {
                HorizontalDivider(modifier = Modifier.padding(start = 28.dp))
            }
        }
    }
}

@Composable
private fun TechRow(
    tech: ResearchTech,
    onTech: (String) -> Unit,
) {
    val context = LocalContext.current
    val externalUrl = tech.externalUrl
    val hasLink = tech.techUrl != null || externalUrl != null

    val onClick: (() -> Unit)? = when {
        tech.techUrl != null -> ({ onTech(tech.tech) })
        externalUrl != null -> ({
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(externalUrl)))
        })
        else -> null
    }

    val row = @Composable {
        Row(
            verticalAlignment = Alignment.Top,
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 28.dp, end = 12.dp, top = 8.dp, bottom = 8.dp),
        ) {
            Column(Modifier.weight(1f)) {
                Text(
                    text = tech.tech,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = if (hasLink) MaterialTheme.colorScheme.primary
                            else MaterialTheme.colorScheme.onSurface,
                )
                if (!tech.specs.isNullOrEmpty()) {
                    Text(
                        text = tech.specs!!,
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            if (tech.isAvailable) {
                Icon(
                    Icons.Filled.Check,
                    contentDescription = "Available",
                    tint = Color(0.10f, 0.50f, 0.22f),
                )
            }
        }
    }
    if (onClick != null) Surface(onClick = onClick, color = Color.Transparent) { row() }
    else row()
}

// ---------- Project detail ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ProjectDetailScreen(
    store: ContentStore,
    title: String,
    indexUrl: String,
    onBack: () -> Unit,
    onTech: (String) -> Unit,
) {
    var loaded by remember(indexUrl) { mutableStateOf<ProjectDetail?>(null) }
    LaunchedEffect(indexUrl) {
        loaded = runCatching { loadProjectMarkdown(indexUrl) }
            .getOrElse { e ->
                ProjectDetail(
                    markdown = "# Error\n\n${e.message ?: e::class.simpleName}",
                    techNames = emptyList(),
                )
            }
    }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(title) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
            )
        },
    ) { p ->
        Box(Modifier.padding(p).fillMaxSize()) {
            val detail = loaded
            if (detail == null) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    androidx.compose.material3.CircularProgressIndicator()
                }
            } else {
                androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxSize()) {
                    item {
                        MarkdownWebView(markdown = detail.markdown)
                    }
                    if (detail.techNames.isNotEmpty()) {
                        item {
                            ProjectTechnologySection(
                                store = store,
                                techNames = detail.techNames,
                                onTech = onTech,
                            )
                        }
                    }
                }
            }
        }
    }
}

// ---------- Tech detail ----------

/** Native tech page — renders title, science chip, topic·category
 *  context, hero image, spec description, and the projects list, all
 *  from `technology.json` data. Replaces the previous markdown-passthrough
 *  approach because most tech `index.md` bodies are empty by design. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun TechDetailScreen(
    store: ContentStore,
    techName: String,
    onBack: () -> Unit,
    onProject: (String, String) -> Unit,
) {
    val topics by store.topics.collectAsStateWithLifecycle()
    val resolved = remember(topics, techName) { store.findTech(techName) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(techName) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
            )
        },
    ) { p ->
        Box(Modifier.padding(p).fillMaxSize()) {
            if (resolved == null) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    if (topics == null) {
                        androidx.compose.material3.CircularProgressIndicator()
                    } else {
                        Text(
                            "Tech not found.",
                            fontStyle = FontStyle.Italic,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            } else {
                val (topic, category, tech) = resolved
                LazyColumn(
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(14.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp),
                ) {
                    tech.heroUrl?.let { url ->
                        item {
                            AsyncImage(
                                model = url,
                                contentDescription = tech.tech,
                                contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(200.dp)
                                    .clip(RoundedCornerShape(8.dp)),
                            )
                        }
                    }
                    item {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            Text(tech.tech, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                            SubjectChip(topic.science)
                        }
                    }
                    // Category context line — only for grouped sciences
                    // (Biology). Flat sciences carry an empty category name,
                    // and the science already shows as a chip by the title.
                    if (category.category.isNotEmpty()) {
                        item {
                            Text(
                                category.category,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                    if (!tech.specs.isNullOrEmpty()) {
                        item { Text("${tech.specs!!}.", fontSize = 14.sp) }
                    }
                    item { HorizontalDivider() }
                    item { Text("Projects", fontSize = 17.sp, fontWeight = FontWeight.Bold) }
                    val projects = tech.projects.orEmpty()
                    if (projects.isEmpty()) {
                        item {
                            Text(
                                "No projects yet.",
                                fontStyle = FontStyle.Italic,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    } else {
                        item {
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                                border = BorderStroke(1.dp, Color.Black.copy(alpha = 0.08f)),
                            ) {
                                Column {
                                    projects.forEachIndexed { i, p ->
                                        TechProjectRow(p, onProject)
                                        if (i != projects.lastIndex) HorizontalDivider()
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun TechProjectRow(
    project: ResearchTechProject,
    onProject: (String, String) -> Unit,
) {
    val onClick: () -> Unit = { onProject(project.title, project.indexUrl) }
    val row = @Composable {
        Row(
            verticalAlignment = Alignment.Top,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 12.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                formatProjectDate(project.date),
                fontSize = 12.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.width(110.dp),
            )
            Column(Modifier.weight(1f)) {
                Text(
                    project.title,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium,
                    color = MaterialTheme.colorScheme.primary,
                )
                if (project.sciences.isNotEmpty()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        project.sciences.forEach { SubjectChip(it) }
                    }
                }
            }
        }
    }
    Surface(onClick = onClick, color = Color.Transparent) { row() }
}

private fun formatProjectDate(iso: String): String {
    // "2026-04-27" → "April 27th 2026"
    val parts = iso.split("-")
    if (parts.size != 3) return iso
    val year = parts[0].toIntOrNull() ?: return iso
    val month = parts[1].toIntOrNull() ?: return iso
    val day = parts[2].toIntOrNull() ?: return iso
    if (month !in 1..12) return iso
    val months = listOf(
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    )
    val suffix = when {
        day % 100 in 11..13 -> "th"
        day % 10 == 1 -> "st"
        day % 10 == 2 -> "nd"
        day % 10 == 3 -> "rd"
        else -> "th"
    }
    return "${months[month - 1]} $day$suffix $year"
}

// ---------- Project Technology section ----------

/** Native rendering of the Tech section for a project page —
 *  replaces the inline `<ul class="updates-list">` HTML that was
 *  shipped in markdown bodies. The list of techs comes from the
 *  project's `tech:` front-matter array; each tech is resolved via
 *  ContentStore for parent topic/category + specs, and tapping a
 *  row navigates internally to TechDetailScreen. */
@Composable
private fun ProjectTechnologySection(
    store: ContentStore,
    techNames: List<String>,
    onTech: (String) -> Unit,
) {
    val topics by store.topics.collectAsStateWithLifecycle()
    val resolved = remember(topics, techNames) {
        val rank = mapOf(
            "Mathematics" to 0, "Computing" to 1, "Physics" to 2,
            "Chemistry" to 3, "Biology" to 4, "Astronomy" to 5,
        )
        techNames.mapNotNull { store.findTech(it) }
            .sortedWith(compareBy(
                { rank[it.first.science] ?: Int.MAX_VALUE },
                { it.third.id },
            ))
    }
    if (resolved.isEmpty()) return

    Column(
        modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text("Technology", fontSize = 17.sp, fontWeight = FontWeight.Bold)
        Surface(
            shape = RoundedCornerShape(8.dp),
            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
            border = BorderStroke(1.dp, Color.Black.copy(alpha = 0.08f)),
        ) {
            Column {
                resolved.forEachIndexed { i, (topic, category, tech) ->
                    Surface(
                        onClick = { onTech(tech.tech) },
                        color = Color.Transparent,
                    ) {
                        Row(
                            verticalAlignment = Alignment.Top,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 12.dp, vertical = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(10.dp),
                        ) {
                            Text(
                                category.category,
                                fontSize = 12.sp,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.width(110.dp),
                            )
                            Column(Modifier.weight(1f)) {
                                Text(
                                    tech.tech,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.SemiBold,
                                    color = MaterialTheme.colorScheme.primary,
                                )
                                if (!tech.specs.isNullOrEmpty()) {
                                    Text(
                                        tech.specs!!,
                                        fontSize = 12.sp,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    )
                                }
                            }
                            SubjectChip(topic.science)
                        }
                    }
                    if (i != resolved.lastIndex) HorizontalDivider()
                }
            }
        }
    }
}

private data class ProjectDetail(val markdown: String, val techNames: List<String>)

/** Fetch + transform an `index.md` into renderable markdown plus the
 *  project's `tech:` frontmatter array (the source for the native
 *  Technology table). Strips the inline `## Technology … </ul>` block
 *  from the body so it doesn't render twice. */
private suspend fun loadProjectMarkdown(indexUrl: String): ProjectDetail {
    var md = Http.getString(indexUrl)
    var photos = MarkdownHelper.extractPhotos(md, "photos")
    if (photos.isEmpty()) {
        photos = scanProjectPhotos(indexUrl).shuffled()
    }
    val dataPhotos = MarkdownHelper.extractPhotos(md, "data_photos")
    val techNames = MarkdownHelper.extractPhotos(md, "tech")
    val titleBlock = MarkdownHelper.synthesizeProjectTitle(md)
    md = MarkdownHelper.stripFrontMatter(md)
    md = titleBlock + md
    md = MarkdownHelper.stripTechnologySection(md)
    md = MarkdownHelper.injectPhotos(md, photos)
    md = MarkdownHelper.injectDataPhotos(md, dataPhotos)
    val base = indexUrl.substringBeforeLast('/')
    return ProjectDetail(
        markdown = MarkdownHelper.resolveRelativeUrls(md, base),
        techNames = techNames,
    )
}

@Serializable
private data class GitHubContentEntry(val name: String, val type: String)

private val githubJson = Json { ignoreUnknownKeys = true }

/** Fetch the union of image filenames under a project's
 *  `photos/setup/` and `photos/samples/` via the GitHub contents API.
 *  Returns relative paths (e.g. `photos/setup/setup1.jpeg`) so they
 *  resolve through MarkdownHelper.resolveRelativeUrls. Silent on
 *  failure — photos are decorative; a broken network must not crash
 *  the page.
 *
 *  `indexUrl` here is the deployed-site URL
 *  (`https://vivianweidai.com/research/projects/{folder}/index.md`),
 *  not a GitHub raw URL — we fetch markdown over the website. The repo
 *  + branch are hardcoded since this app only ever reads its own repo. */
private suspend fun scanProjectPhotos(indexUrl: String): List<String> {
    val parts = indexUrl.substringAfter("://").substringAfter('/').split('/')
    val idxPos = parts.indexOf("index.md").takeIf { it > 0 } ?: return emptyList()
    // indexUrl segments may already be percent-encoded (the per-tech
    // project entry's `url` in technology.json carries `%20` for spaces).
    // Decode the folder name to its raw form before re-encoding it for
    // the GitHub contents API — a double-encode would turn `%20` into
    // `%2520` and the API 404s.
    val folder = java.net.URLDecoder.decode(parts[idxPos - 1], "UTF-8")
    // public/ is the on-disk root mapped to the site root; that's
    // what the GitHub Contents API needs to see.
    val folderParts = listOf("public", "research", "projects", folder)

    val all = mutableListOf<String>()
    for (sub in listOf("photos/setup", "photos/samples")) {
        val apiPath = (folderParts + sub.split("/")).joinToString("/") {
            java.net.URLEncoder.encode(it, "UTF-8").replace("+", "%20")
        }
        val url = "https://api.github.com/repos/vivianweidai/science/contents/$apiPath?ref=main"
        runCatching {
            val body = Http.getString(url)
            val entries = githubJson.decodeFromString<List<GitHubContentEntry>>(body)
            entries.filter { it.type == "file" }.forEach { e ->
                val lower = e.name.lowercase()
                if (lower.endsWith(".jpg") || lower.endsWith(".jpeg") ||
                    lower.endsWith(".png")) {
                    all += "$sub/${e.name}"
                }
            }
        }
        // Failures (404 for projects without one of the subfolders,
        // network blip, rate-limit) are silently skipped.
    }
    return all
}

