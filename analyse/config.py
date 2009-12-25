import os                                                  
from django.conf import settings
import ConfigParser

class Configs:
    def __init__(self, config_dir = None):
        configs = config_dir
        if None ==  configs :            
            configs = os.environ.get("CONFIGS_DIR")
        if None == configs :
            configs = os.path.join(settings.PROJECT_DIR, 'configs')
        self.config_dir = configs
        self.configs = {}
        for file in os.listdir(self.config_dir):
            names = os.path.splitext(file)
            if names[1] == '.cfg':
                id = names[0]
                self.configs[id] = Config(os.path.join(self.config_dir, file))

    def abspath(self):
        return os.path.abspath(self.config_dir)                                        

    def find(self, id):
        if id == None :
            return self.configs.items()[0][1]
        else :
            return self.configs[id]

    def is_empty(self):
        return len(self.configs) == 0

    def size(self):
        return len(self.configs)

    def results_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'results')

    def items(self):
        items = self.configs.items()
        items.sort()
        return items

    def get(self, key):
        return self.configs.get(key)

        
    def __iter__(self):
        items = self.configs.items()
        items.sort()
        return items.__iter__()
    
    def __getitem__(self, key):
        return self.configs.__getitem__(key)

    def __str__( self ):
            return 'the configs dir location is [' + self.config_dir + ']'
    
class Config:
    DEFAULT_FILES_TO_PROCESS = 30
    DEFAULT_DAYS_TO_PROCESS = 14
    DEFAULT_INTERVAL = 600
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.id = os.path.splitext(os.path.split(config_file)[1])[0]
                
    def abspath(self):
        return os.path.abspath(self.config_file)                                        
    
    def exist(self):
        return os.path.exists(self.abspath())
    
    def logdir(self): 
        def anonymous(config): return config.get('Basic', 'logdir', 0)
        return self.__readattr__(anonymous)
    
    def logfile(self, name):
        return os.path.join(self.logdir(), name)

    def days(self):
        def anonymous(config): 
            try:                                        
                return config.getint('Basic', 'days')
            except Exception, e:
                return Config.DEFAULT_DAYS_TO_PROCESS
        return self.__readattr__(anonymous)

    def csv_settings(self):
        def anonymous(config): return config.items("CSV")
        return self.__readattr__(anonymous) 
    
    def csv_keys(self):
        settings = self.csv_settings()
        array = []
        for setting in settings :
            array.append(setting[0])
        return array

    def plugins(self):
        default = ['build_time.py', 'label.py']

        def anonymous(config): 
            try:                                        
                plugins = config.get('CSV', 'plugins')
                splits = plugins.split(',')
                results = []
                for part in splits:
                    results.append(part.strip())
                results.extend(default)
                results.sort()
                return results
            except Exception, e:
                return default
        return self.__readattr__(anonymous)

    def results_dir(self):
        return os.path.join(settings.PROJECT_DIR, 'results')

    def result_dir(self):
       return os.path.join(self.results_dir(), self.id)

    def has_result(self):
        if not os.path.exists(self.result_dir()) :
             return False

        total_generated_json_files = 4        
        return len(os.listdir(self.result_dir())) >= total_generated_json_files

    def status(self):
        if self.has_result() :
            return 'OK'
        else :
            return 'MISSING REPORTS'

    def __readattr__(self, func):
       config = ConfigParser.ConfigParser()
       config.read(self.abspath())
       return func(config)

    def content(self):
       return open(self.config_file).read()
    
    def latest_log(self):
        files = os.sort_by_rule(self.logdir(),"log([0-9]*).*.xml", 'desc')
        return os.path.join(self.logdir(), files[0])
        
    def __str__( self ):
        return 'the config file location is [' + self.config_file + ']'
            
    def __eq__(self, other):
        if self != None and other != None:
            return self.id == other.id
        else:
            return False