import time
from loguru import logger
from xianyu import XianYu
import aiohttp


class Api:
    def __init__(self):
        self.search_url = "https://g-acs.m.goofish.com/gw/mtop.taobao.idlemtopsearch.search/1.0/"
        self.xian_yu = XianYu("rpc.js")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3BRedmi+K30+Pro+Zoom+Edition%29",
            "x-pv": '6.3',
            "x-bx-version": '6.5.88',
            "x-ttid": '231200@fleamarket_android_7.8.40',
            "x-app-ver": '7.8.40',
            "a-orange-q": 'appKey=21407387&appVersion=7.8.40&clientAppIndexVersion=1120221215143500625'
                          '&clientVersionIndexVersion=0',
            "x-utdid": "Y5wu32PRazMDAKz6FvVOHBHu",
            "x-appkey": "21407387",
            "x-devid": "Y5wu32PRazMDAKz6FvVOHBHu",
            "x-features": "27"
        }
        # self.session = aiohttp.ClientSession()

    def update_headers(self, data):
        t = str(int(time.time()))
        sign = self.xian_yu.get_sign(data, t)
        self.headers.update({
            "x-t": t,
            "x-mini-wua": sign.get('x-mini-wua'),
            "x-sgext": sign.get('x-sgext'),
            "x-sign": sign.get('x-sign'),
        })

    async def search(self, keyword):
        data = {
            "data": '{"activeSearch":false,"bizFrom":"home","clientModifiedCpvNavigatorJson":"{\"tabList\":[],'
                    '\"fromClient\":false}","disableHierarchicalSort":0,"forceUseInputKeyword":false,'
                    '"forceUseTppRepair":false,"fromCombo":"Sort","fromFilter":true,"fromKits":false,'
                    '"fromLeaf":false,"fromShade":false,"fromSuggest":false,"keyword":"%s","pageNumber":1,'
                    '"propValueStr":"{\"searchFilter\":\"publishDays:3\"}","resultListLastIndex":0,"rowsPerPage":10,'
                    '"searchReqFromActivatePagePart":"searchButton","searchReqFromPage":"xyHome",'
                    '"searchTabType":"SEARCH_TAB_MAIN","shadeBucketNum":-1,"sortField":"create","sortValue":"desc",'
                    '"suggestBucketNum":37}' % keyword
        }
        self.update_headers(data)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.search_url, data=data) as resp:
                resp = await resp.json()
                logger.info(f"search请求结果: {resp}")
                result = self.parser_search_result(resp)
                logger.info(f"search解析结果: {result}")
                return result

    @staticmethod
    def parser_search_result(response):
        try:
            res = response.get("data").get("resultList")
            result = []
            for item in res:
                main = item.get("data").get("item").get("main")
                click_param = main.get("clickParam")
                ex_content = main.get("exContent")
                target_url = main.get("targetUrl")
                publish_time = click_param.get("publishTime")
                # 时间戳转换
                publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publish_time / 1000))
                title = ex_content.get("title")
                item_id = ex_content.get("itemId")
                pic_url = ex_content.get("picUrl")
                user_nick = ex_content.get('detailParams').get("userNick")
                price = ex_content.get('detailParams').get("soldPrice")
                # 组装数据
                data = {
                    "itemId": item_id,
                    "userNick": user_nick,
                    "price": price,
                    "title": title,
                    "pic_url": pic_url,
                    "publish_time": publish_time,
                }
                result.append(data)
            return result
        except Exception as e:
            logger.error(f"解析search结果失败: {e}")
            return []
