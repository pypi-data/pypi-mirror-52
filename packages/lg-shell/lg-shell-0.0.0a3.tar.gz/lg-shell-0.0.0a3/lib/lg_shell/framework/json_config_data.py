from .abstract_config_data import AbstractConfigData
import json


class JsonConfigData(AbstractConfigData):
    def __init__(self, path):
        super().__init__(path)

    def load(self, path):
        self.path  = path
        with open(path, 'r') as fp:
            self.data = json.load(fp)

    def save(self):
        with open(self.path, 'w') as fp:
            json.dump(self.data, fp)

