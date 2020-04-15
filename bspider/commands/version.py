import os
import sys

from lxml import etree

import bspider
from bspider.commands import BSpiderCommand
from bspider.utils.conf import BSPIDER_VERSION_ENV


class Command(BSpiderCommand):

    def syntax(self):
        return ""

    def short_desc(self):
        return "Print BSpider version"

    def add_options(self, parser):
        parser.add_option("--verbose", "-v", dest="verbose", action="store_true",
                          help="also display aiohttp/python/lxml info (useful for bug reports)")

    def run(self, args, opts):
        if not opts.verbose:
            print(f"BSpider {os.environ[BSPIDER_VERSION_ENV]}")
        else:
            lxml_version = ".".join(map(str, etree.LXML_VERSION))
            libxml2_version = ".".join(map(str, etree.LIBXML_VERSION))

            versions = [
                ("bspider", bspider.__version__),
                ("lxml", lxml_version),
                ("libxml2", libxml2_version),
                ("Python", sys.version.replace("\n", "- ")),
            ]
            width = max(len(n) for (n, _) in versions)
            patt = "%-{}s : %s".format(width)
            for name, version in versions:
                print(patt % (name, version))
