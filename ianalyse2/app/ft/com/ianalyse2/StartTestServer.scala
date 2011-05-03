package com.ianalyse2

import org.apache.commons.io.IOUtils
import java.io.{InputStream, File}

object StartTestServer extends Application {
  System.out.println("started to compile the application...");
  val  pb:ProcessBuilder = new ProcessBuilder("ant", "pkg");
  pb.directory(new File("."));
  var  p:Process = pb.start();
  var inputStream: InputStream = p.getInputStream()
  var a = new Array[Byte](1024)
  while(inputStream.read(a) != -1) {
    System.out.println(new String(a))
  }
  p.waitFor();

  val  javaProcess:ProcessBuilder = new ProcessBuilder("java", "-Durl=http://deadlock.netbeans.org/hudson/api/xml", "-jar", "start.jar");
  javaProcess.directory(new File("./dist/expanded"));
  p = javaProcess.start();
  inputStream = p.getInputStream();
  a = new Array[Byte](1024)
  while(inputStream.read(a) != -1) {
    System.out.println(new String(a))
  }
  p.waitFor();
}
