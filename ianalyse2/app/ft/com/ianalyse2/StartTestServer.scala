package com.ianalyse2

import org.apache.commons.io.IOUtils
import java.io.File

object StartTestServer extends Application {
  System.out.println("started to compile the application...");
  ProcessBuilder pb = new ProcessBuilder("ant", "copy.app.jar");
  pb.directory(new File("."));
  Process p = pb.start();
  String output = IOUtils.toString(p.getInputStream());
  System.out.println(output);
  p.waitFor();
  System.out.println("done");
}
