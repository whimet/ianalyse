from analyse.config import *
import os
import tarfile

class Tar:
    def __init__(self, group):
        self.group = group
    
    def create(self):
        result_dir = self.group.results_dir()
        tar = tarfile.open(os.path.join(result_dir, 'all.tar'), "w")

        for config in self.group:
            project_folder = os.path.join(result_dir, config[0])
            csv = os.path.join(project_folder, config[0] + '.csv')
            if os.path.exists(csv):
                tar.add(csv, config[0] + '.csv')
        tar.close()