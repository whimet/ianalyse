import os                                                  
from django.conf import settings
import ConfigParser

class Groups:
    def __init__(self, config_dir = None):
        self.groups = {}
        configs = config_dir
        if None ==  configs :            
            configs = os.environ.get("CONFIGS_DIR")
        if None == configs :
            configs = os.path.join(settings.PROJECT_DIR, 'configs')
        self.config_dir = configs
        groups_cfg = os.path.join(self.config_dir, 'groups.cfg')
        if os.path.exists(groups_cfg):
            config = ConfigParser.ConfigParser()
            config.read(groups_cfg)
            items = config.items("GROUPS")
            for item in items:
                splits = item[1].split(',')
                results = []
                for part in splits:
                    results.append(part.strip())
                self.groups[item[0]] = Group(self.config_dir, results, group_id=item[0])

        self.groups['default'] = Group(self.config_dir, group_id='default')            

    def __getitem__(self, index):
        return self.groups.items()[index]

    def __len__(self):
        return len(self.groups)
    
    def __iter__(self):
        items = self.groups.items()
        items.sort()
        return items.__iter__()
        
    def find(self, key):
        configs = self.groups.get(key)
        if configs == None:
            configs = self.groups.get('default')
        return configs

    def default(self):
        return self.groups['default']

    def exists(self, key):
        configs = self.groups.get(key)
        return configs != None

    def is_empty(self):
        configs = self.default()
        return configs.is_empty()

class Group:
    def __init__(self,  config_dir = None, file_patterns = [], group_id=None):
        self.id = group_id
        configs = config_dir
        if None ==  configs :            
            configs = os.environ.get("CONFIGS_DIR")
        if None == configs :
            configs = os.path.join(settings.PROJECT_DIR, 'configs')
        self.config_dir = configs
        self.configs = {}
        for file in os.listdir(self.config_dir):
            names = os.path.splitext(file)
            if file_patterns == [] and names[1] == '.cfg' and file != 'groups.cfg':
                self.configs[names[0]] = Config(os.path.join(self.config_dir, file))
            if file_patterns != [] and file_patterns.__contains__(file):
                self.configs[names[0]] = Config(os.path.join(self.config_dir, file))                


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

    def __len__(self):
        return len(self.configs)

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
        default = ['project_name.py', 'label.py', 'build_time.py']

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