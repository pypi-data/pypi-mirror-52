from abc import ABCMeta, abstractmethod

class ConfigDataInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self, path):
        raise NotImplementedError

    @abstractmethod
    def save(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def set(self, key):
        raise NotImplementedError