import time
import hmac
import hashlib
import base64
import urllib.parse
import os
import httpx


def format_message(slow_log):
    line = (f"- 🕒 开始时间: {slow_log.start_time}\n"
            f"- 🧑‍💻 用户主机: {slow_log.user_host}\n"
            f"- 🔍 查询时间: {slow_log.query_time}\n"
            f"- 🔒 锁定时间: {slow_log.lock_time}\n"
            f"- 📤 发送行数: {slow_log.rows_sent}\n"
            f"- 🔍 检查行数: {slow_log.rows_examined}\n"
            f"- 📦 数据库: {slow_log.db}\n"
            f"- 📝 sql内容: \n "
            f"> {slow_log.sql_text}")
    return line


class DingdingChannel:
    def __init__(self):
        self.ding_secret = os.getenv("DING_SECRET", "your_secret")
        self.dingding_base_url = os.getenv("DINGDING_BASE_URL",
                                           "https://oapi.dingtalk.com/robot/send?access_token=7aafe515")

    def send_msg(self, slow_log):
        msg = format_message(slow_log)
        timestamp = str(round(time.time() * 1000))
        secret = self.ding_secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        body = {
            "msgtype": "markdown",
            "markdown": {
                "title": "🐢 慢日志来了",
                "text": msg
            }
        }
        dingding_url = self.dingding_base_url + "&timestamp=" + timestamp + "&sign=" + sign
        httpx.post(dingding_url, json=body, headers=headers)
