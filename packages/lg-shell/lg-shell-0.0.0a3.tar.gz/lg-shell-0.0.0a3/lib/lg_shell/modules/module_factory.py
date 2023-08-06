from .config import Config
from .install import Install
from .setup import Setup
from .update import Update


class ModuleFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_modules(subparser):
        modules = {
            'install': Install(subparser),
            'config': Config(subparser),
            'setup': Setup(subparser),
            'update': Update(subparser),
        }

        return modules