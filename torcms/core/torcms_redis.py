# -*- coding:utf-8 -*-
'''
Using Redis in TorCMS.

redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。
默认，每个Redis实例都会维护一个自己的连接池。
可以直接建立一个连接池，然后作为Redis的参数，这样就可以实现多个Redis实例共享一个连接池。
'''
import redis

from config import REDIS_CFG

redisvr = redis.Redis(
    connection_pool=redis.ConnectionPool(
        host=REDIS_CFG.get('host'),
        port=REDIS_CFG.get('port'),
        # db=0,
        password=REDIS_CFG.get('pass'),
        socket_timeout=None,
        # connection_pool=None,
        encoding='utf-8',
        encoding_errors='strict',
        # unix_socket_path=None
    )
)
