import logging
import os
import platform
import subprocess


class KeyboardManager(object):
    def __init__(self, path):
        self.xkb_config_path = path

    def set_keyboard(self, vendor, type, language):
        assert platform.system() == 'Linux', 'Error: wrong OS, expected <Linux>'
        logging.info("- setting keyboard external")

        if(type == 'internal'):
            self.swap_ctrl_and_cmd_key()
        elif(type == 'external'):
            self.unswap_ctrl_and_cmd_key()
        else:
            logging.fatal("- unknown argument for <type>")

        if(vendor == 'apple'):
            # if the keyboard was made by apple the < and § buttons are probably swapped. Thus use a different key-config file
            self.sudo_cp(self.xkb_config_path + '/macintosh_vndr/ch_fixed',
                         '/usr/share/X11/xkb/symbols/macintosh_vndr/ch')
        else:
            self.sudo_cp(self.xkb_config_path + '/macintosh_vndr/ch_default',
                         '/usr/share/X11/xkb/symbols/macintosh_vndr/ch')

        if(language == 'ch'):
            layout = 'macintosh_vndr/ch'
        elif(language == 'us'):
            self.sudo_cp(self.xkb_config_path + '/macintosh_vndr/us_minus_slash_swapped',
                                     '/usr/share/X11/xkb/symbols/macintosh_vndr/us')
            layout = 'macintosh_vndr/us'
        else:
            logging.fatal("- unknown argument for <language>")

        self.set_xkb(layout)

    def swap_ctrl_and_cmd_key(self):
        self.sudo_cp(self.xkb_config_path + '/pc_cmd_ctrl_swapped', '/usr/share/X11/xkb/symbols/pc')

    def unswap_ctrl_and_cmd_key(self):
        self.sudo_cp(self.xkb_config_path + '/pc_default',  '/usr/share/X11/xkb/symbols/pc')

    def set_xkb(self, layout):
        self.sudo_rm_rf('/var/lib/xkb/')
        os.system(f'setxkbmap -layout {layout}')

    def sudo_cp(self, src, dest):
        cmd = f'sudo cp {src} {dest}'
        os.system(cmd)

    def sudo_rm_rf(self, dir):
        os.system(f'sudo rm -rf {dir}')

    def sudo_rm(self, file):
        os.system(f'sudo rm {file}')
