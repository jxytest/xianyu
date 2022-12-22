import asyncio
import json
import os
import time
import urllib
from urllib.parse import quote_plus, quote

import requests

from core.api.api import Api
from core.frida.xianyu import XianYu

xian_yu = XianYu(os.path.join(os.path.dirname(__file__), "../core/js/rpc.js"))


def test_sign():
    data = {
        'data': '{"activeSearch":false,"bizFrom":"home","disableHierarchicalSort":0,"forceUseInputKeyword":false,"forceUseTppRepair":false,"fromFilter":false,"fromKits":false,"fromLeaf":false,"fromShade":false,"fromSuggest":false,"keyword":"云手机","pageNumber":1,"resultListLastIndex":0,"rowsPerPage":10,"searchReqFromActivatePagePart":"searchButton","searchReqFromPage":"xyHome","searchTabType":"SEARCH_TAB_MAIN","shadeBucketNum":-1,"suggestBucketNum":33}',
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3BRedmi+K30+Pro+Zoom+Edition%29",
        "x-pv": '6.3',
        # TODO 登录后获取
        "x-sid": '14da454c9c1d9e0ca034d26c95e8dbd3',
        "x-bx-version": '6.5.88',
        "x-ttid": '231200@fleamarket_android_7.8.40',
        "x-app-ver": '7.8.40',
        "x-utdid": "X/bTHVUvlf4DAAubT0WJXpoD",
        "x-appkey": "21407387",
        "x-devid": 'Aqt_PBohWdwAsGzXiXY7HF2ViwjRMA05SRnwqIvPFZDx',
        "x-features": "27"
    }

    print(xian_yu.get_sign(json.dumps(data), headers, "1671673341"))
    headers = {
        'umid': 'B94BhVxLPIjTTAKFMw8u0M5OFG+AuwhE',
        'x-sid': '14da454c9c1d9e0ca034d26c95e8dbd3',
        'x-uid': '2143549739',
        'x-nettype': 'WIFI',
        'x-pv': '6.3',
        'x-nq': 'WIFI',
        'EagleEye-UserData': 'spm-cnt=a2170.8011571.0.0&spm-url=a2170.unknown.0.0',
        'first_open': '0',
        'x-features': '27',
        'x-app-conf-v': '0',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Content-Length': '640',
        'oaid': 'ef4d6747261738fd',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Cookie': 'unb=2143549739; munb=2143549739; _nk_=%5Cu5BDE%5Cu661F%5Cu6C89; cookie2=14da454c9c1d9e0ca034d26c95e8dbd3; csg=2e46b480; t=adc81779bfa70b35310aa7c0c8890a3d; _tb_token_=5eea7913e3353; sgcookie=W100EBE%2FgJyMO%2Fh1nUumc1mxY78wzpOFqK4Psj5J97MelFO0hi%2BbuuHHWzjposSC1jvyZimvx8vLCQcW932dGWnTFfoC4%2B8pCgxQ3IA1TXieYvc%3D',
        'x-bx-version': '6.5.88',
        'f-refer': 'mtop',
        'x-extdata': 'openappkey%3DDEFAULT_AUTH',
        'x-ttid': '231200%40fleamarket_android_7.8.40',
        'x-app-ver': '7.8.40',
        'x-c-traceid': f'X%2F{random_str(22)}{int(time.time() * 1000)}0230112176',
        'x-location': '0%2C0',
        'a-orange-q': 'appKey=21407387&appVersion=7.8.40&clientAppIndexVersion=1120221221105400982&clientVersionIndexVersion=0',
        'x-utdid': quote(random_str(24)),
        'x-appkey': '21407387',
        'x-devid': quote(random_str(44)),
        'user-agent': 'MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3BRedmi+K30+Pro+Zoom+Edition%29',
        'Host': 'g-acs.m.goofish.com',
        # 'Accept-Encoding': 'gzip',
        'Connection': 'Keep-Alive',
    }

    update_headers(headers, urllib.parse.urlencode(data))
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    response = requests.post(
        'https://g-acs.m.goofish.com/gw/mtop.taobao.idlemtopsearch.search/1.0/',
        headers=headers,
        data=data,
        proxies=proxies,
        verify=False
    )
    print(response.text)


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
    asyncio.run(api.search("手机"))
