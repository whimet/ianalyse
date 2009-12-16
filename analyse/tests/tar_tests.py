from django.test import TestCase
import os                                                  
from django.conf import settings
from analyse.config import Config, Configs
from analyse.models import ProjectGroup
from analyse.tar import Tar
from analyse.tests.testutil import TestUtils


class TarTests(TestCase):   
    def setUp(self):
        self.utils = TestUtils()
        self.configs = Configs()

    def tearDown(self):
        os.rmdir_p(self.configs.results_dir())
        os.rmdir_p(self.utils.temp_dir())
         
    def test_should_generate_tar_file_with_all_csvs(self):
        ProjectGroup.create()

        tar = Tar(self.configs)

        self.assertEquals(False, os.path.exists(os.path.join(self.configs.results_dir(), 'all.tar')))
        tar.create()
        self.assertEquals(True, os.path.exists(os.path.join(self.configs.results_dir(), 'all.tar')))
        self.utils.extract_tar(os.path.join(self.configs.results_dir(), 'all.tar'), self.utils.temp_dir())
        files = os.list_matched_files(self.utils.temp_dir(), ".*")
        self.assertEquals(4, len(files))
        