from django.test import TestCase

from analyse.models import Build, Builds
import os
from django.conf import settings
from analyse.plugin import Plugins
from analyse.tests.testutil import TestUtils


class PluginsTests(TestCase):
    FAILED_LOG_AT_OCT_11 = '''<cruisecontrol>
      <modifications />
      <info>
        <property name="projectname" value="connectfour4" />
        <property name="lastbuild" value="20091011000000" />
        <property name="lastsuccessfulbuild" value="20091011000000" />
        <property name="builddate" value="2009-10-11T09:39:22" />
        <property name="cctimestamp" value="20091011173922" />
        <property name="label" value="build.1" />
        <property name="interval" value="300" />
        <property name="lastbuildsuccessful" value="true" />
        <property name="logdir" value="/Users/twer/Desktop/cruisecontrol-bin-2.8.2/logs/connectfour4" />
        <property name="logfile" value="log20091011173922.xml" />
      </info>
      <build time="1 minute(s) 0 second(s)">
        <target name="exec">
          <task name="echo">
            <message priority="info"><![CDATA[haha]]></message>
          </task>
        </target>
      </build>
    </cruisecontrol>'''
    
    
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
    
    def test_should_load_the_value_based_on_default_order_if_nothing_defined(self):
        file = TestUtils().write_to_temp('log20090909090.xml', PluginsTests.FAILED_LOG_AT_OCT_11)
        plugins = Plugins.INSTANCE(TestUtils().plugins())
        plugins.load_plugins()
        
        result = plugins.handle(file, TestUtils().connectfour_config())
        self.assertEquals('connectfour4', result[0])
        self.assertEquals('build.1', result[1])
        self.assertEquals('1 minute(s) 0 second(s)', result[2])

    def test_should_load_the_value_based_on_the_order_user_defined(self):
        file = TestUtils().write_to_temp('log20090909090.xml', PluginsTests.FAILED_LOG_AT_OCT_11)
        plugins = Plugins.INSTANCE(TestUtils().plugins())
        plugins.load_plugins()

        config = TestUtils().connectfour_config()
        config.plugins = self._user_defined_order
        result = plugins.handle(file, config)

        self.assertEquals('build.1', result[0])
        self.assertEquals('1 minute(s) 0 second(s)', result[1])
        self.assertEquals('connectfour4', result[2])

    def test_should_load_the_value_based_on_the_order_user_defined(self):
        file = TestUtils().write_to_temp('log20090909090.xml', PluginsTests.FAILED_LOG_AT_OCT_11)
        plugins = Plugins.INSTANCE(TestUtils().plugins())
        plugins.load_plugins()

        config = TestUtils().connectfour_config()
        config.plugins = self._file_is_missing
        result = plugins.handle(file, config)

        self.assertEquals(2, len(result))
        self.assertEquals('build.1', result[0])
        self.assertEquals('1 minute(s) 0 second(s)', result[1])


    def _user_defined_order(self):
        return ['label.py', 'build_time.py', 'project_name.py']

    def _file_is_missing(self):
        return ['label.py', 'build_time.py', 'missing.py']
