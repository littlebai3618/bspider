"""
整个command模块都参考了scrapy 的command模块
https://github.com/scrapy/scrapy/blob/master/scrapy/cmdline.py
https://github.com/scrapy/scrapy/tree/master/scrapy/commands
"""
import inspect
import optparse
import os
import sys

from bspider.commands import BSpiderCommand
from bspider.config import FrameSettings
from bspider.utils.exceptions import UsageError
from bspider.utils.importer import walk_modules
from bspider.utils.conf import init_platform_env, PLATFORM_NAME_ENV, BSPIDER_VERSION_ENV


def _get_commands_from_module(module='bspider.commands'):
    cmds = dict()
    for mod in walk_modules(module):
        for obj in vars(mod).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, BSpiderCommand) and \
                    obj.__module__ == mod.__name__ and \
                    not obj == BSpiderCommand:
                cmds[obj.__module__.split('.')[-1]] = obj()
    return cmds


def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


def _print_header():
    if os.environ.get(PLATFORM_NAME_ENV):
        print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]} - platform {os.environ[PLATFORM_NAME_ENV]}")
    else:
        print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]} - no active platform")

def _print_commands(cmds):
    _print_header()
    print("Usage: bspider <command> [options] [args]")
    print("Available commands:")
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
    print('Use "bspider <command> -h" to see more info about a command')


def _print_unknown_command(cmdname):
    _print_header()
    print("Unknown command: %s\n" % cmdname)
    print('Use "bspider" to see available commands')


def _print_unknow_platform():
    print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]} - no platform")
    print('Please use bspider mkplatform <platform_name> to create a platform')


def run_cmd(cmd, parser, args, opts):
    try:
        cmd.run(args, opts)
    except UsageError:
        parser.print_help()
        sys.exit(2)


@init_platform_env
def execute(argv=None):
    """
    执行终端命令
    :param cmdname:
    :param args:
    :return:
    """
    if argv is None:
        argv = sys.argv
    # 取出命令
    cmdname = _pop_command_name(argv)
    # 获取终端命令列表
    cmds = _get_commands_from_module()
    # 获取命令解析对象
    parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter(), conflict_handler='resolve')
    if not cmdname:
        _print_commands(cmds)
        sys.exit(0)
    if cmdname not in cmds:
        _print_unknown_command(cmdname)
        sys.exit(2)

    if cmdname == 'mkplatform' or cmdname == 'version':
        frame_settings = dict()
    elif os.environ.get(PLATFORM_NAME_ENV):
        frame_settings = FrameSettings()
    else:
        _print_unknow_platform()
        sys.exit(2)

    cmd = cmds[cmdname]
    parser.prog = cmdname
    parser.usage = f"bspider {cmdname} {cmd.syntax()}"
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    cmd.frame_settings = frame_settings
    run_cmd(cmd, parser, args, opts)
    sys.exit(cmd.exitcode)


if __name__ == '__main__':
    print(os.listdir('.'))
    print(execute(['cmdline.py', 'startspider', 'c1_baidu_map']))
