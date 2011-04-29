from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.models import *
from analyse.tests.testutil import TestUtils

class CommitorsTests(TestCase):
    def test_should_return_0_if_no_commitor_provided(self):
        commitor = Commitors()
        self.assertEquals(0, commitor.max())

    def test_should_return_total_commits_for_the_only_commitor(self):
        commitor = Commitors()
        commitor.add_commits([Commit('David', '14'), Commit('David', '15')], True)
        self.assertEquals(2, commitor.max())


    def test_should_return_max_commits_between_commitors(self):
        commitors = Commitors()
        commitors.add_commits([Commit('David', '14'), Commit('David', '15')
            ,Commit('Tom', '14'), Commit('David', '16')], True)
        self.assertEquals(3, commitors.max())

    def test_should_return_empty_commitor_when_request_name_does_exists(self):
        commitors = Commitors()
        self.assertEquals(True, None != commitors.find('David'))

    def test_should_return_commitor_when_request_name_exists(self):
        commitors = Commitors()
        commitors.add_commits([Commit('David', '14'), Commit('David', '15')], True)

        self.assertEquals(2, commitors.find('David').total())
    
    def test_should_return_all_names_from_commits(self):
        commitors = Commitors()
        commitors.add_commits([Commit('David', '14'), Commit('Chris', '15'), Commit('Tom', '15')], True)

        self.assertEquals(True, commitors.names().__contains__('David'))
        self.assertEquals(True, commitors.names().__contains__('Chris'))
        self.assertEquals(True, commitors.names().__contains__('Tom'))
