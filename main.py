import asyncio
import json
import threading
import time

from pusher import ding_push
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from api import Api
from fastapi import FastAPI, Query
import uvicorn
import aioredis

redis = aioredis.from_url("redis://localhost")
api = Api()
app = FastAPI()


@app.get("/getGoodsList")
async def getGoodsList(q: str = Query(default=None, min_length=2, max_length=20),
                       fl: list = Query(default=None),
                       page: int = Query(default=1, ge=1, le=100),
                       page_size: int = Query(default=10, ge=1, le=100)):
    # 从redis中获取所有数据，并过滤title中包含filter的数据
    data = await redis.keys()
    print(data)
    res = []
    index = 1
    for item in data:
        try:
            result = await redis.get(item.decode())
            result = json.loads(result.decode('unicode-escape'))
            flag = False
            if fl:
                for f in fl:
                    if f in result.get("title"):
                        flag = True
                        break
            if flag:
                continue
            if q and q not in result.get("title"):
                continue
            result["index"] = index
            index += 1
            res.append(result)
        except Exception as e:
            print(e)
            await redis.delete(item.decode())
            continue

    # 分页返回数据
    start = (page - 1) * page_size
    end = page * page_size

    return {"code": 200, "msg": "获取成功", "data": res[start:end]}


async def task(keywords):
    redis = aioredis.from_url("redis://localhost")
    while True:
        try:
            for keyword in keywords:
                # 获取数据
                print("开始获取数据", keyword)
                data = await api.search(keyword)
                # 存入redis
                for item in data:
                    if not await redis.exists(item.get("itemId")) and 4000 > int(item.get("price")) > 1000 \
                            and "回收" not in item.get("title") and "求购" not in item.get("title")\
                            and time.mktime(time.strptime(item.get("publish_time"), "%Y-%m-%d %H:%M:%S")) > \
                            time.time() - 3600 * 24 * 3:
                        await ding_push(item)
                    await redis.set(item.get("itemId"), json.dumps(item))
                await asyncio.sleep(10)
        except Exception as e:
            logger.exception(e)
        finally:
            await asyncio.sleep(10)


# 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    # asyncio.run(task(["dell r730", "dell r730xd"]))
    # threading.Timer(10, lambda: asyncio.run(task(["dell r730"]))).start()
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(task, "interval", seconds=10, args=(["dell r730xd"],))
    # 创建一个事件循环loop
    new_loop = asyncio.new_event_loop()
    # 在另一个线程中启动事件循环loop
    t = threading.Thread(target=start_loop, args=(new_loop,))  # 通过当前线程开启新的线程去启动事件循环
    t.start()
    asyncio.run_coroutine_threadsafe(task(['dell r730']), new_loop)  # 在新的线程中启动事件循环
    # 主线程启动fastapi
    uvicorn.run(app)
    # 2022-12-20 16:00:00格式转成时间戳
    # print(time.mktime(time.strptime("2022-12-20 16:00:00", "%Y-%m-%d %H:%M:%S")))
