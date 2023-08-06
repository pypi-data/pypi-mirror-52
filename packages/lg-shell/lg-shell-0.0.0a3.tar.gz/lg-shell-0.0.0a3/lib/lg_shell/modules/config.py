from .abstract_module import AbstractModule

class Config(AbstractModule):
    def __init__(self, subparser):
        super(Config, self).__init__(subparser)

    def add_module_to_parser(self, subparser):
        super().add_module_to_parser(subparser)
        self.module_parser.add_argument('--cfg-file', dest='cfg_file', type=str, help="config file path for lgshell")
        self.module_parser.add_argument('-p', '--print', dest='print', action='store_true',
                                        help="print configs for lgshell")

    def run(self, args):
        if (args.print):
            print(self.config_data)

        self.config_data.save()

    def get_name(self):
        return 'config'
