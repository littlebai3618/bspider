"""
整个 command 模块都参考了scrapy 的 commands模块
这里引用了scrapy 中的代码：https://github.com/scrapy/scrapy/blob/master/scrapy/commands/__init__.py
"""
import os
import re
from optparse import OptionGroup
from os.path import join
from shutil import ignore_patterns, copy2, copystat

import bspider

IGNORE = ignore_patterns('*.pyc', '.svn', '__pycache__')


class BSpiderCommand(object):
    # default settings to be used for this command instead of global defaults
    frame_settings = {}

    exitcode = 0

    def _is_valid_name(self, name):
        def _spider_exists(module_name):
            dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
            return module_name in dirs

        if not re.search(r'^[_a-zA-Z]\w*$', name):
            print('Error: names must begin with a letter and contain'
                  ' only\nletters, numbers and underscores')
        elif _spider_exists(name):
            print('Error: Module %r already exists' % name)
        else:
            return True
        return False

    def _copytree(self, src, dst):
        """
        copy platform template
        """
        ignore = IGNORE
        names = os.listdir(src)
        ignored_names = ignore(src, names)

        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in names:
            if name in ignored_names:
                continue

            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                self._copytree(srcname, dstname)
            else:
                copy2(srcname, dstname)
        copystat(src, dst)

    def __init__(self):
        self.settings = {}  # set in scrapy.cmdline

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since not post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = OptionGroup(parser, "Global Options")
        parser.add_option_group(group)

    def process_options(self, args, opts):
        pass

    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError

    @property
    def templates_dir(self):
        try:
            return self.settings['TEMPLATES_DIR']
        except KeyError:
            return join(bspider.__path__[0], 'templates')
