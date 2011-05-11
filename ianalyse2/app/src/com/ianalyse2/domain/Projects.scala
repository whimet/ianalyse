package com.ianalyse2.domain

import collection.mutable.LinkedHashMap

object Projects {
  var projects: LinkedHashMap[String, Project]
  = new LinkedHashMap[String, Project]();

  def passRates = {
    new PassRates()
  }
  def passedCount = {
    var i = 0;
    for (project <- projects) {
      if (project._2.passed) {
        i = i+ 1
      }
    }
    i
  }

  def failedCount = {
    length - passedCount
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
    var names: List[Project] = List()
    for (val summary <- sorted) {
      names = names ::: List(summary._2)
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