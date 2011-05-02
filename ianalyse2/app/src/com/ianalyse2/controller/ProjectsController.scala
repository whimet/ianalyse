package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.{RequestMethod, RequestMapping}
import org.springframework.web.servlet.ModelAndView
import com.ianalyse2.util.LogHelper
import com.ianalyse2.domain.Projects

@Controller
@RequestMapping(Array("/projects"))
class ProjectsController extends LogHelper {

  @RequestMapping(value = Array("/index"), method = Array(RequestMethod.GET))
  def index() = {
    new ModelAndView("dashboard")
  }

  @RequestMapping(value = Array("/compare"), method = Array(RequestMethod.GET))
  def compare() = {
    val json: String = Projects.passRates.asJson
    new JsonView(json);
  }
}