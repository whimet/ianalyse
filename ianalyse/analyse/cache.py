from analyse.models import *


class Cache:
    _instance = None
    
    def __init__(self):
        self.project_groups = None

    def find(self, project_id):
        return self.project_groups.find('default').find(project_id)

    def refresh(self, config = None):
        builds = Builds.create_builds(config, None)
        self.project_groups.find('default').append(config.id, builds)
        builds.gen_all_reports()

    def get_project_group(self, groups):
        if Cache._instance.project_groups == None:
            Cache._instance.populate()
        return Cache._instance.project_groups.find(groups)

    def populate(self):
        Cache._instance.project_groups = ProjectGroups.create()

    @staticmethod
    def INSTANCE():
        if Cache._instance == None:
            Cache._instance = Cache()
        
        return Cache._instance

