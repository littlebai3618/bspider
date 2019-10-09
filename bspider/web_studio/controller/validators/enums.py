# @Time    : 2019-08-01 15:56
# @Author  : 白尚林
# @File    : enums
# @Use     :
from enum import Enum


class ClientTypeEnum(Enum):
    identity = 101 # 账号登录


class OpTypeEnum(Enum):
    start = 1
    stop = 0
    exec = -1