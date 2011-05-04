package com.ianalyse2.domain


class Project(val config: ProjectConfig) {
  private var builds: Builds = new Builds()
  //private var builds:Builds;

  def commitorSummary = {
      builds.commitorSummary
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

  def update(builds: Builds) = {
    this.builds = this.builds ::: builds
  }

}