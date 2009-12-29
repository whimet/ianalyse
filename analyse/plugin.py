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
    def columns(self, config):
        names = []
        for defined_plugin in config.plugins():
            plugin = self.find_plugin(defined_plugin)
            plugin.append_column_name_to(names)
        return names
        

    def find_plugin(self, key):
        plugin = self.plugins.get(key)
        if plugin == None:
            plugin = NullPlugin(key)
        return plugin

    def multiple_handlers(self, config):
        all_plugins = self.plugins.values();
        handlers = []
        for defined_plugin in config.plugins():
            plugin = self.find_plugin(defined_plugin)
            plugin.append_handler_to(handlers)
        return MultiplePluginHandlers(handlers)

    def handle(self, input, config):
        handlers = self.multiple_handlers(config)
        parse(input, handlers)
        result = []
        for defined_plugin in config.plugins():
            plugin = self.find_plugin(defined_plugin)
            plugin.append_csv_cell_to(result)
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

    def append_handler_to(self, handlers):
        handlers.append(self.handler)

    def append_csv_cell_to(self, result):
        result.append(self.handler.csv_cell())

    def append_column_name_to(self, names):
        names.append(self.column_name)    

class NullPlugin(Plugin):
    def __init__(self, file_name):
        self.file_name = file_name

    def append_handler_to(self, handlers):pass

    def append_csv_cell_to(self, result):pass
    
    def append_column_name_to(self, names):pass
    