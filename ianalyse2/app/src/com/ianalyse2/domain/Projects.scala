package com.ianalyse2.domain


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

  def get(index: Int) = {
    projects(index)
  }
}