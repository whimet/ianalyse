from django.test import TestCase
from analyse.models import *
import os
from django.conf import settings
from datetime import datetime
import django.test.testcases
try:
	NO_CJSON = False
	import cjson
except ImportError:
	NO_CJSON = True
	import json
from analyse.tests.testutil import TestUtils

class SuccessfulRateChartTests(TestCase):
    PATTERN = "log20091011173922Lbuild.1.xml|log20091013220324.xml"

    def setUp(self):
        self.root = settings.PROJECT_DIR
        self.ccroot = self.root + 'analyse/test/fixtures-1/connectfour4'

    def testGenerateTotalPassRate(self):
        builds = Builds.create_builds(TestUtils().connectfour_config(), SuccessfulRateChartTests.PATTERN);
        
        ndaysStat = NDaysStatistics(builds)
        json_str = ndaysStat.successful_rate()
        if NO_CJSON :
            json_obj = json.loads(json_str)
        else:
            json_obj = cjson.decode(json_str)

        self.assertEqual(2, len(json_obj['elements'][0]['values']));


