# @Time    : 2019-08-05 15:16
# @Author  : 白尚林
# @File    : connection
# @Use     :
import json

import requests

from config.frame_settings import MASTER_SERVICE


class Connection(object):

    def __init__(self):
        self.master = MASTER_SERVICE
        self.__headers = {'Content-Type': 'application/json'}

    def query(self, uri, method, data=None):
        url = self.master + uri
        return requests.request(method=method, url=url, data=json.dumps(data), headers=self.__headers).json()

    def agent_register(self, data):
        return self.query('/node', 'POST', data=data)
