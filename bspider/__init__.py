"""
BSpider - a high-level distributed crawling framework written for Python
"""

__all__ = ['__version__', 'version_info']

# Scrapy version
import pkgutil
__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()
version_info = tuple(int(v) if v.isdigit() else v
                     for v in __version__.split('.'))
del pkgutil

# Check minimum required Python version
import sys
if sys.version_info < (3, 7):
    print("BSpider %s requires Python 3.7" % __version__)
    sys.exit(1)
