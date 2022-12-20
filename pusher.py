import asyncio
import json

import aiohttp


async def ding_push(message):
    push = "https://oapi.dingtalk.com/robot/send?access_token" \
           "=cf5385fc80c9d74e620068954dfb10438725a24fac727bb2213e2f4550f42077 "

    text = {
        "msgtype": "markdown",
        "markdown": {
            "title": "result",
            "text": message
        },
        "at": {
            "atUserIds": [

            ],
            "isAtAll": False
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.request("POST", url=push, headers=headers, json=text) as resp:
        print(resp.status)
        print(await resp.text())


if __name__ == '__main__':
    asyncio.run(ding_push("{'itemId': '629239751120', 'userNick': 'caoniuniu', 'price': '1049.99', 'title': '10台戴尔图形工作站R7610，一块E5-2609CPU，支 持双CPU，8G内存，无硬盘，单电源，机器全部正常工作，剩下最后10台，本地自取！'"))
