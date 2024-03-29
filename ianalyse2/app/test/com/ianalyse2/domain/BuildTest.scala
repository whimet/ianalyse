package com.ianalyse2.domain

import org.scalatest.Spec
import org.scalatest.matchers.ShouldMatchers
import org.joda.time.{DateTimeZone, DateTime}

class BuildTest extends Spec with ShouldMatchers {
  describe("analyse the builds") {

    it("should handle the empty builds correctly") {
      val b1 = new Build("analystic-server", "1", new DateTime(2010, 12, 8, 0, 0, 0, 0, DateTimeZone.UTC), 12, false, List("jack", "ying"))
      b1.toJavaScriptDate should be === 1291766400000L
    }

    it("should handle pm correctly") {
      val b1 = new Build("analystic-server", "1", new DateTime(2010, 12, 8, 14, 1, 1, 0, DateTimeZone.UTC), 12, false, List("jack", "ying"))
      b1.toJavaScriptTime should be === 14
    }
    
    it("should handle an correctly") {
      val b1 = new Build("analystic-server", "1", new DateTime(2010, 12, 8, 2, 1, 1, 0, DateTimeZone.UTC), 12, false, List("jack", "ying"))
      b1.toJavaScriptTime should be === 2
    }

    it("should handle per build detail") {
      val b1 = new Build("analystic-server", "1", new DateTime(2010, 12, 8, 2, 0, 0, 0, DateTimeZone.UTC), 12, false, List("jack", "ying"))
      b1.toPerBuild should be === "[1291766400000,2,1]"
    }
  }
}