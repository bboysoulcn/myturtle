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


class WechatChannel:
    def __init__(self):
        self.wechat_baseurl = os.getenv("WECHAT_BASE_URL",
                                        "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your_key")

    def send_msg(self, slow_log):
        msg = format_message(slow_log)
        headers = {'Content-Type': 'application/json'}
        body = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg
            }
        }
        httpx.post(self.wechat_baseurl, json=body, headers=headers)
