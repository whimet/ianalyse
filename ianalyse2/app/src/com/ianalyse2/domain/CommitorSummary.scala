package com.ianalyse2.domain

import collection.mutable.HashMap

class CommitorSummary(val summaries: HashMap[String, CommitResult]) {
  def asJson = {
    var passCount: List[Int] = List()
    var failedCount: List[Int] = List()
    var passRate: List[BigDecimal] = List()
    for (val summary <- summaries) {
      passCount = passCount ::: List(summary._2.passedCount)
      failedCount = failedCount ::: List(summary._2.failedCount)
    }
    String.format("""
{
    "names"  : %s,
    "passed"   : %s,
    "failed" : %s
}
""",
      summaries.keys.mkString("[\"", "\",\"", "\"]"),
      passCount.mkString("[", ",", "]"),
      failedCount.mkString("[", ",", "]"))
  }
}