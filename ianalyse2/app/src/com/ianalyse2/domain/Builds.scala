package com.ianalyse2.domain

import com.ianalyse2.util.LogHelper


class Builds extends LogHelper {
  var builds: List[Build] = List[Build]()

  def failedCount = {
    length - passCount
  }

  def passRate = {
    if (length > 0) {
      val mc = java.math.MathContext.DECIMAL128
      val result: BigDecimal = BigDecimal(passCount)(mc)./(BigDecimal(length))
      val percentage = result(mc) * BigDecimal(100)
      val a = percentage.setScale(1, scala.math.BigDecimal.RoundingMode.HALF_DOWN)
      a
    } else {
      BigDecimal(0)
    }

  }

  def passCount = {
    builds.filter(_.passed).size
  }

  def length = {
    builds.size
  }

  def add(build: Build) = {
    builds = builds ::: List(build)
  }

  def get(index: Int) = {
    builds(index)
  }

  def :::(builds: List[Build]): Builds = {
    val tempbuilds = this.builds.:::(builds)
    val newBuilds = new Builds
    newBuilds.builds = tempbuilds
    newBuilds
  }

  def :::(build: Build): Builds = {
    val tempbuilds = this.builds.:::(List(build))
    val newBuilds = new Builds
    newBuilds.builds = tempbuilds
    newBuilds
  }

  def :::(parseInBuilds: Builds): Builds = {
    :::(parseInBuilds.builds)
  }
}