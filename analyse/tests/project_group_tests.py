from django.test import TestCase

from analyse.models import *
import os
from django.conf import settings
from datetime import datetime
import util.datetimeutils
from analyse.models import *
from analyse.tests.testutil import TestUtils

class ProjectGroupTests(TestCase):
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
        

    def tearDown(self):
        self.testutils.cleantemp()
        
    def testShouldGroupTheBuilds(self):
        acc_builds = self._builds_obj('acc', [self.failed(),  self.another_passed_at_oct_11(), self.passed_at_oct_11()])
        safe_builds = self._builds_obj('safe', [self.failed(),  self.another_passed_at_oct_11()])
        pg = ProjectGroup()
        pg.append('acc', acc_builds)
        pg.append('safe', safe_builds)
        
        values, names, max = pg.projects_comparation()
        self.assertEquals(2, values[0][0])
        self.assertEquals(1, values[0][1])
        self.assertEquals(1, values[1][0])
        self.assertEquals(1, values[1][1])
        self.assertEquals('acc', names[0])
        self.assertEquals('safe', names[1])
        self.assertEquals(3, max)
        

    def _builds_obj(self, project_id, builds):
        all_builds = []
        builds_obj = Builds()
        for build in builds:
            build.project_id = project_id
        
        builds_obj.builds = builds
        return builds_obj
 
    def failed(self):
        return Build.from_file(self.testutils.write_to_temp('FAILED_LOG.xml', ProjectGroupTests.FAILED_LOG))

    def passed_at_oct_11(self):
        return Build.from_file(self.testutils.write_to_temp('PASSED_LOG_AT_OCT_11.xml', ProjectGroupTests.PASSED_LOG_AT_OCT_11))

    def another_passed_at_oct_11(self):
        return Build.from_file(self.testutils.write_to_temp('ANOTHER_PASSED_LOG_AT_OCT_11.xml', ProjectGroupTests.ANOTHER_PASSED_LOG_AT_OCT_11))

    def failed_at_oct_11(self):
        return Build.from_file(self.testutils.write_to_temp('FAILED_LOG_AT_OCT_11.xml', ProjectGroupTests.FAILED_LOG_AT_OCT_11))
        
        
# def test_should_not_remove_records_of_other_project(self):
#     self.assertEqual(0, len(Build.objects.all()))
#     builds = Builds.create_builds(TestUtils().connectfour_config(), BuildFactoryTest.PATTERN);
#     self.assertEqual(2, len(Build.objects.all()))
#     builds = Builds.create_builds(TestUtils().cclive_config(), None);        
#     self.assertEqual(7, len(Build.objects.all()))
#