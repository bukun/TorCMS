# -*- coding:utf-8 -*-

'''
Testing for redis.
'''

from config import REDIS_CFG
import cfg


class TestRedis():
    '''
    Testing for redis.
    '''

    def setup(self):
        print('setup 方法执行于本类中每条用例之前')
        self.torcms_redis = REDIS_CFG

    def test_redis(self):
        cfg_var = dir(cfg)
        if 'REDIS_CFG' in cfg_var:
            assert self.torcms_redis['host'] == cfg.REDIS_CFG['host']
        else:
            assert self.torcms_redis['host'] == 'localhost'
