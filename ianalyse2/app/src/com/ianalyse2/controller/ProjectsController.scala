package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import com.ianalyse2.domain.Projects
import org.springframework.web.bind.annotation.{RequestMethod, RequestMapping}
import java.lang.String
import org.springframework.web.servlet.ModelAndView

@Controller
@RequestMapping(Array("/projects"))
class ProjectsController {

  @RequestMapping(value = Array("/index"), method = Array(RequestMethod.GET))
  def index() = {
    val json: String = Projects.passRates.asJson
    new ModelAndView("dashboard")
  }

  @RequestMapping(value = Array("/compare"), method = Array(RequestMethod.GET))
  def comparation() = {
    val json: String = Projects.passRates.asJson
    new JsonView(json);
  }
}