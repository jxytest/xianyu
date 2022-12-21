import json
import time
from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from .. import redis
from core.filter.xy_filter import FilterXY
from core.task.task_manage import XianYuTask

router = APIRouter()

# 白名单过滤器
whitelist = FilterXY('whitelist.txt')
# 黑名单过滤器
blacklist = FilterXY('blacklist.txt')
xian_yu_task = XianYuTask()


class TaskInfo(BaseModel):
    keywords: List[str]
    seconds: int
    type: int = Query(default=0, description='0:添加任务 1:删除任务 2:暂停任务 3:恢复任务', ge=0, le=3)


@router.get("/getGoodsList")
async def getGoodsList(q: str = Query(default=None, min_length=2, max_length=20),
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
            if blacklist.filter(result):
                continue
            if not whitelist.filter(result):
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
    # 根据价格排序
    # res = sorted(res, key=lambda x: float(x.get("price")))
    # 根据时间排序
    res = sorted(res, key=lambda x: time.mktime(time.strptime(x.get("publish_time"), "%Y-%m-%d %H:%M:%S")),
                 reverse=True)
    # 分页返回数据
    start = (page - 1) * page_size
    end = page * page_size

    return {"code": 200, "msg": "获取成功", "data": res[start:end]}


@router.post("/tasks")
async def tasks(task_info: TaskInfo):
    if task_info.type == 0:
        # 添加任务
        xian_yu_task.add_task(task_info.keywords, task_info.seconds)
    elif task_info.type == 1:
        # 删除任务
        xian_yu_task.del_task(task_info.keywords, task_info.seconds)
    elif task_info.type == 2:
        # 暂停任务
        xian_yu_task.pause()
    elif task_info.type == 3:
        # 恢复任务
        xian_yu_task.resume()
    return {"code": 200, "msg": "操作成功"}


@router.post("/setFilter")
async def setFilter(type_filter: int = Query(default=0, description='0:添加白名单 1:添加黑名单 2:从白名单删除 3:从黑名单删除 4:查看白名单列表 '
                                                                    '5:查看黑名单列表', ge=0, le=4),
                    keywords: List[str] = Query(default=None, description='关键字列表')):
    if type_filter == 0:
        # 添加白名单
        for keyword in keywords:
            whitelist.add_filter(keyword)
    elif type_filter == 1:
        # 添加黑名单
        for keyword in keywords:
            blacklist.add_filter(keyword)
    elif type_filter == 2:
        # 从白名单删除
        for keyword in keywords:
            whitelist.del_filter(keyword)
    elif type_filter == 3:
        # 从黑名单删除
        for keyword in keywords:
            blacklist.del_filter(keyword)
    elif type_filter == 4:
        # 查看白名单列表
        return {"code": 200, "msg": "获取成功", "data": whitelist.filter_list()}
    elif type_filter == 5:
        # 查看黑名单列表
        return {"code": 200, "msg": "获取成功", "data": blacklist.filter_list()}
    return {"code": 200, "msg": "操作成功"}
