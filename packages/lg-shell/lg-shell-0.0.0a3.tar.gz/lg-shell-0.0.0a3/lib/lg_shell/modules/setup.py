import logging
import os
import platform

from .abstract_module import AbstractModule
from .keyboard_manager import KeyboardManager


class Setup(AbstractModule):
    def __init__(self, subparser):
        super(Setup, self).__init__(subparser)
        self.lgsp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def add_module_to_parser(self, subparser):
        super().add_module_to_parser(subparser)
        self.module_parser.add_argument('--keyboard_vendor', type=str, dest='keyboard_vendor', help='keyboard vendor (apple / lenovo)')
        self.module_parser.add_argument('--keyboard_type', type=str, dest='keyboard_type', help='keyboard type (internal / external)')
        self.module_parser.add_argument('--keyboard_language', type=str, dest='keyboard_language', help='keyboard language (ch / us)')

    def run(self, args):
        keyboard_manager = KeyboardManager(self.lgsp + '/resources/xkb_configs')

        # load vendor, type and lanugage from config
        vendor = self.config_data.get('keyboard_vendor')
        type = self.config_data.get('keyboard_type')
        language = self.config_data.get('keyboard_language')

        # overwrite config if different
        if(args.keyboard_vendor):
            vendor = args.keyboard_vendor
            self.config_data.set('keyboard_vendor', args.keyboard_vendor)
        if(args.keyboard_type):
            type = args.keyboard_type
            self.config_data.set('keyboard_type', args.keyboard_type)
        if(args.keyboard_language):
            language = args.keyboard_language
            self.config_data.set('keyboard_language', args.keyboard_language)

        keyboard_manager.set_keyboard(vendor, type, language)
        self.config_data.save()

    def get_name(self):
        return "setup"
