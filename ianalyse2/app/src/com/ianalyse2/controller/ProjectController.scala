package com.ianalyse2.controller

import org.springframework.stereotype.Controller
import com.ianalyse2.util.LogHelper
import com.ianalyse2.domain.Projects
import org.springframework.web.bind.annotation.{PathVariable, RequestMethod, RequestMapping}

@Controller
@RequestMapping(Array("/project"))
class ProjectController extends LogHelper {
  @RequestMapping(value = Array("/{project}/commitors"), method = Array(RequestMethod.GET))
  def commitors(@PathVariable project: String) = {
    new JsonView(project);
  }
}