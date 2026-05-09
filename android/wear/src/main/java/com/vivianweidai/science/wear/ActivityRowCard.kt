package com.vivianweidai.science.wear

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Book
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.wear.compose.foundation.CurvedTextStyle
import androidx.wear.compose.material.Card
import androidx.wear.compose.material.CardDefaults
import androidx.wear.compose.material.Icon
import androidx.wear.compose.material.MaterialTheme
import androidx.wear.compose.material.Text
import com.vivianweidai.science.core.model.Activity

/** One row in the wear olympiads list. Tuned for the narrow watch
 *  canvas — two-line layout, tight spacing, single subject chip (the
 *  phone row may show multiple). Highlight behavior matches the phone
 *  ActivityRow (yellow wash for highlighted == 1). */
@Composable
fun ActivityRowCard(activity: Activity, onClick: () -> Unit) {
    val month = activity.date.substringBefore(' ').take(3).uppercase()
    val primarySubject = activity.subjects?.firstOrNull() ?: activity.subject

    val highlight = activity.highlighted == 1
    // Canonical curriculum highlight yellow — #fff056. Wear rows keep a
    // light alpha wash so the dense row text stays legible on the small
    // screen. Base color matches the phone + iOS curriculum highlight.
    val bg = if (highlight)
        Color(1.0f, 0.941f, 0.337f).copy(alpha = 0.22f)
    else
        Color.Transparent

    Card(
        onClick = onClick,
        backgroundPainter = CardDefaults.cardBackgroundPainter(),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(bg, shape = RoundedCornerShape(8.dp))
                .padding(horizontal = 4.dp, vertical = 2.dp),
            verticalAlignment = Alignment.Top,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            TypeGlyph(activity.isOlympiad)
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                ) {
                    Text(
                        text = month,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Medium,
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colors.onSurfaceVariant,
                    )
                    SubjectPill(primarySubject)
                    if (activity.invited == 1) {
                        Text(
                            "★",
                            fontSize = 9.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(1.0f, 0.75f, 0.0f),
                        )
                    }
                }
                Text(
                    text = activity.name,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 3,
                )
            }
        }
    }
}

@Composable
private fun SubjectPill(subject: String) {
    Text(
        text = subject,
        fontSize = 9.sp,
        fontWeight = FontWeight.SemiBold,
        color = Color.Black.copy(alpha = 0.82f),
        modifier = Modifier
            .clip(RoundedCornerShape(50))
            .background(SubjectColor.color(subject))
            .padding(horizontal = 5.dp, vertical = 1.dp),
    )
}

@Composable
private fun TypeGlyph(isOlympiad: Boolean) {
    Icon(
        imageVector = if (isOlympiad) Icons.Filled.EmojiEvents else Icons.Filled.Book,
        contentDescription = null,
        tint = if (isOlympiad) Color(0.99f, 0.69f, 0.19f) // olympic yellow
               else MaterialTheme.colors.onSurfaceVariant,
        modifier = Modifier.size(14.dp).padding(top = 2.dp),
    )
}
