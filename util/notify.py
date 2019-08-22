# @Time    : 2019/6/17 1:12 PM
# @Author  : 白尚林
# @File    : notify
# @Use     : 通知方法
import datetime
import json

import requests

from config import frame_settings
from util.system import ip_addr


def ding(msg, at=None):
    """
    发送钉钉报警
    :param msg: str 钉钉报警的信息
    :param at: list at 谁
    :return: None
    """
    message = 'Msg: 【bspider】{} \nTime: {} \nIP: {}'.format(
        msg,datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), ip_addr()
    )
    data = {
        'msgtype': 'text',
        'text': {
            'content': message
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
        url=frame_settings.DING,
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
