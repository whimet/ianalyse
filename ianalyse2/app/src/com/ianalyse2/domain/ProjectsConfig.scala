package com.ianalyse2.domain

import java.net.URL
import xml.{Elem, XML}
import collection.immutable.List
import scala.actors.Actor._
import actors.{Actor, DaemonActor}

class ProjectsConfig(val url: String) extends Iterator[ProjectConfig] with Actor {
  private var list: List[ProjectConfig] = List()
  private var actors: List[Actor] = List()

  def init = {
    parseProjectsFromConfiguration
    var projects: List[Project] = List();
    val caller = this;
    for (projectConfig <- list) {
      val myActor: Actor = actor {
        caller ! projectConfig.instantiate
      }
      actors = actors ::: List(myActor)
    }
  }

  private object Stop

  def act() {
    while (true) {
      receive {
        case project: Project =>
          Projects.update(project)
        case Stop => exit()
      }
    }
  }

  def stop() {
    this ! Stop
  }

  def get(index: Int) = {
    list(index);
  }

  def count = {
    list.size
  }

  @Override
  def next = {
    list.iterator.next
  }

  @Override
  def hasNext = {
    list.iterator.hasNext
  }

  def parseToElement = {
    "abc"
  }

  def destory {
    for (actor <- actors) {
      try {
        actor ! exit
      } catch {
        case e => System.out.println(e.printStackTrace)
      }
    }
  }

  def parseProjectsFromConfiguration {
    val elem: Elem = XML.load(new URL(this.url))
    val jobSegments = elem \ "job"
    list = list ::: jobSegments.map(job => new ProjectConfig((job \ "name").text, (job \ "url").text)).toList
  }
}

