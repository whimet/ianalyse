package com.ianalyse2.domain

import collection.mutable.HashMap


class CommitResults {
  val commitorsSummary = new HashMap[String, CommitResult](){
    override def default(key:String) = new CommitResult(0, 0)
  };

  def add(passed: Boolean, commitors:List[String]) = {
    for(commitor <- commitors) {
      val result: CommitResult = commitorsSummary(commitor)
      commitorsSummary += (commitor -> result.updateResult(passed))
    }
  }

  def passedCount(name:String) = {
      commitorsSummary(name).passedCount
  }

  def failedCount(name:String) = {
      commitorsSummary(name).failedCount
  }
}