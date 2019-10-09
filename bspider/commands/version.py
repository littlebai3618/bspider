# @Time    : 2019-09-06 11:10
# @Author  : baii
# @File    : version
# @Use     :
import os

from bspider.commands import BSpiderCommand
from bspider.utils.conf import BSPIDER_VERSION_ENV


class Command(BSpiderCommand):

    def syntax(self):
        return "[-v]"

    def short_desc(self):
        return "Print BSpider version"

    def add_options(self, parser):
        BSpiderCommand.add_options(self, parser)
        parser.add_option("--verbose", "-v", dest="verbose", action="store_true",
            help="show current python env bspider version")

    def run(self, args, opts):
        print(f"Bspider {os.environ[BSPIDER_VERSION_ENV]}")
