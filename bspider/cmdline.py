"""
整个command模块都参考了scrapy 的command模块
https://github.com/scrapy/scrapy/blob/master/scrapy/cmdline.py
https://github.com/scrapy/scrapy/tree/master/scrapy/commands
"""
import inspect
import optparse
import sys
import os

from bspider.commands import BSpiderCommand
from bspider.config import FrameSettings
from bspider.utils.conf import init_platform_env, PLATFORM_NAME_ENV, BSPIDER_VERSION_ENV
from bspider.utils.exceptions import UsageError
from bspider.utils.importer import walk_modules


class CommandLine(object):

    def __init__(self):
        self.cmds = self.__get_commands_from_module()
        print(self.cmds)
        self.args = list()

    @staticmethod
    def __get_commands_from_module(module='bspider.commands'):
        cmds = dict()
        for mod in walk_modules(module):
            for obj in vars(mod).values():
                if inspect.isclass(obj) and \
                        issubclass(obj, BSpiderCommand) and \
                        obj.__module__ == mod.__name__ and \
                        not obj == BSpiderCommand:
                    cmds[obj.__module__.split('.')[-1]] = obj()
        return cmds

    @staticmethod
    def __print_header():
        if os.environ.get(PLATFORM_NAME_ENV):
            print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]} - platform {os.environ[PLATFORM_NAME_ENV]}")
        else:
            print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]} - no active platform")

    @property
    def command_name(self):
        i = 0
        for arg in self.args[1:]:
            if not arg.startswith('-'):
                del self.args[i]
                return arg
            i += 1

    @init_platform_env
    def execute(self, argv=None):
        self.args = sys.argv if argv is None else argv
        command_name = self.command_name
        if not command_name:
            self.__print_header()
            print("Usage: bspider <command> [options] [args]")
            print("Available commands:")
            for cmdname, cmdclass in sorted(self.cmds.items()):
                print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
            print('Use "bspider <command> -h" to see more info about a command')
            sys.exit(0)

        if not command_name in self.cmds:
            self.__print_header()
            print("Unknown command: %s\n" % command_name)
            sys.exit(2)

        if command_name == 'mkplatform' or command_name == 'version':
            frame_settings = dict()
        elif os.environ.get(PLATFORM_NAME_ENV):
            frame_settings = FrameSettings()
        else:
            self.__print_header()
            print('Please use bspider mkplatform <platform_name> to create a platform')
            sys.exit(2)

        command = self.cmds[command_name]
        parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter(), conflict_handler='resolve')
        parser.prog = command_name
        parser.usage = f"bspider {command_name} {command.syntax()}"
        parser.description = command.long_desc()
        command.add_options(parser)
        command.frame_settings = frame_settings
        try:
            command.run(*parser.parse_args(self.args))
        except UsageError:
            parser.print_help()
            sys.exit(2)
        sys.exit(command.exitcode)


def execute(argv):
    """
    执行终端命令
    :param cmdname:
    :param args:
    :return:
    """
    CommandLine().execute(argv)


if __name__ == '__main__':
    print(os.listdir('.'))
    print(execute(['cmdline.py', 'startspider', 'c1_baidu_map']))
