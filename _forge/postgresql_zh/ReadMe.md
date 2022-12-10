
安装了后在导出数据库时显示没有权限，需要下面的命令进行授权：

    GRANT USAGE ON SCHEMA public TO <user>;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO <user>;
