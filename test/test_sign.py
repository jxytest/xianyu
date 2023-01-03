import asyncio
import os
import time
from urllib.parse import quote
from core.api.api import Api
from core.frida.xianyu import XianYu

xian_yu = XianYu(os.path.join(os.path.dirname(__file__), "../core/js/rpc.js"))


def update_headers(headers, data: str):
    t = str(int(time.time()))
    sign = xian_yu.get_sign(data, headers, t)
    headers.update({
        "x-t": t,
        "x-mini-wua": quote(sign.get('x-mini-wua')),
        "x-sgext": quote(sign.get('x-sgext')),
        "x-sign": quote(sign.get('x-sign')),
        "x-mut": quote(sign.get('x-umt')),
    })
    return headers


# 生成随机字符串
def random_str(random_length=8):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    import random
    import string
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(random_length)]
    return ''.join(str_list)


def test_api():
    api = Api()
    asyncio.run(api.search("dell r730"))
