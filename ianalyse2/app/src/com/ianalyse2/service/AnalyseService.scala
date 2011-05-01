package com.ianalyse2.service

import org.springframework.stereotype.Service
import java.util.TimerTask
import com.ianalyse2.domain.ProjectsConfig
import com.ianalyse2.util.LogHelper

@Service
class AnalyseService extends TimerTask with LogHelper {
  override def run() {
    val configs = new ProjectsConfig("http://deadlock.netbeans.org/hudson/api/xml");
    configs.start
    configs.init
  }
}