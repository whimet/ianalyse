from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config, Configs
from analyse.tests.testutil import TestUtils

class ConfigsTests(TestCase):
    def setUp(self):
        self.configs_root = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))
        self.configs = Configs(self.configs_root)
        
    def tearDown(self):
        pass
        
    def testShouldReturnTheConfigFilesUnderConfigsRoot(self):
        self.assertEquals(len(os.listdir(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))), self.configs.size())
        self.assertEquals(os.path.join(self.configs_root, 'ianalyse.cfg'), self.configs['ianalyse'].config_file)
        self.assertEquals(os.path.join(self.configs_root, 'no_days.cfg'), self.configs['no_days'].config_file)
        
    def testShouldReturnTheFirstConfigWhenNoIdProvided(self):
        self.assertEquals(os.path.join(self.configs_root, 'ianalyse.cfg'), self.configs.find(None).config_file)

    def testShouldReturnTheConfigEqualWithId(self):
        self.assertEquals(os.path.join(self.configs_root, 'no_days.cfg'), self.configs.find('no_days').config_file)

    def testShouldOrderTheConfigByName(self):
        configs = Configs()
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
		