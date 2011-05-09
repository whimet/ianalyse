package com.ianalyse2.domain


class Project(val config: ProjectConfig) {
  private var builds: Builds = new Builds()
  //private var builds:Builds;

  def name = {
    config.name
  }

  def commitorSummary = {
    builds.commitResults
  }

  def length = {
    builds.length
  }

  def get(index: Int) = {
    builds.get(index);
  }

  def passCount = {
    builds.passCount
  }

  def failedCount = {
    builds.failedCount
  }

  def passRate = {
    builds.passRate
  }

  def avgDuration = {
    builds.avgDuration / 60000
  }

  def update(builds: Builds) = {
    this.builds = this.builds ::: builds
  }

}