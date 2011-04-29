package com.ianalyse2.parser


import xml.{Elem, XML}
import org.joda.time.DateTime
import org.apache.commons.lang.{StringUtils}
import java.io.{InputStream}
import java.util.regex.{Matcher, Pattern}
import com.ianalyse2.domain.{ProjectConfig, Builds, Build}
import org.apache.commons.io.IOUtils
import java.net.URL

object HudonBuildParser {

  def parse() {
    new Builds()
  }

  def parse(config: ProjectConfig) = {
    val in = new URL(config.jobUrl).openStream();
    try {
      val elem: Elem = XML.load(in)
      val jobSegments = elem \ "job"
      for (jobSegment <- jobSegments) {
        val name: String = (jobSegment \ "name").text
        val url: String = (jobSegment \ "url").text
        //list = list ::: List(new ProjectConfig(name, url))
      }
    } finally {
      IOUtils.closeQuietly(in);
    }
  }

  def parseJob(stream: InputStream) = {
    val elem: Elem = XML.load(stream)
    val commitor = parseCommiter(elem)
    new Build(name((elem \ "url").text),
      (elem \ "number").text,
      new DateTime(),
      (elem \ "duration").text.toInt,
      result((elem \ "result").text),
      commitor);
  }

  def parseCommiter(elem: Elem) = {
    var commiters:List[String] = List[String]()
    var commitorSegment = elem \ "culprit"
    for (commitor <- commitorSegment) {
      commiters = commiters ::: List((commitor \ "fullName").text)
    }

    commiters
  }

  def name(workspace: String) = {
    val pattern: Pattern = Pattern.compile(".*/job/(.+)/.+")
    val matcher: Matcher = pattern.matcher(workspace)
    if (matcher.matches()) {
      matcher.group(1);
    } else {
      ""
    }
  }

  def result(result: String) = {
    !StringUtils.equals(result, "FAILURE")
  }
}