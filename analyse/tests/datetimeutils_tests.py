from django.test import TestCase

from analyse.models import Build
import os
from util.datetimeutils import *
from django.conf import settings
from datetime import datetime,timedelta
import time

class DatetimeUtilsTest(TestCase):

    def setUp(self):
        self.root = settings.PROJECT_DIR

    def testShouldReturn3WeeksAndIgnoreHourMinutesSecondsFromSpecifiedTime(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")

        self.assertEquals(eighthSep, days_ago(21, thirtySep))

    def testShouldReturn3WeeksAgoIfSpecifyVeryOldDate(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")
        veryold = datetime.strptime("20080909000000", "%Y%m%d%H%M%S")

        self.assertEquals(eighthSep, days_ago_not_before(21, thirtySep, veryold))

    def testShouldReturnNow(self):
        thirtySep = datetime.strptime("20090930070001", "%Y%m%d%H%M%S")
        eighthSep = datetime.strptime("20090909000000", "%Y%m%d%H%M%S")
        quiteNew =  datetime.strptime("20090927013000", "%Y%m%d%H%M%S")

        self.assertEquals(quiteNew, days_ago_not_before(21, thirtySep, quiteNew))

    def testShouldEvaluateTheSecondsToSeconds(self):
        self.assertEquals(1, evaluate_time_to_seconds("0 minute(s) 1 second(s)"))

    def testShouldEvaluateTheMinutesToSeconds(self):
        self.assertEquals(61, evaluate_time_to_seconds("1 minute(s) 1 second(s)"))

    def testShouldEvaluateTheHoursToSeconds(self):
        self.assertEquals(3661, evaluate_time_to_seconds("1 hour(s) 1 minute(s) 1 second(s)"))
    
    def testShouldConvertTheStringTimeStampToTimeStampStartFrom1970(self):
        ccdate = datetime.strptime('20090909090909', "%Y%m%d%H%M%S")
        self.assertEquals(1252505349.0, to_unix_timestamp(ccdate))
        
        
    def testShouldReturnMoreThan1MonthAgoIfTimeDeltaIsGreatThan30Days(self):
        self.assertEquals("More than 1 month", time_delta_as_str(timedelta(days=31)))
        
    def testShouldReturn29DaysWhenTimeDeltaIs29Days(self):
        self.assertEquals("29 Days", time_delta_as_str(timedelta(days=29)))
        
    def testShouldReturn15HoursWhenTimeDeltaIs15Hours(self):
        self.assertEquals("15 Hours",  time_delta_as_str(timedelta(hours=15)))
        
    def testshouldReturnOneHourAgoIfTimeDeltaIsLessThanOneHour(self):
        self.assertEquals("Less than 1 hour", time_delta_as_str(timedelta(minutes=31)))
        