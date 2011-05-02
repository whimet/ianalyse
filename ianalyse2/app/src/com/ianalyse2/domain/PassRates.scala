package com.ianalyse2.domain

import collection.mutable.LinkedHashMap

class PassRates() {
  def asJson = {
    val pjs: LinkedHashMap[String, Project] = Projects.projects
    var passCount: List[Int] = List()
    var failedCount: List[Int] = List()
    var passRate: List[BigDecimal] = List()
    for (val pj <- pjs) {
      passCount = passCount ::: List(pj._2.passCount)
      failedCount = failedCount ::: List(pj._2.failedCount)
      passRate = passRate ::: List(pj._2.passRate)
    }
    String.format("""
{
    "names"  : %s,
    "passed"   : %s,
    "failed" : %s,
    "rate"   : %s
}
""",
      pjs.keys.mkString("[\"", "\",\"", "\"]"),
      passCount.mkString("[", ",", "]"),
      failedCount.mkString("[", ",", "]"),
      passRate.mkString("[", ",", "]"))
  }

  def decimalToString(a: List[BigDecimal]) = {
    val b: StringBuilder = new StringBuilder();
    b.append('[');
    var result = ""
    for (i <- 0 until a.length) {
      b.append(a(i));
      if (i == a.length - 1)
        result = b.append(']').toString();
      b.append(", ");
    }
    result
  }
}

