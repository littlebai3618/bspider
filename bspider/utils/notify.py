# @Time    : 2019/6/17 1:12 PM
# @Author  : 白尚林
# @File    : notify
# @Use     : 通知方法
import datetime
import json

import requests
from urllib3 import disable_warnings

disable_warnings()

from bspider.config import FrameSettings
from bspider.utils.system import System


def ding(msg, title='', at=None):
    """
    发送钉钉报警
    :param msg: str 钉钉报警的信息
    :param at: list at 谁
    :return: None
    """
    cur_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'msgtype': 'markdown',
        "markdown": {
            "title": f"【bspider】{title}",
            "text": f"{msg} \n> ###### {cur_time}报警 {System.ip_msg} \n"
        },
        "at": {
            "atMobiles": at,
            "isAtAll": False
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.post(
        url=FrameSettings()['DING'],
        headers=headers,
        data=json.dumps(data),
        verify=False
    )


# 短信通知服务
def sms(msg, phone):
    message = '【bspider】{}'.format(msg)
    for p in phone:
        r = requests.post(
            url=f'http://172.20.31.177/sp/tools/sms.php?phone={p}&msg={message}',
            verify=False
        )
