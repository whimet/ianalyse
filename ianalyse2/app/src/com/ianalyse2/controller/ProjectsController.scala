package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import com.ianalyse2.domain.Projects
import org.springframework.web.bind.annotation.{RequestMethod, RequestMapping}
import java.lang.String
import org.springframework.web.servlet.ModelAndView
import org.apache.log4j.Logger

@Controller
@RequestMapping(Array("/projects"))
class ProjectsController {
  private val logger: Logger = Logger.getLogger(ProjectsController)

  @RequestMapping(value = Array("/index"), method = Array(RequestMethod.GET))
  def index() = {
    logger.info(".......................controller")
    val json: String = Projects.passRates.asJson
    new ModelAndView("dashboard")
  }

  @RequestMapping(value = Array("/compare"), method = Array(RequestMethod.GET))
  def comparation() = {
    val json: String = Projects.passRates.asJson
    new JsonView(json);
  }
}