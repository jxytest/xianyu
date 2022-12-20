import asyncio
import json
import threading

from api import Api
from fastapi import FastAPI, Query
import uvicorn
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
api = Api()
app = FastAPI()


@app.get("/getGoodsList")
async def getGoodsList(fl: str = Query(default=None, min_length=2, max_length=10),
                       page: int = Query(default=1, ge=1, le=100),
                       page_size: int = Query(default=10, ge=1, le=100)):
    # 从redis中获取所有数据，并过滤title中包含filter的数据
    data = redis.keys()
    print(data)
    res = []
    for item in data:
        try:
            item = json.loads(redis.get(item))
            if fl and (fl in item.get("title")):
                res.append(item)
        except Exception as e:
            print(e)
            continue

    # 分页返回数据
    start = (page - 1) * page_size
    end = page * page_size

    return {"code": 200, "msg": "获取成功", "data": res[start:end]}


async def task(keywords):
    while True:
        for keyword in keywords:
            # 获取数据
            data = await api.search(keyword)
            # 存入redis
            for item in data:
                await redis.set(item.get("id"), json.dumps(item))
            await asyncio.sleep(10)
        # 休眠
        await asyncio.sleep(60)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([
        asyncio.run(task(["手机", "电脑", "电视"])),
        uvicorn.run(app)
    ]))


