package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import com.ianalyse2.util.LogHelper
import com.ianalyse2.domain.Projects
import org.springframework.web.bind.annotation.{PathVariable, RequestMethod, RequestMapping}
import org.springframework.web.servlet.ModelAndView
import java.util.HashMap

@Controller
@RequestMapping(Array("/project"))
class ProjectController extends LogHelper {
  @RequestMapping(value = Array("/{project}.html"), method = Array(RequestMethod.GET))
  def index(@PathVariable project: String) = {
    val data:HashMap[String, String] = new HashMap[String, String]();
    data.put("project", project)
    new ModelAndView("project/index", data)
  }

  @RequestMapping(value = Array("/{project}/commitors.json"), method = Array(RequestMethod.GET))
  def commitors(@PathVariable project: String) = {
    new JsonView(Projects.find(project).commitorSummary.asJson);
  }
}