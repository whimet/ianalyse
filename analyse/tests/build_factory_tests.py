from django.test import TestCase

from analyse.models import Build
from analyse.config import Config, Configs
from analyse.models import Builds
import os
from django.conf import settings
from datetime import datetime
from analyse.tests.testutil import TestUtils

class BuildFactoryTest(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def connectfour(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/connectfour4'

    def cclive_release_jdk(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'        
         
    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testToParseAllTheLogs(self):
        self.assertEqual(2, len(Builds.create_builds(TestUtils().connectfour_config(), BuildFactoryTest.PATTERN)))

    def testToParseTheInformationCorrectly(self):
        builds = Builds.create_builds(TestUtils().connectfour_config(), BuildFactoryTest.PATTERN);
        self.assertEqual('connectfour4', builds[0].name)

    def testShouldParseAndPersit(self):
          builds = Builds.create_builds(TestUtils().connectfour_config(), BuildFactoryTest.PATTERN);
          self.assertEqual(2, builds.total_count())
        
    def testShouldNotThrowExceptionWhenProcessingXmlFile(self):
      try:
          builds = Builds.create_builds(TestUtils().cclive_config(), "log20080624064201Lbuild.70.xml")
      except Exception, e:
          self.fail('should not throw any exception at all')

 
    def testShouldOnlyParseThe5Builds(self) :
          builds = Builds.create_builds(TestUtils().cclive_config(), None)
          self.assertEquals(2, len(builds))
          self.assertEquals(datetime(2008, 9, 24, 5, 25, 6), builds[0].start_time)
          self.assertEquals(datetime(2008, 9, 24, 6, 29, 41), builds[1].start_time)

    def testShouldSelectValuesFromFiles(self) :pass
          #to remove the lxml
          # values = Builds.select_values_from(TestUtils().cclive_config(), None)
          # self.assertEquals(5, len(values))
          # 
          # self.assertEquals('cclive-release-jdk1.5', values[0][0])
          # self.assertEquals('build.6', values[0][1])
          # self.assertEquals('2 minutes 45 seconds', values[0][2])
          # self.assertEquals(None, values[0][3])
          # self.assertEquals('cclive-release-jdk1.5', values[1][0])
          # self.assertEquals('build.6', values[1][1])
          # self.assertEquals('3 minutes 45 seconds', values[1][2])
          # self.assertEquals(None, values[1][3])

    def testShouldOnlyParseThe5Builds(self) :
        builds = Builds.create_builds(TestUtils().cclive_config(), None)
        self.assertEquals(5, len(builds))
        self.assertEquals(datetime(2008, 9, 23, 02, 13, 38), builds[0].start_time)
        self.assertEquals(datetime(2008, 9, 24, 6, 29, 41), builds[4].start_time)




    
    
    
    