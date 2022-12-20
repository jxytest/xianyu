import json

from loguru import logger
import frida


class XianYu:
    def __init__(self, file_path):
        self.sign = None
        self.app_name = "闲鱼"
        self.file_path = file_path
        self.hook_code = self.read_js()
        self.process = frida.get_remote_device().attach(self.app_name)
        self.script = self.process.create_script(self.hook_code)
        self.script.on("message", self.on_message)
        self.script.load()

    def read_js(self):
        """
        读取js文件
        :return:
        """
        with open(self.file_path, encoding='utf-8') as f:
            hook_code = f.read()
        return hook_code

    def get_sign(self, data: dict, t):
        """
        获取sign
        :param data: 请求参数
        :param t: 时间戳
        :return:
        """
        self.script.exports.getSign(json.dumps(data), t)
        return self.sign

    def on_message(self, message, data):
        """
        获取sign
        :param message:
        :param data:
        :return:
        """
        sign = message.get("payload").get("sign")
        self.sign = dict([x.split('=', 1) for x in sign[1:-1].split(", ")])
        logger.info(self.sign)

