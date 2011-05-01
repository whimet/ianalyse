package com.ianalyse;

import org.apache.commons.io.FileUtils;
import org.mortbay.jetty.Connector;
import org.mortbay.jetty.Server;
import org.mortbay.jetty.nio.SelectChannelConnector;
import org.mortbay.jetty.webapp.WebAppContext;

import java.io.File;
import java.io.IOException;

public class IanalyseServer {
    public static void main(String[] args) {
        try {
            Server server = new Server();
            Connector con = new SelectChannelConnector();
            con.setPort(8000);
            server.addConnector(con);

            WebAppContext wac = new WebAppContext();
            wac.setResourceBase(getResourceBase());
            wac.setDescriptor("WEB-INF/web.xml");
            wac.setContextPath("/ianalyse2");
            server.setHandler(wac);

            server.start();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private static String getResourceBase() throws IOException {
        FileUtils.cleanDirectory(new File("/Users/twer/Workspace/ianalyse/ianalyse2/app/webapp/WEB-INF/classes"));
        FileUtils.copyDirectory(
                new File("/Users/twer/Workspace/ianalyse/ianalyse2/out/production/app"),
                new File("/Users/twer/Workspace/ianalyse/ianalyse2/app/webapp/WEB-INF/classes")
        );
        return "/Users/twer/Workspace/ianalyse/ianalyse2/app/webapp";
    }
}
