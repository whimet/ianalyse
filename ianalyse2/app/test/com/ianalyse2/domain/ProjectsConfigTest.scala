package com.ianalyse2.domain

import org.scalatest.Spec
import org.scalatest.matchers.ShouldMatchers

class ProjectsConfigTest extends Spec with ShouldMatchers {
  describe("analyse the jobs") {
    it("should pass the all the jobs") {
      val config = new ProjectsConfig("http://deadlock.netbeans.org/hudson/api/xml");
      config.init
      config.count should be > 0
    }

    it("should parse the single config correct") {
      val configs = new ProjectsConfig("http://deadlock.netbeans.org/hudson/api/xml")
      configs.init
      val config: ProjectConfig = configs.get(0)
      config.name should be === "analytics-server"
      config.url should be === "http://deadlock.netbeans.org/hudson/job/analytics-server/"
    }

    it("should parse get the project") {
      val configs = new ProjectsConfig("http://deadlock.netbeans.org/hudson/api/xml")
      configs.start
      configs.init
      Thread.sleep(50000)
      val project: Project = Projects.get(0)
      project.config.name should be === "analytics-server"
    }
  }
}