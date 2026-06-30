package com.vivianweidai.science.core.api

import com.vivianweidai.science.core.model.Activity
import com.vivianweidai.science.core.model.ActivityList
import com.vivianweidai.science.core.model.ResearchScience
import com.vivianweidai.science.core.model.ResearchTechResponse
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.serialization.json.Json

/**
 * Read-only client for activity listings (olympiads + textbooks) and
 * research tech. Source of truth: YAML in public/content/{olympiads,research}/,
 * built to JSON by a Python script, then fetched from vivianweidai.com.
 * No backend, no auth, no writes.
 */
class ApiClient {
    private val mutex = Mutex()
    private val json = Json { ignoreUnknownKeys = true }
    private var cachedActivities: List<Activity>? = null
    private var cachedSciences: List<ResearchScience>? = null

    suspend fun listActivities(): List<Activity> = mutex.withLock {
        cachedActivities?.let { return it }
        val body = Http.getString(OLYMPIADS_URL)
        val list = json.decodeFromString<ActivityList>(body).items
        cachedActivities = list
        list
    }

    suspend fun listResearchSciences(): List<ResearchScience> = mutex.withLock {
        cachedSciences?.let { return it }
        val body = Http.getString(TECH_URL)
        val sciences = json.decodeFromString<ResearchTechResponse>(body).sciences
        cachedSciences = sciences
        sciences
    }

    suspend fun invalidate() = mutex.withLock {
        cachedActivities = null
        cachedSciences = null
    }

    companion object {
        const val OLYMPIADS_URL = "https://vivianweidai.com/olympiads/olympiads.json"
        const val TECH_URL = "https://vivianweidai.com/research/technology.json"
        val shared = ApiClient()
    }
}
