# -*- coding:utf-8 -*-

'''
create a base model class that our application's models will extend. From django
'''
import config
import peewee

class BaseModel(peewee.Model):
    '''
    base model
    '''
    class Meta:
        '''
        meta
        '''
        print('=x' * 20)
        print(config.db_cfg)
        database = config.dbconnect
