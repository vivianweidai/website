package com.vivianweidai.science.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.vivianweidai.science.core.ContentStore
import com.vivianweidai.science.core.grouping.ActivityGrouping
import com.vivianweidai.science.core.model.Activity

/** Unified chronological timeline of olympiads + textbooks, visually
 *  matching the webapp at /olympiads/. Groups by year (newest first). */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OlympiadsView(
    store: ContentStore,
    modifier: Modifier = Modifier,
) {
    val activities by store.activities.collectAsStateWithLifecycle()
    val error by store.activitiesError.collectAsStateWithLifecycle()
    var filter by rememberSaveable(
        stateSaver = androidx.compose.runtime.saveable.Saver<SubjectFilter, String>(
            save = { (it as? SubjectFilter.Named)?.name ?: "__all__" },
            restore = { s -> if (s == "__all__") SubjectFilter.All else SubjectFilter.Named(s) },
        )
    ) { mutableStateOf<SubjectFilter>(SubjectFilter.randomSubject()) }

    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("Olympiads") },
                actions = {
                    SubjectFilterMenu(
                        selected = filter,
                        onSelect = { filter = it },
                    )
                },
            )
        },
    ) { padding ->
        Box(Modifier.padding(padding)) {
            when {
                activities != null -> Timeline(
                    groups = yearGroups(activities!!, filter),
                )
                error != null -> ErrorState(error!!)
                else -> LoadingState(
                    title = "Loading olympiads",
                    subtitle = "Fetching the latest timeline from GitHub.",
                )
            }
        }
    }
}

private fun yearGroups(
    activities: List<Activity>,
    filter: SubjectFilter,
): List<ActivityGrouping.YearGroup> {
    val subjectName = (filter as? SubjectFilter.Named)?.name
    val filtered = ActivityGrouping.filtered(activities, subjectName)
    return ActivityGrouping.groupedByYear(filtered)
}

@Composable
private fun Timeline(
    groups: List<ActivityGrouping.YearGroup>,
) {
    LazyColumn(
        contentPadding = PaddingValues(bottom = 24.dp),
    ) {
        groups.forEach { group ->
            item(key = "year-${group.year}") {
                Text(
                    text = group.year,
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                        .padding(top = 16.dp, bottom = 4.dp),
                )
            }
            items(group.entries, key = { "act-${it.id}" }) { entry ->
                ActivityRow(entry)
                HorizontalDivider(modifier = Modifier.padding(start = 16.dp))
            }
        }
    }
}

@Composable
private fun ActivityRow(a: Activity) {
    val month = remember(a.date) {
        a.date.substringBefore(' ').take(3)
    }
    val chips = a.subjects?.takeIf { it.isNotEmpty() } ?: listOf(a.subject)
    // Canonical curriculum highlight yellow — #fff056, matching
    // --highlight-bg in archives/android/ui/src/main/assets/katex-shell.html
    // and content/research/curriculum.css. Keep these in sync.
    val highlighted = a.highlighted == 1
    val rowBg = if (highlighted)
        Color(red = 1.0f, green = 0.941f, blue = 0.337f)
    else Color.Transparent
    // Force dark ink on highlighted rows — in dark mode the default
    // body color is near-white, which is unreadable on the yellow wash.
    val nameColor = if (highlighted) Color.Black.copy(alpha = 0.82f)
                    else MaterialTheme.colorScheme.onSurface
    val monthColor = if (highlighted) Color.Black.copy(alpha = 0.55f)
                     else MaterialTheme.colorScheme.onSurfaceVariant

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(rowBg)
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            text = month,
            fontSize = 12.sp,
            fontFamily = FontFamily.Monospace,
            color = monthColor,
            modifier = Modifier.width(56.dp),
        )
        Box(Modifier.width(24.dp).padding(end = 4.dp), contentAlignment = Alignment.Center) {
            if (a.isOlympiad) OlympicRings() else Text("📖", fontSize = 13.sp)
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                chips.forEach { SubjectChip(it) }
            }
            Row(verticalAlignment = Alignment.Top) {
                Text(
                    text = a.name,
                    fontSize = 14.sp,
                    color = nameColor,
                    modifier = Modifier.weight(1f, fill = false),
                )
                if (a.invited == 1) Text(" ⭐", fontSize = 12.sp)
                if (a.competitive == 1) Text(" 🎯", fontSize = 12.sp)
            }
        }
    }
}

/** Simplified Olympic rings — 5 circles in two rows matching the webapp SVG. */
@Composable
private fun OlympicRings() {
    Canvas(modifier = Modifier.size(width = 22.dp, height = 12.dp)) {
        val r = size.minDimension * 0.29f
        val stroke = 1.2.dp.toPx()
        fun drawRing(color: Color, cx: Float, cy: Float) {
            drawCircle(color, radius = r, center = androidx.compose.ui.geometry.Offset(cx, cy),
                style = androidx.compose.ui.graphics.drawscope.Stroke(width = stroke))
        }
        val midY = size.height * 0.42f
        val lowY = size.height * 0.66f
        drawRing(Color(0.00f, 0.51f, 0.78f), size.width * 0.18f, midY) // blue
        drawRing(Color.Black,                 size.width * 0.50f, midY)
        drawRing(Color(0.93f, 0.20f, 0.31f), size.width * 0.82f, midY) // red
        drawRing(Color(0.99f, 0.69f, 0.19f), size.width * 0.34f, lowY) // yellow
        drawRing(Color(0.00f, 0.65f, 0.32f), size.width * 0.66f, lowY) // green
    }
}
