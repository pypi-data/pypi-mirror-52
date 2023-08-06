from .abstract_module import AbstractModule


class Update(AbstractModule):
    def __init__(self, subparser):
        super(Update, self).__init__(subparser)

    def add_module_to_parser(self, subparser):
        super().add_module_to_parser(subparser)

    def run(self, args):
        raise NotImplementedError

    def get_name(self):
        return "update"
