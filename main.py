import asyncio
import json
import threading
import time

# from pusher import ding_push
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from core.service.service import router
from fastapi import FastAPI, Query
import uvicorn
import aioredis


# api = Api()
app = FastAPI()
app.include_router(router)
#
# async def task(keywords):
#     redis = aioredis.from_url("redis://localhost")
#     while True:
#         try:
#             for keyword in keywords:
#                 # 获取数据
#                 print("开始获取数据", keyword)
#                 data = await api.search(keyword)
#                 # 存入redis
#                 for item in data:
#                     if not await redis.exists(item.get("itemId")) and 4000 > float(item.get("price")) > 1000 \
#                             and "回收" not in item.get("title") and "求购" not in item.get("title")\
#                             and time.mktime(time.strptime(item.get("publish_time"), "%Y-%m-%d %H:%M:%S")) > \
#                             time.time() - 3600 * 24 * 3:
#                         # {"itemId":"695010780965","userNick":"薄利多销小店","price":"3888","publish_time":"2022-12-19
#                         # 23:47:03","title":"苹果12promax，外版无锁128功能全好面容秒解，成色如 图新原装机。屏幕上角小老化如图不明显，朋友自用机闲置低价出。",
#                         # "pic_url":"http://img.alicdn.com/bao/uploaded/i2/O1CN01uNcGsu2CWLpwt92zT_!!0-fleamarket.jpg
#                         # "} 解析成md格式
#                         message = f"### {item.get('title')}\n" \
#                                     f"> 价格：{item.get('price')}\n" \
#                                     f"> 发布时间：{item.get('publish_time')}\n" \
#                                     f"> 商品链接：https://item.taobao.com/item.htm?id={item.get('itemId')}\n" \
#                                     f"> ![商品图片]({item.get('pic_url')})\n"
#                         await ding_push(message)
#                     await redis.set(item.get("itemId"), json.dumps(item))
#                 await asyncio.sleep(10)
#         except Exception as e:
#             logger.exception(e)
#         finally:
#             await asyncio.sleep(10)
#
#
# # 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()


if __name__ == '__main__':
    # asyncio.run(task(["dell r730", "dell r730xd"]))
    # threading.Timer(10, lambda: asyncio.run(task(["dell r730"]))).start()
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(task, "interval", seconds=10, args=(["dell r730xd"],))
    # # 创建一个事件循环loop
    # new_loop = asyncio.new_event_loop()
    # # 在另一个线程中启动事件循环loop
    # t = threading.Thread(target=start_loop, args=(new_loop,))  # 通过当前线程开启新的线程去启动事件循环
    # t.start()
    # asyncio.run_coroutine_threadsafe(task(['iphone12', '5280m4']), new_loop)  # 在新的线程中启动事件循环
    # 主线程启动fastapi
    uvicorn.run(app)
    # 2022-12-20 16:00:00格式转成时间戳
    # print(time.mktime(time.strptime("2022-12-20 16:00:00", "%Y-%m-%d %H:%M:%S")))
