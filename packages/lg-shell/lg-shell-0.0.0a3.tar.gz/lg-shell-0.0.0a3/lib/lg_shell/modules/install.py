from .abstract_module import AbstractModule
import os
import shutil
import logging
import platform

class Install(AbstractModule):
    def __init__(self, subparser):
        super(Install, self).__init__(subparser)
        self.homep = os.path.expanduser('~')
        self.lgsp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def add_module_to_parser(self, subparser):
        super(Install, self).add_module_to_parser(subparser)
        self.module_parser.add_argument('-a', '--all', dest='all', action='store_true', help='install all')
        self.module_parser.add_argument('--vim', dest='vim', action='store_true', help='install vim config')
        self.module_parser.add_argument('--tmux', dest='tmux', action='store_true', help='install tmux config')
        self.module_parser.add_argument('--bashrc', dest='bashrc', action='store_true', help='install bashrc')
        self.module_parser.add_argument('--alias', dest='alias', action='store_true', help='install alias')

    def run(self, args):
        if (args.all):
            self.install_all()
            return
        if (args.vim):
            self.install_vim()
        if (args.tmux):
            self.install_tmux()
        if (args.bashrc):
            self.install_bashrc()
        if (args.alias):
            self.install_alias()

    def get_name(self):
        return "install"

    def install_vim(self):
        logging.info("- installing vim")
        shutil.rmtree(self.homep + '/.vim', ignore_errors=True)
        shutil.copytree(self.lgsp + '/resources/.vim', self.homep + '/.vim')
        os.system("git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim")
        os.system("vim -c 'PluginInstall' -c 'qa!'")

    def install_tmux(self):
        logging.info("- installing tmux")
        shutil.copy(self.lgsp + '/resources/.tmux.conf', self.homep)

    def install_bashrc(self):
        logging.info("- installing bashrc")
        if (platform.system() == 'Darwin'):
            shutil.copy(self.lgsp + '/resources/.bash_profile', self.homep)

        if (platform.system() == 'Linux'):
            shutil.copy(self.lgsp + '/resources/.bashrc', self.homep)

    def install_alias(self):
        logging.info("- installing alias")
        shutil.copy(self.lgsp + '/resources/.bash_aliases', self.homep)

    def install_all(self):
        logging.info("- installing all...")
        self.install_vim()
        self.install_tmux()
        self.install_bashrc()
        self.install_alias()
        return
