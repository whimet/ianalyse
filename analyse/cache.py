from analyse.models import Build, Builds, ProjectGroup
from analyse.config import Config, Configs

class Cache:
    _instance = None
    
    def __init__(self):
        self.project_group = None

    '''this is a singleton class'''
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
            
    def refresh(self, config = None):
        self.project_group.append(config.id, Builds.create_builds(config, None))
        Builds.gen_all_reports(config.id)

    def find(self, project_id):
        return self.project_group.find(project_id)

    def get_project_group(self):
        if self.project_group == None:
            self.populate()
            
        return self.project_group

    def populate(self):
        self.project_group = ProjectGroup.create()

Cache().populate()