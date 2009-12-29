from analyse.config import Config
from django.db import settings
import os
import util.osutils
import tarfile

class TestUtils:
        
    def connectfour(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/connectfour4'

    def cclive_release_jdk(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/cclive-release-jdk1.5'        
    
    def plugins(self):
        return settings.PROJECT_DIR + '/analyse/tests/fixtures/plugins'
            
    def csv_settings(self):
        return [('project name', '//property[@name="projectname"]/@value'),
            ("label", '//property[@name="label"]/@value'),
            ('buid time', '//build/@time'),
            ('something wrong', '//not right')
            ]
    def twenty_days(self):
        return 20
    def one_day(self):
        return 1
        
        
    def connectfour_config(self):
        config = Config(settings.PROJECT_DIR + '/analyse/tests/fixtures/config/connectfour4.cfg')
        config.logdir = self.connectfour
        config.csv_settings = self.csv_settings 
        config.days = self.twenty_days
        return config
    
    def cclive_config(self):
        config = Config(settings.PROJECT_DIR + '/analyse/tests/fixtures/config/cclive.cfg')
        config.logdir = self.cclive_release_jdk
        config.csv_settings = self.csv_settings
        config.days = self.one_day
        return config
    
    def cleanup_results(self):
        results_dir = os.path.join(settings.PROJECT_DIR, 'results')
        if os.path.exists(results_dir) :
            os.rmdir_p(results_dir) 

    def last_modified_on(self, pj):
        results = {}
        results_dir = os.path.join(settings.PROJECT_DIR, 'results')
        result_dir = os.path.join(results_dir, pj)
        for file in os.listdir(result_dir):
            results[file] = os.path.getmtime(os.path.join(result_dir, file))
        return results
        
    def cleantemp(self):
        temp_dir = os.path.join(settings.PROJECT_DIR, 'temp')
        if os.path.exists(temp_dir):
            os.rmdir_p(temp_dir)
    
    def temp_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'temp')
    
    def write_to_temp(self, file, content):
        temp_dir = os.path.join(settings.PROJECT_DIR, 'temp')
        os.makedirs_p(temp_dir)
        temp_file = os.path.join(temp_dir, file)
        os.touch(temp_file)
        f = open(temp_file, 'w')
        f.write(content)
        return temp_file
    
    def rename_conf_to_bak(self):
        config_dir = os.path.join(settings.PROJECT_DIR, 'analyse/tests/configs/')
        for file in os.listdir(config_dir):
            base_name = os.path.splitext(file)[0]
            if file.endswith('.cfg'):
                os.rename(os.path.join(config_dir, file), os.path.join(config_dir, base_name + '.bak'))
        
    
    def rename_bak_to_conf(self):
        config_dir = os.path.join(settings.PROJECT_DIR, 'analyse/tests/configs/')
        for file in os.listdir(config_dir):
            base_name = os.path.splitext(file)[0]
            if file.endswith('.bak'):
                os.rename(os.path.join(config_dir, file), os.path.join(config_dir, base_name + '.cfg'))
    
    def extract_tar(self, tar_file, dest_dir):
        if os.path.exists(dest_dir):
            os.makedirs_p(dest_dir)

        if not os.path.exists(tar_file):
            raise Exception("i cannot find the tar file.")

        tar = tarfile.open(tar_file)
        tar.extractall(dest_dir)
        tar.close()

    def create_config_file(self, file_name, content):
        config_dir = os.path.join(settings.PROJECT_DIR, 'analyse/tests/configs/')
        config = os.path.join(config_dir, file_name)
        os.touch(config)
        f = open(config, 'w')
        f.write(content)
        return config
        
    def create_l3_support_config(self):
        content = '''
[Basic]
logdir: ./analyse/tests/fixtures/acc-srv
name: connectfour4

[CSV]
project name: //property[@name="projectname"]/@value
buid time: //build/@time
label: //property[@name='label']/@value
'''      
        return self.create_config_file('l3_support.cfg', content)
        
    
        