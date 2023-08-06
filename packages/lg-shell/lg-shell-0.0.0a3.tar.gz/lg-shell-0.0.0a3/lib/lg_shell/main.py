#! /usr/bin/env python3
from .modules.module_manager import ModuleManager

def main():
    manager = ModuleManager()
    manager.parse_args()
    exit_code = manager.run()
    return exit_code



if __name__ == '__main__':
    quit(main())
