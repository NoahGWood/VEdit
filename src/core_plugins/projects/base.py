import os
from shutil  import rmtree
from tempfile import gettempdir
from zipfile import ZipFile
from configparser import ConfigParser

class Project:
    def __init__(self, prompt=None):
        self.configs = ConfigParser()
        self.settings = None
        self.title = 'New Project'
        self.fname = "New Project.vedit"
        self.tmp = os.path.join(gettempdir(), '.vedit')
        if prompt:
            self.prompt = prompt

    def setup(self):
        if os.path.exists(self.tmp):
            self.prompt('old_project')
            
    def rm_old_project(self):
        print("Deleting old project")
        rmtree(self.tmp)

    def load_old_project(self):
        print("Loading old project")
        self._get_project_settings()

    def load_project(self, fname=None):
        if fname == None:
            fname = self.fname
        # Unzip folder into tmp directory
        os.mkdir(self.tmp)
        with ZipFile(fname, 'r') as zip_ref:
            zip_ref.extractall(self.tmp)

        # load project settings
        self._get_project_settings()

    def _get_project_settings(self):
        self.settings = os.path.join(self.tmp, 'settings.ini')
        if os.path.exists(self.settings):
            self.configs.read(self.settings)

    def _save_project_settings(self):
        with open(self.settings, 'w') as f:
            self.configs.write(f)

    def save_project(self):
        # save project settings
        self._save_project_settings()

        with ZipFile(self.fname, 'w') as zip_ref:
            for folderName, subFolders, filenames in os.walk(self.tmp):
                for filename in filenames:
                    # Create complete filepath of file in directory
                    filePath=os.path.join(folderName, filename)
                    # Safe to zip file
                    zip_ref.write(filePath, os.path.basename(filePath))