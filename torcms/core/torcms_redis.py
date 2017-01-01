# -*- coding:utf-8 -*-

import redis

redisvr = redis.Redis(host='localhost',
                             port=6379,
                             db=0,
                             password=None,
                             socket_timeout=None,
                             connection_pool=None,
                             charset='utf-8',
                             errors='strict',
                             unix_socket_path=None)
