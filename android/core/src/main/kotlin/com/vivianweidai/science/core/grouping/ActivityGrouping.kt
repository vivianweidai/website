package com.vivianweidai.science.core.grouping

import com.vivianweidai.science.core.model.Activity

/**
 * Pure-data helpers for filtering and grouping the unified olympiad +
 * textbook list. No Android deps so a future Wear module can share the
 * exact same semantics as the phone app.
 */
object ActivityGrouping {

    /** Filter by a single subject. `null`/empty returns everything.
     *  If the activity has a `subjects` array, match if it contains the
     *  subject; otherwise fall back to the scalar `subject` field.
     *  Result is sorted newest-first by `sortKey`. */
    fun filtered(items: List<Activity>, subject: String?): List<Activity> {
        val matched = if (subject.isNullOrEmpty()) {
            items
        } else {
            items.filter { a ->
                val all = a.subjects
                if (!all.isNullOrEmpty()) subject in all else a.subject == subject
            }
        }
        return matched.sortedByDescending { it.sortKey }
    }

    /** Group a (pre-sorted) list of activities into year buckets in
     *  source order. */
    fun groupedByYear(items: List<Activity>): List<YearGroup> {
        val order = mutableListOf<String>()
        val buckets = mutableMapOf<String, MutableList<Activity>>()
        for (entry in items) {
            val year = entry.sortKey.take(4)
            if (year !in buckets) { order += year; buckets[year] = mutableListOf() }
            buckets.getValue(year) += entry
        }
        return order.map { YearGroup(year = it, entries = buckets.getValue(it)) }
    }

    data class YearGroup(val year: String, val entries: List<Activity>)
}
