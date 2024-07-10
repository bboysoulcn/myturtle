mysql 需要配置的参数


CREATE USER `myturtle`@`%` IDENTIFIED BY 'passwd';
GRANT Select ON `mysql`.* TO `myturtle`@`%`;