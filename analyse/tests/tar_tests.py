from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Groups
from analyse.models import ProjectGroup
from analyse.tar import Tar
from analyse.tests.testutil import TestUtils


class TarTests(TestCase):   
    def setUp(self):
        self.utils = TestUtils()
        self.configs = Groups().default()
        self.tar_file = os.path.join(self.configs.results_dir(), 'all.tar')
        if os.path.exists(self.tar_file):
            os.remove(self.tar_file)
        os.rmdir_p(self.configs.results_dir())
        os.rmdir_p(self.utils.temp_dir())

    def tearDown(self):
        if os.path.exists(self.tar_file):
            os.remove(self.tar_file)
        os.rmdir_p(self.configs.results_dir())
        os.rmdir_p(self.utils.temp_dir())
         
    def test_should_generate_tar_file_with_all_csvs(self):
        self.assertEquals(False, os.path.exists(self.tar_file))
        pg = ProjectGroup.create('default', self.configs)

        tar = Tar(self.configs)

        tar.create()
        self.assertEquals(True, os.path.exists(os.path.join(self.configs.results_dir(), 'all.tar')))
        self.utils.extract_tar(os.path.join(self.configs.results_dir(), 'all.tar'), self.utils.temp_dir())
        files = os.list_matched_files(self.utils.temp_dir(), ".*")
        self.assertEquals(4, len(files))
        