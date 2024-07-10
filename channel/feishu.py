import httpx
import hashlib
import base64
import hmac
import time
import os


def format_message(slow_log):
    line = (f"🕒 开始时间: {slow_log.start_time}\n"
            f"🧑‍💻 用户主机: {slow_log.user_host}\n"
            f"🔍 查询时间: {slow_log.query_time}\n"
            f"🔒 锁定时间: {slow_log.lock_time}\n"
            f"📤 发送行数: {slow_log.rows_sent}\n"
            f"🔍 检查行数: {slow_log.rows_examined}\n"
            f"📦 数据库: {slow_log.db}\n"
            f"📝 sql内容: \n {slow_log.sql_text}")
    return line


class FeishuChannel:
    def __init__(self):
        self.bot_url = os.getenv("FEISHU_BOT_URL", "https://open.feishu.cn/open-apis/bot/v2/hook/")
        self.sign = os.getenv("FEISHU_SIGN", "your_sign")

    def send_msg(self, slow_log):
        msg = format_message(slow_log)
        timestamp = int(time.time())
        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, self.sign)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        body = {
            "msg_type": "interactive",
            "timestamp": timestamp,
            "sign": sign,
            "card": {
                "elements": [
                    {
                        "tag": "markdown",
                        "content": msg
                    },
                    {
                        "tag": "hr"
                    }
                ],
                "header": {
                    "template": "blue",
                    "title": {
                        "content": "🐢 慢日志来了",
                        "tag": "plain_text"
                    }
                }
            }
        }
        httpx.post(self.bot_url, json=body, headers=headers)
