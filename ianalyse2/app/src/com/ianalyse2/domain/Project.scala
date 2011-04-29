package com.ianalyse2.domain



class Project(val config: ProjectConfig) {
  private  val builds:Builds = new Builds()
  //private var builds:Builds;

  def init() {
    //val builds = config.parser.parse.asInstanceOf[Builds]()
    //this.builds = builds
  }

  def get(index:Int) = {
     builds.get(index);
  }

}