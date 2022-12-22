import json
import os
from urllib.parse import quote_plus, quote

from core.frida.xianyu import XianYu


def test_sign():
    xian_yu = XianYu(os.path.join(os.path.dirname(__file__), "../core/js/rpc.js"))
    data = {
        "data": {"activeSearch": False, "bizFrom": "home", "disableHierarchicalSort": 0, "forceUseInputKeyword": False,
                 "forceUseTppRepair": False, "fromFilter": False, "fromKits": False, "fromLeaf": False,
                 "fromShade": False, "fromSuggest": False, "keyword": "云手机", "pageNumber": 1, "resultListLastIndex": 0,
                 "rowsPerPage": 10, "searchReqFromActivatePagePart": "historyItem", "searchReqFromPage": "xyHome",
                 "searchTabType": "SEARCH_TAB_MAIN", "shadeBucketNum": -1, "suggestBucketNum": 33}
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


def test_qu():
    data = {
        "activeSearch": False,
        "bizFrom": "home",
        "disableHierarchicalSort": 0, "forceUseInputKeyword": False,
        "forceUseTppRepair": False, "fromFilter": False, "fromKits": False, "fromLeaf": False, "fromShade": False,
        "fromSuggest": False, "keyword": "sa5212m4", "pageNumber": 1, "resultListLastIndex": 0, "rowsPerPage": 10,
        "searchReqFromActivatePagePart": "historyItem", "searchReqFromPage": "xyHome",
        "searchTabType": "SEARCH_TAB_MAIN", "shadeBucketNum": -1, "suggestBucketNum": 33}
    print(json.dumps(data))
    # 去空格
    data = json.dumps(data).replace(" ", "")
    print(quote(data))
