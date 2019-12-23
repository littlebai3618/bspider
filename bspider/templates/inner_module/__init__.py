"""
一些内置的模块
"""
import re

text = open('/Users/baishanglin/PycharmProjects/bspider/bspider/templates/inner_module/auto_clear_operation.py').read()
desc = re.compile('@([A-Za-z]+)=(.*?)\n').findall(text)
print(desc)
