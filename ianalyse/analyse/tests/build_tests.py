from django.test import TestCase

from analyse.models import *
import os
from django.conf import settings
from datetime import datetime, timedelta
from analyse.tests.testutil import TestUtils
from analyse.config import *
from analyse.plugin import Plugins

class BuildTest(TestCase):

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + '/analyse/tests/fixtures/connectfour4'

    def testToParseTheProjectName(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual("connectfour4", build.name)
    
    def testToParseThePassLogForBuildNumber(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual("build.1", build.number)
    
    def testToParseTheFailedLogForBuildNumber(self):
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual("build.18", build.number)
    
    def testToParseThePassFailedLogForResult(self):
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual(False, build.is_passed)
    
    def testToParseThePassPassedLogForResult(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual(True, build.is_passed)
    
    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 17, 39, 22);
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual(expecteddate, build.start_time)
    
    def testToParseTheFailedLogForBuildDate(self):
        expecteddate = datetime(2009, 10, 11, 20, 11, 49);
        build = Build.from_file(self.ccroot + '/log20091013220324.xml')
        self.assertEqual(expecteddate, build.last_pass)
    
    def testToParseTheFailedLogForBuildDate(self):
            expecteddate = datetime(2009, 10, 11, 20, 11, 49);
            build = Build.from_file(self.ccroot + '/log20091013220324.xml')
            self.assertEqual(expecteddate, build.last_build)
    
    def testToSelectValuesAsArrayByApplyingXPath(self):
        file = self.ccroot + '/log20091011173922Lbuild.1.xml'
        config = Groups().default().find('connectfour4')
        result = Build.select_values(file, config, Plugins.INSTANCE())
    
    
        self.assertEquals('1 minute(s) 0 second(s)', result[0])
        self.assertEquals('build.1', result[1])
        self.assertEquals('20091011000000', result[2])
        self.assertEquals('20091011000000', result[3])
        self.assertEquals('connectfour4', result[4])
        self.assertEquals('Passed', result[5])
        self.assertEquals('20091011173922', result[6])
    
    
    def testUserShouldPayMoreAttentionIfLastBuildHappend24HoursAgo(self):
        build = Build()
        twenty_five_hours_ago = datetime.now() - timedelta(hours=25)
        build.start_time = twenty_five_hours_ago
        self.assertEquals(True, build.need_attention())
    
    def testUserShouldFeelSafeIfLastBuildHappendLessThan24HoursAgo(self):
        build = Build()
        twenty_three_hours_ago = datetime.now() - timedelta(hours=23)
        build.start_time = twenty_three_hours_ago
        self.assertEquals(False, build.need_attention())
    
    def testUserShouldPayMoreAttentionIfLastPassedBuildHappend24HoursAgo(self):
        build = Build()
        twenty_five_hours_ago = datetime.now() - timedelta(hours=25)
        build.last_pass = twenty_five_hours_ago
        self.assertEquals(True, build.need_attention())
    
    def testUserShouldFeelSafeIfLastPassedBuildHappendLessThan23HoursAgo(self):
       build = Build()
       twenty_three_hours_ago = datetime.now() - timedelta(hours=23)
       build.last_pass = twenty_three_hours_ago
       self.assertEquals(False, build.need_attention())
    
    def test_should_return_this_build_date_if_current_build_passed(self):
        build = Build()
        build.is_passed  = True
        build.last_pass  = datetime(2009, 10, 11, 20, 11, 49);
        build.last_build = datetime(2009, 10, 12, 20, 11, 49);
        build.start_time = datetime(2009, 10, 13, 20, 11, 49);
        self.assertEquals(build.start_time, build.find_last_pass())
        
    def test_should_return_last_build_date_if_current_build_failed(self):
        build = Build()
        build.is_passed = False
        build.last_pass = datetime(2009, 10, 11, 20, 11, 49);
        build.last_build = datetime(2009, 10, 12, 20, 11, 49);
        build.start_time = datetime(2009, 10, 13, 20, 11, 49);
        self.assertEquals(build.last_pass, build.find_last_pass())
        
    def test_should_print_last_pass_time_if_current_build_is_broken(self):
        build = Build()
        build.is_passed = False
        build.last_pass = datetime.now() - timedelta(hours=3) 
        build.last_build = datetime.now() - timedelta(hours=2)
        build.start_time = datetime.now() - timedelta(hours=1)
        self.assertEquals('3 Hours', build.last_pass_t())
    
    def test_should_print_start_time_if_current_build_is_passed(self):
        build = Build()
        build.is_passed = True
        build.last_pass = datetime.now() - timedelta(hours=3) 
        build.last_build = datetime.now() - timedelta(hours=2)
        build.start_time = datetime.now() - timedelta(hours=1)
        self.assertEquals('1 Hours', build.last_pass_t())

    def test_should_parse_the_commitor_from_the_files(self):
        build = Build.from_file(self.root + '/analyse/tests/fixtures/cclive-release-jdk1.5/log20080922021338.xml')
        self.assertEqual(6, len(build.commits))
        self.assertEqual(True, Commit('jfredrick', '4006') in build.commits)
        self.assertEqual(True, Commit('jfredrick', '4007') in build.commits)
        self.assertEqual(True, Commit('jfredrick', '4008') in build.commits)
        self.assertEqual(True, Commit('bhamail', '4009') in build.commits)
        self.assertEqual(True, Commit('jfredrick', '4010') in build.commits)
        self.assertEqual(True, Commit('jfredrick', '4011') in build.commits)

    def test_should_parse_no_commitor_if_user_forces_build(self):
        build = Build.from_file(self.ccroot + '/log20091011173922Lbuild.1.xml')
        self.assertEqual(0, len(build.commits))
    
