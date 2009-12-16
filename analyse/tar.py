from analyse.config import Config, Configs
import os
import tarfile

class Tar:
    def __init__(self, configs):
        self.configs = configs
    
    def create(self):
        result_dir = self.configs.results_dir()
        tar = tarfile.open(os.path.join(result_dir, 'all.tar'), "w")

        for config in self.configs:
            project_folder = os.path.join(result_dir, config[0])
            csv = os.path.join(project_folder, config[0] + '.csv')
            if os.path.exists(csv):
                tar.add(csv, config[0] + '.csv')
        tar.close()