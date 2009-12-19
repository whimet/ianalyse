from analyse.models import Build, Builds, ProjectGroup
from analyse.config import Config, Configs

class Cache:
    _instance = None
    
    def __init__(self):
        self.project_group = None
            
    def refresh(self, config = None):
        builds = Builds.create_builds(config, None)
        self.project_group.append(config.id, builds)
        builds.gen_all_reports()

    def find(self, project_id):
        return self.project_group.find(project_id)

    def get_project_group(self):
        if Cache._instance.project_group == None:
            Cache._instance.populate()
            
        return Cache._instance.project_group

    def populate(self):
        Cache._instance.project_group = ProjectGroup.create()
    
    @staticmethod
    def INSTANCE():
        if Cache._instance == None:
            Cache._instance = Cache()
        
        return Cache._instance

