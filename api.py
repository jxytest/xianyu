import requests


def search(keyword, sign, t):
    url = "https://g-acs.m.goofish.com/gw/mtop.taobao.idlemtopsearch.search/1.0/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3BRedmi+K30+Pro+Zoom+Edition%29",
        "x-t": t,
        "x-pv": '6.3',
        "x-mini-wua": sign.get('x-mini-wua'),
        "x-sgext": sign.get('x-sgext'),
        "x-sign": sign.get('x-sign'),
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
    res = requests.post(url, headers=headers, data=data)

    return res.json()
