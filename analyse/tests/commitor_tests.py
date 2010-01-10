from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.models import *
from analyse.tests.testutil import TestUtils

class CommitorTests(TestCase):
    def test_should_return_0_passed_count_if_there_is_no_commit(self):
        commitor = Commitor('David')
        self.assertEquals(0, commitor.passed_count())

    def test_should_return_0_failed_count_if_there_is_no_commit(self):
        commitor = Commitor('David')
        self.assertEquals(0, commitor.failed_count())

    def test_should_return_0_as_max_count_if_there_is_no_commit(self):
        commitor = Commitor('David')
        self.assertEquals(0, commitor.total())
        
    def test_should_return_2_pass_count(self):
        commitor = Commitor('David')
        commitor.add(Commit('David', '4'), True)
        commitor.add(Commit('David', '5'), True)
        commitor.add(Commit('David', '6'), False)
        self.assertEquals(2, commitor.passed_count())
        
    def test_should_return_1_failed_count(self):
        commitor = Commitor('David')
        commitor.add(Commit('David', '4'), True)
        commitor.add(Commit('David', '5'), True)
        commitor.add(Commit('David', '6'), False)
        self.assertEquals(1, commitor.failed_count())

    def test_should_return_3_as_total_count(self):
        commitor = Commitor('David')
        commitor.add(Commit('David', '4'), True)
        commitor.add(Commit('David', '5'), True)
        commitor.add(Commit('David', '6'), False)
        self.assertEquals(3, commitor.total())
