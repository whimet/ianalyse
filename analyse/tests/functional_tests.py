from django.test import TestCase
from analyse.tests.testutil import TestUtils
from django.test.client import Client
import re

class FunctionalTests(TestCase):

    def setUp(self):
        self.test_utils = TestUtils()
        self.test_utils.cleanup_results()

    def tearDown(self):
        self.test_utils.cleanup_results()
        self.test_utils.rename_bak_to_conf()

    def test_user_should_be_able_to_setup_the_application(self):
        user = User()
        user.open_home_page()
        self.assertContains(user.response, 'Missing Data')
        user.open_show_page('connectfour4')
        self.assertContains(user.response, 'MISSING REPORT')
        self.assertContains(user.response, user.found_config_file_location())
        user.generates_reports_for('connectfour4')

        user.open_setup_page('connectfour4')
        self.assertContains(user.response, 'OK')

        user.downloads_build_times_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_csv()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_pass_rate_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_per_build_time_data()
        self.assertEquals(True, user.can_visit_resource())
    
    def test_user_should_be_able_to_request_with_project_id(self):
        user = User()
        user.open_home_page()
        self.assertContains(user.response, 'Missing Data')
        user.open_show_page('cclive')       
        self.assertContains(user.response, 'MISSING REPORT')
        self.assertContains(user.response, user.found_config_file_location())
        user.generates_reports_for('cclive')

        user.open_setup_page('cclive')
        self.assertContains(user.response, 'OK')
        
        user.open_show_page('cclive')

        self.assertContains(user.response, '4 runs')
        self.assertContains(user.response, '0.00%')
        self.assertContains(user.response, '399.5(s)')
        user.downloads_build_times_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_csv()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_pass_rate_data()
        self.assertEquals(True, user.can_visit_resource())
        user.downloads_per_build_time_data()
        self.assertEquals(True, user.can_visit_resource())
    
    def test_user_should_not_wait_for_re_generating_the_data_when_referesh_the_page(self):
       user = User()
       self.test_utils.rename_conf_to_bak()
       user.open_home_page()
       self.assertContains(user.response, 'Opps! seems you did not create any config file')

       self.test_utils.rename_bak_to_conf()
       user.open_home_page()
       self.assertContains(user.response, 'cclive')
       self.assertContains(user.response, 'connectfour4')
       
    def test_should_print_hint_on_the_screen_when_user_first_time_uses_software(self):
       user = User()
       user.open_home_page()
       self.assertContains(user.response, 'Missing Data')
    
    def test_user_can_find_which_project_might_go_wrong(self):
        user = User()
        user.generates_reports_for('connectfour4')
        user.open_home_page()
        self.assertEquals(True, user.noticed_warning_icon('connectfour4'))
        
        user.open_show_page('connectfour4')
        self.assertEquals('More than 1 month', user.found_last_build_happened_at())
        self.assertEquals('More than 1 month', user.found_last_pass_happened_at())

    def test_user_can_find_latest_status_for_each_project(self):
        user = User()
        user.generates_reports_for('connectfour4')
        user.open_home_page()
        self.assertEquals('failed', user.found_status_for('connectfour4'))
        self.assertEquals('failed', user.found_status_for('cclive-release-jdk1.5'))
        self.assertEquals('passed', user.found_status_for('acc-srv'))
        
        
        
class User :
    def __init__(self):
        self.client = Client()
        
    def open_home_page(self):
        self.response = self.client.get('/analyse/index.html', follow=True)

    def open_show_page(self, id):
        self.response = self.client.get('/analyse/show.html?id=' + id, follow=True)

    def open_setup_page(self, id):
        self.response = self.client.get('/analyse/setup.html?id=' + id, follow=True)
    
    def found_config_file_location(self):
        return self.response.context['current'].abspath()
    
    def found_pass_rate(self):
        return self.response.context['config_file']
    
    def generates_reports_for(self, id):
        self.response = self.client.post('/analyse/generate.html', {'id' : id}, follow=True)
        self.project_id = id
    
    def downloads_build_times_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/build_times.txt')
        
    def downloads_csv(self):
        self.response = self.client.get('/results/' + self.project_id + '/' + self.project_id + '.csv')
        
    def downloads_pass_rate_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/pass_rate.txt')        

    def downloads_per_build_time_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/per_build_time.txt')
        
    def downloads_successful_rate_data(self):
        self.response = self.client.get('/results/' + self.project_id + '/successful_rate.txt')        

    def can_visit_resource(self):
        code = self.response.status_code
        return code >= 200 and code < 300

    def found_status_for(self, project_id):
        if self.response.content.find('id="now_passed_' + project_id + '"') > -1 :
            return 'passed'
        else:
            return 'failed'

    def noticed_warning_icon(self, project_id):
        return self.response.content.find('id="warning_' + project_id + '"') > -1
        
    def found_last_pass_happened_at(self):
        prog = re.compile('.*class="last_pass_at".*>(.*)</span>.*', re.M)
        matched = prog.search(self.response.content)
        if matched == None:
            return ''
        else:
            return matched.group(1)

    def found_last_build_happened_at(self):
        prog = re.compile('.*class="last_build_at".*>(.*)</span>.*', re.M)
        matched = prog.search(self.response.content)
        if matched == None:
            return ''
        else:
            return matched.group(1)

