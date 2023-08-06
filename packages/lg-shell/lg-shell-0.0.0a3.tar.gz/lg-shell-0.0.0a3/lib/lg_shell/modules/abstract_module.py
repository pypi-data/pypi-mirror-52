from ..framework.module_interface import ModuleInterface
from ..framework.json_config_data import JsonConfigData
import os


class AbstractModule(ModuleInterface):

    def __init__(self, subparser):
        self.add_module_to_parser(subparser)
        path = os.path.expanduser('~') + '/.config/lg_shell/config.json'
        self.config_data = JsonConfigData(path)

    def add_module_to_parser(self, subparser):
        self.module_parser = subparser.add_parser(self.get_name())
