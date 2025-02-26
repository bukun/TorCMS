# -*- coding:utf-8 -*-

'''
Testing for redis.
'''

import cfg
from config import REDIS_CFG


class TestRedis:
    '''
    Testing for redis.
    '''

    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')
        self.torcms_redis = REDIS_CFG

    def test_redis(self):
        cfg_var = dir(cfg)
        if 'REDIS_CFG' in cfg_var:
            assert self.torcms_redis['host'] == cfg.REDIS_CFG['host']
            assert self.torcms_redis['port'] == cfg.REDIS_CFG['port']
            assert self.torcms_redis['pass'] == cfg.REDIS_CFG['pass']
        else:
            assert self.torcms_redis['host'] == 'localhost'
            assert self.torcms_redis['port'] == 6379
            assert self.torcms_redis['pass'] == None
