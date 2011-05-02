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
    projects.contains(name)
  }

  //  def get(index: Int) = {
  //    projects(index)
  //  }

  def length = {
    projects.size
  }
}