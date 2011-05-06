package com.ianalyse2.domain

import collection.mutable.LinkedHashMap

object Projects {
  var projects: LinkedHashMap[String, Project]
  = new LinkedHashMap[String, Project]();

  def passRates = {
    new PassRates()
  }

  def reset() {
    projects.clear
  }

  def update(project: Project) {
    projects.put(project.config.name, project)
  }

  def find(name: String) = {
    projects(name)
  }

  def inOrder = {
    val sorted = projects.toSeq.sortBy(_._1)
    var names: List[String] = List()
    for (val summary <- sorted) {
      names = names ::: List(summary._1)
    }
    names
  }

  //  def get(index: Int) = {
  //    projects(index)
  //  }

  def length = {
    projects.size
  }
}