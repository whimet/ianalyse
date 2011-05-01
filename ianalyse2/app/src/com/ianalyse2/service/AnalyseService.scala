package com.ianalyse2.service

import org.springframework.stereotype.{Service, Controller}
import java.util.TimerTask
import com.ianalyse2.domain.ProjectsConfig
import org.apache.log4j.Logger

@Service
class AnalyseService extends TimerTask {
  private val logger: Logger = Logger.getLogger(AnalyseService)

  override def run() {
    logger.info("starting the analyse")
    System.out.println("Start......................");
    //    val configs = new ProjectsConfig("http://deadlock.netbeans.org/hudson/api/xml");
    //    configs.start
    //    configs.init
  }

}