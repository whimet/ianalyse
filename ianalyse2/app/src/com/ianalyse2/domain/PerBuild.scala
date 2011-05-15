package com.ianalyse2.domain

class PerBuild(val builds: List[Build]) {
  def asJson = {
    var allPassed = List[String]()
    var allFailed = List[String]()
    for (val build <- builds) {
      if (build.passed) {
        allPassed = allPassed ::: List(build.toPerBuild)
      } else{
        allFailed = allFailed ::: List(build.toPerBuild)
      }
    }
    String.format("""
{
    "passed"   : %s,
    "failed" : %s
}
""",allPassed.mkString("[", ",", "]"), allFailed.mkString("[", ",", "]"))
  }
}