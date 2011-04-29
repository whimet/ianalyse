from django.test import TestCase

from analyse.models import Build, Builds
import os
from django.conf import settings
from datetime import datetime
import util.datetimeutils
from analyse.tests.testutil import TestUtils

class BuildsByDayTests(TestCase):
    FAILED_LOG_AT_OCT_11 = '''<cruisecontrol>
      <modifications />
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
    
    PASSED_LOG_AT_OCT_11 = '''<cruisecontrol>
  <modifications />
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
    ANOTHER_PASSED_LOG_AT_OCT_11 = '''<cruisecontrol>
  <modifications />
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

    FAILED_LOG = '''<?xml version="1.0" encoding="UTF-8"?>
<cruisecontrol>
  <modifications>
    <modification type="mercurial">
      <file action="added">
        <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
        <filename>b</filename>
      </file>
      <date>2009-10-13T09:48:27</date>
      <user>twer@localhost</user>
      <comment><![CDATA[fucked]]></comment>
      <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
    </modification>
    <modification type="mercurial">
      <file action="modified">
        <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
        <filename>b</filename>
      </file>
      <date>2009-10-17T09:48:27</date>
      <user>twer@localhost</user>
      <comment><![CDATA[fucked]]></comment>
      <revision>1:96ad1ef37c2ae7828a66e16d8eb508b7b69465a4</revision>
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

    def setUp(self):
        self.testutils                = TestUtils()
        self.root                     = settings.PROJECT_DIR
        self.failed                   = Build.from_file(self.testutils.write_to_temp('FAILED_LOG.xml', BuildsByDayTests.FAILED_LOG))
        self.passed_at_oct_11         = Build.from_file(self.testutils.write_to_temp('PASSED_LOG_AT_OCT_11.xml', BuildsByDayTests.PASSED_LOG_AT_OCT_11))
        self.another_passed_at_oct_11 = Build.from_file(self.testutils.write_to_temp('ANOTHER_PASSED_LOG_AT_OCT_11.xml', BuildsByDayTests.ANOTHER_PASSED_LOG_AT_OCT_11))
        self.failed_at_oct_11 = Build.from_file(self.testutils.write_to_temp('FAILED_LOG_AT_OCT_11.xml', BuildsByDayTests.FAILED_LOG_AT_OCT_11))        
        

    def tearDown(self):
        self.testutils.cleantemp()

    def test_should_total_runs_by_day(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed_at_oct_11]
        n_days_summary = builds.get_n_days_summary();
        
        self.assertEquals(3, n_days_summary.total_runs_values()[0].get('y'))
    
    def test_should_return_zero_total_runs_if_no_builds(self):
        builds = Builds()
        n_days_summary = builds.get_n_days_summary();
        
        self.assertEquals(0, len(n_days_summary.total_runs_values()))

    
    def test_should_passed_runs_by_day(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed_at_oct_11]
        n_days_summary = builds.get_n_days_summary();

        self.assertEquals(2, n_days_summary.passed_runs_values()[0].get('y'))
    
    def test_should_return_zero_if_no_passed_build(self):
        builds = Builds()
        builds.builds = [self.failed_at_oct_11]

        n_days_summary = builds.get_n_days_summary();
        self.assertEquals(0, n_days_summary.passed_runs_values()[0].get('y'))

    def test_should_return_zero_passed_build_if_no_builds(self):
        builds = Builds()
        n_days_summary = builds.get_n_days_summary();
        self.assertEquals(0, len(n_days_summary.passed_runs_values()))

    
    def test_should_passed_runs_by_day(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11, self.failed_at_oct_11]
        n_days_summary = builds.get_n_days_summary();

        self.assertEquals(1, n_days_summary.failed_runs_values()[0].get('y'))

    def test_should_return_zero_if_no_passed_build(self):
        builds = Builds()
        builds.builds = [self.passed_at_oct_11,  self.another_passed_at_oct_11]

        n_days_summary = builds.get_n_days_summary();
        self.assertEquals(0, n_days_summary.failed_runs_values()[0].get('y'))

    def test_should_return_zero_passed_build_if_no_builds(self):
        builds = Builds()
        n_days_summary = builds.get_n_days_summary();
        self.assertEquals(0, len(n_days_summary.failed_runs_values()))


