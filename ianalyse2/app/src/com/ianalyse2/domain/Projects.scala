package com.ianalyse2.domain

import scala.util.control._

object Projects {
  var projects: List[Project] = List();

  def passRates = {
    new PassRates()
  }

  def clearAndReset() {

  }

  def update(project: Project) {
    projects = projects ::: List(project)
  }

  def find(name: String) = {
    projects.filter(project => project.config.name == name)
  }

  def get(index: Int) = {
    projects(index)
  }

  def length = {
    projects.length
  }
}