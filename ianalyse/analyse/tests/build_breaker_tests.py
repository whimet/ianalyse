from django.test import TestCase

from analyse.models import Build, Builds
import os
from django.conf import settings
from datetime import datetime
import util.datetimeutils
from analyse.tests.testutil import TestUtils

class BuildBreakerTests(TestCase):
    FAILED_LOG_AT_OCT_11 = '''<cruisecontrol>
    <modifications>
      <modification type="mercurial">
        <file action="added">
          <revision>12</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-13T09:48:27</date>
        <user>khu</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>12</revision>
      </modification>
      <modification type="mercurial">
        <file action="modified">
          <revision>12</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-17T09:48:27</date>
        <user>khu</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>12</revision>
      </modification>
    </modifications>
      <info>
        <property name="projectname" value="connectfour4" />
        <property name="lastbuild" value="20091011000000" />
        <property name="lastsuccessfulbuild" value="20091011000000" />
        <property name="builddate" value="2009-10-11T09:39:22" />
        <property name="cctimestamp" value="20091011173922" />
        <property name="label" value="build.1" />
        <property name="interval" value="300" />
        <property name="lastbuildsuccessful" value="true" />
        <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
        <property name="logfile" value="log20091011173922.xml" />
      </info>
      <build time="1 minute(s) 0 second(s)">
        <target name="exec">
          <task name="echo">
            <message priority="info"><![CDATA[haha]]></message>
          </task>
        </target>
      </build>
    </cruisecontrol>'''
        
    DID_NOT_FIX_IT_LOG = '''<?xml version="1.0" encoding="UTF-8"?>
    <cruisecontrol>
      <modifications>
        <modification type="mercurial">
          <file action="added">
            <revision>12</revision>
            <filename>b</filename>
          </file>
          <date>2009-10-13T09:48:27</date>
          <user>khu</user>
          <comment><![CDATA[fucked]]></comment>
          <revision>12</revision>
        </modification>
        <modification type="mercurial">
          <file action="modified">
            <revision>12</revision>
            <filename>b</filename>
          </file>
          <date>2009-10-17T09:48:27</date>
          <user>khu</user>
          <comment><![CDATA[fucked]]></comment>
          <revision>12</revision>
        </modification>
        <modification type="mercurial">
          <file action="modified">
            <revision>13</revision>
            <filename>b</filename>
          </file>
          <date>2009-10-17T09:48:27</date>
          <user>xkf</user>
          <comment><![CDATA[fucked]]></comment>
          <revision>13</revision>
        </modification>
      </modifications>
      <info>
        <property name="projectname" value="connectfour4" />
        <property name="lastbuild" value="20091011201149" />
        <property name="lastsuccessfulbuild" value="20091011201149" />
        <property name="builddate" value="2009-10-17T14:03:24" />
        <property name="cctimestamp" value="20091017220324" />
        <property name="label" value="build.18" />
        <property name="interval" value="300" />
        <property name="lastbuildsuccessful" value="true" />
        <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
        <property name="logfile" value="log20091017220324.xml" />
      </info>
      <build time="0 minute(s) 4 second(s)" error="exec error">
        <target name="exec">
          <task name="echa">
            <message priority="error"><![CDATA[Could not execute command: echa with arguments: haha]]></message>
          </task>
        </target>
      </build>
    </cruisecontrol>'''
        
    FIXED_IT_LOG = '''<cruisecontrol>
    <modifications>
      <modification type="mercurial">
        <file action="added">
          <revision>12</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-13T09:48:27</date>
        <user>khu</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>12</revision>
      </modification>
      <modification type="mercurial">
        <file action="modified">
          <revision>12</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-17T09:48:27</date>
        <user>khu</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>12</revision>
      </modification>
      <modification type="mercurial">
        <file action="modified">
          <revision>13</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-17T09:48:27</date>
        <user>xkf</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>13</revision>
      </modification>
      <modification type="mercurial">
        <file action="modified">
          <revision>14</revision>
          <filename>b</filename>
        </file>
        <date>2009-10-17T09:48:27</date>
        <user>xkf</user>
        <comment><![CDATA[fucked]]></comment>
        <revision>14</revision>
      </modification>
    </modifications>
  <info>
    <property name="projectname" value="connectfour4" />
    <property name="lastbuild" value="20091011000000" />
    <property name="lastsuccessfulbuild" value="20091011000000" />
    <property name="builddate" value="2009-10-11T09:39:22" />
    <property name="cctimestamp" value="20091011173922" />
    <property name="label" value="build.1" />
    <property name="interval" value="300" />
    <property name="lastbuildsuccessful" value="true" />
    <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
    <property name="logfile" value="log20091011173922Lbuild.1.xml" />
  </info>
  <build time="1 minute(s) 0 second(s)">
    <target name="exec">
      <task name="echo">
        <message priority="info"><![CDATA[haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''

    ANOTHER_PASS = '''<cruisecontrol>
    <modifications>
        <modification type="mercurial">
          <file action="added">
            <revision>15</revision>
            <filename>b</filename>
          </file>
          <date>2009-10-13T09:48:27</date>
          <user>xkf</user>
          <comment><![CDATA[fucked]]></comment>
          <revision>15</revision>
        </modification>
      </modifications>
  <info>
    <property name="projectname" value="connectfour4" />
    <property name="lastbuild" value="20091011000000" />
    <property name="lastsuccessfulbuild" value="20091011000000" />
    <property name="builddate" value="2009-10-11T10:39:22" />
    <property name="cctimestamp" value="20091011173900" />
    <property name="label" value="build.1" />
    <property name="interval" value="300" />
    <property name="lastbuildsuccessful" value="true" />
    <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
    <property name="logfile" value="log20091011173922Lbuild.1.xml" />
  </info>
  <build time="0 minute(s) 2 second(s)">
    <target name="exec">
      <task name="echo">
        <message priority="info"><![CDATA[haha]]></message>
      </task>
    </target>
  </build>
</cruisecontrol>'''



    def setUp(self):
        self.testutils                = TestUtils()
        self.root                     = settings.PROJECT_DIR
        self.failed                   = Build.from_file(self.testutils.write_to_temp('FAILED_LOG.xml', BuildBreakerTests.FAILED_LOG_AT_OCT_11))
        self.did_not_fix         = Build.from_file(self.testutils.write_to_temp('PASSED_LOG_AT_OCT_11.xml', BuildBreakerTests.DID_NOT_FIX_IT_LOG))
        self.fixed_it = Build.from_file(self.testutils.write_to_temp('ANOTHER_PASSED_LOG_AT_OCT_11.xml', BuildBreakerTests.FIXED_IT_LOG))
        self.another_pass = Build.from_file(self.testutils.write_to_temp('FAILED_LOG_AT_OCT_11.xml', BuildBreakerTests.ANOTHER_PASS))        
        

    def tearDown(self):
        self.testutils.cleantemp()
        
    def test_should_group_the_commitors_based_on_(self):
        builds = Builds()
        builds.builds = [self.failed,  self.did_not_fix, self.fixed_it, self.another_pass]
        grouped_commitors = builds.build_breakers()
        commitor = grouped_commitors.find('xkf')
        self.assertEquals(2, commitor.passed_count())
        self.assertEquals(1, commitor.failed_count())

        commitor = grouped_commitors.find('khu')
        self.assertEquals(0, commitor.passed_count())
        self.assertEquals(1, commitor.failed_count())
        

