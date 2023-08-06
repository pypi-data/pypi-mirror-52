from .config_data_interface import ConfigDataInterface

class AbstractConfigData(ConfigDataInterface):

    def __init__(self, path):
        self.data = dict
        self.load(path)

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def print(self):
        print(self.data)

    def __str__(self):
        return self.data.__str__()
