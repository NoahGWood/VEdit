#!/usr/bin/python3
import configparser
import os
from importlib.machinery import SourceFileLoader

class Core:
    def __init__(self, app_name="PluGUI", settings='settings.ini', plugin_folder='plugins'):
        self.app_name = app_name
        self.settings_file = settings
        self.plugin_folder = plugin_folder
        self.core_plugins = 'core_plugins' # DO NOT CHANGE
        self.configs = configparser.ConfigParser()
        self.default_plugins = []
        self.plugins = {}
        self.pre_update_functions = []
        self.update_functions = []
        self.post_update_functions = []

        self.player = None

        if os.path.exists(self.settings_file):
            self.configs.read(self.settings_file)
        else:
            self.generate_app_settings()

    def save_app_settings(self):
        with open(self.settings_file, 'w') as f:
            self.configs.write(f)

    def generate_app_settings(self):
        """Generates a settings.ini file based on plugins in folder"""
        if 'Plugins' not in self.configs.sections():
            # Generate core settings file
            self.configs.add_section('Plugins')
        for d in os.listdir(self.plugin_folder):
            if d not in self.configs['Plugins'].keys():
                self.add_app_setting('Plugins', d, str(True), save=False)
        # manually save to reduce unneeded read/writes
        self.save_app_settings()

    def register_update(self, func, when=0):
        """Used to register a function to be called
            each frame.

            when: int:
                when < 0 - Updates before frame
                when == 0 - Updates with frame
                when > 0 - Updates after frame
        """
        if when < 0:
            self.pre_update_functions.append(func)
        elif when == 0:
            self.update_functions.append(func)
        elif when > 0:
            self.post_update_functions.append(func)

    # Called before each frame
    def pre_update(self):
        for func in self.pre_update_functions:
            func()

    # Called after each frame
    def post_update(self):
        for func in self.post_update_functions:
            func()

    # Called each frame
    def update(self):
        self.pre_update()
        for func in self.update_functions:
            func()
        self.post_update()

    def get_app_settings(self, section, key=None):
        """Returns the app settings of a section or key value"""
        if not key:
            return self.configs[section]
        else:
            return self.configs[section][key]

    def add_app_setting(self, section, key, value, save=True):
        """Adds a setting to section, key, value of app settings"""
        if section not in self.configs.sections():
            self.configs.add_section(section)
        self.configs[section][key] = value
        if save:
            self.save_app_settings()

    def load_plugin(self, path, name):
        plg = SourceFileLoader(name, path).load_module().Plugin(parent=self)
        self.plugins[plg.name]=plg

    def load_plugins(self):
        # Load core plugins first
        cplgs = []
        with open('core_plugins/load_order.txt','r') as f:
            cplgs = f.readlines()
        for plugin in cplgs:
            plugin=plugin.strip()
            fp = os.path.join('core_plugins',plugin,plugin+'.py')
            self.load_plugin(fp, plugin)
            self.default_plugins.append(plugin)
        for plugin, enabled in self.configs['Plugins'].items():
            if enabled in ("True","true", "TRUE", "t", "enabled", "e"):
                fp = os.path.join(self.plugin_folder, plugin, plugin+'.py')
                self.load_plugin(fp, plugin)

        

if __name__ in '__main__':
    core = Core()
    core.load_plugins()
    core.plugins['gui'].main()
