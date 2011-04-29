package com.ianalyse2.domain

import org.joda.time.DateTime


class Build(val name: String,
            val number: String,
            val startTime: DateTime,
            val duration: Int,
            val passed: Boolean,
            val commitors: List[String]) {
}
