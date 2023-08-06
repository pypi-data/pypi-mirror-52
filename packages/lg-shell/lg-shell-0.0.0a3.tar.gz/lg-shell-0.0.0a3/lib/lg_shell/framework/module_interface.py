from abc import ABCMeta, abstractmethod

class ModuleInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, args):
        raise NotImplementedError

    @abstractmethod
    def get_name(self):
        raise NotImplementedError

    @abstractmethod
    def add_module_to_parser(self, subparser):
        raise NotImplementedError