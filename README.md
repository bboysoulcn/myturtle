### 简介

myturtle 是一个发送mysql慢查询日志到各个IM的工具

### 项目由来

### 目前支持的IM

- 飞书
- 钉钉
- 企业微信

### 使用

首先配置mysql

```ini
slow_query_log = 1 # 开启慢查询日志
slow_query_log_file = /var/lib/mysql/mysql.slow # 慢查询日志文件
long_query_time = 1 # 慢查询阈值
log_output = TABLE # 将慢查询日志写入到表中
```

之后创建mysql用户

```sql
CREATE USER `myturtle`@`%` IDENTIFIED BY 'passwd';
GRANT Select ON `mysql`.* TO `myturtle`@`%`;
```

首先配置你要发送的IM的机器人

- `CHANNEL`: 支持下面几个参数 wechat,dingding,feishu

如果是wechat

- `WECHAT_BASE_URL`: 企业微信机器人的url

如果是dingding

- `DING_SECRET`: 钉钉机器人的secret
- `DINGDING_BASE_URL`: 钉钉机器人的url

如果是feishu

- `FEISHU_BOT_URL`: 飞书机器人的url
- `FEISHU_SIGN`: 飞书机器人的签名

之后配置要监控的数据库

- `DB_HOST`: mysql的地址
- `DB_PASSWORD`: mysql的密码
- `DB_USER`: mysql的用户名
- `DB_PORT`: mysql的端口

之后配置慢查询的阈值

- `QUERY_TIME`: 慢查询的阈值
- `TIME_RANGE`: 查询的时间范围

