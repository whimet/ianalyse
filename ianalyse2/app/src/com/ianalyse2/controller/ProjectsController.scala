package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import com.ianalyse2.domain.Projects
import org.springframework.web.bind.annotation.{RequestMethod, RequestMapping}
import java.lang.String
import org.springframework.web.servlet.ModelAndView
import com.ianalyse2.util.LogHelper

@Controller
@RequestMapping(Array("/projects"))
class ProjectsController extends LogHelper {

  @RequestMapping(value = Array("/index"), method = Array(RequestMethod.GET))
  def index() = {
    val json: String = Projects.passRates.asJson
    new ModelAndView("dashboard")
  }

  @RequestMapping(value = Array("/compare"), method = Array(RequestMethod.GET))
  def compare() = {
    val json: String = Projects.passRates.asJson
    new JsonView(json);
  }
}