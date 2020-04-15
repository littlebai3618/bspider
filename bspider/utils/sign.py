import hashlib
import json


class Sign(object):

    def __init__(self, **kwargs):
        plaintext = json.dumps(kwargs).encode('utf-8')
        self.__sign = hashlib.md5(plaintext).hexdigest()

    def __eq__(self, other):
        return self.__sign == str(other)

    def __str__(self):
        return self.__sign
