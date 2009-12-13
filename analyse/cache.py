from analyse.models import Build, Builds
from analyse.config import Config, Configs

class Cache:
    def __init__(self):
        self.builds = {}
        self.latest_builds = {}

    def refresh(self, config = None, over_all_result={}):
        if config == None:
            self.latest_builds = Builds.latest_builds(Configs())
        else:
            self.latest_builds = Builds.latest_builds(Configs())
            self.builds[config.id] = Builds.create_builds(config, None, config.builds())
            Build.analyse_all(config.id, over_all_result)
            Builds.create_csv(config.id)

    def find(self, project_id):
        return self.builds.get(project_id)

    def get_latest_builds(self):
        if self.latest_builds == {}:
            self.latest_builds = Builds.latest_builds(Configs())
            
        return self.latest_builds