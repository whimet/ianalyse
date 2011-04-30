package com.ianalyse2.domain

import xml.{Elem, XML}
import com.ianalyse2.parser.HudonBuildParser

class ProjectConfig(val name: String, val url: String) {
  private var list: List[ProjectConfig] = List()

  def instantiate() = {
    val project: Project = new Project(this)
    val builds = HudonBuildParser.parse(this)
    project.update(builds)
    System.out.println("return project")
    project
  }

  def jobUrl = {
    this.url + "api/xml"
  }
}