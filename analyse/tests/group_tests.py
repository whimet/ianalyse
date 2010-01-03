from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import *
from analyse.tests.testutil import TestUtils

class GroupTests(TestCase):
    def setUp(self):
        self.configs_root = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))
        self.configs = Group(self.configs_root)
        
    def tearDown(self):
        if os.path.exists(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/groups.bak')):
            TestUtils().rename_bak_to_conf('groups.bak')
        
    def test_should_return_the_config_files_under_configs_root(self):
        self.assertEquals(len(os.listdir(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))) - 1, self.configs.size())
        self.assertEquals(os.path.join(self.configs_root, 'ianalyse.cfg'), self.configs['ianalyse'].config_file)
        self.assertEquals(os.path.join(self.configs_root, 'no_days.cfg'), self.configs['no_days'].config_file)
        
    def test_should_return_the_first_config_when_no_id_provided(self):
        self.assertEquals(os.path.join(self.configs_root, 'ianalyse.cfg'), self.configs.find(None).config_file)

    def test_should_return_the_config_equal_with_id(self):
        self.assertEquals(os.path.join(self.configs_root, 'no_days.cfg'), self.configs.find('no_days').config_file)

    def test_should_load_the_project_groups_information(self):
        groups = Groups(self.configs_root)
        self.assertEquals(3, len(groups))

    def test_should_load_the_default_configs_when_group_id_cannot_be_found(self):
        groups = Groups(self.configs_root)
        configs = groups.find('not_exist')
        default_configs = groups.find('default')
        self.assertEquals(len(configs), len(default_configs))

    def test_should_order_the_groups_by_name(self):
        group = Groups(self.configs_root)[0]
        self.assertEquals('acc', group[0])
        group = Groups(self.configs_root)[1]
        self.assertEquals('default', group[0])
        group = Groups(self.configs_root)[2]
        self.assertEquals('others', group[0])

    def test_should_return_the_default_group_if_there_is_no_groups_defined(self):
        TestUtils().rename_conf_to_bak('groups.cfg')
        groups = Groups()
        group = groups[0]
        self.assertEquals('default', group[0])
        self.assertEquals(1, len(groups))

    def test_should_order_the_config_by_name(self):
        configs = Group()
        configs_hash = {
        	'safe' : Config('safe'),
        	'acc_ci_commit' : Config('acc_ci_commit'),
        	'acc_ci_all' : Config('acc_ci_all'),
        	'l3' : Config('l3')
        }
        configs.configs = configs_hash
        items = configs.items()
        self.assertEquals('acc_ci_all', items[0][0]);
        self.assertEquals('acc_ci_commit', items[1][0]);
        self.assertEquals('l3', items[2][0]);
        self.assertEquals('safe', items[3][0]);
		