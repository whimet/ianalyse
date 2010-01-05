from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import *


class ConfigTests(TestCase):   
    original = os.environ["CONFIGS_DIR"]
    
    def setUp(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/ianalyse.cfg')))
        
    def tearDown(self):
         project1 = self.config.result_dir()
         if os.path.exists(project1) :
            os.rmdir_p(project1)
         os.environ["CONFIGS_DIR"] = ConfigTests.original
         
    def testShouldReturnTheAbsolutePathOfTheDefaultConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'configs'))
        os.environ.pop("CONFIGS_DIR")
        config = Group()
        self.assertEquals(expected, config.abspath())

    def testShouldReturnSpecificConfigFile(self):
        expected = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/'))
        config = Group(expected)
        self.assertEquals(expected, config.abspath())
    
    def testShouldReturnFalseWhenConfigFileIsMissing(self):
        not_exist_file = os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/not.exist.cfg'))
        self.assertEquals(False, Config(not_exist_file).exist())
	  
    def testShouldReadTheLogDir(self):
        self.assertEquals('/var/logs', self.config.logdir())
	
    def testShouldReturnNDaysIfDefined(self):
        self.assertEquals(3, self.config.days())
	
    def testShouldReturn30BuildsAsDefaultValue(self):
        self.config = Config(os.path.abspath(os.path.join(settings.PROJECT_DIR, 'analyse/tests/fixtures/config/no_days.cfg')))
        self.assertEquals(14, self.config.days())


    def testShouldReturnTrueIfAllResultsJsonGenerated(self):
        project1 = self.config.result_dir()
				
        os.touch(os.path.join(project1, 'build_times.txt'))
        os.touch(os.path.join(project1, 'pass_rate.txt'))
        os.touch(os.path.join(project1, 'per_build_time.txt'))
        os.touch(os.path.join(project1, 'successful_rate.txt'))
        
        self.assertEquals(True, self.config.has_result())


    def testShouldReturnFalseIfAnyResultJsonIsMissing(self):
        project1 = self.config.result_dir()
        os.makedirs_p(project1)
        os.touch(os.path.join(project1, 'pass_rate.txt'))
        self.assertEquals(False, self.config.has_result())        


    def testShouldReturnFalseIfAnyResultJsonGenerated(self):
        self.assertEquals(False, self.config.has_result())
        
    def testShouldReturnTrueIfConfigIDAreSame(self):
        config1 = Config("")
        config1.id = 'id'
        config2 = Config("")
        config2.id = 'id'
        self.assertEquals(True, config1 == config2)
        
    def testShouldReturnFalseIfConfigIDAreNotSame(self):
        config1 = Config("")
        config1.id = 'id1'
        config2 = Config("")
        config2.id = 'id2'
        self.assertEquals(False, config1 == config2)
        
    def test_should_return_all_the_plugins_under_the_plugins_folder_as_default_plugins(self):
        config = Config("")
        list = config.plugins()
        self.assertEquals(7, len(list))
        self.assertEquals(True, list.count('build_time.py') == 1)
        self.assertEquals(True, list.count('label.py') == 1)
        self.assertEquals(True, list.count('last_build.py') == 1)
        self.assertEquals(True, list.count('last_passed.py') == 1)
        self.assertEquals(True, list.count('project_name.py') == 1)
        self.assertEquals(True, list.count('result.py') == 1)
        self.assertEquals(True, list.count('start_at.py') == 1)
        
    def test_should_return_plugins_in_the_same_order_as_user_defined(self):
        plugins = self.config.plugins()

        self.assertEquals(len(plugins), 3)
        self.assertEquals('my_plugin.py', plugins[0])
        self.assertEquals('my_plugin2.py', plugins[1])
        self.assertEquals('my_plugin3.py', plugins[2])
    


        
        
        
        