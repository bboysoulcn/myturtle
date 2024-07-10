import pymysql
import os
from channel.feishu import FeishuChannel
from apscheduler.schedulers.background import BackgroundScheduler
import time


# Define a class to represent a slow log entry
class SlowLog:
    def __init__(self, start_time, user_host, query_time, lock_time, rows_sent, rows_examined, db, last_insert_id,
                 insert_id, server_id, sql_text, thread_id):
        self.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        self.user_host = user_host
        self.query_time = float(query_time.total_seconds())
        self.lock_time = int(lock_time.total_seconds())
        self.rows_sent = rows_sent
        self.rows_examined = rows_examined
        self.db = db
        self.last_insert_id = last_insert_id
        self.insert_id = insert_id
        self.server_id = server_id
        self.sql_text = sql_text.decode('utf-8')
        self.thread_id = thread_id


# Fetch slow logs from MySQL
def fetch_slow_log():
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'passwd'))
    slow_logs = []
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM mysql.slow_log WHERE start_time > DATE_SUB(NOW(), INTERVAL %s SECOND) and query_time > %s"
            cursor.execute(sql, (time_range, query_time))
            results = cursor.fetchall()
            for row in results:
                print(row)
                log_entry = SlowLog(*row)
                slow_logs.append(log_entry)
    except Exception as e:
        print(f"Error fetching slow logs: {e}")
    finally:
        connection.close()
    return slow_logs


def slow_job():
    slow_logs = fetch_slow_log()
    if len(slow_logs) == 0:
        print("No slow logs found")
    else:
        channel = FeishuChannel()
        for slow_log in slow_logs:
            print(slow_log.lock_time)
            channel.send_msg(slow_log)


if __name__ == '__main__':
    time_range = os.getenv('TIME_RANGE', '60')
    query_time = os.getenv('QUERY_TIME', '1')
    scheduler = BackgroundScheduler()
    scheduler.add_job(slow_job, 'interval', seconds=int(time_range))
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
