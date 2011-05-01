package com.ianalyse2.domain


class Builds {
  var builds: List[Build] = List[Build]()

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