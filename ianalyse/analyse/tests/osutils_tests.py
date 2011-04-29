from django.test import TestCase
import os              
import util.osutils                                     
from django.conf import settings

class OSUtilsTests(TestCase):                               
    def setUp(self):
        self.root = settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'
        
        
    def testShouldSortTheFilesBasedOnTheRuleAsc(self):
        files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml', 'asc')
        self.assertEquals(7, len(files))
        self.assertEquals('log20080624064201Lbuild.70.xml', files[0])
        self.assertEquals('log20080924062941.xml', files[6])

    def testShouldSortTheFilesBasedOnTheRuleDesc(self):
        files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml', 'desc')
        self.assertEquals('log20080924062941.xml', files[0])
        self.assertEquals('log20080923021338.xml', files[5])     
                                                             
    def testShouldSortTheFilesBasedOnTheRuleDesc(self):
        files = os.sort_by_rule(self.root, 'log([0-9]*).*.xml', 'desc')
        self.assertEquals('log20080924062941.xml', files[0])
        self.assertEquals('log20080922021338.xml', files[5])     

    def test_should_find_files_not_more_than_10_days(self):
        files = os.filter_by_days(self.root, 'log([0-9]*).*.xml', 10)
        self.assertEquals('log20080924062941.xml', files[5])
        self.assertEquals('log20080922021338.xml', files[0])     

    def test_should_find_files_not_more_than_2_days(self):
        files = os.filter_by_days(self.root, 'log([0-9]*).*.xml', 2)
        self.assertEquals('log20080922021338.xml', files[0])
        self.assertEquals('log20080924062941.xml', files[5])


    def test_should_find_files_not_more_than_1_day(self):
        files = os.filter_by_days(self.root, 'log([0-9]*).*.xml', 1)
        self.assertEquals('log20080924001513.xml', files[0])
        self.assertEquals('log20080924062941.xml', files[2])

    def test_should_find_files_not_more_than_1_day(self):
        files = os.filter_by_days(self.root, 'log([0-9]*).*.xml', None)
        self.assertEquals(0, len(files))
