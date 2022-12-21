import asyncio
import aiohttp
from corpwechatbot import AppMsgSender

from core.config import corp_id, corp_secret, agent_id, ding_webhook, wx_push_open, ding_push_open

try:
    app = AppMsgSender(corpid=corp_id,  # 你的企业id
                       corpsecret=corp_secret,  # 你的应用凭证密钥
                       agentid=agent_id,  # 你的应用id
                       log_level=10)
except Exception as e:
    print(e)
    app = None


async def ding_push(message):
    try:
        if not ding_push_open:
            print("ding_push_open is False")
            return
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
        async with aiohttp.request("POST", url=ding_webhook, headers=headers, json=text) as resp:
            print(resp.status)
            print(await resp.text())
    except Exception as e:
        print(e)
        print("ding_push error")
    finally:
        return 1


async def wx_push(message):
    try:
        if not wx_push_open or not app:
            print("wx_push_open is False")
            return
        app.send_text(message, touser=['lmx'])
    except Exception as e:
        print(e)
        print("wx_push error")
    finally:
        return 1


if __name__ == '__main__':
    asyncio.run(ding_push(
        "{'itemId': '629239751120', 'userNick': 'caoniuniu', 'price': '1049.99', 'title': '10台戴尔图形工作站R7610，一块E5-2609CPU，支 持双CPU，8G内存，无硬盘，单电源，机器全部正常工作，剩下最后10台，本地自取！'"))
    asyncio.run(wx_push("{'itemId':"))