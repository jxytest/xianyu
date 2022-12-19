import json
import threading
import time
import frida
import os
from fastapi import FastAPI, Query
import uvicorn
from redis import Redis
from api import search

packageName = "com.taobao.idlefish"
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, "rpc.js"), encoding='utf-8') as f:
    hookCode = f.read()
process = frida.get_remote_device().attach("闲鱼")
script = process.create_script(hookCode)
result = {}

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


sign = None
t = None


def search_v1(keyword):
    try:
        script.exports.getSign(keyword, t)
        res = search(keyword, sign, t)
        res = res.get("data").get("resultList")
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
            # 存入redis
            redis.set(item_id, json.dumps(data))
        global result
        result = res
    except Exception as e:
        print(e)


def on_message(message, data):
    global sign
    global t
    sign = message.get("payload").get("sign")
    keyword = message.get("payload").get("keyword")
    t = message.get("payload").get("t")
    sign = dict([x.split('=', 1) for x in sign[1:-1].split(", ")])
    print(sign, keyword, t)


script.on('message', on_message)
script.load()
app = FastAPI()


@app.get("/getGoodsList")
async def getGoodsList(fl: str = Query(default=None, min_length=2, max_length=10),
                       page: int = Query(default=1, ge=1, le=100),
                       page_size: int = Query(default=10, ge=1, le=100)):
    # 从redis中获取所有数据，并过滤title中包含filter的数据
    data = redis.keys()
    res = []
    for item in data:
        item = json.loads(redis.get(item))
        if fl and (fl in item.get("title")):
            res.append(item)

    # 分页返回数据
    start = (page - 1) * page_size
    end = page * page_size

    return {"code": 200, "msg": "获取成功", "data": res[start:end]}


def task():
    while True:
        search_v1("dell r730")
        time.sleep(10)


def create_thread(task, args=()):
    t = threading.Thread(target=task, args=args)
    t.setDaemon(True)
    t.start()
    return t


if __name__ == '__main__':
    create_thread(task)
    uvicorn.run(app)
