package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import org.springframework.web.bind.annotation.{RequestMethod, RequestMapping}
import org.springframework.web.servlet.ModelAndView
import com.ianalyse2.util.LogHelper

@Controller
@RequestMapping(Array("/projects"))
class ProjectsController extends LogHelper {

  @RequestMapping(value = Array("/index"), method = Array(RequestMethod.GET))
  def index() = {
    new ModelAndView("dashboard")
  }

  @RequestMapping(value = Array("/compare"), method = Array(RequestMethod.GET))
  def compare() = {
    val json ="""
    {
      "names"    : "['analystic', 'lnp']"
      "passed"   : "[3, 2]"
      "failed"   : "[1, 1]"
      "rate"     : "[33.1, 66.7]"

    }
    """
    //val json: String = Projects.passRates.asJson
    new JsonView(json);
  }
}