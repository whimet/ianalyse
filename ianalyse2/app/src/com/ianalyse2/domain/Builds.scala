package com.ianalyse2.domain


class Builds {
  private var builds:List[Build] = List[Build]()

  def passCount = {
    builds.filter(_.passed).size
  }

  def totalCount = {
    builds.size
  }

  def add(build:Build)= {
    builds = builds ::: List(build)
  }

  def get(index:Int) = {
    builds(index)
  }
}