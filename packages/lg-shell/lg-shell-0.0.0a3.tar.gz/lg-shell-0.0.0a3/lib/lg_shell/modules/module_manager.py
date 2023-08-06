import argparse
from .module_factory import ModuleFactory
import logging


class ModuleManager:
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(description='lgshell - a CLI for easy system setup')
        self.subparser = self.parser.add_subparsers(dest='module_name')
        self.modules = ModuleFactory.create_modules(self.subparser)
        self.parsed_args = False

    def parse_args(self):
        self.args = self.parser.parse_args()

    def run(self):
        # assure arguments are parsed
        if (self.parsed_args == False):
            self.parse_args()

        # run appropriate module
        try:
            self.modules[self.args.module_name].run(self.args)
        except KeyError:
            logging.error('module <{}> not found - see -h for help'.format(self.args.module_name))
            return 1

        else:
            logging.info("Done")
            return 0
