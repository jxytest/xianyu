import asyncio
import json
import time

from loguru import logger

from .. import redis
from ..api.api import Api
from ..pusher import ding_push
from ..pusher import wx_push

api = Api()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# loop.run_forever()


async def xy_task(keywords):
    try:
        for keyword in keywords:
            # 获取数据
            print("开始获取数据", keyword)
            data = await api.search(keyword)
            # 存入redis
            for item in data:
                if not await redis.exists(item.get("itemId")) and 4000 > float(item.get("price")) > 1000 \
                        and "回收" not in item.get("title") and "求购" not in item.get("title") \
                        and time.mktime(time.strptime(item.get("publish_time"), "%Y-%m-%d %H:%M:%S")) > \
                        time.time() - 3600 * 24 * 3:
                    # {"itemId":"695010780965","userNick":"薄利多销小店","price":"3888","publish_time":"2022-12-19
                    # 23:47:03","title":"苹果12promax，外版无锁128功能全好面容秒解，成色如 图新原装机。屏幕上角小老化如图不明显，朋友自用机闲置低价出。",
                    # "pic_url":"http://img.alicdn.com/bao/uploaded/i2/O1CN01uNcGsu2CWLpwt92zT_!!0-fleamarket.jpg
                    # "} 解析成md格式
                    message = f"### {item.get('title')}\n" \
                              f"> 价格：{item.get('price')}\n" \
                              f"> 发布时间：{item.get('publish_time')}\n" \
                              f"> 商品链接：https://item.taobao.com/item.htm?id={item.get('itemId')}\n" \
                              f"> ![商品图片]({item.get('pic_url')})\n"

                    await ding_push(message)
                    await wx_push(message)
                await redis.set(item.get("itemId"), json.dumps(item))
    except Exception as e:
        logger.exception(e)
    finally:
        pass


def start_task(keyword):
    logger.info("==============================")
    logger.info(f"开始任务：{keyword}")

    xt = loop.create_task(xy_task(keyword))
    loop.run_until_complete(asyncio.wait([xt]))
    # loop.close()
    # asyncio.run(xy_task(keyword))
    logger.info(f"任务结束：{keyword}")
    logger.info("-------------------------------")
