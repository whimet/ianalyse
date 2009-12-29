from xml.sax.handler import ContentHandler
from xml.sax import parse, parseString
from analyse.config import Config, Configs
from django.conf import settings
import os

class MultiplePluginHandlers(ContentHandler):
    def __init__(self, handles):
        self.handlers = handles

    def startElement(self, name, attrs):
        for handler in self.handlers :
            handler.startElement(name, attrs)
    
    def __iter__(self):
        return self.handlers.__iter__()

    def __getitem__(self, key):
        return self.handlers.__getitem__(key)

class Plugins:
    _instance = None

    def __init__(self, plugins_folder=None):
        self.plugins = {}
        self.current_plugin = None;
        self.plugins_folder = plugins_folder
        if plugins_folder == None:
            self.plugins_folder = os.path.join(settings.PROJECT_DIR, 'plugins');
    
    def load_plugins(self):        
        files = os.list_matched_files(self.plugins_folder);
        for file in files:
            self.current_plugin = Plugin(file)
            try:
                execfile(os.path.join(self.plugins_folder, file))
            except Exception, e:
                pass

    def multiple_handlers(self, config):
        all_plugins = self.plugins.values();
        handlers = []
        for defined_plugin in config.plugins():
            plugin = self.plugins.get(defined_plugin)
            if not plugin == None:
                handlers.append(plugin.handler)
        return MultiplePluginHandlers(handlers)

    def handle(self, input, config):
        handlers = self.multiple_handlers(config)
        parse(input, handlers)
        result = []
        for defined_plugin in config.plugins():
            plugin = self.plugins.get(defined_plugin)
            if not plugin == None:
                result.append(self.plugins.get(defined_plugin).handler.csv_cell())
        return result

    @staticmethod
    def register(column_name, handler):
        Plugins.INSTANCE()._register(column_name, handler)

    def _register(self, column_name, handler):
        self.current_plugin.update(column_name, handler)
        self.plugins[self.current_plugin.file_name]=self.current_plugin

    @staticmethod
    def INSTANCE(plugins_folder = None):
        if Plugins._instance == None:
            Plugins._instance = Plugins(plugins_folder)
            Plugins._instance.load_plugins()
        return Plugins._instance
    

    
    def __len__(self):
        return len(self.plugins)

    def clear(self):
        self.plugins.clear()

class Plugin:
    def __init__(self, file_name):
        self.file_name = file_name
        self.column_name = None
        self.handler = None
        
    def update(self, column_name, handler):
        self.column_name = column_name
        self.handler = handler

    
    
