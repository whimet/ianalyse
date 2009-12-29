from django.test import TestCase

from analyse.models import Build, Builds
import os
from django.conf import settings
from analyse.plugin import Plugins
from analyse.tests.testutil import TestUtils

class PluginsTests(TestCase):
    def setUp(self):
        Plugins._instance = None

    def tearDown(self):
        Plugins._instance = None

    def test_should_load_all_plugin_from_plugins_folder(self):
        files = os.list_matched_files(os.path.join(settings.PROJECT_DIR, 'plugins'));
        count_of_init_py = 1
        count = len(files) - count_of_init_py

        plugins = Plugins.INSTANCE()
        plugins.load_plugins()
        self.assertEquals(count, len(plugins))

    def test_should_not_load_the_plugins_with_incorrect_syntax(self):
        plugins = Plugins.INSTANCE(TestUtils().plugins())
        plugins.load_plugins()
        self.assertEquals(3, len(plugins))

    def test_should_load_thebase_on_the_configs_i_defiend(self):
        plugins = Plugins.INSTANCE(TestUtils().plugins())
        plugins.load_plugins()
        self.assertEquals(3, len(plugins))

