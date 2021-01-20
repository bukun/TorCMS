# -*- coding:utf-8 -*-
'''
Using Redis in TorCMS.
'''
import redis

from config import REDIS_CFG

redisvr = redis.Redis(host=REDIS_CFG.get('host'),
                      port=REDIS_CFG.get('port'),
                      db=0,
                      password=REDIS_CFG.get('pass'),
                      socket_timeout=None,
                      connection_pool=None,
                      charset='utf-8',
                      errors='strict',
                      unix_socket_path=None)
